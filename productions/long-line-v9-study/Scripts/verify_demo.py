from pathlib import Path
import json,hashlib,subprocess,sys,numpy as np,soundfile as sf
R=Path(__file__).resolve().parents[1];ROOT=R.parents[1];sys.path.insert(0,str(ROOT/'tools/melodic_weave'))
from texture_weave import validate
from reference_analysis import measure
FF=r'C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe'
s=json.loads((R/'texture.json').read_text());qa=validate(s);assert qa['passed'];x,sr=sf.read(R/'Renders/Long Line - Inner Detail B.wav');base,_=sf.read(R/'Media/01_v8_scaffold_excerpt.flac');inner,_=sf.read(R/'Media/06_Inner_texture.flac');assert len(x)==96*sr and sr==48000 and np.isfinite(x).all() and abs(x).max()<.99
cp=subprocess.run([FF,'-hide_banner','-i',str(R/'Renders/Long Line - Inner Detail B.wav'),'-af','loudnorm=I=-21:TP=-1:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True);loud=json.JSONDecoder().raw_decode(cp.stderr[cp.stderr.rfind('{'):])[0]
for p,out in [(R/'Renders/Long Line - Inner Detail B.wav',R/'Renders/Long Line - Inner Detail - 96s.mp3'),(R/'Media/06_Inner_texture.flac',R/'Renders/Inner arrangement - exposed.mp3')]:
 subprocess.run([FF,'-y','-loglevel','error','-i',str(p),'-c:a','libmp3lame','-b:a','256k',str(out)],check=True)
# Same source position for all diagnostic sections; normalize separately to equal RMS.
segments=[]
for y in [base[28*sr:40*sr],inner[28*sr:40*sr],x[28*sr:40*sr]]:
 y=y.copy();y*=.05/np.sqrt(np.mean(y*y));fade=np.linspace(0,1,int(.02*sr));y[:len(fade)]*=fade[:,None];y[-len(fade):]*=fade[::-1,None];segments.append(y)
sf.write(R/'Renders/Diagnostic - scaffold inner blend.wav',np.concatenate(segments),sr,subtype='PCM_24');subprocess.run([FF,'-y','-loglevel','error','-i',str(R/'Renders/Diagnostic - scaffold inner blend.wav'),'-c:a','libmp3lame','-b:a','256k',str(R/'Renders/Diagnostic - scaffold inner blend.mp3')],check=True)
# The central comparison is free of the demo's endpoint fades.
a=base[8*sr:88*sr];b=x[8*sr:88*sr];res=b-.92*a
qa.update({'duration_s':96,'source_excerpt_s':[140,236],'notes_in_demo':sum(e['voice']>=4 and e['end_s']>140 and e['start_s']<236 for e in s['events']),'old_source_events':len(s['scaffold']['events']),'mean_full_source_onsets_per_s':len(s['events'])/s['duration_s'],'mean_texture_onsets_per_active_s':qa['texture_events']/(s['duration_s']-11),'native_peak':float(abs(x).max()),'loudness':{k:v for k,v in loud.items()if k.startswith('input_')},'residual_to_scaffold_db':float(20*np.log10(np.sqrt(np.mean(res**2))/np.sqrt(np.mean(a**2)))),'old_new_waveform_correlation':float(np.corrcoef(a.ravel(),b.ravel())[0,1]),'render_sha256':hashlib.sha256((R/'Renders/Long Line - Inner Detail B.wav').read_bytes()).hexdigest(),'tests':{'melody_tool_total':22,'harmony_protocol':10,'texture_seeded_trials':100},'gemini_cumulative':98,'gemini_remaining':2,'review_status':'Construction and non-silent rendering verified. In-context superiority NOT established; paired Gemini reviews could not distinguish versions.'})
(R/'Audit/QA.json').write_text(json.dumps(qa,indent=2));print(json.dumps(qa,indent=2))
