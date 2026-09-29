#!/usr/bin/env python3
"""
hecker2midi.py
Long-window, microtonal audio-to-MIDI for dense, saturated, reverb-heavy ambient material.

Why this exists: note-onset transcribers (Basic Pitch, NeuralNote, Melodyne) look for
attacks and short notes. Hecker-style material has no attacks, sits under broadband noise,
drifts off 12-TET, and is full of distortion partials. This tool instead:

  1. strips transients and glitch noise (harmonic/percussive separation)
  2. analyses a high-resolution constant-Q spectrum (default 20-cent bins)
  3. averages over frequency-dependent windows: long in the bass (where pitch needs time to
     resolve and noise needs averaging), short in the upper register (keeps melodic detail).
     --preset early (default) reads down to 0.1 s up top; --preset late suits slow walls
  4. whitens the broadband noise floor per frame (rain, hiss, crush)
  5. finds fundamentals by harmonic summation with iterative, smoothness-based subtraction
     (so overtones and distortion products are not reported as extra notes)
  6. estimates the piece's own tuning reference (tape-speed / pitch-shift offsets)
  7. tracks sustained pitches into notes, keeping their cents offset and drift

Outputs (next to the input file, or in --out):
  <name>_mpe.mid        exact pitch: one note per MPE channel with pitch bend (cents + drift)
  <name>_quantized.mid  plain 12-TET notes on one channel, relative to the piece's tuning
  <name>_notes.csv      every note: start, end, name, cents offset, drift, level
  <name>_harmony.txt    pitch-class content per segment (the harmonic field over time)
  <name>_resynth.wav    sine resynthesis of the extracted notes, for A/B checking (--render)

Requires: numpy, scipy, librosa, soundfile, mido
  pip install numpy scipy librosa soundfile mido
"""

import argparse
import csv
import math
import os
import sys

import numpy as np
import librosa
import soundfile as sf
import mido
from scipy.ndimage import median_filter, maximum_filter1d, uniform_filter1d

NOTE_NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
HARM_WEIGHTS = np.array([1.0, 0.8, 0.65, 0.55, 0.45, 0.4, 0.35, 0.3, 0.27, 0.24, 0.22, 0.2])


def midi_name(m):
    n = int(round(m))
    return f"{NOTE_NAMES[n % 12]}{n // 12 - 1}"


