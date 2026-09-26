import copy, struct, unittest
from pathlib import Path
import tempfile
from harmony_tool import read_protocol,generate,validate,write_midi

class ProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.p=read_protocol()
    def test_all_profiles_across_seeds(self):
        for profile in self.p['profiles']:
            for seed in range(25):
                s=generate(self.p,profile,seed,240)
                self.assertTrue(validate(s,self.p)['passed'],(profile,seed,validate(s,self.p)))
                self.assertEqual(s['states'][-1]['end_s'],240)
    def test_deterministic(self):
        self.assertEqual(generate(self.p,'radio_suspended',11,240),generate(self.p,'radio_suspended',11,240))
    def test_unlisted_harmony_rejected(self):
        s=generate(self.p,'radio_suspended',2,60);s['states'][0]['family']='fully_diminished_seventh'
        self.assertFalse(validate(s,self.p)['passed'])
    def test_major_is_permitted(self):
        s={'profile':'common_tone_clarity','duration_s':40,'states':[{'family':'major','anchor_midi':48,'start_s':0,'end_s':40,'notes':[{'midi':48,'cents':0},{'midi':55,'cents':0},{'midi':64,'cents':0}]}]}
        self.assertTrue(validate(s,self.p)['passed'])
    def test_injected_third_rejected_in_open_fifth(self):
        s={'profile':'radio_suspended','duration_s':40,'states':[{'family':'open_fifth','anchor_midi':48,'start_s':0,'end_s':40,'notes':[{'midi':48,'cents':0},{'midi':51,'cents':0},{'midi':55,'cents':0}]}]}
        self.assertFalse(validate(s,self.p)['passed'])
    def test_low_pair_requires_context(self):
        s=generate(self.p,'low_beating_field',2,60);s['profile']='radio_suspended'
        self.assertFalse(validate(s,self.p)['passed'])
    def test_false_common_tone_declaration_rejected(self):
        s=generate(self.p,'radio_suspended',2,180)
        a=s['states'][0];b=copy.deepcopy(a);a['end_s']=90;b['start_s']=90;b['end_s']=180
        b['notes']=[dict(n,midi=n['midi']+6) for n in b['notes']];b['anchor_midi']+=6;b['transition']='common_tone_revoicing';s['states']=[a,b]
        self.assertFalse(validate(s,self.p)['passed'])
    def test_cadential_default_rejected(self):
        s=generate(self.p,'common_tone_clarity',2,60);s['cadential_plan']='repeating_ii_V_I'
        self.assertFalse(validate(s,self.p)['passed'])
    def test_nonfinite_time_rejected(self):
        s=generate(self.p,'radio_suspended',2,60);s['states'][0]['start_s']=float('nan')
        self.assertFalse(validate(s,self.p)['passed'])
    def test_midi_balanced_events_and_duration(self):
        s=generate(self.p,'mirages_pressure',2,240)
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'test.mid';write_midi(s,p);b=p.read_bytes()
        self.assertEqual(b[:4],b'MThd');self.assertEqual(struct.unpack('>IHHH',b[4:14]),(6,0,1,480))
        self.assertEqual(b[14:18],b'MTrk');self.assertEqual(struct.unpack('>I',b[18:22])[0],len(b)-22)
        i=22;time=0;active=set()
        def readvlq():
            nonlocal i
            n=0
            while True:
                q=b[i];i+=1;n=n*128+(q&127)
                if not(q&128):return n
        while i<len(b):
            time+=readvlq();status=b[i];i+=1
            if status==255:
                kind=b[i];i+=1;length=readvlq();i+=length
                if kind==47:break
            else:
                a,c=b[i:i+2];i+=2;ch=status&15
                if status>>4==9:
                    self.assertNotIn((ch,a),active);active.add((ch,a))
                elif status>>4==8:
                    self.assertIn((ch,a),active);active.remove((ch,a))
        self.assertFalse(active);self.assertEqual(time,240*480)

if __name__=='__main__':unittest.main()
