"""Resolve close-register clashes in the optional inner texture, leaving its scaffold intact."""
import copy,json,argparse
from pathlib import Path
from texture_weave import BOUNDS,validate,write_midi

def overlaps(a,b,tail=0):return a['start_s']<b['end_s']+tail and b['start_s']<a['end_s']+tail

def clashes(score,tail=0):
 es=score['events'];out=[]
 for i,a in enumerate(es):
  for b in es[i+1:]:
   if b['start_s']>=a['end_s']+tail:break
   if a['voice']<4 and b['voice']<4:continue
   if 0<abs(a['midi']-b['midi'])<=2 and overlaps(a,b,tail):out.append((a['start_s'],b['start_s'],a['midi'],b['midi']))
 return out

def revise(score,tail=1.0):
 if not 0<=tail<=3:raise ValueError('Tail guard must be 0..3 seconds')
 s=copy.deepcopy(score);base=copy.deepcopy(score['scaffold']['events']);accepted=[];history={v:[] for v in range(4,8)};log=[]
 for e in sorted((e for e in s['events']if e['voice']>=4),key=lambda e:(e['start_s'],e['voice'])):
  f=next(f for f in s['harmonic_fields']if f['start_s']<=e['start_s']<f['end_s']);pcs={n['midi']%12 for n in f['notes']};lo,hi=BOUNDS[e['voice']-4]
  sounding=[a for a in base+accepted if overlaps(a,e,tail)];hist=history[e['voice']]
  forbidden=set(hist[-1:])
  if len(hist)>=2 and abs(hist[-1]-hist[-2])==1:forbidden.add(hist[-2])
  pool=[m for m in range(lo,hi+1)if m%12 in pcs and m not in forbidden and all(not 0<abs(m-a['midi'])<=2 for a in sounding)]
  if not pool:
   log.append({'start_s':e['start_s'],'voice':e['voice'],'from':e['midi'],'to':None,'reason':'Leave space rather than force a close-register clash'});continue
  m=min(pool,key=lambda m:(abs(m-e['midi']),sum(a['midi']==m for a in sounding),m))
  if m!=e['midi']:log.append({'start_s':e['start_s'],'voice':e['voice'],'from':e['midi'],'to':m,'reason':'Respect actual sounding voices including conservative release guard'})
  e['midi']=m;accepted.append(e);history[e['voice']]=(hist+[m])[-2:]
 for v in range(4,8):
  last={}
  for e in (e for e in accepted if e['voice']==v):
   if e['midi']in last and last[e['midi']]['end_s']>e['start_s']:last[e['midi']]['end_s']=round(e['start_s']-.01,4)
   last[e['midi']]=e
 s['events']=sorted(base+accepted,key=lambda e:(e['start_s'],e['voice']));s['version']='2.1-context-blend';s['blend_revision']={'tail_guard_s':tail,'edits':log,'scope':'Avoid added 1-2 semitone proximity in actual register; scaffold tensions and wider intervals remain unchanged. Guard is an authored approximation, not a measured plugin release.'};s['cycles_status']='Original proposal cells only; events and blend_revision are authoritative after contextual edits.'
 check=validate(s)
 if not check['passed']:raise ValueError(check)
 assert not clashes(s,tail)
 return s
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('score',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();s=revise(json.loads(a.score.read_text()));a.out.parent.mkdir(parents=True,exist_ok=True);a.out.with_suffix('.json').write_text(json.dumps(s,indent=2));write_midi(s,a.out.with_suffix('.mid'));print(json.dumps(validate(s)))
