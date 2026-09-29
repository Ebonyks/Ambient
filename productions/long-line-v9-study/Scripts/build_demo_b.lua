local _,s=reaper.get_action_context();local root=s:gsub('\\','/'):match('^(.*)/Scripts/[^/]+$')..'/'
assert(not io.open(root..'Renders/Long Line - Inner Detail B.wav','rb'),'Existing render preserved')
for _,n in ipairs({'01_v8_scaffold_excerpt.flac','06_Inner_texture.flac'})do assert(io.open(root..'Media/'..n,'rb'),'Missing media')end
reaper.Main_OnCommand(40859,0);reaper.SetCurrentBPM(0,60,true)
for i,n in ipairs({'01_v8_scaffold_excerpt.flac','06_Inner_texture.flac'})do
 reaper.InsertTrackAtIndex(i-1,true);local tr=reaper.GetTrack(0,i-1);reaper.GetSetMediaTrackInfo_String(tr,'P_NAME',i==1 and 'Original v8 scaffold (2:20-3:56)' or 'Four interlocking inner strands',true)
 local it=reaper.AddMediaItemToTrack(tr);local tk=reaper.AddTakeToMediaItem(it);reaper.SetMediaItemTake_Source(tk,reaper.PCM_Source_CreateFromFile(root..'Media/'..n));reaper.SetMediaItemInfo_Value(it,'D_LENGTH',96);reaper.SetMediaItemInfo_Value(it,'D_FADEINLEN',2);reaper.SetMediaItemInfo_Value(it,'D_FADEOUTLEN',3)
 reaper.SetMediaTrackInfo_Value(tr,'D_VOL',i==1 and .92 or .45)
end
local tr=reaper.GetTrack(0,1);local fx=reaper.TrackFX_AddByName(tr,'VST3: Surge XT Effects (Surge Synth Team)',false,-1);assert(fx>=0);reaper.TrackFX_SetParamNormalized(tr,fx,12,.35)
local start=reaper.time_precise();local function done()
 if reaper.time_precise()-start<1 then reaper.defer(done);return end
 for p,v in pairs({[0]=.25,[1]=.4,[2]=.44,[3]=.82,[4]=.65,[5]=0,[6]=.45,[7]=.72,[8]=.5,[9]=.28})do reaper.TrackFX_SetParamNormalized(tr,fx,p,v)end
 for k,v in pairs({PROJECT_SRATE=48000,PROJECT_SRATE_USE=1,RENDER_SETTINGS=0,RENDER_BOUNDSFLAG=0,RENDER_STARTPOS=0,RENDER_ENDPOS=96,RENDER_TAILFLAG=0,RENDER_CHANNELS=2,RENDER_SRATE=48000,RENDER_NORMALIZE=0})do reaper.GetSetProjectInfo(0,k,v,true)end
 reaper.GetSetProjectInfo_String(0,'RENDER_FORMAT','ZXZhdxgAAQ==',true);reaper.GetSetProjectInfo_String(0,'RENDER_FILE',root..'Renders',true);reaper.GetSetProjectInfo_String(0,'RENDER_PATTERN','Long Line - Inner Detail B',true)
 reaper.Main_SaveProjectEx(0,root..'Long Line - Inner Detail B.rpp',8);reaper.Main_OnCommand(42230,0)
 local f=assert(io.open(root..'Audit/demo_B_returned.txt','w'));f:write('Native demo render returned');f:close()
end;reaper.defer(done)
