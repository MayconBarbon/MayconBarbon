#!/usr/bin/env python3
"""Reel de teste v2 (evento Comida na Rua) com as regras do PiraBeer 2026, com mais efeitos das referências.
Trilha 120 BPM: batida = 0,5 s. A virada cai em R=4,5 s, o respiro vai de 68,5 a 76,5 e o clímax entra em 76,5.

Uso: montar_reel_v2.py WORK OUT TRILHA SFX_DIR [--so-final]

Velocidade: número (constante) ou tupla (a, s1, s2) para speed ramp, em que os primeiros `a` s da
timeline rodam a s1 e o restante a s2.
Flags (separadas por espaço):
  zo/zi = zoom-blur saindo/entrando        wo/wi = whip pan saindo/entrando
  fl = flash branco na entrada              pi = punch-in na batida
  sk = tremida de câmera                    ri = entrada com rotação
  bw = preto e branco                       hl = hyperlapse (motion blur por mistura de quadros)
"""
import subprocess, os, sys, json, hashlib
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.abspath(__file__))
BR = os.path.join(ROOT, "brutos")
LOGOS = os.path.join(ROOT, "..", "logos")
WORK, OUT, TRILHA, SFX = sys.argv[1:5]
os.makedirs(WORK, exist_ok=True)
FPS = 30
SRC = {"T01": "T01_693086FD.mov", "T02": "T02_709025AC.mov", "T03": "T03_IMG_9593.mov"}

