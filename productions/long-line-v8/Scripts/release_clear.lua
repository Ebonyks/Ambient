local _,s=reaper.get_action_context();local root=s:gsub('\\','/'):match('^(.*)/Scripts/[^/]+$')..'/'
local _,name=reaper.EnumProjects(-1,'');assert(name:find('Long Line %- Tonal Revision.rpp'))
local tr=reaper.GetTrack(0,8);local _,n=reaper.TrackFX_GetParamName(tr,0,5,'');assert(n=='Clear');reaper.TrackFX_SetParamNormalized(tr,0,5,0)
reaper.GetSetProjectInfo_String(0,'RENDER_PATTERN','Long Line - Tonal Revision B',true);reaper.Main_OnCommand(40101,0)
reaper.Main_SaveProjectEx(0,root..'Long Line - Tonal Revision B.rpp',8);reaper.Main_OnCommand(42230,0)
local f=assert(io.open(root..'Audit/revision_b.txt','w'));f:write('Supermassive Clear explicitly released to 0; other settings as final_fx_parameters.tsv. Native render returned.');f:close()
