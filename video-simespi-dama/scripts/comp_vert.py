"""Versão vertical (Reels 1080x1920) do lançamento v10.
Reaproveita o roteiro de comp.py (mesmas batidas, cenas, textos e transições) e recompõe para o formato em pé:
- mosaicos: colunas quando as fontes são verticais, linhas quando são horizontais;
- painel de texto marinho entra por cima (desce), imagem abaixo;
- cartela com as três logos empilhadas.
Uso: comp_vert.py saida.mp4 [--preview] [--from T0 --to T1]"""
import os, sys, json, subprocess, math
import numpy as np, cv2
from PIL import Image, ImageDraw
S = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]
OUT = args[0]
PREVIEW = "--preview" in args
T_FROM = float(args[args.index("--from") + 1]) if "--from" in args else 0.0
T_TO = float(args[args.index("--to") + 1]) if "--to" in args else 58.0
sys.argv = ['comp.py', '--x']
g = {'__file__': f"{S}/comp.py", '__name__': 'x'}
exec(open(f"{S}/comp.py").read().replace('if __name__ == "__main__":\n    main()', ''), g)
W, HH, FPS = 1080, 1920, 30
g['W'], g['HH'] = W, HH
NAVY, CYAN, WHITE = g['NAVY'], g['CYAN'], g['WHITE']
ease, cover, frames, font, wrap_lines = g['ease'], g['cover'], g['frames'], g['font'], g['wrap_lines']
GAP = 8
PH = 700   # altura do painel de texto (topo)

# ---- mesmo trecho do brinde da v10 (taças com logos SIMESPI/35, câmera lenta)
F_ = g['F_']; SEQ = g['SEQ']
i0 = next(i for i, x in enumerate(SEQ) if x[0] == "full" and x[2][0] == "IMG_2600")
i1 = next(i for i, x in enumerate(SEQ) if x[0] == "hero")
SEQ[i0:i1] = [
    ("tri", 4, [F_("BRS_2808", 1.82), F_("BRS_2806", 2.20), F_("BRS_2805", 2.34)], "flash"),
    ("tri", 3, [F_("BRS_2806", 3.60), F_("BRS_2808", 3.20), F_("BRS_2805", 4.40)], "cut"),
    ("tri", 2, [F_("BRS_2805", 5.60), F_("BRS_2806", 4.40), F_("BRS_2808", 4.80)], "cut"),
]
_orig_src = g['src_path']
def src_path(name):
    if name.startswith("BRS_"): return f"{S}/v_br/{name}.mp4"
    return _orig_src(name)
g['src_path'] = src_path

_vert = {}
def is_vertical(name):
    if name not in _vert:
        p = src_path(name)
        if p.endswith(".jpg"):
            im = Image.open(p); _vert[name] = im.height > im.width
        else:
            info = g['probe'](p); _vert[name] = info['h'] > info['w']
    return _vert[name]

