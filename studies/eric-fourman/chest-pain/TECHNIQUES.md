# Chest Pain: techniques distilled from the verified main line

The owner confirms that the supplied Ableton screenshot is the main line of Eric Fourman's [Chest Pain](https://ericfourman.bandcamp.com/track/chest-pain). This confirmation is accepted. The visible MIDI clip is labelled 1-Addictive Keys. It gives direct compositional evidence; effect processing, exact pitches, velocities and sustain-controller data are not visible.

The [Decreased album page](https://ericfourman.bandcamp.com/album/decreased) describes free improvisation influenced by Chopin, Debussy and Romantic piano. Three new Google audio reviews examined 0:40-1:00, 2:40-3:00 and 5:20-5:40 of the artist's public listening stream. Those 60 seconds are a sample, not a new full-track listening pass. Audio is retained privately for reference and is not sampled or redistributed.

## Main finding

Variation belongs in the musical gesture itself. Our recent generator changes touch on recurring contour cells, but still gives four lines fairly fixed duties. The source supports larger changes in register, contour, density and foreground responsibility, with small performance differences occurring inside those changes.

## Evidence and transferable techniques

| Evidence | Technique to carry into the original work |
| --- | --- |
| The MIDI overview begins with relatively compact upper activity, opens into broader descending/rising shapes and lower clusters through the middle, and later revisits higher activity. This is a coarse reading of the visible contours, not exact pitch transcription. | Compose a registral trajectory for each phrase and section. Let range open, migrate and reconverge; avoid using the same pitch band throughout. |
| The 0:40 review reports rapid upper figures against lower anchors; the 2:40 review reports chordal support, a higher voice and local inner movement. These roles are model interpretations, consistent with the visibly different shapes. | Give parts unequal jobs: support, connecting motion, upper response and resonance. Let those jobs transfer between parts instead of keeping every strand equally busy. |
| The 5:20 review describes a move from spacious chordal material to upper flourishes and a return to sparse support. | Make an octave excursion a directed gesture with a destination and return. Upper harmonies should sometimes anticipate or answer a phrase, rather than recur only on an independent periodic timer. |
| The image contains runs, clustered regions and more isolated shapes, rather than one uniformly repeated visual block. Reviews differ strongly between passages. | Vary phrase length, contour direction, event grouping and local density together. Retain the requested fast surface while redistributing activity among the voices. |
| Reviews describe shifts of emphasis and pauses. The model sometimes labels them as defects; that judgment is not adopted automatically. | Weight the approach, turning point, arrival and release differently. A pause or reduction should follow a musical gesture, not an arbitrary script boundary. |
| The main-line MIDI itself contains extensive motion. The screenshot does not disclose a processing chain. | Build evolving harmonic and melodic behavior in the notes before relying on effects to create interest. Use processing to blend those relationships, without erasing all articulation. |

## What this changes in our tool design

1. Add a phrase-level gesture plan: launch register, direction, turning point, arrival, degree of activity and response voice. These are musical targets, not a fixed arpeggio cell length.
2. At each recurrence retain part of the identity while changing a small musical detail: an internal voicing, the endpoint of a run, a delayed answer, the voice carrying an extension, a compressed approach or a slightly longer release. Timing jitter alone is insufficient.
3. Tie dynamic weight to that plan. Approach notes can gather energy, a passing high note can remain light, and an arrival can settle. Do not treat every high note as an accent or assign an unrelated random crest to every cycle.
4. Preserve the owner's 3.5-second harmonic changes while allowing gestures to cross those boundaries. Carry common tones and alter selected inner voices; a new harmony need not restart all four parts.
5. Replace purely periodic octave-window scheduling with phrase-related upper responses. Preserve the broader range already requested, but give excursions a harmonic purpose.
6. Continue the bounded touch variation as a finishing layer after these relationships exist. The existing repeat-specific MIDI/gain work is useful, but does not yet establish this larger-scale behavior.

These are proposed composition rules distilled for the next revision, not claims that the current v14 render already implements them. No new music render or generator change was made in this study.

## Tone: what is supported and what remains an adaptation

The sampled Chest Pain passages are described by the reviews as articulated piano with substantial differences in brightness and activity, rather than a uniformly neutral drone. The composition can supply the moving interior of our piece. The desired neutral outer tone remains an adaptation informed by Fourman's separate Refrigerate/Heed references and the owner's direction.

The screenshot cannot establish an exact effects chain, pedal technique, note count, key, octave count or tempo. No specific compressor, saturation, reverb or MIDI-humanize setting is inferred from it. Model claims about exact hands, accents and counter-motion are hypotheses until verified against a score or clearer performance evidence. The useful common result is the contrast among gestures and registral roles; descriptive labels are not treated as recovered notation.

## Listening budget

Three additional successful Google listens were used here (109-111 cumulatively). Nine of the new 50-listen allowance have now been used; **41 remain**. The prior allowance and review history remain preserved in the v14 study. See `LISTENING_BUDGET.json` and the raw review files.
