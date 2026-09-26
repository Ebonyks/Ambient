from pathlib import Path
import sys,json,hashlib
R=Path(__file__).resolve().parents[1];repo=R.parents[1]
sys.path.insert(0,str(repo/'protocols/hecker-harmony-v1'))
from harmony_tool import read_protocol,validate,write_midi
P=read_protocol()
rows=[(0,70,'major_add_ninth',38,[38,54,57,64],'D / F# A E','initial'),(70,112,'minor_seventh',35,[35,54,57,62],'B below retained F# and A','common_tone_revoicing'),(112,160,'major_seventh',43,[43,54,59,62],'G below retained F# and D','common_tone_revoicing'),(160,208,'major_seventh',36,[36,55,59,64],'C with B retained as a major seventh','common_tone_revoicing'),(208,252,'minor_seventh',40,[40,55,59,62],'E below retained G and B','common_tone_revoicing'),(252,294,'minor_seventh',43,[43,58,62,65],'G minor keeps D; Bb and F darken the object','common_tone_revoicing'),(294,336,'major',38,[38,54,57,62],'D remains; F# and A return around it','common_tone_revoicing')]
tuning={m:round(((m*17)%9-4)*.65,2)for row in rows for m in row[4]}
states=[]
for i,(a,b,f,root,notes,title,tr)in enumerate(rows):
 states.append({'index':i,'start_s':a,'end_s':b,'family':f,'anchor_midi':root,'transition':tr,'title':title,'notes':[{'midi':m,'cents':tuning[m],'role':'anchor' if m==min(notes) else 'body','velocity':48 if m==min(notes) else 54}for m in notes],'automation_targets':{'distorted_parallel_gain_db':[-15,-14,-17,-13,-9,-11,-18][i],'noise_relative_db':-26,'upper_layer_gain_db':[-3,-2,-5,-2,0,-2,-5][i],'reverb_send':.18},'parameter_status':'authored_original_not_recovered_from_reference'})
sketch={'schema_version':'1.0','protocol_version':'1.0','profile':'common_tone_clarity','duration_s':336,'seed':260926,'cadential_plan':'nonfunctional','status':'authored_expansion_of_Long_Line_original_motif','states':states}
result=validate(sketch,P);assert result['passed'],result
(R/'harmony.json').write_text(json.dumps(sketch,indent=2));(R/'Audit/harmony_validation.json').write_text(json.dumps(result,indent=2));write_midi(sketch,R/'harmony.mid')
# Real source identities, tied by absolute pitch and cents; shared notes are rendered once.
events=[];active={}
for i,s in enumerate(states):
 desired={n['midi']:n for n in s['notes']}
 for m in list(active):
  if m not in desired:events[active.pop(m)]['end_s']=s['start_s']
 new=[m for m in desired if m not in active]
 for j,m in enumerate(new):
  start=(10+j*2.7 if i==0 else s['start_s']+j*1.7)
  active[m]=len(events);events.append({'midi':m,'cents':tuning[m],'role':desired[m]['role'],'start_s':start,'end_s':330,'source_id':len(events)})
for m in active:events[active[m]]['end_s']=330
(R/'voice_events.json').write_text(json.dumps(events,indent=2))
# Seven complete motif statements, with three recorded articulations; no whole-track looping.
phrases=[{'start_s':16,'source_start_s':7,'source_end_s':40.5,'variant':0,'gain':.9}, {'start_s':57,'source_start_s':38,'source_end_s':73,'variant':1,'gain':1}, {'start_s':103,'source_start_s':72,'source_end_s':108,'variant':2,'gain':.85}, {'start_s':150,'source_start_s':38,'source_end_s':73,'variant':1,'gain':.95}, {'start_s':202,'source_start_s':7,'source_end_s':40.5,'variant':0,'gain':1.08}, {'start_s':250,'source_start_s':72,'source_end_s':108,'variant':2,'gain':.96}, {'start_s':292,'source_start_s':38,'source_end_s':73,'variant':1,'gain':.82}]
(R/'phrase_map.json').write_text(json.dumps({'phrases':phrases,'intent':'Source timing remains; bass reinterpretation, independent color and distortion change context. Pauses occur after completed descents to D, not mid-statement.'},indent=2))
print(json.dumps(result));print('Tied source events',len(events),'versus',sum(len(s['notes'])for s in states),'state entries')
