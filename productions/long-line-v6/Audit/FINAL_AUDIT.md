# Full-length audit and refinement record

Authority is the Ambient handoff and synthesis/harmony protocol at commit 6e33f20, with measured-study source 163d5a9. These are designed construction constraints and imperfect spectral evidence, not recovered artist sessions.

## Implementation

The revised piece is 336 seconds. It retains the original motif and prior eroded sample timbre while rebuilding the accompaniment as seven persistent four-voice states. Nine common-tone entries are tied, making 19 actual body events instead of 28 state entries. Including motif overlaps, the maximum nominal source count is six. Processing partials and reverb are not counted as performed notes. C/B supplies sustained friction; the new bass and body remain distinct from distortion. The last D is continued through 332 seconds using recorded material from the same D source.

## Machine evidence

- The shipped H00–H08 validator passes the authored core without warnings. All ten protocol unit tests pass.
- All nine shared boundary identities occupy one continuous source event. No common tone receives a new random cents value at its state boundary.
- Seven low anchors meet a 0.5-Hz tolerance both in their source stem and the final mix. This check does not establish exact tuning of the natural piano body or the previously distorted motif.
- Eight referenced media stems are present, stereo, 48 kHz and exactly 336 seconds. A fresh-tab rebuild from the bundled sources and ambience template succeeded.
- Final native REAPER WAV: 336 seconds, 24-bit / 48-kHz stereo, -21.12 LUFS integrated, -7.55 dBTP, 7.4 LU loudness range; no clipping or nonfinite samples. No master normalization or limiter.
- Identical handoff extractor, 22,050 Hz: median power centroid changes from 799.5 to 497.7 Hz; side/mid changes from +1.17 to -1.76 dB. Eleven final analysis windows contain supported narrow peaks. These are descriptive results, not an artist-similarity score or proof of performed-note identity.

See construction_checks.json, saved_project_verification.json, final_measurements.json, feature_comparison.json and the original feature/envelope arrays for details.

## Listening and refinement

The first complete render was reviewed in seventeen excerpts. Reports generally favored continuity but often described uniformly smooth pads and intermittent masking. A middle-section revision exchanged some pitched-body level for its own eroded returns, leaving the pitch object and event timing intact. Nine targeted excerpts then reported legible pitch and useful grain, with remaining comments about some entrances and local low-mid accumulation.

The tail was repeatedly flagged at the end of the last motif. It was repaired by continuing the existing D material through a longer decay, rather than adding a new voice or a blanket reverb swell. The final sixteen-second check described a smooth transition into the environmental ending.

The equal-RMS, equal-duration tied-versus-reattacked body control was inconclusive: Gemini failed to identify the deliberate reattack reliably. This explicitly limits confidence in its detailed judgments. Repeated generic frequency suggestions were not treated as mandatory EQ instructions. Excerpt-boundary complaints are retained in the logs and are not automatically interpreted as full-track edits.

## Remaining artistic review

This is a first full-length study draft. Human review should judge whether seven motif statements sustain interest across 5:36, whether the central pressure is sufficiently distinct, and whether the cleaner body still has too much conventional pad character. The model's 20-second limit does not validate whole-track form. Protocol compliance is not a proxy for sounding like Hecker, and owner acceptance remains open.

## Verification limitation

Automatic approval review rejected an additional native REAPER verification/save command, interpreting it as a potential destructive reset. It was not retried. Final project-reference and source-metadata verification was completed read-only from the saved RPP; the previously successful fresh-tab rebuild is recorded separately. No additional project edit was required.
