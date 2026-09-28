# Long Line: phrase weight and restrained tone

[Play the revised 96-second excerpt](Renders/Long%20Line%20-%20Phrase%20Weight%20-%2096s.mp3). Editable REAPER session: `Long Line - Phrase Weight.rpp`.

## Every repetition receives a different performance shape

The new `phrase_touch.py` keeps pitches, harmony, event count, fast note flow and upper-octave companions intact. Each of the 1,652 contour repetitions receives its own correlated timing arc (at most 5 ms), changing emphasis (roughly three velocity units), note-length variation (up to 5%), and a three-point gain curve with a variable crest position. Actual lane gain remains within approximately +/-0.65 dB. There is no shared accent or random new melody. Octave companions follow their source notes' timing and touch.

All four native tracks have gain automation, including FB-3300, whose ordinary MIDI velocity does not produce the required touch response. Tyrell also uses velocity. The curves change the weight across each phrase; they do not independently scatter every note. Every repetition has distinct control values. That is verified construction, not proof that the result sounds like a human performance.

## Fourman reference and tone revision

Fresh Google audio reviews examined Eric Fourman's Refrigerate and Heed at 2:00-2:20. Their reports describe restrained attacks and sustained, damped tone. Model descriptions of 'reeds', exact frequency regions and hidden activity are interpretations, not recovered instrumentation or score facts. The earlier source credits and provenance remain in [v9 study](../long-line-v9-study/COMPOSITION_AUDIT.md). No reference recording is sampled or republished.

Tyrell feedback and filter-envelope emphasis are reduced, both synths use less resonance, and Tape drive/saturation/wet mix fall from 34/38/75% to 26/28/60%. Short attack settings and the 3.5-second harmonic cycle remain. The final pass has an enabled 140-Hz high-pass, a broad -6 dB bell at 350 Hz and a -1.5 dB shelf at 2.5 kHz. Native parameter dumps verify these settings. Final output is -19.36 LUFS, close to the previous -19.16 LUFS, and -3.28 dBTP with no clipping. The master is 1.72 to compensate for the reduced output level after tonal cleanup.

The intermediate B export is rejected: a ReaEQ band-type mapping created a notch rather than the intended shelf. C corrects that band type; the final session uses C's verified processing with level compensation. Prior A/B/C sessions are retained as development evidence, not alternate accepted deliveries.

## Listening result remains inconclusive

Six of the newly authorized 50 Google listens were used; 44 remain (108 successful listens cumulatively). The final matched comparison could not establish a less mechanical result. The final standalone review reported noise and low-mid masking that concealed phrase detail. Those negative reports are preserved, not treated as artistic approval. The requested performance variation is implemented and rendered, but audible human-like phrasing and tonal success remain unconfirmed. No claim is made that the listener must hear every subtle difference.

42 melody/texture tests and 10 harmony tests pass. Tests verify unchanged pitch order and harmony, bounded timing, every repetition's distinct controls, deterministic reproduction and gain data for all voices. `Audit/performance_changes.json` verifies four native volume envelopes. This is the existing 96-second source span (140-236 seconds); the full-length updated score/MIDI is supplied, but no newly finished full-length master is claimed.

## Newly supplied Chest Pain reference

The user's screenshot is titled Chest Pain and shows a MIDI clip labelled 1-Addictive Keys in Ableton Live 9 Suite. [Chest Pain](https://ericfourman.bandcamp.com/track/chest-pain) is confirmed as track 3 of [Decreased](https://ericfourman.bandcamp.com/album/decreased), duration 6:38, with Bandcamp album date September 14, 2013. Fourman describes free improvisation influenced by Chopin, Debussy and Romantic piano. This is useful composition evidence distinct from the drone references. Bandcamp does not independently authenticate the screenshot or confirm its instrument. The image was not republished and this recording has not yet been reviewed with an audio model in this revision.

## Reproduction

Run `python tools/melodic_weave/phrase_touch.py productions/long-line-v13-octaves/texture.json --out productions/long-line-v14-touch/texture`, then `Scripts/prepare_demo.py` to export notes and `phrase_gains.lua`. In REAPER run `render_instruments.lua`, wait for its receipt, then `print_lanes.lua`. Run `prepare_demo.py --calibrate` (inherited lane and composite gains), run `build_final.lua` in REAPER, and run `verify_final.py`. Use a new version directory to preserve existing WAVs. Native source project, separate prints and relative session media are included. Plugin requirements and environmental-source provenance remain those of [v13](../long-line-v13-octaves/README.md) and [v6 licenses](../long-line-v6/Sources/LICENSES.md).
