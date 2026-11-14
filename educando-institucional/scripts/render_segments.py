"""Render each EDL shot from the ORIGINAL 4K clip into a 1080p29.97 graded intermediate.
usage: python3 render_segments.py edl.json"""
import json, sys, os, subprocess, csv
S="/tmp/claude-0/-home-user-MayconBarbon/99707c74-1abd-56d4-a68a-c149be73686e/scratchpad"
edl=json.load(open(sys.argv[1]))
inv={}
for r in csv.reader(open(f"{S}/inventory.tsv"),delimiter="\t"):
    inv[(r[0], r[1].replace("fx3 gabriel","C").replace(".MP4",""))]=(r[2],int(r[3]))
GRADE=edl.get("grade","eq=contrast=1.05:saturation=1.06:gamma=0.98,unsharp=3:3:0.3")
def seg_name(sh): return f"{S}/render/seg/{sh['id']}.mov"
def key(sh): return json.dumps([sh['day'],sh['clip'],sh['in'],sh['dur'],sh.get('speed',1),sh.get('vf',''),GRADE])
by_clip={}
for sh in edl["shots"]:
    if sh.get("type","clip")!="clip": continue
    by_clip.setdefault((sh["day"],sh["clip"]),[]).append(sh)
for (day,clip),shots in sorted(by_clip.items()):
    todo=[sh for sh in shots if not (os.path.exists(seg_name(sh)) and open(seg_name(sh)+".key").read()==key(sh) if os.path.exists(seg_name(sh)+".key") else False)]
    if not todo: continue
    fid,size=inv[(day,clip)]
    src=f"{S}/render/orig/{day}_{clip}.MP4"
    if not (os.path.exists(src) and os.path.getsize(src)==size):
        for t in range(4):
            subprocess.run(["curl","-sS","-L","--retry","3","-o",src,f"https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t"])
            if os.path.getsize(src)==size: break
            if b"Quota exceeded" in open(src,"rb").read(3000):
                os.remove(src); print("QUOTA",day,clip,flush=True); sys.exit(3)
        if os.path.getsize(src)!=size:
            print("FAIL",day,clip,flush=True); os.remove(src); continue
    for sh in todo:
        sp=sh.get("speed",1.0); srcdur=sh["dur"]*sp
        vf=f"setpts=PTS/{sp}," if sp!=1 else ""
        vf+=f"scale=1920:1080:flags=lanczos,fps=30000/1001,{GRADE}"
        if sh.get("vf"): vf+=","+sh["vf"]
        subprocess.run(["ffmpeg","-v","error","-ss",str(sh["in"]),"-t",str(srcdur+0.05),"-i",src,
            "-ss",str(sh["in"]),"-t",str(sh["dur"]),"-i",src,
            "-map","0:v:0","-vf",vf,"-t",str(sh["dur"]),"-c:v","libx264","-preset","fast","-crf","15","-pix_fmt","yuv420p","-r","30000/1001",
            "-map","1:a:0?","-af","aresample=48000,apad","-ac","2","-c:a","pcm_s16le","-t",str(sh["dur"]),"-y",seg_name(sh)],check=True)
        open(seg_name(sh)+".key","w").write(key(sh))
        print("seg",sh["id"],day,clip,sh["in"],sh["dur"],sp,flush=True)
    if not edl.get("keep_orig"): os.remove(src)
