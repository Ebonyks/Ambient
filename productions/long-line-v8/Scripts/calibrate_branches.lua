local _,s=reaper.get_action_context();local root=s:gsub('\\','/'):match('^(.*)/Scripts/[^/]+$')..'/'
local _,name=reaper.EnumProjects(-1,'');assert(name:find('Long Line %- Tonal Revision C.rpp'))
local chunks={};for _,i in ipairs({0,1,2,3,6,7})do local ok,ch=reaper.GetTrackStateChunk(reaper.GetTrack(0,i),'',false);assert(ok);chunks[#chunks+1]=ch end
reaper.Main_OnCommand(40859,0);assert(reaper.CountTracks(0)==0)
local paths={'../long-line-v6/Media/01_Anchor_bypasses_drive.flac','Media/02_Inner_piano.flac','Media/03_Foreground_piano.flac','Media/04_Final_string.flac','../long-line-v6/Media/07_Water.flac','../long-line-v6/Media/08_Wood_air.flac'}
for i,ch in ipairs(chunks)do reaper.InsertTrackAtIndex(i-1,true);local tr=reaper.GetTrack(0,i-1);assert(reaper.SetTrackStateChunk(tr,ch,false));reaper.SetMediaTrackInfo_Value(tr,'D_VOL',1);local it=reaper.GetTrackMediaItem(tr,0);local src=reaper.PCM_Source_CreateFromFile(root..paths[i]);assert(src);reaper.SetMediaItemTake_Source(reaper.GetActiveTake(it),src)end
reaper.SetMediaTrackInfo_Value(reaper.GetMasterTrack(0),'D_VOL',1)
for k,v in pairs({PROJECT_SRATE=48000,PROJECT_SRATE_USE=1,RENDER_SETTINGS=0,RENDER_BOUNDSFLAG=0,RENDER_STARTPOS=43,RENDER_ENDPOS=63,RENDER_TAILFLAG=0,RENDER_CHANNELS=2,RENDER_SRATE=48000,RENDER_NORMALIZE=0})do reaper.GetSetProjectInfo(0,k,v,true)end
reaper.GetSetProjectInfo_String(0,'RENDER_FORMAT','ZXZhdxgAAQ==',true);reaper.GetSetProjectInfo_String(0,'RENDER_FORMAT2','',true);reaper.GetSetProjectInfo_String(0,'RENDER_FILE',root..'Renders',true);reaper.Main_OnCommand(40101,0)
reaper.Main_SaveProjectEx(0,root..'Branch Calibration.rpp',8)
for i=0,5 do
 for j=0,5 do reaper.SetMediaTrackInfo_Value(reaper.GetTrack(0,j),'B_MUTE',j==i and 0 or 1)end
 reaper.GetSetProjectInfo_String(0,'RENDER_PATTERN','Calibration_'..i,true);reaper.Main_OnCommand(42230,0)
end
local f=assert(io.open(root..'Audit/calibration_returned.txt','w'));f:write('Six isolated post-FX branches printed at unity fader for 43-63 seconds.');f:close()
