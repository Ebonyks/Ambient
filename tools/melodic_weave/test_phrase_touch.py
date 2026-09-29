import json,unittest
from pathlib import Path
from phrase_touch import shape
from texture_weave import validate
ROOT=Path(__file__).resolve().parents[2]
class PhraseTouchTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.old=json.loads((ROOT/'productions/long-line-v13-octaves/texture.json').read_text());cls.new=shape(cls.old)
 def test_pitch_harmony_and_event_count_preserved(self):
  self.assertTrue(validate(self.new)['passed']);self.assertEqual(self.old['harmonic_fields'],self.new['harmonic_fields']);self.assertEqual(len(self.old['events']),len(self.new['events']))
  for v in range(8):
   a=[e for e in self.old['events'] if e['voice']==v];b=[e for e in self.new['events'] if e['voice']==v];self.assertEqual([e['midi'] for e in a],[e['midi'] for e in b]);self.assertTrue(all(abs(x['start_s']-y['start_s'])<=.0051 for x,y in zip(a,b)))
 def test_each_repetition_has_distinct_bounded_touch(self):
  rows=self.new['phrase_touch']['cycles'];signatures=[(r['crest_fraction'],r['timing_s'],r['touch'],tuple(r['gain_db'])) for r in rows];self.assertEqual(len(set(signatures)),len(rows));self.assertTrue(all(max(abs(x) for x in r['gain_db'])<=.71 for r in rows));self.assertTrue(all(abs(r['timing_s'])<=.005 for r in rows))
 def test_reproducible_with_actual_gain_data_for_all_parts(self):
  self.assertEqual(self.new,shape(self.old));self.assertEqual(set(self.new['phrase_touch']['lane_gain_points']),{'4','5','6','7'});self.assertTrue(all(len(p)>500 for p in self.new['phrase_touch']['lane_gain_points'].values()))
if __name__=='__main__':unittest.main()
