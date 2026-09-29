local _,script=reaper.get_action_context();local root=script:gsub('\\','/'):match('^(.*)/Scripts/[^/]+$')..'/'
local prior=io.open(root..'Renders/Long Line - Moving Voices - 5m36.wav','rb');if prior then prior:close();error('Existing render preserved. Choose a new render/project filename before rebuilding.')end
reaper.Main_OnCommand(40859,0);assert(reaper.CountTracks(0)==0)
for i=0,8 do reaper.InsertTrackAtIndex(i,true)end
local file=assert(io.open(root..'../long-line-v6/Scripts/ambience_bus.RTrackTemplate','r'));local ch=file:read('*a');file:close()
ch=ch:gsub('\n%s*AUXRECV[^\n]*','');assert(reaper.SetTrackStateChunk(reaper.GetTrack(0,8),ch,false));reaper.SetCurrentBPM(0,60,true)
local stems={'01_Anchor_bypasses_drive','02_Moving_inner_voices','03_Developing_foreground','04_Eroded_melodic_return','05_Independent_distorted_body','06_Source_residue','07_Water','08_Wood_air'}
local bus=reaper.GetTrack(0,8)
local function flat_env(tr)
 local e=reaper.GetTrackEnvelopeByName(tr,'Volume')
 if not e then local ok,ch=reaper.GetTrackStateChunk(tr,'',false);assert(ok);ch=ch:gsub('>%s*$','<VOLENV2\nACT 1 -1\nVIS 0 1 1\nLANEHEIGHT 45 0\nARM 0\nDEFSHAPE 0 -1 -1\nPT 0 1 0\n>\n>\n');assert(reaper.SetTrackStateChunk(tr,ch,false));e=reaper.GetTrackEnvelopeByName(tr,'Volume')end
 assert(e);reaper.DeleteEnvelopePointRange(e,-1,1000);reaper.InsertEnvelopePoint(e,0,1,0,0,false,true);reaper.Envelope_SortPoints(e)
end
for i=0,7 do
 local tr=reaper.GetTrack(0,i);local item=reaper.AddMediaItemToTrack(tr);local take=reaper.AddTakeToMediaItem(item);local src=reaper.PCM_Source_CreateFromFile(root..((i==0 or i==6 or i==7) and '../long-line-v6/Media/' or 'Media/')..stems[i+1]..'.flac');assert(src);reaper.SetMediaItemTake_Source(take,src)
 reaper.SetMediaItemInfo_Value(item,'D_POSITION',0);reaper.SetMediaItemInfo_Value(item,'D_LENGTH',336);reaper.SetMediaItemInfo_Value(item,'C_BEATATTACHMODE',0);reaper.SetMediaItemInfo_Value(item,'B_LOOPSRC',0)
 reaper.SetMediaItemTakeInfo_Value(take,'D_STARTOFFS',0);reaper.SetMediaItemTakeInfo_Value(take,'D_PLAYRATE',1);reaper.SetMediaTrackInfo_Value(tr,'D_VOL',1);reaper.SetMediaTrackInfo_Value(tr,'B_MUTE',0);reaper.SetMediaTrackInfo_Value(tr,'I_SOLO',0)
 reaper.GetSetMediaTrackInfo_String(tr,'P_NAME',stems[i+1],true);flat_env(tr)
 for j=reaper.GetTrackNumSends(tr,0)-1,0,-1 do reaper.RemoveTrackSend(tr,0,j)end
 local send=reaper.CreateTrackSend(tr,bus);reaper.SetTrackSendInfo_Value(tr,0,send,'D_VOL',({.04,.16,.18,.18,.10,.2,.025,.025})[i+1])
