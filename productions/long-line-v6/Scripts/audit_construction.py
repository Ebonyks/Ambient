from pathlib import Path
import numpy as np,soundfile as sf,json,sys,hashlib
R=Path(__file__).resolve().parents[1];repo=R.parents[1];sys.path.insert(0,str(repo/'protocols/hecker-harmony-v1'))
from harmony_tool import read_protocol,validate
s=json.loads((R/'harmony.json').read_text());events=json.loads((R/'voice_events.json').read_text());ph=json.loads((R/'phrase_map.json').read_text())['phrases'];old=json.loads((R/'Audit/baseline_score.json').read_text())
core=validate(s,read_protocol());assert core['passed']
shared=[]
for before,after in zip(s['states'],s['states'][1:]):
 for m in set(n['midi']for n in before['notes'])&set(n['midi']for n in after['notes']):
  boundary=after['start_s'];matching=[e for e in events if e['midi']==m and e['start_s']<boundary<e['end_s']]
  shared.append({'boundary_s':boundary,'midi':m,'single_continuous_event':len(matching)==1})
assert all(v['single_continuous_event']for v in shared)
all_events=[(e['start_s'],e['end_s'],'body',e['midi'])for e in events]
for p in ph:
 for t,d,m,voice in old['melodic_voices']:
  if voice=='arch' and p['source_start_s']<=t<p['source_end_s']:
   a=p['start_s']+t-p['source_start_s'];b=p['start_s']+min(t+d,p['source_end_s'])-p['source_start_s'];all_events.append((a,b,'motif',m))
all_events=[(a,332 if role=='motif' and a>320 and m==62 else b,role,m)for a,b,role,m in all_events]
grid=np.arange(0,336,.02);count=np.array([sum(a<=t<b for a,b,_,_ in all_events)for t in grid]);assert max(count)<=6
anchor,sr=sf.read(R/'Media/01_Anchor_bypasses_drive.flac',always_2d=True);mix,msr=sf.read(R/'Renders/Long Line - Full Length - Study Draft - 5m36.wav',always_2d=True);pitch=[]
for state in s['states']:
 m=min(n['midi']for n in state['notes']);c=next(n['cents']for n in state['notes']if n['midi']==m);hz=440*2**((m-69+c/100)/12);t=(state['start_s']+state['end_s'])/2
 row={'state':state['index'],'time_s':t,'midi':m,'expected_hz':hz}
 for name,x,fs in [('source',anchor,sr),('mix',mix,msr)]:
  seg=x[int((t-3)*fs):int((t+3)*fs)].mean(axis=1);sp=abs(np.fft.rfft(seg*np.hanning(len(seg))))**2;freq=np.fft.rfftfreq(len(seg),1/fs);ids=np.where(abs(freq-hz)<1)[0];i=ids[np.argmax(sp[ids])];v=np.log(sp[i-1:i+2]+1e-30);delta=.5*(v[0]-v[2])/(v[0]-2*v[1]+v[2]);measured=(i+delta)*fs/len(seg);row[name+'_measured_hz']=float(measured);row[name+'_error_hz']=float(measured-hz)
 pitch.append(row)
assert max(abs(v['source_error_hz'])for v in pitch)<.5
assert max(abs(v['mix_error_hz'])for v in pitch)<.5
files=[]
for p in sorted((R/'Media').glob('*.flac')):
 if p.stem in ['03_Pitched_motif_route','04_Eroded_motif_return']:continue
 info=sf.info(p);assert info.frames/info.samplerate==336 and info.channels==2 and info.samplerate==48000;files.append({'path':str(p.relative_to(R)),'duration':336,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
result={'core_protocol':core,'retained_boundary_identities':shared,'retained_identities_all_continuous':True,'maximum_nominal_source_voices_including_motif_overlaps':int(max(count)),'source_voice_count_excludes_derived_distortion_and_reverb_partials':True,'anchor_pitch_checks':pitch,'pitch_tolerance_hz':.5,'all_anchors_meet_tolerance_in_source_and_mix':True,'media':files,'limitations':'No claim that audible harmonics are source notes; body-sample tuning and legacy distorted motif are not claimed to meet the sub-0.5Hz oscillator test. Listening acceptance remains separate.'}
(R/'Audit/construction_checks.json').write_text(json.dumps(result,indent=2));(R/'Audit/nominal_source_events.json').write_text(json.dumps(all_events,indent=2));print('PASS: protocol; 9 retained boundary identities; max',int(max(count)),'nominal source voices; 7 rendered anchor checks; 8 complete media stems.')
# Same extractor statistics for the final render; compare descriptively rather than scoring style.
fp=R/'Audit/feature_comparison.json';comp=json.loads(fp.read_text());a=np.load(R/'Scripts/analysis/audio_analysis/features/long_line_08.npz');comp['statistics']['long_line_08']={k:{'median':float(np.median(a[k])),'p10':float(np.percentile(a[k],10)),'p90':float(np.percentile(a[k],90))}for k in ['rms','centroid','side','flatness']};fp.write_text(json.dumps(comp,indent=2));print({k:round(v['median'],3)for k,v in comp['statistics']['long_line_08'].items()})
