# Long Line: continuous flow revision

[Play the integrated 96-second candidate B](Renders/Long%20Line%20-%20Continuous%20Flow%20B%20-%2096s.mp3). Editable session: `Long Line - Continuous Flow B.rpp`. This is a compositional alternative after the owner rejected the previous foreground/inner-layer hierarchy. Listening acceptance is pending.

## Musical change

The previous mix kept an individually legible melodic foreground and added faster notes underneath. This revision removes that foreground from the audition. Four continuous strands now carry the composition above quiet water and wood; there is no retained piano lead, string lead, anchor pulse, or previous mixed master in the rendered audio.

The new `continuous_field.py` mode uses approximately fourteen articulations per second, equal velocity, narrow timing variation and fairer pitch distribution. Its collective register follows a 150-second arc while neighboring harmonic fields exchange pitch weight over 24 seconds. Common tones retain their probability during the transition. Repeated-note ownership and short close-register clashes are guarded. No synchronized accents, phrase resets, semitone-return figures or pitch LFOs are introduced. The authored pitch distribution uses seeded weighted choices, not recovered piano fingering or a transcription.

The original seven harmonic destinations remain, but the foreground's ordering is replaced. There are 4,600 newly authored notes over 336 seconds and 1,381 notes in this audition. Greater note count is not the acceptance criterion: the intended result is slow collective movement without a dominant single-note line. Equal MIDI velocity does not prove equal acoustic salience, especially with FB-3300; four native stems are calibrated to equal RMS before summing.

The original 123 scaffold events are retained in JSON as reference provenance only. The exported MIDI excludes their performed notes; its first four tracks are silent, with the four new voices on channels 5-8. `Texture Instruments.rpp` directly supplies the four native performing lanes.

## Reference basis and limits

The owner's description governs this revision: slow melodic movement formed by many notes of low individual significance. [Melnyk's artist page for Rivers and Streams](https://lubomyrmelnyk.bandcamp.com/album/rivers-and-streams) describes his continuous playing in terms of connected flow. The earlier [reference audit](../long-line-v9-study/COMPOSITION_AUDIT.md) examined locally acquired Parasol excerpts and separates spectral articulation proxies from played-note counts. No new reference recording was downloaded or sampled here. Our rates, transition lengths and voicings are original design choices, not claimed measurements of Melnyk's technique.

This is an electronic adaptation of that requested organizational principle. The retained analog patches are not a piano performance model. Algorithmic density and smoothing do not establish expressive equivalence to a human continuous-piano performance.

## Render iteration and audit

A uses the softened TyrellN6 / FB-3300 patches from the preceding tone revision, Surge Tape and a 38% short-room mix. Gemini listen 100 described A as a dark noise drone with strong low-mid buildup; it did not confirm the intended flowing inner detail. That unfavorable evidence is preserved in `Listening/100-flow-A-review.json`.

B reduces room mix to 22% and adds a broad -5 dB ReaEQ bell at 350 Hz, bandwidth 2.2 octaves. Native settings are in `Audit/flow_B_eq.tsv`. The measured 200-500 Hz share of mono-summed spectral power fell from 42.4% to 36.0%. This demonstrates changed balance, not perceptual success. B is 96 seconds, -21.36 LUFS integrated, -8.08 dBTP, finite stereo 48 kHz / 24-bit and unclipped. All 100 authorized successful Gemini listens are now used; B has not received a further model listening review. Owner listening remains required to determine whether the texture has enough inner motion rather than becoming static.

31 melody/texture tests and 10 harmony tests pass. Tests cover deterministic generation, continuous note activity, absence of velocity accents, 24-second transition coverage, distributed pitch occupancy across seeds, MIDI-safe note ownership, and exclusion of the reference foreground from performance export. These are construction checks, not artistic approval.

## Reproduction and sources

Run `python tools/melodic_weave/continuous_field.py --out productions/long-line-v10-flow/texture`; `Scripts/prepare_demo.py` exports the native audition notes. In REAPER execute `render_instruments.lua`, then `print_lanes.lua` after the render receipt appears. Run `prepare_demo.py --calibrate`, then `build_flow_b.lua`, and finally `verify_flow_b.py`. The supplied nature bed is already cropped to source 140-236 seconds; derivation gains and originals are recorded in `Audit/bed_sources.json`. Scripts preserve existing WAVs; use a new version directory for another render. Native instrument versions are the same as [v9 blend](../long-line-v9-blend/README.md).

All source prints and relative session media are included. The corrected full-length score is supplied; only this 96-second audition has been rendered with the new arrangement. Original environmental-source provenance remains in [v6 licenses](../long-line-v6/Sources/LICENSES.md). No artist recording or plugin binary is redistributed. Earlier candidates and their audits remain preserved.