end
flat_env(bus);reaper.SetMediaTrackInfo_Value(bus,'D_VOL',.28);reaper.GetSetMediaTrackInfo_String(bus,'P_NAME','09 Shared distance | post-branch ambience',true)
local f=reaper.GetFXEnvelope(bus,0,6,true);reaper.DeleteEnvelopePointRange(f,-1,1000);for _,v in ipairs({{0,.48},{318,.48},{327,.6},{332,.53},{336,.44}})do reaper.InsertEnvelopePoint(f,v[1],v[2],0,0,false,true)end;reaper.Envelope_SortPoints(f)
local e=reaper.GetTrackEnvelopeByName(bus,'Volume');for _,v in ipairs({{327,1},{331,.7},{334,.25},{336,0}})do reaper.InsertEnvelopePoint(e,v[1],v[2],0,0,false,true)end;reaper.Envelope_SortPoints(e)
reaper.SetMediaTrackInfo_Value(reaper.GetMasterTrack(0),'D_VOL',2.2)
local _,nm,nr=reaper.CountProjectMarkers(0);for i=nm+nr-1,0,-1 do reaper.DeleteProjectMarkerByIndex(0,i)end
for _,v in ipairs({{0,70,'I | D field - staggered moving voices'},{70,112,'II | B beneath retained F# and A'},{112,160,'III | G - retained F# and D'},{160,208,'IV | C / B - stable distant friction'},{208,252,'V | E - G and B persist'},{252,294,'VI | G minor - D remains'},{294,336,'VII | D return - melodic completion'}})do reaper.AddProjectMarker2(0,true,v[1],v[2],v[3],-1,0)end
reaper.GetSetProjectInfo(0,'PROJECT_SRATE',48000,true);reaper.GetSetProjectInfo(0,'PROJECT_SRATE_USE',1,true);reaper.GetSetProjectInfo(0,'RENDER_SETTINGS',0,true);reaper.GetSetProjectInfo(0,'RENDER_BOUNDSFLAG',0,true);reaper.GetSetProjectInfo(0,'RENDER_STARTPOS',0,true);reaper.GetSetProjectInfo(0,'RENDER_ENDPOS',336,true);reaper.GetSetProjectInfo(0,'RENDER_TAILFLAG',0,true);reaper.GetSetProjectInfo(0,'RENDER_CHANNELS',2,true);reaper.GetSetProjectInfo(0,'RENDER_SRATE',48000,true);reaper.GetSetProjectInfo(0,'RENDER_NORMALIZE',0,true)
reaper.GetSetProjectInfo_String(0,'RENDER_FORMAT','ZXZhdxgAAQ==',true);reaper.GetSetProjectInfo_String(0,'RENDER_FORMAT2','',true);reaper.GetSetProjectInfo_String(0,'RENDER_FILE',root..'Renders',true);reaper.GetSetProjectInfo_String(0,'RENDER_PATTERN','Long Line - Moving Voices - 5m36',true)
reaper.GetSetProjectNotes(0,true,'LONG LINE v7 | Moving voices. Original motif grammar and staggered local revoicing, slower harmonic fields retained. See weave.json, tools/melodic_weave and Audit/comparison.json. Source palette inherited from v6; shorter envelopes. Protocol compliance is not artist similarity.\n')
local function env(i,points)
 local tr=reaper.GetTrack(0,i);local e=reaper.GetTrackEnvelopeByName(tr,'Volume');assert(e);reaper.DeleteEnvelopePointRange(e,-1,1000)
 for _,v in ipairs(points)do reaper.InsertEnvelopePoint(e,v[1],v[2],0,0,false,true)end;reaper.Envelope_SortPoints(e)
end
-- Exchange clean body for its own returns; no extra harmonic voices, no phrase gates.
env(1,{{0,1},{142,1},{162,.84},{202,.74},{220,.7},{240,.7},{265,.84},{292,1},{336,1}})
env(3,{{0,1},{142,1},{162,1.4},{202,1.7},{220,1.8},{240,1.8},{265,1.35},{292,1},{336,1}})
env(4,{{0,1},{142,1},{162,1.35},{202,1.8},{220,2},{240,2},{265,1.4},{292,1},{336,1}})
reaper.Main_OnCommand(40101,0)
local receipt=io.open(root..'Audit/reaper_receipt.txt','w')
for i=0,7 do local tr=reaper.GetTrack(0,i);local src=reaper.GetMediaItemTake_Source(reaper.GetActiveTake(reaper.GetTrackMediaItem(tr,0)));local n=reaper.GetMediaSourceLength(src);assert(math.abs(n-336)<.001);receipt:write(stems[i+1]..' '..n..' seconds\n')end;receipt:close()
reaper.Main_SaveProjectEx(0,root..'Long Line - Moving Voices.rpp',8)
reaper.Main_OnCommand(42230,0)
local check=assert(io.open(root..'Audit/render_complete.txt','w'));check:write('Native REAPER render action returned; verify WAV independently.');check:close()
