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
 assert (R/'Media/01_Nature_bed.flac').exists()

def calibrate():
 assert (R/'Audit/lanes_returned.txt').exists();base,s=sf.read(R/'Media/01_Nature_bed.flac');target=.10;mix=np.zeros_like(base);rows=[];frozen=json.loads((R/'Audit/inherited_gains.json').read_text())
 for i in range(4):
  p=R/'Renders'/f'Inner lane {i}.wav';x,sr=sf.read(p);assert sr==s and len(x)==len(base) and np.isfinite(x).all() and abs(x).max()<.99
  rms=np.sqrt(np.mean(x[4*s:-4*s]**2));assert rms>1e-6;gain=frozen['lane_gains'][i];x*=gain;mix+=x;sf.write(R/'Media'/f'0{i+2}_Inner_lane_{i}.flac',x,s,subtype='PCM_24');rows.append({'lane':i,'native_rms':float(rms),'native_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'gain_db':float(20*np.log10(gain)),'printed_rms':float(rms*gain)})
 mix*=frozen['sum_gain'];sf.write(R/'Media/06_Inner_texture.flac',mix,s,subtype='PCM_24')
 (R/'Audit/print_calibration.json').write_text(json.dumps({'lanes':rows,'texture_bus_rms_before_fader':float(np.sqrt(np.mean(mix[4*s:-4*s]**2))),'calibration':'Inherited v11 gains, no renormalization','note':'FB-3300 has no ordinary per-note velocity response; use envelopes, register and lane/bus gain. Tyrell velocity is enabled.'},indent=2))
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--calibrate',action='store_true');a=p.parse_args();calibrate() if a.calibrate else prepare()
