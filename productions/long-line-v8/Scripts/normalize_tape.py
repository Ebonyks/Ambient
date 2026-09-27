from pathlib import Path
import soundfile as sf,numpy as np,json
R=Path(__file__).resolve().parents[1];assert (R/'Audit/tape_prints_returned.txt').exists();receipts=[]
for i,(name,target)in enumerate([('05_Tape_inner',.009),('06_Tape_foreground',.0145),('07_Tape_string',.0058)]):
 x,s=sf.read(R/'Renders'/(f'Calibrated_Tape_{i}.wav' if i<2 else 'Calibrated_Tape_2_safe.wav'),always_2d=True,dtype='float32');assert s==48000 and len(x)==336*s and np.isfinite(x).all();pk=float(abs(x).max());assert pk<.99
 rms=float(np.sqrt(np.mean(x[10*s:325*s].astype(float)**2)));g=target/rms;x*=g;assert abs(x).max()<.65
 sf.write(R/'Media'/f'{name}.flac',x,s,subtype='PCM_24');receipts.append({'file':name+'.flac','input_rms':rms,'input_peak':pk,'output_target_rms':target,'normalization_gain_db':float(20*np.log10(g)),'output_peak':float(abs(x).max())})
(R/'Audit/printed_tape_levels.json').write_text(json.dumps(receipts,indent=2),encoding='utf8');print(json.dumps(receipts,indent=2))
