local _,s=reaper.get_action_context();local root=s:gsub('\\','/'):match('^(.*)/Scripts/[^/]+$')..'/'
reaper.Main_OnCommand(40859,0)
for i,name in ipairs({'VST3i: TyrellN6 (u-he)','VST3i: FB-3300 (Full Bucket Music)'})do
 reaper.InsertTrackAtIndex(i-1,true);local tr=reaper.GetTrack(0,i-1);local fx=reaper.TrackFX_AddByName(tr,name,false,-1);assert(fx>=0,name)
 local out=assert(io.open(root..'Audit/plugin_'..i..'.tsv','w'))
 for p=0,reaper.TrackFX_GetNumParams(tr,fx)-1 do local _,n=reaper.TrackFX_GetParamName(tr,fx,p,'');local _,v=reaper.TrackFX_GetFormattedParamValue(tr,fx,p,'');out:write(p..'\t'..n..'\t'..reaper.TrackFX_GetParamNormalized(tr,fx,p)..'\t'..v..'\n')end;out:close()
end
reaper.Main_SaveProjectEx(0,root..'Instrument Laboratory.rpp',8)
