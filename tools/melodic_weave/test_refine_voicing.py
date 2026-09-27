import copy,json,unittest
from pathlib import Path
from refine_voicing import revise,semitone_returns
from melody_tool import generate,validate
ROOT=Path(__file__).resolve().parents[2]
H=json.loads((ROOT/'productions/long-line-v6/harmony.json').read_text(encoding='utf8'))
OLD=json.loads((ROOT/'productions/long-line-v7/weave.json').read_text(encoding='utf8'))
class VoicingRevisionTests(unittest.TestCase):
 def test_actual_regression(self):
  self.assertEqual(len(semitone_returns(OLD)),12);s=revise(OLD,H);self.assertEqual(semitone_returns(s),[]);self.assertTrue(validate(s)['passed'])
 def test_preserves_source_and_timing(self):
  before=copy.deepcopy(OLD);s=revise(OLD,H);self.assertEqual(OLD,before)
  self.assertEqual([(e['voice'],e['start_s'],e['end_s'])for e in OLD['events']],[(e['voice'],e['start_s'],e['end_s'])for e in s['events']])
 def test_sustained_semitone_and_one_way_motion_remain(self):
  s=copy.deepcopy(OLD);s['events']=[{'voice':0,'start_s':0,'end_s':9,'midi':59,'cents':0},{'voice':1,'start_s':0,'end_s':3,'midi':60,'cents':0},{'voice':1,'start_s':3,'end_s':6,'midi':61,'cents':0},{'voice':1,'start_s':6,'end_s':9,'midi':65,'cents':0}]
  self.assertEqual(revise(s,H)['events'],s['events'])
 def test_determinism_and_fixed_nonanchor_pitch(self):
  self.assertEqual(revise(OLD,H),revise(OLD,H));self.assertTrue(all(e['cents']==0 for e in revise(OLD,H)['events']if e['voice']!=3))
 def test_100_seeded_sketches_terminate_and_validate(self):
  for seed in range(100):
   s=revise(generate(H,seed),H);self.assertFalse(semitone_returns(s));self.assertTrue(validate(s)['passed'],seed)
if __name__=='__main__':unittest.main()
