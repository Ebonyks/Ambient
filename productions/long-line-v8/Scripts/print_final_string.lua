local _,s=reaper.get_action_context();local root=s:gsub('\\','/'):match('^(.*)/Scripts/[^/]+$')..'/'
local prior=io.open(root..'Renders/Physical String - Pink Bed.wav','rb');assert(not prior,'Existing source print preserved')
reaper.Main_OnCommand(40859,0);assert(reaper.CountTracks(0)==0);reaper.SetCurrentBPM(0,60,true);reaper.InsertTrackAtIndex(0,true)
local tr=reaper.GetTrack(0,0);reaper.SetMediaTrackInfo_Value(tr,'D_VOL',100);reaper.GetSetMediaTrackInfo_String(tr,'P_NAME','Physical string | no vibrato, no detune',true);local fx=reaper.TrackFX_AddByName(tr,'VST3: Surge XT (Surge Synth Team)',false,-1);assert(fx==0)
reaper.TrackFX_SetParamNormalized(tr,fx,256,.8);reaper.TrackFX_SetParamNormalized(tr,fx,317,.06)
local start=reaper.time_precise()
local function build()
 if reaper.time_precise()-start<.8 then reaper.defer(build);return end
 local settings={[12]=.72,[234]=0,[259]=.56,[260]=.24,[261]=.64,[262]=.80,[263]=.5,[264]=0,[265]=.18,[319]=.57,[320]=.05,[329]=.55,[331]=.73,[333]=.62,[334]=.63,[230]=0}
 for p,v in pairs(settings)do reaper.TrackFX_SetParamNormalized(tr,fx,p,v)end
 local it=reaper.CreateNewMIDIItemInProj(tr,0,336,false);local take=reaper.GetActiveTake(it)
 local notes=dofile(root..'Scripts/string_notes.lua');for _,n in ipairs(notes)do reaper.MIDI_InsertNote(take,false,false,reaper.MIDI_GetPPQPosFromProjTime(take,n[1]),reaper.MIDI_GetPPQPosFromProjTime(take,n[2]-.25),0,n[3],n[4],true)end;reaper.MIDI_Sort(take)
 reaper.GetSetProjectInfo(0,'PROJECT_SRATE',48000,true);reaper.GetSetProjectInfo(0,'PROJECT_SRATE_USE',1,true);reaper.GetSetProjectInfo(0,'RENDER_SETTINGS',0,true);reaper.GetSetProjectInfo(0,'RENDER_BOUNDSFLAG',0,true);reaper.GetSetProjectInfo(0,'RENDER_STARTPOS',0,true);reaper.GetSetProjectInfo(0,'RENDER_ENDPOS',336,true);reaper.GetSetProjectInfo(0,'RENDER_TAILFLAG',0,true);reaper.GetSetProjectInfo(0,'RENDER_CHANNELS',2,true);reaper.GetSetProjectInfo(0,'RENDER_SRATE',48000,true);reaper.GetSetProjectInfo(0,'RENDER_NORMALIZE',0,true)
 reaper.GetSetProjectInfo_String(0,'RENDER_FORMAT','ZXZhdxgAAQ==',true);reaper.GetSetProjectInfo_String(0,'RENDER_FORMAT2','',true);reaper.GetSetProjectInfo_String(0,'RENDER_FILE',root..'Renders',true);reaper.GetSetProjectInfo_String(0,'RENDER_PATTERN','Physical String - Pink Bed',true)
 local out=assert(io.open(root..'Audit/string_patch_final.tsv','w'));for p,v in pairs(settings)do local _,n=reaper.TrackFX_GetParamName(tr,fx,p,'');local _,val=reaper.TrackFX_GetFormattedParamValue(tr,fx,p,'');out:write(p..'\t'..n..'\t'..v..'\t'..val..'\n')end;out:close()
 reaper.Main_SaveProjectEx(0,root..'Physical String - Pink Bed.rpp',8);reaper.Main_OnCommand(42230,0)
 local f=assert(io.open(root..'Audit/string_final_returned.txt','w'));f:write('Native source print returned. Verify WAV independently.');f:close()
end
reaper.defer(build)
