import json,unittest
from pathlib import Path
from flowing_lines import generate,BOUNDS,RATES,CELLS
from continuous_field import performance_score
from texture_weave import validate
ROOT=Path(__file__).resolve().parents[2]
class FlowingLineTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.base=json.loads((ROOT/'productions/long-line-v8/weave.json').read_text());cls.s=generate(cls.base)
 def test_fourfold_activity(self):
  old=json.loads((ROOT/'productions/long-line-v10-flow/texture.json').read_text());a=sum(e['voice']>=4 for e in old['events']);b=sum(e['voice']>=4 for e in self.s['events']);self.assertAlmostEqual(b/a,4,delta=.01)
 def test_distinct_lines_and_moving_tonality(self):
  self.assertEqual(len(set(CELLS)),4);self.assertEqual(len(set(BOUNDS)),4);self.assertEqual(len(set(RATES)),4)
  for lane in range(4):
   notes=[e['midi'] for e in self.s['events'] if e['voice']==lane+4];self.assertTrue(all(BOUNDS[lane][0]<=n<=BOUNDS[lane][1] for n in notes));self.assertGreater(len(set(notes)),8)
  self.assertTrue(all(a['pitch_classes']!=b['pitch_classes'] for a,b in zip(self.s['tonal_plan'],self.s['tonal_plan'][1:])))
 def test_determinism_validity_and_foreground_exclusion(self):
  self.assertEqual(self.s,generate(self.base));self.assertTrue(validate(self.s)['passed']);p=performance_score(self.s);self.assertTrue(validate(p)['passed']);self.assertTrue(all(e['voice']>=4 for e in p['events']))
 def test_three_and_half_second_harmony_preserves_note_clock(self):
  quick=generate(self.base,harmonic_period_s=3.5);self.assertTrue(validate(quick)['passed'])
  self.assertEqual([q['start_s'] for q in quick['tonal_plan']],[i*3.5 for i in range(96)])
  self.assertEqual([(e['voice'],e['start_s'],e['velocity']) for e in quick['events']],[(e['voice'],e['start_s'],e['velocity']) for e in self.s['events']])
  for bad in [0,float('nan'),13]:
   with self.assertRaises(ValueError):generate(self.base,harmonic_period_s=bad)
 def test_other_seeds_preserve_construction(self):
  for seed in [1,77,234]:self.assertTrue(validate(generate(self.base,seed))['passed'])
if __name__=='__main__':unittest.main()
