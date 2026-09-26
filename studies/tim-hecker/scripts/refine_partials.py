from pathlib import Path
import json,sys,numpy as np,soundfile as sf
from scipy.signal import find_peaks
ROOT=Path(__file__).parent/'audio_analysis';F=ROOT/'features'
for p in sorted(F.glob('*.json')):
    if len(sys.argv)>1 and p.stem not in sys.argv[1:]:continue
    t=json.loads(p.read_text());y,sr=sf.read(t['analysis_wav_path'],dtype='float32',always_2d=True);y=y.mean(axis=1)
    for s in t['sections']:
        yy=y[int(s['start_s']*sr):int(s['end_s']*sr)]
        N=65536;sp=np.zeros(N//2+1)
        for off in range(0,max(1,len(yy)-N+1),N//2):
            c=yy[off:off+N]
            if len(c)<N:c=np.pad(c,(0,N-len(c)))
            sp+=abs(np.fft.rfft(c*np.hanning(N)))**2
        hz=np.fft.rfftfreq(N,1/sr)
        for n in s['voicing_candidates']:
            freq=440*2**((n['midi']-69)/12)
            ids=np.where((hz>freq*2**(-.45/12))&(hz<freq*2**(.45/12)))[0]
            if not len(ids):continue
            i=ids[np.argmax(sp[ids])]
            near=(hz>freq*2**(-1.5/12))&(hz<freq*2**(1.5/12))&(abs(hz-hz[i])>sr/N*2)
            prom=10*np.log10((sp[i]+1e-20)/(np.median(sp[near])+1e-20)) if near.any() else 0
            logs=np.log(sp[max(0,i-1):i+2]+1e-20)
            delta=.5*(logs[0]-logs[2])/(logs[0]-2*logs[1]+logs[2]+1e-20)
            f=(i+np.clip(delta,-.5,.5))*sr/N
            n['measured_peak_hz']=round(float(f),2)
            n['peak_cents_from_note']=round(float(1200*np.log2(f/freq)),1)
            n['local_peak_prominence_db']=round(float(prom),1)
            n['narrow_peak_supported']=bool(prom>=6 and n['fundamental_support_fraction']>=.25)
        for n in s['prominent_spectral_partials']:
            i=np.argmin(abs(hz-n['hz']));freq=hz[i]
            near=(hz>freq*2**(-1.5/12))&(hz<freq*2**(1.5/12))&(abs(hz-freq)>sr/N*2)
            n['local_peak_prominence_db']=round(float(10*np.log10((sp[i]+1e-20)/(np.median(sp[near])+1e-20))),1) if near.any() else 0
        confirmed=[n for n in s['voicing_candidates'] if n.get('narrow_peak_supported')]
        s['supported_pitch_components']=[n['note'] for n in confirmed]
        s['tonality_status']='pitched_components_supported_mode_unverified' if len(confirmed)>=2 else 'insufficient_narrow_peak_support_for_key_claim'
    p.write_text(json.dumps(t,indent=2),encoding='utf-8')
    print(t['id'],sum(bool(s['supported_pitch_components']) for s in t['sections']),'/',len(t['sections']),'sections with narrow peaks',flush=True)
