# Baseline audit: Long Line, revision 5

Authority: Ambient handoff at 6e33f20; harmony protocol v1; measured study source at 163d5a9. This is an audit of an original composition against a designed protocol, not a claim to match an authenticated Tim Hecker session.

| Criterion | Baseline finding | Expansion action / evidence |
|---|---|---|
| Small source object, H04 | The score lists four-note harmony, but body, motif, contrary line, fixed fifths, bowed voice and articulation can coexist. Source-event count is not the number of spectral peaks. | Four-note core states; remove the separate contrary/fixed-fifths/gesture layers. Main motif and its decays remain separate. |
| Accurate harmony labels, H01 | Bm11 written B/F#/A/D lacks E; G6/9 written G/G/B/D lacks E/A; Aadd9 lacks B; Fmaj7#11 lacks B; Bbmaj7#11 lacks E/A; closing D6/9 lacks B/E. Melodic overlap can add pitches, but these labels do not describe the written body by themselves. | Explicit MIDI/cents/role JSON with exact family validation; do not repair labels by filling all omitted notes. |
| Common-tone identity, H03/H06 | Same nominal pitches were separately regenerated in each chord, with randomized grain detuning and new envelopes. | Render each contiguous shared MIDI/cents identity once. 28 state entries become 19 actual events. |
| Pitched route before distortion | Main and accompaniment were already nonlinear audio stems; limited independent access to a low anchor or cleaner sustained core. | New anchor bypasses drive. Tied inner voices, motif route and distorted branches remain separately controllable. |
| Register and center | Identical extractor gives median power centroid 799.5 Hz and side/mid +1.17 dB. Selected Spectral / Trade Winds / Celestina / Incurably references are 274–461 Hz and -4.17 to -1.79 dB. These are descriptive comparisons, not universal targets. | Restore a deliberate low-register anchor; moderate the inherited wide motif; keep the body centered. Do not EQ blindly to a corpus average. |
| Phrase continuity | Revision 5 repairs the 48–59 second cut, but seven short states in the underlying source are still rearticulated; earlier listener reports flag temporary masking. | Seven long states over 336 seconds, complete motif statements, no mid-phrase global withdrawal. |
| Friction behavior | Original score favors major/add-note objects and one minor-plagal return. Dirty processing alone is not the protocol's stable harmonic friction. | Sustained C2 versus B3 for 48 seconds; retain B3 through C-major-seven to E-minor-seven. G-minor span retains the original upper B motif as deliberate compound semitone friction with Bb. |
| Three clocks | Grain timing, rendered note entrances, and repeated level contours became conflated. | Preserve motif source timing; independently sustain the harmonic body; vary returns over 5–20 seconds. |
| End state | Existing 112-second sample is not a full-length arrangement. | 5:36 first full-length draft, with a closing D object and exposed environmental tail. |

## Measurement limits

The baseline was decoded to 22,050 Hz and analyzed with the handoff's unchanged analyze_streams.py, refine_partials.py and envelope_analysis.py, using librosa 0.11.0. All four detected baseline windows contain supported narrow peaks. This is evidence of pitch components, not proof that every detected candidate was played. Mono RMS values from the study are not LUFS targets. The proposed weighted reference loss is not used as a style score: the new composition has different notes and duration and no justified one-to-one source alignment.

The full-length core passes H00–H08 in the shipped validator. That does not validate all audible melodic overlays, rendered timbre, performance intent or perceptual similarity. Those require separate source-event, audio-feature and listening review.
