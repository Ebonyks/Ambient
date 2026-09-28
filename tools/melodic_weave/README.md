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

## Tonal-review correction (v8)

The v7 always-on upper B and nearest-palette mapping created repeated B-C-B figures. Sustained chromatic tension in the reference study was not evidence for that melodic habit. For new candidates, use `--friction-pc -1`, then run the local revision pass:

```powershell
python tools/melodic_weave/refine_voicing.py my-sketch.json --harmony productions/long-line-v6/harmony.json --out my-sketch-refined
```

This preserves event timing and source count, removes repeated A-B-A semitone-return figures, and keeps isolated one-way semitone movement and simultaneously sustained semitone pairs. It is an owner-directed construction constraint for this piece, not a claim about everything Hecker composed. The v8 script also supplies an authored replacement for the 2:48 passage. Fifteen tool tests now include this regression and 100 seeded refinement cases. [Tonal revision and actual plugin chain](../../productions/long-line-v8/README.md).

## Inner texture mode (v2)

The new **texture_weave.py** mode separates the existing slow scaffold from fast inner note activity. It addresses a limitation of v1: more local voice changes still did not create the multi-note interior of a sustained sound. The original generator and its six-source validator remain unchanged for reproducibility; the new score has its own construction validator.

```powershell
python tools/melodic_weave/texture_weave.py --scaffold productions/long-line-v8/weave.json --harmony productions/long-line-v6/harmony.json --out my-inner-study --density 1 --level 1 --seed 260928
```

`--density` accepts 0.25-1.5 and changes the four independent inner clocks; `--level` accepts 0.25-1.5 and adjusts proposed velocity. The existing scaffold is unchanged. Lower MIDI velocity does not guarantee a quieter sound on every VSTi: calibrate the instrument response and the inner bus in audio. FB-3300 in particular needs envelope/lane gain rather than assuming velocity response.

The grammar uses persistent unequal-length broken-chord cells, single-position mutations, bounded registers, local-field pitch membership, stable tuning and staggered transitions. It permits repeated same-key notes only after the prior note-off. It forbids the rejected semitone-return habit without banning simultaneously sustained tension. The score reaches 13 overlapping keys under an 18-key guardrail; released acoustic tails are additional. MIDI type 1 keeps all eight voices separately editable, preserves the original tuning with safe bend ownership, and includes no tempo-synchronized arpeggiator or drum part.

Default output: 2,698 inner notes plus 123 retained scaffold notes over 336 seconds. These are authored design settings, not measured Melnyk/Fourman note counts. Event density, pitch vocabulary, simultaneous key count, perceived density and harmonic change rate are separate quantities.

[Audit, Bandcamp source record, listening evidence, MIDI and rendered examples](../../productions/long-line-v9-study/README.md). The source and MIDI construction checks pass; perceived improvement of the combined example remains unconfirmed. Test coverage is now 22 tests, including 100 texture seeds across density extremes and eight-track note/bend lifecycle checks.

## Optional context blend revision (v2.1)

`python tools/melodic_weave/blend_texture.py input-texture.json --out revised-texture` checks inner voices against actual overlapping notes with a one-second release guard. It avoids added 1-2 semitone neighbors in the same register, retains the scaffold, and omits impossible notes. This is a conservative piece-specific experiment, not a universal harmony rule or an acoustic release simulation. The original v2 remains reproducible. See [rendered revision and limitations](../../productions/long-line-v9-blend/README.md). Four new regression tests bring melody/texture coverage to 26 tests.

## Continuous field mode (v3)

`python tools/melodic_weave/continuous_field.py --out my-flow` builds an original performance from Long Line's seven harmonic fields. Four nearly even clocks distribute pitch activity while register changes on a 150-second arc and neighboring harmonic weights cross over 24 seconds. The old foreground is retained only in JSON provenance, and excluded from performed MIDI notes. This mode replaces the foreground hierarchy rather than adding another background layer. Its pitch occupancy and constant velocity do not establish acoustic salience. See [rendered candidate, negative listening evidence and limitations](../../productions/long-line-v10-flow/README.md).

## Differentiated fast lines (v4)

`python tools/melodic_weave/flowing_lines.py --out my-lines` replaces randomized common-register selection with four different persistent contour grammars, nominal rates four times v3, and an authored 12-second harmonic itinerary. It is intentionally scoped to this 336-second Long Line arrangement. Its performance MIDI omits the retained reference foreground. See [reference listening, native patches, mixed measurement evidence and draft](../../productions/long-line-v11-lines/README.md). MIDI rate is not perceptual speed; the new output remains pending owner review.
