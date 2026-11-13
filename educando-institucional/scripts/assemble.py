"""Assemble final review MP4 from rendered segments + VO + music + texts.
usage: python3 assemble.py edl.json out.mp4"""
import json, sys, os, subprocess
S="/tmp/claude-0/-home-user-MayconBarbon/99707c74-1abd-56d4-a68a-c149be73686e/scratchpad"
edl=json.load(open(sys.argv[1])); out=sys.argv[2]
FPS=30000/1001
shots=edl["shots"]; t=0.0
for sh in shots:
    sh["tl"]=t; t+=sh["dur"]
TOTAL=t
# ---- ASS texts
def ts(x):
    h=int(x//3600); m=int(x%3600//60); s=x%60
    return f"{h}:{m:02d}:{s:05.2f}"
ass=["[Script Info]","ScriptType: v4.00+","PlayResX: 1920","PlayResY: 1080","",
"[V4+ Styles]","Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
"Style: Lower,Montserrat,46,&H00FFFFFF,&H00FFFFFF,&H64000000,&H00000000,0,0,0,0,100,100,2,0,1,0,2,1,120,120,110,1",
"Style: Big,Montserrat,130,&H00FFFFFF,&H00FFFFFF,&H64000000,&H00000000,1,0,0,0,100,100,6,0,1,0,3,5,80,80,80,1",
"Style: Title,Montserrat,64,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,4,0,1,0,0,5,80,80,80,1",
"Style: Sub,Montserrat,40,&H00E0E0E0,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,3,0,1,0,0,5,80,80,80,1",
"Style: Guide,DejaVu Sans,26,&H0000D7FF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,3,4,0,9,30,30,24,1","",
"[Events]","Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
for x in edl.get("texts",[]):
    fi=int(x.get("fade",0.5)*1000)
    pos=x.get("pos","")
    ass.append(f"Dialogue: 0,{ts(x['start'])},{ts(x['end'])},{x.get('style','Lower')},,0,0,0,,{{\\fad({fi},{fi}){pos}}}{x['text']}")
if edl.get("watermark"):
    ass.append(f"Dialogue: 1,{ts(0)},{ts(TOTAL)},Guide,,0,0,0,,{edl['watermark']}")
open(f"{S}/render/texts.ass","w").write("\n".join(ass)+"\n")
# ---- video inputs
inputs=[]; fc=[]; vlabels=[]; alabels=[]
for i,sh in enumerate(shots):
    if sh.get("type","clip")=="clip":
        inputs+=["-i",f"{S}/render/seg/{sh['id']}.mov"]
        fc.append(f"[{i}:v]settb=AVTB,setpts=PTS-STARTPTS,format=yuv420p[v{i}]")
        g=sh.get("amb_db",-14)
        if sh.get("audio")=="mute": g=-90
        fc.append(f"[{i}:a]atrim=0:{sh['dur']},asetpts=PTS-STARTPTS,volume={g}dB,afade=t=in:d=0.08,afade=t=out:st={max(0,sh['dur']-0.08)}:d=0.08[a{i}]")
    elif sh["type"]=="still":
        inputs+=["-loop","1","-t",str(sh["dur"]),"-i",sh["path"]]
        z=sh.get("zoom","in")
        zexpr="1+0.06*on/({n})".format(n=int(sh['dur']*FPS)) if z=="in" else "1.06-0.06*on/({n})".format(n=int(sh['dur']*FPS))
        fc.append(f"[{i}:v]scale=3840:2160:force_original_aspect_ratio=decrease,pad=3840:2160:(ow-iw)/2:(oh-ih)/2:black,zoompan=z='{zexpr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=30000/1001,trim=duration={sh['dur']},setpts=PTS-STARTPTS,format=yuv420p[v{i}]")
        fc.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{sh['dur']}[a{i}]")
    else:  # black
        inputs+=["-f","lavfi","-t",str(sh["dur"]),"-i",f"color=black:s=1920x1080:r=30000/1001"]
        fc.append(f"[{i}:v]settb=AVTB,setpts=PTS-STARTPTS,format=yuv420p[v{i}]")
        fc.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{sh['dur']}[a{i}]")
    vlabels.append(f"[v{i}]"); alabels.append(f"[a{i}]")
n=len(shots)
fc.append("".join(vlabels)+f"concat=n={n}:v=1:a=0[vcat]")
fc.append("".join(alabels)+f"concat=n={n}:v=0:a=1[amb]")
vf="[vcat]"+f"subtitles={S}/render/texts.ass:fontsdir={S}/fonts"
fo=edl.get("fade_out",1.5); fi=edl.get("fade_in",0)
if fi: vf+=f",fade=t=in:st=0:d={fi}"
vf+=f",fade=t=out:st={TOTAL-fo}:d={fo}[vout]"
fc.append(vf)
# ---- VO guide + sync dialog bus
k=len(shots); voc=[]
for j,v in enumerate(edl.get("vo",[])):
    inputs+=["-i",v["path"]]
    d=int(v["start"]*1000)
    fc.append(f"[{k}:a]aresample=48000,pan=stereo|c0=c0|c1=c0,volume={v.get('db',0)}dB,adelay={d}|{d}[vo{j}]"); voc.append(f"[vo{j}]"); k+=1
# sync speech: duplicate amb at shots with audio=sync to a speech bus (already in amb at its own gain); we key ducking from VO + sync shots
key_parts=list(voc)
for i,sh in enumerate(shots):
    if sh.get("audio")=="sync":
        inputs+=["-ss",str(0),"-i",f"{S}/render/seg/{sh['id']}.mov"]
        d=int(sh["tl"]*1000)
        fc.append(f"[{k}:a]atrim=0:{sh['dur']},asetpts=PTS-STARTPTS,adelay={d}|{d}[sy{i}]"); key_parts.append(f"[sy{i}]"); k+=1
if voc:
    fc.append("".join(voc)+f"amix=inputs={len(voc)}:normalize=0,apad=whole_dur={TOTAL}[vobus]")
else:
    fc.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{TOTAL}[vobus]")
fc.append("[vobus]asplit=2[vomix][vokey0]")
if len(key_parts)>len(voc):
    sy=key_parts[len(voc):]
    fc.append("".join(sy)+f"amix=inputs={len(sy)}:normalize=0,apad=whole_dur={TOTAL}[sybus]")
    fc.append("[vokey0][sybus]amix=inputs=2:normalize=0[key]")
else:
    fc.append("[vokey0]anull[key]")
# ---- music with keyframed volume, ducked by key
m=edl.get("music")
if m:
    inputs+=["-ss",str(m.get("src_in",0)),"-i",m["path"]]
    kf=m["keys"]  # [[t,db],...] timeline seconds
    expr=f"{kf[-1][1]}"
    for (t0,d0),(t1,d1) in reversed(list(zip(kf[:-1],kf[1:]))):
        expr=f"if(lt(t,{t1}),{d0}+({d1}-{d0})*(t-{t0})/({t1}-{t0}+0.0001),{expr})"
    expr=f"if(lt(t,{kf[0][0]}),{kf[0][1]},{expr})"
    d=int(m.get("start",0)*1000)
    fc.append(f"[{k}:a]aresample=48000,adelay={d}|{d},volume=eval=frame:volume='pow(10,({expr})/20)',apad=whole_dur={TOTAL}[mus0]"); k+=1
    fc.append(f"[mus0][key]sidechaincompress=threshold=0.02:ratio=6:attack=80:release=600:makeup=1[mus]")
    fc.append("[amb][vomix][mus]amix=inputs=3:normalize=0,atrim=0:{T},afade=t=out:st={st}:d={fo},loudnorm=I=-16:TP=-1.5:LRA=11[aout]".format(T=TOTAL,st=TOTAL-fo,fo=fo))
else:
    fc.append("[amb][vomix]amix=inputs=2:normalize=0,loudnorm=I=-16:TP=-1.5[aout]")
open(f"{S}/render/filter.txt","w").write(";\n".join(fc))
cmd=["ffmpeg","-v","error","-stats"]+inputs+["-filter_complex_script",f"{S}/render/filter.txt","-map","[vout]","-map","[aout]",
     "-c:v","libx264","-preset","medium","-crf",str(edl.get("crf",20)),"-pix_fmt","yuv420p","-r","30000/1001","-movflags","+faststart",
     "-c:a","aac","-b:a","192k","-ar","48000","-t",str(TOTAL),"-y",out]
print(" ".join(cmd[:6]), "...", len(shots),"shots", f"{TOTAL:.2f}s")
subprocess.run(cmd,check=True)
