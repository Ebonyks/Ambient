from pathlib import Path
import soundfile as sf,numpy as np,json,subprocess,re,hashlib,shutil
R=Path(__file__).resolve().parents[1];ff=shutil.which('ffmpeg') or r'C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\FFmpeg\8.1.2\bin\ffmpeg.exe';p=R/'Renders/Long Line - Full Length - Study Draft - 5m36.wav'
x,s=sf.read(p,dtype='float32',always_2d=True)
c=subprocess.run([ff,'-hide_banner','-i',str(p),'-af','loudnorm=I=-20:TP=-2:LRA=15:print_format=json','-f','null','NUL'],text=True,capture_output=True);v=json.loads(re.findall(r'\{\s*"input_i".*?\}',c.stderr,re.S)[-1])
data={'duration_seconds':len(x)/s,'sample_rate':s,'channels':x.shape[1],'integrated_lufs':float(v['input_i']),'true_peak_dbtp':float(v['input_tp']),'loudness_range_lu':float(v['input_lra']),'clipped_samples':int(np.sum(abs(x)>=1)),'nonfinite_samples':int(np.sum(~np.isfinite(x))),'stereo_correlation':float(np.corrcoef(x.T)[0,1]),'wav_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'renderer':'Native REAPER 48kHz 24-bit stereo; no loudness normalization or master limiter'}
(R/'Audit/final_measurements.json').write_text(json.dumps(data,indent=2));print(json.dumps(data,indent=2))
for a in range(0,336,20):sf.write(R/'Listening'/f'full_{a:03d}.wav',x[a*s:min((a+20)*s,len(x))],s,subtype='PCM_16')
subprocess.run([ff,'-y','-hide_banner','-loglevel','error','-i',str(p),'-codec:a','libmp3lame','-b:a','256k','-metadata','title=Long Line - Full Length Study Draft',str(p.with_suffix('.mp3'))],check=True)
dest=R/'Scripts/analysis/audio_analysis/full_draft.wav';subprocess.run([ff,'-y','-hide_banner','-loglevel','error','-i',str(p),'-ar','22050','-c:a','pcm_s24le',str(dest)],check=True)
manpath=R/'Scripts/analysis/audio_analysis/manifest.json';man=json.loads(manpath.read_text());man=[t for t in man if t['track_num']!=8];man.append({'album':'long_line','track_num':8,'title':'Long Line full length','duration':336,'page':'original composition','stream_sha256':data['wav_sha256'],'source_quality':'48kHz 24-bit native REAPER WAV, decoded at 22050 Hz for identical extractor','analysis_wav_path':str(dest)});manpath.write_text(json.dumps(man,indent=2))
# Controlled envelope ablation at 112 s, matched source, duration and RMS. Reviewer filenames conceal condition.
b,s=sf.read(R/'Media/02_Tied_inner_voices.flac',dtype='float32',always_2d=True);a=b[100*s:120*s].copy();tt=np.arange(len(a))/s;gate=np.interp(tt,[0,11.65,12,14.2,20],[1,1,0,1,1]);variants={'control_X':a,'control_Y':a*gate[:,None]}
for k,z in variants.items():z*=.0631/(np.sqrt(np.mean(z*z))+1e-12);sf.write(R/'Listening'/f'{k}.wav',z,s,subtype='PCM_16')
(R/'Audit/control_key.json').write_text(json.dumps({'control_X':'tied original inner-body envelope','control_Y':'simulated synchronized reattack envelope at 112 seconds; source waveform preserved; no harmonic change','both':'20s, same source and RMS; tests one envelope behavior only, not complete synthesis quality'},indent=2))
