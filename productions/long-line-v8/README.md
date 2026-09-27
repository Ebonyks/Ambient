# Long Line v8 - tonal revision

A 5:36 original review draft. V7 is preserved. Open **Long Line - Tonal Revision F.rpp** for the delivered mix.

- [Listen to the full revision](Renders/Long%20Line%20-%20Tonal%20Revision%20-%205m36.mp3)
- [Editable final REAPER mix](Long%20Line%20-%20Tonal%20Revision%20F.rpp)
- [Instrument/plugin audit and historical sources](PLUGIN_AUDIT.md)
- [Editable modeled-string source](Physical%20String%20-%20Pink%20Bed.rpp)
- [Editable native tape processing](Calibrated%20Tape%20Sources.rpp)
- [Corrected score](weave.json), [MIDI](weave.mid), [pitch-change audit](Audit/voicing_revision.json)
- [Render comparisons](Audit/tonal_comparison.json), [final excerpt reviews](Audit/listening_f.json)

## What changed

Eleven pitch edits remove twelve repeated A-B-A semitone figures without banning sustained harmonic friction. The passage around 2:48 now follows G-E-G-B-D-E-G in its foreground strand rather than alternating B/C. All score-event start/end times and the seven harmonic fields are retained. The modeled-string print releases MIDI excitation 250 ms before each score-event end to leave room for its synth release; score timing preservation is not a claim of identical acoustic envelopes.

The previous three-piano/wavefolded palette is replaced by two processed piano strands and a physically modeled string, with native Surge Tape hysteresis/loss, Nimbus granular memory, a separate damped short room and a reduced long Supermassive return. The old sine-folded returns and middle-section distortion boosts are removed. Pitch drift, portamento, tape degradation, Nimbus pitch shift and reverb pitch modulation are disabled. The late anchor is eased to expose the melodic strand.

The study changed the work by separating evolving inner voicing from pitch wobble, and separating processing roles instead of adding parallel distortion indiscriminately. Historical accounts point to Reaktor/rAmpler and shortwave/melodic recombination; they do not establish a complete early-era free-VST inventory. The modern free instruments/effects are functional substitutions, not recovered album presets. See the sourced plugin audit.

## Verification and remaining limitation

The final F render is 336 seconds, stereo 48 kHz/24 bit, -20.28 LUFS, -5.11 dBTP and 6.3 LU LRA. No clipping or nonfinite samples. Fifteen melody tests and ten harmony tests pass, including 100 seeded revision trials. Final excerpts are reported softer with little upper harshness, but low-mid masking remains a review concern. This is not an accepted finished master or a demonstrated artist match. Cumulative successful Gemini listens: 89 of 100, leaving 11. Their descriptions and scores are advisory, not acoustic measurements.

## Playback and reproduction

Clone this repository with v6 retained: the final session references its anchor, water and wood stems by relative path. Source licenses remain [the v6 CC0 lineage](../long-line-v6/Sources/LICENSES.md). New synth performance and processing are original. No reference-artist recordings or plugin binaries are redistributed.

For the final mix, install Surge XT Effects 1.3.4 and Valhalla Supermassive 5.0.0; ReaEQ comes with REAPER. The modeled-string source additionally uses Surge XT VSTi 1.3.4. All were already installed here; no extra download was required. Final core stems contain the printed instrument/Tape/EQ sound, so the live final mix needs no instrument loading.

Open the final RPP and choose a new render destination on another machine. For rebuilding a fresh candidate, run Scripts/revise.py then Scripts/render_piano.py in the documented Python audio environment; print the modeled string with Scripts/print_final_string.lua and normalize_final_string.py. Existing-output guards preserve published prints: use a separate candidate directory and render filenames. Calibrated Tape Sources.rpp preserves the native input gains, Tape and EQ; render its tracks individually with the retained safe master headroom, then normalize each to the levels in Audit/printed_tape_levels.json. Do not reuse the rejected clipped Calibrated_Tape_2.wav export. The final mix can be assembled with Scripts/build_final_mix.lua and measured with verify_release.py. Scripts use local REAPER/FFmpeg paths where applicable; adapt those paths on another machine.

Other scripts and audit files record rejected experiments, parameter discovery and intermediate comparisons, not alternative delivery instructions. Scripts/print_tape_sources.lua is the historical calibration experiment that first exposed clipping, not the safe production reprint path. Source prints and granular returns can differ between fresh native renders; the published lossless stems freeze this candidate.
