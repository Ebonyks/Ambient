import os
os.environ['OMP_NUM_THREADS']='2'
os.environ['OPENBLAS_NUM_THREADS']='2'
from pathlib import Path
import json,sys,time,math,hashlib
import numpy as np
import soundfile as sf
import librosa
from scipy.ndimage import median_filter,gaussian_filter1d
from scipy.signal import find_peaks
from scipy.optimize import nnls

ROOT=Path(__file__).parent/'audio_analysis'
OUT=ROOT/'features';OUT.mkdir(exist_ok=True)
MAN=json.loads((ROOT/'manifest.json').read_text())
PC=['C','C#','D','Eb','E','F','F#','G','Ab','A','Bb','B']
def note(m):return PC[int(m)%12]+str(int(m)//12-1)
def norm(x):return x/(np.linalg.norm(x,axis=0,keepdims=True)+1e-9)
MAJ=np.array([6.35,2.23,3.48,2.33,4.38,4.09,2.52,5.19,2.39,3.66,2.29,2.88])
MIN=np.array([6.33,2.68,3.52,5.38,2.60,3.53,2.54,4.75,3.98,2.69,3.34,3.17])
def keys(c):
    rows=[]
    for kind,template in [('major',MAJ),('minor',MIN)]:
        for p in range(12):
            r=float(np.corrcoef(c,np.roll(template,p))[0,1]) if np.std(c)>1e-10 else 0
            rows.append({'label':PC[p]+' '+kind,'correlation':round(r,3)})
    return sorted(rows,key=lambda x:x['correlation'],reverse=True)[:3]

def analyze(t):
    ident=t['album']+'_'+str(t['track_num']).zfill(2)
    if (OUT/(ident+'.json')).exists():print('cached',ident,flush=True);return
    print('START',ident,flush=True);start=time.time()
    stereo,sr=sf.read(t['analysis_wav_path'],dtype='float32',always_2d=True)
    y=stereo.mean(axis=1);dur=len(y)/sr
    hop=2048
    C=np.abs(librosa.cqt(y=y,sr=sr,hop_length=hop,fmin=librosa.midi_to_hz(24),n_bins=252,bins_per_octave=36,tuning=0)).astype('float32')
    ft=librosa.frames_to_time(np.arange(C.shape[1]),sr=sr,hop_length=hop)
    # Half-second medians; fixed A440 bins preserve rather than conceal detuning.
    n=int(np.ceil(dur/.5))
    X=np.zeros((252,n),dtype='float32')
    for j in range(n):
        ix=(ft>=j*.5)&(ft<(j+1)*.5)
        if ix.any():X[:,j]=np.median(C[:,ix],axis=1)
    del C
    # Remove locally broad spectral components; no claim this is source separation.
    floor=median_filter(X,size=(13,1),mode='nearest')
    tonal=np.maximum(X-floor,0)
    # Harmonic-template deconvolution; results are candidates, not verified score notes.
    grid=24+np.arange(252)/3
    mids=np.arange(24,96)
    W=np.zeros((252,len(mids)))
    for j,m in enumerate(mids):
        for h in range(1,9):
            center=m+12*np.log2(h)
            W[:,j]+=np.exp(-.5*((grid-center)/.28)**2)/(h**1.2)
    W=norm(W)
    A=np.zeros((len(mids),n),dtype='float32')
    rawfund=np.zeros_like(A)
    for j,m in enumerate(mids):
        ix=np.where(np.abs(grid-m)<=.5)[0]
        rawfund[j]=np.max(tonal[ix],axis=0)
    for j in range(n):
        v=tonal[:,j]
        if np.max(v)<1e-8:continue
        sal=W.T@v
        active=np.argsort(sal)[-18:]
        fit,_=nnls(W[:,active],v,maxiter=180)
        A[active,j]=fit
    A=median_filter(A,size=(1,3))
    chroma=np.zeros((12,n))
    for j,m in enumerate(mids):chroma[m%12]+=A[j]
    direct=np.zeros((12,n))
    for j,m in enumerate(mids):direct[m%12]+=rawfund[j]
    rms=[];cent=[];flat=[];side=[];bands=[]
    for j in range(n):
        seg=stereo[int(j*.5*sr):int(min(dur,(j+1)*.5)*sr)]
        if len(seg)==0:seg=stereo[-1:]
        mono=seg.mean(axis=1)
        rms.append(20*np.log10(np.sqrt(np.mean(mono**2))+1e-10))
        ss=np.abs(np.fft.rfft(mono*np.hanning(len(mono))))**2
        ff=np.fft.rfftfreq(len(mono),1/sr)
        cent.append(float(np.sum(ff*ss)/(ss.sum()+1e-15)))
        flat.append(float(np.exp(np.mean(np.log(ss+1e-15)))/(ss.mean()+1e-15)))
        mid=seg.mean(axis=1);s=(seg[:,0]-seg[:,1])/2
        side.append(float(10*np.log10((np.mean(s*s)+1e-12)/(np.mean(mid*mid)+1e-12))))
        bands.append([float(ss[(ff>=lo)&(ff<hi)].sum()) for lo,hi in [(20,150),(150,500),(500,2000),(2000,6000),(6000,11025)]])
    rms=np.array(rms);cent=np.array(cent);flat=np.array(flat);side=np.array(side);bands=np.array(bands).T
    # 8-second context novelty combines pitch distribution, level, brightness, stereo.
    feat=np.vstack([norm(chroma),norm(np.sqrt(bands)),rms[None,:]/20,np.log2(cent[None,:]+1)/4,side[None,:]/20])
    sm=gaussian_filter1d(feat,3,axis=1)
    nov=np.zeros(n)
    for j in range(16,n-16):nov[j]=np.linalg.norm(sm[:,j:j+16].mean(axis=1)-sm[:,j-16:j].mean(axis=1))
    threshold=max(float(np.percentile(nov,70)),.15)
    peaks,_=find_peaks(nov,distance=30,prominence=threshold*.45,height=threshold)
    bounds=[0]+[int(x) for x in peaks if x*.5>10 and x*.5<dur-10]+[n]
    # Limit very long low-novelty regions to readable 90s analysis windows.
    expanded=[0]
    for b in bounds[1:]:
        while b-expanded[-1]>180:expanded.append(expanded[-1]+180)
        expanded.append(b)
    bounds=expanded
    sections=[]
    for idx,(a,b) in enumerate(zip(bounds,bounds[1:])):
        e=A[:,a:b].mean(axis=1)
        order=np.argsort(e)[::-1]
        notes=[]
        for i in order[:8]:
            if e[i]<max(e)*.12:continue
            supported=float(np.mean(rawfund[i,a:b]>.15*np.max(rawfund[:,a:b],axis=0)))
            notes.append({'note':note(mids[i]),'midi':int(mids[i]),'relative_salience':round(float(e[i]/(max(e)+1e-9)),3),'fundamental_support_fraction':round(supported,3)})
        c=chroma[:,a:b].mean(axis=1);dc=direct[:,a:b].mean(axis=1)
        k=keys(c);dk=keys(dc)
        pcorder=np.argsort(c)[::-1]
        # Local sinusoidal peaks via Welch-style averaged 2s spectra, independent of CQT dictionary.
        yy=y[int(a*.5*sr):int(min(dur,b*.5)*sr)]
        N=65536;spec=np.zeros(N//2+1);count=0
        for off in range(0,max(1,len(yy)-N+1),N//2):
            chunk=yy[off:off+N]
            if len(chunk)<N:chunk=np.pad(chunk,(0,N-len(chunk)))
            spec+=np.abs(np.fft.rfft(chunk*np.hanning(N)))**2;count+=1
        ff=np.fft.rfftfreq(N,1/sr)
        ids,_=find_peaks(spec,distance=3)
        ids=[i for i in ids if 35<ff[i]<2200]
        ids=sorted(ids,key=lambda i:spec[i],reverse=True)[:10]
        partials=[]
        for i in ids:
            logs=np.log(spec[i-1:i+2]+1e-20)
            delta=.5*(logs[0]-logs[2])/(logs[0]-2*logs[1]+logs[2]+1e-20)
            hz=float((i+np.clip(delta,-.5,.5))*sr/N)
            midi=69+12*np.log2(hz/440)
            partials.append({'hz':round(hz,2),'nearest_note':note(round(midi)),'cents_from_A440_note':round(float((midi-round(midi))*100),1),'relative_db':round(float(10*np.log10((spec[i]+1e-20)/(max(spec)+1e-20))),1)})
        sections.append({'section':idx+1,'start_s':round(a*.5,2),'end_s':round(min(dur,b*.5),2),'boundary_kind':'measured novelty candidate or 90s analysis cap','pitch_class_ranking':[PC[i] for i in pcorder[:7]],'key_profile_candidates':k,'direct_spectrum_key_candidates':dk,'key_model_agreement':k[0]['label']==dk[0]['label'],'voicing_candidates':notes,'prominent_spectral_partials':partials,'rms_dbfs':round(float(rms[a:b].mean()),2),'power_centroid_hz':round(float(cent[a:b].mean()),1),'side_to_mid_db':round(float(side[a:b].mean()),2),'spectral_flatness':round(float(flat[a:b].mean()),4)})
    # Candidate note regions; not independent voices or a polyphonic transcription.
    events=[]
    rel=A/(A.max(axis=0,keepdims=True)+1e-9)
    for i,m in enumerate(mids):
        active=(rel[i]>.28)&(rawfund[i]>.08*rawfund.max(axis=0))&(rms>-55)
        edges=np.diff(np.r_[False,active,False].astype(int));ons=np.where(edges==1)[0];offs=np.where(edges==-1)[0]
        for a,b in zip(ons,offs):
            if b-a>=3:events.append({'pitch_midi':int(m),'note':note(m),'start_s':round(a*.5,2),'duration_s':round(min(dur,b*.5)-a*.5,2),'mean_relative_salience':round(float(rel[i,a:b].mean()),3),'status':'machine_pitch_candidate_not_verified_note'})
    events.sort(key=lambda x:(x['start_s'],x['pitch_midi']))
    result={**t,'id':ident,'decoded_duration_s':round(dur,3),'analysis_hop_s':.5,'status':'audio_measured_with_inferred_pitch_candidates','sections':sections,'candidate_events':events,'cautions':['MP3 stream, not lossless mastering reference','Tonal profile correlation is not confidence probability','Spectral partials can be harmonics rather than played notes','Voicing candidates summarize a section and are not necessarily simultaneous','No automatic meter or monophonic transcription assumed']}
    np.savez_compressed(OUT/(ident+'.npz'),activation=A,direct_fund=rawfund,chroma=chroma,direct_chroma=direct,rms=rms,centroid=cent,flatness=flat,side=side,novelty=nov,midi=mids,hop_s=.5)
    (OUT/(ident+'.json')).write_text(json.dumps(result,indent=2),encoding='utf-8')
    print('DONE',ident,len(sections),'sections',len(events),'events',round(time.time()-start,1),'sec',flush=True)

if __name__=='__main__':
    selected=sys.argv[1:]
    for t in MAN:
        ident=t['album']+'_'+str(t['track_num']).zfill(2)
        if not selected or ident in selected:analyze(t)
