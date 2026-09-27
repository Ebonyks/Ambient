from pathlib import Path
import json,hashlib,numpy as np,soundfile as sf
from scipy import signal
R=Path(__file__).resolve().parents[1]
CACHE=Path('C:/Users/Peter/Music/Ambient Reference Cache/continuous-study')
def measure(path):
 x,sr=sf.read(path,always_2d=True);y=x.mean(axis=1);f,t,z=signal.stft(y,sr,nperseg=2048,noverlap=1808);a=np.abs(z);keep=(f>=90)&(f<6000);a=a[keep];f=f[keep]
 flux=np.maximum(np.diff(np.log1p(a*1000),axis=1),0).mean(axis=0);med=np.median(flux);mad=np.median(abs(flux-med))+1e-9;hop=t[1]-t[0]
 rates={}
 for threshold in [1,2,3]:
  peaks,_=signal.find_peaks(flux,height=med+threshold*mad,distance=max(1,round(.065/hop)));rates[str(threshold)]=len(peaks)/(len(y)/sr)
 chroma=np.zeros((12,len(t)));pc=np.round(69+12*np.log2(f/440)).astype(int)%12
 for k in range(12):chroma[k]=np.sum(a[pc==k]**2,axis=0)
 chroma/=np.sqrt(np.sum(chroma**2,axis=0,keepdims=True))+1e-12
 lag=round(2/hop);similarity=np.sum(chroma[:,:-lag]*chroma[:,lag:],axis=0)
 return {'duration_s':len(y)/sr,'flux_peak_rates_per_s_by_MAD_threshold':rates,'median_2s_spectral_chroma_cosine':float(np.median(similarity)),'rms':float(np.sqrt(np.mean(y*y))),'meaning':'Flux peaks are articulation proxies, NOT performed-note counts. Spectral chroma includes overtones and processing; no chord transcription.'}
if __name__=='__main__':
 rows=[]
 for e in json.loads((CACHE/'excerpts.json').read_text()):
  rows.append({'source_file':Path(e['source']).name,'source_sha256':e['source_sha256'],'start_s':e['start_s'],'measurement':measure(e['excerpt'])})
 (R/'Audit/reference_measurements.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
