from pathlib import Path
import soundfile as sf,numpy as np,json,subprocess,hashlib
R=Path('productions/long-line-v7');old=R.parent/'long-line-v6';ff=r'C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\FFmpeg\8.1.2\bin\ffmpeg.exe';p=R/'Renders/Long Line - Moving Voices - 5m36.wav'
x,s=sf.read(p,always_2d=True,dtype='float32');assert s==48000 and len(x)==336*s and np.isfinite(x).all()
(R/'Listening').mkdir(exist_ok=True);clips=[]
for ver,source in [('v7',p),('v6',next(p for p in [old/'Renders/Long Line - Full Length - Study Draft - 5m36.wav',old/'Renders/Long Line - Full Length - Study Draft - 5m36.mp3'] if p.exists()))]:
 for start in ([24,43,107,165,248,310]if ver=='v7'else[43,165]):
  z,sr=sf.read(source,start=start*48000,frames=20*48000,dtype='float32',always_2d=True);rms=float(np.sqrt(np.mean(z.astype(float)**2)));g=10**(-26/20)/(rms+1e-12);z*=g;assert np.max(abs(z))<1
  dest=R/'Listening'/f'{ver}_{start:03}.wav';sf.write(dest,z,sr,subtype='PCM_24');clips.append({'path':str(dest.resolve()),'original_start_s':start,'rms_match_dbfs':-26,'gain_db':20*np.log10(g)})
cp=subprocess.run([ff,'-hide_banner','-i',str(p),'-af','loudnorm=I=-20:TP=-1:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True);assert cp.returncode==0
stats=json.JSONDecoder().raw_decode(cp.stderr[cp.stderr.rfind('{'):])[0];stats.update({'duration_s':len(x)/s,'sample_rate':s,'peak':float(np.max(abs(x))),'nonfinite_samples':int((~np.isfinite(x)).sum()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'clips':clips})
(R/'Audit/render_verification.json').write_text(json.dumps(stats,indent=2),encoding='utf8')
subprocess.run([ff,'-y','-hide_banner','-loglevel','error','-i',str(p),'-codec:a','libmp3lame','-b:a','256k',str(p.with_suffix('.mp3'))],check=True)
print(json.dumps({k:v for k,v in stats.items()if k!='clips'},indent=2))
