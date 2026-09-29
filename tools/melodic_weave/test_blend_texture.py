import copy,json,unittest
from pathlib import Path
from blend_texture import revise,clashes,overlaps
ROOT=Path(__file__).resolve().parents[2]
class BlendTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.old=json.loads((ROOT/'productions/long-line-v9-study/texture.json').read_text());cls.new=revise(cls.old)
 def test_context_and_release_guard(self):
  self.assertGreater(len(clashes(self.old,1)),0);self.assertEqual(clashes(self.new,1),[])
 def test_preserves_scaffold_without_mutating_input(self):
  original=copy.deepcopy(self.old);revise(self.old);self.assertEqual(self.old,original);self.assertEqual(self.new['scaffold'],self.old['scaffold']);self.assertEqual([e for e in self.new['events'] if e['voice']<4],self.old['scaffold']['events'])
 def test_omits_instead_of_forcing_conflict(self):
  omitted=[e for e in self.new['blend_revision']['edits'] if e['to'] is None];self.assertGreater(len(omitted),0)
  keys={(e['voice'],e['start_s']) for e in self.new['events'] if e['voice']>=4}
  self.assertTrue(all((e['voice'],e['start_s']) not in keys for e in omitted))
 def test_tail_boundary_and_invalid_guard(self):
  a={'start_s':0,'end_s':1};b={'start_s':1.5,'end_s':2};self.assertFalse(overlaps(a,b));self.assertTrue(overlaps(a,b,1))
  for tail in [-1,4,float('nan')]:
   with self.assertRaises(ValueError):revise(self.old,tail)
if __name__=='__main__':unittest.main()
