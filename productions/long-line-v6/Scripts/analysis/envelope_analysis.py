from pathlib import Path
import json,numpy as np,soundfile as sf
from scipy.signal import butter,sosfilt,find_peaks,correlate
from scipy.ndimage import gaussian_filter1d
root=Path(__file__).parent/'audio_analysis';F=root/'features'
for p in sorted(F.glob('*.json')):
    if p.stem.startswith('validation'):continue
    t=json.loads(p.read_text());y,sr=sf.read(t['analysis_wav_path'],dtype='float32',always_2d=True)
    N=441;n=len(y)//N;mono=y[:n*N].mean(axis=1)
    broad=np.sqrt(np.mean(mono.reshape(n,N)**2,axis=1))
    filt=sosfilt(butter(3,[500,4000],btype='band',fs=sr,output='sos'),mono)
    high=np.sqrt(np.mean(filt.reshape(n,N)**2,axis=1))
    left=np.sqrt(np.mean(y[:n*N,0].reshape(n,N)**2,axis=1));right=np.sqrt(np.mean(y[:n*N,1].reshape(n,N)**2,axis=1))
    log=np.log(high+1e-7);nov=np.maximum(np.diff(log,prepend=log[0]),0)
    peaks,_=find_peaks(nov,distance=4,prominence=max(.08,float(np.percentile(nov,85))))
    for s in t['sections']:
        a=int(s['start_s']/.02);b=min(n,int(s['end_s']/.02))
        v=log[a:b];v=v-gaussian_filter1d(v,50)
        ac=correlate(v,v,mode='full',method='fft')[len(v)-1:];ac=ac/(ac[0]+1e-12)
        ps,_=find_peaks(ac[4:min(200,len(ac))],distance=4)
        ps=ps+4
        if len(ps):
            i=ps[np.argmax(ac[ps])]
            s['amplitude_period_candidate_s']=round(float(i*.02),3)
            s['amplitude_period_autocorrelation']=round(float(ac[i]),3)
        else:s['amplitude_period_candidate_s']=None;s['amplitude_period_autocorrelation']=0
        ss=peaks[(peaks>=a)&(peaks<b)]
        s['detected_envelope_attack_rate_hz']=round(float(len(ss)/max(.1,s['end_s']-s['start_s'])),3)
    np.savez_compressed(F/(t['id']+'_envelope.npz'),time_s=np.arange(n)*.02,mono_rms=broad,left_rms=left,right_rms=right,band500_4000_rms=high,attack_candidate_times_s=peaks*.02)
    p.write_text(json.dumps(t,indent=2),encoding='utf-8')
    print(t['id'],'envelopes done',flush=True)
