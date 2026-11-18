import json, subprocess
cenas = json.load(open("cenas.json"))
VERT = {22738, 4953, 34408}
lista = []
for c in cenas:
    n, d = c["n"], c["dur"]
    ins, chain = [], ""
    if c["clip"] is None:
        ins = ["-loop", "1", "-t", str(d), "-i", f"ov/c{n}_0.png"]
        base = "[0:v]scale=1080:1920,setsar=1,fps=30,format=yuv420p[b0]"
        k0 = 1; legs = c["legendas"][1:]; first = 1
        # card: overlay of subsequent legends uses their own full-card png
        chain = base; cur = "b0"; t = c["legendas"][0]["dur"]
        for i, l in enumerate(legs, start=1):
            ins += ["-loop", "1", "-t", str(d), "-i", f"ov/c{n}_{i}.png"]
            chain += f";[{i}:v]scale=1080:1920,format=rgba[o{i}];[{cur}][o{i}]overlay=0:0:enable='gte(t,{t:.2f})'[b{i}]"
            cur = f"b{i}"; t += l["dur"]
    else:
        ins = ["-stream_loop", "-1", "-ss", str(c["ss"]), "-i", f"clips/{c['clip']}.mp4"]
        if c["clip"] in VERT:
            chain = "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,eq=saturation=1.06[b0]"
        else:
            chain = ("[0:v]split[a][f];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=28:2,eq=brightness=-0.22:saturation=0.8[bg];"
                     "[f]scale=1080:-2,eq=saturation=1.06[fg];[bg][fg]overlay=0:560,setsar=1,fps=30[b0]")
        cur, t = "b0", 0.0
        for i, l in enumerate(c["legendas"]):
            ins += ["-loop", "1", "-t", str(d), "-i", f"ov/c{n}_{i}.png"]
            chain += f";[{i+1}:v]format=rgba[o{i}];[{cur}][o{i}]overlay=0:0:enable='between(t,{t:.2f},{t + l['dur']:.2f})'[b{i+1}]"
            cur = f"b{i+1}"; t += l["dur"]
    chain += f";[{cur}]format=yuv420p,fade=t=in:st=0:d=0.25[out]"
    out = f"s{n:02d}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", chain, "-map", "[out]", "-t", str(d), "-an",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-r", "30", "-pix_fmt", "yuv420p", out], check=True)
    lista.append(f"file '{out}'")
open("lista.txt", "w").write("\n".join(lista) + "\n")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "lista.txt", "-c", "copy", "sem_som.mp4"], check=True)
D = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", "sem_som.mp4"], capture_output=True, text=True).stdout)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "sem_som.mp4", "-i", "m634.mp3", "-filter_complex",
                f"[1:a]apad,atrim=0:{D},afade=t=in:d=1,afade=t=out:st={D-5:.2f}:d=5,volume=0.8[a]",
                "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "vsl-storymaker-9x16.mp4"], check=True)
print("duração", D)
