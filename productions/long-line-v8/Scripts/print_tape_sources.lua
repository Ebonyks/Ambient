local _,s=reaper.get_action_context();local root=s:gsub('\\','/'):match('^(.*)/Scripts/[^/]+$')..'/'
local _,name=reaper.EnumProjects(-1,'');assert(name:find('Long Line %- Tonal Revision D.rpp'))
local chunks={};for i=1,3 do local ok,ch=reaper.GetTrackStateChunk(reaper.GetTrack(0,i),'',false);assert(ok);chunks[#chunks+1]=ch end
reaper.Main_OnCommand(40859,0);assert(reaper.CountTracks(0)==0);reaper.SetCurrentBPM(0,60,true)
local paths={'02_Inner_piano','03_Foreground_piano','04_Final_string'};local gains=dofile(root..'Scripts/input_gains.lua')
for i,ch in ipairs(chunks)do reaper.InsertTrackAtIndex(i-1,true);local tr=reaper.GetTrack(0,i-1);assert(reaper.SetTrackStateChunk(tr,ch,false));reaper.SetMediaTrackInfo_Value(tr,'D_VOL',1);local it=reaper.GetTrackMediaItem(tr,0);local take=reaper.GetActiveTake(it);local src=reaper.PCM_Source_CreateFromFile(root..'Media/'..paths[i]..'.flac');assert(src);reaper.SetMediaItemTake_Source(take,src);reaper.SetMediaItemTakeInfo_Value(take,'D_VOL',gains[i])end
reaper.SetMediaTrackInfo_Value(reaper.GetMasterTrack(0),'D_VOL',1)
for k,v in pairs({PROJECT_SRATE=48000,PROJECT_SRATE_USE=1,RENDER_SETTINGS=0,RENDER_BOUNDSFLAG=0,RENDER_STARTPOS=0,RENDER_ENDPOS=336,RENDER_TAILFLAG=0,RENDER_CHANNELS=2,RENDER_SRATE=48000,RENDER_NORMALIZE=0})do reaper.GetSetProjectInfo(0,k,v,true)end
reaper.GetSetProjectInfo_String(0,'RENDER_FORMAT','ZXZhdxgAAQ==',true);reaper.GetSetProjectInfo_String(0,'RENDER_FORMAT2','',true);reaper.GetSetProjectInfo_String(0,'RENDER_FILE',root..'Renders',true);reaper.Main_OnCommand(40101,0)
reaper.Main_SaveProjectEx(0,root..'Calibrated Tape Sources.rpp',8)
for i=0,2 do
 for j=0,2 do reaper.SetMediaTrackInfo_Value(reaper.GetTrack(0,j),'B_MUTE',j==i and 0 or 1)end
 reaper.GetSetProjectInfo_String(0,'RENDER_PATTERN','Calibrated_Tape_'..i,true);reaper.Main_OnCommand(42230,0)
end
for j=0,2 do reaper.SetMediaTrackInfo_Value(reaper.GetTrack(0,j),'B_MUTE',0)end
local f=assert(io.open(root..'Audit/tape_prints_returned.txt','w'));f:write('Native source processing returned: three separately printed 336-second branches at calibrated input level.');f:close()
