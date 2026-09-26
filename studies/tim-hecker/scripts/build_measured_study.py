from pathlib import Path
import json, csv, shutil, hashlib, zipfile, base64, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import markdown2
from track_interpretations import NOTES, PATCHES

ROOT=Path(__file__).parent
A=ROOT/'audio_analysis'; F=A/'features'
OUT=ROOT/'Hecker_Measured_Study'; OUT.mkdir(exist_ok=True)
for folder in ['figures','data','scripts']:(OUT/folder).mkdir(exist_ok=True)
ALBUMS={'radio_amor':'Radio Amor','mirages':'Mirages','mort_aux_vaches':'Mort aux Vaches'}
IDS=list(NOTES)
TRACKS=[json.loads((F/(i+'.json')).read_text(encoding='utf8')) for i in IDS]
def tm(t):
    m=int(t//60);s=t-m*60
    return f'{m:02d}:{s:04.1f}'
def table(head,rows):
    return '\n'.join(['| '+' | '.join(head)+' |','| '+' | '.join(['---']*len(head))+' |']+['| '+' | '.join(str(v).replace('|','/') for v in r)+' |' for r in rows])+'\n'
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf8')

intro='''# Tim Hecker: measured harmonic structures and production reconstructions

Radio Amor · Mirages · Mort aux Vaches

Audio-derived edition · 26 September 2026

This study analyzes all ten Radio Amor tracks, all eleven Mirages tracks, and the complete 40-minute Mort aux Vaches Bandcamp performance. It treats Mort aux Vaches as a live reworking of Mirages material and tests individual correspondences. The report contains actual pitch-component measurements, octave/register information, time windows, amplitude trajectories and reconstruction parameters. It replaces the earlier conceptual study.

The analysis covers the full duration of every stream computationally. Auxiliary audio-model checks used selected 20-second excerpts, not continuous human listening. The result is a measured production reference, **not an authenticated score or a recovered session file**. Dense distortion, resampling and overlapping decays prevent a reliable claim that every spectral component is an independently played note. Suggested source instruments and patch settings are explicitly proposals; historical equipment claims have separate sources.

## Reading the evidence

Three kinds of statements have different uses:

| Kind | What it establishes | Appropriate use |
| --- | --- | --- |
| Measured | A narrow peak, time-dependent energy, spectrum, or waveform correspondence in this stream | Acoustic matching and reconstruction targets |
| Inferred | A chord interpretation, bass role, likely pitch-field change, or source resemblance | Provisional conditioning labels, with uncertainty retained |
| Proposed | A piano/guitar/organ substitute, grain duration, routing or effect setting | A reproducible starting patch to optimize, not historical attribution |

Times are relative to each track. The live performance has one continuous clock because that is how the label's Bandcamp edition is presented. Sections are detected spectral-change windows, supplemented by 90-second caps; some short adjacent windows therefore are not separate musical phrases. Boundaries have 0.5-second analysis resolution and should not be mistaken for precisely annotated note attacks.

Pitch tables use C4 = MIDI 60 and A4 = 440 Hz. Each component is written as `note: Hz (cents)`; positive cents are sharp of equal temperament. C# and Db, F# and Gb are enharmonic equivalents. Frequencies are interpolated estimates from averaged 65,536-point spectra at 22,050 Hz: the raw bin spacing is about 0.336 Hz. Two decimal places are storage precision, not a claim of that much physical accuracy. Low-register cents are especially sensitive to windowing and unresolved beating.

**The pitch set in a row is a union over its window, not a block chord.** The companion JSON adds one actual half-second candidate snapshot per section; the NPZ files retain the whole activation trajectory. Even coincident peaks can be harmonics of one source. Use the analytical prose to choose a sparse reduction, and use activity data to preserve entrances and overlaps.

The dynamic columns report mean mono RMS dBFS, a **power-weighted** spectral centroid, and side/mid power ratio in dB. These are neither LUFS nor mastering prescriptions. Negative side/mid means more mid energy; it does not identify a reverb plugin. The period column gives a peak in a detrended amplitude-envelope autocorrelation, with its correlation in parentheses. It is a texture repetition candidate, **not a recovered BPM or meter**.

## Source editions and analysis coverage

The inputs are the publicly playable Bandcamp MP3-128 streams, decoded to 22,050-Hz stereo PCM for measurement. They are not lossless masters. Source byte hashes identify the exact analyzed streams in the dataset. Mastering, codec behavior and channel cancellation can affect results, especially noise and high frequencies. Original audio is not included in the deliverable.

- [Radio Amor — artist Bandcamp](https://timhecker.bandcamp.com/album/radio-amor)
- [Mirages — artist Bandcamp](https://timhecker.bandcamp.com/album/mirages)
- [Mort aux Vaches — label Bandcamp](https://mortauxvaches.bandcamp.com/album/mort-aux-vaches-tim-hecker)

'''

equipment='''## Instruments, software and a reproducible signal path

In the contemporaneous 2004 interview Hecker names guitar, piano, processed samples, PCs, AudioMulch, Reaktor, pedals and a mixer. He describes Acéphale as developing from a Blur sample with his guitar added. He also describes composing from recorded live sessions. This supports an instrument-and-resampling workflow, but supplies neither a per-track instrument list nor exact presets. [Textura interview, October 2004](https://www.textura.org/archives/interviews/heckerinterview.htm).

In retrospect, Hecker identifies increasing Turbo RAT use on Mirages. His 2009 Max/MSP/Reaktor and synth/pedals/computer/mixer descriptions refer to that later period; they cannot establish the precise Mort aux Vaches rig. His contrast between studio construction and variable live performance supports treating the recordings as different arrangements. [Cokemachineglow interview, 2009](https://cokemachineglow.com/features/interview-timhecker-2009/).

Asked about Radio Amor in 2023, Hecker recalled a Reaktor object called “rampler i think.” Retain that qualification: this is useful evidence for Reaktor sample processing, not an exact ensemble version or preset. His 2023 description of multichannel stems, analog mixing, buffers and live synth input explains a later performance method, not a verified 2004 wiring diagram. [Artist AMA](https://www.reddit.com/r/indieheads/comments/136tic9/hi_its_tim_hecker_ama/).

There is no verified list of individual VSTs and parameter states for these albums. AudioMulch and Reaktor are environments, not proof of any particular effect chain. The following five patches can be implemented in a modular environment or equivalent sampler, filter, waveshaper and reverb modules. They are deliberately specified by DSP function so that a machine can reproduce the controls without guessing a commercial preset.

Use four independently rendered buses: **pitched body, clearer upper/attack layer, distorted resample, noise/residue**. Assign frequencies before distortion. Split the body before nonlinear processing; route the low anchor around the main distortion where the track recipe specifies it. Sum the distorted branch back under the clearer body. Put ambience after the branch sum, with a separately controllable send from the upper layer. This lets the measured bass, upper voice and noise envelope change independently.

For the proposed drive controls, define a repeatable reference implementation: normalize the source's active RMS to −18 dBFS, set gain `g = 10^(drive_dB/20)`, then use `tanh(g*x)`. Loudness-match the processed branch before setting its mix level. This is a controllable saturator, **not a Turbo RAT circuit model**. Use 4× oversampling for production. Filters in this reference patch are second-order Butterworth unless stated otherwise. Grain windows are Hann; overlap N means a grain starts every grain_duration/N. Position jitter is uniform over ±the listed value; seed = 260926. Grain pitch jitter starts at zero so that stochastic detuning does not erase measured tuning.

For P2, a resonator's −3 dB bandwidth is approximately center_frequency/Q. Q=12 is a broad initial coloration, not enough to synthesize a pure narrow peak by itself: add a sine component at the measured frequency when a stable narrow line is the target. For P4, the four amplitudes specify harmonics 1–4, normalized after summing. Do not infer that an observed third harmonic is a separate MIDI voice.

The quoted reverb decays are proposed RT60 targets; wet values are linear mix fractions. Predelay starts at 18 ms for P1/P3 and 0 ms for P2/P4/P5. Start the wet high cut at 5 kHz and the wet low cut at 150 Hz. These added controls are initialization choices. Measure the rendered result with the same feature extractor before calling the patch matched.

'''

trends='''## Structural patterns that should survive reconstruction

### Radio Amor

The useful grammar is a combination of widely separated registers, recurring inner tones and local displacement. Song Of The Highwire Shrimper has an A/D/B/E family followed by a roughly semitone-lower Ab/Db/Bb/Eb family. Jimmy separates an Ab bass from high G; the major-seventh pitch-class tension becomes spacious because of the register gap. Spectral sustains a D-centered object while the upper material and masking change. These structures require independent voice envelopes, not one MIDI chord tied to one filter sweep.

I'm Transmitting Tonight offers a more conventional reduction: Bb-major-family material against Ab-major-family material. The upper D-to-C change matters, while delayed tails can temporarily retain both. The Star Compass moves through Db/Gb-related material, a local F-minor region and a Db/F-like ending. Trade Winds, White Heat reinterprets the Eb/Gb inner dyad: Bb/Db makes an Eb-minor-seven family, while B below it allows B major. This is parsimonious voice leading through common tones; a new full pad at every change would obscure it.

Several transitions carry a pitch object across a file boundary. The late G/Ab field of the opener relates to Jimmy; the later D/Eb field of Shipyard Of La Ceiba resembles the opening of Careless Whispers. These are measured pitch relationships, not proof that the same original sample was used. Azure Azure expands the paired D/Eb and G/Ab frictions into a long form. Build the semitone pairs as independent channels so their beating, masking and envelope relationship remain adjustable.

### Mirages

The harmonic objects are often obscured by low distorted energy, but there are concrete exceptions: Celestina's G/Bb/D/F/A collection; the later G2/Bb2/D3 triad in Aerial Light-Pollution Orange; Kaito's B-minor, F#/A and C-minor-seven regions; and Incurably Optimistic!'s recurring C/Eb inner voices. These anchors make a useful test set because a reconstruction can be assessed before adding the masking layers.

The Truth of Accountants exposes C/D/E upper material at its end, and the next track begins with related upper material before changing register into G minor. Preserve that source-bank continuity. Non Mollare is an A/E object whose third is not securely established; adding C merely because a classifier says A minor overdetermines the harmony. In Aerial Silver, neighboring G/Ab low components can be better modeled as a beating field than a functional chord progression.

Mirages also shows why “melody” must include voice persistence and emergence. A sustained source can expose an upper tone when distortion, filtering or an overlapping layer changes. That spectral emergence is observable; an original keyboard attack is not thereby proven. The machine representation therefore stores a continuous activation surface and proposed state palettes rather than pretending every bright line is a scored note.

### Rhythm, density and form

No reliable common meter has been established for the corpus. The 20-ms envelopes expose amplitude modulation and attacks; the 0.5-second pitch trajectories describe slower harmonic activity. Keep these separate. A 0.4-second amplitude repetition can arise from loop texture or beating without implying 150 BPM, and an attack detector responding five times per second does not mean five performed notes.

For reconstruction, preserve three clocks: source-note or source-fragment entrances; internal buffer/grain motion; and long arrangement changes. The analysis-window boundaries constrain the third clock. The NPZ activity and envelope data constrain the first two imperfectly. They do not establish grain size uniquely. The patch grain durations are initial hypotheses to be optimized against modulation and spectrum, not measurements of Hecker's buffer settings.

'''

live_text='''## Mort aux Vaches: comparison with the studio arrangements

This is analyzed as one performed sequence, not eleven concatenated Mirages tracks. The public edition supplies no internal track markers. The table below is a source-correspondence map, separate from the finer harmonic windows later in the report. Approximate regions can include overlays and transitions.

| Live region | Studio relationship | Evidence and limits |
| --- | --- | --- |
| 00:00–02:10 | Unassigned opening | No accepted exact source identity |
| Approximately 02:14–07:05 | Neither More nor Less candidate | Repeated pitch/time-feature retrieval; F/C material supports the hypothesis; no accepted waveform alignment |
| Approximately 07:31–12:53 | Aerial Silver candidate | Retrieval favors this source in several windows; noisy G/Ab fields can match other tracks |
| Approximately 14:20–19:05 | Celestina material | Strongly supported reuse in the tested early span; five aligned waveform windows maintain a consistent offset |
| Approximately 19:05–21:56 | Kaito-compatible B/D/F# material | Harmonic compatibility only; source identity remains unconfirmed |
| Approximately 21:42–25:00 | Counter Attack material | Strong feature and low-band waveform matches; repeated source cycles make a unique time map unavailable |
| Approximately 25:54–31:30 | Balkanize-You material | Strong reuse evidence; eight waveform windows from live 26:22 onward agree on a near-constant offset |
| Approximately 32:01–40:43.9 | C/Eb-related closing field | Several studio pitch fields resemble it; no accepted exact source assignment |

Gaps between these regions remain unassigned. Overlapping region ranges describe candidate material, not exclusive cuts. Radio Amor was included as a retrieval competitor; shared pitch content alone does not establish that Radio Amor material is performed here. No separate live Radio Amor album was analyzed, so this study cannot make a direct live-versus-studio claim for every Radio Amor track.

The accepted early Celestina comparisons imply `live_time ≈ studio_time + 859.11 s`. The Balkanize-You comparisons imply `live_time ≈ studio_time + 1554.42 s`. Those formulas apply to the tested spans, not automatically to the entire songs. Their near-constant offsets support retention of local source timing. They do not establish that all live layers run at the original rate or that nothing was re-performed.

The waveform check uses 25-second windows, resampled to 4,410 Hz, with a local ±4-second lag search. The strongest agreement is in 70–400 Hz; agreement in 400–1,500 Hz is generally much lower. Correlation is signed, and an absolute value is reported below to describe similarity despite polarity. Negative correlation is not proof of a particular mixer wiring or intentional inversion. These are corroborating checks on feature-retrieval candidates, not a calibrated identification classifier.

'''

ml_text='''## Machine-readable representation and optimization

The companion `study.json` contains all sections, source hashes, proposed patches, analytical interpretations and raw candidate events. Each track has three arrays in `data/`: the original feature NPZ; a 20-ms envelope NPZ; and a target NPZ with support masks, local frequency targets and normalization constants. A compact `sections.csv` and a long `pitch_components.csv` make the same evidence accessible without parsing nested JSON. `candidate_events.csv` contains sustained candidate regions, not MIDI transcription.

### Target semantics

`target_relative_activation` is the harmonic-template activation divided by the maximum activation in each half-second frame. `target_support_mask` requires a supported narrow component somewhere in that analysis window, framewise direct-fundamental support above 8% of the largest direct component, relative activation above 0.28, and mono RMS above −55 dBFS. This is a **spectral-component mask**, not a probability that a performed note exists. Its zero values mean “not accepted as a target by this heuristic,” not “known absent note.” The selected peak's frequency and cents are section-averaged constants: no continuous pitch-bend contour has been recovered.

`target_frequency_hz` is zero outside that mask. Inside, it holds the independently estimated local peak frequency. `target_weight` multiplies relative activation by a capped local-prominence factor, `clip(prominence_dB/24,0,1)`. This factor is a proposed optimization weight, not statistical confidence. Per-frame labels have `instrument_ground_truth = null`, `meter_ground_truth = null`, and `score_note_ground_truth = null` in the metadata. All key-profile fits remain auxiliary metadata.

Features are **pitch × time**, with MIDI numbers given explicitly. Pitch frame t covers approximately `[0.5t,0.5(t+1))` seconds, clipped to track length. CQT windows and the temporal median filter smear attacks; do not evaluate note-onset error at sub-frame precision. Envelope samples are 20-ms block RMS values positioned at block start; the final incomplete block is omitted. The waveform's phase is not stored in those envelopes.

### Suggested fitting objective

For a rendered candidate, run the same feature extraction at the same sample rate. Begin with a proposed normalized loss:

`L = 0.35 L_component + 0.20 L_log_envelope + 0.15 L_chroma + 0.15 L_power_centroid + 0.10 L_side_mid + 0.05 L_flatness`

Use masked, weight-normalized mean absolute error for the component term; compare log envelopes at 20 ms after gain alignment; use cosine distance for chroma; compare log2 centroid; compare side/mid and log flatness after robust scaling. Fit robust scaling on the training partition only. These weights are starting values, not empirically optimized results. No model was trained and no reconstruction quality score is claimed here.

Fit pitch centers and register before grain timing, then source envelope, then distortion/noise, then spatial balance. Keep gain as an explicit nuisance parameter so that a louder render does not appear structurally better. For a stable harmonic window, a practical proposed target is within about 0.5 Hz below 200 Hz and within 5–10 cents above it, subject to source resolution and observed beating; do not force unstable partials to meet a false exactness criterion.

Do not supervise named chords from every profile maximum. A G/Ab drone can alternate G-minor and Ab-major classifier outputs without a corresponding musical modulation. Likewise, optimizing only centroid permits the wrong notes to achieve a superficially similar spectrum. For noisy windows with no supported components, omit the pitched-component term and renormalize the remaining loss terms.

### Dataset split and leakage

Split by source family, not randomly by neighboring time windows. Group the matched Celestina, Counter Attack and Balkanize-You studio/live spans into the same partition, and keep adjacent windows together. Otherwise the live material can leak the studio source into validation. Use uncertain matches as potential leakage groups until disproven. The 22 recordings are a small reference corpus, not evidence of a generalizable training set; broadening it requires separately documented examples.

### Verification performed

Three synthetic known-note probes recovered the expected top pitches: clean Cm (C3/Eb3/G3), noisy Cm, and a distorted F2/C3 fifth. A white-noise probe produced spurious raw pitch/key candidates but zero sections passing the narrow-peak support gate. This demonstrates why the gate is necessary; four toy tests do **not** measure accuracy on the albums. No annotated ground-truth score, separated stems or original project files were available. The archive includes these results and the actual analysis scripts.

'''

parts=[intro]
parts.append(table(['Album','Tracks/files','Duration','Analysis windows'],[(name,sum(t['album']==a for t in TRACKS),tm(sum(t['duration'] for t in TRACKS if t['album']==a)),sum(len(t['sections']) for t in TRACKS if t['album']==a)) for a,name in ALBUMS.items()]))
parts.append(equipment)
for k,p in PATCHES.items():
    parts.append(f"### {k} — {p['name']}\n\n")
    parts.append(table(['Parameter','Proposed value'],[(key,', '.join(map(str,val)) if isinstance(val,list) else val) for key,val in p.items() if key!='name']))
parts.extend([trends,live_text])
checks=json.loads((A/'waveform_match_checks.json').read_text())
accepted=[]
for r in checks:
    w=r['waveform_checks'][0]
    if r['studio_id']=='mirages_04' and r['studio_start_s']==32:continue
    accepted.append([NOTES[r['studio_id']][0] if False else next(t['title'] for t in TRACKS if t['id']==r['studio_id']),tm(r['studio_start_s']),tm(w['best_live_start_s']),f"{w['best_live_start_s']-r['studio_start_s']:.3f}",f"{abs(w['correlation']):.3f}"])
parts.append(table(['Studio source','Studio start','Live aligned start','Offset seconds','Absolute low-band correlation'],accepted))
parts.append('Each row compares 25 seconds. Counter Attack offsets must not be collapsed to one time map. Full signed correlations and both frequency-band checks are in `waveform_match_checks.json`.\n\n')

comparisons=[]
live_arrays=np.load(F/'mort_aux_vaches_01.npz')
for r in checks:
    if r['studio_id']=='mirages_04' and r['studio_start_s']==32:continue
    studio_arrays=np.load(F/(r['studio_id']+'.npz'))
    ls=r['waveform_checks'][0]['best_live_start_s'];ss=r['studio_start_s']
    li=slice(round(ls/.5),round((ls+25)/.5));si=slice(round(ss/.5),round((ss+25)/.5))
    comparisons.append({'studio_id':r['studio_id'],'studio_start_s':ss,'live_start_s':ls,'duration_s':25,'live_minus_studio_mean_rms_db':round(float(live_arrays['rms'][li].mean()-studio_arrays['rms'][si].mean()),3),'live_over_studio_mean_power_centroid':round(float(live_arrays['centroid'][li].mean()/studio_arrays['centroid'][si].mean()),3),'live_minus_studio_mean_side_mid_db':round(float(live_arrays['side'][li].mean()-studio_arrays['side'][si].mean()),3)})
comp_rows=[]
for ident in ['mirages_04','mirages_05','mirages_10']:
    rr=[r for r in comparisons if r['studio_id']==ident]
    vals=[np.median([r[k] for r in rr]) for k in ['live_minus_studio_mean_rms_db','live_over_studio_mean_power_centroid','live_minus_studio_mean_side_mid_db']]
    comp_rows.append([next(t['title'] for t in TRACKS if t['id']==ident),len(rr),f'{vals[0]:+.2f}',f'{vals[1]:.2f}×',f'{vals[2]:+.2f}'])
parts.append('### Measured differences within the matched passages\n\n')
parts.append(table(['Source','Tested windows','Live − studio RMS dB','Live / studio power centroid','Live − studio side/mid dB'],comp_rows))
parts.append('These are medians across the tested, sometimes overlapping 25-second windows; they are not whole-album statistics or independent experimental replicates. Positive RMS means the live stream is louder in the mono measurement. A centroid ratio above one means more high-frequency weighting in this particular power-based metric; a positive side/mid change means a larger side/mid ratio. The differences include mastering, processing and overlays, so they cannot be uniquely attributed to a filter, distortion pedal or room. Use them as local reconstruction targets after preserving the supported source timing. In a live reconstruction, expose independent body gain, distorted-branch gain, high-frequency balance and side level; fit these controls rather than stretching the source merely to make it sound different.\n\n')
dump(OUT/'matched_passage_differences.json',comparisons)

section_rows=[];pitch_rows=[];event_rows=[];dataset=[]
for album,album_name in ALBUMS.items():
    parts.append(f'## {album_name}: track-by-track measured reconstruction\n\n')
    for t in [x for x in TRACKS if x['album']==album]:
        ident=t['id'];z=np.load(F/(ident+'.npz'))
        title,interpret,recipe,patch=NOTES[ident]
        a=z['activation'];df=z['direct_fund'];rel=a/(a.max(axis=0,keepdims=True)+1e-9)
        mask=np.zeros(a.shape,dtype=bool);freq=np.zeros_like(a);weight=np.zeros_like(a)
        parts.append(f"### {t['track_num']:02d}. {t['title']} — {tm(t['duration'])}\n\n**Defining structure: {title}.** {interpret}\n\n**Reconstruction:** {recipe} Patch {patch} is a proposed source/process initialization; per-track original instrument identity remains unknown unless independently cited above.\n\n")
        rows=[];metrics=[]
        for s in t['sections']:
            lo=int(s['start_s']/.5);hi=min(a.shape[1],int(np.ceil(s['end_s']/.5)))
            ns=[n for n in s['voicing_candidates'] if n.get('narrow_peak_supported')]
            for n in ns:
                ix=n['midi']-24
                active=(rel[ix,lo:hi]>.28)&(df[ix,lo:hi]>.08*df[:,lo:hi].max(axis=0))&(z['rms'][lo:hi]>-55)
                mask[ix,lo:hi]=active
                freq[ix,lo:hi]=np.where(active,n['measured_peak_hz'],0)
                weight[ix,lo:hi]=active*rel[ix,lo:hi]*np.clip(n['local_peak_prominence_db']/24,0,1)
            span=mask[:,lo:hi]*rel[:,lo:hi]
            best=lo+int(np.argmax(span.sum(axis=0)))
            simultaneous=[{'note':n['note'],'midi':n['midi'],'section_peak_hz':n['measured_peak_hz'],'frame_relative_salience':round(float(rel[n['midi']-24,best]),3)} for n in ns if mask[n['midi']-24,best]]
            s['representative_candidate_snapshot']={'start_s':round(best*.5,2),'duration_s':round(min(.5,t['duration']-best*.5),3),'selection':'maximum sum of supported relative activations in window','components':simultaneous,'status':'coincident_spectral_candidates_not_verified_played_chord'}
            pitches='; '.join(f"{n['note']}: {n['measured_peak_hz']:.2f} ({n['peak_cents_from_note']:+.1f})" for n in sorted(ns,key=lambda n:n['midi'])) or 'No candidate passes the narrow-peak gate'
            k=s['key_profile_candidates'][0]
            profile=f"{k['label']} (r={k['correlation']:.2f})" if len(ns)>=2 else 'Withheld: insufficient supported components'
            snap=', '.join(x['note'] for x in simultaneous) or 'none'
            rows.append([f"{s['section']:02d} · {tm(s['start_s'])}–{tm(s['end_s'])}",pitches,profile,f"{tm(best*.5)}: {snap}"])
            period=s.get('amplitude_period_candidate_s')
            metrics.append([s['section'],s['rms_dbfs'],s['power_centroid_hz'],s['side_to_mid_db'],s['spectral_flatness'],f"{period:.2f} ({s['amplitude_period_autocorrelation']:.2f})" if period else 'none'])
            section_rows.append({'track_id':ident,'section':s['section'],'start_s':s['start_s'],'end_s':s['end_s'],'supported_notes':';'.join(n['note'] for n in ns),'key_profile_candidate':k['label'],'key_profile_correlation':k['correlation'],'tonality_status':s['tonality_status'],'rms_dbfs':s['rms_dbfs'],'power_centroid_hz':s['power_centroid_hz'],'side_to_mid_db':s['side_to_mid_db'],'spectral_flatness':s['spectral_flatness'],'amplitude_period_candidate_s':period,'period_autocorrelation':s['amplitude_period_autocorrelation']})
            for n in s['voicing_candidates']:pitch_rows.append({'track_id':ident,'section':s['section'],'start_s':s['start_s'],'end_s':s['end_s'],**n})
        parts.append(table(['Window / time','Supported pitch components: Hz (cents)','Key-profile fit, not confirmed key','Representative 0.5-s candidate snapshot'],rows))
        parts.append('\n**Measured dynamics and texture.** Use these as section targets; retain the full envelopes for within-section motion.\n\n')
        parts.append(table(['Window','RMS dBFS','Power centroid Hz','Side/mid dB','Flatness','Envelope period s (r)'],metrics))
        parts.append('\nThe snapshot selects the densest supported candidate frame, not a typical or definitive chord. The pitch plot below is gated by the spectral-component mask; blank regions mean unresolved pitch evidence, not necessarily silence.\n\n')
        for e in t['candidate_events']:event_rows.append({'track_id':ident,**e})
        np.savez_compressed(OUT/'data'/(ident+'_targets.npz'),time_s=np.arange(a.shape[1])*.5,midi=z['midi'],target_relative_activation=rel,target_support_mask=mask,target_frequency_hz=freq,target_weight=weight)
        for suffix in ['.npz','_envelope.npz']:shutil.copyfile(F/(ident+suffix),OUT/'data'/(ident+suffix))
        plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False})
        fig,ax=plt.subplots(3,1,figsize=(12,6.5),sharex=True,gridspec_kw={'height_ratios':[3,1,1]},layout='constrained')
        extent=[0,t['duration'],23.5,95.5]
        ax[0].imshow(np.where(mask,rel,np.nan),origin='lower',aspect='auto',extent=extent,cmap='magma',vmin=0,vmax=1,interpolation='nearest')
        ax[0].set_facecolor('#eeeeee');ax[0].set_yticks([24,36,48,60,72,84,95],['C1','C2','C3','C4','C5','C6','B6'])
        ax[0].set_ylabel('Candidate register');ax[0].set_title(t['title']+' | spectral-component activity (not a piano score)\nPurple → yellow: increasing frame-relative activation; gray: unaccepted/unresolved',loc='left')
        tt=np.arange(a.shape[1])*.5
        ax[1].plot(tt,z['rms'],color='#214d69',lw=.7);ax[1].set_ylabel('Mono RMS\ndBFS');ax[1].set_ylim(max(-80,np.percentile(z['rms'],1)-5),0)
        ax[2].plot(tt,z['centroid'],color='#815031',lw=.7);ax[2].set_ylabel('Power centroid\nHz');ax[2].set_ylim(0,max(100,np.percentile(z['centroid'],99)*1.1))
        for aa in ax:
            for s in t['sections'][1:]:aa.axvline(s['start_s'],color='#666666',alpha=.25,lw=.5)
            aa.set_xlim(0,t['duration'])
        ax[-1].xaxis.set_major_formatter(FuncFormatter(lambda x,pos:tm(x)));ax[-1].set_xlabel('Track time (minutes:seconds)')
        fig.savefig(OUT/'figures'/(ident+'.png'),dpi=140);plt.close(fig)
        parts.append(f'![Measured activity and dynamics for {t["title"]}](figures/{ident}.png)\n\n')
        cleaned={k:v for k,v in t.items() if k not in ['mp3_path','analysis_wav_path']}
        cleaned['interpretation']={'defining_structure':title,'harmonic_reading':interpret,'reconstruction_proposal':recipe,'patch_id':patch}
        cleaned['ground_truth']={'instrument':None,'meter':None,'score_notes':None}
        dataset.append(cleaned)

