"""Render corrected inner/foreground piano sources for native plugin processing."""
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
    z/=np.maximum(weight,.2)[:,None];z=filt(z,160 if e['voice']==2 else 90,2600 if e['voice']==2 else 2100);z*=.126/rms(z)
    tt=np.arange(L)/S;attack=.55 if e['voice']==2 else .8;release=1.0
    shape=np.sin(np.minimum(tt/attack,1)*np.pi/2)**2*np.sin(np.minimum((d-tt)/release,1)*np.pi/2)**2
    pan=(-.22,.25,.04)[e['voice']];z*=np.array([np.sqrt(1-pan),np.sqrt(1+pan)])
    shape*=.62+.38*np.exp(-tt/2.7)
    return (z*shape[:,None]*(.11 if e['voice']==2 else .085)).astype('float32')

def out(name,x):
    assert np.isfinite(x).all() and np.max(abs(x))<.95
    sf.write(R/'Media'/f'{name}.flac',signal.resample_poly(x,2,1,axis=0),48000,subtype='PCM_24');print(name,round(float(rms(x)),5),flush=True)

score=json.loads((R/'weave.json').read_text(encoding='utf8'));body=np.zeros((N,2),np.float32);lead=np.zeros_like(body)
for i,e in enumerate(score['events']):
    if e['voice'] in [0,3]:continue
    z=voice(e,i);a=round(e['start_s']*S);b=min(N,a+len(z));dest=lead if e['voice']==2 else body;dest[a:b]+=z[:b-a]
    if i%30==0:print('Rendered event',i,flush=True)
out('02_Inner_piano',body);out('03_Foreground_piano',lead)
