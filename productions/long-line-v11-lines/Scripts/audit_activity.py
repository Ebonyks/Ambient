from pathlib import Path
import json,numpy as np,soundfile as sf
from scipy import signal
R=Path(__file__).resolve().parents[1]
def measure(p):
 x,s=sf.read(p,always_2d=True);x=x.mean(axis=1);x=signal.resample_poly(x,1,4);s=s//4
 f,t,z=signal.stft(x,s,nperseg=1024,noverlap=964);a=abs(z[(f>=100)&(f<4000)]);flux=np.maximum(np.diff(np.log1p(a*1000),axis=1),0).mean(axis=0);med=np.median(flux);mad=np.median(abs(flux-med))+1e-9;rates={}
 for k in [1,2,3]:rates[str(k)]=len(signal.find_peaks(flux,height=med+k*mad,distance=4)[0])/(len(x)/s)
 return {'flux_peak_rate_per_s_by_MAD':rates,'note':'20ms peak separation; spectral articulation proxy, not performed-note count.'}
s=json.loads((R/'texture.json').read_text());old=json.loads((R.parent/'long-line-v10-flow/texture.json').read_text());es=[e for e in s['events'] if e['voice']>=4];prior=[e for e in old['events'] if e['voice']>=4];rows=[]
for lane in range(4):
 notes=[e for e in es if e['voice']==lane+4];rows.append({'lane':lane,'events':len(notes),'midi_range':[min(e['midi'] for e in notes),max(e['midi'] for e in notes)],'new_native_articulation':measure(R/'Renders'/f'Inner lane {lane}.wav'),'old_native_articulation':measure(R.parent/'long-line-v10-flow/Renders'/f'Inner lane {lane}.wav')})
report={'old_events':len(prior),'new_events':len(es),'actual_count_ratio':len(es)/len(prior),'demo_new_events':sum(e['end_s']>140 and e['start_s']<236 for e in es),'lanes':rows,'tonal_itinerary_in_demo':[q for q in s['tonal_plan'] if 132<=q['start_s']<236],'limits':'Envelope, masking and timbre govern perceived speed. Fourfold MIDI rate does not establish fourfold perceived speed. Tonal itinerary is an authored score, not a transcription.'};(R/'Audit/line_activity.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
