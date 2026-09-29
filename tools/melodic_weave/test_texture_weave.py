import copy,json,tempfile,unittest,struct
from pathlib import Path
from texture_weave import generate,validate,write_midi
ROOT=Path(__file__).resolve().parents[2]
H=json.loads((ROOT/'productions/long-line-v6/harmony.json').read_text())
S=json.loads((ROOT/'productions/long-line-v8/weave.json').read_text())
class TextureTests(unittest.TestCase):
 def test_determinism_and_scaffold_preservation(self):
  original=copy.deepcopy(S);a=generate(S,H);self.assertEqual(a,generate(S,H));self.assertEqual(S,original);self.assertEqual([e for e in a['events']if e['voice']<4],S['events']);self.assertNotEqual(a,generate(S,H,22))
 def test_hundred_seeds_and_density_extremes(self):
  for seed in range(100):
   self.assertTrue(validate(generate(S,H,seed,density=[.25,1,1.5][seed%3]))['passed'])
 def test_density_changes_activity_not_scaffold(self):
  a,b=generate(S,H,density=.4),generate(S,H,density=1.2)
  self.assertGreater(len(b['events']),len(a['events'])*2);self.assertEqual(a['scaffold'],b['scaffold'])
 def test_rejects_invalid_inputs(self):
  for d in [0,2,float('nan')]:
   with self.assertRaises(ValueError):generate(S,H,density=d)
  h=copy.deepcopy(H);h['states'][1]['start_s']+=.1
  with self.assertRaises(ValueError):generate(S,h)
 def test_detects_note_ownership_pitch_and_palette_corruption(self):
  for kind in ['collision','pitch','palette','scaffold']:
   s=generate(S,H);e=next(e for e in s['events']if e['voice']==4)
   if kind=='collision':s['events'].append(copy.deepcopy(e))
   elif kind=='pitch':e['cents']=4
   elif kind=='palette':e['midi']=next(m for m in range(50,65)if m%12 not in {n['midi']%12 for n in H['states'][0]['notes']})
   else:s['events'][0]['midi']+=1
   self.assertFalse(validate(s)['passed'],kind)
 def test_fields_do_not_reset_texture_together(self):
  s=generate(S,H)
  for f in H['states'][1:]:
   starts=[min(e['start_s']for e in s['events']if e['voice']==v and e['start_s']>=f['start_s'])for v in range(4,8)]
   self.assertGreater(max(starts)-min(starts),.01)
 def test_midi_multitrack_note_lifecycle(self):
  s=generate(S,H)
  with tempfile.TemporaryDirectory()as d:
   p=Path(d)/'x.mid';write_midi(s,p);b=p.read_bytes();self.assertEqual(struct.unpack('>HHH',b[8:14]),(1,8,480));offset=14;ons=0
   for voice in range(8):
    self.assertEqual(b[offset:offset+4],b'MTrk');n=int.from_bytes(b[offset+4:offset+8],'big');tr=b[offset+8:offset+8+n];offset+=8+n;i=0;active={};tick=0
    def readvar():
     nonlocal i
     v=0
     while True:
      z=tr[i];i+=1;v=(v<<7)|(z&127)
      if z<128:return v
    while i<len(tr):
     tick+=readvar();status=tr[i];i+=1
     if status==255:
      k=tr[i];i+=1;n=readvar();i+=n
      if k==47:break
     else:
      a,c=tr[i:i+2];i+=2;kind=status&240;self.assertEqual(status&15,voice)
      if kind==144:self.assertNotIn(a,active);active[a]=tick;ons+=1
      elif kind==128:self.assertIn(a,active);self.assertLess(active.pop(a),tick)
    self.assertFalse(active);self.assertEqual(tick,round(s['duration_s']*480))
   self.assertEqual(ons,len(s['events']));self.assertEqual(offset,len(b))
if __name__=='__main__':unittest.main()
