import sys, glob, os, subprocess, json
S="/tmp/claude-0/-home-user-MayconBarbon/99707c74-1abd-56d4-a68a-c149be73686e/scratchpad"
day=sys.argv[1]; per=8
clips=sorted(c for c in glob.glob(f"{S}/proc/{day}/C*") if os.path.exists(c+"/done"))
os.makedirs(f"{S}/mosaic/{day}",exist_ok=True)
for b in range(0,len(clips),per):
    grp=clips[b:b+per]; rows=[]
    for c in grp:
        name=os.path.basename(c); dur=float(json.load(open(c+"/probe.json"))["format"]["duration"])
        r=f"{S}/mosaic/{day}/row_{name}.jpg"
        subprocess.run(["ffmpeg","-v","error","-i",c+"/sheet.jpg","-vf",f"scale=1440:135,pad=1600:135:160:0:black,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='{name}':x=8:y=40:fontsize=26:fontcolor=yellow,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='{dur:.0f}s':x=8:y=80:fontsize=24:fontcolor=white","-y",r])
        rows.append(r)
    out=f"{S}/mosaic/{day}/m_{os.path.basename(grp[0])}_{os.path.basename(grp[-1])}.jpg"
    args=[]; [args.extend(["-i",r]) for r in rows]
    subprocess.run(["ffmpeg","-v","error"]+args+["-filter_complex","".join(f"[{i}]" for i in range(len(rows)))+f"vstack={len(rows)}" if len(rows)>1 else "null","-y",out])
    for r in rows: os.remove(r)
print(len(clips))
