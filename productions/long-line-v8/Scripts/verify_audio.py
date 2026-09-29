from pathlib import Path
import numpy as np,soundfile as sf,json,subprocess,hashlib
R=Path(__file__).resolve().parents[1];FF=Path(r'C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\FFmpeg\8.1.2\bin\ffmpeg.exe')
assert (R/'Audit/render_C_returned.txt').exists()
paths={'v7':R.parent/'long-line-v7/Renders/Long Line - Moving Voices - 5m36.wav','B':R/'Renders/Long Line - Tonal Revision B.wav','C':R/'Renders/Long Line - Tonal Revision C.wav'}
metrics={}
for label,p in paths.items():
 x,s=sf.read(p,dtype='float32',always_2d=True);assert s==48000 and len(x)==336*s and np.isfinite(x).all()
 cp=subprocess.run([str(FF),'-hide_banner','-i',str(p),'-af','loudnorm=I=-21:TP=-1:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True);assert cp.returncode==0;loud=json.JSONDecoder().raw_decode(cp.stderr[cp.stderr.rfind('{'):])[0]
 data={'duration_s':336,'sample_rate':s,'sample_peak':float(abs(x).max()),'nonfinite':0,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'loudness':{k:v for k,v in loud.items()if k.startswith('input_')},'windows':{}}
 for t in [43,107,168,188,248,308]:
  z=x[t*s:(t+20)*s];mono=z.mean(axis=1);f=np.fft.rfftfreq(s,1/s);power=(abs(np.fft.rfft(mono.reshape(20,s)*np.hanning(s),axis=1))**2).sum(axis=0)
  bands={f'{lo}-{hi}':float(power[(f>=lo)&(f<hi)].sum()) for lo,hi in [(120,500),(500,1500),(1500,4000),(4000,10000),(150,2500),(2500,8000)]}
  data['windows'][str(t)]={'upper_mid_to_low_mid_db':float(10*np.log10(bands['1500-4000']/bands['500-1500'])),'upper_to_body_db':float(10*np.log10(bands['2500-8000']/bands['150-2500'])),'centroid_hz':float((power*f).sum()/power.sum()),'rms':float(np.sqrt(np.mean(z.astype(float)**2)))}
  z=z.copy();z*=.05/np.sqrt(np.mean(z.astype(float)**2));assert abs(z).max()<1;sf.write(R/'Listening'/f'{label}_{t}.wav',z,s,subtype='PCM_24')
 metrics[label]=data
for label1,label2,t in [('B','C',43),('v7','C',168)]:
 a,s=sf.read(R/'Listening'/f'{label1}_{t}.wav');b,s=sf.read(R/'Listening'/f'{label2}_{t}.wav');sf.write(R/'Listening'/f'pair_{label1}_{label2}_{t}.wav',np.concatenate([a[:10*s],b[:10*s]]),s,subtype='PCM_24')
(R/'Audit/tonal_comparison.json').write_text(json.dumps(metrics,indent=2),encoding='utf8')
for label,d in metrics.items():print(label,d['loudness'],'2:48',d['windows']['168'])
subprocess.run([str(FF),'-y','-hide_banner','-loglevel','error','-i',str(paths['C']),'-codec:a','libmp3lame','-b:a','256k',str(paths['C'].with_suffix('.mp3'))],check=True)
