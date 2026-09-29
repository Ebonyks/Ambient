# Long Line — first full-length study draft (5:36)

[Listen to the final MP3](Renders/Long%20Line%20-%20Full%20Length%20-%20Study%20Draft%20-%205m36.mp3) · [Open the REAPER project](Long%20Line%20-%20Full%20Length.rpp) · [Read the audit](Audit/FINAL_AUDIT.md) · [Production-impact journal](PRODUCTION_JOURNAL.md)

Developed from the 112-second Long Line study. The existing A–B–D–B–A–E–D melodic arch and its eroded recorded timbre remain. The accompaniment is revoiced and slowed into seven states with tied common tones. This is a first full-length composition draft, not an accepted master or a claim of artist equivalence.

## What the new study changed

- **Harmonic identity:** four-note source objects replace stacks of independently changing accompaniment. Nine shared-tone entries carry across boundaries without reattack or retuning.
- **Long-form development:** Dadd9 → Bm7 → Gmaj7 → Cmaj7 → Em7 → Gm7 → D, each 42–70 seconds. The motif runs in complete statements across those states. Some earlier chord labels were corrected rather than filled with more notes.
- **Stable friction:** C2/B3 remains a compound major seventh over a long span. B3 then continues through the E-minor reinterpretation. The G-minor region retains the motif's upper B as deliberate friction against Bb.
- **Synthesis:** separate low anchor, pitched body, clearer motif, eroded motif return, distorted body and residue. The new body saturation is 4x oversampled and level-matched; the anchor bypasses it. Stronger middle returns trade against a lower body level instead of adding voices.
- **Ending:** the last D continues from existing recorded D material through 5:32, then leaves the environmental tail. Loud field-recording clicks were locally attenuated.

## Session and files

Eight 48-kHz / 24-bit FLAC source stems are included in Media; the ninth REAPER track is the shared Valhalla Supermassive return. Install that plugin to reproduce the wet mix; no plugin binary is distributed. The MP3 is the portable listening version. The original local 48-kHz / 24-bit master WAV is retained in Renders but excluded from Git to avoid duplication. Audit/audio_inputs contains 22,050-Hz lossless analysis inputs, not mastering files.

harmony.json is the authoritative core-state sketch; harmony.mid ties its shared pitches on separate channels. This MIDI is a harmonic skeleton, not the rendered performance. The actual delayed entries and persistent source identities are in voice_events.json; phrase_map.json documents reuse of the three prior motif articulations. The final coda continuation is documented separately in Audit/coda_continuation.json.

## Reproduction

Use requirements-analysis.txt in a local Python environment. From Scripts run compose.py, synthesize.py, then extend_coda.py. Sources are bundled and referenced relative to the production folder. These steps recreate the media; they may differ by a few quantization units across numerical runtimes, so current hashes identify the delivered edition rather than a universal bit-exact guarantee.

In REAPER run Scripts/rebuild_from_stems.lua. It creates a fresh project tab from the bundled stems and ambience template, applies the final mixer automation, validates source lengths, and saves Long Line - Rebuilt.rpp. It does not render automatically. Render its configured 0–336-second stereo range to create a new WAV. The delivered project has already been rendered and verified. Historical refinement scripts are kept for inspection; they are not prerequisites to open the session.

For analysis, run Scripts/prepare_analysis.py to point the original handoff extractor at bundled baseline/final audio. The three unchanged extraction scripts live in Scripts/analysis. Their cached outputs and the 20-ms envelope arrays are included. Follow the study README's fresh-output-directory rule if changing extraction parameters. Scripts/audit_construction.py checks the delivered source-event plan and local master; plot_audit.py uses Matplotlib to draw the audit figure.

## Review status

H00–H08 core validation, common-tone continuity, source-count, anchor-frequency, media-integrity and render checks pass. They do not prove timbral or long-form artistic success. 29 new Gemini excerpt calls were made: 17 spanning the first full render, two controls, nine middle/tail refinement checks, and one final ending check. The cumulative authorized-listen count is 70. The control was inconclusive and is not counted as proof of the protocol. The tool hears at most 20 seconds per call; full-track artistic acceptance remains a human listening question.

Sources and their licenses are documented in Sources/LICENSES.md and Sources/provenance.json. No reference-artist audio or MusicGen audio is used or redistributed.
