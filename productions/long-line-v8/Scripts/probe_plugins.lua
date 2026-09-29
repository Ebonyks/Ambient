local _,s=reaper.get_action_context();local root=s:gsub('\\','/'):match('^(.*)/Scripts/[^/]+$')..'/'
reaper.Main_OnCommand(40859,0);assert(reaper.CountTracks(0)==0)
local out=assert(io.open(root..'Audit/plugin_probe.tsv','w'))
for i,name in ipairs({'VST3: Surge XT Effects (Surge Synth Team)','VST3: Surge XT (Surge Synth Team)'})do
 reaper.InsertTrackAtIndex(i-1,true);local tr=reaper.GetTrack(0,i-1);local fx=reaper.TrackFX_AddByName(tr,name,false,-1);out:write('PLUGIN\t'..name..'\t'..fx..'\n')
 if fx>=0 then
  for j=0,reaper.TrackFX_GetNumParams(tr,fx)-1 do local _,n=reaper.TrackFX_GetParamName(tr,fx,j,'');local _,v=reaper.TrackFX_GetFormattedParamValue(tr,fx,j,'');out:write(j..'\t'..n..'\t'..reaper.TrackFX_GetParamNormalized(tr,fx,j)..'\t'..v..'\n')end
 end
end
out:close();reaper.Main_SaveProjectEx(0,root..'Plugin Laboratory.rpp',8)
