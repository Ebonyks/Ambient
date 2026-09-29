# Long Line: context blend revision

[Play the revised integrated 96-second excerpt](Renders/Long%20Line%20-%20Context%20Blend%20-%2096s.mp3). Source position remains 2:20-3:56 of the 5:36 draft. This is an audition candidate, not owner-accepted work or a replacement full-length master.

The owner rejected the previous blend and located the problem at the analog synth entrance around 13 seconds. In the previous 36-second diagnostic, 12 seconds starts an isolated synth layer normalized to the RMS of the entire original arrangement. That abrupt diagnostic exaggerates the separation, but does not invalidate the tonal criticism. This revision supplies an integrated excerpt rather than another abrupt exposed-layer demonstration.

## What changed

- TyrellN6 cutoff lowered, resonance reduced from 8% to 3%, and attack softened. FB-3300 cutoff lowered, resonator intensity reduced from 12% to 2.5%, and attack softened. These percentages are normalized control settings, not measured acoustic units. See native parameter dumps.
- The new inner bus now passes through native Surge XT Effects Tape before the existing short Reverb 2. Tape uses 34% hysteresis drive, 38% saturation, -20% tone, 15.01 ips loss speed, and 75% mix. Degradation and pitch modulation remain off. Input calibration targets 0.126 RMS; output gain compensates for that calibration. Base remains at 0.92 gain; nominal inner contribution was reduced from 0.45 to 0.32 before tape gain changes.
- The previous generator checked field membership but not actual sustaining neighbors. The new optional `blend_texture.py` revises inner voices against the unchanged scaffold and previously accepted inner notes, with a one-second release guard. It avoids added neighboring notes one or two semitones apart in actual register, preserves wider intervals and existing scaffold tensions, and omits a note when no safe candidate exists.
- Full-length score: 1,044 inner notes repitched and 87 omitted; 2,611 inner notes plus the original 123 scaffold events remain. Timing and original scaffold are retained. This is a piece-specific conservative constraint, not a general rule for ambient harmony or a claim about Hecker's scores. It may reduce useful tension; listening acceptance remains necessary. The guard approximates releases and does not measure all acoustic tails.

## Editable delivery and reproduction

- `Long Line - Context Blend.rpp`: integrated two-track session, relative lossless media, live Tape and Reverb 2.
- `Texture Instruments.rpp`: four editable native MIDI lanes using TyrellN6 and FB-3300, with softened patches.
- `texture.json` and `texture.mid`: corrected full-length score; `Media/02` through `05` are individual 96-second prints, and `06_Inner_texture.flac` is their calibrated sum before live bus effects.
- Preserve earlier versions under `long-line-v9-study`; their evidence describes that historical version, now rejected by the owner for tone clash.

Run `python tools/melodic_weave/blend_texture.py productions/long-line-v9-study/texture.json --out productions/long-line-v9-blend/texture`, then `Scripts/prepare_demo.py`. In REAPER run `render_instruments.lua`, wait for its receipt, run `print_lanes.lua`, wait for all four lanes, run `prepare_demo.py --calibrate`, then `build_blend.lua`. The saved script includes the gain calibration for these supplied media; recalibrate it if changing sources. Render scripts refuse to overwrite existing WAVs; use a new version directory for another revision. Finally run `verify_blend.py`.

Requires the previously installed TyrellN6 revision 16976, FB-3300 1.2.5 and Surge XT Effects 1.3.4. Native parameter names and settings are recorded in `Audit/native_patches.tsv` and `Audit/blend_effects.tsv`. FB-3300 does not provide ordinary per-note velocity response; its envelopes and audio gains govern level.

## Evidence and limits

26 melody/texture tests and 10 harmony tests passed. Native render is 96 seconds, finite stereo 48 kHz / 24-bit, -20.54 LUFS integrated and -5.75 dBTP. Construction audit reports zero added close-register pairs under the one-second guard, down from 3,069 across the full score; this is not a perceptual quality score.

Gemini listen 99 compares RMS-matched ten-second excerpts of the same passage. It again reports indistinguishable versions, so it does not substantiate improvement. One of the 100 authorized successful listens remains. The owner's negative assessment of the previous mix is authoritative; this version remains pending owner listening. The 96-second excerpt is the only newly rendered integrated duration; the full-length corrected score is supplied, but no new full-length master is claimed.

All composition is original. No reference-artist recording is sampled or redistributed. Existing scaffold provenance remains in [v6 licenses](../long-line-v6/Sources/LICENSES.md); new synth prints were made locally. Plugin binaries are not included.
