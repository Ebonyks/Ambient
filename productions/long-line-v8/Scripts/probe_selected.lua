local _,s=reaper.get_action_context();local root=s:gsub('\\','/'):match('^(.*)/Scripts/[^/]+$')..'/'
local _,name=reaper.EnumProjects(-1,'');assert(name:find('Plugin Laboratory.rpp'))
local out=assert(io.open(root..'Audit/selected_parameters.tsv','w'))
local function dump(tr,label)
 out:write('PLUGIN\t'..label..'\n');for j=0,reaper.TrackFX_GetNumParams(tr,0)-1 do
 if label:find('FX') or (j>=228 and j<=344) then local _,n=reaper.TrackFX_GetParamName(tr,0,j,'');local _,v=reaper.TrackFX_GetFormattedParamValue(tr,0,j,'');out:write(j..'\t'..n..'\t'..reaper.TrackFX_GetParamNormalized(tr,0,j)..'\t'..v..'\n')end end
end
for _,pair in ipairs({{'Tape',.78},{'Nimbus',.745},{'Airwindows',.46},{'Reverb2',.35}})do
 local tr=reaper.GetTrack(0,0);reaper.TrackFX_SetParamNormalized(tr,0,12,pair[2]);dump(tr,'FX '..pair[1])
end
for _,pair in ipairs({{'String',.80},{'Twist',.90},{'Sine',.08}})do
 local tr=reaper.GetTrack(0,1);reaper.TrackFX_SetParamNormalized(tr,0,256,pair[2]);dump(tr,pair[1])
end
out:close()
