from pathlib import Path
import json,numpy as np,soundfile as sf
from scipy.signal import butter,sosfiltfilt,resample_poly,correlate,correlation_lags
ROOT=Path(__file__).parent/'audio_analysis'
def excerpt(path,start,duration):
    with sf.SoundFile(path) as f:
        f.seek(int(start*f.samplerate));sr=f.samplerate;y=f.read(int(duration*sr),dtype='float32',always_2d=True).mean(axis=1)
    return resample_poly(y,1,5)
manifest={t['album']+'_'+str(t['track_num']).zfill(2):t for t in json.loads((ROOT/'manifest.json').read_text())}
matches=json.loads((ROOT/'live_matches.json').read_text())
chosen=[]
for x in matches:
    c=x['top_candidates'][0]
    if c['score']>.77 and c['studio_seconds_per_live_second']==1 and c['temporal_shape_similarity']>.5:chosen.append((x,c))
rows=[];sr=4410
for x,c in chosen:
    ls=x['live_start_s'];ss=c['studio_start_s']
    a=excerpt(manifest[c['studio_id']]['analysis_wav_path'],ss,25)
    b=excerpt(manifest['mort_aux_vaches_01']['analysis_wav_path'],max(0,ls-4),33)
    vals=[]
    for lo,hi in [(70,400),(400,1500)]:
        sos=butter(4,[lo,hi],btype='band',fs=sr,output='sos')
        aa=sosfiltfilt(sos,a);bb=sosfiltfilt(sos,b)
        cc=correlate(bb,aa,mode='valid',method='fft')
        den=np.sqrt(np.convolve(bb*bb,np.ones(len(aa)),mode='valid')*sum(aa*aa)) if False else None
        cum=np.r_[0,np.cumsum(bb*bb)];energy=cum[len(aa):]-cum[:-len(aa)]
        corr=cc/(np.sqrt(energy*sum(aa*aa))+1e-12)
        k=np.argmax(abs(corr));vals.append({'band_hz':[lo,hi],'correlation':round(float(corr[k]),4),'best_live_start_s':round(max(0,ls-4)+k/sr,3)})
    rows.append({'studio_id':c['studio_id'],'studio_start_s':ss,'live_query_start_s':ls,'duration_s':25,'feature_score':c['score'],'waveform_checks':vals})
(ROOT/'waveform_match_checks.json').write_text(json.dumps(rows,indent=2))
print(json.dumps(rows,indent=2))
