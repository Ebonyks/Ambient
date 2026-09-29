local _,s=reaper.get_action_context();local root=s:gsub('\\','/'):match('^(.*)/Scripts/[^/]+$')..'/'
local prior=io.open(root..'Renders/Long Line - Tonal Revision A.wav','rb');assert(not prior,'Existing mix preserved')
reaper.Main_OnCommand(40859,0);assert(reaper.CountTracks(0)==0);reaper.SetCurrentBPM(0,60,true)
local names={'01 Anchor','02 Inner piano | tape','03 Foreground | tape','04 Modeled string | tape','05 Granular memory | Nimbus','06 Short damped room','07 Water','08 Wood air','09 Long distance'}
for i=0,8 do reaper.InsertTrackAtIndex(i,true);reaper.GetSetMediaTrackInfo_String(reaper.GetTrack(0,i),'P_NAME',names[i+1],true)end
local function track(i)return reaper.GetTrack(0,i)end
local function volume(i,g)reaper.SetMediaTrackInfo_Value(track(i),'D_VOL',g)end
local function send(a,b,g)local n=reaper.CreateTrackSend(track(a),track(b));reaper.SetTrackSendInfo_Value(track(a),0,n,'D_VOL',g)end
local paths={[0]='../long-line-v6/Media/01_Anchor_bypasses_drive.flac',[1]='Media/02_Inner_piano.flac',[2]='Media/03_Foreground_piano.flac',[3]='Media/04_Physical_string.flac',[6]='../long-line-v6/Media/07_Water.flac',[7]='../long-line-v6/Media/08_Wood_air.flac'}
for i,path in pairs(paths)do local it=reaper.AddMediaItemToTrack(track(i));local take=reaper.AddTakeToMediaItem(it);local src=reaper.PCM_Source_CreateFromFile(root..path);assert(src);reaper.SetMediaItemTake_Source(take,src);reaper.SetMediaItemInfo_Value(it,'D_POSITION',0);reaper.SetMediaItemInfo_Value(it,'D_LENGTH',336);reaper.SetMediaItemInfo_Value(it,'B_LOOPSRC',0);reaper.SetMediaItemInfo_Value(it,'C_BEATATTACHMODE',0)end
local instances={}
local function surge(i,mode)local fx=reaper.TrackFX_AddByName(track(i),'VST3: Surge XT Effects (Surge Synth Team)',false,-1);assert(fx>=0);reaper.TrackFX_SetParamNormalized(track(i),fx,12,mode);instances[i]=fx end
surge(1,.78);surge(2,.78);surge(3,.78);surge(4,.745);surge(5,.35)
local f=assert(io.open(root..'../long-line-v6/Scripts/ambience_bus.RTrackTemplate','r'));local ch=f:read('*a');f:close();ch=ch:gsub('\n%s*AUXRECV[^\n]*','');assert(reaper.SetTrackStateChunk(track(8),ch,false))
local function env(i,points)
 local tr=track(i);local e=reaper.GetTrackEnvelopeByName(tr,'Volume')
 if not e then local ok,ch=reaper.GetTrackStateChunk(tr,'',false);assert(ok);ch=ch:gsub('>%s*$','<VOLENV2\nACT 1 -1\nVIS 0 1 1\nLANEHEIGHT 45 0\nARM 0\nDEFSHAPE 0 -1 -1\nPT 0 1 0\n>\n>\n');assert(reaper.SetTrackStateChunk(tr,ch,false));e=reaper.GetTrackEnvelopeByName(tr,'Volume')end
 assert(e);reaper.DeleteEnvelopePointRange(e,-1,1000);for _,p in ipairs(points)do reaper.InsertEnvelopePoint(e,p[1],p[2],0,0,false,true)end;reaper.Envelope_SortPoints(e)
