from pathlib import Path
import numpy as np,soundfile as sf,json
from scipy import signal
R=Path(__file__).resolve().parents[1];x,s=sf.read(R/'Renders/Physical String Source - High Resolution.wav',always_2d=True,dtype='float32');assert s==48000 and len(x)==336*s and np.isfinite(x).all()
rms=float(np.sqrt(np.mean(x[10*s:325*s].astype(float)**2)));assert rms>1e-4
x=signal.sosfilt(signal.butter(2,[110,2400],btype='bandpass',fs=s,output='sos'),x,axis=0);g=.011/np.sqrt(np.mean(x[10*s:325*s]**2));x*=g;x[-s*3:]*=np.linspace(1,0,s*3)[:,None]
sf.write(R/'Media/04_Physical_string.flac',x,s,subtype='PCM_24');(R/'Audit/string_print.json').write_text(json.dumps({'duration_s':336,'sample_rate':s,'input_active_rms':rms,'normalization_gain_db':float(20*np.log10(g)),'output_active_rms':.011,'peak':float(abs(x).max()),'source':'Native Surge XT print, Physical String Source - High Resolution.rpp','print_gain_db':40,'pitch_modulation':'Portamento, drift, second-string detune disabled; no pitch LFO','filter':'110-2400Hz second-order bandpass after VST print'},indent=2),encoding='utf8');print('Normalized high-resolution source',rms,g)
