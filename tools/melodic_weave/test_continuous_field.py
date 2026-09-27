import json,unittest
from pathlib import Path
from continuous_field import generate,performance_score
from texture_weave import validate
ROOT=Path(__file__).resolve().parents[2]
class ContinuousTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.base=json.loads((ROOT/'productions/long-line-v8/weave.json').read_text());cls.h=json.loads((ROOT/'productions/long-line-v6/harmony.json').read_text());cls.score=generate(cls.base,cls.h)
 def test_valid_deterministic_and_preserved_reference(self):
  self.assertTrue(validate(self.score)['passed']);self.assertEqual(self.score,generate(self.base,self.h));self.assertEqual(self.score['scaffold'],self.base)
 def test_no_velocity_accents_and_continuous_activity(self):
  es=[e for e in self.score['events'] if e['voice']>=4];self.assertEqual({e['velocity'] for e in es},{25});self.assertGreater(len(es),4000)
  for t in range(8,330):self.assertGreaterEqual(sum(t<=e['start_s']<t+1 for e in es),9)
 def test_performance_excludes_reference_foreground(self):
  p=performance_score(self.score);self.assertTrue(validate(p)['passed']);self.assertTrue(all(e['voice']>=4 for e in p['events']));self.assertEqual(len(self.score['scaffold']['events']),123)
 def test_explicit_slow_transitions(self):
  w=[f for f in self.score['harmonic_fields'] if f.get('role')];self.assertEqual(len(w),6);self.assertTrue(all(f['end_s']-f['start_s']==24 for f in w))
  self.assertEqual(self.score['render_contract']['scaffold_moving_voices'],'reference only; excluded from audition audio')
 def test_multiple_seeds_and_distributed_pitches(self):
  for seed in range(8):
   s=generate(self.base,self.h,seed);self.assertTrue(validate(s)['passed'])
   for t in range(10,310,20):
    notes=[e['midi'] for e in s['events'] if e['voice']>=4 and t<=e['start_s']<t+20]
    self.assertLess(max(notes.count(m) for m in set(notes))/len(notes),.4)
if __name__=='__main__':unittest.main()
