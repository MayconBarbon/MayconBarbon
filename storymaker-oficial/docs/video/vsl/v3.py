"""VSL v3 — mesmo roteiro e mesma narração do Gabriel da v2, visual no estilo da referência
(tipografia animada em fundos sólidos intercalada com vídeo; mais natureza e brindes, menos bolo)."""
import json, re, subprocess, os, sys
CENA = {
 1: dict(tipo="FOOT", lay="S", clips=[(4632, 1), (51540, 2), (51541, 4)], tituloMd="Você conhece essa **cena?**"),
 2: dict(tipo="WHEEL", tituloMd="O que gravar **primeiro?**", itens=["a decoração", "a chegada", "o palco", "as pessoas", "o discurso", "o brinde"]),
 3: dict(tipo="FOOT", lay="S", clips=[(5224, 0.5), (51553, 1), (18204, 0.5)], tituloMd="Imagens **bonitas…**"),
 4: dict(tipo="FOOT", lay="S", clips=[(41222, 1), (43256, 0.5), (4537, 3)], tituloMd="O que o cliente **espera?**"),
 5: dict(tipo="FOOT", lay="S", clips=[(44071, 2), (41273, 1), (44074, 2)], tituloMd="A edição que não **termina**"),
 6: dict(tipo="FOOT", lay="S", clips=[(51529, 1), (51643, 2), (4632, 4)], tituloMd="O momento que não **volta**"),
 7: dict(tipo="SWAP", rotulo="Método", frases=["Nada disso é falta de **talento.**", "É falta de **método.**", "E método **se aprende.**"]),
 8: dict(tipo="FOOT", lay="V", clips=[(1170, 2)], tituloMd="Começa antes do **evento**"),
 9: dict(tipo="FOOT", lay="S", clips=[(5217, 0.5), (5206, 1), (18204, 4)], tituloMd="", rotulos=["ABERTO", "MÉDIO", "DETALHE"]),
 10: dict(tipo="FOOT", lay="S", clips=[(50406, 0.5), (50470, 1), (44074, 6)], tituloMd="A edição não escolhe **por você**"),
 11: dict(tipo="SWAP", rotulo="Para quem é", frases=["Materiais **práticos.**", "Story**maker**", "Social **media**", "Social**maker**"]),
 12: dict(tipo="LIST", itens=["Checklists", "Modelo de briefing", "Planilha de custos", "Modelo de contrato", "E-book", "Kit Lançamento"]),
 13: dict(tipo="FOOT", lay="V", clips=[(1186, 1)], tituloMd="Comece **pequeno**"),
 14: dict(tipo="FOOT", lay="S", clips=[(1780, 2), (4702, 2), (51540, 8)], tituloMd="Do simples ao **grande**"),
 15: dict(tipo="FINAL"),
}
cenas = json.load(open("cenas.json")); os.makedirs("v3", exist_ok=True)

def chunks(texto, n=4):
    out = []
    for frase in [f.strip() for f in re.split(r"(?<=[,:.?!])\s+", texto) if f.strip()]:
        w = frase.split()
        while w:
            k = n if len(w) != n + 1 else n + 1
            out.append(" ".join(w[:k])); w = w[k:]
    res = []
    for x in out:
        if res and len(x.split()) == 1 and len(res[-1].split()) < 5: res[-1] += " " + x
        else: res.append(x)
    return res
def destaque(chunk):
    ws = [re.sub(r"[^\wÀ-ú-]", "", x) for x in chunk.split()]
    i = max(range(len(ws)), key=lambda j: len(ws[j])); return i if len(ws[i]) > 3 else -1

plano = []
for c in cenas:
    legs = sum((chunks(l["texto"]) for l in c["legendas"]), [])
    pesos = [len(x.split()) + 0.6 for x in legs]; tot = sum(pesos); t = c["pad_ini"]; L = []
    for x, p in zip(legs, pesos):
        dd = c["voz_dur"] * p / tot; L.append({"texto": x, "ini": round(t, 2), "fim": round(t + dd, 2), "hl": destaque(x)}); t += dd
    L[-1]["fim"] = round(c["dur"] - 0.05, 2)
    e = CENA[c["n"]]
    tf = round(min(2.0, max(1.3, c["dur"] * 0.33)), 2) if e.get("tituloMd") else 0
    # nas cenas com título, a legenda só entra depois que o título sai
    if tf:
        for x in L:
            if x["ini"] < tf: x["ini"] = tf
        L = [x for x in L if x["fim"] - x["ini"] > 0.35]
    plano.append({**c, **e, "caps": L, "titulo_fim": tf})
json.dump(plano, open("v3/plano.json", "w"), ensure_ascii=False, indent=1)
if "--so-plano" in sys.argv: raise SystemExit

subprocess.run(["node", "v3_render.js"] + sys.argv[1:2], check=True)

