local _,s=reaper.get_action_context();local root=s:gsub('\\','/'):match('^(.*)/Scripts/[^/]+$')..'/'
local target=nil
for i=0,40 do local p,name=reaper.EnumProjects(i,'');if not p then break end;if name:find('Physical String Source %- High Resolution.rpp') then target=p;break end end
assert(target);local tr=reaper.GetTrack(target,0);local old=reaper.TrackFX_GetParamNormalized(tr,0,259);local out=assert(io.open(root..'Audit/exciters.tsv','w'));local last=''
for j=0,100 do local v=j/100;reaper.TrackFX_SetParamNormalized(tr,0,259,v);local _,n=reaper.TrackFX_GetFormattedParamValue(tr,0,259,'');if n~=last then out:write(v..'\t'..n..'\n');last=n end end
reaper.TrackFX_SetParamNormalized(tr,0,259,old);out:close()
