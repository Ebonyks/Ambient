"""Local revision of an existing event score: remove repeated semitone return figures."""
import copy

def semitone_returns(score):
    found=[]
    for voice in range(3):
        es=sorted((e for e in score['events'] if e['voice']==voice),key=lambda e:e['start_s'])
        for a,b,c in zip(es,es[1:],es[2:]):
            if a['midi']==c['midi'] and abs(a['midi']-b['midi'])==1:found.append({'voice':voice,'start_s':a['start_s'],'middle_s':b['start_s'],'pitches':[a['midi'],b['midi'],c['midi']]})
    return found

def revise(score,harmony,passage_overrides=None):
    result=copy.deepcopy(score);log=[];before=semitone_returns(score)
    for e in result['events']:
        key=(e['voice'],e['start_s'])
        if passage_overrides and key in passage_overrides:
            m=passage_overrides[key];log.append({'voice':e['voice'],'time_s':e['start_s'],'from':e['midi'],'to':m,'reason':'Authored replacement of the weak 2:48 passage'});e['midi']=m
        if e['voice']!=3:e['cents']=0
    for _ in range(100):
        turns=semitone_returns(result)
        if not turns:break
        turn=turns[0];voice=turn['voice'];es=sorted((e for e in result['events']if e['voice']==voice),key=lambda e:e['start_s']);i=next(i for i,e in enumerate(es)if e['start_s']==turn['middle_s']);e=es[i]
        state=next(s for s in harmony['states']if s['start_s']<=e['start_s']<s['end_s']);pcs={n['midi']%12 for n in state['notes']};lo,hi=[(50,62),(59,71),(62,79)][voice]
        choices=[m for m in range(lo,hi+1)if m%12 in pcs and abs(m-es[i-1]['midi'])>=3 and m!=es[i+1]['midi']]
        if not choices:raise ValueError('No non-rocking local candidate; author this passage explicitly')
        m=min(choices,key=lambda m:(abs(m-e['midi']),abs(m-es[i-1]['midi']),m));log.append({'voice':voice,'time_s':e['start_s'],'from':e['midi'],'to':m,'reason':'Remove A-B-A semitone return without banning isolated semitone motion'});e['midi']=m
    else:raise ValueError('Revision did not converge')
    result['revision']='1.1-tonal-review';result['pitch_policy']='No automatic friction injection in revision. Semitone return figures removed; isolated tension allowed. Original timing and roles retained. Non-anchor pitch offsets zero.'
    result['revision_log']=log;result['semitone_return_audit']={'before':before,'after':semitone_returns(result)}
    result['gestures_status']='Inherited v7 proposal log; events and revision_log are authoritative after edits.'
    return result

if __name__=='__main__':
    import argparse,json
    from pathlib import Path
    from melody_tool import validate,write_midi
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('score',type=Path);p.add_argument('--harmony',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    s=revise(json.loads(a.score.read_text(encoding='utf-8-sig')),json.loads(a.harmony.read_text(encoding='utf-8-sig')))
    check=validate(s)
    if not check['passed']:raise ValueError(check)
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.with_suffix('.json').write_text(json.dumps(s,indent=2),encoding='utf8');write_midi(s,a.out.with_suffix('.mid'));print(json.dumps({'revised_events':len(s['revision_log']),'semitone_returns_after':len(semitone_returns(s)),'validation':check}))