def parse_args():
    p = argparse.ArgumentParser(description="Long-window microtonal audio-to-MIDI for dense ambient audio.")
    p.add_argument("audio", help="input audio file (wav/flac/aiff/mp3)")
    p.add_argument("--out", help="output folder (default: next to input)")
    p.add_argument("--start", type=float, default=0.0, help="start time in seconds")
    p.add_argument("--duration", type=float, default=None, help="seconds to analyse (default: all)")
    p.add_argument("--sr", type=int, default=22050, help="analysis sample rate")
    p.add_argument("--resolution", type=int, default=5, help="CQT bins per semitone (5 = 20-cent bins)")
    p.add_argument("--lowest", default="C1", help="lowest candidate note")
    p.add_argument("--highest", default="C7", help="highest candidate note")
    p.add_argument("--preset", choices=["early", "late"], default="early",
                   help="early = Haunt Me / Harmony in Ultraviolet era: fast melodic detail (default); "
                        "late = Ravedeath onward: slow dense walls")
    p.add_argument("--hop", type=float, default=None, help="analysis frame hop in seconds")
    p.add_argument("--window", type=float, default=None,
                   help="smoothing window for the bass register (at C2 and below), seconds")
    p.add_argument("--window-min", type=float, default=None,
                   help="shortest smoothing window, used in the upper register, seconds. The window "
                        "shrinks in proportion to frequency between the two (constant-Q), because low "
                        "notes need long windows to be resolved while high notes can be read quickly")
    p.add_argument("--hpss-margin", type=float, default=2.0,
                   help="harmonic/percussive separation margin; 0 disables (default 2.0)")
    p.add_argument("--floor-k", type=float, default=1.5,
                   help="noise-floor subtraction strength (multiples of the local spectral median)")
    p.add_argument("--max-voices", type=int, default=12, help="maximum simultaneous pitches per frame")
    p.add_argument("--rel-thresh", type=float, default=0.12,
                   help="stop adding voices below this fraction of the frame's strongest voice")
    p.add_argument("--abs-thresh", type=float, default=0.03,
                   help="ignore voices below this fraction of the loudest voice in the whole file")
    p.add_argument("--harmonics", type=int, default=8, help="harmonics used for salience (max 8)")
    p.add_argument("--fund-ratio", type=float, default=0.25,
                   help="a candidate's fundamental must be at least this fraction of its strongest "
                        "upper harmonic (suppresses octave-down errors); 0 disables")
    p.add_argument("--prune-margin", type=float, default=2.0,
                   help="drop a note unless its fundamental carries more than this multiple of the "
                        "energy that lower notes' overtones predict there; 0 disables")
    p.add_argument("--min-support", type=float, default=0.1,
                   help="quiet notes need 2nd-4th harmonics of at least this fraction of the "
                        "fundamental; lone sine-like partials (aliasing, intermodulation) are dropped")
    p.add_argument("--support-db", type=float, default=-15.0,
                   help="the harmonic-support rule applies only to notes quieter than this (dB)")
    p.add_argument("--attack-db", type=float, default=0.0,
                   help="attack-gated melody rescue: recover melody notes hidden on chord overtones "
                        "when their fundamental and a harmonic rise by this many dB within 100 ms "
                        "(try 6). Off by default: it recovers melody but adds some octave errors")
    p.add_argument("--attack-lowest", default="C4", help="lowest pitch considered by the attack pass")
    p.add_argument("--keep-difference-tones", action="store_true",
                   help="keep notes identified as distortion difference tones in the MIDI files")
    p.add_argument("--link-cents", type=float, default=50.0, help="max pitch jump to continue a note")
    p.add_argument("--gap", type=float, default=None, help="max silence inside one note (seconds)")
    p.add_argument("--merge-gap", type=float, default=None,
                   help="join same-pitch fragments separated by up to this many seconds")
    p.add_argument("--min-dur", type=float, default=None,
                   help="shortest note kept in the upper register (seconds); low notes must also last "
                        "at least 0.8 x their smoothing window")
    p.add_argument("--no-retune", action="store_true",
                   help="do not estimate the piece's own tuning reference")
    p.add_argument("--bend-range", type=int, default=48, help="pitch-bend range in semitones (MPE default 48)")
    p.add_argument("--segment", type=float, default=10.0, help="segment length for harmony report (s)")
    p.add_argument("--render", action="store_true", help="write a sine resynthesis WAV for A/B checking")
    a = p.parse_args()
    presets = {
        #        hop   window window_min gap  merge_gap min_dur
        "early": (0.05, 1.0, 0.1, 0.2, 0.3, 0.25),
        "late": (0.1, 2.0, 0.5, 0.5, 2.0, 1.5),
    }
    for name, val in zip(("hop", "window", "window_min", "gap", "merge_gap", "min_dur"), presets[a.preset]):
        if getattr(a, name) is None:
            setattr(a, name, val)
    a.window_min = min(a.window_min, a.window)
    return a


def window_at(a, midi):
    """Smoothing window (s) for a pitch: a.window at C2 and below, shrinking in proportion
    to frequency above that, never shorter than a.window_min."""
    f = 440.0 * 2 ** ((midi - 69) / 12.0)
    return float(np.clip(a.window * 65.41 / f, a.window_min, a.window))


# ---------------------------------------------------------------- analysis

def load_audio(a):
    y, sr = librosa.load(a.audio, sr=a.sr, mono=True, offset=a.start, duration=a.duration)
    if y.size == 0:
        sys.exit("No audio loaded.")
    peak = np.max(np.abs(y))
    if peak > 0:
        y = y / peak
    return y, sr


def spectrum(y, sr, a):
    if a.hpss_margin > 0:
        y = librosa.effects.harmonic(y, margin=a.hpss_margin)
    bpo = 12 * a.resolution
    fmin = librosa.note_to_hz("C1")
    # as many octaves as fit under Nyquist
    n_oct = int(math.floor(math.log2((sr / 2.0) / fmin) - 0.05))
    n_bins = bpo * n_oct
    hop = 256
    C = np.abs(librosa.cqt(y, sr=sr, hop_length=hop, fmin=fmin, n_bins=n_bins, bins_per_octave=bpo))
    # aggregate into analysis frames
    k = max(1, int(round(a.hop * sr / hop)))
    n_frames = C.shape[1] // k
    C = C[:, : n_frames * k].reshape(C.shape[0], n_frames, k).mean(axis=2)
    frame_hop = k * hop / sr
    # frequency-dependent temporal smoothing: long in the bass (needed to resolve low pitches and
    # reject noise there), short in the upper register (keeps fast melodic detail)
    midi_fmin = librosa.hz_to_midi(fmin)
    a._raw = C.copy()  # unsmoothed (hop-averaged) magnitudes, used for onset evidence
    a._frame_hop = frame_hop
    a._midi_fmin = midi_fmin
    for b in range(C.shape[0]):
        win = max(1, int(round(window_at(a, midi_fmin + b / a.resolution) / frame_hop)))
        if win > 1:
            C[b] = uniform_filter1d(C[b], size=win, mode="nearest")
    # whiten broadband noise floor: subtract a local median across frequency (half-octave each side)
    width = bpo + 1
    floor = median_filter(C, size=(width, 1), mode="nearest")
    X = np.maximum(C - a.floor_k * floor, 0.0)
    a._X = X
    return X, frame_hop, fmin, bpo


