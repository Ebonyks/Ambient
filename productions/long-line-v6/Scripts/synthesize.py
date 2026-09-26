from pathlib import Path
import numpy as np,soundfile as sf,json
from scipy import signal
from scipy.ndimage import maximum_filter1d,gaussian_filter1d
R=Path(__file__).resolve().parents[1];S=24000;D=336;N=D*S;T=np.arange(N,dtype=np.float64)/S
rng=np.random.default_rng(260926)
def read(p):
 x,s=sf.read(p,dtype='float32',always_2d=True)
 if x.shape[1]==1:x=np.repeat(x,2,axis=1)
 if s!=S:x=signal.resample_poly(x,S//np.gcd(s,S),s//np.gcd(s,S),axis=0)
 return x.astype('float32')
def filt(x,lo=None,hi=None):
 if lo and hi: sos=signal.butter(2,[lo,hi],btype='bandpass',fs=S,output='sos')
 else:sos=signal.butter(2,lo or hi,btype='highpass' if lo else 'lowpass',fs=S,output='sos')
 return signal.sosfilt(sos,x,axis=0).astype('float32')
def rms(x):return float(np.sqrt(np.mean(x.astype('float64')**2))+1e-10)
def norm(x,target):return x*(target/rms(x))
def env(points):return np.interp(T,*np.array(points).T).astype('float32')
def out(name,x):
 assert np.isfinite(x).all();assert np.max(abs(x))<.98,(name,np.max(abs(x)))
 z=signal.resample_poly(x,2,1,axis=0)
 if name in ['07_Water','08_Wood_air']:
  peak=maximum_filter1d(np.max(abs(z),axis=1),size=4801);g=gaussian_filter1d(np.minimum(1,.027/(peak+1e-10)),240);z*=g[:,None]
 sf.write(R/'Media'/f'{name}.flac',z,48000,subtype='PCM_24');print(name,'rms',round(rms(x),5),'peak',round(float(abs(x).max()),4),flush=True)
def put(x,z,t,g=1):
 a=int(t*S);b=min(N,a+len(z));x[a:b]+=z[:b-a]*g
samples={}
for p in (R/'Sources').glob('UR1*.flac'):
 n=p.stem.split('_')[1];m={'C':0,'G':7}[n[0]]+(int(n[1])+1)*12;samples[m]=read(p)
def piano_tail(m,c,d,seed):
 rr=np.random.default_rng(seed);root=min(samples,key=lambda a:abs(a-m));src=samples[root];L=int(d*S);z=np.zeros((L,2),np.float32);weight=np.zeros(L,np.float32)
 ratio=2**((m-root+c/100)/12);grain=.11;G=int(grain*S);win=np.hanning(G).astype('float32');ix=np.arange(G)*ratio;sourcepos=np.arange(len(src));pos=-G
 # 110-ms Hann grains / 4 overlaps, 35-ms position jitter; no random pitch jitter.
 while pos<L:
  clock=pos/S;off=np.clip(.7+.28*np.sin(clock*.081+seed)+rr.uniform(-.035,.035),.24,2.2)*S
  q=np.column_stack([np.interp(off+ix,sourcepos,src[:,ch])for ch in range(2)]).astype('float32')
  a=max(0,pos);b=min(L,pos+G)
  if b>a:z[a:b]+=q[a-pos:b-pos]*win[a-pos:b-pos,None];weight[a:b]+=win[a-pos:b-pos]
  pos+=G//4
 z/=np.maximum(weight,.2)[:,None];z=filt(z,90,3600);z=norm(z,.126)
 tt=np.arange(L)/S;shape=np.sin(np.minimum(tt/2.2,1)*np.pi/2)**2*np.sin(np.minimum((d-tt)/4.2,1)*np.pi/2)**2
 return z*shape[:,None]
events=json.loads((R/'voice_events.json').read_text());anchor=np.zeros((N,2),np.float32);body=np.zeros_like(anchor)
for ev in events:
 m,c,a,b=ev['midi'],ev['cents'],ev['start_s'],ev['end_s'];d=b-a
 if ev['role']=='anchor':
  tt=np.arange(int(d*S))/S;f=440*2**((m-69+c/100)/12)
  z=np.sin(2*np.pi*f*tt)+.12*np.sin(4*np.pi*f*tt)+.025*np.sin(6*np.pi*f*tt)
  shape=np.sin(np.minimum(tt/3.6,1)*np.pi/2)**2*np.sin(np.minimum((d-tt)/5.5,1)*np.pi/2)**2
  z=np.column_stack([z,z]).astype('float32')*shape[:,None];put(anchor,z,a,.014)
 else:
  z=piano_tail(m,c,d,300+ev['source_id']);pan=-.22 if m%2 else .25;z*=np.array([np.sqrt(1-pan),np.sqrt(1+pan)])
  put(body,z,a,.085 if m<60 else .07)
out('01_Anchor_bypasses_drive',anchor)
# Body has no synchronized swells: its changes are the authored source-voice entrances/exits.
out('02_Tied_inner_voices',body)
# Reference P3-style parallel: RMS-referenced, 4x oversampled tanh, loudness-matched before gain.
hi=signal.resample_poly(norm(body,.126),4,1,axis=0);wet=np.tanh(hi*10**(12/20));del hi
wet=signal.resample_poly(wet,1,4,axis=0).astype('float32');wet=filt(wet,180,3600);wet=norm(wet,rms(body))
wet*=env([(0,.14),(58,.18),(80,.20),(115,.14),(149,.14),(171,.22),(213,.30),(239,.35),(270,.27),(295,.20),(316,.13),(330,.1),(336,0)])[:,None]
out('05_Independent_distorted_body',wet)
clear=read(R/'Sources/02_Eroded_arch_and_pitch_drift.flac');dirty=read(R/'Sources/K_continuous_arch.flac')
lead=np.zeros_like(body);grain=np.zeros_like(body);phrases=json.loads((R/'phrase_map.json').read_text())['phrases']
for i,p in enumerate(phrases):
 a=p['source_start_s'];b=min(p['source_end_s'],38 if a==7 else 72 if a==38 else 108)
 p['source_end_s']=b
 for src,dest,target in [(clear,lead,.024),(dirty,grain,.024)]:
  z=src[int(a*S):int(b*S)].copy();z=norm(z,target);tt=np.arange(len(z))/S
  fade=np.minimum(1,tt/1.5)*np.minimum(1,((len(z)-1)/S-tt)/1.8);z*=np.maximum(fade,0)[:,None]
  # Exchange prominence and stereo placement, preserving event rate and complete motif order.
  if i in [2,5]:z=z[:,::-1]
  z=(z.mean(axis=1)[:,None]*.38+z*.62).astype('float32')
  put(dest,z,p['start_s'],p['gain'])
(R/'phrase_map.json').write_text(json.dumps({'phrases':phrases,'intent':'Complete motif statements; trimmed before the following statement attacks. Local source event timing retained.'},indent=2))
lead=filt(lead,280,4000);out('03_Pitched_motif_route',lead)
grain*=env([(0,.43),(55,.48),(92,.44),(137,.30),(175,.48),(218,.7),(243,.68),(279,.52),(299,.36),(327,.22),(336,0)])[:,None]
out('04_Eroded_motif_return',grain)
# Residue is a delayed copy of the same pitched object, never extra MIDI notes.
res=np.zeros_like(body)
for delay,g in [(1.137,.08),(2.719,.065),(4.183,.042),(6.347,.026)]:
 n=int(delay*S);res[n:]+=grain[:-n,::-1]*g+wet[:-n]*g*.4
res=filt(res,500,3000);out('06_Source_residue',res)
del clear,dirty,lead,grain,res,body,wet,anchor
# Environmental continuity uses long excerpts, equal-power seams and no rhythmic retriggers.
water=read(R/'Sources/stream.flac');wood=read(R/'Sources/tree_ms.flac')
wood=np.column_stack([wood[:,0]+.65*wood[:,1],wood[:,0]-.65*wood[:,1]]).astype('float32')
for name,src,target,overlap in [('07_Water',water,.008,9),('08_Wood_air',wood,.003,14)]:
 buf=np.zeros((N,2),np.float32);weight=np.zeros(N,np.float32);pos=0;L=len(src);fadeN=int(overlap*S)
 while pos<N:
  z=src.copy();w=np.ones(L,np.float32);w[:fadeN]=np.sin(np.linspace(0,np.pi/2,fadeN))**2;w[-fadeN:]=np.cos(np.linspace(0,np.pi/2,fadeN))**2
  b=min(N,pos+L);buf[pos:b]+=z[:b-pos]*w[:b-pos,None];weight[pos:b]+=w[:b-pos];pos+=L-fadeN
 buf/=np.maximum(weight,.2)[:,None];buf=filt(buf,120,6200);buf=norm(buf,target)
 buf*=env([(0,0),(3,1),(12,1),(27,.27),(65,.19),(112,.22),(147,.3),(173,.19),(229,.13),(277,.18),(309,.25),(326,.6),(331,.72),(334,.35),(336,0)])[:,None]
 out(name,buf)
(R/'synthesis_receipt.json').write_text(json.dumps({'duration_s':D,'synthesis_rate_hz':S,'delivery_rate_hz':48000,'new_saturation_oversampling':4,'source_rms_reference_dbfs':-18,'new_parallel_drive_db':12,'pitch_jitter_cents':0,'seed':260926,'common_source_events':len(events),'harmony_states':7,'legacy_motif_processing':'Preserved transformed piano/grain source, including prior distortion; not claimed to have been oversampled retroactively.','independent_roles':['anchor','pitched body','clearer upper motif','distorted returns','residue','environment']},indent=2))
print('Full-length sources complete',flush=True)
