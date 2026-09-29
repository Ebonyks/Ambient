# Palimpsest — Common Light, revision 3

A substantially reworked 112-second production study. The deliverables are `Renders/Palimpsest - 112s.wav`, the MP3 beside it, and `Common Light III - Palimpsest.rpp`. Earlier revisions remain untouched. Files named Design, review, or Listening are iteration evidence rather than the final mix.

## Musical and tonal changes

The clean piano foreground and live stock-synth parts from revision 2 have been removed. Piano recordings survive only as transformed source bodies: attack-free overlapping grains, reversed fragments, nonlinear intermodulation and folding, irregular pitch trajectories, sample-and-hold reduction and selected quantization. Dirt belongs to the moving pitched material rather than being confined to a low-level reverb tail.

The supplied progression remains the harmonic ground: Dadd9 → Bm11 → G6/9 → Aadd9 → C → Fmaj7#11 → Gm → Bbmaj7#11 → Gm → D. The original A–B–D / B–A / E–D arch overlaps a contrary-motion line, persistent upper fifths and an added unevenly phrased line using chord tones, borrowed tones and suspensions. The Bb-to-A resolution around 95 seconds remains a single clear arrival.

Additional real source identities replace reliance on different versions of one piano tone: cello sustain, cello pizzicato and spiccato, viola ensemble and flute. Their bow/breath and uneven natural decays remain audible through processing. The new articulated string line has selected displaced reverse answers and independent reflection tails. This is source-based sound design, not a claim that these were Hecker's precise instruments or presets.

The background recedes around 20–23, 41–44, 63–66 and 84–88 seconds to expose the moving voices. No drum part, metrical ostinato or tempo-synchronized stutter was added. Some short irregular fragments are intentional; they should read as broken material rather than a primary rhythm section. Environmental sound remains as a framing element and is intentionally exposed at the end.

## Listening process

Gemini cloud listening was explicitly authorized by the user up to 100 calls. Each successful call receives at most a 20-second excerpt. The complete machine-readable responses and the final count are in `Listening/listening_log.json`; timestamps in responses are local to each excerpt. Final excerpts cover the entire 112-second delivery, with overlapping ending coverage.

A: Long-grain transformation was still judged too smooth, dark and pad-like.

B: Stronger variable rate reduction, fragmentation and high-partial damage made erosion unmistakable, but constant upper-mid noise obscured the music. This was rejected as a final balance.

C: Reduced constant fracture, added real bowed/breath sources, separated roles and stereo motion. Listens described integrated texture, but the crest still risked becoming a sustained pad.

D: Bringing more existing layers forward did not solve that envelope problem. The critiques again described clutter and indistinct roles.

E: Added a distinct, unevenly articulated processed-string line and gaps in the background. The opening improved, but the crest was still too polite.

F/G: Folded the central melodic voice, reduced masking from the background, brought the articulated line forward, and corrected monitoring/render level. G listens identified phrasing, audible dirt and separate roles in all three main sections, with some intentional upper-mid bite.

27 successful Gemini excerpt listens were used (540 seconds of submitted audio across successive designs); three missing-file attempts sent no audio. Six excerpts checked the complete final arrangement, followed by one extra listen after extending the ending tail. The last listen described the transition as coherent. These reports are advisory opinions, not proof of resemblance to a reference artist, a calibrated quality score or a substitute for the user's judgement. Their repeated exact-frequency guesses were not blindly applied as EQ prescriptions. A missing-file attempt for three G excerpts failed before sending audio and is recorded separately.

## Session and editing

The final REAPER session contains nine processed audio stems, a native Valhalla Supermassive return, and two muted MIDI reference tracks. REAPER performs routing, independent track-level automation, shared distance and the native master render. The substantial source transformations are generated offline by the saved Python scripts; they are not falsely represented as live Reaktor or Surge processing.

`score.json` contains the underlying harmonies and first two melodic strands. `articulated_score.json` records the additional foreground gestures. `C_gain.json` records the bowed/breath phrase events. MIDI reference edits do not automatically regenerate processed audio. Use the scripts for source changes and the REAPER tracks for balance, placement, automation and effects.

The scripts form a chronological production trail, not a single idempotent one-click build. Final RPP state and `Scripts/final_track_*.RTrackTemplate` are authoritative. Main construction steps: design.py → design_b.py → design_c.py → build_reaper.lua → articulation.py / articulate_reaper.lua → fold_voice.py / fold_reaper.lua → finalize.lua, followed by ending.lua.

REAPER was taking media offline when inactive. The finalizer explicitly runs the verified native `Item: Set all media online` action and checks all nine audio source lengths before rendering. The final `session_receipt.txt` confirms sources, mutes and solos. This check prevents a partial render from passing as a complete mix. Intermediate source-length assertion failures and incomplete setup renders are not final delivery evidence.

## Provenance

- VSCO 2 Community Edition, official repository, CC0: https://github.com/sgossner/VSCO-2-CE
- Additional cello sustain, cello pizzicato/spiccato round robins, viola and flute source URLs and SHA-256 hashes are in `Sources/new_samples.json`. `Sources/VSCO_CC0_LICENSE` preserves the license. Source pitch naming differs across instruments; decoded spectral checks were used to set actual MIDI roots rather than blindly copying the filename octave. Cello C3 sources were mapped to MIDI 60; viola/flute C4 sources to MIDI 72.
- Soft upright source recordings retained in `../Revision 2/Sources/VSCO`; transformations preserve attribution. All final session playback media are local under this revision's Media directory.
- River: humansalad, Freesound 323458, CC0, public HQ MP3 preview source preserved in the original project's Sources folder. https://freesound.org/people/humansalad/sounds/323458/
- Tree/wind/birds: Felix Blume, Freesound 140047, CC0, public HQ MP3 preview, M/S decoded and processed. https://freesound.org/people/felix.blume/sounds/140047/
- Valhalla Supermassive is an existing installed VST used for the shared return. No new paid plugin or subscription was purchased.
- No Tim Hecker recording is sampled. No MusicGen audio is used in this revision. This is authored sample processing and composition, not a newly generated AI-model performance.

The source/gear research for the early Hecker references is in `../Revision 2/README.md`. Its historical caveats still apply: Reaktor/AudioMulch and processed guitar/piano sources are documented in era interviews; an exact Haunt Me VST inventory is not established. Modern tools here are substitutes, not asserted historical matches.

## Verification

The master is rendered natively in REAPER at 48 kHz, 24-bit stereo. No master limiter or automatic loudness normalization is applied. `verification.json` contains measured loudness, true peak, dynamics, stereo correlation, spectrum and WAV hash. Technical integrity and Gemini listening evidence are separate from artistic acceptance.
