import os
os.environ['OPENBLAS_NUM_THREADS']='4'
from pathlib import Path
import numpy as np,json
from scipy.ndimage import gaussian_filter1d
ROOT=Path(__file__).parent/'audio_analysis';F=ROOT/'features'

def normalize(a,axis=0):return a/(np.linalg.norm(a,axis=axis,keepdims=True)+1e-9)
def features(p):
    z=np.load(p);a=z['activation'].astype(float)
    # Downsample to 2s; discount low frequency rumble bins below C2.
    a[:12]*=.25
    a=gaussian_filter1d(a,1,axis=1)
    n=a.shape[1]//4;a=a[:,:n*4].reshape(72,n,4).mean(axis=2)
    c=np.zeros((12,n))
    for i in range(72):c[i%12]+=a[i]
    return np.vstack([normalize(np.sqrt(a))*.8,normalize(np.sqrt(c))*.6]).astype('float32')
stud=[]
for p in sorted(F.glob('*.npz')):
    if p.stem.startswith(('radio_amor_', 'mirages_')) and not p.stem.endswith('_envelope'):stud.append((p.stem,features(p)))
live=features(F/'mort_aux_vaches_01.npz')
allvec=[];allshape=[];meta=[]
L=15
for ident,a in stud:
    for speed in [.75,1.,1.25,1.5]:
        # studio_seconds/live_seconds; resample studio window onto live 30s grid
        width=(L-1)*speed
        for s in range(0,max(0,int(a.shape[1]-width-1)),2):
            xx=s+np.arange(L)*speed
            w=np.array([np.interp(xx,np.arange(a.shape[1]),row) for row in a]).astype('float32')
            v=w.flatten();v/=np.linalg.norm(v)+1e-9
            d=w-w.mean(axis=1,keepdims=True);d=d.flatten();energy=np.linalg.norm(d);d/=energy+1e-9
            allvec.append(v);allshape.append(d);meta.append((ident,s*2,float(speed),float(energy)))
V=np.array(allvec);D=np.array(allshape)
results=[]
for s in range(0,live.shape[1]-L,7):
    w=live[:,s:s+L];v=w.flatten();v/=np.linalg.norm(v)+1e-9
    d=w-w.mean(axis=1,keepdims=True);d=d.flatten();energy=np.linalg.norm(d);d/=energy+1e-9
    absolute=V@v;shape=D@d
    score=.60*absolute+.40*shape
    order=np.argsort(score)[::-1]
    top=[];used=set()
    for k in order:
        ident,ss,speed,se=meta[k]
        if ident in used:continue
        used.add(ident)
        top.append({'studio_id':ident,'studio_start_s':ss,'studio_end_s':round(ss+30*speed,2),'studio_seconds_per_live_second':speed,'score':round(float(score[k]),4),'absolute_similarity':round(float(absolute[k]),4),'temporal_shape_similarity':round(float(shape[k]),4),'studio_window_variation':round(se,3)})
        if len(top)==3:break
    results.append({'live_start_s':s*2,'live_end_s':s*2+30,'live_window_variation':round(float(energy),3),'top_candidates':top,'status':'retrieval_candidates_not_accepted_correspondence'})
out=ROOT/'live_matches.json';out.write_text(json.dumps(results,indent=2),encoding='utf-8')
for x in results:
    t=x['top_candidates'][0]
    if t['score']>.77:print(x['live_start_s'],t,flush=True)
print('Wrote',len(results),'live windows;',len(meta),'studio reference windows')
