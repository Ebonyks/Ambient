"""Add intermittent upper octave companions while preserving the existing score."""
import argparse,copy,json
from pathlib import Path
from texture_weave import validate,write_midi
from continuous_field import performance_score

def add_upper_octaves(score):
 s=copy.deepcopy(score);added=[]
 for voice,period,offset,width in [(4,11.3,1.7,2.8),(6,13.7,6.1,3.1)]:
  lane=[e for e in score['events'] if e['voice']==voice]
  for i,e in enumerate(lane):
   if i%3 or (e['start_s']-offset)%period>=width:continue
   interval=24 if e['midi']+24<=90 else 12;m=e['midi']+interval
   if m<72 or m>90:continue
   if any(a['midi']==m and a['start_s']<e['end_s'] and e['start_s']<a['end_s'] for a in lane+added if a['voice']==voice):continue
   n=copy.deepcopy(e);n.update(midi=m,velocity=max(10,round(e['velocity']*.55)),role='upper_octave_companion',operation='intermittent_octave_extension',source_midi=e['midi'],octave_semitones=interval);added.append(n)
 s['events']=sorted(s['events']+added,key=lambda e:(e['start_s'],e['voice']));s['version']='4.2-upper-octaves';s['octave_extension']={'added_events':len(added),'voices':[4,6],'intervals_semitones':[12,24],'velocity_ratio':.55,'meaning':'Existing pitches doubled in upper octaves, not chromatic notes outside the active harmony. Authored intermittent windows, not an artist transcription.'}
 check=validate(s)
 if not check['passed']:raise ValueError(check)
 return s
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();s=add_upper_octaves(json.loads(a.source.read_text()));a.out.parent.mkdir(parents=True,exist_ok=True);a.out.with_suffix('.json').write_text(json.dumps(s,indent=2));write_midi(performance_score(s),a.out.with_suffix('.mid'));print(json.dumps(s['octave_extension']))
