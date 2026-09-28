# Long Line: intermittent upper-octave harmonies

[Play the updated 96-second excerpt](Renders/Long%20Line%20-%20Upper%20Octaves%20-%2096s.mp3). Editable REAPER session: `Long Line - Upper Octaves.rpp`.

Adds occasional upper-octave companions to the existing harmony. The new notes are one or two octaves above their source notes, so their pitch classes remain within the active harmony. The performance range expands from MIDI 48-81 (C3-A5) to 48-90 (C3-F#6).

Two Tyrell lines carry these additions, using their existing velocity-sensitive patches at 55% of the source note's MIDI velocity. This is a velocity setting, not a calibrated acoustic loudness ratio. The FB-3300 parts remain untouched. Short windows of 2.8 and 3.1 seconds recur on separate 11.3- and 13.7-second cycles, with every third source note eligible. This adds 204 notes to the 96-second audition and 701 to the full score, under 4% additional events overall.

All existing notes, the 3.5-second harmony sequence, source-note speed, shortened attacks, effects, nature bed and gain settings remain unchanged. The added notes are original octave doublings, not sampled or transcribed Melnyk material. No listening-model calls or unrelated tone revisions were made.

`Audit/octave_changes.json` confirms the widened range and identical native patch settings. 39 melody/texture tests and 10 harmony tests pass; the focused tests check preservation of original notes, exact octave intervals, lower added velocities, periodic gaps and valid MIDI ownership. Audio export checks are in `Audit/QA.json`.

Reproduce with `python tools/melodic_weave/upper_octaves.py productions/long-line-v12-quick-shifts/texture.json --out productions/long-line-v13-octaves/texture`, then `Scripts/prepare_demo.py`. Run `render_instruments.lua` and then `print_lanes.lua` in REAPER, waiting for each receipt. Run `prepare_demo.py --calibrate` (retains inherited gains), then `build_octaves.lua` in REAPER, then `verify_octaves.py`. Render scripts preserve existing WAVs. Use a new version directory for another render.

Four editable native instrument lanes, individual lossless prints, combined media, full-length score and MIDI are supplied. Only the 96-second excerpt at source 140-236 seconds is newly rendered. Plugin requirements and underlying environmental provenance remain those of [v12](../long-line-v12-quick-shifts/README.md) and [v6 licenses](../long-line-v6/Sources/LICENSES.md). No artist recordings or plugin binaries are redistributed.
