from pathlib import Path
import json,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
R=Path(__file__).resolve().parents[1];s=json.loads((R/'texture.json').read_text());fig,axes=plt.subplots(2,1,figsize=(14,7),sharex=True,gridspec_kw={'height_ratios':[1,1.5]})
colors=['#5b6877','#bd7040','#785ba7','#889549','#347f95','#c28d45','#5977b0','#ac6580']
for ax,low,high,title in [(axes[0],0,4,'Preserved scaffold: slow changing voices'),(axes[1],4,8,'New inner arrangement: 809 quiet, interlocking notes in this excerpt')]:
 for voice in range(low,high):
  es=[e for e in s['events']if e['voice']==voice and e['end_s']>140 and e['start_s']<236]
  seg=[[(max(140,e['start_s']),e['midi']),(min(236,e['end_s']),e['midi'])]for e in es]
  ax.add_collection(LineCollection(seg,colors=colors[voice],linewidths=2.4 if low==0 else 1.5,label=('Anchor' if voice==3 else 'Voice '+str(voice))))
 ax.set_xlim(140,236);ax.set_ylim(34 if low==0 else 48,81);ax.set_ylabel('MIDI pitch');ax.set_title(title,loc='left',fontsize=12);ax.grid(alpha=.18);ax.legend(loc='upper right',ncol=4,fontsize=8)
 for t in [160,208]:ax.axvline(t,color='#444444',linestyle='--',alpha=.5)
axes[1].set_xlabel('Position in full composition (seconds); dashed lines mark harmonic-field changes')
fig.suptitle('Melodic Weave: activity inside a sustained tonal surface',fontsize=16,x=.06,ha='left');fig.text(.06,.025,'These are generated MIDI notes, not transcribed reference audio. MIDI density alone does not prove audible richness.',fontsize=10,color='#555555');fig.tight_layout(rect=[0,.05,1,.94]);fig.savefig(R/'Audit/inner_note_structure.png',dpi=140)