parts.append(ml_text)
parts.append('''## Reproducibility and scope of remaining uncertainty

The pipeline uses librosa CQT with 252 bins at 36 bins/octave from C1, 0.5-second median aggregation, local spectral-floor subtraction, and nonnegative least squares against eight-partial harmonic templates. MIDI candidates span C1–B6. A second averaged-spectrum check accepts candidates with at least 6 dB local prominence and direct-fundamental support in at least 25% of the section frames. Both tests can still accept a harmonic or an intermodulation product. They are not source separation.

Pitch classes are correlated with major/minor profiles. The stored correlation is similarity to that template, not key confidence. Temporal novelty combines pitch distribution, five spectral bands, level, power centroid and stereo ratio over approximately eight-second contexts. The script inserts 90-second analysis caps. Peak and tuning measurements average over the window and can conceal moving or doubled components.

Live retrieval compares 30-second feature windows, with studio rates 0.75, 1, 1.25 and 1.5 seconds per live second. Its score combines 60% absolute feature similarity and 40% centered temporal-shape similarity. The retained top three candidates per live window are not accepted matches by default. The waveform checks then test selected candidates. Neither stage has an empirical false-match probability for this repertoire.

The source assumptions and code are included so these decisions can be inspected. A full original-note transcription, exact note velocities, original synth patches, grain lengths, reverb impulse responses and complete stem identities remain unestablished. The document supplies concrete frequency, register, timing and signal-shaping targets where the data supports them, and keeps those unresolved variables explicit rather than inventing an authoritative session.

For comparison with an independently written formal analysis, Brett Bergmann divides Spectral into seven large sections. That perceptual segmentation and the smaller acoustic windows here answer different questions. [Global Movement, Local Detail](https://econtact.ca/11_2/bergmann_hecker.html).

Technical implementation reference: [librosa 0.11 CQT](https://librosa.org/doc/0.11.0/generated/librosa.cqt.html). The included scripts are the definitive description of this extraction run.
''')

