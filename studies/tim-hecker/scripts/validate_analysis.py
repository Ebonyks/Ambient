from pathlib import Path
import numpy as np,json,soundfile as sf
import analyze_streams as a
root=a.ROOT
sr=22050;sec=24
tt=np.arange(sr*sec)/sr
rng=np.random.default_rng(92726)
specs=[('clean_minor',[48,51,55],0),('noisy_minor',[48,51,55],.025),('distorted_fifth',[41,48],.015)]
res=[]
for name,notes,noise in specs:
    y=np.zeros_like(tt)
    for m in notes:
        f=440*2**((m-69)/12)
        for h in range(1,7):y+=np.sin(2*np.pi*f*h*tt)/(h**1.2)
    y/=max(abs(y));y*=.25
    if 'distorted' in name:y=np.tanh(y*4)*.3
    y+=rng.standard_normal(len(y))*noise
    y*=np.minimum(tt,1)*np.minimum(sec-tt,1)
    p=root/(name+'.wav');sf.write(p,np.column_stack([y,y]),sr)
    t={'album':'validation','track_num':len(res)+1,'title':name,'analysis_wav_path':str(p)}
    a.analyze(t)
    q=json.loads((a.OUT/('validation_'+str(len(res)+1).zfill(2)+'.json')).read_text())
    inferred=[x['midi'] for x in q['sections'][0]['voicing_candidates'][:len(notes)]]
    res.append({'test':name,'known_midi':notes,'top_inferred_midi':inferred,'all_known_in_top_n':set(notes)==set(inferred)})
(root/'validation.json').write_text(json.dumps(res,indent=2))
print(json.dumps(res,indent=2))
