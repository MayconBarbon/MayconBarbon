#!/usr/bin/env python3
"""Montagem do reel de teste (evento Comida na Rua) com as regras do PiraBeer 2026.
Trilha 120 BPM: batida = 0,5 s. A virada da trilha cai em R=4,5 s."""
import subprocess, os, sys, json
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.abspath(__file__))
BR = os.path.join(ROOT, "brutos")
LOGOS = os.path.join(ROOT, "..", "logos")
WORK = sys.argv[1]
OUT = sys.argv[2]
TRILHA = sys.argv[3]
os.makedirs(WORK, exist_ok=True)
FPS = 30
SRC = {"T01": "T01_693086FD.mov", "T02": "T02_709025AC.mov", "T03": "T03_IMG_9593.mov"}

# (arquivo, entrada no bruto, duração na timeline, velocidade, flags)
# flags: bw = preto e branco, zo = zoom-blur saindo, zi = zoom-blur entrando
EDL = [
    # GANCHO 0 a 4,5 (riser da trilha)
    ("T01", 46.00, 2.00, 0.6, ""),        # chope saindo da torneira, câmera lenta
    ("T01", 48.05, 1.25, 1.0, ""),        # brinde na direção da lente
    ("T02", 9.45, 1.25, 1.0, "zo"),       # copos se encontrando
    # CONTEXTO 4,5 a 16,5 (virada)
    ("T03", 0.30, 2.50, 1.0, "zi"),       # drone de dia sobre a cidade
    ("T03", 3.10, 1.00, 1.0, "zo"),       # drone sobre a tenda
    ("T02", 0.20, 2.00, 1.0, "zi"),       # corte dia -> noite: drone noturno
    ("T01", 51.15, 2.50, 1.0, ""),        # tenda vista de cima, público
    ("T02", 5.55, 1.50, 1.0, ""),         # palco aberto com público
    ("T02", 18.00, 1.50, 1.0, ""),        # multidão sob a tenda
    ("T01", 13.75, 1.00, 1.0, ""),        # teto da tenda iluminado
    # EXPERIÊNCIAS 16,5 a 40,5
    ("T03", 29.75, 1.50, 1.0, ""),        # copo de cerveja em close
    ("T01", 4.70, 1.00, 1.0, ""),         # balcão com copos
    ("T02", 23.70, 1.50, 1.0, ""),        # cerveja passando de mão em mão
    ("T01", 38.95, 2.50, 0.75, ""),       # fogo na grelha, lento
    ("T01", 42.55, 1.00, 1.0, ""),        # corte da carne
    ("T03", 25.45, 1.00, 1.0, ""),        # carne fatiada
    ("T03", 36.20, 0.50, 1.0, ""),        # chapa (sequência rápida)
    ("T03", 37.72, 0.50, 1.0, ""),        # pizza
    ("T02", 20.15, 0.50, 1.0, ""),        # sobremesa
    ("T03", 43.80, 0.50, 1.0, ""),        # doce
    ("T03", 46.92, 0.50, 1.0, ""),        # pote de doce
    ("T02", 28.72, 1.00, 1.0, ""),        # queijo em close
    ("T02", 33.72, 1.50, 1.0, ""),        # sorriso com a tigela
    ("T03", 39.05, 1.50, 1.0, ""),        # pizza saindo
    ("T01", 36.30, 1.50, 1.0, ""),        # balcão de comida
    ("T03", 27.85, 1.50, 1.0, ""),        # cerveja na mão
    ("T01", 2.40, 1.00, 1.0, ""),         # atendimento
    ("T02", 25.75, 1.50, 1.0, ""),        # pedido no balcão
    ("T03", 48.55, 1.00, 1.0, ""),        # doce na mão
    ("T02", 13.75, 1.00, 1.0, ""),        # prato
    ("T03", 11.20, 1.50, 1.0, ""),        # público sob as árvores
    # PESSOAS 40,5 a 62,5
    ("T02", 6.98, 1.50, 1.0, ""),         # abraço cantando
    ("T03", 14.18, 1.50, 1.0, ""),        # pai dançando com a filha
    ("T01", 20.72, 0.50, 1.0, ""),        # brinde
    ("T03", 6.35, 1.00, 1.0, ""),         # amigas dançando
    ("T02", 41.95, 1.50, 1.0, ""),        # risada dançando
    ("T01", 28.18, 1.00, 1.0, ""),        # dança
    ("T03", 33.38, 1.00, 1.0, ""),        # brinde para a câmera
    ("T02", 36.08, 2.00, 1.0, ""),        # público dançando
    ("T03", 68.02, 1.50, 1.0, ""),        # grupo dançando
    ("T02", 52.58, 1.50, 1.0, ""),        # dança
    ("T03", 72.22, 1.00, 1.0, ""),        # casal
    ("T02", 54.65, 1.50, 1.0, ""),        # selfie
    ("T03", 17.68, 1.50, 1.0, ""),        # braços para cima
    ("T03", 19.75, 1.00, 1.0, ""),        # amigas dançando
    ("T03", 22.08, 2.00, 1.0, ""),        # artista cumprimentando o público
    ("T01", 81.82, 1.00, 1.0, ""),        # dança
    ("T03", 61.68, 1.00, 1.0, ""),        # celular filmando o show
    # PALCO 62,5 a 68,5
    ("T02", 3.05, 1.50, 1.0, ""),         # cantora
    ("T01", 30.72, 1.50, 1.0, ""),        # guitarrista
    ("T01", 22.32, 1.00, 1.0, ""),        # bateria com fumaça
    ("T02", 48.50, 1.00, 1.0, ""),        # guitarrista
    ("T02", 38.60, 1.00, 1.0, ""),        # guitarrista no palco
    # RESPIRO 68,5 a 76,5 (pausa da trilha, P&B em câmera lenta)
    ("T01", 21.42, 1.50, 0.5, "bw"),
    ("T02", 27.48, 1.50, 0.5, "bw"),
    ("T02", 40.78, 1.50, 0.5, "bw"),
    ("T03", 70.32, 1.50, 0.5, "bw"),
    ("T01", 64.75, 2.00, 1.0, "zo"),      # cor volta: tenda lotada
    # CLÍMAX 76,5 a 86,5
    ("T01", 72.35, 1.50, 1.0, "zi"),      # palco aberto à noite, multidão
    ("T01", 23.42, 0.50, 1.0, ""),
    ("T01", 70.18, 0.50, 1.0, ""),
    ("T01", 77.22, 0.50, 1.0, ""),
    ("T01", 59.78, 0.50, 1.0, ""),
    ("T01", 78.60, 1.50, 1.0, ""),        # público visto do palco
    ("T01", 82.85, 1.00, 1.0, ""),
    ("T02", 46.38, 1.50, 1.0, ""),        # tenda lotada
    ("T01", 84.00, 1.50, 1.0, ""),
    ("T01", 63.38, 1.00, 1.0, ""),        # guitarra no vermelho
]
CARTELA = ("T01", 86.15, 2.95, 0.28)      # drone noturno sobre a catedral, escurecido (plano limpo, antes da transição do CapCut)

