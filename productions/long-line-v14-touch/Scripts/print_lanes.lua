local _,s=reaper.get_action_context();local root=s:gsub('\\','/'):match('^(.*)/Scripts/[^/]+$')..'/'
local target=nil;for i=0,60 do local p,n=reaper.EnumProjects(i,'');if not p then break end;if n:gsub('\\','/'):find(root..'Texture Instruments.rpp',1,true)then target=p;break end end;assert(target);reaper.SelectProjectInstance(target)
for i=0,3 do
 assert(not io.open(root..'Renders/Inner lane '..i..'.wav','rb'),'Existing stem preserved')
 for j=0,3 do reaper.SetMediaTrackInfo_Value(reaper.GetTrack(0,j),'B_MUTE',i==j and 0 or 1)end
 reaper.GetSetProjectInfo_String(0,'RENDER_PATTERN','Inner lane '..i,true);reaper.Main_OnCommand(42230,0)
end
for j=0,3 do reaper.SetMediaTrackInfo_Value(reaper.GetTrack(0,j),'B_MUTE',0)end
reaper.GetSetProjectInfo_String(0,'RENDER_PATTERN','Inner texture native',true);reaper.Main_SaveProjectEx(0,root..'Texture Instruments.rpp',8)
local f=assert(io.open(root..'Audit/lanes_returned.txt','w'));f:write('Four individual native instrument prints returned');f:close()