EDL = [
    # GANCHO 0 a 4,5 (riser)
    ("T01", 46.00, 2.00, (0.5, 1.0, 0.45), "wo"),   # chope: ramp de normal para câmera lenta
    ("T01", 48.05, 1.25, 1.0, "wi pi"),             # brinde na direção da lente
    ("T02", 9.45, 1.25, 1.0, "zo"),                 # copos se encontrando
    # CONTEXTO 4,5 a 16,5
    ("T03", 0.30, 2.50, 1.0, "zi fl"),              # virada: drone de dia
    ("T03", 3.10, 1.00, 1.0, "zo"),                 # drone sobre a tenda
    ("T02", 0.20, 2.00, 1.0, "zi fl"),              # corte dia -> noite
    ("T01", 51.15, 2.50, 1.0, "wo"),                # tenda vista de cima
    ("T02", 5.55, 1.50, 1.0, "wi"),                 # palco aberto
    ("T02", 18.00, 1.50, 1.0, ""),                  # multidão sob a tenda
    ("T01", 14.10, 1.00, 1.0, "pi"),                # balcão com telões
    # EXPERIÊNCIAS 16,5 a 40,5
    ("T03", 29.92, 1.50, 1.0, ""),                  # público com copo
    ("T01", 4.70, 1.00, 1.0, "pi"),                 # balcão com copos
    ("T02", 23.95, 1.50, 1.0, ""),                  # cerveja servida
    ("T01", 38.95, 2.50, (0.75, 1.0, 0.45), "wo"),  # fogo: ramp para câmera lenta
    ("T01", 42.55, 1.00, 1.0, "wi"),                # corte da carne
    ("T03", 25.45, 1.00, 1.0, ""),                  # carne fatiada
    ("T03", 36.20, 0.50, 1.0, "pi"),                # chapa
    ("T03", 37.72, 0.50, 1.0, "pi"),                # pizza (match cut)
    ("T03", 39.05, 1.50, 1.0, ""),                  # pizza saindo nas mãos
    ("T02", 20.15, 0.50, 1.0, "pi"),                # sobremesa
    ("T03", 43.80, 0.50, 1.0, "pi"),                # doce
    ("T03", 46.92, 0.50, 1.0, "pi"),                # pote de doce (match cut)
    ("T03", 48.55, 1.00, 1.0, ""),                  # doce na mão
    ("T02", 28.72, 1.00, 1.0, "wo"),                # queijo em close
    ("T02", 33.72, 1.50, 1.0, "wi"),                # sorriso com a tigela
    ("T01", 36.30, 1.50, 1.0, ""),                  # balcão de comida
    ("T03", 27.85, 1.50, 1.0, "ri"),                # cerveja na mão (entrada com rotação)
    ("T01", 2.40, 1.00, 1.0, "pi"),                 # atendimento
    ("T02", 25.75, 1.50, 1.0, ""),                  # pedido no balcão
    ("T02", 13.75, 1.00, 1.0, "wo"),                # prato
    ("T03", 11.20, 1.50, 1.0, "wi"),                # público sob as árvores
    # PESSOAS 40,5 a 62,5
    ("T02", 6.98, 1.50, 1.0, ""),                   # abraço cantando
    ("T03", 14.18, 1.50, 1.0, ""),                  # pai dançando com a filha
    ("T01", 21.42, 0.50, 1.0, "pi"),                # brinde das amigas
    ("T03", 6.35, 1.00, 1.0, "wo"),                 # amigas dançando
    ("T02", 41.95, 1.50, 1.0, "wi"),                # risada dançando
    ("T01", 28.18, 1.00, 1.0, ""),                  # dança
    ("T03", 33.38, 1.00, 1.0, "pi"),                # brinde para a câmera
    ("T02", 36.08, 2.00, 1.0, ""),                  # público dançando
    ("T03", 68.02, 1.50, 1.0, "wo"),                # grupo dançando
    ("T02", 52.58, 1.50, 1.0, "wi"),                # dança
    ("T03", 72.22, 1.00, 1.0, ""),                  # casal
    ("T02", 54.65, 1.50, 1.0, ""),                  # selfie
    ("T03", 17.68, 1.50, 1.0, "wo"),                # braços para cima
    ("T03", 19.75, 1.00, 1.0, "wi"),                # amigas
    ("T03", 22.08, 2.00, 1.0, ""),                  # artista cumprimenta o público
    ("T01", 81.82, 1.00, 1.0, "pi"),                # dança
    ("T03", 61.68, 1.00, 1.0, ""),                  # celular filmando o show
    # PALCO 62,5 a 68,5
    ("T02", 3.05, 1.50, 1.0, "ri"),                 # cantora (entrada com rotação)
    ("T01", 30.72, 1.50, 1.0, "pi"),                # baixista
    ("T01", 25.70, 1.00, 1.0, "pi"),                # baterista
    ("T02", 48.50, 1.00, 1.0, "pi"),                # guitarrista
    ("T02", 38.60, 1.00, 1.0, "pi"),                # guitarrista no palco
    # RESPIRO 68,5 a 76,5 (pausa da trilha)
    ("T01", 7.20, 1.50, 0.5, "bw"),                 # cantora (P&B, lento)
    ("T02", 27.48, 1.50, 0.5, "bw"),
    ("T02", 40.78, 1.50, 0.5, "bw"),
    ("T03", 70.32, 1.50, 0.5, "bw"),
    ("T01", 64.75, 2.00, 2.0, "hl zo"),             # hyperlapse da tenda lotada até a virada
    # CLÍMAX 76,5 a 86,5
    ("T01", 72.35, 1.50, 1.0, "zi fl sk"),          # palco aberto, multidão
    # rajada stutter (8 x 1/4 de batida)
    ("T01", 23.42, 0.125, 1.0, ""), ("T01", 77.22, 0.125, 1.0, ""),
    ("T01", 23.55, 0.125, 1.0, ""), ("T01", 77.35, 0.125, 1.0, ""),
    ("T01", 23.68, 0.125, 1.0, ""), ("T01", 77.48, 0.125, 1.0, ""),
    ("T01", 23.81, 0.125, 1.0, ""), ("T01", 77.61, 0.125, 1.0, ""),
    ("T01", 70.18, 0.50, 1.0, "pi"),
    ("T01", 59.78, 0.50, 1.0, "pi"),
    ("T01", 78.60, 1.50, 1.0, "sk"),                # público visto do palco
    ("T01", 82.85, 1.00, 1.0, "wo"),
    ("T02", 46.38, 1.50, 1.0, "wi sk"),             # tenda lotada
    ("T01", 84.00, 1.50, 1.0, "pi"),
    ("T01", 63.38, 1.00, 1.0, "pi"),                # guitarra no vermelho
]
CARTELA = ("T01", 86.15, 2.95, 0.28)

GRADE = "eq=contrast=1.06:saturation=1.08:gamma=0.98,colorbalance=rs=0.03:gs=0.0:bs=-0.03:rm=0.02:bm=-0.02"
ZB = 0.2   # metade do zoom-blur (s)
WP = 0.15  # metade do whip pan (s)


def zc(z):
    """scale por quadro com fator z(t) e crop central 1080x1920"""
    return f"scale=w='trunc(1080*{z}/2)*2':h='trunc(1920*{z}/2)*2':eval=frame,crop=1080:1920"


def src_len(dur, speed):
    if isinstance(speed, tuple):
        a, s1, s2 = speed
        return a * s1 + (dur - a) * s2
    return dur * speed


