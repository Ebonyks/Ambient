"""Generate/validate original harmonic sketches against a bounded reference protocol.
Standard library only. This is a compositional constraint engine, not a style classifier.
"""
import argparse, json, math, random, struct
from pathlib import Path

HERE=Path(__file__).resolve().parent
def read_protocol():
    return json.loads((HERE/'protocol.json').read_text(encoding='utf8'))

def voicing(family, root, rng):
    intervals=rng.choice(family['voicings_semitones'])
    return [root+i for i in intervals]

def generate(protocol, profile, seed, duration):
    if not math.isfinite(duration) or not 30<=duration<=3600:
        raise ValueError('Duration must be 30–3600 seconds.')
    cfg=protocol['profiles'][profile];policy=protocol['generation_policy'];rng=random.Random(seed)
    families=protocol['families'];states=[];t=0.;previous=None
    tuning={};i=0
    while t<duration-.001:
        hold=rng.uniform(*cfg['state_duration_s']);end=min(duration,t+hold)
        if duration-end<8:end=duration
        transition='initial';chosen=None
        if previous and rng.random()<policy['probability_retain_pitch_object']:
            chosen=(previous['family'],previous['anchor_midi'],[n['midi'] for n in previous['notes']]);transition='retain_pitch_object'
        elif previous and rng.random()<policy['probability_parallel_semitone_given_not_retained'] and profile!='low_beating_field':
            step=rng.choice([-1,1]);root=previous['anchor_midi']+step
            pitches=[n['midi']+step for n in previous['notes']]
            if min(pitches)>=28 and max(pitches)<=90:
                chosen=(previous['family'],root,pitches);transition='parallel_semitone_displacement'
        if chosen is None:
            candidates=[]
            for _ in range(160):
                fid=rng.choice(cfg['families']);family=families[fid]
                root=rng.randint(*cfg['anchor_midi_range']);pitches=voicing(family,root,rng)
                if max(pitches)>90:continue
                common=set(pitches)&set(n['midi'] for n in previous['notes']) if previous else set()
                if previous and not common:continue
                candidates.append((fid,root,pitches))
            if candidates:
                chosen=rng.choice(candidates);transition='common_tone_revoicing' if previous else 'initial'
            elif previous:
                chosen=(previous['family'],previous['anchor_midi'],[n['midi'] for n in previous['notes']]);transition='retain_pitch_object'
            else:raise RuntimeError('No initial candidate fits the selected profile.')
        fid,anchor,pitches=chosen
        notes=[]
        for midi in sorted(pitches):
            if midi not in tuning:tuning[midi]=round(rng.uniform(*policy['cents_uniform_range']),2)
            role='anchor' if midi==min(pitches) else ('color' if midi>=anchor+19 else 'body')
            notes.append({'midi':midi,'cents':tuning[midi],'role':role,'velocity':48 if role=='color' else 60})
        states.append({'index':i,'start_s':round(t,3),'end_s':round(end,3),'family':fid,'anchor_midi':anchor,'transition':transition,'notes':notes,'automation_targets':{'distorted_parallel_gain_db':round(rng.uniform(-18,-6),1),'noise_relative_db':round(rng.uniform(-30,-18),1),'upper_layer_gain_db':round(rng.uniform(-10,0),1),'reverb_send':round(rng.uniform(.15,.32),2)},'parameter_status':'proposed_initialization_not_measured_original'})
        t=end;previous=states[-1];i+=1
    return {'schema_version':'1.0','protocol_version':protocol['version'],'profile':profile,'seed':seed,'duration_s':duration,'status':'original_rule_generated_harmonic_sketch_not_audio_style_verified','cadential_plan':'nonfunctional','states':states}