def harmonic_offsets(bpo, H):
    return [bpo * math.log2(h) for h in range(1, H + 1)]


def salience(Xmax, offs, weights, lo, hi, fund_ratio=0.0):
    """Harmonic-sum salience for candidate bins lo..hi. Candidates whose own fundamental is
    weak relative to their upper harmonics are suppressed (prevents 'virtual fundamental'
    octave-down errors, where a chord such as Bb2+F3+Bb3 reads as a Bb1 harmonic series)."""
    n = Xmax.shape[0]
    s = np.zeros(hi - lo)
    hmax = np.zeros(hi - lo)
    idx = np.arange(lo, hi)
    for k, (off, w) in enumerate(zip(offs, weights)):
        j = idx + int(round(off))
        valid = j < n
        v = np.zeros(hi - lo)
        v[valid] = Xmax[j[valid]]
        s += w * v
        if k > 0:
            hmax = np.maximum(hmax, v)
    if fund_ratio > 0:
        s[Xmax[idx] < fund_ratio * hmax] = 0.0
    return s


def refine_peak(x, b, tol):
    """Return fractional bin of the local peak of x near b (parabolic interpolation on log magnitude)."""
    n = x.shape[0]
    lo, hi = max(1, b - tol), min(n - 2, b + tol)
    if hi < lo:
        return float(b), 0.0
    seg = x[lo : hi + 1]
    pk = lo + int(np.argmax(seg))
    amp = x[pk]
    if amp <= 0:
        return float(b), 0.0
    eps = 1e-12
    la, lb, lc = math.log(x[pk - 1] + eps), math.log(x[pk] + eps), math.log(x[pk + 1] + eps)
    den = la - 2 * lb + lc
    d = 0.5 * (la - lc) / den if den < 0 else 0.0
    d = max(-0.5, min(0.5, d))
    return pk + d, amp


def estimate_frame(x, offs, weights, lo, hi, tol, bpo, max_voices, rel, abs_level, fund_ratio):
    """Iterative multi-pitch estimate for one frame. Returns list of (fractional_bin, amplitude)."""
    x = x.copy()
    n = x.shape[0]
    found = []
    first = None
    H = len(offs)
    for _ in range(max_voices):
        xmax = maximum_filter1d(x, size=2 * tol + 1)
        s = salience(xmax, offs, weights, lo, hi, fund_ratio)
        i = int(np.argmax(s))
        sv = s[i]
        if first is None:
            first = sv
        if sv <= 0 or sv < rel * first or sv < abs_level:
            break
        b = lo + i
        fb, famp = refine_peak(x, b, tol)
        # harmonic amplitudes at ideal positions
        amps = []
        for off in offs:
            j = int(round(fb + off))
            if j >= n:
                amps.append(0.0)
                continue
            amps.append(float(xmax[j]))
        amps = np.array(amps)
        if famp < 0.1 * max(amps.max(), 1e-12) and amps[1] > 0:
            # weak or missing fundamental: locate via 2nd harmonic
            fb2, _ = refine_peak(x, int(round(b + offs[1])), tol)
            fb = fb2 - offs[1]
        found.append((fb, float(amps.sum())))
        # smoothness-based subtraction (Klapuri-style): remove only the smooth part of each
        # harmonic so a genuinely separate note sharing that harmonic keeps its residual
        # smooth envelope from the neighbouring harmonics only, so a harmonic that sticks out
        # above its neighbours (because another note sits there) keeps the excess
        # Saturated tones (tanh, clipping, square-ish) have strong odd and weak even harmonics,
        # so the envelope is also estimated from same-parity neighbours (h-2, h+2) and the
        # larger of the two estimates is used. Without this, odd harmonics of saturated notes
        # are under-subtracted and reappear as false notes an octave-plus-fifth up.
        sm = amps.copy()
        for h in range(1, H):
            adj = [amps[k] for k in (h - 1, h + 1) if 0 <= k < H]
            par = [amps[k] for k in (h - 2, h + 2) if 0 <= k < H]
            est = max(float(np.mean(adj)), float(np.mean(par)) if par else 0.0)
            sm[h] = min(amps[h], est)
        sm[0] = amps[0]  # the fundamental itself is removed fully
        for off, a_h in zip(offs, sm):
            j = int(round(fb + off))
            if j >= n or a_h <= 0:
                continue
            r0, r1 = max(0, j - tol - 1), min(n, j + tol + 2)
            x[r0:r1] = np.maximum(x[r0:r1] - a_h, 0.0)
    return found


