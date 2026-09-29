from pathlib import Path
import json,hashlib,subprocess,soundfile as sf,numpy as np
R=Path(__file__).resolve().parents[1];assert (R/'Audit/render_D_returned.txt').exists();p=R/'Renders/Long Line - Tonal Revision D.wav';ff=r'C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\FFmpeg\8.1.2\bin\ffmpeg.exe'
x,s=sf.read(p,dtype='float32',always_2d=True);assert len(x)==336*s and s==48000 and np.isfinite(x).all()
cp=subprocess.run([ff,'-hide_banner','-i',str(p),'-af','loudnorm=I=-21:TP=-1:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True);assert cp.returncode==0;loud=json.JSONDecoder().raw_decode(cp.stderr[cp.stderr.rfind('{'):])[0]
data={'duration_s':336,'sample_rate':s,'sample_peak':float(abs(x).max()),'nonfinite':0,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'loudness':{k:v for k,v in loud.items()if k.startswith('input_')},'windows':{}}
for t in [43,107,168,188,248,308]:
 z=x[t*s:(t+20)*s];mono=z.mean(axis=1);f=np.fft.rfftfreq(s,1/s);power=(abs(np.fft.rfft(mono.reshape(20,s)*np.hanning(s),axis=1))**2).sum(axis=0)
 def band(lo,hi):return power[(f>=lo)&(f<hi)].sum()
 data['windows'][str(t)]={'upper_mid_to_low_mid_db':float(10*np.log10(band(1500,4000)/band(500,1500))),'upper_to_body_db':float(10*np.log10(band(2500,8000)/band(150,2500))),'centroid_hz':float((power*f).sum()/power.sum()),'rms':float(np.sqrt(np.mean(z.astype(float)**2)))}
 z=z.copy();z*=.05/np.sqrt(np.mean(z.astype(float)**2));assert abs(z).max()<1;sf.write(R/'Listening'/f'D_{t}.wav',z,s,subtype='PCM_24')
for label,t in [('B',43),('v7',168)]:
 a,s=sf.read(R/'Listening'/f'{label}_{t}.wav');b,s=sf.read(R/'Listening'/f'D_{t}.wav');sf.write(R/'Listening'/f'pair_{label}_D_{t}.wav',np.concatenate([a[:10*s],b[:10*s]]),s,subtype='PCM_24')
metrics=json.loads((R/'Audit/tonal_comparison.json').read_text(encoding='utf8'));metrics['D']=data;(R/'Audit/tonal_comparison.json').write_text(json.dumps(metrics,indent=2),encoding='utf8');print(json.dumps(data,indent=2))
subprocess.run([ff,'-y','-hide_banner','-loglevel','error','-i',str(p),'-codec:a','libmp3lame','-b:a','256k',str(R/'Renders/Long Line - Tonal Revision - 5m36.mp3')],check=True)
