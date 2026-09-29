local _,s=reaper.get_action_context();local root=s:gsub('\\','/'):match('^(.*)/Scripts/[^/]+$')..'/'
local _,name=reaper.EnumProjects(-1,'');assert(name:find('Plugin Laboratory.rpp'))
local out=assert(io.open(root..'Audit/plugin_modes.tsv','w'))
local function enum(track,param,label)
 local tr=reaper.GetTrack(0,track);local prev=''
 for step=0,1000 do local v=step/1000;reaper.TrackFX_SetParamNormalized(tr,0,param,v);local _,text=reaper.TrackFX_GetFormattedParamValue(tr,0,param,'');if text~=prev then out:write(label..'\t'..v..'\t'..text..'\n');prev=text end end
end
enum(0,12,'FX');enum(1,256,'OSC');enum(1,317,'FILTER')
out:close()
