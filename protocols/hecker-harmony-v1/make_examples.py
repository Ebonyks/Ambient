from pathlib import Path
import json
from harmony_tool import read_protocol,generate,validate,write_midi
root=Path(__file__).resolve().parent
p=read_protocol();out=root/'examples';out.mkdir(exist_ok=True)
results=[]
for i,profile in enumerate(p['profiles']):
    seed=60 if profile=='common_tone_clarity' else 41+i*11
    sketch=generate(p,profile,seed,240)
    result=validate(sketch,p);assert result['passed']
    (out/(profile+'.json')).write_text(json.dumps(sketch,indent=2)+'\n',encoding='utf8')
    write_midi(sketch,out/(profile+'.mid'))
    results.append({'profile':profile,'seed':sketch['seed'],'harmonic_state_count':len(sketch['states']),'duration_s':240,'validation':result,'audio_similarity_evaluated':False})
(out/'validation.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf8')
print(json.dumps(results,indent=2))
