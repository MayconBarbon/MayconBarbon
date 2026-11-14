"""OFFLINE animatic segments from analysis keyframes (~1/s, 320x180) or proxies. Same seg names as render_segments.py
usage: python3 render_offline.py edl.json"""
import json, sys, os, subprocess, glob
S="/tmp/claude-0/-home-user-MayconBarbon/99707c74-1abd-56d4-a68a-c149be73686e/scratchpad"
edl=json.load(open(sys.argv[1]))
os.makedirs(f"{S}/render/seg",exist_ok=True); os.makedirs(f"{S}/render/tmp",exist_ok=True)
GRADE=edl.get("grade","eq=contrast=1.05:saturation=1.06:gamma=0.98")
for sh in edl["shots"]:
    if sh.get("type","clip")!="clip": continue
    P=f"{S}/proc/{sh['day']}/{sh['clip']}"; out=f"{S}/render/seg/{sh['id']}.mov"
    key=json.dumps(["off",sh['day'],sh['clip'],sh['in'],sh['dur'],sh.get('speed',1),sh.get('vf','')])
    if os.path.exists(out+".key") and (open(out+".key").read()==key or os.environ.get("KEEP")): continue
    sp=sh.get("speed",1.0); srcdur=sh["dur"]*sp
    dur=float(json.load(open(P+"/probe.json"))["format"]["duration"])
    post=f"scale=1920:1080:flags=bicubic,{GRADE}"+(","+sh["vf"] if sh.get("vf") else "")
    if os.path.exists(P+"/proxy.mp4"):
        vin=["-ss",str(sh["in"]),"-t",str(srcdur+0.1),"-i",P+"/proxy.mp4"]
        vf=(f"setpts=PTS/{sp}," if sp!=1 else "")+"fps=30000/1001,"+post
    else:
        kfs=sorted(glob.glob(P+"/kf/*.jpg")); g=dur/len(kfs)
        a=int(sh["in"]/g); b=max(a+1,int((sh["in"]+srcdur)/g+0.999))
        sel=kfs[a:min(b+1,len(kfs))] or kfs[-1:]
        lst=f"{S}/render/tmp/{sh['id']}.txt"
        with open(lst,"w") as f:
            for p in sel: f.write(f"file '{p}'\nduration {g/sp:.4f}\n")
            f.write(f"file '{sel[-1]}'\n")
        vin=["-f","concat","-safe","0","-i",lst]
        vf=("scale=640:360,fps=30000/1001,framerate=fps=30000/1001:interp_start=0:interp_end=255:scene=100,"
            f"zoompan=z='1.0+0.0004*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=640x360:fps=30000/1001,"+post)
    ain=["-ss",str(sh["in"]),"-t",str(sh["dur"]),"-i",P+"/audio16k.wav"]
    subprocess.run(["ffmpeg","-v","error"]+vin+ain+["-map","0:v:0","-vf",vf,"-t",str(sh["dur"]),"-c:v","libx264","-preset","veryfast","-crf","20",
        "-pix_fmt","yuv420p","-r","30000/1001","-map","1:a:0","-af","aresample=48000,apad","-ac","2","-c:a","pcm_s16le","-t",str(sh["dur"]),"-y",out],check=True)
    open(out+".key","w").write(key); print("off",sh["id"],sh["clip"],flush=True)
