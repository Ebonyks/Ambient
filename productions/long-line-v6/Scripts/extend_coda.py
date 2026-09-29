from pathlib import Path
import numpy as np,soundfile as sf,json
R=Path(__file__).resolve().parents[1]
changes=[]
for original,source,name,target in [('03_Pitched_motif_route','02_Eroded_arch_and_pitch_drift','03_Pitched_motif_coda',.016),('04_Eroded_motif_return','K_continuous_arch','04_Eroded_motif_coda',.005)]:
 x,s=sf.read(R/'Media'/f'{original}.flac',dtype='float32',always_2d=True);src,sr=sf.read(R/'Sources'/f'{source}.flac',dtype='float32',always_2d=True);assert sr==s
 segment=src[70*s:int(71.5*s)];L=9*s;G=len(segment);win=np.hanning(G).astype('float32');z=np.zeros((L,2),np.float32);w=np.zeros(L,np.float32)
 for j in range(-G,L,G//4):
  a=max(0,j);b=min(L,j+G)
  if b>a:z[a:b]+=segment[a-j:b-j]*win[a-j:b-j,None];w[a:b]+=win[a-j:b-j]
 z/=np.maximum(w,.1)[:,None];z*=target/(np.sqrt(np.mean(z*z))+1e-12);tt=np.arange(L)/s;shape=np.sin(np.minimum(tt/2.8,1)*np.pi/2)**2*np.minimum((9-tt)/6,1)**2;z*=shape[:,None]
 x[323*s:332*s]+=z;sf.write(R/'Media'/f'{name}.flac',x,s,subtype='PCM_24');changes.append({'stem':name,'source':source,'source_interval_s':[70,71.5],'placement_s':[323,332],'method':'Overlapped continuation of existing D; 2.8s entry / 6s release; no new pitch or source instrument'})
(R/'Audit/coda_continuation.json').write_text(json.dumps(changes,indent=2));print('Closing D continuation prepared')