end
for i=0,8 do env(i,{{0,1},{330,1},{336,0}})end
volume(0,1);volume(1,1);volume(2,1);volume(3,.85);volume(4,.40);volume(5,.22);volume(6,.75);volume(7,.6);volume(8,.20)
send(1,4,.45);send(2,4,.65);send(1,5,.22);send(2,5,.25);send(3,5,.35)
send(0,8,.03);send(1,8,.08);send(2,8,.10);send(3,8,.10);send(4,8,.10);send(6,8,.02);send(7,8,.02)
-- Return prominence changes slowly; none of the old distortion boosts are inherited.
env(4,{{0,.5},{70,.68},{112,.55},{160,.65},{208,.75},{252,.68},{294,.55},{326,.35},{336,0}})
env(8,{{0,1},{327,1},{331,.7},{334,.25},{336,0}})
reaper.SetMediaTrackInfo_Value(reaper.GetMasterTrack(0),'D_VOL',2.8)
for _,r in ipairs({{0,70,'D field'},{70,112,'B beneath retained tones'},{112,160,'G field'},{160,208,'C field - rewritten melodic continuation'},{208,252,'E field'},{252,294,'G minor'},{294,336,'D return'}})do reaper.AddProjectMarker2(0,true,r[1],r[2],r[3],-1,0)end
local start=reaper.time_precise()
local function complete()
 if reaper.time_precise()-start<1 then reaper.defer(complete);return end
 local function set(i,p,v)reaper.TrackFX_SetParamNormalized(track(i),instances[i],p,v)end
 for i=1,3 do set(i,0,({.38,.30,.42})[i]);set(i,1,.38);set(i,2,.5);set(i,3,.40);set(i,4,.286);set(i,5,.05);set(i,6,.025);set(i,7,.025);set(i,8,.04);set(i,9,.08);set(i,10,0);set(i,11,.75)end
 for p,v in pairs({[0]=0,[1]=0,[2]=.23,[3]=.78,[4]=.5,[5]=.64,[6]=.78,[7]=.15,[8]=0,[9]=.18,[10]=0,[11]=1})do set(4,p,v)end
 for p,v in pairs({[0]=.30,[1]=.43,[2]=.49,[3]=.85,[4]=.62,[5]=0,[6]=.35,[7]=.68,[8]=.5,[9]=1})do set(5,p,v)end
 local function lowpass(i,hz)
  local fx=reaper.TrackFX_AddByName(track(i),'JS: filters/resonantlowpass',false,-1);assert(fx>=0,'Missing stock lowpass');reaper.TrackFX_SetParam(track(i),fx,0,hz);reaper.TrackFX_SetParam(track(i),fx,1,.15)
 end
 lowpass(1,2900);lowpass(2,3100);lowpass(3,2700);lowpass(4,2200);lowpass(5,2600);lowpass(8,2800)
 -- Remove modulation depth, keep diffusion. Existing automation, if any, must not restore it.
 for p=0,reaper.TrackFX_GetNumParams(track(8),0)-1 do local _,n=reaper.TrackFX_GetParamName(track(8),0,p,'');local key=n:lower():gsub('[^a-z]','');local v=nil
 if key:find('mod')and key:find('depth')then v=0 elseif key:find('feedback')then v=.43 end
 if v then reaper.TrackFX_SetParamNormalized(track(8),0,p,v);local e=reaper.GetFXEnvelope(track(8),0,p,false);if e then reaper.DeleteEnvelopePointRange(e,-1,1000);reaper.InsertEnvelopePoint(e,0,v,0,0,false,false)end end end
 reaper.Main_OnCommand(40101,0)
 for i,path in pairs(paths)do local src=reaper.GetMediaItemTake_Source(reaper.GetActiveTake(reaper.GetTrackMediaItem(track(i),0)));assert(math.abs(reaper.GetMediaSourceLength(src)-336)<.001)end
 local out=assert(io.open(root..'Audit/final_fx_parameters.tsv','w'))
 for i=0,8 do for fx=0,reaper.TrackFX_GetCount(track(i))-1 do local _,name=reaper.TrackFX_GetFXName(track(i),fx,'');out:write('FX\t'..i..'\t'..fx..'\t'..name..'\n');for p=0,reaper.TrackFX_GetNumParams(track(i),fx)-1 do local _,n=reaper.TrackFX_GetParamName(track(i),fx,p,'');local _,v=reaper.TrackFX_GetFormattedParamValue(track(i),fx,p,'');out:write(p..'\t'..n..'\t'..reaper.TrackFX_GetParamNormalized(track(i),fx,p)..'\t'..v..'\n')end end end;out:close()
 reaper.GetSetProjectInfo(0,'PROJECT_SRATE',48000,true);reaper.GetSetProjectInfo(0,'PROJECT_SRATE_USE',1,true);reaper.GetSetProjectInfo(0,'RENDER_SETTINGS',0,true);reaper.GetSetProjectInfo(0,'RENDER_BOUNDSFLAG',0,true);reaper.GetSetProjectInfo(0,'RENDER_STARTPOS',0,true);reaper.GetSetProjectInfo(0,'RENDER_ENDPOS',336,true);reaper.GetSetProjectInfo(0,'RENDER_TAILFLAG',0,true);reaper.GetSetProjectInfo(0,'RENDER_CHANNELS',2,true);reaper.GetSetProjectInfo(0,'RENDER_SRATE',48000,true);reaper.GetSetProjectInfo(0,'RENDER_NORMALIZE',0,true)
 reaper.GetSetProjectInfo_String(0,'RENDER_FORMAT','ZXZhdxgAAQ==',true);reaper.GetSetProjectInfo_String(0,'RENDER_FORMAT2','',true);reaper.GetSetProjectInfo_String(0,'RENDER_FILE',root..'Renders',true);reaper.GetSetProjectInfo_String(0,'RENDER_PATTERN','Long Line - Tonal Revision A',true)
 reaper.GetSetProjectNotes(0,true,'Long Line v8. Corrected semitone-return figures; modeled-string source, tape hysteresis, granular memory, short damped room, diffuse long return. No deliberate pitch warble. See weave.json and Audit. Review draft, not an artist-session reconstruction.')
 reaper.Main_SaveProjectEx(0,root..'Long Line - Tonal Revision.rpp',8);reaper.Main_OnCommand(42230,0)
 local f=assert(io.open(root..'Audit/render_returned.txt','w'));f:write('Native full mix render returned; verify WAV independently.');f:close()
end
reaper.defer(complete)
