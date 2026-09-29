local _,s=reaper.get_action_context();local root=s:gsub('\\','/'):match('^(.*)/Scripts/[^/]+$')..'/'
local _,name=reaper.EnumProjects(-1,'');assert(name:find('Branch Calibration.rpp'))
reaper.InsertTrackAtIndex(6,true);local tr=reaper.GetTrack(0,6);local fx=reaper.TrackFX_GetEQ(tr,true);assert(fx>=0)
local out=assert(io.open(root..'Audit/eq_probe.tsv','w'))
for k=0,12 do local ok=reaper.TrackFX_SetNamedConfigParm(tr,fx,'BANDTYPE0',tostring(k));local valid,bt,bi,pt,norm=reaper.TrackFX_GetEQParam(tr,fx,0);out:write(k..'\t'..tostring(ok)..'\t'..tostring(bt)..'\n')end
out:close()