def L_panels(specs, n, w_, h_, grid=False):
    k = len(specs)
    if grid:   # 2x2
        pw = (w_ - 3 * GAP) // 2; ph = (h_ - 3 * GAP) // 2
        cells = [(GAP + (i % 2) * (pw + GAP), GAP + (i // 2) * (ph + GAP), pw, ph) for i in range(k)]
    elif sum(is_vertical(s[0]) for s in specs) * 2 > k:   # colunas
        pw = (w_ - GAP * (k + 1)) // k; ph = h_ - 2 * GAP
        cells = [(GAP + i * (pw + GAP), GAP, pw, ph) for i in range(k)]
    else:  # linhas
        pw = w_ - 2 * GAP; ph = (h_ - GAP * (k + 1)) // k
        cells = [(GAP, GAP + i * (ph + GAP), pw, ph) for i in range(k)]
    clips = []
    for s, (x, y, w, h) in zip(specs, cells):
        o = s[2] if len(s) > 2 else {}
        clips.append(frames(s[0], s[1], n, w, h, o.get("speed", 1.0), o.get("zoom", (1.0, 1.06)), o.get("focus", (0.5, 0.5))))
    out = []
    for i in range(n):
        c = np.zeros((h_, w_, 3), np.uint8); c[:] = NAVY
        for (x, y, w, h), cl in zip(cells, clips):
            off = 0 if i >= 3 else int((1 - ease(i / 3)) * (h * 0.12))
            f = cl[i]
            if off: c[y + off:y + h, x:x + w] = f[:h - off]
            else: c[y:y + h, x:x + w] = f
        out.append(c)
    return out

def render(kind, content, n, trans, nxt_whip, h_):
    g['W'], g['HH'] = W, h_
    try:
        if kind == "full":
            o = content[2] if len(content) > 2 else {}
            frs = frames(content[0], content[1], n, W, h_, o.get("speed", 1.0), o.get("zoom", (1.0, 1.04)), o.get("focus", (0.5, 0.5)))
        elif kind == "tri":
            c = content
            if h_ < 1500: c = content[1:]   # área baixa (painel aberto): só 2 painéis, inteiros
            frs = L_panels(c, n, W, h_)
        elif kind == "quad": frs = L_panels(content, n, W, h_, grid=True)
        elif kind == "hero": frs = g['L_hero'](content, n)
        if trans == "punch": frs = g['punch'](frs)
        elif trans == "flash": frs = g['flash'](g['punch'](frs, 5, 1.08))
        elif trans == "whip": frs = g['whip'](frs, "in", 1)
        if nxt_whip: frs = g['whip'](frs, "out", 1, 3)
    finally:
        g['W'], g['HH'] = W, HH
    return frs

def panel_text(img, tx, t, p):
    pil = Image.fromarray(img).convert("RGBA"); lay = Image.new("RGBA", pil.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    words = [w for ln in tx.lines for w in ln]; size = int(tx.size * 1.15)
    while True:
        fnt = font(tx.weight, size); lines = wrap_lines(words, fnt, W - 180, d)
        subh = 0
        if tx.sub:
            sf0 = font("SemiBold", int(size * 0.42)); subh = 20 + len(wrap_lines([(w, WHITE) for w in tx.sub.split()], sf0, W - 180, d)) * int(size * 0.52)
        if (len(lines) <= 4 and int(size * 1.12) * len(lines) + subh <= PH - 190) or size < 60: break
        size -= 4
    lh = int(size * 1.12); tot = lh * len(lines) + subh
    x0 = 90; y0 = int(PH / 2 - tot / 2 + 30 - (1 - p) * PH)
    fade = min(1, max(0, (tx.t1 - t) / 0.18)); k = 0
    bw = int(120 * ease(min(1, (t - tx.t0) / 0.3)))
    d.rectangle((x0, y0 - 40, x0 + bw, y0 - 29), fill=CYAN + (int(255 * fade),))
    for li, ln in enumerate(lines):
        x = x0; y = y0 + li * lh
        for w, col in ln:
            dt = t - tx.t0 - 0.12 - k * 0.05; k += 1; a = min(1, max(0, dt / 0.15)) * fade
            if a > 0:
                dy = int((1 - ease(min(1, dt / 0.2))) * 34)
                d.text((x, y + dy), w, font=fnt, fill=col + (int(255 * a),))
            x += d.textlength(w + " ", font=fnt)
    if tx.sub:
        sf_ = font("SemiBold", int(size * 0.42)); a = min(1, max(0, (t - tx.t0 - 0.35) / 0.2)) * fade
        sl = wrap_lines([(w, WHITE) for w in tx.sub.split()], sf_, W - 180, d)
        for j, ln in enumerate(sl):
            d.text((x0 + 2, y0 + lh * len(lines) + 14 + j * int(size * 0.52)), " ".join(w for w, _ in ln), font=sf_, fill=WHITE + (int(230 * a),))
    return np.array(Image.alpha_composite(pil, lay).convert("RGB"))

def compose_panel(fr, TX, t, alt=None):
    win = [w for w in g['panel_windows'](TX) if w[0] <= t < w[1]]
    if not win: return fr
    a, b = win[0]
    act = [tx for tx in TX if tx.t0 <= t < tx.t1]; tx = act[0] if act else None
    p = ease(min(1, max(0, (t - a) / 0.22))) * ease(min(1, max(0, (b - t) / 0.22)))
    y0 = int(PH * p)
    out = np.zeros_like(fr); out[:] = NAVY
    if HH - y0 > 0: out[y0:] = cover(alt, W, HH - y0, (0.5, 0.5)) if alt is not None else cover(fr, W, HH - y0, (0.5, 0.6))
    out[max(0, y0 - 6):y0] = CYAN
    if tx is not None: out = panel_text(out, tx, t, p)
    return out

LOGOS = [g['logo'](f"{g['B']}/simespi_small_crop.png", 190), g['logo'](f"{g['B']}/logo35_crop.png", 300), g['logo'](f"{g['B']}/Logo_Dama_Horizontal_t_crop.png", 190)]
IBI = g['IBI']
def card_frame(t):
    c = Image.new("RGBA", (W, HH), (255, 255, 255, 255))
    gap = 150; tot = sum(l.height for l in LOGOS) + 2 * gap; y = (HH - tot) // 2
    for i, lg in enumerate(LOGOS):
        dt = t - 0.10 - i * IBI / 2; a = min(1, max(0, dt / 0.18))
        if a > 0:
            s = 0.86 + 0.14 * (1 - (1 - min(1, dt / 0.3)) ** 3) + 0.04 * math.sin(min(1, dt / 0.3) * math.pi)
            im = lg.resize((max(1, int(lg.width * s)), max(1, int(lg.height * s))), Image.LANCZOS)
            im.putalpha(im.getchannel("A").point(lambda v: int(v * a)))
            c.alpha_composite(im, (int((W - im.width) / 2), int(y + (lg.height - im.height) / 2)))
        y += lg.height + gap
    fo = min(1, max(0, (t - 5.2) / 0.5))
    out = np.array(c.convert("RGB")).astype(np.float32)
    return (out * (1 - fo) + 255 * fo).astype(np.uint8)

def main():
    tl, kend = g['build_timeline']()
    card_t0 = g['tb'](kend); END = 58.0
    texts = json.load(open(f"{S}/n/texts.json"))
    TX = [g['Text'](**{**x, 'lines': [[(w, tuple(c)) for w, c in ln] for ln in x['lines']], 'pos': tuple(x['pos'])}) for x in texts]
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{HH}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-preset", "veryfast" if PREVIEW else "medium", "-crf", "26" if PREVIEW else "15",
                            "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", OUT], stdin=subprocess.PIPE)
    for idx, (t0, t1, kind, nb, content, trans) in enumerate(tl):
        if t1 <= T_FROM or t0 >= T_TO: continue
        f0, f1 = int(round(t0 * FPS)), int(round(t1 * FPS)); n = f1 - f0
        nxt = idx + 1 < len(tl) and tl[idx + 1][5] == "whip"
        frs = render(kind, content, n, trans, nxt, HH)
        overl = any(a < t1 and b > t0 for a, b in g['panel_windows'](TX))
        alt = render(kind, content, n, trans, nxt, HH - PH) if overl else None
        for i, fr in enumerate(frs):
            tt = (f0 + i) / FPS
            if not (T_FROM <= tt < T_TO): continue
            fr = compose_panel(fr, TX, tt, alt[i] if alt is not None else None)
            enc.stdin.write(np.ascontiguousarray(fr).tobytes())
        print(f"  {idx:02d} {t0:5.2f}-{t1:5.2f} {kind:5s} {trans}", flush=True)
    fidx = int(round(max(card_t0, T_FROM) * FPS))
    while fidx < int(min(END, T_TO) * FPS):
        tt = fidx / FPS; fr = card_frame(tt - card_t0)
        if tt - card_t0 < 0.12: fr = g['flash']([fr], 1, 0.4)[0]
        enc.stdin.write(fr.tobytes()); fidx += 1
    enc.stdin.close(); enc.wait(); print("ok", OUT)

main()