GRADE = "eq=contrast=1.06:saturation=1.08:gamma=0.98,colorbalance=rs=0.03:gs=0.0:bs=-0.03:rm=0.02:bm=-0.02"
ZB = 0.2  # duração de cada metade do zoom-blur (s)


def seg_filter(dur, speed, flags, extra=""):
    f = [f"setpts=(PTS-STARTPTS)/{speed}"]
    if speed < 1:
        f.append(f"minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1")
    f.append(f"fps={FPS},scale=1080:1920:flags=lanczos,setsar=1")
    f.append(GRADE)
    if "bw" in flags:
        f.append("hue=s=0,eq=contrast=1.12")
    if "zo" in flags:
        s = dur - ZB
        z = f"(1+0.35*pow(max(0,(t-{s})/{ZB}),2))"
        f.append(f"scale=w='trunc(1080*{z}/2)*2':h='trunc(1920*{z}/2)*2':eval=frame,crop=1080:1920")
        f.append(f"gblur=sigma=6:enable='between(t,{s},{s+ZB/2})',gblur=sigma=16:enable='gte(t,{s+ZB/2})'")
    if "zi" in flags:
        z = f"(1+0.35*pow(max(0,1-t/{ZB}),2))"
        f.append(f"scale=w='trunc(1080*{z}/2)*2':h='trunc(1920*{z}/2)*2':eval=frame,crop=1080:1920")
        f.append(f"gblur=sigma=16:enable='lt(t,{ZB/2})',gblur=sigma=6:enable='between(t,{ZB/2},{ZB})'")
    if extra:
        f.append(extra)
    return ",".join(f)


def render(i, src, tin, dur, speed, flags, frames, extra=""):
    out = os.path.join(WORK, f"s{i:03d}.mp4")
    srcdur = dur * speed + 0.5
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{tin:.3f}", "-t", f"{srcdur:.3f}",
           "-i", os.path.join(BR, SRC[src]), "-an",
           "-vf", seg_filter(dur, speed, flags, extra), "-frames:v", str(frames),
           "-c:v", "libx264", "-preset", "medium", "-crf", "12", "-pix_fmt", "yuv420p",
           "-r", str(FPS), out]
    subprocess.run(cmd, check=True)
    n = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
                            "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", out],
                           capture_output=True, text=True).stdout.strip())
    assert n == frames, (i, n, frames)
    return out


