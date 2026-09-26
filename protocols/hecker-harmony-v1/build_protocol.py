from pathlib import Path
import json,hashlib,sys
import numpy as np
ROOT=Path(__file__).resolve().parent
source=Path(sys.argv[1])
study=json.loads((source/'study.json').read_text(encoding='utf8'))
stats=[]
for album in ['radio_amor','mirages','mort_aux_vaches']:
    for threshold in [.28,.40,.55]:
        total=active=poly=0.;num={i:0. for i in range(1,7)};counts=[];spans=[]
        for t in study['tracks']:
            if t['album']!=album:continue
            z=np.load(source/'data'/(t['id']+'_targets.npz'))
            mask=z['target_support_mask']&(z['target_relative_activation']>=threshold);m=z['midi'];times=z['time_s']
            for k in range(mask.shape[1]):
                w=min(.5,t['duration']-times[k]);ns=m[mask[:,k]];pcs=set(int(v%12) for v in ns)
                total+=w;active+=w*bool(len(ns));counts.append(len(pcs))
                if len(pcs)>=2:
                    poly+=w;spans.append(int(max(ns)-min(ns)))
                    intervals={min((b-a)%12,(a-b)%12) for a in pcs for b in pcs if a!=b}
                    for i in num:num[i]+=w*(i in intervals)
        stats.append({'album':album,'relative_activation_threshold':threshold,'analyzed_seconds':round(total,2),'accepted_component_coverage_pct':round(active/total*100,1),'multi_pitch_class_seconds':round(poly,2),'median_distinct_pitch_classes_all_frames':float(np.median(counts)),'median_register_span_semitones_multi_pc_frames':float(np.median(spans)),'interval_class_presence_pct_of_multi_pc_seconds':{str(k):round(v/poly*100,1) for k,v in num.items()}})

def f(name,pcs,voices,evidence,status='allowed'):
    return {'name':name,'pitch_classes':pcs,'voicings_semitones':voices,'permission':status,'evidence':evidence,'claim_scope':'inferred source palette from measured components; not authenticated score','voicing_status':'proposed transposable realization'}
families={
 'open_fifth':f('Open fifth / third omitted',[0,7],[[0,7],[0,7,12]],['mirages_08: A/E field','radio_amor_03: D/A pedal relation']),
 'suspended_second':f('Root, fifth and ninth',[0,2,7],[[0,7,14]],['radio_amor_01: A/E/B component relation']),
 'suspended_fourth':f('Root, fourth and fifth',[0,5,7],[[0,5,19]],['radio_amor_03: D/G/A relation']),
 'suspended_second_fourth':f('Thirdless second/fourth/fifth field',[0,2,5,7],[[0,5,14,19]],['radio_amor_01: A/D/B/E family']),
 'minor_third':f('Minor-third kernel',[0,3],[[0,3],[0,3,12]],['mirages_09: F#/A at 100.5–130.5 s','radio_amor_10: Eb/Gb inner dyad']),
 'minor':f('Minor triad',[0,3,7],[[0,7,15],[0,3,7]],['mirages_07: G2/Bb2/D3 after about 65 s','mirages_09: B/D/F# early']),
 'minor_seventh':f('Minor seventh',[0,3,7,10],[[0,7,15,22],[0,3,7,10]],['mirages_09: C/Eb/G/Bb ending','radio_amor_10: Eb/Gb/Bb/Db family']),
 'minor_ninth':f('Minor ninth field',[0,2,3,7,10],[[0,7,15,22,26]],['mirages_04: G/Bb/D/F/A opening collection; simultaneity provisional']),
 'major':f('Major triad',[0,4,7],[[0,7,16],[0,4,7]],['radio_amor_04: Ab/Eb/C family','radio_amor_08: Db/F/Ab ending']),
 'major_seventh':f('Major seventh',[0,4,7,11],[[0,7,16,23],[0,7,11,16]],['radio_amor_04: Bb/F/A/D family when simultaneous']),
 'major_add_ninth':f('Major add ninth',[0,2,4,7],[[0,7,14,16]],['mirages_11: Ab bass with C/Eb/Bb supports Abadd9 locally']),
 'major_seventh_dyad':f('Bass against distant major seventh',[0,11],[[0,35],[0,23]],['radio_amor_02: low Ab versus high G']),
 'upper_semitone':f('Exposed semitone with optional octave anchor',[0,1],[[0,12,13]],['radio_amor_07: D/Eb opening','mirages_10: D/Eb later'], 'conditional'),
 'paired_semitones':f('Two semitone pairs separated by a fifth',[0,1,7,8],[[0,1,7,8],[0,1,19,20]],['radio_amor_09: G/Ab plus D/Eb middle and late'],'conditional'),
 'low_semitone':f('Two-component low beating field',[0,1],[[0,1]],['mirages_03: G1/Ab1-related low field'],'conditional')}
