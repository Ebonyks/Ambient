"""Derive original demo media from the published score and native lane prints.
Run after native prints exist; no reference-artist samples are used.
"""
from pathlib import Path
import json,hashlib,soundfile as sf,numpy as np
R=Path(__file__).resolve().parents[1]
def prepare():
 score=json.loads((R/'texture.json').read_text());start,end=140,236
 notes=['return {']
 for e in score['events']:
  if e['voice']>=4 and e['end_s']>start and e['start_s']<end:notes.append('{%d,%.4f,%.4f,%d,%d},'%(e['voice']-4,max(0,e['start_s']-start),min(96,e['end_s']-start),e['midi'],e['velocity']))
 (R/'Scripts/demo_notes.lua').write_text('\n'.join(notes+['}']))
 p=R.parent/'long-line-v8/Renders/Long Line - Tonal Revision F.wav'
 if p.exists():
  x,s=sf.read(p,start=start*48000,stop=end*48000);sf.write(R/'Media/01_v8_scaffold_excerpt.flac',x,s,subtype='PCM_24')
 elif not (R/'Media/01_v8_scaffold_excerpt.flac').exists():raise FileNotFoundError('Render v8 F or retain the supplied lossless excerpt')
def calibrate():
 assert (R/'Audit/lanes_returned.txt').exists();base,s=sf.read(R/'Media/01_v8_scaffold_excerpt.flac');target=np.sqrt(np.mean(base[4*s:-4*s]**2));mix=np.zeros_like(base);rows=[]
 for i in range(4):
  p=R/'Renders'/f'Inner lane {i}.wav';x,sr=sf.read(p);assert sr==s and len(x)==len(base) and np.isfinite(x).all() and abs(x).max()<.99
  rms=np.sqrt(np.mean(x[4*s:-4*s]**2));assert rms>1e-6;x*=.012/rms;mix+=x;sf.write(R/'Media'/f'0{i+2}_Inner_lane_{i}.flac',x,s,subtype='PCM_24');rows.append({'lane':i,'native_rms':float(rms),'native_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'gain_db':float(20*np.log10(.012/rms)),'normalized_rms':.012})
 mix*=target/np.sqrt(np.mean(mix[4*s:-4*s]**2));sf.write(R/'Media/06_Inner_texture.flac',mix,s,subtype='PCM_24')
 (R/'Audit/print_calibration.json').write_text(json.dumps({'lanes':rows,'texture_bus_rms_before_fader':float(target),'proposed_fader_db':-12.0412,'note':'FB-3300 has no ordinary per-note velocity response; use envelopes, register and lane/bus gain. Tyrell velocity is enabled.'},indent=2))
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--calibrate',action='store_true');a=p.parse_args();calibrate() if a.calibrate else prepare()
