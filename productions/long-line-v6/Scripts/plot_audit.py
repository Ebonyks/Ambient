from pathlib import Path
import numpy as np,json,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
R=Path(__file__).resolve().parents[1];d=np.load(R/'Scripts/analysis/audio_analysis/features/long_line_08.npz');events=json.loads((R/'Audit/nominal_source_events.json').read_text());states=json.loads((R/'harmony.json').read_text())['states']
fig,ax=plt.subplots(3,1,figsize=(13,8),sharex=True,gridspec_kw={'height_ratios':[2.5,1,1]});fig.patch.set_facecolor('#fafaf7')
for a in ax:a.set_facecolor('#fafaf7');a.spines[['top','right']].set_visible(False);a.grid(axis='x',alpha=.15)
for a,b,role,m in events:ax[0].plot([a,b],[m,m],color='#bd622d' if role=='motif' else '#187b83',lw=3 if role=='body' else 1.8,solid_capstyle='round')
for state in states:
 for a in ax:a.axvline(state['start_s'],color='#aaa',lw=.7,alpha=.5)
 ax[0].text((state['start_s']+state['end_s'])/2,77,['Dadd9','Bm7','Gmaj7','Cmaj7','Em7','Gm7','D'][state['index']],ha='center',fontsize=10)
ax[0].set_ylim(32,81);ax[0].set_ylabel('Nominal source pitch (MIDI)');ax[0].set_title('Long Line • 5:36 study draft\nTeal: tied harmonic source events · orange: existing melodic arch',loc='left',fontsize=15,pad=16)
t=np.arange(len(d['rms']))*.5;ax[1].plot(t,d['rms'],color='#343d58',lw=1);ax[1].set_ylabel('Mono RMS\n(dBFS)');ax[1].set_ylim(-70,-10)
ax[2].plot(t,d['centroid'],color='#834789',lw=1);ax[2].set_ylabel('Power centroid\n(Hz)');ax[2].set_ylim(0,2200);ax[2].set_xlim(0,336);ax[2].xaxis.set_major_formatter(FuncFormatter(lambda x,p:f'{int(x)//60}:{int(x)%60:02d}'));ax[2].set_xlabel('Track time')
fig.text(.07,.018,'Source events are authored intent, not an audio transcription. Measurements use the handoff extractor at 22,050 Hz.',fontsize=9,color='#555');fig.tight_layout(rect=[0,.035,1,1]);fig.savefig(R/'Audit/arrangement_and_measurements.png',dpi=160)
print('Audit figure saved')
