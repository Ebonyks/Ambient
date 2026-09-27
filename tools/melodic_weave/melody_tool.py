"""Original motivic/voicing generator. Seconds, not a beat grid; no style classifier."""
import argparse, json, math, random, struct
from pathlib import Path

OPERATIONS=('statement','fragment_continue','interleave_answer','register_exchange','contract','turn_and_extend','return_changed')
CELLS=((69,71,74,71,69,64,62),(71,74,71,69,71,76),(74,71,76,69,74,64,71),(69,64,71,62,74,69),(74,71,69,71),(71,69,64,66,69,76,74),(69,71,74,76,71,64,62))

def generate(harmony,seed=260927,change_range=(1.8,3.3),cells=None,friction_pc=11):
    cells=CELLS if cells is None else cells
    if not cells or any(not cell or any(not isinstance(m,int) or isinstance(m,bool) or not 28<=m<=90 for m in cell) for cell in cells): raise ValueError("Cells must be nonempty MIDI pitch lists in 28..90")
    if friction_pc is not None and (not isinstance(friction_pc,int) or not 0<=friction_pc<=11): raise ValueError("Invalid friction pitch class")
    if len(change_range)!=2 or not all(math.isfinite(x) and x>0 for x in change_range) or change_range[1]<change_range[0]: raise ValueError('Invalid change interval')
    duration=harmony['duration_s']; states=harmony['states']
    if not math.isfinite(duration) or duration<30 or not states: raise ValueError('Finite duration >=30 and states required')
    cursor=0
    for s in states:
        if s['start_s']!=cursor or s['end_s']<=cursor or not s['notes']: raise ValueError('Contiguous nonempty harmonic fields required')
        cursor=s['end_s']
    if cursor!=duration: raise ValueError('Harmony duration mismatch')
    rng=random.Random(seed); events=[]; active={}; gestures=[]; ticks=[]; phrase=0; step=0; next_phrase=24.; t=7.; k=0
    def field(at): return next(s for s in states if s['start_s']<=at<s['end_s'])
    def add(voice,m,at,end,operation,phrase_id):
        e={'voice':voice,'midi':m,'cents':round(((m*17)%9-4)*.65,2),'start_s':round(at,3),'end_s':round(end,3),'velocity':52 if voice==2 else 44,'operation':operation,'phrase':phrase_id}
        events.append(e);return e
    # Anchors retain their slow clock; three moving strands share a faster clock.
    for s in states:
        n=min(s['notes'],key=lambda n:n['midi'])
        if events and events[-1]['midi']==n['midi']: events[-1]['end_s']=s['end_s']
        else: add(3,n['midi'],s['start_s'],s['end_s'],'anchor',-1)
    pcs={n['midi']%12 for n in states[0]['notes']}
    initial=tuple(min([m for m in range(lo,hi+1) if m%12 in pcs],key=lambda m:abs(m-target)) for lo,hi,target in [(50,62,54),(59,71,64),(62,81,cells[0][0])])
    for voice,m in enumerate(initial): active[voice]=add(voice,m,7+voice*.43,duration-4,'initial',0)
    t=9.8
    while t<duration-11:
        if t>=next_phrase:
            phrase+=1;step=0;next_phrase=t+rng.uniform(15,25)
        op=OPERATIONS[phrase%len(OPERATIONS)]; cell=cells[phrase%len(cells)]
        voice=(2,0,2,1,0,2,1)[k%7]; s=field(t)
        pcs={n['midi']%12 for n in s['notes']}
        # B is the original motif's independently declared persistent friction.
        if voice==2 and friction_pc is not None: pcs.add(friction_pc)
        bounds=((50,62),(59,71),(62,81))[voice]
        pool=[m for m in range(bounds[0],bounds[1]+1) if m%12 in pcs]
        previous=active[voice]['midi']
        if voice==2:
            target=cell[step%len(cell)];step+=1
            if op=='register_exchange' and step%3==1:target-=12
        else:
            # Contrary response to the preceding foreground move, with own register.
            direction=-1 if (k//3+voice)%2 else 1
            target=previous+direction*(2 if k%3 else 5)
        m=min(pool,key=lambda m:(abs(m-target),abs(m-previous),m))
        if m!=previous:
            active[voice]['end_s']=round(t+.55,3)
            active[voice]=add(voice,m,t,duration-4,op,phrase)
            ticks.append(round(t,3))
        # Other strands continue through every local change and harmonic boundary.
        gestures.append({'time_s':round(t,3),'voice':voice,'target_midi':target,'realized_midi':m,'field_index':s['index'],'operation':op,'phrase':phrase,'retained':m==previous})
        t+=rng.uniform(*change_range);k+=1
    # End by completing the original descending fragment, staggered, not a global gate.
    for voice,m,at in [(2,64,duration-10),(1,62,duration-7),(2,62,duration-5)]:
        if active[voice]['midi']!=m:
            active[voice]['end_s']=at+.55; active[voice]=add(voice,m,at,duration-.8,'completion',phrase+1)
    for voice,e in active.items():e['end_s']=round(duration-(.8+voice*.25),3)
    return {'version':'1.0','seed':seed,'duration_s':duration,'change_interval_proposal_s':list(change_range),'cells':[list(c) for c in cells],'friction_pitch_class':friction_pc,'pitch_policy':'Local harmony palette; explicit upper friction pitch class; pre-existing voices may carry across fields. No automatic scale correction.','events':sorted(events,key=lambda e:(e['start_s'],e['voice'])),'gestures':gestures,'meaning':'Original compositional proposal, not transcribed or trained artist model'}

def validate(score):
    errors=[];events=score['events'];d=score['duration_s'];boundaries=[]
    for i,e in enumerate(events):
        if not all(math.isfinite(e[k]) for k in ('start_s','end_s','cents')) or not 0<=e['start_s']<e['end_s']<=d:errors.append(f'Invalid timing {i}')
        if not isinstance(e['midi'],int) or not 28<=e['midi']<=90 or abs(e['cents'])>50:errors.append(f'Invalid pitch {i}')
        boundaries.extend([(e['start_s'],1),(e['end_s'],-1)])
    count=peak=0
    for _,delta in sorted(boundaries):count+=delta;peak=max(peak,count)
    if peak>6:errors.append('More than six source events overlap')
    for v in range(4):
        es=sorted([e for e in events if e['voice']==v],key=lambda e:e['start_s'])
        for a,b in zip(es,es[1:]):
            if a['midi']==b['midi'] and b['start_s']<=a['end_s']:errors.append('Needless same-pitch reattack')
    return {'passed':not errors,'errors':errors,'max_source_polyphony':peak,'meaning':'Construction validation only; tails can increase acoustic density'}

def vlq(n):
    b=[n&127];n>>=7
    while n:b.insert(0,(n&127)|128);n>>=7
    return bytes(b)

def write_midi(score,path):
    if not validate(score)['passed']: raise ValueError('Refusing invalid score')
    # Individual channels for overlapping notes: pitch bends cannot retune held notes.
    changes=[];free=[c for c in range(16) if c!=9];assigned={};out=[(0,0,b'\xff\x51\x03\x0f\x42\x40')]
    for c in free:
        for cc,val in [(101,0),(100,0),(6,2),(38,0),(101,127),(100,127)]:out.append((0,0,bytes([176+c,cc,val])))
    for i,e in enumerate(score['events']):changes.extend([(round(e['start_s']*480),1,i),(round(e['end_s']*480),0,i)])
    for tick,kind,i in sorted(changes):
        e=score['events'][i]
        if kind:
            c=free.pop(0);assigned[i]=c;b=round(8192+e['cents']/200*8192)
            out.extend([(tick,2,bytes([224+c,b&127,b>>7])),(tick,3,bytes([144+c,e['midi'],e['velocity']]))])
        else:
            c=assigned.pop(i);free.append(c);out.append((tick,1,bytes([128+c,e['midi'],0])))
    track=bytearray();last=0
    for tick,_,msg in sorted(out,key=lambda x:(x[0],x[1])):track.extend(vlq(tick-last)+msg);last=tick
    track.extend(b'\0\xff\x2f\0');Path(path).write_bytes(b'MThd'+struct.pack('>IHHH',6,0,1,480)+b'MTrk'+struct.pack('>I',len(track))+track)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--harmony',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--seed',type=int,default=260927);p.add_argument('--change-min',type=float,default=1.8);p.add_argument('--change-max',type=float,default=3.3);p.add_argument('--cells',type=Path,help='JSON list of original MIDI-pitch cells');p.add_argument('--friction-pc',type=int,default=11,help='Upper friction pitch class; -1 disables');a=p.parse_args()
    score=generate(json.loads(a.harmony.read_text(encoding='utf-8-sig')),a.seed,(a.change_min,a.change_max),json.loads(a.cells.read_text(encoding='utf-8-sig')) if a.cells else None,None if a.friction_pc==-1 else a.friction_pc);result=validate(score)
    if not result['passed']:raise ValueError(result)
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.with_suffix('.json').write_text(json.dumps(score,indent=2),encoding='utf8');write_midi(score,a.out.with_suffix('.mid'));print(json.dumps(result))
if __name__=='__main__':main()
