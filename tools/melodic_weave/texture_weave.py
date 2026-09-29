"""Dense, low-salience inner patterns beneath an unchanged harmonic scaffold.
Original construction rules, not transcription or a learned artist model.
"""
import argparse, copy, json, math, random, struct
from pathlib import Path
from melody_tool import validate as validate_scaffold, vlq

CELLS=((0,2,1,3,2),(0,3,1,2,4,1,3),(2,0,3,1,4,2,1,3,0),(0,2,4,1,3,2,1))
BOUNDS=((50,65),(57,72),(62,77),(55,70))
RATES=(1.73,2.11,2.57,1.91)

def _field(h,t):
    return next(s for s in h['states'] if s['start_s']<=t<s['end_s'])

def generate(scaffold,harmony,seed=260928,density=1.0,level=1.0):
    if not validate_scaffold(scaffold)['passed']: raise ValueError('Invalid scaffold')
    if not math.isfinite(density) or not .25<=density<=1.5: raise ValueError('Density must be .25..1.5')
    if not math.isfinite(level) or not .25<=level<=1.5: raise ValueError('Level must be .25..1.5')
    d=scaffold['duration_s'];cursor=0
    for f in harmony['states']:
        if f['start_s']!=cursor or f['end_s']<=cursor or not f['notes']: raise ValueError('Invalid fields')
        cursor=f['end_s']
    if cursor!=d or harmony['duration_s']!=d: raise ValueError('Duration mismatch')
    rng=random.Random(seed);micro=[];cycles=[]
    for lane in range(4):
        t=7+lane*.137;step=0;cycle=0;previous=[];cell=list(CELLS[lane]);previous_field=None
        while t<d-4:
            f=_field(harmony,t);pcs={n['midi']%12 for n in f['notes']};lo,hi=BOUNDS[lane]
            pool=[m for m in range(lo,hi+1) if m%12 in pcs]
            if len(pool)<3:raise ValueError('Field/register requires at least three realizable pitches')
            if step%len(cell)==0:
                # Persist most of a broken-chord contour; mutate only one cell position.
                if cycle and cycle%3==0:
                    pos=(cycle//3+lane)%len(cell);cell[pos]=(cell[pos]+1)%len(pool)
                cycles.append({'voice':lane+4,'start_s':round(t,4),'cycle':cycle,'field_index':f['index'],'cell':list(cell)})
                cycle+=1
            target=pool[cell[step%len(cell)]%len(pool)]
            # A change of field enters near the previous pitch, never resets every strand.
            if previous and previous_field!=f['index']:
                target=min(pool,key=lambda m:(abs(m-previous[-1]),m))
            forbidden={previous[-1]} if previous else set()
            if len(previous)>=2 and abs(previous[-1]-previous[-2])==1:forbidden.add(previous[-2])
            candidates=[m for m in pool if m not in forbidden]
            m=min(candidates,key=lambda m:(abs(m-target),m))
            # Independent smoothly breathing clocks; no synchronized accent or bar reset.
            breath=1+.12*math.sin(t/(9+lane*2)+lane*.9)
            rate=RATES[lane]*density*breath
            dt=(1/rate)*rng.uniform(.94,1.06)
            dur=min(1.15,max(.38,dt*1.65))
            # More events do not automatically increase energy; rendering still needs gain matching.
            vel=round((27+4*math.sin(t/(11+lane)+lane)+rng.uniform(-2,2))*level/math.sqrt(density))
            vel=max(12,min(43,vel))
            micro.append({'voice':lane+4,'midi':m,'cents':0.0,'start_s':round(t,4),'end_s':round(min(d-.8,t+dur),4),'velocity':vel,'role':'inner_texture','field_index':f['index'],'cycle':cycle-1,'operation':'persistent_broken_chord'})
            previous=(previous+[m])[-2:];previous_field=f['index'];t+=dt;step+=1
    # MIDI note ownership: repeated same-key notes on one lane cannot share note-off state.
    for lane in range(4,8):
        last={}
        for e in sorted((e for e in micro if e['voice']==lane),key=lambda e:e['start_s']):
            a=last.get(e['midi'])
            if a and a['end_s']>=e['start_s']:a['end_s']=round(e['start_s']-.01,4)
            last[e['midi']]=e
    result={'version':'2.0-texture','seed':seed,'duration_s':d,'density':density,'level':level,'max_key_polyphony':18,'scaffold':copy.deepcopy(scaffold),'harmonic_fields':copy.deepcopy(harmony['states']),'events':sorted(copy.deepcopy(scaffold['events'])+micro,key=lambda e:(e['start_s'],e['voice'])),'cycles':cycles,'render_contract':{'micro_bus_start_db':-12,'pitch_modulation':False,'attack_s':[.12,.24],'release_s':[.5,1.4],'note':'Subtlety is an audio acceptance criterion. Velocity is not a calibrated loudness scale; inspect solo and in-context renders.'},'meaning':'Designed density values, not inferred played-note rates. Existing core harmony unchanged; new notes use each local field. Released tones may carry across its boundary.'}
    check=validate(result)
    if not check['passed']:raise ValueError(check)
    return result

def validate(score):
    errors=[];es=score['events'];d=score['duration_s'];boundaries=[]
    if not math.isfinite(d) or d<=0:errors.append('Invalid duration')
    if [e for e in es if e['voice']<4]!=score['scaffold']['events']:errors.append('Scaffold altered')
    for i,e in enumerate(es):
        if not all(math.isfinite(e[k]) for k in ('start_s','end_s','cents')) or not 0<=e['start_s']<e['end_s']<=d:errors.append(f'Invalid time {i}')
        if not isinstance(e['midi'],int) or not 28<=e['midi']<=90 or not 1<=e['velocity']<=127 or not 0<=e['voice']<8:errors.append(f'Invalid MIDI {i}')
        if abs(e['cents'])>50:errors.append(f'Invalid tuning {i}')
        if e['voice']>=4:
            f=next((f for f in score['harmonic_fields']if f['start_s']<=e['start_s']<f['end_s']),None)
            if not f or e['midi']%12 not in {n['midi']%12 for n in f['notes']}:errors.append(f'Outside local field {i}')
            if e['cents']!=0:errors.append('Texture pitch wobble')
        boundaries.extend([(e['start_s'],1),(e['end_s'],-1)])
    count=peak=0
    for _,v in sorted(boundaries):count+=v;peak=max(count,peak)
    if peak>18:errors.append('Key polyphony exceeds 18')
    for voice in range(8):
        lane=sorted((e for e in es if e['voice']==voice),key=lambda e:e['start_s']);last={};active=[]
        for e in lane:
            if e['midi'] in last and last[e['midi']]['end_s']>e['start_s']:errors.append('Same-key note-off collision')
            if any(a['end_s']>e['start_s'] and a['cents']!=e['cents'] for a in active):errors.append('Pitch bend affects held note')
            active=[a for a in active if a['end_s']>e['start_s']]+[e];last[e['midi']]=e
        if voice>=4:
            for a,b,c in zip(lane,lane[1:],lane[2:]):
                if a['midi']==c['midi'] and abs(a['midi']-b['midi'])==1:errors.append('Semitone rocking')
    return {'passed':not errors,'errors':errors,'max_key_polyphony':peak,'source_events':len(es),'texture_events':sum(e['voice']>=4 for e in es),'meaning':'Key overlap only; acoustic release tails are additional. No claim of perceived simplicity.'}

def write_midi(score,path):
    if not validate(score)['passed']:raise ValueError('Invalid texture score')
    tracks=[]
    for voice in range(8):
        label=('Scaffold ' if voice<4 else 'Inner texture ')+str(voice)
        out=[(0,0,b'\xff\x03'+vlq(len(label))+label.encode()),(0,0,b'\xff\x51\x03\x0f\x42\x40')]
        for cc,val in [(101,0),(100,0),(6,2),(38,0),(101,127),(100,127)]:out.append((0,0,bytes([176+voice,cc,val])))
        for e in score['events']:
            if e['voice']!=voice:continue
            st=round(e['start_s']*480);en=round(e['end_s']*480);bend=round(8192+e['cents']/200*8192)
            out.extend([(st,2,bytes([224+voice,bend&127,bend>>7])),(st,3,bytes([144+voice,e['midi'],e['velocity']])),(en,1,bytes([128+voice,e['midi'],0]))])
        data=bytearray();last=0
        for t,_,msg in sorted(out,key=lambda x:(x[0],x[1])):data.extend(vlq(t-last)+msg);last=t
        data.extend(vlq(max(0,round(score['duration_s']*480)-last))+b'\xff\x2f\x00');tracks.append(b'MTrk'+struct.pack('>I',len(data))+data)
    Path(path).write_bytes(b'MThd'+struct.pack('>IHHH',6,1,len(tracks),480)+b''.join(tracks))

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--scaffold',type=Path,required=True);p.add_argument('--harmony',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--seed',type=int,default=260928);p.add_argument('--density',type=float,default=1);p.add_argument('--level',type=float,default=1);a=p.parse_args()
    score=generate(json.loads(a.scaffold.read_text(encoding='utf-8-sig')),json.loads(a.harmony.read_text(encoding='utf-8-sig')),a.seed,a.density,a.level);a.out.parent.mkdir(parents=True,exist_ok=True);a.out.with_suffix('.json').write_text(json.dumps(score,indent=2),encoding='utf8');write_midi(score,a.out.with_suffix('.mid'));print(json.dumps(validate(score)))
if __name__=='__main__':main()
