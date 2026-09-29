# Long Line: inner-note composition study

An opt-in update to Melodic Weave plus a **96-second review example**, not a replacement full-length master. The 5:36 score keeps v8's form and adds a separately controllable inner arrangement.

- [Listen: combined study B](Renders/Long%20Line%20-%20Inner%20Detail%20-%2096s.mp3)
- [Listen: exposed inner arrangement](Renders/Inner%20arrangement%20-%20exposed.mp3)
- [Diagnostic: 0-12s scaffold, 12-24s inner layer, 24-36s blend](Renders/Diagnostic%20-%20scaffold%20inner%20blend.mp3), all at matched RMS and the same source position
- [Composition audit and reference evidence](COMPOSITION_AUDIT.md)
- [New tool and usage](../../tools/melodic_weave/README.md#inner-texture-mode-v2)
- [Full 5:36 event score](texture.json) and [eight-track MIDI](texture.mid)
- [Editable demo mix](Long%20Line%20-%20Inner%20Detail%20B.rpp)
- [Editable four-instrument performance](Texture%20Instruments.rpp)
- [Construction diagram](Audit/inner_note_structure.png)
- [Checks and listening limitations](Audit/QA.json)

The full score has 2,821 events: the unchanged 123-event scaffold and 2,698 new inner notes. The example covers source time 2:20-3:56 and includes 809 inner notes. It uses TyrellN6 and FB-3300 with stable pitch, softened envelopes and calibrated levels. No reference-artist audio is included or sampled. Existing piano/nature lineage remains [v6's source licenses](../long-line-v6/Sources/LICENSES.md); new instrument performances are original music, not a reusable third-party synth sample library.

The new activity is verified in the MIDI and rendered audio. Paired Gemini reviews did not reliably distinguish the new mix, while standalone reviews described inner movement; improvement remains a listening judgment, not a passed automated gate. Try the exposed arrangement and diagnostic before judging the restrained blend.

## Reproduction

From the repository root:

```powershell
python tools/melodic_weave/texture_weave.py --scaffold productions/long-line-v8/weave.json --harmony productions/long-line-v6/harmony.json --out productions/long-line-v9-study/texture --density 1 --level 1
python -m unittest discover -s tools/melodic_weave
python productions/long-line-v9-study/Scripts/prepare_demo.py
```

Use a fresh candidate directory or change render filenames: the native scripts refuse to overwrite existing renders. Run Scripts/render_instruments.lua in REAPER, then print_lanes.lua, then `python Scripts/prepare_demo.py --calibrate` using its full path from the repository root. Run build_demo_b.lua and verify_demo.py. Prepare_demo retains the supplied scaffold excerpt when the ignored v8 native master is absent. The saved mix needs Surge XT Effects and REAPER; instrument rebuilding also needs TyrellN6 3.0.0 beta revision 16976 and FB-3300 1.2.5. FFmpeg/Python paths in analysis scripts are local configuration. Native free-running oscillators can differ between fresh renders; supplied lossless prints preserve this candidate.

Fourman FLAC downloads and Melnyk streaming audio are outside the repo in the local reference cache. Their stable Bandcamp links, quality, source hashes and reviewed windows are in Audit/reference_sources.json. Scripted signal analysis needs those reference files; no download URL tokens or copyrighted audio are distributed.
