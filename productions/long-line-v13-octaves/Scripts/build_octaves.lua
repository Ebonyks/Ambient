local _,s=reaper.get_action_context();local root=s:gsub('\\','/'):match('^(.*)/Scripts/[^/]+$')..'/'
assert(not io.open(root..'Renders/Long Line - Upper Octaves.wav','rb'),'Existing render preserved')
for _,n in ipairs({'01_Nature_bed.flac','06_Inner_texture.flac'})do assert(io.open(root..'Media/'..n,'rb'),'Missing media')end
reaper.Main_OnCommand(40859,0);reaper.SetCurrentBPM(0,60,true)
for i,n in ipairs({'01_Nature_bed.flac','06_Inner_texture.flac'})do
 reaper.InsertTrackAtIndex(i-1,true);local tr=reaper.GetTrack(0,i-1);reaper.GetSetMediaTrackInfo_String(tr,'P_NAME',i==1 and 'Quiet water and wood; old melodic scaffold excluded' or 'Four differentiated fast lines',true)
 local it=reaper.AddMediaItemToTrack(tr);local tk=reaper.AddTakeToMediaItem(it);reaper.SetMediaItemTake_Source(tk,reaper.PCM_Source_CreateFromFile(root..'Media/'..n));reaper.SetMediaItemTakeInfo_Value(tk,'D_VOL',i==1 and 1 or 1.26);reaper.SetMediaItemInfo_Value(it,'D_LENGTH',96);reaper.SetMediaItemInfo_Value(it,'D_FADEINLEN',2);reaper.SetMediaItemInfo_Value(it,'D_FADEOUTLEN',3)
 reaper.SetMediaTrackInfo_Value(tr,'D_VOL',i==1 and .35 or 0.7936507936507936)
end
local tr=reaper.GetTrack(0,1);local fx=reaper.TrackFX_AddByName(tr,'VST3: Surge XT Effects (Surge Synth Team)',false,-1);assert(fx>=0);reaper.TrackFX_SetParamNormalized(tr,fx,12,.35)
local tape=reaper.TrackFX_AddByName(tr,'VST3: Surge XT Effects (Surge Synth Team)',false,-1);assert(tape>=0);reaper.TrackFX_SetParamNormalized(tr,tape,12,.78)
local start=reaper.time_precise();local function done()
 if reaper.time_precise()-start<1 then reaper.defer(done);return end
 for p,v in pairs({[0]=.25,[1]=.4,[2]=.48,[3]=.82,[4]=.65,[5]=0,[6]=.45,[7]=.72,[8]=.5,[9]=.16})do reaper.TrackFX_SetParamNormalized(tr,fx,p,v)end
 for p,v in pairs({[0]=.34,[1]=.38,[2]=.5,[3]=.40,[4]=.286,[5]=.05,[6]=.025,[7]=.025,[8]=0,[9]=0,[10]=0,[11]=.75})do reaper.TrackFX_SetParamNormalized(tr,tape,p,v)end
 reaper.TrackFX_CopyToTrack(tr,tape,tr,0,true)
 local eq=reaper.TrackFX_AddByName(tr,'VST: ReaEQ (Cockos)',false,-1);assert(eq>=0)
 assert(reaper.TrackFX_SetEQParam(tr,eq,2,0,0,350,false));assert(reaper.TrackFX_SetEQParam(tr,eq,2,0,1,10^(-5/20),false));assert(reaper.TrackFX_SetEQParam(tr,eq,2,0,2,2.2,false))
 local eqlog=assert(io.open(root..'Audit/octaves_eq.tsv','w'));for p=0,reaper.TrackFX_GetNumParams(tr,eq)-1 do local _,name=reaper.TrackFX_GetParamName(tr,eq,p,'');local _,val=reaper.TrackFX_GetFormattedParamValue(tr,eq,p,'');eqlog:write(p..'\t'..name..'\t'..val..'\n')end;eqlog:close()
 local audit=assert(io.open(root..'Audit/octaves_effects.tsv','w'));for f=0,reaper.TrackFX_GetCount(tr)-1 do for p=0,12 do local _,name=reaper.TrackFX_GetParamName(tr,f,p,'');local _,val=reaper.TrackFX_GetFormattedParamValue(tr,f,p,'');audit:write(f..'\t'..p..'\t'..name..'\t'..val..'\n')end end;audit:close()
 reaper.SetMediaTrackInfo_Value(reaper.GetMasterTrack(0),'D_VOL',.86)
 for k,v in pairs({PROJECT_SRATE=48000,PROJECT_SRATE_USE=1,RENDER_SETTINGS=0,RENDER_BOUNDSFLAG=0,RENDER_STARTPOS=0,RENDER_ENDPOS=96,RENDER_TAILFLAG=0,RENDER_CHANNELS=2,RENDER_SRATE=48000,RENDER_NORMALIZE=0})do reaper.GetSetProjectInfo(0,k,v,true)end
 reaper.GetSetProjectInfo_String(0,'RENDER_FORMAT','ZXZhdxgAAQ==',true);reaper.GetSetProjectInfo_String(0,'RENDER_FILE',root..'Renders',true);reaper.GetSetProjectInfo_String(0,'RENDER_PATTERN','Long Line - Upper Octaves',true)
 reaper.Main_SaveProjectEx(0,root..'Long Line - Upper Octaves.rpp',8);reaper.Main_OnCommand(42230,0)
 local f=assert(io.open(root..'Audit/octaves_returned.txt','w'));f:write('Native demo render returned');f:close()
end;reaper.defer(done)
