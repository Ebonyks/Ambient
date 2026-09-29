# Harmonic construction protocol v1

Radio Amor · Mirages · Mort aux Vaches

The target is a **recognizable relationship between a persistent pitched object and changing distortion, masking, register and temporal density**. The source harmony should remain recoverable without having to behave like a conventional chord progression. This protocol converts the previous measurements into compositional choices and executable constraints.

Its central recommendation is to compose a small object, preserve selected voices, and change the way the object is exposed. Major harmony is allowed. Minor harmony is allowed. Stable dissonance is allowed. What the default protocol resists is automatic tonal correction, constant replacement of all voices, and a regular cadence that makes every tension sound like a promise to resolve.

This is a bounded protocol for the three reference recordings, not a universal rulebook for Hecker's career. “Allowed” means supported enough to include in this designed vocabulary. “Not allowed” means excluded from strict generation until explicitly reviewed. It does **not** establish that the artist never used a chord. The underlying audio analysis identifies spectral components imperfectly; a source-chord interpretation can remain provisional even when the component frequencies are clear.

Source: [the complete measured study at its pinned revision](https://github.com/Ebonyks/Ambient/blob/163d5a9d79c12476bbc7fad41ca4f59397ebf66d/studies/tim-hecker/Tim_Hecker_Production_Study.md). The machine protocol records the SHA-256 of that study's JSON. Numeric generator limits and probabilities below are **design proposals**, not parameters learned from Hecker's sessions.

## 1. Synthesis: what recurs, and what should govern construction

### A. The harmonic object is smaller than the apparent sound mass

The measured tracks repeatedly expose a dyad, open fifth, triad or small extended collection under a much larger spectrum. Examples include D/A in Spectral; A/E in Non Mollare; Eb/Gb in Trade Winds, White Heat; and C/Eb in Incurably Optimistic!. Their dense surroundings do not justify adding a corresponding number of independent MIDI voices.

**Construction rule:** start with two to four source voices. Add an extension only for a specific function: ninth, seventh, suspended tone, neighboring pitch or a change in bass interpretation. Derive density from parallel processing, sustained tails and resampling before adding more harmony. The tool allows up to six source voices as a guardrail, not as a measured maximum in the originals.

### B. Third ambiguity is an active choice

Spectral has D-centered evidence without a consistently established independent F#; Non Mollare has A/E without a securely established C. Adding the conventional third would make each easier to label but less faithful to the available evidence.

**Construction rule:** represent “third absent” explicitly. An open-fifth source must not receive a major or minor third from automatic chord completion. The validator rejects a third inserted into an object labeled `open_fifth`. A major or minor triad remains available when selected deliberately as a different family.

### C. Common tones make change possible without a new musical sentence

The Eb/Gb dyad can belong to an Eb-minor collection or function as D#/F# over B. C/Eb can remain while the bass changes between C-, Ab- and Bb-related contexts. The same inner voices acquire a different harmonic interpretation through the bass and surrounding pitches.

**Construction rule:** prefer one retained voice, better still a retained inner dyad, through most state changes. Preserve its absolute pitch, cents offset and envelope. Reinterpret it with a new bass, remove a fifth, or expose an upper extension. Do not release and retrigger every voice when a JSON state boundary occurs. The MIDI exporter ties exactly shared pitches across those boundaries.

### D. Friction can be the stable object

Azure Azure supports G/Ab and D/Eb pairs; Jimmy places high G against low Ab; Careless Whispers opens with D/Eb. These are not all “wrong notes” awaiting correction. An interval class of one can be a close minor second, a major seventh, or a compound interval, with very different audible consequences.

**Construction rule:** declare the register and role of the friction. A high major seventh above a low anchor is different from two adjacent bass resonances. Keep the two components independently controllable. Automatic scale quantization must not collapse the pair into one pitch or resolve it at the next bar line.

### E. Major and minor are local colors, not album-wide identities

I'm Transmitting Tonight includes Bb-major-family and Ab-major-family objects. The Star Compass includes a local F-minor group and a Db/F-like ending. Kaito moves from B-minor material to F#/A material and then a C-minor-seven group. The evidence does not support “use a minor scale for the entire album” or “major chords are too happy.”

**Construction rule:** choose a local pitch object, not one global scale mask. For a new piece, transpose the relationship freely. Retain register, voice persistence and tension behavior; do not reproduce the source track's complete time-and-pitch sequence merely to satisfy the style target.

### F. A parallel shift and a functional progression are different operations

Song Of The Highwire Shrimper supports an A/D/B/E family and a roughly semitone-lower Ab/Db/Bb/Eb family. This can be modeled as displacement of an object while its internal relations survive. It need not be given a dominant or leading-tone explanation.

**Construction rule:** occasionally move the complete object by one semitone. Preserve interval structure and processing continuity. This is one allowed way to make a strong change without requiring common tones. It should be a deliberate change of scene, not an automatic move every few seconds.

### G. Live variation can preserve source time

The strongest Celestina and Balkanize-You comparisons maintain near-constant live/studio offsets over the tested spans. The performance differs even where local source timing is retained. This favors live control of layered material over the assumption that live recomposition must alter tempo or rewrite all notes.

**Construction rule:** construct playable buses from the same pitched objects: body, upper detail, distorted return and residue. In a performance, allow a source to continue while its mix, filtering, resampling and overlap change. The exact historical bus architecture is not established; this is a practical design derived from the observed relationship.

## 2. Quantitative trends and their limits

The following table counts **whether an interval class is present** among accepted spectral candidates in each half-second frame. Denominator: duration of frames containing at least two distinct accepted pitch classes. Columns can overlap and do not sum to 100%. Octave duplicates are collapsed before interval counting.

| Interval class | Musical relations represented | Radio Amor | Mirages | Mort aux Vaches |
| --- | --- | ---: | ---: | ---: |
| 1 | Minor second / major seventh | 51.1% | 36.9% | 47.9% |
| 2 | Major second / minor seventh | 31.5% | 37.5% | 39.4% |
| 3 | Minor third / major sixth | 41.0% | 45.7% | 37.0% |
| 4 | Major third / minor sixth | 41.8% | 38.3% | 35.6% |
| 5 | Perfect fourth / fifth | 56.8% | 54.3% | 54.4% |
| 6 | Tritone | 13.2% | 13.2% | 8.0% |

These percentages are **not chord frequencies or played-note probabilities**. Harmonics, resonances and intermodulation can pass the detector. The dataset also retains only selected candidates and uses section-level peak support, so it is not an unbiased census of polyphony. Fifth relationships are particularly vulnerable to harmonic-series confounds. The live recording reuses studio material and must not be treated as an independent third sample when estimating prevalence.

At the baseline gate, the median count is two accepted pitch classes per frame for each album. Raising the relative-activation threshold from 0.28 to 0.55 reduces that median to one. Thus “exactly two notes at a time” would be a false rule. The stronger conclusion is that a small number of prominent components can carry the identity of a much denser sound.

Across that same threshold change, interval-class-1 presence ranges from 43.4–51.1% in Radio Amor, 31.7–36.9% in Mirages, and 41.5–47.9% in the live recording. The major-third/minor-sixth class remains present as well. The useful qualitative conclusion survives: chromatic friction coexists with consonant relations; neither a strictly diatonic generator nor a minor-only generator captures the reference vocabulary. The precise percentages should not be used as transition weights.

The baseline median register span among multi-pitch-class frames is 16 semitones for Radio Amor and 12 for the other two recordings; this contracts substantially at higher thresholds. This supports explicitly modeling register, but not a universal minimum spacing. Complete baseline and sensitivity results are in [corpus_statistics.json](corpus_statistics.json); [build_protocol.py](build_protocol.py) reproduces them from the published arrays.

## 3. Allowed harmony vocabulary

Pitch-class sets below are offsets from a **reference pitch**, not a claim of functional tonic. A template can be transposed. Registers in the examples are intentional. A source family is a palette: sustained tails and staggered entrances are still required to decide what is simultaneous.

| Family | Relative pitch classes | Concrete permitted example | Why it belongs / condition |
| --- | --- | --- | --- |
| Open fifth | 0, 7 | A1–E2–A2 | Non Mollare-type A/E object; omit the third |
| Suspended second/ninth | 0, 2, 7 | A2–E3–B3 | A/E/B relation in Highwire; no automatic C or C# |
| Suspended fourth | 0, 5, 7 | D2–G2–A3 | D/G/A relation in Spectral; no assumed major third |
| Second + fourth field | 0, 2, 5, 7 | A2–D3–B3–E4 | Sparse realization of Highwire's A/D/B/E palette |
| Minor-third kernel | 0, 3 | Eb3–Gb3 | Trade Winds inner dyad; can be reinterpreted over another bass |
| Minor triad | 0, 3, 7 | G2–Bb2–D3 | Strong local reduction in Aerial Light-Pollution Orange |
| Minor seventh | 0, 3, 7, 10 | C2–Eb2–G2–Bb2 | Kaito ending; do not infer a subsequent dominant |
| Minor ninth field | 0, 2, 3, 7, 10 | G2–D3–Bb3–F4–A4 | Celestina opening collection; full simultaneity remains provisional |
| Major triad | 0, 4, 7 | Ab2–Eb3–C4 | I'm Transmitting Tonight; major quality is explicitly permitted |
| Major seventh | 0, 4, 7, 11 | Bb2–F3–A3–D4 | Same track when A is part of the sounding object |
| Major add ninth | 0, 2, 4, 7 | Ab2–Eb3–Bb3–C4 | Ab-bass interpretation of Incurably Optimistic!'s upper object; local reading |
| Distant major-seventh dyad | 0, 11 | Ab2–G5 | Jimmy-type register-separated friction; upper pitch is not resolved by default |
| Upper semitone | 0, 1 | D2–D3–Eb3 | Conditional: a deliberate exposed D/Eb relationship, not random detuning |
| Paired semitones | 0, 1, 7, 8 | G3–Ab3–D4–Eb4 | Conditional: Azure-type friction; control both pairs separately |
| Low semitone field | 0, 1 | G1–Ab1 | Conditional: Aerial Silver-type low texture; use the dedicated profile |

The familiar chord labels are convenient reductions. They are not instructions to use a lush keyboard preset at every moment. For example, Gm9 can be distributed as low G/D, a quieter Bb/F body and a intermittently exposed A. The top extension should have its own gain envelope rather than being locked to the bass attack.

The conditional low pair is especially sensitive to treatment. Equal-tempered G1 and Ab1 differ by about 2.9 Hz, so two sufficiently clean sustained components can beat at that difference frequency. Broad noise excitation and distortion can change that behavior substantially. The exact source peaks in the study are preferable when reconstructing the reference; equal temperament is a starting point for an original sketch, not a recovery of the measured detuning.

## 4. Not allowed in strict mode, and what the exclusion means

### A. Excluded compositional operations

| Operation excluded by default | Reason for the protocol | Better construction |
| --- | --- | --- |
| Automatically fill an open fifth with a third | Converts an intentionally ambiguous object into an unsupported major/minor statement | Keep the third absent; choose a triad explicitly only when desired |
| Snap every voice to one album-wide scale | Deletes the measured chromatic pairs and local collection changes | Use local objects; preserve neighboring tones |
| Resolve every semitone or major seventh immediately | Turns stable friction into conventional suspension/leading-tone behavior | Sustain the conflict or alter its prominence |
| Declare a recurring ii–V–I or dominant–tonic cadence as the default engine | This grammar is not established by the reference study and redirects attention toward tonal arrival | Change bass interpretation, common tones, register or object displacement |
| Replace all voices at every regular bar boundary | Loses the persistent inner object | Retain at least one voice for common-tone transitions; reserve total replacement for deliberate scenes |
| Read all peaks in a section summary as one chord | Combines sequential notes, tails and harmonics into invented dense harmony | Use the time-dependent activity and sparse candidate objects |
| Write three or more adjacent chromatic bass voices below C3 as a default source block | Goes beyond the deliberately restricted low-friction model | One low neighboring pair, or separate the extra conflict into a higher register |
| Treat distortion sidebands as additional performed MIDI notes | Confuses processing with composition and compounds density | Keep sidebands in the effect return |
| Treat repeated grain/envelope motion as proof of a beat grid | Gives internal texture a meter not established by the analysis | Maintain separate source, texture and arrangement clocks |

Some of these are automatically checked only when encoded in the sketch. The validator checks declared cadence plans; it does not hear a MIDI/audio file and discover all functional harmony. Scale snapping, perceptual resolution and phrase regularity still require renderer/composition review. The protocol is explicit about this boundary.

### B. Chord families not enabled without review

The following are not available as primary source objects in strict v1: fully diminished seventh `{0,3,6,9}`, half-diminished seventh `{0,3,6,10}`, diminished triad `{0,3,6}`, augmented triad `{0,4,8}`, a complete whole-tone collection, large chromatic blocks, or an arbitrary quartal stack with no reference anchor.

This is a **closed-vocabulary design decision** based on insufficient specific source support, not evidence that these sounds are absent from the recordings. Distortion can produce their component relations, and the measured tritone is plainly not zero. A tritone interval is therefore not globally prohibited. To add one of these families, record an exact source window, register, independent component evidence and intended function; then update the family and test its behavior in context.

An isolated dominant-seventh or dominant-extension object requires particular care. The late Balkanize-You reading allows a provisional G-dominant extended interpretation from G/F/B/A/E-related material. That does **not** justify a blanket ban on dominant color, nor does it establish a functional G7→C cadence. V1 leaves that source family in review while explicitly excluding a declared cadential engine. This distinction matters more than the chord name.

## 5. Voice-leading grammar: permitted transformations

Treat a harmonic state as `(reference pitch, source voices, register, tuning, sustained identity, processing state)`. A new state may change only some of those fields.

| Transformation | Operation | Example | Preserve |
| --- | --- | --- | --- |
| Retain / reveal | Same notes; change foreground, noise and distortion balance | Hold C3/Eb3 while the upper layer emerges | Pitch, cents and sustained envelope |
| Bass reinterpretation | Keep inner dyad; change the lower anchor | Eb3/Gb3/Bb3/Db4 → B2/Eb3/Gb3 | Eb3 and Gb3, not necessarily all upper tones |
| Add or remove extension | Introduce a seventh/ninth without replacing the core | G2/Bb2/D3 → G2/Bb2/D3/F3/A4 | The triad and its articulation history |
| Register exchange | Move one exposed voice by an octave | D3/Eb3 → D3/Eb4 | Pitch classes; acknowledge changed roughness |
| Parallel displacement | Move the entire object ±1 semitone | A/D/B/E → Ab/Db/Bb/Eb | Relative intervals and continuity of treatment |
| Scene replacement | Switch to another object after a long span | B-minor family → F#/A → C-minor-seven family | Deliberate long-form placement, not a mandatory common tone |

The shipped generator implements retained objects, common-tone revoicing and occasional parallel semitone displacement. Custom authored JSON may express scene replacements; these receive review warnings when no common tone is retained. The generator does not claim to reproduce the reference tracks' full transition probabilities or durations.

For a practical original 3–4-minute sketch, begin with a 30–70-second pitch object, retain it through one processing change, add/remove one color voice, and make at most a few strongly audible harmonic replacements. Those numbers are compositional initialization choices. They are not statistics of the 233 analysis windows, which include artificial 90-second caps and are not all musical phrases.

## 6. Construction protocol beyond the chord list

1. **Choose the identity:** one kernel, one register arrangement, and one friction or omission. Example: a low fifth plus a distant major seventh. Name what must remain audible even after processing.
2. **Render the source cleanly:** separate anchor, inner body and color. Use the original study's P1 struck-source, P2 resonator, P3 guitar-like or P4 sustained source proposals. The instrument resemblance is a means of constructing the sound, not a verified track credit.
3. **Preserve a pitched route:** duplicate the body before saturation. Keep a cleaner path so the harmonic object survives changes to the distorted return.
4. **Create mass in the return:** use distortion, filtered noise and resampling with independent gain. As a starting range, place the distorted return 18–6 dB below the dry reference and the noise source 30–18 dB below it. These are explicit proposal ranges, not measured original stems.
5. **Separate the three clocks:** long harmonic-state duration; entrances and tails of source material; internal grain/buffer motion. Grain motion need not retrigger harmony. A note object may last a minute while its internal texture changes dozens of times.
6. **Expose and mask selectively:** vary the color layer by about 10 dB over a state, move the return level, or change which register is clear. The JSON records targets; interpolate controls over 5–20 seconds rather than making every boundary a hard mixer jump. That interpolation time is a proposal.
7. **Carry common voices across changes:** avoid retriggering or randomly retuning them. The generator assigns each MIDI pitch a stable ±4-cent offset for the sketch. This small range is a neutral initialization, not a model of the recordings' larger and inconsistent offsets.
8. **Review harmony and timbre separately:** first check the skeleton, then the processed rendering. A correct pitch set through an unrelated polished pad can fail the perceptual goal. A convincing noise texture over arbitrary chords can also fail it.

Source and processor choices are not interchangeable with chord names. P1 can articulate a suspended field; P4 can sustain the same field; P3 can obscure it. A source family does not imply one VST. The original study supplies parameterized patches and distinguishes the historically documented environments from proposed substitutions.

## 7. Executable tools

Files:

- [protocol.json](protocol.json): 15 transposable source families, four profiles, nine rule IDs, source provenance and proposed parameters.
- [harmony_tool.py](harmony_tool.py): deterministic generator, validator and microtuned MIDI exporter. Standard library only.
- [test_harmony_tool.py](test_harmony_tool.py): acceptance/rejection, determinism and MIDI structure tests.
- [corpus_statistics.json](corpus_statistics.json): interval presence and threshold sensitivity.
- [build_protocol.py](build_protocol.py): rebuilds the vocabulary metadata and statistics from the measured study; requires NumPy.
- `examples/`: four original four-minute harmonic sketches, each as JSON and MIDI, plus their validation report.

Run from this directory:

```text
python harmony_tool.py generate --profile radio_suspended --seed 41 --duration 240 --out my_sketch
python harmony_tool.py generate --profile mirages_pressure --seed 52 --duration 240 --out pressure_sketch
python harmony_tool.py validate my_sketch.json
python -m unittest -v test_harmony_tool.py
```

The other profiles are `common_tone_clarity` and `low_beating_field`. Profile names describe construction priorities, not trained artist classifiers. The output contains transposed original combinations; it does not copy the source recordings or their full sequences.

The MIDI uses 60 BPM solely as a seconds-to-ticks carrier, with 480 ticks per second. **It does not assert that the music is in 60 BPM or any meter.** Common pitches tie across states. Each active voice has its own MIDI channel and pitch bend; the file requests a ±2-semitone bend range using RPN. Some DAWs/instruments ignore those messages. Confirm that separate channels and the bend range survive import before using the cents offsets. A single-channel import can corrupt the tuning.

JSON is the authoritative sketch. `automation_targets` are intended renderer controls and are **not executed by the MIDI file**. MIDI supplies a harmonic skeleton, not the complete sonic result. Route the voices to the proposed sources, implement the parallel buses, and interpolate the automation targets in your DAW or synthesis engine.

`passed: true` means conformance to these encoded rules. It is not evidence that an audio rendering sounds like Hecker. The tests cover 100 generated sketches across the four profiles, deterministic output, allowed major harmony, rejected chord completion and unlisted families, conditional low friction, transition declarations, declared cadence plans, finite time and balanced MIDI note events. They do not measure perceptual similarity.

## 8. How to improve the protocol rather than merely accumulate rules

The present study has positive references but no annotated comparison corpus of music judged outside the target style. Consequently, it cannot statistically establish a list of forbidden chords. The exclusions above are design hypotheses that should be evaluated, not disguised as learned laws.

Use controlled render comparisons: hold source sound, loudness and duration fixed while changing one structural property. Compare persistent versus retriggered common tones; retained versus automatically resolved friction; sparse versus fully filled voicings; and independent layer motion versus identical envelopes. Separately compare the same harmony through different processing chains. This distinguishes a useful harmonic rule from a preference for a particular distortion sound.

For machine evaluation, retain the previous study's supported-component, envelope, spectral and stereo targets, but group studio/live source matches in the same train/test partition. Do not use compliance with this protocol as the ground-truth label for “sounds like Hecker”: that would only teach a model to repeat the rules. Obtain independent blinded judgments of rendered outputs and include counterexamples that break one rule at a time. Judge harmonic continuity, friction behavior, register, source articulation and processing development separately.

The next revision should promote, relax or remove a rule based on those results. A dominant-color object that performs well should be added with its intended noncadential behavior. A supposed required spacing that performs poorly should be revised. The purpose is a useful construction system with inspectable evidence, not a collection of prohibitions immune to listening.

## 2026-09-27 scoped composition extension: inner note activity

The owner requested a separate dense-but-subtle inner arrangement informed by Melnyk and Fourman. V1's small primary harmonic objects and six-source guardrail remain the core-palette/scaffold rules. They are not a universal ceiling on performed notes, repeated articulations or released resonance. The opt-in [texture mode](../../tools/melodic_weave/README.md#inner-texture-mode-v2) preserves those fields and the corrected scaffold, while adding rapid inner realizations of the same pitch classes under a separate validator. Its 18-key limit and activity defaults are authored guardrails, not claims about the reference recordings. This extension neither changes the strict family validator nor licenses interpreting every spectral peak as another source note.
