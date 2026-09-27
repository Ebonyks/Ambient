"""Continuous distributed voicing: fast articulation, slowly moving pitch weights."""
import argparse,copy,json,math,random
from pathlib import Path
from texture_weave import validate,write_midi
# Authored registral voicings of Long Line's existing seven fields.
VOICINGS=((50,57,62,66,69,76),(47,54,57,62,66,69,74),(43,54,59,62,66,71,74),(48,55,59,64,67,71,76),(40,55,59,62,67,71,74),(43,53,58,62,65,70,74),(50,57,62,66,69,74))
RATES=(3.11,3.37,3.73,3.97)
def generate(scaffold,harmony,seed=261001):
 rng=random.Random(seed);d=scaffold['duration_s'];fields=copy.deepcopy(harmony['states']);events=[];history=[[] for _ in range(4)];nexts=[7+i*.069 for i in range(4)]
 # Permit only explicitly documented neighboring-field transitions.
 windows=[]
 for i,f in enumerate(fields):
  start=f['start_s'];end=f['end_s'];transition=min(start+24,end) if i else start
  if i:
   pcs=sorted({n['midi']%12 for n in fields[i-1]['notes']+f['notes']})
   windows.append({'start_s':start,'end_s':transition,'notes':[{'midi':p+48} for p in pcs],'index':i,'role':'24-second neighboring-field transition'})
  windows.append(dict(f,start_s=transition))
 while min(nexts)<d-4:
  lane=min(range(4),key=nexts.__getitem__);t=nexts[lane];idx=next(i for i,f in enumerate(fields) if f['start_s']<=t<f['end_s']);f=fields[idx]
  alpha=min(1,max(0,(t-f['start_s'])/24)) if idx else 1;alpha=alpha*alpha*(3-2*alpha)
  old=set(VOICINGS[max(0,idx-1)]);new=set(VOICINGS[idx]);pool=sorted(old|new) if alpha<1 else sorted(new)
  # A slow registral arc carries direction; no prominent top-line or beat accents.
  center=61+2.8*math.sin(2*math.pi*t/150-.7)+(.7 if lane%2 else -.7)
  active=[e for e in events[-120:] if e['end_s']+.45>t]
  counts={m:sum(n==m for n in history[lane][-24:]) for m in pool}
  choices=[]
  for m in pool:
   if m<50:continue
   if history[lane] and m==history[lane][-1]:continue
   if len(history[lane])>1 and m==history[lane][-2] and abs(m-history[lane][-1])==1:continue
   if any(0<abs(m-e['midi'])<=2 for e in active):continue
   w=(1 if m in old and m in new else alpha if m in new else 1-alpha)
   w*=math.exp(-((m-center)/11)**2)/(1+counts[m]*.55)
   if w>0:choices.append((m,w))
  if choices:
   # Weighted fair distribution avoids privileging one pitch; seeded choice keeps reproducibility.
   m=rng.choices([m for m,w in choices],weights=[w for m,w in choices])[0]
   events.append({'voice':lane+4,'midi':m,'cents':0.0,'start_s':round(t,4),'end_s':round(min(d-.8,t+.48),4),'velocity':25,'role':'continuous_field','field_index':idx,'operation':'slow_weight_morph'})
   history[lane].append(m)
  nexts[lane]+=1/(RATES[lane]*(1+.035*math.sin(t/31+lane)))*rng.uniform(.985,1.015)
 for v in range(4,8):
  last={}
  for e in (e for e in events if e['voice']==v):
   if e['midi'] in last and last[e['midi']]['end_s']>=e['start_s']:last[e['midi']]['end_s']=round(e['start_s']-.01,4)
   last[e['midi']]=e
 s={'version':'3.0-continuous-field','duration_s':d,'seed':seed,'scaffold':copy.deepcopy(scaffold),'harmonic_fields':windows,'events':sorted(copy.deepcopy(scaffold['events'])+events,key=lambda e:(e['start_s'],e['voice'])),'render_contract':{'scaffold_moving_voices':'reference only; excluded from audition audio','foreground':'four equally weighted continuous strands','velocity':25,'transition_seconds':24,'register_arc_seconds':150,'pitch_modulation':False},'meaning':'Authored distributed voicing, not an artist transcription. No perceptual equivalence claim.'}
 check=validate(s)
 if not check['passed']:raise ValueError(check)
 return s
def performance_score(score):
 s=copy.deepcopy(score);s['scaffold']['events']=[];s['events']=[e for e in s['events'] if e['voice']>=4];return s

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();root=Path(__file__).resolve().parents[2];s=generate(json.loads((root/'productions/long-line-v8/weave.json').read_text()),json.loads((root/'productions/long-line-v6/harmony.json').read_text()));a.out.parent.mkdir(parents=True,exist_ok=True);a.out.with_suffix('.json').write_text(json.dumps(s,indent=2));write_midi(performance_score(s),a.out.with_suffix('.mid'));print(json.dumps(validate(s)))
