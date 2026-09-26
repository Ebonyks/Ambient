# Measured Hecker reference package

Open Tim_Hecker_Production_Study.html (self-contained, with charts), or read the Markdown.
study.json is the canonical combined annotation/metadata artifact. CSVs are convenience exports.
Source audio, transient download URLs and the Python environment are deliberately not packaged.

## Array files
- data/ID.npz: half-second raw candidate activation, direct_fund, chroma, direct_chroma, rms (dBFS), centroid (power-weighted Hz), flatness, side (side/mid dB), novelty, midi, hop_s.
- data/ID_envelope.npz: time_s, mono_rms, left_rms, right_rms, band500_4000_rms, attack_candidate_times_s. RMS values here are linear amplitude, not dB.
- data/ID_targets.npz: time_s, midi, target_relative_activation, target_support_mask, target_frequency_hz, target_weight. Read the report's target semantics before using these as labels.
Arrays are pitch x time where applicable; all clocks are track-relative seconds.
Zero mask values mean unaccepted/unresolved, not ground-truth absence.

## Re-running extraction
Use Python with numpy, scipy, soundfile, librosa==0.11.0; matplotlib==3.10.8 and markdown2==2.5.4 build the report.
The scripts preserve the actual run's directory conventions: place them in a work folder beside audio_analysis/.
Create audio_analysis/manifest.json as a list of objects with album (radio_amor/mirages/mort_aux_vaches), track_num, title, duration, page, stream_sha256, source_quality, analysis_wav_path. Point analysis_wav_path at your own decoded 22,050-Hz stereo WAVs. Retain MP3 hashes only if you analyze the same source bytes.
Create audio_analysis/features/. Run analyze_streams.py, refine_partials.py, envelope_analysis.py, match_live.py, verify_matches.py in that order. The analyzer caches existing outputs; use a fresh folder to change extraction parameters.
The source-specific verify_matches.py probes the documented candidates; it is not a general discovery algorithm. validate_analysis.py creates the three pitched toy probes. Run validate_noise.py to generate and refine the fourth white-noise probe. It is not an album track.
Run build_measured_study.py after the analysis and validation outputs exist. It writes a new Hecker_Measured_Study folder and ZIP. Historical interpretation text is stored in track_interpretations.py and must be reconsidered if source editions differ.

No original stems, verified MIDI score, trained model or validated timbral reconstruction is included. Patch parameters are proposals, not claims about Hecker's original sessions.
