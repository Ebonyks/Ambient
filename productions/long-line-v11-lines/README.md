# Long Line: differentiated fast lines

[Play the revised 96-second draft B](Renders/Long%20Line%20-%20Differentiated%20Flow%20B%20-%2096s.mp3). Editable session: `Long Line - Differentiated Flow B.rpp`. Owner acceptance remains pending.

## Fresh reference listening before drafting

At the owner's explicit request, two fresh audio-model reviews examined Lubomyr Melnyk's [Parasol](https://lubomyrmelnyk.bandcamp.com/track/parasol), 2:00-2:20 and 6:00-6:20, before this score was generated. The cached artist stream and excerpts were checked against source metadata, hashes and independently resampled audio. The reference audio is not redistributed or sampled. These two targeted reference reviews extend the exhausted earlier allowance to 102 successful listens; they do not establish a new open-ended review budget.

Both model reports emphasize rapid articulation and register separation despite resonance. Specific descriptions such as 'stride', 'syncopated', 'bouncing bass' and 'soaring treble' are model interpretations, not reliable score analysis, and were not adopted as genre or transcription facts. Only two short windows were reviewed; this is not a claim to have reviewed the entire performance anew. Full outputs and source receipts are retained in `Listening/` and `Audit/reference_listening_sources.json`.

The practical correction is to preserve internal articulation and independent line behavior. The previous draft's randomized, equal-velocity selection and slow synth envelopes flattened differences among lines. Increasing that generator's density alone would have retained the same failure.

## Composition and synthesis revision

- Four nominal rates are now 12.44, 13.48, 14.92 and 15.88 notes per second: exactly four times the previous nominal rates. Full-score activity is 18,398 notes versus 4,600, a 3.9996x count ratio. This audition contains 5,509 notes. These are original authored rates, not claimed measurements of Melnyk's playing.
- Each line has its own persistent contour cell, 7/11/13/17 positions long, its own mutation period, register, clock and dynamic inflection. Registers are MIDI 48-62, 62-76, 55-69 and 67-81. One contour position changes at a time; no shared cell reset or accent grid is added.
- An explicit 28-stage tonal itinerary changes every 12 seconds across the full 336-second score. In this excerpt it proceeds Em9 -> Cmaj7 -> Am9 -> D6 -> Em9 -> Bm7 -> Cmaj7 -> Em7 -> Am9. Lines enter the new harmony at offsets of 0, 0.9, 2.1 and 3.6 seconds. This replaces the former narrow pitch distribution and 24-second blending rule. Harmonic labels describe the authored pitch sets, not a claim that every root is perceptually dominant.
- Tyrell and FB-3300 now use much quicker attacks, lower sustain and shorter releases. Line low-pass settings differ: 1.8, 3.0, 2.3 and 3.3 kHz. The existing low resonance, calibrated Tape stage and broad 350-Hz reduction remain; room mix falls to 16%. No deliberate pitch modulation is added. Actual native parameter values are in `Audit/native_patches.tsv`.
- The old melodic scaffold remains excluded from the audio and MIDI performance. JSON retains it only as reference provenance. The quiet nature bed is unchanged except for reduced gain. FB-3300 still has no ordinary per-note velocity response; its articulation comes from its native envelope and gain, not the proposed MIDI velocity alone.

## Evidence and limits

35 melody/texture tests and 10 harmony tests pass. Tests cover the fourfold activity change, distinct line registers/cells/rates, changing tonal pitch sets, seed reproducibility, safe note ownership and exclusion of the old foreground. B is 96 seconds, stereo 48 kHz/24-bit, -21.39 LUFS integrated and -7.71 dBTP, without clipping. Its 1.72 master gain matches the previous -21.36 LUFS audition closely; A preserves the quieter first native render.

`Audit/line_activity.json` compares individual native prints at several spectral-flux thresholds. The results are mixed and threshold-sensitive; they do NOT demonstrate a fourfold increase in perceived speed. The score rate is confirmed; perceived speed, separation, tonal motion and suitability still require owner listening. No subjective review of this new mix is claimed. The reference reviews informed the draft, but neither test counts nor favorable descriptions of Melnyk validate this output.

## Editable sources and reproduction

`Texture Instruments.rpp` holds the four native performing MIDI tracks, while `texture.mid` is the full-length performance export with its first four reference tracks silent. `texture.json` contains the full tonal itinerary and original reference scaffold. Individual lossless lane prints and the calibrated composite are in `Media/`; the combined session uses relative media paths. Only this 96-second excerpt is newly rendered; no full-length finished master is claimed.

Run `python tools/melodic_weave/flowing_lines.py --out productions/long-line-v11-lines/texture`, then `Scripts/prepare_demo.py`. In REAPER run `render_instruments.lua`; after its receipt run `print_lanes.lua`. Run `prepare_demo.py --calibrate`, then `build_lines_b.lua`, then `verify_lines_b.py`. Render scripts preserve existing WAVs; use a new version directory to iterate. `audit_activity.py` requires the prior local v10 native WAVs for its comparison.

Plugin versions remain TyrellN6 revision 16976, FB-3300 1.2.5 and Surge XT Effects 1.3.4, plus native ReaEQ. Environmental-source provenance is in [v6 licenses](../long-line-v6/Sources/LICENSES.md); derivation gains are in `Audit/bed_sources.json`. No artist recordings or plugin binaries are included. Earlier candidates and their rejection history are preserved.
