#!/usr/bin/env python3
"""Pizza do Bem 2018-2025 - renderização do slideshow.

Uso: python3 render.py <pasta_trabalho> <principal|loop> <saida.mp4> [workers]

Linha do tempo (30 fps, 1920x1080):
  * cada foto fica D segundos em tela + X segundos de cross dissolve;
  * Ken Burns alternado: zoom in 100->105% / zoom out 105->100%, centrado no
    grupo de rostos detectado (nunca empurra rostos para fora do quadro);
  * ano em destaque (centro) por ~2 s na primeira foto do bloco, depois
    identificação discreta no canto inferior esquerdo até o fim do bloco;
  * principal: fade-in curto da primeira foto, última foto ~4 s + fade out;
  * loop: sem abertura/encerramento, 2025 dissolve de volta para 2018.
"""
import json, math, os, subprocess, sys
from concurrent.futures import ProcessPoolExecutor
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1920, 1080, 30
D = 4.4            # tempo de cada foto (s) sem contar o dissolve
X = 0.8            # cross dissolve (s)
ZOOM = 1.05
FONT_BIG = "/usr/share/fonts/opentype/inter/InterDisplay-Light.otf"
FONT_SMALL = "/usr/share/fonts/opentype/inter/InterDisplay-Regular.otf"

# Ordem: abertura de cada bloco com foto que mostra o uniforme do ano, depois
# ordem cronológica (EXIF). O encerramento de 2025 é o registro coletivo das
# voluntárias de uniforme vinho.
WA = "WhatsApp_Image_2026-11-11_at_09.02.50"
OPENER = {2018: ["IMG_2529"],
          2019: [WA, WA + "_(1)", WA + "_(2)", WA + "_(3)", "IMG_4323"],
          2022: ["1L8A7852"], 2023: ["Cópia_de_IMG_0336"],
          2025: ["Cesar_Cinato_Foto_CasaRonald_MOEMA_2025_Pizza_Bem-5974"]}
# 2018 fecha com o grupo de voluntárias de rosa e passa ao grupo de preto de 2019.
CLOSER = {2018: [WA + "_(8)"], 2019: [WA + "_(5)", WA + "_(4)", WA + "_(7)", WA + "_(6)"],
          2025: ["Cesar_Cinato_Foto_CasaRonald_MOEMA_2025_Pizza_Bem-5767"]}
SHOW_YEAR = False   # cliente pediu o vídeo sem a identificação dos anos

WORK = sys.argv[1]
MODE = sys.argv[2]


def timeline():
    man = [r for r in json.load(open(os.path.join(WORK, "manifest.json"))) if r["status"] == "ok"]
    seq = []
    for y in sorted({r["year"] for r in man}):
        rs = sorted([r for r in man if r["year"] == y], key=lambda r: (r["exif_date"] or "9", r["file"]))
        key = lambda r: os.path.splitext(r["plate"])[0][5:]
        pick = lambda names: [r for n in names for r in rs if key(r) == n]
        op = pick(OPENER.get(y, [])); cl = pick(CLOSER.get(y, []))
        mid = [r for r in rs if r not in op and r not in cl]
        seq += op + mid + cl
    clips = []
    for i, r in enumerate(seq):
        clips.append(dict(plate=r["plate"], year=r["year"], focus=r["focus"],
                          zin=(i % 2 == 0), start=i * D))
    n = len(clips)
    if MODE == "principal":
        clips[-1]["hold"] = 4.6            # última foto ~4 s visível + fade out
        total = clips[-1]["start"] + X + clips[-1]["hold"]
    else:
        total = n * D                      # ciclo perfeito
    # blocos de ano
    blocks = []
    for c in clips:
        if not blocks or blocks[-1]["year"] != c["year"]:
            blocks.append(dict(year=c["year"], start=c["start"]))
    for b, nb in zip(blocks, blocks[1:] + [None]):
        b["end"] = nb["start"] if nb else total
    return clips, blocks, total


CLIPS, BLOCKS, TOTAL = timeline()
_cache = {}


def plate(name):
    if name not in _cache:
        if len(_cache) > 6:
            _cache.pop(next(iter(_cache)))
        im = Image.open(os.path.join(WORK, "plates", name)).convert("RGB")
        _cache[name] = im.resize((round(W * ZOOM), round(H * ZOOM)), Image.LANCZOS)
    return _cache[name]


def ease(u):
    return 0.5 - 0.5 * math.cos(math.pi * min(max(u, 0), 1))


def clip_frame(c, local, dur):
    """Ken Burns: janela de recorte na placa (1.05x) mapeada para 1920x1080."""
    u = local / dur
    s = 1 + (ZOOM - 1) * (u if c["zin"] else 1 - u)        # 1.00 -> 1.05 (zoom in)
    s = 1 + (s - 1) * 1.0
    pw, ph = W * ZOOM, H * ZOOM
    ww, wh = pw / s, ph / s                                 # janela na placa
    fx, fy = c["focus"]
    k = (s - 1) / (ZOOM - 1)                                # 0..1: quanto aproximar do foco
    cx = pw / 2 + (fx * pw - pw / 2) * k * 0.6
    cy = ph / 2 + (fy * ph - ph / 2) * k * 0.6
    cx = min(max(cx, ww / 2), pw - ww / 2); cy = min(max(cy, wh / 2), ph - wh / 2)
    a = ww / W; e = wh / H
    return plate(c["plate"]).transform((W, H), Image.AFFINE,
                                       (a, 0, cx - ww / 2, 0, e, cy - wh / 2), Image.BICUBIC)


