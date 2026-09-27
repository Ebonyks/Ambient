local _,s=reaper.get_action_context();local root=s:gsub('\\','/'):match('^(.*)/Scripts/[^/]+$')..'/'
local target=nil;for i=0,50 do local p,name=reaper.EnumProjects(i,'');if not p then break end;if name:find('Calibrated Tape Sources.rpp')then target=p;break end end;assert(target);reaper.SelectProjectInstance(target)
reaper.SetMediaTrackInfo_Value(reaper.GetMasterTrack(0),'D_VOL',.125)
for i=0,2 do reaper.SetMediaTrackInfo_Value(reaper.GetTrack(0,i),'B_MUTE',i==2 and 0 or 1)end
reaper.GetSetProjectInfo_String(0,'RENDER_PATTERN','Calibrated_Tape_2_safe',true);reaper.Main_OnCommand(40101,0);reaper.Main_OnCommand(42230,0)
for i=0,2 do reaper.SetMediaTrackInfo_Value(reaper.GetTrack(0,i),'B_MUTE',0)end
reaper.Main_SaveProjectEx(0,root..'Calibrated Tape Sources.rpp',8)
local f=assert(io.open(root..'Audit/safe_tape_print.txt','w'));f:write('String tape branch reprinted with 0.125 post-FX master gain. First clipped export rejected. Source processor project now retains this export headroom.');f:close()
