# Instrument and effects audit - Long Line v8

## Historical evidence and the free-tool question

There is no verified complete list of free VST instruments used on the two early records in the sources checked. The historical tools below must not be replaced with a fabricated plugin list.

- In his [2023 AMA](https://www.reddit.com/r/indieheads/comments/136tic9/hi_its_tim_hecker_ama/), Hecker identifies Reaktor and an object he recalls as rAmpler for much of Radio Amor, and describes combining shortwave recordings with melodic fragments. He also describes later ppooll work, but that does not establish its use on the 2001/2003 sessions.
- His [2009 interview](https://cokemachineglow.com/features/interview-timhecker-2009/) describes Max/MSP/Reaktor processing and a progression from clearer Haunt Me textures toward more distortion, including Turbo RAT use in Mirages. This is evidence against treating all eras as a maximum-distortion recipe.
- These accounts identify environments and processes, not recoverable session presets. None of the modern tools below is claimed to be present on those early albums. A percentage of the artist's effects suite cannot be established from this evidence.

## What was actually used here

| Tool | Previous v7 | Revision v8 | Purpose |
| --- | --- | --- | --- |
| Surge XT VSTi | Installed, not used | Actual native REAPER source print | Physically modeled string strand, replacing one piano voice |
| Surge XT Effects: Tape | Not used | Three independent instances | Hysteresis and tape-loss behavior instead of the old tanh-plus-sine wavefolded returns |
| Surge XT Effects: Nimbus | Not used | Dedicated return | Buffered granular texture from existing notes, at zero pitch shift |
| Surge XT Effects: Reverb 2 | Not used | Dedicated short room | Separate diffusion and room buildup, with pitch modulation disabled |
| Valhalla Supermassive | Shared long return | Retained, reduced send levels; modulation depth zero | Long diffuse distance separated from short room |
| Cockos ReaEQ | Not used | Branch-specific filters after tape and on returns | Suppress upper interaction after nonlinear processing; no global master lowpass |
| Custom Python source preparation | Grain piano plus wavefolding | Two revised piano strands; source rendering/normalization | Existing CC0 piano-tail lineage retained; no full-mix distortion formula |

[Surge](https://surge-synthesizer.github.io/) is open source and available without purchase. Its [manual](https://surge-synthesizer.github.io/manual/) documents the string model, Nimbus, and the Tape port of Chow Tape Model. The built-in Tape effect was used, not a separately installed Chow Tape plugin. [Supermassive](https://valhalladsp.com/shop/reverb/valhalla-supermassive/) is free. ReaEQ is bundled with the existing REAPER installation; REAPER itself is commercial.

All selected third-party plugins were already installed and loaded successfully. Installing more binaries was unnecessary to access these new processing methods. V7's cached presence of Surge was not evidence that it had been used in that render.

## Alternatives researched, not used

[Standalone Chow Tape Model](https://chowdsp.com/products.html) provides a more extensive tape interface, but duplicating the already available tape engine was not necessary for this iteration. [Airwindows ToTape6](https://www.airwindows.com/totape6/) offers another free tape treatment; its default flutter would require disabling for this request. Neither was added to the session, and no installer was downloaded. Reaktor/rAmpler was not installed or represented as a free unrestricted instrument.

## Findings that changed the revision

V7 contained 12 three-note semitone-return figures. At 161.766-203.207 seconds, the upper line repeatedly alternated B and C. Eleven targeted pitch edits remove all 12 figures while preserving event start/end times. This is not a ban on sustained semitone tension. The revised middle passage has a directed G-E-G-B-D-E-G contour instead of the B/C rocking.

V7 also increased two distortion branches in the middle. Its added sine wavefolding and parallel boosts are gone. The new physical-string source is printed with no oscillator drift, portamento, or second-string detuning. Nimbus has zero pitch shift; Reverb 2 and Supermassive have zero pitch-modulation depth. Individual component spectra still interact acoustically; these settings do not promise a perfectly stationary spectrum.

Candidate B failed the 0:43 tonal check because its continuously noise-excited string read as metallic buzzing. A pink-noise burst experiment decayed too quickly under the softened attack and was rejected. Candidate C uses continuously fed pink noise with stronger damping, a lower source contribution, less anchor prominence, and stronger branch-specific upper attenuation. A larger plugin inventory alone was not counted as progress.

Exact settings, plugin hashes, source-print data and iteration measurements accompany the project. Plugin binaries are not redistributed. Audio rendered from the new synth is original performance material; the piano/nature sources retain the v6 CC0 lineage.

## Final candidate F and rejected intermediates

Candidate C/D exposed another problem: source levels feeding Tape were too low and the processed foreground lost presence. The stock JS lowpass also did not map its displayed frequency to the intended cutoff; it was replaced with verified ReaEQ settings. Those intermediate mixes are not the delivery.

The final source passes feed Tape at calibrated active RMS 0.126, then normalize each separately printed branch to its musical role. A clipped string export was rejected and reprinted with 18.06 dB of post-effect export headroom before normalization. Final prints peak below 0.14 linear. The saved Calibrated Tape Sources project retains the safe export headroom. These prints contain native Tape and branch EQ; the final mix does not apply Tape twice.

Candidate E restored foreground presence. Candidate F adds a foreground 1800 Hz lowpass and reduces the late anchor to 65% of its preceding envelope value from 4:54 onward. The final mix retains Nimbus, short Reverb 2, Supermassive and return-specific ReaEQ live. The modeled string and tape processing are supplied both as editable source projects and lossless prints. No new metrical rhythmic layer was added.

Final native render: 336 seconds, 48 kHz/24-bit stereo, -20.28 LUFS integrated, -5.11 dBTP, 6.3 LU loudness range; no clipped or nonfinite samples. Eleven new Gemini excerpt reviews bring the cumulative count to 89/100. Final reviews describe soft attacks/minimal harshness but still flag low-mid masking. An earlier paired review made questionable precise-frequency claims and the E review called movement adjacent-note rocking despite the event audit; listening-model descriptions are not a transcription or proof of artist resemblance. Human tonal acceptance remains pending.
