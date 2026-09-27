local _,s=reaper.get_action_context();local root=s:gsub('\\','/'):match('^(.*)/Scripts/[^/]+$')..'/'
local _,name=reaper.EnumProjects(-1,'');assert(name:find('Plugin Laboratory.rpp'))
local types={{'Tape',.78},{'Nimbus',.745},{'Reverb2',.35},{'Airwindows',.46}}
for i,pair in ipairs(types)do reaper.InsertTrackAtIndex(i+1,true);local tr=reaper.GetTrack(0,i+1);local fx=reaper.TrackFX_AddByName(tr,'VST3: Surge XT Effects (Surge Synth Team)',false,-1);assert(fx==0);reaper.TrackFX_SetParamNormalized(tr,0,12,pair[2]);reaper.GetSetMediaTrackInfo_String(tr,'P_NAME',pair[1],true)end
reaper.TrackFX_SetParamNormalized(reaper.GetTrack(0,1),0,256,.80);reaper.TrackFX_SetParamNormalized(reaper.GetTrack(0,1),0,317,.03)
local start=reaper.time_precise()
local function done()
 if reaper.time_precise()-start<1 then reaper.defer(done);return end
 local out=assert(io.open(root..'Audit/settled_parameters.tsv','w'))
 for i=1,5 do local tr=reaper.GetTrack(0,i);local _,n=reaper.GetTrackName(tr);out:write('TRACK\t'..i..'\t'..n..'\n')
 for j=0,reaper.TrackFX_GetNumParams(tr,0)-1 do if i>1 or (j>=256 and j<=344)then local _,n=reaper.TrackFX_GetParamName(tr,0,j,'');local _,v=reaper.TrackFX_GetFormattedParamValue(tr,0,j,'');out:write(j..'\t'..n..'\t'..reaper.TrackFX_GetParamNormalized(tr,0,j)..'\t'..v..'\n')end end end
 out:close();reaper.Main_SaveProjectEx(0,root..'Plugin Laboratory.rpp',8)
end
reaper.defer(done)
