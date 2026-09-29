# hecker2midi

A microtonal audio-to-MIDI extractor for dense, saturated, reverb-heavy ambient audio: the material that note-based transcribers can't read. It favors precision. A note is only written to MIDI when the audio can't be explained without it.

## Install (Windows)

```
pip install numpy scipy librosa soundfile mido
```

The first run takes 20 to 30 seconds longer than later runs because librosa compiles itself. After that, a 10-minute track takes about 1 to 2 minutes.

## Run

```
python hecker2midi.py "excerpt.wav" --render
```

All output files are written next to the input unless you pass `--out folder`.

| File | What it is |
|---|---|
| `_mpe.mid` | Exact pitch. Each note has its own MIDI channel, with pitch bend carrying its cents offset and drift (MPE, ±48 semitone bend range). Load it into Surge XT or Vital with MPE switched on. |
| `_quantized.mid` | Plain 12-TET notes on one channel, relative to the piece's own tuning. Use this for reading and editing. |
| `_notes.csv` | Every kept note: start and end time, note name, cents against A440, cents against the piece's tuning, drift, level. |
| `_rejected.csv` | Every pitch that was distilled out, with the reason: overtone, lone partial or difference tone. Check it if something you can hear is missing. |
| `_harmony.txt` | The piece's tuning reference, a whole-file pitch-class ranking, and the harmonic field (bass note plus pitch classes) for each segment. |
| `_resynth.wav` | Sine resynthesis of the kept notes. Put it on a track under the original in REAPER and A/B them. |

## Presets

The averaging window depends on register. Low notes need a long window, because resolving a 20-cent difference at 40 Hz physically takes over a second of signal. High notes can be read in a tenth of a second.

| Preset | Bass window | Shortest window | Min note | Use for |
|---|---|---|---|---|
| `--preset early` (default) | 1.0 s | 0.1 s | 0.25 s | *Haunt Me*, *Radio Amor*, *Harmony in Ultraviolet*: melodic lines, faster chord changes, stutter |
| `--preset late` | 2.0 s | 0.5 s | 1.5 s | *Ravedeath* onward: slow, dense organ walls |

## Distillation controls

| Goal | Setting |
|---|---|
| Even fewer notes (stricter) | `--prune-margin 3` |
| More inner voices (looser) | `--prune-margin 1 --rel-thresh 0.08` |
| Recover a melody hidden on chord overtones | `--attack-db 6` (adds some octave errors; see the results below) |
| Keep quiet sine-like tones (for example a glassy synth) | `--min-support 0` |
| Keep distortion difference tones | `--keep-difference-tones` |
| A specific passage | `--start 95 --duration 40` |
| Very low drones | `--lowest A0` |

## How it works

1. **Transients removed.** Harmonic/percussive separation takes out glitches and crackle.
2. **High-resolution spectrum.** 60 bins per octave (20-cent bins), with interpolation to locate each peak more precisely.
3. **Register-dependent averaging.** Long windows in the bass, short ones in the upper register.
4. **Noise floor whitened.** Rain, hiss and crush are estimated from the surrounding frequencies and subtracted.
5. **Fundamentals, not overtones.** Candidates are scored by summing their harmonics, and each one must have a real fundamental. After each note is found, its harmonic envelope is subtracted. The envelope is estimated from both adjacent and same-parity harmonics, because saturated tones have strong odd and weak even harmonics.
6. **Note-level overtone pruning.** Each note's harmonic envelope is measured over its whole duration. A note is dropped when its fundamental carries no more than 2x the energy that lower notes' overtones predict there. Real doublings carry clearly more than that and survive.
7. **Lone-partial filter.** A quiet "note" with no harmonics of its own is an aliased or intermodulation partial, not a played note, so it is dropped.
8. **Difference tones flagged.** A low pitch at the frequency gap between two louder notes is a distortion byproduct.
9. **Tuning estimated.** The piece's own reference pitch is found, so tape-speed or pitch-shift offsets don't flip notes to the wrong name.
10. **Notes tracked.** Each note keeps its cents offset and its drift over time.

## Test results

The tests used three synthetic files with a known score:
- **Slow:** late-era walls with a semitone cluster, detuned voices and a 30-cent-flat tuning, plus saturation, 8-bit crush, a sample-rate reduction to 8810 Hz, reverb, rain noise and glitches.
- **Fast:** early-era material with a chord every 3 seconds, a 31-note pentatonic melody played on the chords' own overtones, stutters and aliasing.
- **Third file:** a different instrument model and processing chain, built before the new rules. It has piano-like chords, a melody inside the chord register, tape wobble, chorus detune, long reverb, crackle and hiss. It was scored alongside the other two while the rules were developed, so it is a cross-check, not a strict held-out test.

| Version | False notes (all 3 files) | Slow: coverage | Fast: chords / melody | Third file: chords / melody |
|---|---|---|---|---|
| Previous version | 32 | 70% | 62% / 68% | 62% / 65% |
| **Current defaults** | **11** | 66% | 58% / 45% | 56% / 60% |
| Current + `--attack-db 6` | 18 | 66% | 58% / 48% | 58% / 75% |
| Current, `--preset late` on the slow file | 1 (of 13 notes) | 70% | | |

- Median pitch error on kept notes:
  - slow file: 0.4 cents
  - fast file: 2.5 cents
  - third file: 4.8 cents (it has ±8 cents of tape wobble built in)
- Every tuning offset was estimated within 3.4 cents.
- 7 of the 11 remaining false notes are the right pitch class in the wrong octave.
- The main cost is the fast file's melody, whose notes sit exactly on the chord tones' overtones. That is the hardest case, and the recall loss is largest there.

For comparison, Basic Pitch (NeuralNote's engine) found 9% of the slow file's notes on default settings. With permissive settings it found 46%, but as 215 fragments with 26 false notes.

## Known limits

- **Same-onset octave doublings.** A doubling that starts together with its lower octave is physically the same thing as a strong overtone. The tool keeps it only if it carries clearly more energy than an overtone would. Re-double by ear where you want the voicing thicker.
- **Timing depends on register.** Upper-register starts land within about 0.1 s of the true onset. Bass starts blur by up to half a second.
- **Some tonality isn't notes.** Aliasing glitter, noise color and distortion partials belong in your processing chain. Check `_rejected.csv` to see what was set aside.

## Reproducing the tests

```
cd tests
python make_slow.py
python make_fast.py
python make_holdout.py
python evalh.py
```

`evalh.py` passes any extra flags to hecker2midi, for example `python evalh.py --prune-margin 3`.
