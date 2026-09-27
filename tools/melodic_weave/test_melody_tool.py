import copy,json,unittest
from pathlib import Path
from melody_tool import generate,validate,write_midi
H=json.loads((Path(__file__).resolve().parents[2]/'productions/long-line-v6/harmony.json').read_text(encoding='utf8'))
class MelodyTests(unittest.TestCase):
 def test_seed_reproducibility_and_variation(self):
  self.assertEqual(generate(H,4),generate(H,4));self.assertNotEqual(generate(H,4),generate(H,5))
 def test_100_seeds_have_valid_bounded_overlap(self):
  for seed in range(100):self.assertTrue(validate(generate(H,seed))['passed'],seed)
 def test_tied_notes_not_retriggered(self):
  s=generate(H);self.assertTrue(any(g['retained']for g in s['gestures']))
  bad=copy.deepcopy(s);e=copy.deepcopy(bad['events'][3]);bad['events'].append(e);self.assertFalse(validate(bad)['passed'])
 def test_reject_invalid_timing_and_density(self):
  s=generate(H);s['events'][0]['end_s']=float('nan');self.assertFalse(validate(s)['passed'])
  s=generate(H);s['events']+=copy.deepcopy(s['events']);self.assertFalse(validate(s)['passed'])
 def test_custom_cells_and_friction_controls(self):
  a=generate(H,cells=[[64,66,69],[71,74]],friction_pc=None)
  self.assertTrue(validate(a)['passed']);self.assertNotEqual(a['events'],generate(H)['events'])
  self.assertIsNone(a['friction_pitch_class'])
  for cells in [[],[[]],[[500]],[[True]]]:
   with self.assertRaises(ValueError):generate(H,cells=cells)
 def test_anchor_is_tied_across_identical_states(self):
  h=copy.deepcopy(H);h['states'][1]['notes']=copy.deepcopy(h['states'][0]['notes'])
  s=generate(h);es=[e for e in s['events']if e['voice']==3]
  self.assertEqual(es[0]['end_s'],112);self.assertTrue(validate(s)['passed'])
 def test_bad_inputs(self):
  for interval in [(0,2),(3,2),(float('nan'),2)]:
   with self.assertRaises(ValueError):generate(H,change_range=interval)
  bad=copy.deepcopy(H);bad['states'][1]['start_s']+=1
  with self.assertRaises(ValueError):generate(bad)
 def test_fields_do_not_reset_whole_ensemble(self):
  s=generate(H)
  for state in H['states'][1:]:
   boundary=state['start_s'];self.assertTrue(any(e['voice']!=3 and e['start_s']<boundary<e['end_s']for e in s['events']))
 def test_development_is_not_seven_identical_arches(self):
  s=generate(H);phrases={}
  for e in s['events']:
   if e['voice']==2:phrases.setdefault(e['phrase'],[]).append(e['midi'])
  self.assertGreater(len(set(tuple(x)for x in phrases.values())),6)
 def test_midi_note_lifecycle_and_bends(self):
  import tempfile
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'x.mid';s=generate(H);write_midi(s,p);data=p.read_bytes();self.assertEqual(data[:4],b'MThd')
   b=data[22:];i=0;active={};ons=0
   while i<len(b):
    while b[i]&128:i+=1
    i+=1;status=b[i];i+=1
    if status==255:
     kind=b[i];n=b[i+1];i+=2+n
     if kind==47:break
    else:
     a,c=b[i:i+2];i+=2;channel=status&15;kind=status&240
     if kind==144:self.assertNotIn(channel,active);active[channel]=a;ons+=1
     elif kind==128:self.assertEqual(active.pop(channel),a)
     elif kind==224:self.assertNotIn(channel,active)
   self.assertEqual(ons,len(s['events']));self.assertFalse(active)
if __name__=='__main__':unittest.main()
