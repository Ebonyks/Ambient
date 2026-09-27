# Melodic Weave

A deterministic JSON/MIDI composition tool for the Long Line project. It addresses the gap between **a slowly changing harmonic field** and **frequently changing individual voices**. It is an original rule-based proposal, not a transcription, trained model, or artist-similarity test.

From the repository root:

```powershell
python tools/melodic_weave/melody_tool.py --harmony productions/long-line-v6/harmony.json --out my-sketch --seed 260927 --change-min 1.8 --change-max 3.3
python -m unittest discover -s tools/melodic_weave -v
```

The core tool and tests use only Python's standard library. `--out` produces `.json` and `.mid`. MIDI uses 60 BPM only as a seconds carrier; it does not impose a musical beat. Overlapping notes receive separate channels and individual pitch bends with a two-semitone bend range.

## What changes

Three strands move above a retained bass. One strand changes at a time. Unequal proposal intervals, retained pitches and 550 ms transitions produce a median actual source change interval of 2.48 seconds in the supplied example. A candidate equal to the held pitch extends the existing source rather than retriggering it. Two other strands continue through each change. The source overlap ceiling is six; this example reaches five, including bass. Reverb tails are additional acoustic energy and are not hidden inside that count.

Seven authored cell variants develop the earlier A-B-D-B-A-E-D material through partial returns, interleaved responses, contraction, register exchange and continuation. Phrase windows last 15-25 seconds; windows can expose only part of a longer cell. Inner lines take alternating bounded steps inside their own registers; this version does not calculate counterpoint against the actual foreground interval. This is designed motif variation, not unconstrained random notes. The current scheduling pattern is deterministic in voice order and seed-random in duration; it is not learned from the references.

`--cells cells.json` accepts a JSON list of MIDI-pitch lists to replace the authored cells. `--friction-pc 11` explicitly retains B in the upper vocabulary; `-1` disables that addition. Pitch targets are realized within the current local field, not an album-wide major/minor scale. The Long Line preset closes with E-D in the upper voice and D in the middle; this closing gesture is intentionally piece-specific, even when custom cells are supplied. Adapt the completion block for another composition rather than assuming it is universally appropriate.

## Relationship to the harmony protocol

The [existing protocol](../../protocols/hecker-harmony-v1/README.md) still owns harmonic **palettes**. Its H08 warning about rapid replacement of an entire harmonic state does not prohibit motion inside that palette. This tool leaves the seven existing states intact, changes their momentary realization, carries already sounding pitches across a boundary, and declares upper B as an independent friction voice. The ending E is a declared continuation from the original motif, over the final D-major body.

Do not feed every momentary subset back to the harmony validator under a full-family label: the validator deliberately requires equality with that family's complete pitch-class set. Core-palette validation and foreground/voicing construction are separate claims. `validate()` checks finite bounds, pitch range, overlap limits and redundant reattacks; it does not assert that every foreground subset independently passes H01.

## Evidence and listening

[Full 5:36 REAPER example, comparison and limitations](../../productions/long-line-v7/README.md).

The reference comparison uses the study's supported pitch-prominence trajectories in six tracks, with thresholds 0.28, 0.40 and 0.55. These include masking and processing changes; they are not exact played-note clocks. The two-second neighborhood is a compositional direction supported in some registers, not a universal rule.

Tests cover reproducibility, seed variation, 100 bounded realizations, continuity across fields, rejection of invalid timing/density, cell diversity, and MIDI channel/note/bend lifecycles. Passing those tests does not establish musical quality.
