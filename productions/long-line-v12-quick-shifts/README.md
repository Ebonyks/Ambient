# Long Line: 3.5-second tonal shifts

[Play the revised 96-second excerpt](Renders/Long%20Line%20-%20Quick%20Shifts%20B%20-%2096s.mp3). Editable REAPER session: `Long Line - Quick Shifts B.rpp`.

Applied the owner's two changes directly:

- Halved the native attack controls: TyrellN6 0.10 -> 0.05; FB-3300 0.014 -> 0.007. These are normalized plugin settings. Every other authored native synth parameter is unchanged.
- Harmony changes every 3.5 seconds instead of 12. The existing tonal itinerary continues cyclically across the full score, skipping a duplicate harmony at the loop join. The per-line transition offsets scale proportionately to 0 / 0.2625 / 0.6125 / 1.05 seconds, keeping their stagger within the shorter harmonic period.

Note rate, onset timing, dynamic contours, register bounds, contour cells, effects and nature bed remain as in v11. The preceding lane calibration gains, composite gain and bus gains are frozen. The initial export clipped; B halves only the master output from 1.72 to 0.86 to provide headroom, without changing timbre or relative balance. No listening-model calls or additional tonal refinements were made.

`Audit/requested_changes.json` verifies that the only native patch changes are the four attack controls and that note onset times, velocities and count are retained. The full source score still has 18,398 performing notes. JSON retains the old scaffold as reference only; it is excluded from the performed MIDI and audio.

Reproduce with `python tools/melodic_weave/flowing_lines.py --harmonic-period 3.5 --out productions/long-line-v12-quick-shifts/texture`, then `Scripts/prepare_demo.py`. Run `render_instruments.lua` in REAPER, wait for its receipt, then run `print_lanes.lua`. Run `prepare_demo.py --calibrate` (uses the frozen gains in `Audit/inherited_gains.json`), `build_quick_b.lua` in REAPER, and finally `verify_quick_b.py`. Existing WAVs are preserved; use a new version directory for another render.

36 melody/texture tests and 10 harmony tests pass. Native audio duration, finite samples, clipping and loudness are recorded in `Audit/QA.json`. This is a 96-second render of source 140-236 seconds; the full 336-second revised score and MIDI are included, but no new full-length master is claimed. Original environmental-source provenance remains in [v6 licenses](../long-line-v6/Sources/LICENSES.md). Plugin requirements remain those of [v11](../long-line-v11-lines/README.md). No reference-artist recordings or plugin binaries are included.
