from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path('productions/long-line-v7');s=json.loads((R/'weave.json').read_text(encoding='utf8'));old=json.loads((R.parent/'long-line-v6/voice_events.json').read_text(encoding='utf8'))
fig,ax=plt.subplots(2,1,figsize=(15,7),sharex=True)
for e in old:ax[0].plot([e['start_s'],e['end_s']],[e['midi']]*2,color='#6f869e',lw=3)
starts=[16,57,103,150,202,250,292];pattern=[69,71,74,71,69,64,62];times=[0,3.8,8.1,15,19,24,27.5]
for t in starts:
 for off,m in zip(times,pattern):ax[0].plot([t+off,min(336,t+off+4)],[m]*2,color='#ba7134',lw=3)
ax[0].set_title('v6: sustained inner pitches and seven repeats of the same upper contour (upper timing schematic)')
colors=['#277d8e','#53a567','#c27931','#79808b']
for e in s['events']:ax[1].plot([e['start_s'],e['end_s']],[e['midi']]*2,color=colors[e['voice']],lw=3)
ax[1].set_title('v7: staggered inner motion, developed fragments, retained anchors; actual score events')
for a in ax:a.set_ylabel('MIDI pitch');a.set_ylim(30,82);a.grid(alpha=.18);a.set_xlim(0,336)
ax[1].set_xlabel('Seconds');fig.tight_layout();fig.savefig(R/'Audit/voicing_comparison.png',dpi=140)