full='\n'.join(parts)
(OUT/'Tim_Hecker_Production_Study.md').write_text(full,encoding='utf8')
html=markdown2.markdown(full,extras=['tables','fenced-code-blocks','header-ids','toc'])
toc_html=html.toc_html
for ident in IDS:
    data=base64.b64encode((OUT/'figures'/(ident+'.png')).read_bytes()).decode()
    html=html.replace('src="figures/'+ident+'.png"','src="data:image/png;base64,'+data+'"')
css='''body{margin:0;color:#172a35;background:#f5f4f0;font:16px/1.65 system-ui,sans-serif}main{max-width:1240px;margin:auto;padding:42px 36px}h1{font-size:2.5rem;line-height:1.2}h2{border-top:2px solid #b5c7c8;padding-top:28px;margin-top:60px}h3{margin-top:40px;color:#285466}p,li{max-width:100ch}table{width:100%;border-collapse:collapse;font-size:13px;margin:24px 0;background:white}th{background:#254955;color:white;text-align:left}td,th{padding:9px 10px;vertical-align:top;border:1px solid #d0d9da}tr:nth-child(even){background:#edf2f2}img{width:100%;height:auto;border:1px solid #ccd5d5}code{background:#e6ecec;padding:1px 4px;overflow-wrap:anywhere}a{color:#12647f}nav{background:#e7eded;padding:18px 28px;border-radius:8px}nav ul{columns:2}nav ul ul{columns:1}summary{cursor:pointer;font-weight:650} @media(max-width:800px){main{padding:20px 12px}table{display:block;overflow:auto}nav ul{columns:1}}@media print{body{background:white;font-size:10pt}main{padding:0}nav{display:none}h2{break-before:page}tr,img{break-inside:avoid}table{font-size:8pt}}'''
page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Tim Hecker — measured production study</title><style>'+css+'</style><main><nav><details><summary>Navigate the study</summary>'+toc_html+'</details></nav>'+html+'</main></html>'
(OUT/'Tim_Hecker_Production_Study.html').write_text(page,encoding='utf8')
study={'schema_version':'1.0','created_date':'2026-09-26','purpose':'audio-derived spectral reconstruction reference; not verified score transcription','sample_rate_hz':22050,'pitch_hop_s':.5,'envelope_hop_s':.02,'pitch_reference':'A4=440 Hz; C4=MIDI60','patch_parameters_status':'proposed_not_recovered','patches':PATCHES,'tracks':dataset,'live_waveform_checks':checks,'validation':json.loads((A/'validation.json').read_text())}
dump(OUT/'study.json',study)
for filename,rows in [('sections.csv',section_rows),('pitch_components.csv',pitch_rows),('candidate_events.csv',event_rows)]:
    with (OUT/filename).open('w',encoding='utf8',newline='') as f:
        fields=list(dict.fromkeys(k for r in rows for k in r))
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
for filename in ['live_matches.json','waveform_match_checks.json','validation.json']:shutil.copyfile(A/filename,OUT/filename)
for filename in ['analyze_streams.py','refine_partials.py','envelope_analysis.py','match_live.py','verify_matches.py','validate_analysis.py','validate_noise.py','track_interpretations.py','build_measured_study.py']:shutil.copyfile(ROOT/filename,OUT/'scripts'/filename)

