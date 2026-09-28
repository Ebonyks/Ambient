import json,unittest
from pathlib import Path
from upper_octaves import add_upper_octaves
from texture_weave import validate
ROOT=Path(__file__).resolve().parents[2]
class UpperOctaveTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.base=json.loads((ROOT/'productions/long-line-v12-quick-shifts/texture.json').read_text());cls.s=add_upper_octaves(cls.base)
 def test_original_notes_and_harmony_unchanged(self):
  self.assertEqual([e for e in self.s['events'] if e.get('role')!='upper_octave_companion'],self.base['events']);self.assertEqual(self.s['harmonic_fields'],self.base['harmonic_fields']);self.assertTrue(validate(self.s)['passed'])
 def test_octaves_only_and_subordinate_velocity(self):
  added=[e for e in self.s['events'] if e.get('role')=='upper_octave_companion'];self.assertGreater(len(added),0)
  for e in added:
   parent=next(a for a in self.base['events'] if a['voice']==e['voice'] and a['start_s']==e['start_s']);self.assertIn(e['midi']-parent['midi'],[12,24]);self.assertLess(e['velocity'],parent['velocity']);self.assertEqual(e['end_s'],parent['end_s'])
 def test_intermittent_and_wider_range(self):
  added=[e for e in self.s['events'] if e.get('role')=='upper_octave_companion'];self.assertLess(len(added)/len(self.base['events']),.05)
  self.assertGreater(max(e['midi'] for e in self.s['events']),max(e['midi'] for e in self.base['events']))
  for voice,period,offset,width in [(4,11.3,1.7,2.8),(6,13.7,6.1,3.1)]:
   self.assertTrue(all((e['start_s']-offset)%period<width for e in added if e['voice']==voice))
if __name__=='__main__':unittest.main()