def validate(sketch,protocol):
    errors=[];warnings=[]
    def error(rule,detail):errors.append({'rule':rule,'detail':detail})
    def warn(rule,detail):warnings.append({'rule':rule,'detail':detail})
    states=sketch.get('states',[]);profile=sketch.get('profile')
    duration=sketch.get('duration_s')
    if not isinstance(duration,(int,float)) or not math.isfinite(duration) or duration<=0:
        error('H00','A finite positive duration_s is required.');return {'passed':False,'errors':errors,'warnings':warnings}
    if profile not in protocol['profiles']:error('H00','Unknown profile.');return {'passed':False,'errors':errors,'warnings':warnings}
    if not states:error('H00','At least one state is required.')
    if sketch.get('cadential_plan') in ['functional_dominant_tonic','repeating_ii_V_I']:
        error('H07','Declared functional cadence plan is outside this protocol default.')
    prev=None;previous_end=0
    for idx,s in enumerate(states):
        fid=s.get('family');a=s.get('start_s');b=s.get('end_s');ns=s.get('notes',[])
        if not isinstance(a,(int,float)) or not isinstance(b,(int,float)) or not math.isfinite(a) or not math.isfinite(b) or b<=a:
            error('H00',f'State {idx}: invalid finite time interval.');continue
        if abs(a-previous_end)>.002:error('H00',f'State {idx}: timeline gap/overlap.')
        previous_end=b
        if fid not in protocol['families']:
            error('H01',f'State {idx}: unapproved source family {fid}; requires evidence review.');continue
        if fid not in protocol['profiles'][profile]['families']:error('H02',f'State {idx}: family not enabled in profile.')
        root=s.get('anchor_midi')
        if not isinstance(root,int):error('H00',f'State {idx}: integer anchor required.');continue
        valid=[]
        for n in ns:
            m=n.get('midi');c=n.get('cents',0)
            if not isinstance(m,int) or not 0<=m<=127 or not isinstance(c,(int,float)) or not math.isfinite(c):
                error('H00',f'State {idx}: invalid note.');continue
            valid.append(n)
            if abs(c)>50:error('H03',f'State {idx}: >50-cent offset must be represented as another pitch or separately reviewed.')
        if len(valid)!=len(ns):continue
        pitches=[n['midi'] for n in ns]
        if not 1<=len(pitches)<=6:error('H04',f'State {idx}: source body must contain 1–6 voices.')
        if len(pitches)!=len(set(pitches)):error('H04',f'State {idx}: duplicate MIDI entries; encode unison layers separately.')
        pcs={(m-root)%12 for m in pitches}
        expected=set(protocol['families'][fid]['pitch_classes'])
        if pcs!=expected:error('H01',f'State {idx}: voiced pitch classes {sorted(pcs)} do not match family {fid}.')
        if pitches and (min(pitches)<28 or max(pitches)>90):error('H04',f'State {idx}: exceeds protocol register E1–F#6 guardrails (MIDI 28–90).')
        if fid=='low_semitone' and profile!='low_beating_field':error('H02',f'State {idx}: low beating pair needs the dedicated texture profile.')
        if pitches and min(pitches)<48:
            low=sorted(set(m for m in pitches if m<48))
            if any(low[k+2]-low[k]<=2 for k in range(len(low)-2)):error('H05',f'State {idx}: three adjacent chromatic low voices are excluded.')
        if prev:
            before={n['midi']:n for n in prev['notes']};after={n['midi']:n for n in ns};common=set(before)&set(after)
            tag=s.get('transition')
            if tag=='common_tone_revoicing' and not common:error('H06',f'State {idx}: declared common tone is absent.')
            if tag=='retain_pitch_object' and set(before)!=set(after):error('H06',f'State {idx}: retained object changed pitches.')
            if tag=='parallel_semitone_displacement':
                p=sorted(before);q=sorted(after)
                if not(len(p)==len(q) and all(v-u==1 for u,v in zip(p,q)) or len(p)==len(q) and all(v-u==-1 for u,v in zip(p,q))):error('H06',f'State {idx}: declared parallel semitone move is not exact.')
            elif not common:warn('H06',f'State {idx}: complete pitch replacement; use as a deliberate scene change, not every transition.')
            if any(abs(before[m].get('cents',0)-after[m].get('cents',0))>.01 for m in common):warn('H03',f'State {idx}: shared voices retune; preserve offsets unless intentional.')
            if set(before)!=set(after) and b-a<8:warn('H08',f'State {idx}: rapid harmonic-state change; confirm it is not an imposed pop grid.')
        prev=s
    if abs(previous_end-sketch.get('duration_s',previous_end))>.002:error('H00','Declared duration differs from timeline.')
    return {'passed':not errors,'meaning':'protocol compliance only, not measured artist similarity','errors':errors,'warnings':warnings}

def vlq(n):
    out=[n&127];n>>=7
    while n:out.insert(0,(n&127)|128);n>>=7
    return bytes(out)

def write_midi(sketch,path):
    """Format 0, 480 PPQ, 60 BPM time carrier; no meter claim. Common tones tie."""
    channels=[c for c in range(16) if c!=9];events=[];active={};free=channels.copy()
    events.append((0,0,b'\xff\x51\x03\x0f\x42\x40'))
    for c in channels:
        for cc,val in [(101,0),(100,0),(6,2),(38,0),(101,127),(100,127)]:events.append((0,0,bytes([0xB0+c,cc,val])))
    def off(key,tick):
        ch=active.pop(key);events.append((tick,1,bytes([0x80+ch,key[0],0])));free.append(ch)
    for s in sketch['states']:
        tick=round(s['start_s']*480);desired={(n['midi'],n['cents']):n for n in s['notes']}
        for key in list(active):
            if key not in desired:off(key,tick)
        for key,n in desired.items():
            if key in active:continue
            ch=free.pop(0);active[key]=ch
            bend=round(8192+key[1]/200*8192);bend=max(0,min(16383,bend))
            events.append((tick,2,bytes([0xE0+ch,bend&127,bend>>7])))
            events.append((tick,3,bytes([0x90+ch,key[0],n['velocity']])))
    for key in list(active):off(key,round(sketch['duration_s']*480))
    events.sort(key=lambda x:(x[0],x[1]));track=bytearray();last=0
    for tick,_,msg in events:track.extend(vlq(tick-last)+msg);last=tick
    track.extend(b'\x00\xff\x2f\x00')
    path.write_bytes(b'MThd'+struct.pack('>IHHH',6,0,1,480)+b'MTrk'+struct.pack('>I',len(track))+track)

def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    g=sub.add_parser('generate');g.add_argument('--profile',default='radio_suspended');g.add_argument('--seed',type=int,default=260926);g.add_argument('--duration',type=float,default=240);g.add_argument('--out',type=Path,required=True)
    v=sub.add_parser('validate');v.add_argument('path',type=Path)
    args=p.parse_args();protocol=read_protocol()
    if args.command=='validate':
        result=validate(json.loads(args.path.read_text()),protocol);print(json.dumps(result,indent=2));raise SystemExit(0 if result['passed'] else 1)
    sketch=generate(protocol,args.profile,args.seed,args.duration);result=validate(sketch,protocol)
    if not result['passed']:raise RuntimeError(result)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.with_suffix('.json').write_text(json.dumps(sketch,indent=2)+'\n',encoding='utf8');write_midi(sketch,args.out.with_suffix('.mid'))
    print(json.dumps({'json':str(args.out.with_suffix('.json')),'midi':str(args.out.with_suffix('.mid')),'validation':result},indent=2))
if __name__=='__main__':main()