def text_layer(txt, size, font, tracking, shadow):
    f = ImageFont.truetype(font, size)
    chars = list(txt); widths = [f.getlength(ch) for ch in chars]
    tw = int(sum(widths) + tracking * (len(chars) - 1)); asc, desc = f.getmetrics()
    pad = shadow * 4
    lay = Image.new("L", (tw + 2 * pad, asc + desc + 2 * pad), 0)
    d = ImageDraw.Draw(lay); x = pad
    for ch, w_ in zip(chars, widths):
        d.text((x, pad), ch, font=f, fill=255); x += w_ + tracking
    sh = lay.filter(ImageFilter.GaussianBlur(shadow))
    return np.asarray(lay, np.float32) / 255, np.asarray(sh, np.float32) / 255


_text = {}


def labels(year):
    if year not in _text:
        _text[year] = (text_layer(str(year), 210, FONT_BIG, 10, 16),
                       text_layer(str(year), 46, FONT_SMALL, 6, 5))
    return _text[year]


def composite(img, layer, x, y, alpha):
    if alpha <= 0.002:
        return
    t, sh = layer; h, w = t.shape
    reg = img[y:y + h, x:x + w]
    reg *= 1 - (sh * 0.55 * alpha)[..., None]               # sombra suave
    reg += (255 - reg) * (t * alpha)[..., None]             # texto branco


def ramp(t, a, b):
    return min(max((t - a) / (b - a), 0), 1)


def frame(fi):
    t = fi / FPS
    if MODE == "loop":
        t = (t + X) % TOTAL                                 # arquivo começa já em 2018 puro
    n = len(CLIPS); active = []
    for i, c in enumerate(CLIPS):
        dur = c.get("hold", D) + X
        local = t - c["start"]
        if MODE == "loop" and i == n - 1 and t < X:        # cauda de 2025 sobre o início
            local = t + TOTAL - c["start"]
        if 0 <= local < dur:
            active.append((-local, c, local, dur))          # o mais antigo primeiro
    active.sort(key=lambda z: z[0])
    acc = None
    for _, c, local, dur in active:
        im = np.asarray(clip_frame(c, local, dur), np.float32)
        acc = im if acc is None else acc * (1 - ramp(local, 0, X)) + im * ramp(local, 0, X)
    img = acc if acc is not None else np.zeros((H, W, 3), np.float32)
    # identificação dos anos
    for b in (BLOCKS if SHOW_YEAR else []):
        bs, be = b["start"], b["end"]
        tt = t
        if MODE == "loop" and b is BLOCKS[0] and t > TOTAL - X:
            tt = t - TOTAL
        big, small = labels(b["year"])
        # grande: entra 0.4 s após o início do bloco, ~2 s em destaque
        a_big = ramp(tt, bs + 0.4, bs + 1.1) * (1 - ramp(tt, bs + 2.7, bs + 3.4))
        # pequeno: entra quando o grande sai; sai junto com o dissolve do próximo bloco
        a_small = ramp(tt, bs + 3.3, bs + 4.0) * (1 - ramp(tt, be, be + X))
        if MODE == "principal" and b is BLOCKS[-1]:
            a_small *= 1 - ramp(tt, TOTAL - 2.4, TOTAL - 1.4)
        if a_big > 0:
            h, w = big[0].shape
            pad = 16 * 4
            composite(img, big, 72 - pad, H - 64 - h + pad, a_big)
        if a_small > 0:
            h, w = small[0].shape
            composite(img, small, 80 - 20, H - 64 - h + 20, a_small)
    if MODE == "principal":
        g = ramp(t, 0, 0.8) * (1 - ramp(t, TOTAL - 1.6, TOTAL))
        img *= g
    return np.clip(img + 0.5, 0, 255).astype(np.uint8)


def render_chunk(args):
    a, b, out = args
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-tune", "film",
           "-profile:v", "high", "-level", "4.2", "-pix_fmt", "yuv420p",
           "-x264-params", "keyint=60:min-keyint=30:vbv-maxrate=20000:vbv-bufsize=30000",
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
           "-color_range", "tv", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for fi in range(a, b):
        p.stdin.write(frame(fi).tobytes())
    p.stdin.close(); p.wait()
    return out


def main():
    out = sys.argv[3]; workers = int(sys.argv[4]) if len(sys.argv) > 4 else 4
    nf = int(round(TOTAL * FPS))
    if os.environ.get("PREVIEW"):                           # frames de conferência
        for s in os.environ["PREVIEW"].split(","):
            Image.fromarray(frame(int(float(s) * FPS))).save(f"{out}_{s}.jpg", quality=90)
        return
    tmp = out + ".parts"; os.makedirs(tmp, exist_ok=True)
    k = workers * 3; step = math.ceil(nf / k)
    jobs = [(i, min(i + step, nf), os.path.join(tmp, f"{j:03d}.mp4"))
            for j, i in enumerate(range(0, nf, step))]
    with ProcessPoolExecutor(workers) as ex:
        parts = list(ex.map(render_chunk, jobs))
    lst = os.path.join(tmp, "list.txt")
    open(lst, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", lst, "-c", "copy", "-movflags", "+faststart", out], check=True)
    # linha do tempo editável (EDL simples)
    with open(os.path.splitext(out)[0] + "_timeline.csv", "w") as f:
        f.write("ordem;ano;placa;inicio_s;duracao_s;movimento\n")
        for i, c in enumerate(CLIPS):
            f.write(f"{i+1};{c['year']};{c['plate']};{c['start']:.2f};{c.get('hold', D) + X:.2f};"
                    f"{'zoom in 100-105%' if c['zin'] else 'zoom out 105-100%'}\n")
    print(out, nf, "frames", f"{TOTAL:.1f}s")


if __name__ == "__main__":
    main()