def seg_filter(dur, speed, flags, extra=""):
    fl = flags.split()
    f = []
    if isinstance(speed, tuple):
        a, s1, s2 = speed
        u = "((PTS-STARTPTS)*TB)"
        f.append(f"setpts='if(lt({u},{a*s1}),{u}/{s1},{a}+({u}-{a*s1})/{s2})/TB'")
        slow = min(s1, s2) < 1
    else:
        f.append(f"setpts=(PTS-STARTPTS)/{speed}")
        slow = speed < 1
    if "hl" in fl:
        f.append("tmix=frames=4:weights='1 1 1 1'")
    if slow:
        f.append(f"minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1")
    f.append(f"fps={FPS},scale=1080:1920:flags=lanczos,setsar=1")
    f.append(GRADE)
    if "bw" in fl:
        f.append("hue=s=0,eq=contrast=1.12")
    if "pi" in fl:
        f.append(zc("(1+0.09*exp(-t*9))"))
    if "sk" in fl:
        f.append("scale=1166:2074,crop=1080:1920:x='43+22*sin(n*1.9)*sin(n*0.7)':y='77+22*cos(n*2.3)*sin(n*0.5)'")
    if "zo" in fl:
        s = dur - ZB
        f.append(zc(f"(1+0.35*pow(max(0,(t-{s})/{ZB}),2))"))
        f.append(f"gblur=sigma=6:enable='between(t,{s},{s+ZB/2})',gblur=sigma=16:enable='gte(t,{s+ZB/2})'")
    if "zi" in fl:
        f.append(zc(f"(1+0.35*pow(max(0,1-t/{ZB}),2))"))
        f.append(f"gblur=sigma=16:enable='lt(t,{ZB/2})',gblur=sigma=6:enable='between(t,{ZB/2},{ZB})'")
    if "wo" in fl:  # sai deslizando para a esquerda com borrão horizontal
        s = dur - WP
        p = f"pow(max(0,(t-{s})/{WP}),2)"
        f.append(f"scale=1404:2496,crop=1080:1920:x='162+162*{p}':y=288")
        f.append(f"avgblur=sizeX=24:sizeY=1:enable='between(t,{s},{s+WP/2})',avgblur=sizeX=70:sizeY=1:enable='gte(t,{s+WP/2})'")
    if "wi" in fl:  # entra vindo da direita
        p = f"pow(max(0,1-t/{WP}),2)"
        f.append(f"scale=1404:2496,crop=1080:1920:x='162-162*{p}':y=288")
        f.append(f"avgblur=sizeX=70:sizeY=1:enable='lt(t,{WP/2})',avgblur=sizeX=24:sizeY=1:enable='between(t,{WP/2},{WP})'")
    if "ri" in fl:
        R = 0.25
        k = f"pow(max(0,1-t/{R}),2)"
        f.append(zc(f"(1+0.9*{k})"))
        f.append(f"rotate=a='-0.8*{k}':fillcolor=black")
        f.append(f"gblur=sigma=10:enable='lt(t,{R/2})'")
    if "fl" in fl:
        f.append("fade=t=in:st=0:d=0.18:color=white")
    if extra:
        f.append(extra)
    return ",".join(f)


def render(i, src, tin, dur, speed, flags, frames, extra=""):
    vf = seg_filter(dur, speed, flags, extra)
    key = hashlib.md5(json.dumps([src, tin, dur, speed, flags, frames, vf]).encode()).hexdigest()[:10]
    out = os.path.join(WORK, f"s{i:03d}_{key}.mp4")
    if os.path.exists(out):
        return out
    tmp = out + ".tmp.mp4"
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{tin:.3f}", "-t", f"{src_len(dur, speed) + 0.5:.3f}",
           "-i", os.path.join(BR, SRC[src]), "-an", "-vf", vf, "-frames:v", str(frames),
           "-c:v", "libx264", "-preset", "medium", "-crf", "12", "-pix_fmt", "yuv420p",
           "-r", str(FPS), tmp]
    subprocess.run(cmd, check=True)
    n = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
                            "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", tmp],
                           capture_output=True, text=True).stdout.strip())
    assert n == frames, (i, n, frames)
    os.rename(tmp, out)
    return out


jobs, t, bounds = [], 0.0, []
for i, (src, tin, dur, sp, fl) in enumerate(EDL):
    a, b = round(t * FPS), round((t + dur) * FPS)
    jobs.append((i, src, tin, dur, sp, fl, b - a))
    bounds.append((t, t + dur, fl))
    t += dur
CONTENT_END = t
src, tin, dur, sp = CARTELA
cart_frames = round((t + dur) * FPS) - round(t * FPS)
jobs.append((len(EDL), src, tin, dur, sp, "", cart_frames,
             "colorchannelmixer=rr=0.5:gg=0.5:bb=0.5,gblur=sigma=2"))
