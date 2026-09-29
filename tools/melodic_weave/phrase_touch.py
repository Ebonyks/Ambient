"""Repeat-specific phrase touch with bounded timing, duration and actual lane-gain curves."""
import argparse,copy,json,math,random
from pathlib import Path
from texture_weave import validate,write_midi
from continuous_field import performance_score
LENGTHS=(7,11,13,17)
def shape(score,seed=261005):
 s=copy.deepcopy(score);rng=random.Random(seed);log=[];gain={};mapping={}
 for voice in range(4,8):
  lane=[e for e in s['events'] if e['voice']==voice and e.get('role')!='upper_octave_companion'];points=[];last_db=0
  for cycle,start in enumerate(range(0,len(lane),LENGTHS[voice-4])):
   group=lane[start:start+LENGTHS[voice-4]];st=group[0]['start_s'];en=lane[start+len(group)]['start_s'] if start+len(group)<len(lane) else group[-1]['end_s'];crest=rng.uniform(.32,.72);peak=rng.uniform(-.65,.65);end=last_db*.6+rng.uniform(-.28,.28);timing=rng.uniform(-.005,.005);touch=rng.uniform(-2.2,2.2);length=rng.uniform(.95,1.05)
   points.extend([[st,10**(last_db/20)],[st+(en-st)*crest,10**(peak/20)],[en-.0001,10**(end/20)]])
   log.append({'voice':voice,'cycle':cycle,'start_s':st,'end_s':en,'crest_fraction':crest,'gain_db':[last_db,peak,end],'timing_s':timing,'touch':touch,'duration_ratio':length})
   for j,e in enumerate(group):
    old=e['start_s'];phase=(old-st)/max(.001,en-st);delta=timing*math.sin(math.pi*phase);new=round(old+delta,4)
    f=next(f for f in s['harmonic_fields'] if f['start_s']<=old<f['end_s']);new=max(f['start_s'],min(f['end_s']-.0001,new))
    dur=(e['end_s']-old)*length;e['start_s']=new;e['end_s']=round(new+dur,4);e['velocity']=max(10,min(40,round(e['velocity']+touch*math.sin(math.pi*phase)+.65*math.sin(j*1.71+cycle*.83))));e['performance_cycle']=cycle;mapping[(voice,old)]=(e['start_s'],e['end_s'],e['velocity'])
   last_db=end
  gain[str(voice)]=points
 for e in s['events']:
  if e.get('role')=='upper_octave_companion':
   st,en,v=mapping[(e['voice'],e['start_s'])];e.update(start_s=st,end_s=en,velocity=max(10,round(v*.55)))
 s['events'].sort(key=lambda e:(e['start_s'],e['voice']))
 for voice in range(4,8):
  last={}
  for e in (e for e in s['events'] if e['voice']==voice):
   if e['midi'] in last and last[e['midi']]['end_s']>=e['start_s']:last[e['midi']]['end_s']=round(e['start_s']-.001,4)
   last[e['midi']]=e
 s['version']='4.3-phrase-touch';s['phrase_touch']={'seed':seed,'cycles':log,'lane_gain_points':gain,'meaning':'Authored bounded performance variation, not a human performance claim. Gain automation is required for the FB-3300 parts.'};q=validate(s)
 if not q['passed']:raise ValueError(q)
 return s
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();s=shape(json.loads(a.source.read_text()));a.out.parent.mkdir(parents=True,exist_ok=True);a.out.with_suffix('.json').write_text(json.dumps(s,indent=2));write_midi(performance_score(s),a.out.with_suffix('.mid'));print(json.dumps(validate(s)))
