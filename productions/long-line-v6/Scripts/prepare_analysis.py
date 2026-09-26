from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];a=R/'Scripts/analysis/audio_analysis';a.mkdir(parents=True,exist_ok=True);(a/'features').mkdir(exist_ok=True)
rows=[]
for num,file,title in [(5,'baseline_22050.flac','Revision 5 baseline'),(8,'full_draft_22050.flac','Full-length final study draft')]:
 p=R/'Audit/audio_inputs'/file
 rows.append({'album':'long_line','track_num':num,'title':title,'duration':112 if num==5 else 336,'page':'original user composition; no reference-artist audio','stream_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source_quality':'lossless 22050 Hz analysis-input FLAC, derived from 48 kHz 24-bit native REAPER WAV','analysis_wav_path':str(p)})
(a/'manifest.json').write_text(json.dumps(rows,indent=2));print('Configured bundled baseline/final inputs. Existing feature files are cached by the original extractor; use a fresh analysis directory when changing parameters.')
