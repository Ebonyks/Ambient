from pathlib import Path
import json, sys, numpy as np
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools/melodic_weave'));from melody_tool import validate
score=json.loads((R/'weave.json').read_text(encoding='utf8'))
rows=[]
for tid in ['radio_amor_01','radio_amor_04','radio_amor_09','mirages_04','mirages_07','mirages_11']:
    a=np.load(ROOT/'studies/tim-hecker/data'/f'{tid}_targets.npz');act=a['target_relative_activation'];mask=a['target_support_mask'].astype(bool);midi=a['midi'];t=a['time_s']
    bands={}
    for lo,hi in [(48,65),(65,84)]:
        select=(midi>=lo)&(midi<hi);x=np.where(mask[select],act[select],0);ms=midi[select];sensitivity={}
        for gate in [.28,.4,.55]:
            strongest=ms[np.argmax(x,axis=0)].astype(int);strongest[np.max(x,axis=0)<gate]=-1
            # Accept a new dominant component after two frames; no filling missing support.
            accepted=-1;changes=[]
            for k in range(1,len(t)):
                if strongest[k]>=0 and strongest[k]==strongest[k-1] and strongest[k]!=accepted:
                    if accepted>=0:changes.append(float(t[k-1]))
                    accepted=strongest[k]
                elif strongest[k]<0:accepted=-1
            gaps=np.diff(changes)
            sensitivity[str(gate)]={'supported_fraction':round(float(np.mean(strongest>=0)),3),'accepted_prominence_changes':len(changes),'change_gap_median_s':round(float(np.median(gaps)),3) if len(gaps) else None}
        bands[f'{lo}..{hi-1}']=sensitivity
    rows.append({'track':tid,'register_bands':bands})
starts=sorted(set(e['start_s'] for e in score['events'] if e['voice']!=3 and 10<e['start_s']<325));gaps=np.diff(starts)
phrases={}
for e in score['events']:
    if e['voice']==2:phrases.setdefault(e['phrase'],[]).append(e['midi'])
result={'evidence':'Existing reference-sample-derived half-second pitch-support trajectories, not newly auditioned audio or note transcription. Dominance changes include processing/masking; gaps across unresolved intervals are included. No universal two-second claim. Threshold sensitivity is descriptive, not a generator fit.','reference':rows,'new_score':{'event_count':len(score['events']),'upper_phrase_sequences':phrases,'unique_upper_sequences':len({tuple(v)for v in phrases.values()}),'median_source_change_gap_s':float(np.median(gaps)),'gap_10_90_percentile_s':np.percentile(gaps,[10,90]).tolist(),'validation':validate(score)},'baseline':{'complete_arch_statements':7,'literal_pitch_sequence_variants':1,'sequence':[69,71,74,71,69,64,62],'source':'v6 phrase_map.json and Audit/baseline_score.json; three source-timing variants share one pitch sequence','body_source_events':19,'harmonic_states':7}}
(R/'Audit/comparison.json').write_text(json.dumps(result,indent=2),encoding='utf8');print(json.dumps(result['new_score'],indent=2))
for row in rows:print(row['track'],row['register_bands'])
