from pathlib import Path
import json,sys
R=Path(__file__).resolve().parents[1];ROOT=R.parents[1];sys.path.insert(0,str(ROOT/'tools/melodic_weave'))
from refine_voicing import revise
from melody_tool import validate,write_midi
old=json.loads((R.parent/'long-line-v7/weave.json').read_text(encoding='utf8'));h=json.loads((R.parent/'long-line-v6/harmony.json').read_text(encoding='utf8'))
patch={(2,t):m for t,m in [(161.766,67),(174.159,64),(179.668,67),(184.864,71),(192.237,74),(197.174,76),(203.207,67)]}
s=revise(old,h,patch);assert validate(s)['passed'];(R/'weave.json').write_text(json.dumps(s,indent=2),encoding='utf8');write_midi(s,R/'weave.mid')
# Native REAPER source printing uses a simple, inspectable Lua event table.
lines=['return {']
for e in s['events']:
 if e['voice']==0:lines.append('{%.3f,%.3f,%d,%d},'%(e['start_s'],e['end_s'],e['midi'],e['velocity']))
lines.append('}');(R/'Scripts/string_notes.lua').write_text('\n'.join(lines),encoding='utf8')
(R/'Audit/voicing_revision.json').write_text(json.dumps({'edits':s['revision_log'],'semitone_returns':s['semitone_return_audit'],'timing_preserved':all(a['start_s']==b['start_s']and a['end_s']==b['end_s'] for a,b in zip(old['events'],s['events'])),'validation':validate(s)},indent=2),encoding='utf8')
print('Revised',len(s['revision_log']),'events; semitone returns:',len(s['semitone_return_audit']['before']),'to',len(s['semitone_return_audit']['after']))
