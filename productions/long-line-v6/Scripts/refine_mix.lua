local _,script=reaper.get_action_context();local root=script:gsub('\\','/'):match('^(.*)/Scripts/[^/]+$')..'/'
local _,p=reaper.EnumProjects(-1,'');assert(p:find('Full Length'));assert(reaper.CountTracks(0)==9);reaper.Main_OnCommand(40101,0)
local function env(i,points)
 local tr=reaper.GetTrack(0,i);local e=reaper.GetTrackEnvelopeByName(tr,'Volume');assert(e);reaper.DeleteEnvelopePointRange(e,-1,1000)
 for _,v in ipairs(points)do reaper.InsertEnvelopePoint(e,v[1],v[2],0,0,false,true)end;reaper.Envelope_SortPoints(e)
end
-- Exchange clean body for its own returns; no extra harmonic voices, no phrase gates.
env(1,{{0,1},{142,1},{162,.84},{202,.74},{220,.7},{240,.7},{265,.84},{292,1},{336,1}})
env(3,{{0,1},{142,1},{162,1.4},{202,1.7},{220,1.8},{240,1.8},{265,1.35},{292,1},{336,1}})
env(4,{{0,1},{142,1},{162,1.35},{202,1.8},{220,2},{240,2},{265,1.4},{292,1},{336,1}})
reaper.GetSetProjectInfo_String(0,'RENDER_PATTERN','Long Line - Full Length - Refined - 5m36',true)
local ok,ch=reaper.GetTrackStateChunk(reaper.GetTrack(0,8),'',false);assert(ok);local f=io.open(root..'Scripts/ambience_bus.RTrackTemplate','w');f:write(ch);f:close()
for i=0,8 do local ok,ch=reaper.GetTrackStateChunk(reaper.GetTrack(0,i),'',false);assert(ok);local f=io.open(root..'Audit/track_'..i..'.RTrackTemplate','w');f:write(ch);f:close()end
reaper.Main_SaveProjectEx(0,root..'Long Line - Full Length.rpp',8);reaper.Main_OnCommand(42230,0);reaper.Main_SaveProjectEx(0,root..'Long Line - Full Length.rpp',8)