profiles={
 'radio_suspended':{'description':'Register-separated, third-ambiguous and major/minor inner objects','families':['open_fifth','suspended_second','suspended_fourth','suspended_second_fourth','major','major_seventh','minor','minor_seventh','major_seventh_dyad'],'anchor_midi_range':[36,55],'state_duration_s':[28,72]},
 'mirages_pressure':{'description':'Minor kernels and deliberate friction; distortion remains a separate renderer task','families':['open_fifth','minor_third','minor','minor_seventh','minor_ninth','upper_semitone','paired_semitones'],'anchor_midi_range':[36,50],'state_duration_s':[32,88]},
 'common_tone_clarity':{'description':'Exposed inner voices, major/minor reinterpretation and sustained common tones','families':['minor_third','minor','minor_seventh','major','major_seventh','major_add_ninth'],'anchor_midi_range':[41,55],'state_duration_s':[36,96]},
 'low_beating_field':{'description':'Two low neighboring components treated as a texture object, not a full keyboard chord','families':['low_semitone'],'anchor_midi_range':[28,40],'state_duration_s':[40,100]}}
rules=[
 {'id':'H00','level':'error','rule':'Use finite, contiguous track-relative time and valid MIDI/cents values.'},
 {'id':'H01','level':'error','rule':'Strict-mode source objects must match an approved transposition-relative family; unlisted families require review.'},
 {'id':'H02','level':'error','rule':'Conditional families must be enabled in the selected profile; low semitone requires the low-beating profile.'},
 {'id':'H03','level':'mixed','rule':'Reject offsets beyond 50 cents in a named-note representation; flag unintended common-tone retuning.'},
 {'id':'H04','level':'error','rule':'Use 1–6 separately represented source voices within MIDI 28–90; no duplicate MIDI entries masquerading as new notes.'},
 {'id':'H05','level':'error','rule':'Exclude three or more adjacent chromatic source voices below C3; spectral distortion products are not source voices.'},
 {'id':'H06','level':'mixed','rule':'Validate declared retained objects, common tones and parallel semitone moves; flag complete replacement otherwise.'},
 {'id':'H07','level':'error','rule':'Default protocol excludes declared dominant-to-tonic or repeating ii–V–I cadential plans; no automatic audio cadence recognition claimed.'},
 {'id':'H08','level':'warning','rule':'Flag changed harmonic states shorter than 8 seconds; this is not a constraint on grains or individual note attacks.'}]
protocol={'version':'1.0','source_revision':'163d5a9d79c12476bbc7fad41ca4f59397ebf66d','source_study_sha256':hashlib.sha256((source/'study.json').read_bytes()).hexdigest(),'scope':'early-period Radio Amor / Mirages / Mort aux Vaches reference protocol, not universal Tim Hecker rules','approval_semantics':'allowed and blocked describe this designed generator; absence from the study is not evidence of artistic prohibition','parameter_status':'all generator ranges, probabilities and limits are design proposals, not learned estimates','families':families,'profiles':profiles,'rules':rules,'unapproved_pending_review':['dominant_seventh_as_functional_cadence','diminished_triad_as_primary_object','fully_diminished_seventh_as_primary_object','augmented_triad_as_primary_object','whole_tone_planing','quartal_stack_with_no_reference_anchor','complete_chromatic_source_cluster'],'generation_policy':{'probability_retain_pitch_object':.30,'probability_parallel_semitone_given_not_retained':.15,'cents_uniform_range':[-4,4],'max_voices':6,'harmonic_state_seconds_are_proposed':True}}
(ROOT/'protocol.json').write_text(json.dumps(protocol,indent=2)+'\n',encoding='utf8')
(ROOT/'corpus_statistics.json').write_text(json.dumps({'method':'duration-weighted interval presence in supported candidate frames; not score-note frequency; medians use frames','source_study_sha256':protocol['source_study_sha256'],'results':stats},indent=2)+'\n',encoding='utf8')
print('Wrote 15 families, 4 profiles, 9 rules, and interval sensitivity statistics.')
