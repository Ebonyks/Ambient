from pathlib import Path
import json,hashlib,subprocess,sys,numpy as np,soundfile as sf
R=Path(__file__).resolve().parents[1];ROOT=R.parents[1];sys.path.insert(0,str(ROOT/'tools/melodic_weave'))
from blend_texture import clashes
from texture_weave import validate
FF='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe'
p=R/'Renders/Long Line - Context Blend.wav';x,sr=sf.read(p);assert (R/'Audit/blend_returned.txt').exists();assert sr==48000 and len(x)==96*sr and np.isfinite(x).all() and abs(x).max()<.99
s=json.loads((R/'texture.json').read_text());old=json.loads((R.parent/'long-line-v9-study/texture.json').read_text());qa=validate(s);assert qa['passed'];qa.update({'old_close_pairs_including_one_second_guard':len(clashes(old,1)),'new_close_pairs_including_one_second_guard':len(clashes(s,1)),'omitted_notes':sum(e['to'] is None for e in s['blend_revision']['edits']),'repitched_notes':sum(e['to'] is not None for e in s['blend_revision']['edits']),'peak':float(abs(x).max()),'duration_s':96,'source_excerpt_s':[140,236],'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'audition_status':'Pending owner review; numeric interval policy does not establish musical quality'})
cp=subprocess.run([FF,'-hide_banner','-i',str(p),'-af','loudnorm=I=-21:TP=-1:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True);loud=json.JSONDecoder().raw_decode(cp.stderr[cp.stderr.rfind('{'):])[0];qa['loudness']={k:v for k,v in loud.items() if k.startswith('input_')}
subprocess.run([FF,'-y','-loglevel','error','-i',str(p),'-c:a','libmp3lame','-b:a','256k',str(R/'Renders/Long Line - Context Blend - 96s.mp3')],check=True)
y,_=sf.read(R.parent/'long-line-v9-study/Renders/Long Line - Inner Detail B.wav');segments=[]
for z in [y[28*sr:38*sr],x[28*sr:38*sr]]:
 z=z.copy();z*=.05/np.sqrt(np.mean(z*z));fade=np.linspace(0,1,int(.04*sr));z[:len(fade)]*=fade[:,None];z[-len(fade):]*=fade[::-1,None];segments.append(z)
sf.write(R/'Listening/old-new-matched.wav',np.concatenate(segments),sr,subtype='PCM_24')
(R/'Audit/QA.json').write_text(json.dumps(qa,indent=2));print(json.dumps(qa,indent=2))
