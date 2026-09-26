local _,script=reaper.get_action_context();local root=script:gsub('\\','/'):match('^(.*)/Scripts/[^/]+$')..'/'
local _,p=reaper.EnumProjects(-1,'');assert(p:find('Full Length'));reaper.Main_OnCommand(40101,0)
for _,v in ipairs({{2,'03_Pitched_motif_coda'},{3,'04_Eroded_motif_coda'}})do local item=reaper.GetTrackMediaItem(reaper.GetTrack(0,v[1]),0);local take=reaper.GetActiveTake(item);local src=reaper.PCM_Source_CreateFromFile(root..'Media/'..v[2]..'.flac');assert(src);reaper.SetMediaItemTake_Source(take,src)end
reaper.GetSetProjectInfo_String(0,'RENDER_PATTERN','Long Line - Full Length - Study Draft - 5m36',true)
reaper.Main_SaveProjectEx(0,root..'Long Line - Full Length.rpp',8);reaper.Main_OnCommand(42230,0);reaper.Main_SaveProjectEx(0,root..'Long Line - Full Length.rpp',8)
