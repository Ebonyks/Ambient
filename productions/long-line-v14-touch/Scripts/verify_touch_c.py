from pathlib import Path
import json,hashlib,subprocess,sys,numpy as np,soundfile as sf
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R.parents[1]/'tools/melodic_weave'))
from texture_weave import validate
FF='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe'
p=R/'Renders/Long Line - Phrase Touch C.wav';assert (R/'Audit/touch_C_returned.txt').exists();x,sr=sf.read(p);assert sr==48000 and len(x)==96*sr and np.isfinite(x).all() and abs(x).max()<.99
s=json.loads((R/'texture.json').read_text());qa=validate(s);assert qa['passed'];qa.update({'duration_s':96,'source_excerpt_s':[140,236],'native_peak':float(abs(x).max()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'prior_melodic_scaffold_in_audio':False,'rendered_primary_voices':[4,5,6,7],'tests':{'melody_texture':42,'harmony':10},'review_status':'Pending listening; MIDI distribution is not acoustic salience'})
cp=subprocess.run([FF,'-hide_banner','-i',str(p),'-af','loudnorm=I=-21:TP=-1:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True);qa['loudness']={k:v for k,v in json.JSONDecoder().raw_decode(cp.stderr[cp.stderr.rfind('{'):])[0].items() if k.startswith('input_')}
subprocess.run([FF,'-y','-loglevel','error','-i',str(p),'-c:a','libmp3lame','-b:a','256k',str(R/'Renders/Long Line - Phrase Touch C - 96s.mp3')],check=True)
(R/'Audit/QA_C.json').write_text(json.dumps(qa,indent=2));print(json.dumps(qa,indent=2))
