# Composition audit: note activity inside a tonal surface

This audit updates the original composition tool; it does not claim that a plugin or more MIDI notes alone establishes artistic success. Reference review is bounded to four 20-second windows, supported by artist/label statements and reproducible signal measurements. It is not a whole-catalogue audit or recovered score.

## Reference evidence and its limits

- **Lubomyr Melnyk, Parasol, 2:00-2:20 and 6:00-6:20**, from [Rivers and Streams](https://lubomyrmelnyk.bandcamp.com/album/rivers-and-streams). The public Bandcamp MP3 stream was used; the paid lossless album was not purchased. Gemini describes rapid discrete attacks and repeated inner figures over slower harmonic movement in both windows. The attacks remain conspicuous: this is not evidence that all dense playing is perceptually hidden.
- Melnyk's own [Continuous Music explanation](https://www.lubomyr.com/continuousmusic.html) describes rapid patterns/broken chords, sustained pedal, and independent hand patterns combining into continuous sound. The transferable idea is multiple temporal scales, not an instruction to copy a piano passage or match a speed record. His broader claims about digital sound are not adopted as engineering facts here.
- **Eric Fourman, Refrigerate, 2:00-2:20**, from [Wander To The Moon](https://ericfourman.bandcamp.com/album/wander-to-the-moon). The artist credits processed baby-grand piano. The excerpt review describes sustained, blurred resonance and subtle inner harmonic movement. It does not establish a high count of underlying played notes.
- **Eric Fourman, Heed, 2:00-2:20**, from the same album. The artist credits a live field-recorder performance using Microkorg and Prophet 08. The excerpt review describes reedy sustained tones and local activity. The record does not disclose the exact voicings or processing settings.

The Fourman album was successfully acquired through its artist-offered **Free Download** route in FLAC. Both artists' recordings remain all-rights-reserved, are stored locally outside this repository, and are not sampled in the example. Stable links, source hashes, quality and time windows are in Audit/reference_sources.json; signed download tokens are excluded.

## Measured reference comparison

| Excerpt | Spectral-flux peak rate at thresholds 1 / 2 / 3 MAD above median | Median spectral-chroma similarity across 2 seconds |
| --- | --- | --- |
| Parasol 2:00 | 7.55 / 6.90 / 6.75 per second | 0.710 |
| Parasol 6:00 | 7.60 / 7.35 / 7.30 | 0.828 |
| Refrigerate 2:00 | 7.70 / 4.85 / 2.45 | 0.744 |
| Heed 2:00 | 7.65 / 5.00 / 2.95 | 0.828 |

These are **spectral articulation proxies, not note counts**. The much greater threshold sensitivity in Fourman is a reason not to turn every fluctuation into a performed note. Chroma includes harmonics and processing and cannot certify source chords or exact harmonic-change times. Measurement implementation and parameters are in Scripts/reference_analysis.py. Original audio is needed to reproduce it locally.

## Findings in our current tool

| Finding | Consequence | Change |
| --- | --- | --- |
| Three slow strands plus anchor; only 123 source events over 336 seconds | No separate layer for fast internal activity | Four additional inner-pattern lanes with independent clocks |
| Six simultaneous source notes treated as a general density limit | Conflates stable harmonic vocabulary with number of performed events | Preserve the old core validator; give the texture score a separate 18-key ceiling, reaching 13 here |
| Texture richness largely delegated to grain repetition and effects | Processing can color notes but cannot supply authored internal voice relationships | Persistent broken-chord cells, register-separated lanes, gradual single-position cell changes |
| New notes could simply become another foreground melody | More count does not guarantee subtlety | Low MIDI velocities, softened native envelopes, calibrated lane prints, exposed/combined diagnostics and explicit bus levels |
| Prior nearest-palette mapping produced semitone rocking | Sustained tension became a repetitive melodic habit | Keep v8's corrected scaffold and forbid A-B-A semitone returns in each new lane |

## Implemented design

The original seven harmonic fields and 123 scaffold events are unchanged. The new mode adds **2,698 original inner events**, with zero cents offsets, drawn only from each field's pitch classes. Sounding releases may carry across a boundary. Registers and octave distribution create changing realizations of that palette; extra dissonant pitch classes are not invented to inflate complexity.

Four cycles of 5, 7, 9 and 7 positions proceed at unequal rates. Every third cycle changes one position. On a field transition, each lane enters near its previous pitch at its own next onset. Slow rate curves and small timing variation prevent a shared repeated accent. This is a deterministic designed grammar, not an artist-trained model. No swing grid, drum part or periodic pitch LFO is added.

The default activity is about 8.30 new events per active second. Rates, velocity range, register bounds and overlap limits are **authored defaults**, not recovered reference parameters. Higher density reduces the proposed velocity by a square-root factor, but velocity is not calibrated loudness and this does not prove energy invariance. Renderer gain calibration remains necessary.

MIDI is type 1 with eight named tracks and fixed voice channels. The exporter configures pitch-bend range, rejects same-key overlap on the same lane, preserves note-offs and refuses overlapping unequal bends on a voice. The existing generator remains reproducible; the new mode is additive and opt-in.

## Render review

The 96-second study covers v8 at 2:20-3:56, including the previously weak passage. It contains 809 inner events, performed by two TyrellN6 instances and two FB-3300 instances, with ReaEQ and a small Surge Reverb 2 blend. Tyrell velocity response is enabled. FB-3300's architecture does not supply ordinary per-note velocity dynamics; its salience instead comes from its envelopes, register and calibrated lane/mix gain. Neither instrument uses deliberate pitch modulation; chorus is disabled. A listening-model description of pitch modulation is not evidence that the patch contains it.

Candidate A's -12 dB inner bus was too cautious to distinguish in Gemini's paired review. Candidate B reduces the old bed to 0.92 and raises the inner bus to 0.45 (about -6.94 dB before its reverb mix). The central residual is measured at -9.64 dB relative to the unscaled scaffold; its waveform is demonstrably changed. The paired model review still called them virtually indistinguishable, although a standalone B excerpt described interlocking pitched swells. **These inconsistent descriptions do not establish perceptual improvement.** B is a review candidate, not accepted superiority.

The exposed inner-layer audio and three-part diagnostic make the construction inspectable without relying on the model's verdict. Remaining issue: overlapping inner notes can still add low-mid masking. The next musical acceptance question is whether the layer reads as internal harmonic life, rather than extra thickness; increasing event count is not the acceptance test.

Final demo B: 96 seconds, 48 kHz/24 bit, -20.39 LUFS, -5.60 dBTP, no clipping/nonfinite samples. 22 melody/texture tests and 10 harmony tests pass, including 100 new seeded texture trials. Cumulative successful Gemini listens: **98/100**, with two reserved. Four reference listens and five original-material reviews were used in this task.
