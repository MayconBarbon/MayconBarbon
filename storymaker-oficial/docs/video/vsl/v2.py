"""VSL v2 — estilo dinâmico (lettering animado, imagens verticais ou empilhadas).
Lê cenas.json (falas + narração já gerada por narrar.py) e monta vsl-v2.mp4.
Layouts:  V = clipe vertical em tela cheia
          S = três clipes horizontais empilhados (quadro inteiro, sem cortar rostos)
          C = clipe horizontal de detalhe recortado em 9:16
"""
import json, re, subprocess, os

LAYOUT = {
 1: ("S", [(4632, 1), (4640, 3), (51541, 4)]),
 2: ("S", [(5227, 1), (46893, 2), (4385, 2)]),
 3: ("S", [(5224, 0.5), (5223, 1), (18204, 0.5)]),
 4: ("S", [(41222, 1), (43256, 0.5), (4537, 3)]),
 5: ("S", [(44071, 2), (41273, 1), (44074, 2)]),
 6: ("S", [(4663, 2), (5112, 1), (5109, 1)]),
 7: ("V", [(42308, 1)]),
 8: ("S", [(41813, 0.5), (43266, 1), (1741, 3)]),
 9: ("S", [(5217, 0.5), (5206, 1), (18204, 4)]),
 10: ("S", [(50406, 0.5), (50470, 1), (44074, 6)]),
 11: ("S", [(4919, 1), (817, 1), (50015, 0.5)]),
 12: ("V", [(34408, 0.5)]),
 13: ("S", [(50053, 0), (3581, 1), (46874, 1)]),
 14: ("S", [(817, 4), (5117, 0.5), (4632, 5)]),
 15: ("CARD", []),
}

cenas = json.load(open("cenas.json"))
os.makedirs("v2", exist_ok=True)

def chunks(texto, n=4):
    """Quebra nas pausas (vírgula, dois-pontos, ponto) e depois em blocos de até 4 palavras (5 se sobrar uma)."""
    out = []
    for frase in [f.strip() for f in re.split(r"(?<=[,:.?!])\s+", texto) if f.strip()]:
        w = frase.split()
        while w:
            k = n if len(w) != n + 1 else n + 1
            out.append(" ".join(w[:k])); w = w[k:]
    # junta pedaços de uma palavra só ao anterior
    res = []
    for x in out:
        if res and len(x.split()) == 1 and len(res[-1].split()) < 5: res[-1] += " " + x
        else: res.append(x)
    return res

def destaque(chunk):
    ws = [re.sub(r"[^\wÀ-ú-]", "", x) for x in chunk.split()]
    if not ws: return -1
    i = max(range(len(ws)), key=lambda j: len(ws[j]))
    return i if len(ws[i]) > 3 else -1

# legendas curtas (até 4 palavras), tempo proporcional às palavras dentro do trecho de fala de cada cena
plano = []
for c in cenas:
    fala0, d = c["pad_ini"], c["voz_dur"]
    legs = []
    for l in c["legendas"]:
        legs += chunks(l["texto"])
    pesos = [len(x.split()) + 0.6 for x in legs]
    tot = sum(pesos); t = fala0; L = []
    for x, p in zip(legs, pesos):
        dd = d * p / tot
        L.append({"texto": x, "ini": round(t, 2), "fim": round(t + dd, 2), "hl": destaque(x)}); t += dd
    L[-1]["fim"] = round(c["dur"] - 0.05, 2)
    titulo_fim = round(min(2.2, max(1.4, c["dur"] * 0.35)), 2)
    plano.append({**c, "layout": LAYOUT[c["n"]][0], "clips": LAYOUT[c["n"]][1], "caps": L, "titulo_fim": titulo_fim})
json.dump(plano, open("v2/plano.json", "w"), ensure_ascii=False, indent=1)

# ---------- overlays (Playwright) ----------
subprocess.run(["node", "v2_overlays.js"], check=True)

