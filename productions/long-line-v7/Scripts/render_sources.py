"""Render the v7 score through v6's CC0 piano-tail palette; retain independent returns."""
from pathlib import Path
import json, numpy as np, soundfile as sf
from scipy import signal
R=Path(__file__).resolve().parents[1]; OLD=R.parent/'long-line-v6'; S=24000;D=336;N=S*D

if any((R/'Media').glob('*.flac')):raise SystemExit('Existing candidate stems preserved. Render a new candidate in a separate version directory.')

def filt(x,lo,hi):return signal.sosfilt(signal.butter(2,[lo,hi],btype='bandpass',fs=S,output='sos'),x,axis=0).astype('float32')
def rms(x):return np.sqrt(np.mean(x.astype('float64')**2))+1e-10
samples={}
for p in (OLD/'Sources').glob('UR1*.flac'):
    name=p.stem.split('_')[1];m={'C':0,'G':7}[name[0]]+(int(name[1])+1)*12
    x,s=sf.read(p,dtype='float32',always_2d=True)
    if x.shape[1]==1:x=np.repeat(x,2,axis=1)
    samples[m]=signal.resample_poly(x,S//np.gcd(s,S),s//np.gcd(s,S),axis=0)

def voice(e,i):
    d=e['end_s']-e['start_s'];m=e['midi'];c=e['cents'];L=round(d*S);G=2640
    root=min(samples,key=lambda a:abs(a-m));src=samples[root];rr=np.random.default_rng(800+i)
    z=np.zeros((L,2),np.float32);weight=np.zeros(L,np.float32);win=np.hanning(G).astype('float32');ix=np.arange(G)*2**((m-root+c/100)/12);sourcepos=np.arange(len(src))
    # Same 110ms / four-overlap source as v6, variable position, stable pitch per note.
    for pos in range(-G,L,G//4):
        off=np.clip(.7+.28*np.sin(pos/S*.081+i)+rr.uniform(-.035,.035),.24,2.2)*S
        q=np.column_stack([np.interp(off+ix,sourcepos,src[:,ch]) for ch in range(2)])
        a=max(0,pos);b=min(L,pos+G)
        if b>a:z[a:b]+=q[a-pos:b-pos]*win[a-pos:b-pos,None];weight[a:b]+=win[a-pos:b-pos]
    z/=np.maximum(weight,.2)[:,None];z=filt(z,160 if e['voice']==2 else 90,4000 if e['voice']==2 else 3600);z*=.126/rms(z)
    tt=np.arange(L)/S;attack=.38 if e['voice']==2 else .65;release=.8
    shape=np.sin(np.minimum(tt/attack,1)*np.pi/2)**2*np.sin(np.minimum((d-tt)/release,1)*np.pi/2)**2
    pan=(-.22,.25,.04)[e['voice']];z*=np.array([np.sqrt(1-pan),np.sqrt(1+pan)])
    return (z*shape[:,None]*(.145 if e['voice']==2 else .10)).astype('float32')

def out(name,x):
    assert np.isfinite(x).all() and np.max(abs(x))<.95
    sf.write(R/'Media'/f'{name}.flac',signal.resample_poly(x,2,1,axis=0),48000,subtype='PCM_24');print(name,round(float(rms(x)),5),flush=True)

def dirty(x,drive,gain):
    h=signal.resample_poly(x,4,1,axis=0);h*=.126/rms(h)
    h=np.tanh(h*drive)+.16*np.sin(h*drive*2.7)
    z=filt(signal.resample_poly(h,1,4,axis=0),240,3600);return z*(rms(x)/rms(z))*gain

score=json.loads((R/'weave.json').read_text(encoding='utf8'));body=np.zeros((N,2),np.float32);lead=np.zeros_like(body)
for i,e in enumerate(score['events']):
    if e['voice']==3:continue
    z=voice(e,i);a=round(e['start_s']*S);b=min(N,a+len(z));dest=lead if e['voice']==2 else body;dest[a:b]+=z[:b-a]
    if i%30==0:print('Rendered event',i,flush=True)
out('02_Moving_inner_voices',body);out('03_Developing_foreground',lead)
wet=dirty(body,10**(.6),.26);grain=dirty(lead,10**(.75),.62)
out('04_Eroded_melodic_return',grain);out('05_Independent_distorted_body',wet)
res=np.zeros_like(body)
for delay,g in [(1.137,.08),(2.719,.065),(4.183,.042),(6.347,.026)]:
    n=int(delay*S);res[n:]+=grain[:-n,::-1]*g+wet[:-n]*g*.4
out('06_Source_residue',filt(res,500,3000))
(R/'Audit/synthesis.json').write_text(json.dumps({'sample_source':'../long-line-v6/Sources/UR1*.flac; existing CC0 VSCO upright tails','source_rate':S,'delivery_rate':48000,'grain_ms':110,'grain_overlap':4,'position_jitter_ms':35,'pitch_jitter':0,'parallel_oversampling':4,'attack_seconds':{'foreground':.38,'inner':.65},'release_seconds':.8,'held_tones':'One continuous source event; never retriggered at harmony boundary','inherited':'v6 anchor, water, wood and Valhalla Supermassive template','melody_residue':'Regenerated from new events, no old arch retained','caution':'Same source palette and routing; envelopes and parallel transfer adapted for shorter voices, not identical timbre'},indent=2),encoding='utf8')