lista = []
for c in plano:
    n, d = c["n"], c["dur"]; out = f"v3/s{n:02d}.mp4"; seq = f"v3/f{n:02d}/%05d.png"
    if c["tipo"] != "FOOT":
        cmd = ["-framerate", "30", "-i", seq, "-filter_complex", "[0:v]format=yuv420p[out]"]
    else:
        ins, fc = [], [f"color=c=0x1b1a1f:s=1080x1920:r=30:d={d}[base]"]; cur = "base"
        for k, (clip, ss) in enumerate(c["clips"]):
            ins += ["-stream_loop", "-1", "-ss", str(ss), "-t", str(d + 0.5), "-i", f"clips/{clip}.mp4"]
            z = f"(1+0.07*t/{d})"
            if c["lay"] == "V":
                fc.append(f"[{k}:v]fps=30,scale=w='ceil(1080*{z}/2)*2':h=-2:eval=frame,crop=1080:1920,setsar=1[t{k}]")
                fc.append(f"[{cur}][t{k}]overlay=0:0:shortest=1[c{k}]")
            else:
                y = [32, 656, 1280][k]; dl = 0.08 * k; s = -1 if k % 2 == 0 else 1
                fc.append(f"[{k}:v]fps=30,scale=w='ceil(1080*{z}/2)*2':h=-2:eval=frame,crop=1080:608,setsar=1[t{k}]")
                fc.append(f"[{cur}][t{k}]overlay=x='{s}*1080*(1-min(1,max(0,(t-{dl})/0.28))^0.35)':y={y}:shortest=1[c{k}]")
            cur = f"c{k}"
        m = len(c["clips"])
        ins += ["-framerate", "30", "-i", seq]
        fc.append(f"[{cur}]trim=0:{d},setpts=PTS-STARTPTS[bb];[{m}:v]format=rgba[ov];[bb][ov]overlay=0:0:shortest=1,format=yuv420p[out]")
        cmd = ins + ["-filter_complex", ";".join(fc)]
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", *cmd, "-map", "[out]", "-t", str(d), "-an", "-c:v", "libx264", "-preset", "medium",
                        "-crf", "20", "-r", "30", "-pix_fmt", "yuv420p", out], capture_output=True, text=True)
    if r.returncode: print("ERRO", n, r.stderr[-1200:]); raise SystemExit(1)
    lista.append(f"file 's{n:02d}.mp4'"); print("montada", n, flush=True)

open("v3/lista.txt", "w").write("\n".join(lista) + "\n")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "v3/lista.txt", "-c", "copy", "v3/sem_som.mp4"], check=True)
D = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", "v3/sem_som.mp4"], capture_output=True, text=True).stdout)
al = []
for c in plano:
    o = f"v3/a{c['n']:02d}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", c["voz"], "-af", f"adelay={int(c['pad_ini']*1000)},apad,atrim=0:{c['dur']}", "-ar", "48000", "-ac", "1", o], check=True)
    al.append(f"file 'a{c['n']:02d}.wav'")
open("v3/lista_a.txt", "w").write("\n".join(al) + "\n")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "v3/lista_a.txt", "-c", "pcm_s16le", "v3/voz.wav"], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "50", "-i", "m634.mp3", "-ss", "50", "-i", "m634.mp3", "-filter_complex", "[0:a][1:a]acrossfade=d=3[m]", "-map", "[m]", "v3/trilha.wav"], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "v3/sem_som.mp4", "-i", "v3/voz.wav", "-i", "v3/trilha.wav", "-filter_complex",
                f"[1:a]loudnorm=I=-16:TP=-1.5:LRA=11,aformat=channel_layouts=stereo[v];[2:a]atrim=0:{D},afade=t=in:d=0.8,afade=t=out:st={D-4:.2f}:d=4,volume=0.14[m];[v][m]amix=inputs=2:duration=first:normalize=0[a]",
                "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-t", str(D), "-movflags", "+faststart", "v3/vsl-v3.mp4"], check=True)
def ts(x):
    h, r = divmod(x, 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s-int(s))*1000)):03d}"
srt, k = [], 1
for c in plano:
    for l in c["legendas"]:
        pass
    # legendas completas da fala (inclusive nas cenas tipográficas), alinhadas à voz
    legs = sum((chunks(l["texto"]) for l in c["legendas"]), []); pesos = [len(x.split()) + 0.6 for x in legs]; tot = sum(pesos); t = c["inicio"] + c["pad_ini"]
    for x, p in zip(legs, pesos):
        dd = c["voz_dur"] * p / tot; srt.append(f"{k}\n{ts(t)} --> {ts(t+dd)}\n{x}\n"); k += 1; t += dd
open("v3/vsl-v3.srt", "w").write("\n".join(srt))
print("duração", D)