TOTAL = t + dur
assert abs(CONTENT_END - 86.5) < 1e-6, CONTENT_END
print(f"conteúdo {CONTENT_END:.2f}s, total {TOTAL:.2f}s, {len(jobs)} segmentos", flush=True)

if "--so-final" not in sys.argv:
    with ThreadPoolExecutor(max_workers=6) as ex:
        outs = list(ex.map(lambda j: render(*j), jobs))
    with open(os.path.join(WORK, "lista.txt"), "w") as fh:
        fh.writelines(f"file '{o}'\n" for o in outs)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i",
                    os.path.join(WORK, "lista.txt"), "-c", "copy", os.path.join(WORK, "video.mp4")], check=True)

# ---------- trilha: peças separadas (atrim repetido sobre a mesma entrada corta a trilha) ----------
D = 0.012
full = os.path.join(WORK, "trilha_full.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", TRILHA, "-ar", "48000", full], check=True)
pecas = []
for nome, a, b in (("a", 11.55, 88.05 + D), ("b", 16.05, 26.05 + D), ("c", 88.05, 91.0)):
    pp = os.path.join(WORK, f"trilha_{nome}.wav"); pecas.append(pp)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", full, "-af", f"atrim={a}:{b},asetpts=PTS-STARTPTS", pp], check=True)
musica = os.path.join(WORK, "musica.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", pecas[0], "-i", pecas[1], "-i", pecas[2], "-filter_complex",
                f"[0][1]acrossfade=d={D}:c1=tri:c2=tri[ab];[ab][2]acrossfade=d={D}:c1=tri:c2=tri,"
                f"aresample=48000,asetpts=N/SR/TB,atrim=0:{TOTAL:.3f}[o]", "-map", "[o]", musica], check=True)

# ---------- efeitos sonoros ----------
ev = []  # (arquivo, início, volume)
ev.append(("pour", 0.0, 0.55))
ev.append(("clink", 3.45, 0.7))
for (a, b, fl) in bounds:
    f_ = fl.split()
    if "zo" in f_ or "wo" in f_:
        ev.append(("whoosh", max(0, b - 0.32), 0.45))
    if "ri" in f_:
        ev.append(("whoosh", max(0, a - 0.2), 0.35))
for tt in (4.5, 76.5):
    ev.append(("impact", tt - 0.03, 0.8))
ev.append(("cheer", 76.6, 0.42))
ev.append(("cheer", 82.4, 0.32))
inputs, parts = [], []
for k, (nm, st, vol) in enumerate(ev):
    inputs += ["-i", os.path.join(SFX, nm + ".mp3")]
    ms = int(st * 1000)
    parts.append(f"[{k}]aresample=48000,volume={vol},adelay={ms}|{ms}[e{k}]")
fx = os.path.join(WORK, "sfx.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex",
                ";".join(parts) + ";" + "".join(f"[e{k}]" for k in range(len(ev))) +
                f"amix=inputs={len(ev)}:normalize=0:duration=longest,apad,atrim=0:{TOTAL:.3f}[o]",
                "-map", "[o]", "-ar", "48000", fx], check=True)

aud = os.path.join(WORK, "trilha.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", musica, "-i", fx, "-filter_complex",
                f"[1]volume=0.9[f];[0][f]amix=inputs=2:normalize=0:duration=first,"
                f"loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,asetpts=N/SR/TB,"
                f"afade=t=out:st={TOTAL - 0.6:.2f}:d=0.6,atrim=0:{TOTAL:.3f}[o]",
                "-map", "[o]", "-c:a", "pcm_s16le", aud], check=True)
dur_aud = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                "-of", "csv=p=0", aud], capture_output=True, text=True).stdout)
assert abs(dur_aud - TOTAL) < 0.05, f"trilha com {dur_aud:.2f}s, esperado {TOTAL:.2f}s"

# ---------- logos ----------
from PIL import Image
st = Image.open(os.path.join(LOGOS, "secretaria-turismo_branco.png")).convert("RGBA")
st = st.crop(st.getchannel("A").getbbox())
st.resize((390, round(st.height * 390 / st.width)), Image.LANCZOS).save(os.path.join(WORK, "wm.png"))
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
                "-crf", "18", "-r", str(FPS), "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
                "-movflags", "+faststart", OUT], check=True)
json.dump({"content_end": ce, "total": TOTAL, "segments": len(EDL), "sfx": ev},
          open(os.path.join(WORK, "info.json"), "w"), ensure_ascii=False, indent=1)
print("ok", OUT, flush=True)