def analyse(X, frame_hop, fmin, bpo, a):
    tol = max(1, a.resolution // 2)
    H = max(2, min(a.harmonics, len(HARM_WEIGHTS)))
    offs = harmonic_offsets(bpo, H)
    weights = HARM_WEIGHTS[:H]
    midi_fmin = librosa.hz_to_midi(fmin)
    lo = max(0, int(round((librosa.note_to_midi(a.lowest) - midi_fmin) * a.resolution)))
    hi = min(X.shape[0], int(round((librosa.note_to_midi(a.highest) - midi_fmin) * a.resolution)) + 1)
    # global level reference: strongest first-voice salience in the file
    Xmax_all = maximum_filter1d(X, size=2 * tol + 1, axis=0)
    gmax = 0.0
    for t in range(X.shape[1]):
        gmax = max(gmax, float(salience(Xmax_all[:, t], offs, weights, lo, hi, a.fund_ratio).max()))
    abs_level = a.abs_thresh * gmax
    frames = []
    for t in range(X.shape[1]):
        det = estimate_frame(X[:, t], offs, weights, lo, hi, tol, bpo, a.max_voices, a.rel_thresh,
                             abs_level, a.fund_ratio)
        frames.append([(midi_fmin + fb / a.resolution, amp) for fb, amp in det])
    return frames


def estimate_tuning(frames):
    """Circular mean of deviations from 12-TET, amplitude weighted. Returns offset in semitones."""
    num = 0j
    for fr in frames:
        for m, amp in fr:
            num += amp * np.exp(2j * np.pi * (m - round(m)))
    if abs(num) == 0:
        return 0.0
    return float(np.angle(num) / (2 * np.pi))


def track(frames, frame_hop, a):
    link = a.link_cents / 100.0
    gap_frames = max(1, int(round(a.gap / frame_hop)))
    active, done = [], []
    for t, det in enumerate(frames):
        det = sorted(det, key=lambda d: -d[1])
        used = set()
        for m, amp in det:
            best, bd = None, None
            for k, tr in enumerate(active):
                if k in used:
                    continue
                d = abs(tr["pts"][-1][1] - m)
                if d <= link and (bd is None or d < bd):
                    best, bd = k, d
            if best is None:
                active.append({"pts": [(t, m, amp)]})
                used.add(len(active) - 1)
            else:
                active[best]["pts"].append((t, m, amp))
                used.add(best)
        still = []
        for tr in active:
            if t - tr["pts"][-1][0] > gap_frames:
                done.append(tr)
            else:
                still.append(tr)
        active = still
    done.extend(active)
    # merge fragments of the same pitch separated by short dropouts (sustained tones that dip
    # under the threshold for a moment inside a dense texture)
    segs = sorted((np.array(tr["pts"]) for tr in done), key=lambda p: p[0, 0])
    merge_frames = a.merge_gap / frame_hop
    merged = []
    for p in segs:
        pm = float(np.average(p[:, 1], weights=p[:, 2]))
        for q in reversed(merged):
            qm = float(np.average(q["pts"][:, 1], weights=q["pts"][:, 2]))
            gap = p[0, 0] - q["pts"][-1, 0]
            if abs(pm - qm) <= 0.3 and 0 < gap <= merge_frames:
                q["pts"] = np.vstack([q["pts"], p])
                break
        else:
            merged.append({"pts": p})
    notes = []
    for tr in merged:
        pts = tr["pts"]
        t0, t1 = pts[0, 0] * frame_hop, (pts[-1, 0] + 1) * frame_hop
        w = pts[:, 2]
        pitch = float(np.sum(pts[:, 1] * w) / np.sum(w))
        if t1 - t0 < max(a.min_dur, 0.8 * window_at(a, pitch)):
            continue
        notes.append({
            "start": t0, "end": t1, "pitch": pitch,
            "drift": float(np.sqrt(np.sum(w * (pts[:, 1] - pitch) ** 2) / np.sum(w)) * 100.0),
            "amp": float(w.max()),
            "curve": [(p[0] * frame_hop, p[1]) for p in pts],
            "env": {int(p[0]): float(p[2]) for p in pts},
        })
    notes.sort(key=lambda n: (n["start"], n["pitch"]))
    return notes


def _smooth_at(env, i):
    """Envelope estimate at harmonic index i from its neighbours (adjacent or same parity),
    excluding the harmonic itself."""
    H = len(env)
    adj = [env[k] for k in (i - 1, i + 1) if 0 <= k < H]
    par = [env[k] for k in (i - 2, i + 2) if 0 <= k < H]
    return max(float(np.mean(adj)) if adj else 0.0, float(np.mean(par)) if par else 0.0)


def prune(notes, a, offset):
    """Note-level distillation. Each note's harmonic envelope is measured over its whole
    duration (median, so momentary fluctuations don't count). A note is dropped when the
    energy at its own fundamental is no more than a.prune_margin times what the overtones of
    lower, overlapping, already-kept notes predict there. Genuine doublings carry clearly
    more energy than an overtone would and survive; overtones and distortion partials that
    only crossed the threshold now and then do not."""
    if a.prune_margin <= 0 or not notes:
        return notes
    X, fh, res = a._X, a._frame_hop, a.resolution
    bpo = 12 * res
    nb = X.shape[0]
    H = max(2, min(a.harmonics, len(HARM_WEIGHTS)))
    tol = max(1, res // 2)
    Xmax = maximum_filter1d(X, size=2 * tol + 1, axis=0)
    for n in notes:
        t0 = int(n["start"] / fh)
        t1 = max(t0 + 1, int(n["end"] / fh))
        fb = (n["pitch"] - a._midi_fmin) * res
        env = []
        for k in range(1, H + 1):
            j = int(round(fb + bpo * math.log2(k)))
            env.append(float(np.median(Xmax[j, t0:t1])) if 0 <= j < nb else 0.0)
        n["henv"] = np.array(env)
        n["pruned"] = False
    # lone-partial filter: a quiet "note" with no harmonics of its own is an aliased or
    # intermodulation partial (sample-rate reduction folds partials into inharmonic sine
    # components), not a played note
    for n in notes:
        e = n["henv"]
        support = float(e[1:4].max() / (e[0] + 1e-12)) if len(e) > 3 else 1.0
        n["support"] = support
        if support < a.min_support and n.get("db", 0.0) < a.support_db:
            n["pruned"] = True
    for n in sorted(notes, key=lambda n: n["pitch"]):
        if n["pruned"]:
            continue
        obs = n["henv"][0]
        dur = n["end"] - n["start"]
        pred = 0.0
        for p in notes:
            if p is n or p["pruned"] or p["pitch"] >= n["pitch"] - 0.5:
                continue
            ov = min(n["end"], p["end"]) - max(n["start"], p["start"])
            if ov <= 0.5 * dur:
                continue
            d = n["pitch"] - p["pitch"]
            k = int(round(2 ** (d / 12.0)))
            if 2 <= k <= H and abs(12 * math.log2(k) - d) < 0.35:
                pred += _smooth_at(p["henv"], k - 1) * min(1.0, ov / dur)
        n["pred"] = pred
        if pred > 0 and obs <= a.prune_margin * pred:
            n["pruned"] = True
    return notes


def rescue_attacks(notes, a):
    """Attack-gated melody pass. Sustained chord partials have no spectral flux; a new melodic
    note does. At each onset in the upper register, the pitch whose whole harmonic series
    rises together is taken as a new note if the main pass suppressed it (typically because it
    sits on an overtone of a held chord tone, as consonant melodies over drones usually do)."""
    if a.attack_db <= 0:
        return notes
    R, fh, res = a._raw, a._frame_hop, a.resolution
    bpo = 12 * res
    nb, nt = R.shape
    tol = max(1, res // 2)
    H = max(2, min(a.harmonics, len(HARM_WEIGHTS)))
    offs = harmonic_offsets(bpo, H)
    weights = HARM_WEIGHTS[:H]
    lag = max(1, int(round(0.1 / fh)))
    Rdb = 20 * np.log10(R + 1e-9)
    lo = max(0, int(round((librosa.note_to_midi(a.attack_lowest) - a._midi_fmin) * res)))
    hi = min(nb, int(round((librosa.note_to_midi(a.highest) - a._midi_fmin) * res)) + 1)
    # flux: positive dB change at each bin versus 100 ms earlier (only where there is energy)
    flux = np.zeros_like(R)
    flux[:, lag:] = np.maximum(Rdb[:, lag:] - Rdb[:, :-lag], 0.0)
    gate = R > (0.02 * R.max())
    flux *= gate
    total = flux[lo:hi].sum(axis=0)
    thr = np.median(total) + 3 * np.median(np.abs(total - np.median(total)))
    added = []
    for t in range(lag + 1, nt - 1):
        if not (total[t] > thr and total[t] >= total[t - 1] and total[t] > total[t + 1]):
            continue
        fx = maximum_filter1d(flux[:, t], size=2 * tol + 1)
        # salience of the flux spectrum: which pitch's harmonics all rose at once
        s = np.zeros(hi - lo)
        idx = np.arange(lo, hi)
        cnt = np.zeros(hi - lo)
        for k, (off, w) in enumerate(zip(offs[:4], weights[:4])):
            j = idx + int(round(off))
            v = np.zeros(hi - lo)
            ok = j < nb
            v[ok] = fx[j[ok]]
            s += w * v
            cnt += v >= a.attack_db
        s[fx[idx] < a.attack_db] = 0.0      # the fundamental itself must rise
        s[cnt < 2] = 0.0                    # and at least one harmonic with it
        i = int(np.argmax(s))
        if s[i] <= 0:
            continue
        b = lo + i
        fb, _ = refine_peak(R[:, min(nt - 1, t + lag)], b, tol)
        pitch = a._midi_fmin + fb / res
        t0 = t * fh
        # already covered by an existing note of this pitch?
        if any(abs(n["pitch"] - pitch) < 0.4 and n["start"] - 0.3 <= t0 <= n["end"] for n in notes + added):
            continue
        # skip overtones of a louder note that starts at the same moment (chord onset)
        clash = False
        for n in notes:
            if abs(n["start"] - t0) <= 0.2 and n["pitch"] < pitch - 0.5:
                d = pitch - n["pitch"]
                k = int(round(2 ** (d / 12.0)))
                if 2 <= k <= 8 and abs(12 * math.log2(k) - d) < 0.35:
                    clash = True
                    break
        if clash:
            continue
        # sustain: until the fundamental falls 12 dB below its post-onset peak (max 4 s)
        jb = int(round(fb))
        seg = Rdb[max(0, jb - tol): jb + tol + 1, t: min(nt, t + int(4 / fh))].max(axis=0)
        if seg.size < 2:
            continue
        pk = seg[: max(2, int(0.3 / fh))].max()
        below = np.where(seg < pk - 12)[0]
        t_end = t + (below[0] if below.size else seg.size)
        if (t_end - t) * fh < a.min_dur:
            continue
        added.append({
            "start": t0, "end": t_end * fh, "pitch": pitch, "drift": 0.0,
            "amp": float(R[jb, min(nt - 1, t + lag)]),
            "curve": [(t0, pitch), (t_end * fh, pitch)], "env": {}, "attack": True,
        })
    if added:
        ref = max(n["amp"] for n in notes) if notes else 1.0
        # express rescued levels on the same scale as the main pass (approximate)
        scale = ref / max(float(R.max()), 1e-12)
        for n in added:
            n["amp"] *= scale
    return sorted(notes + added, key=lambda n: (n["start"], n["pitch"]))


def flag_difference_tones(notes, tol_cents=30.0):
    """Mark notes that sit at the frequency difference of two louder, overlapping notes.
    Saturation creates these intermodulation tones; they are real in the audio but are
    regenerated automatically when the played notes are distorted again, so they are
    excluded from the MIDI by default and listed separately."""
    hz = lambda m: 440.0 * 2 ** ((m - 69) / 12.0)
    for n in notes:
        n["diff"] = None
        fn = hz(n["pitch"])
        dur = n["end"] - n["start"]
        for i, p in enumerate(notes):
            if p is n:
                continue
            for q in notes[i + 1 :]:
                if q is n or q is p:
                    continue
                ov = min(n["end"], p["end"], q["end"]) - max(n["start"], p["start"], q["start"])
                if ov < 0.5 * dur:
                    continue
                d = abs(hz(q["pitch"]) - hz(p["pitch"]))
                if d <= 0:
                    continue
                if abs(1200 * math.log2(fn / d)) <= tol_cents and n["amp"] < max(p["amp"], q["amp"]):
                    n["diff"] = (p, q)
                    break
            if n["diff"]:
                break


# ---------------------------------------------------------------- output

def velocities(notes):
    if not notes:
        return
    ref = max(n["amp"] for n in notes)
    for n in notes:
        db = 20 * math.log10(max(n["amp"], 1e-12) / ref)
        n["db"] = db
        n["vel"] = int(np.clip(115 + 1.6 * db, 20, 127))


def write_mpe(notes, path, a):
    tpb = 480  # 60 BPM: 480 ticks = 1 second
    mid = mido.MidiFile(ticks_per_beat=tpb)
    tr = mido.MidiTrack()
    mid.tracks.append(tr)
    tr.append(mido.MetaMessage("set_tempo", tempo=1_000_000, time=0))
    tr.append(mido.MetaMessage("track_name", name="hecker2midi MPE", time=0))
    ev = []
    # MPE configuration: lower zone, master ch 1, 15 member channels
    for cc, v in ((101, 0), (100, 6), (6, 15)):
        ev.append((0, 0, mido.Message("control_change", channel=0, control=cc, value=v)))
    for ch in range(1, 16):
        for cc, v in ((101, 0), (100, 0), (6, a.bend_range), (38, 0)):
            ev.append((0, 1, mido.Message("control_change", channel=ch, control=cc, value=v)))
    free_at = {ch: -1.0 for ch in range(1, 16)}
    scale = 8192 / (a.bend_range * 100.0)  # units per cent
    for n in notes:
        ch = min(free_at, key=lambda c: free_at[c])
        if free_at[ch] > n["start"]:
            # more than 15 overlapping notes: steal the channel that frees soonest
            pass
        free_at[ch] = n["end"] + 0.01
        key = int(round(n["pitch"]))
        key = max(0, min(127, key))

        def bend_val(m):
            cents = (m - key) * 100.0
            return int(np.clip(round(cents * scale), -8192, 8191))

        ev.append((n["start"], 2, mido.Message("pitchwheel", channel=ch, pitch=bend_val(n["pitch"]))))
        ev.append((n["start"], 3, mido.Message("note_on", channel=ch, note=key, velocity=n["vel"])))
        last = bend_val(n["pitch"])
        for t, m in n["curve"][1:]:
            if t >= n["end"]:
                break
            v = bend_val(m)
            if abs(v - last) >= 3 * scale:  # update on changes of 3 cents or more
                ev.append((t, 4, mido.Message("pitchwheel", channel=ch, pitch=v)))
                last = v
        ev.append((n["end"], 1, mido.Message("note_off", channel=ch, note=key, velocity=0)))
    write_events(tr, ev, tpb)
    mid.save(path)


def write_quantized(notes, path, offset):
    tpb = 480
    mid = mido.MidiFile(ticks_per_beat=tpb)
    tr = mido.MidiTrack()
    mid.tracks.append(tr)
    tr.append(mido.MetaMessage("set_tempo", tempo=1_000_000, time=0))
    tr.append(mido.MetaMessage("track_name", name="hecker2midi quantized", time=0))
    ev, sounding = [], {}
    for n in notes:
        key = max(0, min(127, int(round(n["pitch"] - offset))))
        ev.append((n["start"], 3, mido.Message("note_on", channel=0, note=key, velocity=n["vel"])))
        ev.append((n["end"], 1, mido.Message("note_off", channel=0, note=key, velocity=0)))
    write_events(tr, ev, tpb)
    mid.save(path)


def write_events(tr, ev, tpb):
    ev.sort(key=lambda e: (e[0], e[1]))
    now = 0
    for t, _, msg in ev:
        tick = int(round(t * tpb))
        msg.time = max(0, tick - now)
        now = max(now, tick)
        tr.append(msg)
    tr.append(mido.MetaMessage("end_of_track", time=0))


def write_csv(notes, path, offset):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["start_s", "end_s", "note", "midi_exact", "cents_vs_440", "note_in_piece_tuning",
                    "cents_vs_piece_tuning", "drift_cents_rms", "level_db", "velocity",
                    "source", "difference_tone", "difference_of", "rejected_as"])
        for n in notes:
            k = int(round(n["pitch"]))
            kp = int(round(n["pitch"] - offset))
            dt = n.get("diff")
            src = f"{midi_name(dt[1]['pitch'])}-{midi_name(dt[0]['pitch'])}" if dt else ""
            w.writerow([f"{n['start']:.2f}", f"{n['end']:.2f}", midi_name(k), f"{n['pitch']:.3f}",
                        f"{(n['pitch'] - k) * 100:+.1f}", midi_name(kp),
                        f"{(n['pitch'] - offset - kp) * 100:+.1f}", f"{n['drift']:.1f}",
                        f"{n.get('db', 0.0):.1f}", n.get("vel", 0), "attack" if n.get("attack") else "sustain",
                        "yes" if dt else "", src, n.get("reason", "") if n.get("pruned") or dt else ""])


def write_harmony(notes, path, offset, total, a):
    lines = []
    ref_a = 440.0 * 2 ** (offset / 12.0)
    lines.append(f"Estimated tuning offset: {offset * 100:+.1f} cents (A4 = {ref_a:.2f} Hz)")
    lines.append(f"Notes kept: {len(notes)}")
    lines.append("")

    def pcs(t0, t1):
        wts = np.zeros(12)
        bass = None
        for n in notes:
            ov = min(t1, n["end"]) - max(t0, n["start"])
            if ov <= 0:
                continue
            kp = int(round(n["pitch"] - offset))
            wts[kp % 12] += ov * n["amp"]
            if bass is None or kp < bass:
                bass = kp
        return wts, bass

    wts, _ = pcs(0, total)
    order = np.argsort(-wts)
    tot = wts.sum() or 1.0
    lines.append("Whole-file pitch-class weight (duration x level):")
    for i in order:
        if wts[i] > 0:
            lines.append(f"  {NOTE_NAMES[i]:>2}  {100 * wts[i] / tot:5.1f}%")
    lines.append("")
    lines.append(f"Harmonic field per {a.segment:.0f} s segment (strongest first; pitch classes above 5%):")
    t = 0.0
    while t < total:
        t1 = min(total, t + a.segment)
        w, bass = pcs(t, t1)
        s = w.sum()
        if s > 0:
            pcs_on = [NOTE_NAMES[i] for i in np.argsort(-w) if w[i] / s >= 0.05]
            lines.append(f"  {a.start + t:7.1f}-{a.start + t1:7.1f} s  bass {midi_name(bass) if bass is not None else '-':>4}  "
                         f"field: {' '.join(pcs_on)}")
        else:
            lines.append(f"  {a.start + t:7.1f}-{a.start + t1:7.1f} s  (no sustained pitch)")
        t = t1
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return lines


def render(notes, path, total, sr=44100):
    out = np.zeros(int(total * sr) + sr)
    for n in notes:
        ts = np.array([c[0] for c in n["curve"]])
        ms = np.array([c[1] for c in n["curve"]])
        i0, i1 = int(n["start"] * sr), int(n["end"] * sr)
        tt = np.arange(i0, i1) / sr
        m = np.interp(tt, ts, ms)
        f = 440.0 * 2 ** ((m - 69) / 12.0)
        ph = 2 * np.pi * np.cumsum(f) / sr
        sig = np.sin(ph) + 0.35 * np.sin(2 * ph) + 0.15 * np.sin(3 * ph)
        env = np.ones_like(tt)
        fade = min(int(0.3 * sr), len(env) // 2)
        if fade > 0:
            env[:fade] = np.linspace(0, 1, fade)
            env[-fade:] = np.linspace(1, 0, fade)
        amp = 10 ** (n["db"] / 20.0)
        out[i0:i1] += 0.2 * amp * env * sig
    peak = np.max(np.abs(out)) or 1.0
    sf.write(path, (0.8 * out / peak).astype(np.float32), sr)


def process(a, log=print):
    """Full pipeline. Returns (played, rejected, offset, total_seconds)."""
    y, sr = load_audio(a)
    total = len(y) / sr
    log(f"  {total:.1f} s at {sr} Hz. Building {12 * a.resolution}-bin/octave spectrum ...")
    X, frame_hop, fmin, bpo = spectrum(y, sr, a)
    log(f"  {X.shape[1]} frames. Estimating pitches ...")
    frames = analyse(X, frame_hop, fmin, bpo, a)
    offset = 0.0 if a.no_retune else estimate_tuning(frames)
    log(f"  Tuning offset: {offset * 100:+.1f} cents")
    notes = track(frames, frame_hop, a)
    velocities(notes)
    notes = prune(notes, a, offset)
    rejected = [n for n in notes if n.get("pruned")]
    for n in rejected:
        n["reason"] = "lone partial" if n.get("support", 1.0) < a.min_support else "overtone"
    kept = [n for n in notes if not n.get("pruned")]
    kept = rescue_attacks(kept, a)
    velocities(kept)
    flag_difference_tones(kept)
    for n in kept:
        if n.get("diff"):
            n["reason"] = "difference tone"
    played = kept if a.keep_difference_tones else [n for n in kept if not n["diff"]]
    rejected += [n for n in kept if n.get("diff") and not a.keep_difference_tones]
    n_att = sum(1 for n in played if n.get("attack"))
    log(f"  {len(played)} notes kept ({n_att} from the attack pass); {len(rejected)} distilled out "
        f"({sum(1 for n in rejected if n['reason'] == 'overtone')} overtones, "
        f"{sum(1 for n in rejected if n['reason'] == 'lone partial')} lone partials, "
        f"{sum(1 for n in rejected if n['reason'] == 'difference tone')} difference tones).")
    return played, rejected, offset, total


def main():
    a = parse_args()
    base = os.path.splitext(os.path.basename(a.audio))[0]
    outdir = a.out or os.path.dirname(os.path.abspath(a.audio))
    os.makedirs(outdir, exist_ok=True)
    stem = os.path.join(outdir, base)

    print(f"Loading {a.audio} ...")
    played, rejected, offset, total = process(a)

    write_mpe(played, stem + "_mpe.mid", a)
    write_quantized(played, stem + "_quantized.mid", offset)
    write_csv(played, stem + "_notes.csv", offset)
    write_csv(rejected, stem + "_rejected.csv", offset)
    lines = write_harmony(played, stem + "_harmony.txt", offset, total, a)
    if a.render:
        render(played, stem + "_resynth.wav", total)
    print("\n".join(lines[:3]))
    print(f"Wrote {stem}_mpe.mid, _quantized.mid, _notes.csv, _rejected.csv, _harmony.txt"
          + (", _resynth.wav" if a.render else ""))


if __name__ == "__main__":
    main()
