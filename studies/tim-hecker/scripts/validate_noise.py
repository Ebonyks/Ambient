from pathlib import Path
import sys, subprocess, json
import numpy as np
import soundfile as sf
import analyze_streams as a

sr=22050
path=a.ROOT/'white_noise.wav'
rng=np.random.default_rng(260926)
y=rng.normal(0,.1,sr*30).astype('float32')
result=a.OUT/'validation_04.json'
# Preserve an existing diagnostic run rather than replacing its cached source.
if not result.exists():
    sf.write(path,np.column_stack([y,y]),sr)
    a.analyze({'album':'validation','track_num':4,'title':'white_noise','analysis_wav_path':str(path)})
subprocess.run([sys.executable,str(Path(__file__).parent/'refine_partials.py'),'validation_04'],check=True)
t=json.loads(result.read_text())
n=sum(bool(s['supported_pitch_components']) for s in t['sections'])
assert n==0, 'White noise unexpectedly passed the section pitch gate'
print('White-noise accepted pitch windows:',n)
