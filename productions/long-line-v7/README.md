# Long Line v7 - Moving Voices

A **5:36 review draft** addressing the overly fixed voicing and repeated melodic arch in v6. The previous version is preserved.

- [Listen: full MP3](Renders/Long%20Line%20-%20Moving%20Voices%20-%205m36.mp3)
- [Editable REAPER project](Long%20Line%20-%20Moving%20Voices.rpp)
- [Melody/voicing tool and controls](../../tools/melodic_weave/README.md)
- [Generated MIDI](weave.mid) and [authoritative event score](weave.json)
- [Reference comparison data](Audit/comparison.json)
- [Construction comparison figure](Audit/voicing_comparison.png)
- [Matched-level excerpt reviews](Audit/listening.json)
- [Render verification](Audit/render_verification.json)

## What the study changed in this production

V6 held 19 core source events across seven long harmonic states and replayed one upper pitch sequence seven times. That kept harmony coherent but confused persistence of a pitch collection with immobility of its realization.

V7 retains the harmonic fields and bass anchors while three strands change independently. Its 123 source events include the anchors; 16 distinct upper phrase fragments replace literal whole-arch repetition. Actual non-anchor change spacing has a 2.48-second median and a 2.00-4.58-second 10th-90th percentile range. Unchanged voices stay sounding, so a local change does not reset the ensemble. Maximum source overlap is five notes, compared with v6's six. There are no added drums or metrical arpeggiator.

The study's middle-register prominence-change medians support a faster local clock: I'm Transmitting Tonight is 2.25-2.5 seconds across three thresholds; Incurably Optimistic! is 3-3.5 seconds. Highwire and Celestina have different upper and middle timescales. Therefore the generator changes individual strands at unequal intervals instead of forcing all voices to change every two seconds. Full threshold results and unsupported-frame coverage are in the comparison JSON. These are existing sample-derived measurements, not freshly auditioned reference audio, score transcriptions, or recovered session data. Haunt Me is outside this study's scope.

## Tonal continuity and changes

The same CC0 VSCO upright-tail source bank, 110 ms grains, fourfold overlap, stable per-pitch tuning, separate anchor, parallel distortion, nature tracks, and Valhalla Supermassive return remain. Shorter notes use 380/650 ms upper/inner attacks and 800 ms releases. The parallel transfer combines oversampled saturation with a restrained folded component. This is the same source palette and routing, not an identical-tone A/B. The old processed arch is replaced, and residue is regenerated from the new events so it cannot secretly replay the old melody.

The project references three preserved v6 stems and the v6 bus template using relative paths. Clone the repository with both production directories; v7 alone is not a self-contained download. [Existing source licenses and lineage](../long-line-v6/Sources/LICENSES.md) apply to these derivatives. No reference-artist audio is included. Valhalla Supermassive is required for the wet return; its binary is not bundled.

## Review result and remaining limitations

The native REAPER master is 336 seconds, stereo 48 kHz/24 bit, -19.28 LUFS integrated, -8.86 dBTP, with no clipping or nonfinite samples. Its 2.1 LU loudness range is substantially smaller than v6's 7.4 LU. Faster voice movement has not, by itself, solved long-form breathing; the source texture remains continuous. This should be judged as a melody/voicing revision, not an accepted finished track.

Six new-version and two baseline excerpts were matched to -26 dBFS RMS and reviewed with Gemini. It described moving pitches and soft attacks in the new excerpts, but gave similar descriptions to the baseline. Those reviews do **not** demonstrate superiority or artist resemblance. Cumulative successful listens: 78 of the authorized 100; 22 remain. No extra listens were spent chasing generic frequency complaints.

Ten melody-tool tests, including 100 seeded realizations and MIDI channel/bend lifecycle checks, pass. The original harmony protocol remains unchanged. Palette compliance, note-construction correctness and artistic acceptance remain separate.

## Rebuild

From the repository root, with the v6 Python audio dependencies installed:

```powershell
python tools/melodic_weave/melody_tool.py --harmony productions/long-line-v6/harmony.json --out productions/long-line-v7/weave
python productions/long-line-v7/Scripts/render_sources.py
python productions/long-line-v7/Scripts/compare.py
```

Run `Scripts/build_and_render.lua` in REAPER to create a **new tab**, populate the eight stems and inherited ambience return, save and render. It refuses to replace the existing WAV; choose new project/render filenames for another candidate. Do not overwrite the published score/stems with a different seed if you want to preserve this candidate. `verify_audio.py` measures the native render, exports MP3, and prepares matched-level excerpts; its FFmpeg path is local configuration. `plot.py` additionally needs Matplotlib. The locally generated WAV and listening excerpts are ignored by Git; the complete MP3 and lossless stems are published.
