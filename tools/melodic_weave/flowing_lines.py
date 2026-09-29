"""Four differentiated continuous lines and an authored changing tonal itinerary."""
import argparse,copy,json,math,random
from pathlib import Path
from texture_weave import validate,write_midi
from continuous_field import performance_score
RATES=(12.44,13.48,14.92,15.88)
BOUNDS=((48,62),(62,76),(55,69),(67,81))
CELLS=((0,2,1,3,2,4,1),(4,2,3,1,2,0,3,2,1,4,2),(0,3,1,4,2,0,2,4,1,3,2,1,4),(4,1,3,0,2,4,2,1,3,4,0,2,3,1,4,2,0))
CHORDS={'Dadd9':(2,6,9,4),'Bm7':(11,2,6,9),'Gmaj7':(7,11,2,6),'Em9':(4,7,11,2,6),'Cmaj7':(0,4,7,11),'Am9':(9,0,4,7,11),'D6':(2,6,9,11),'Em7':(4,7,11,2),'Gm7':(7,10,2,5),'Bbmaj7':(10,2,5,9),'Dsus':(2,7,9,0),'Dmaj7':(2,6,9,1)}
PLAN=('Dadd9','Bm7','Gmaj7','D6','Em9','Bm7','Gmaj7','Cmaj7','Am9','D6','Gmaj7','Em9','Cmaj7','Am9','D6','Em9','Bm7','Cmaj7','Em7','Am9','Gm7','Bbmaj7','Gm7','Dsus','Dadd9','Bm7','Dmaj7','Dadd9')
def generate(scaffold,seed=261002,harmonic_period_s=12):
 rng=random.Random(seed);d=scaffold['duration_s'];assert d==336;fields=[]
 if not math.isfinite(harmonic_period_s) or not 3<=harmonic_period_s<=12:raise ValueError('Harmonic period must be 3..12 seconds')
 period=harmonic_period_s;scale=period/12;plan=list(PLAN)
 while len(plan)<math.ceil(d/period):
  for name in PLAN:
   if name!=plan[-1]:plan.append(name)
 plan=plan[:math.ceil(d/period)]
 for i,name in enumerate(plan):
  start=i*period;pcs=set(CHORDS[name]);old=set(CHORDS[plan[max(0,i-1)]])
  if i:fields.append({'index':i,'start_s':start,'end_s':min(d,start+4.8*scale),'notes':[{'midi':48+p} for p in sorted(pcs|old)],'title':plan[i-1]+' -> '+name})
  fields.append({'index':i,'start_s':start+(4.8*scale if i else 0),'end_s':min(d,start+period),'notes':[{'midi':48+p} for p in sorted(pcs)],'title':name})
 es=[]
 for lane in range(4):
  t=7+lane*.01725;step=0;hist=[];cell=list(CELLS[lane]);phrase=-1
  while t<d-4:
   fi=max(0,min(len(plan)-1,int((t-(0,.9,2.1,3.6)[lane]*scale)/period)));pcs=set(CHORDS[plan[fi]]);lo,hi=BOUNDS[lane];pool=[m for m in range(lo,hi+1) if m%12 in pcs]
   ph=int(t/(8.3+lane*1.7))
   if ph!=phrase:
    if phrase>=0:pos=(ph*3+lane)%len(cell);cell[pos]=(cell[pos]+1)%5
    phrase=ph
   # Separate contour grammar, range, speed, phrase length and inflection for every strand.
   index=cell[step%len(cell)]*(len(pool)-1)/4
   shift=.65*math.sin(t/(17+lane*4)+lane*1.4)
   target=pool[max(0,min(len(pool)-1,round(index+shift)))];forbidden=set(hist[-1:])
   if len(hist)>=2 and abs(hist[-1]-hist[-2])==1:forbidden.add(hist[-2])
   m=min((m for m in pool if m not in forbidden),key=lambda m:(abs(m-target),m))
   dt=1/(RATES[lane]*(1+.035*math.sin(t/31+lane)))*rng.uniform(.985,1.015)
   vel=round(25+3*math.sin(t/(9+lane*3)+lane)+1.5*math.sin(step*.37+lane));vel=max(20,min(30,vel))
   es.append({'voice':lane+4,'midi':m,'cents':0.0,'start_s':round(t,4),'end_s':round(t+dt*1.35,4),'velocity':vel,'role':'continuous_differentiated_line','field_index':fi,'operation':'persistent_contour_with_local_mutation'})
   hist=(hist+[m])[-2:];t+=dt;step+=1
 for lane in range(4,8):
  last={}
  for e in (e for e in es if e['voice']==lane):
   if e['midi'] in last and last[e['midi']]['end_s']>=e['start_s']:last[e['midi']]['end_s']=round(e['start_s']-.001,4)
   last[e['midi']]=e
 s={'version':'4.0-differentiated-flow','seed':seed,'duration_s':d,'scaffold':copy.deepcopy(scaffold),'harmonic_fields':fields,'events':sorted(copy.deepcopy(scaffold['events'])+es,key=lambda e:(e['start_s'],e['voice'])),'tonal_plan':[{'start_s':i*period,'name':n,'pitch_classes':CHORDS[n]} for i,n in enumerate(plan)],'render_contract':{'moving_scaffold':'reference only, excluded','rates':RATES,'rate_multiplier_vs_v10':4,'registers':BOUNDS,'cells':CELLS,'harmonic_period_s':period,'lane_harmonic_delays_s':[x*scale for x in (0,.9,2.1,3.6)],'pitch_modulation':False},'meaning':'Original authored lines informed by reference listening, not a Melnyk transcription or measured played-note-rate claim.'}
 q=validate(s)
 if not q['passed']:raise ValueError(q)
 return s
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--harmonic-period',type=float,default=12);a=p.parse_args();root=Path(__file__).resolve().parents[2];s=generate(json.loads((root/'productions/long-line-v8/weave.json').read_text()),harmonic_period_s=a.harmonic_period);a.out.parent.mkdir(parents=True,exist_ok=True);a.out.with_suffix('.json').write_text(json.dumps(s,indent=2));write_midi(performance_score(s),a.out.with_suffix('.mid'));print(json.dumps(validate(s)))