# ---------- montagem ----------
lista = []
for c in plano:
    n, d = c["n"], c["dur"]
    ins, fc = [], []
    if c["layout"] == "CARD":
        ins += ["-loop", "1", "-t", str(d), "-i", f"v2/card.png"]
        fc.append("[0:v]scale=1080:1920,setsar=1,fps=30,format=yuva420p[b]")
        idx = 1
    else:
        fc.append(f"color=c=0x1b1a1f:s=1080x1920:r=30:d={d}[base]")
        cur = "base"
        for k, (clip, ss) in enumerate(c["clips"]):
            ins += ["-stream_loop", "-1", "-ss", str(ss), "-t", str(d + 0.5), "-i", f"clips/{clip}.mp4"]
            z = f"(1+0.07*t/{d})"
            if c["layout"] == "V":
                fc.append(f"[{k}:v]fps=30,scale=w='ceil(1080*{z}/2)*2':h=-2:eval=frame,crop=1080:1920,setsar=1[t{k}]")
                fc.append(f"[{cur}][t{k}]overlay=0:0:shortest=1[c{k}]")
            elif c["layout"] == "C":
                fc.append(f"[{k}:v]fps=30,scale=w=-2:h='ceil(1920*{z}/2)*2':eval=frame,crop=1080:1920,setsar=1[t{k}]")
                fc.append(f"[{cur}][t{k}]overlay=0:0:shortest=1[c{k}]")
            else:  # S: três faixas 1080x608 com entrada deslizando, alternando lados
                y = [32, 656, 1280][k]; dl = 0.10 * k
                fc.append(f"[{k}:v]fps=30,scale=w='ceil(1080*{z}/2)*2':h=-2:eval=frame,crop=1080:608,setsar=1[t{k}]")
                xexp = f"if(lt(t,{dl}),{'-1080' if k % 2 == 0 else '1080'},{'-1080+1080' if k % 2 == 0 else '1080-1080'}*min(1,(t-{dl})/0.32)+{'(-1080)*(1-min(1,(t-' + str(dl) + ')/0.32))' if k % 2 == 0 else '1080*(1-min(1,(t-' + str(dl) + ')/0.32))'})"
                fc.append(f"[{cur}][t{k}]overlay=x='{xexp}':y={y}:shortest=1[c{k}]")
            cur = f"c{k}"
        fc.append(f"[{cur}]trim=0:{d},setpts=PTS-STARTPTS,format=yuva420p[b]")
        idx = len(c["clips"])
        # título grande com "pop"
        ins += ["-loop", "1", "-t", str(d), "-i", f"v2/t{n:02d}.png"]
        T = c["titulo_fim"]
        fc.append(f"[{idx}:v]format=rgba,scale=w='ceil(1080*min(1,0.78+0.22*t/0.16)/2)*2':h=-2:eval=frame,fade=t=out:st={T-0.18}:d=0.18:alpha=1[tt]")
        fc.append(f"[b][tt]overlay=x='(W-w)/2':y='(H-h)/2':enable='lt(t,{T})'[b2]")
        fc[-1] = fc[-1]; idx += 1
        cur = "b2"
    if c["layout"] == "CARD": cur = "b"
    # legendas com "pop"
    for j, cap in enumerate(c["caps"]):
        ins += ["-loop", "1", "-t", str(d), "-i", f"v2/l{n:02d}_{j}.png"]
        a = cap["ini"]
        fc.append(f"[{idx}:v]format=rgba,scale=w='ceil(1080*min(1,0.84+0.16*max(0,t-{a})/0.12)/2)*2':h=-2:eval=frame[l{j}]")
        ycap = 1150 if c["layout"] == "CARD" else 1180
        fc.append(f"[{cur}][l{j}]overlay=x='(W-w)/2':y='{ycap}+(360-h)/2':enable='between(t,{a},{cap['fim']})'[k{j}]")
        cur = f"k{j}"; idx += 1
    fc.append(f"[{cur}]format=yuv420p,fade=t=in:st=0:d=0.14:color=white[out]")
    out = f"v2/s{n:02d}.mp4"
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "[out]", "-t", str(d), "-an",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-r", "30", "-pix_fmt", "yuv420p", out], capture_output=True, text=True)
    if r.returncode: print("ERRO cena", n, r.stderr[-1500:]); raise SystemExit(1)
    lista.append(f"file 's{n:02d}.mp4'"); print("cena", n, "ok", flush=True)

open("v2/lista.txt", "w").write("\n".join(lista) + "\n")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "v2/lista.txt", "-c", "copy", "v2/sem_som.mp4"], check=True)
D = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", "v2/sem_som.mp4"], capture_output=True, text=True).stdout)
# narração (mesma da v1, alinhada por cena)
al = []
for c in plano:
    o = f"v2/a{c['n']:02d}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", c["voz"], "-af", f"adelay={int(c['pad_ini']*1000)},apad,atrim=0:{c['dur']}", "-ar", "48000", "-ac", "1", o], check=True)
    al.append(f"file 'a{c['n']:02d}.wav'")
open("v2/lista_a.txt", "w").write("\n".join(al) + "\n")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "v2/lista_a.txt", "-c", "pcm_s16le", "v2/voz.wav"], check=True)
# trilha a partir de 0:50 da faixa; quando acaba, emenda de novo a partir de 0:50 com crossfade
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "50", "-i", "m634.mp3", "-ss", "50", "-i", "m634.mp3", "-filter_complex",
                "[0:a][1:a]acrossfade=d=3[m]", "-map", "[m]", "v2/trilha.wav"], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "v2/sem_som.mp4", "-i", "v2/voz.wav", "-i", "v2/trilha.wav", "-filter_complex",
                f"[1:a]loudnorm=I=-16:TP=-1.5:LRA=11,aformat=channel_layouts=stereo[v];[2:a]atrim=0:{D},afade=t=in:d=0.8,afade=t=out:st={D-4:.2f}:d=4,volume=0.14[m];[v][m]amix=inputs=2:duration=first:normalize=0[a]",
                "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-t", str(D), "-movflags", "+faststart", "v2/vsl-v2.mp4"], check=True)
# legendas .srt
def ts(x):
    h, r = divmod(x, 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s-int(s))*1000)):03d}"
srt, k = [], 1
for c in plano:
    for cap in c["caps"]:
        srt.append(f"{k}\n{ts(c['inicio']+cap['ini'])} --> {ts(c['inicio']+cap['fim'])}\n{cap['texto']}\n"); k += 1
open("v2/vsl-v2.srt", "w").write("\n".join(srt))
print("duração", D)