# quadros por segmento a partir de tempos acumulados (sem deriva)
jobs, t = [], 0.0
for i, (src, tin, dur, sp, fl) in enumerate(EDL):
    a, b = round(t * FPS), round((t + dur) * FPS)
    jobs.append((i, src, tin, dur, sp, fl, b - a))
    t += dur
CONTENT_END = t
src, tin, dur, sp = CARTELA
cart_frames = round((t + dur) * FPS) - round(t * FPS)
jobs.append((len(EDL), src, tin, dur, sp, "", cart_frames,
             "colorchannelmixer=rr=0.5:gg=0.5:bb=0.5,gblur=sigma=2"))
TOTAL = t + dur
print(f"conteúdo {CONTENT_END:.2f}s, total {TOTAL:.2f}s, {len(jobs)} segmentos")

with ThreadPoolExecutor(max_workers=6) as ex:
    outs = list(ex.map(lambda j: render(*j), jobs))
with open(os.path.join(WORK, "lista.txt"), "w") as fh:
    fh.writelines(f"file '{o}'\n" for o in outs)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i",
                os.path.join(WORK, "lista.txt"), "-c", "copy", os.path.join(WORK, "video.mp4")], check=True)

# trilha: [11,55 a 88,05] + [16,05 a 26,05] (virada de novo no clímax) + [88,05 a 91,0] (acorde final)
D = 0.012
aud = os.path.join(WORK, "trilha.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", TRILHA, "-filter_complex",
    f"[0]atrim={11.55}:{88.05 + D},asetpts=PTS-STARTPTS[a];"
    f"[0]atrim={16.05}:{26.05 + D},asetpts=PTS-STARTPTS[b];"
    f"[0]atrim={88.05}:{91.0},asetpts=PTS-STARTPTS[c];"
    f"[a][b]acrossfade=d={D}:c1=tri:c2=tri[ab];[ab][c]acrossfade=d={D}:c1=tri:c2=tri,"
    f"aresample=48000,loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=out:st={TOTAL - 0.6:.2f}:d=0.6,"
    f"atrim=0:{TOTAL:.3f}[o]", "-map", "[o]", "-c:a", "pcm_s16le", aud], check=True)

# logos
from PIL import Image
st = Image.open(os.path.join(LOGOS, "secretaria-turismo_branco.png")).convert("RGBA")
st = st.crop(st.getchannel("A").getbbox())
wm = st.resize((390, round(st.height * 390 / st.width)), Image.LANCZOS)
wm.save(os.path.join(WORK, "wm.png"))
pb = Image.open(os.path.join(LOGOS, "pirabeer_4ed_branco_transparente.png")).convert("RGBA")
pb = pb.crop(pb.getchannel("A").point(lambda p: 255 if p > 8 else 0).getbbox())
card = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
pw = 640; pbr = pb.resize((pw, round(pb.height * pw / pb.width)), Image.LANCZOS)
sw = 500; str_ = st.resize((sw, round(st.height * sw / st.width)), Image.LANCZOS)
gap = 120
top = (1920 - (pbr.height + gap + str_.height)) // 2 - 40
card.alpha_composite(pbr, ((1080 - pw) // 2, top))
card.alpha_composite(str_, ((1080 - sw) // 2, top + pbr.height + gap))
card.save(os.path.join(WORK, "cartela.png"))

ce = CONTENT_END
fc = (f"[1]format=rgba,colorchannelmixer=aa=0.8[wm];"
      f"[0][wm]overlay=x=W-w-68:y=150:enable='lt(t,{ce:.3f})'[v1];"
      f"[2]format=rgba,fade=t=in:st={ce + 0.1:.3f}:d=0.45:alpha=1,fade=t=out:st={TOTAL - 0.5:.3f}:d=0.5:alpha=1[cd];"
      f"[v1][cd]overlay=0:0:enable='gte(t,{ce:.3f})',fade=t=out:st={TOTAL - 0.35:.3f}:d=0.35,format=yuv420p[v]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(WORK, "video.mp4"),
                "-loop", "1", "-i", os.path.join(WORK, "wm.png"),
                "-loop", "1", "-framerate", str(FPS), "-i", os.path.join(WORK, "cartela.png"),
                "-i", aud, "-filter_complex", fc, "-map", "[v]", "-map", "3:a",
                "-t", f"{TOTAL:.3f}", "-c:v", "libx264", "-profile:v", "high", "-preset", "slow",
                "-crf", "17", "-r", str(FPS), "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
                "-movflags", "+faststart", OUT], check=True)
json.dump({"content_end": ce, "total": TOTAL, "segments": len(EDL)}, open(os.path.join(WORK, "info.json"), "w"))
print("ok", OUT)
