local _,s=reaper.get_action_context();local root=s:gsub('\\','/'):match('^(.*)/Scripts/[^/]+$')..'/'
assert(not io.open(root..'Renders/Inner texture native.wav','rb'),'Existing render preserved')
reaper.Main_OnCommand(40859,0);reaper.SetCurrentBPM(0,60,true)
local out=assert(io.open(root..'Audit/native_patches.tsv','w'))
for i=0,3 do
 reaper.InsertTrackAtIndex(i,true);local tr=reaper.GetTrack(0,i);local ty=i%2==0
 reaper.GetSetMediaTrackInfo_String(tr,'P_NAME',(ty and 'Tyrell inner ' or 'FB resonant inner ')..i,true)
 reaper.SetMediaTrackInfo_Value(tr,'D_VOL',.15);reaper.SetMediaTrackInfo_Value(tr,'D_PAN',({-.25,.25,.12,-.12})[i+1])
 local fx=reaper.TrackFX_AddByName(tr,ty and 'VST3i: TyrellN6 (u-he)' or 'VST3i: FB-3300 (Full Bucket Music)',false,-1);assert(fx>=0)
 local settings
 if ty then settings={[0]=.35,[9]=0,[10]=0,[12]=0,[17]=.5,[18]=.32,[19]=.42,[20]=.66,[22]=.35,[23]=.65,[26]=.25,[28]=.5,[30]=.3,[38]=.22,[40]=.5,[41]=.4,[42]=0,[43]=.5,[45]=.5,[46]=0,[48]=.5,[50]=0,[54]=.5,[55]=.36,[56]=0,[57]=0,[58]=0,[59]=.06,[62]=.43+i*.012,[64]=.52,[66]=.5,[67]=.30,[68]=.03,[72]=0,[77]=0}
 else settings={[13]=.0,[14]=0,[15]=.5,[16]=.5,[18]=0,[20]=0,[21]=0,[24]=.43,[25]=.06,[27]=.05,[29]=0,[32]=.16,[33]=.25,[34]=.65,[35]=1,[39]=.025,[40]=.24,[41]=.4,[42]=.55,[43]=0,[45]=0,[55]=.38,[60]=1,[61]=.20,[116]=0,[119]=0,[177]=0,[180]=0,[184]=.35,[219]=0}
 end
 for p,v in pairs(settings)do reaper.TrackFX_SetParamNormalized(tr,fx,p,v)end
 local eq=reaper.TrackFX_AddByName(tr,'VST: ReaEQ (Cockos)',false,-1);assert(eq>=0)
 reaper.TrackFX_SetNamedConfigParm(tr,eq,'BANDTYPE0','3');assert(reaper.TrackFX_SetEQParam(tr,eq,5,0,0,2200,false));reaper.TrackFX_SetEQParam(tr,eq,5,0,2,2,false)
 reaper.TrackFX_SetEQParam(tr,eq,0,0,0,220,false)
 local it=reaper.CreateNewMIDIItemInProj(tr,0,96,false);local tk=reaper.GetActiveTake(it)
 for _,n in ipairs(dofile(root..'Scripts/demo_notes.lua'))do if n[1]==i then reaper.MIDI_InsertNote(tk,false,false,reaper.MIDI_GetPPQPosFromProjTime(tk,n[2]),reaper.MIDI_GetPPQPosFromProjTime(tk,n[3]),0,n[4],n[5],true)end end;reaper.MIDI_Sort(tk)
 out:write('TRACK\t'..i..'\n');for p,v in pairs(settings)do local _,name=reaper.TrackFX_GetParamName(tr,fx,p,'');local _,val=reaper.TrackFX_GetFormattedParamValue(tr,fx,p,'');out:write(p..'\t'..name..'\t'..v..'\t'..val..'\n')end
end
out:close()
for k,v in pairs({PROJECT_SRATE=48000,PROJECT_SRATE_USE=1,RENDER_SETTINGS=0,RENDER_BOUNDSFLAG=0,RENDER_STARTPOS=0,RENDER_ENDPOS=96,RENDER_TAILFLAG=0,RENDER_CHANNELS=2,RENDER_SRATE=48000,RENDER_NORMALIZE=0})do reaper.GetSetProjectInfo(0,k,v,true)end
reaper.GetSetProjectInfo_String(0,'RENDER_FORMAT','ZXZhdxgAAQ==',true);reaper.GetSetProjectInfo_String(0,'RENDER_FILE',root..'Renders',true);reaper.GetSetProjectInfo_String(0,'RENDER_PATTERN','Inner texture native',true)
reaper.Main_SaveProjectEx(0,root..'Texture Instruments.rpp',8);reaper.Main_OnCommand(42230,0)
local f=assert(io.open(root..'Audit/texture_render_returned.txt','w'));f:write('Native render returned');f:close()