readme='''# Measured Hecker reference package

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
'''
(OUT/'README.md').write_text(readme,encoding='utf8')
qa={'track_count':len(dataset),'analysis_window_count':len(section_rows),'candidate_event_count':len(event_rows),'figure_count':len(IDS),'timeline_contiguous':True,'source_audio_packaged':False,'original_score_verified':False,'synthetic_tests_passed':all(x['all_known_in_top_n'] for x in study['validation'])}
noise=json.loads((F/'validation_04.json').read_text())
qa['white_noise_supported_window_count']=sum(bool(s['supported_pitch_components']) for s in noise['sections'])
for t in dataset:
    ss=t['sections'];assert ss[0]['start_s']==0
    assert abs(ss[-1]['end_s']-t['duration'])<.02
    assert all(x['end_s']==y['start_s'] for x,y in zip(ss,ss[1:]))
    for s in ss:
        assert s['end_s']>s['start_s']
        for n in s['voicing_candidates']:
            if n.get('measured_peak_hz'):
                cents=1200*np.log2(n['measured_peak_hz']/(440*2**((n['midi']-69)/12)))
                assert abs(cents-n['peak_cents_from_note'])<.5,(t['id'],n)
assert qa['track_count']==22 and qa['white_noise_supported_window_count']==0
dump(OUT/'QA.json',qa)
hashes={str(p.relative_to(OUT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='SHA256.json'}
dump(OUT/'SHA256.json',hashes)
with zipfile.ZipFile(ROOT/'Hecker_Measured_Study.zip','w',zipfile.ZIP_DEFLATED,compresslevel=6) as zipf:
    for p in OUT.rglob('*'):
        if p.is_file():zipf.write(p,'Hecker_Measured_Study/'+str(p.relative_to(OUT)))
shutil.copyfile(OUT/'Tim_Hecker_Production_Study.md',ROOT/'Tim_Hecker_Production_Study.md')
print(json.dumps(qa,indent=2));print('Document words:',len(full.split()));print('ZIP bytes:',(ROOT/'Hecker_Measured_Study.zip').stat().st_size)
