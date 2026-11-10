"""Compositor quadro a quadro — SIMESPI x Dama Bier (lançamento, 16:9, <=60 s).
Monta cortes no compasso da trilha, mosaicos, zooms, whips, tipografia animada e cartela."""
import os, sys, json, subprocess, math, glob
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = os.path.dirname(os.path.abspath(__file__))
H, V, B, F, N = f"{S}/h", f"{S}/v", f"{S}/brand", f"{S}/fonts", f"{S}/n"
W, HH, FPS = 1920, 1080, 30
OUT = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else f"{S}/out/v6_video.mp4"
PREVIEW = '--preview' in sys.argv
NAVY = (10, 54, 67); BLUE = (39, 110, 132); CYAN = (59, 185, 216); WHITE = (255, 255, 255)

beats = json.load(open(f"{N}/beats.json"))
B0, IBI = 0.511, beats["ibi"]
def bt(b): return 0.0 if b == 0 else B0 + (b - 1) * IBI * 1.0 if False else B0 + b * IBI - (0 if b else 0)
def T(b): return 0.0 if b <= 0 else B0 + (b - 1) * IBI + IBI * 0  # beat b (1-based after first)
# grade simples: tempo do beat k (k=0 -> 0.0 ; k>=1 -> 0.511 + (k-1)*IBI)
def tb(k): return 0.0 if k == 0 else B0 + (k - 1) * IBI

TM = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,"
      "zscale=t=bt709:m=bt709:r=tv,format=yuv420p,eq=gamma=1.05:saturation=1.06:contrast=1.03")
ROT = {"IMG_2608": 4.3, "IMG_2652": 4.0, "root_IMG_1184": -3.0}

def src_path(name):
    for d, exts in ((H, (".mov", ".MOV", ".mp4", ".jpg")), (V, (".mov", ".MOV", ".MP4", ".mp4"))):
        for e in exts:
            p = f"{d}/{name}{e}"
            if os.path.exists(p): return p
    raise FileNotFoundError(name)

def probe(p):
    o = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                 "stream=width,height,color_transfer:stream_side_data=rotation:format=duration", "-of", "json", p])
    j = json.loads(o); st = j["streams"][0]; rot = 0
    for sd in st.get("side_data_list", []) or []:
        if "rotation" in sd: rot = int(sd["rotation"])
    w, h = st["width"], st["height"]
    if abs(rot) == 90: w, h = h, w
    return dict(w=w, h=h, hdr=st.get("color_transfer") == "arib-std-b67", dur=float(j["format"]["duration"]))

_cache = {}
def frames(name, t0, n, w, h, speed=1.0, zoom=(1.0, 1.0), focus=(0.5, 0.5)):
    """Decodifica n quadros a partir de t0 (velocidade 'speed'), recortados p/ cobrir w x h."""
    p = src_path(name)
    if p.endswith(".jpg"):
        im = Image.open(p).convert("RGB")
        im = cover(np.array(im), int(w * 1.15), int(h * 1.15), focus)
        out = []
        for i in range(n):
            z = 1.0 + 0.12 * i / max(1, n - 1)
            out.append(zoom_img(im, z, w, h))
        return out
    info = probe(p)
    span = n / FPS * speed + 0.15
    t0 = max(0.0, min(t0, info["dur"] - span))
    vf = (TM + "," if info["hdr"] else "format=yuv420p,")
    if name in ROT:
        a = ROT[name]; sc = math.cos(math.radians(abs(a))) + (16 / 9) * math.sin(math.radians(abs(a)))
        vf += f"rotate={a}*PI/180:ow=iw:oh=ih,scale=iw*{sc:.3f}:ih*{sc:.3f},crop={info['w']}:{info['h']},"
    vf += f"setpts=PTS/{speed},fps={FPS},format=rgb24"
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-t", f"{span:.3f}", "-i", p, "-vf", vf,
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    raw = subprocess.run(cmd, stdout=subprocess.PIPE, check=True).stdout
    sw, sh = info["w"], info["h"]
    fs = np.frombuffer(raw, np.uint8).reshape(-1, sh, sw, 3)
    if len(fs) == 0: raise RuntimeError(f"sem quadros: {name}")
    out = []
    for i in range(n):
        f = fs[min(i, len(fs) - 1)]
        z = zoom[0] + (zoom[1] - zoom[0]) * ease(i / max(1, n - 1))
        out.append(cover(f, w, h, focus, z))
    return out

def ease(x): return 0.5 - 0.5 * math.cos(math.pi * min(1, max(0, x)))
def cover(img, w, h, focus=(0.5, 0.5), z=1.0):
    ih, iw = img.shape[:2]
    s = max(w / iw, h / ih) * z
    nw, nh = int(round(iw * s)), int(round(ih * s))
    r = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC)
    x = int((nw - w) * focus[0]); y = int((nh - h) * focus[1])
    return np.ascontiguousarray(r[y:y + h, x:x + w])
def zoom_img(img, z, w, h):
    ih, iw = img.shape[:2]; cw, ch = iw / z, ih / z
    x0, y0 = (iw - cw) / 2, (ih - ch) / 2
    M = np.array([[w / cw, 0, -x0 * w / cw], [0, h / ch, -y0 * h / ch]], np.float32)
    return cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

# ---------------- layouts
GAP = 8
def L_full(spec, n):
    name, t0 = spec[0], spec[1]; o = spec[2] if len(spec) > 2 else {}
    return frames(name, t0, n, W, HH, o.get("speed", 1.0), o.get("zoom", (1.0, 1.04)), o.get("focus", (0.5, 0.5)))

def L_vcenter(spec, n):
    """vertical no centro + fundo desfocado do próprio clipe (marca: faixas ciano)."""
    name, t0 = spec[0], spec[1]; o = spec[2] if len(spec) > 2 else {}
    pw = int(HH * 9 / 16)
    fg = frames(name, t0, n, pw, HH, o.get("speed", 1.0), o.get("zoom", (1.0, 1.05)), o.get("focus", (0.5, 0.5)))
    out = []
    for i, f in enumerate(fg):
        bg = cv2.resize(f, (W // 8, HH // 8)); bg = cv2.GaussianBlur(bg, (0, 0), 6)
        bg = cv2.resize(bg, (W, HH), interpolation=cv2.INTER_LINEAR)
        bg = (bg.astype(np.float32) * 0.45 + np.array(NAVY, np.float32) * 0.25).clip(0, 255).astype(np.uint8)
        x = (W - pw) // 2; bg[:, x:x + pw] = f
        bg[:, x - 6:x - 2] = CYAN; bg[:, x + pw + 2:x + pw + 6] = CYAN
        out.append(bg)
    return out

def L_panels(specs, n, rows=1):
    """mosaico de k painéis (verticais lado a lado, ou 2x2)."""
    k = len(specs); canvas = []
    if rows == 1:
        pw = (W - GAP * (k + 1)) // k; ph = HH - 2 * GAP
        cells = [(GAP + i * (pw + GAP), GAP, pw, ph) for i in range(k)]
    else:
        pw = (W - 3 * GAP) // 2; ph = (HH - 3 * GAP) // 2
        cells = [(GAP + (i % 2) * (pw + GAP), GAP + (i // 2) * (ph + GAP), pw, ph) for i in range(k)]
    clips = []
    for s, (x, y, w, h) in zip(specs, cells):
        name, t0 = s[0], s[1]; o = s[2] if len(s) > 2 else {}
        clips.append(frames(name, t0, n, w, h, o.get("speed", 1.0), (1.0, 1.06), o.get("focus", (0.5, 0.5))))
    for i in range(n):
        c = np.zeros((HH, W, 3), np.uint8); c[:] = NAVY
        for j, ((x, y, w, h), cl) in enumerate(zip(cells, clips)):
            # entrada escalonada: painel desliza de baixo nos 5 primeiros quadros
            d = i - j; off = 0 if d >= 4 else int((1 - ease(max(0, d) / 4)) * (h * 0.35))
            if d < 0: continue
            f = cl[i]
            if off: c[y + off:y + h, x:x + w] = f[:h - off]
            else: c[y:y + h, x:x + w] = f
        canvas.append(c)
    return canvas

# ---------------- transições
def whip(frs, side, direction=1, k=4):
    """aplica saída/entrada em chicote (deslocamento + borrão de movimento)."""
    n = len(frs)
    for j in range(min(k, n)):
        i = n - 1 - j if side == "out" else j
        a = (k - j) / k
        shift = int(direction * a * a * W * 0.55) * (-1 if side == "out" else 1)
        f = frs[i].astype(np.float32); acc = np.zeros_like(f)
        taps = 7
        for t in range(taps):
            dx = shift + int(direction * a * 160 * (t - taps // 2) / taps)
            acc += np.roll(f, dx, axis=1)
        frs[i] = (acc / taps).astype(np.uint8)
    return frs

def punch(frs, k=6, z0=1.12):
    for i in range(min(k, len(frs))):
        z = z0 - (z0 - 1.0) * ease(i / k)
        frs[i] = zoom_img(frs[i], z, W, HH)
    return frs

def flash(frs, k=3, amt=0.55):
    for i in range(min(k, len(frs))):
        a = amt * (1 - i / k)
        frs[i] = (frs[i].astype(np.float32) * (1 - a) + 255 * a).astype(np.uint8)
    return frs

# ---------------- tipografia
FONT = {w: f"{F}/Montserrat-{w}.ttf" for w in ("Black", "ExtraBold", "Bold", "SemiBold", "Medium")}
def font(w, s): return ImageFont.truetype(FONT[w], s)

class Text:
    """linhas: lista de listas de (palavra, cor). anima palavra a palavra."""
    def __init__(self, t0, t1, lines, size=86, weight="Black", pos=("left", 0.70), box=False, sub=None):
        self.t0, self.t1, self.lines, self.size, self.weight, self.pos, self.box, self.sub = t0, t1, lines, size, weight, pos, box, sub
    def draw(self, img, t):
        if not (self.t0 <= t < self.t1): return img
        pil = Image.fromarray(img).convert("RGBA")
        lay = Image.new("RGBA", pil.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        fnt = font(self.weight, self.size); lh = int(self.size * 1.08)
        widths = [sum(d.textlength(w + " ", font=fnt) for w, _ in ln) for ln in self.lines]
        tot_h = lh * len(self.lines)
        if self.pos[0] == "center": x0s = [(W - wd) / 2 for wd in widths]
        else: x0s = [120] * len(widths)
        y0 = int(HH * self.pos[1] - tot_h / 2)
        # sombra/vinheta de leitura
        sh = Image.new("RGBA", pil.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
        k = 0; fade_out = min(1, max(0, (self.t1 - t) / 0.18))
        for li, ln in enumerate(self.lines):
            x = x0s[li]; y = y0 + li * lh
            for w, col in ln:
                dt = t - self.t0 - k * 0.06; k += 1
                a = min(1, max(0, dt / 0.16)) * fade_out
                if a <= 0: x += d.textlength(w + " ", font=fnt); continue
                dy = int((1 - ease(min(1, dt / 0.22))) * 46)
                sd.text((x + 3, y + dy + 5), w, font=fnt, fill=(0, 0, 0, int(150 * a)))
                d.text((x, y + dy), w, font=fnt, fill=col + (int(255 * a),))
                x += d.textlength(w + " ", font=fnt)
        # barra ciano de assinatura
        bar_a = min(1, max(0, (t - self.t0) / 0.25)) * fade_out
        if self.pos[0] != "center":
            bw = int(90 * ease(min(1, (t - self.t0) / 0.3)))
            d.rectangle((120, y0 - 26, 120 + bw, y0 - 18), fill=CYAN + (int(255 * bar_a),))
        if self.sub:
            sf_ = font("SemiBold", int(self.size * 0.42)); dt = t - self.t0 - 0.25
            a = min(1, max(0, dt / 0.2)) * fade_out
            sx = x0s[0] if self.pos[0] != "center" else (W - d.textlength(self.sub, font=sf_)) / 2
            d.text((sx + 4, y0 + tot_h + 10), self.sub, font=sf_, fill=WHITE + (int(235 * a),))
        sh = sh.filter(ImageFilter.GaussianBlur(7))
        pil = Image.alpha_composite(pil, sh); pil = Image.alpha_composite(pil, lay)
        return np.array(pil.convert("RGB"))

def wd(s, col=WHITE): return [(w, col) for w in s.split()]

# ---------------- cartela final animada
def logo(path, h):
    im = Image.open(path).convert("RGBA"); im = im.crop(im.getbbox())
    return im.resize((round(im.width * h / im.height), h), Image.LANCZOS)
LOGOS = [logo(f"{B}/simespi_small_crop.png", 168), logo(f"{B}/logo35_crop.png", 270), logo(f"{B}/Logo_Dama_Horizontal_t_crop.png", 172)]
def card_frame(t):  # t desde o início da cartela
    c = Image.new("RGBA", (W, HH), (255, 255, 255, 255)); d = ImageDraw.Draw(c)
    gap = 120; tot = sum(l.width for l in LOGOS) + 2 * gap; x = (W - tot) // 2; cy = HH // 2 - 30
    for i, lg in enumerate(LOGOS):
        dt = t - 0.10 - i * IBI / 2  # entra no contratempo
        a = min(1, max(0, dt / 0.18))
        if a > 0:
            s = 0.86 + 0.14 * (1 - (1 - min(1, dt / 0.3)) ** 3) + 0.04 * math.sin(min(1, dt / 0.3) * math.pi)
            im = lg.resize((max(1, int(lg.width * s)), max(1, int(lg.height * s))), Image.LANCZOS)
            im.putalpha(im.getchannel("A").point(lambda v: int(v * a)))
            c.alpha_composite(im, (int(x + (lg.width - im.width) / 2), int(cy - im.height / 2)))
        x += lg.width + gap
    # linha ciano que cresce
    p = ease(min(1, max(0, (t - 0.6) / 0.5))); lw = int(760 * p)
    d.rectangle((W // 2 - lw // 2, cy + 175, W // 2 + lw // 2, cy + 181), fill=CYAN + (255,))
    f2 = font("Bold", 40); msg = "SIMESPI — 35 ANOS FORTALECENDO A INDÚSTRIA"; a = min(1, max(0, (t - 0.9) / 0.3))
    tw = d.textlength(msg, font=f2)
    d.text(((W - tw) / 2, cy + 205), msg, font=f2, fill=NAVY + (int(255 * a),))
    fo = min(1, max(0, (t - 5.2) / 0.5))
    out = np.array(c.convert("RGB")).astype(np.float32)
    return (out * (1 - fo) + 255 * fo).astype(np.uint8)

# =====================================================================
# ROTEIRO DE IMAGENS (em batidas da trilha; 1 batida = 0,488 s)
# tipo, batidas, conteúdo, transição de entrada
def F_(n, t, **o): return (n, t, o)
SEQ = [
    # ---- GANCHO (0–2,5 s): a novidade
    ("vcenter", 1, F_("IMG_2398", 1.0), "flash"),
    ("vcenter", 1, F_("IMG_2667", 1.5), "whip"),
    ("vcenter", 1, F_("IMG_2395", 0.3), "punch"),
    ("vcenter", 2, F_("08DC7867", 2.0, zoom=(1.0, 1.08)), "whip"),
    # ---- 1: uma cerveja criada para o SIMESPI
    ("vcenter", 2, F_("B399EA75", 5.0), "punch"),
    ("vcenter", 2, F_("IMG_2397", 6.0), "whip"),
    ("full", 2, F_("IMG_2655", 0.05, speed=0.8), "punch"),
    # ---- 2: parceria inédita — SIMESPI + Dama Bier
    ("full", 2, F_("IMG_2701", 0.2), "whip"),
    ("tri", 2, [F_("IMG_2699", 1.0), F_("IMG_2702", 1.5), F_("IMG_2607", 0.5)], "cut"),
    ("full", 1, F_("IMG_2606", 1.2), "punch"),
    ("full", 2, F_("IMG_2608", 2.2), "whip"),
    ("tri", 2, [F_("IMG_2609", 3.0), F_("IMG_2612", 2.0), F_("IMG_2618", 1.0)], "cut"),
    ("full", 1, F_("IMG_2611", 0.5), "punch"),
    # ---- 3: indústria / processos (1 batida cada)
    ("full", 1, F_("IMG_2669", 0.8), "whip"),
    ("full", 1, F_("IMG_2691", 0.6), "cut"),
    ("tri", 1, [F_("IMG_2670", 1.0), F_("IMG_2672", 3.0), F_("IMG_2674", 1.0)], "cut"),
    ("full", 1, F_("IMG_2694", 0.4), "punch"),
    ("full", 1, F_("IMG_2671", 6.2), "cut"),
    ("tri", 1, [F_("IMG_2689", 1.0), F_("IMG_2690", 3.0), F_("IMG_2692", 0.5)], "cut"),
    ("full", 1, F_("IMG_2677", 1.0), "whip"),
    ("full", 1, F_("IMG_2675", 2.2), "cut"),
    ("tri", 1, [F_("IMG_2678", 2.0), F_("IMG_2679", 1.0), F_("IMG_2680", 2.0)], "cut"),
    ("full", 1, F_("IMG_2676", 5.6), "punch"),
    ("full", 1, F_("IMG_2682", 0.6), "cut"),
    ("tri", 1, [F_("IMG_2681", 1.0), F_("IMG_2684", 2.0), F_("IMG_2685", 0.5)], "cut"),
    ("full", 1, F_("IMG_2683", 0.5), "whip"),
    ("full", 1, F_("IMG_2696", 9.0), "cut"),
    ("tri", 1, [F_("IMG_2686", 1.0), F_("IMG_2693", 0.5), F_("IMG_2695", 6.0)], "cut"),
    ("full", 1, F_("IMG_2698", 0.6), "punch"),
    ("tri", 1, [F_("IMG_2697", 3.0), F_("IMG_2663", 12.0), F_("IMG_2633", 15.0)], "cut"),
    ("full", 1, F_("IMG_2668", 0.6), "cut"),
    # ---- 4: cadeia produtiva / CPL Cerva / pessoas
    ("full", 1, F_("IMG_2687", 0.4), "whip"),
    ("quad", 2, [F_("IMG_2688", 0.6), F_("IMG_2673", 0.5), F_("IMG_2631", 4.0), F_("IMG_2634", 9.6)], "cut"),
    ("full", 2, F_("IMG_2617", 0.4), "punch"),
    ("tri", 1, [F_("IMG_2619", 2.0), F_("IMG_2620", 2.0), F_("IMG_2624", 3.0)], "cut"),
    ("full", 2, F_("IMG_2622", 0.4), "whip"),
    ("tri", 1, [F_("IMG_2630_2", 1.0), F_("IMG_2632_2", 0.0), F_("IMG_2640", 1.0)], "cut"),
    ("full", 2, F_("IMG_2641", 0.4), "punch"),
    ("quad", 2, [F_("IMG_2621", 0.4), F_("IMG_2623", 0.4), F_("IMG_2610", 6.3), F_("IMG_2635", 9.2)], "cut"),
    ("tri", 1, [F_("IMG_2648", 0.5), F_("IMG_2649", 0.5), F_("root_IMG_1181", 30.0)], "cut"),
    ("full", 1, F_("IMG_2650", 0.5), "whip"),
    ("quad", 2, [F_("IMG_2636", 6.0), F_("IMG_2700", 1.0), F_("IMG_2642", 0.4), F_("IMG_2646", 0.0)], "cut"),
    ("full", 1, F_("IMG_2653", 0.4), "punch"),
    ("full", 1, F_("IMG_2654", 0.6), "cut"),
    ("tri", 1, [F_("IMG_2643", 3.0), F_("IMG_2644", 2.0), F_("IMG_2658", 1.0)], "cut"),
    ("tri", 1, [F_("IMG_2613", 0), F_("IMG_2614", 0), F_("IMG_2615", 0)], "whip"),
    ("full", 1, F_("IMG_2616", 0), "cut"),
    ("tri", 1, [F_("IMG_2625_2", 0), F_("IMG_2626", 0), F_("IMG_2627", 0)], "cut"),
    # ---- TENSÃO (silêncio da trilha): a construção do rótulo
    ("vcenter", 2, F_("IMG_2592", 14.0, zoom=(1.0, 1.15)), "whip"),
    ("full", 1, F_("PC_zoom", 1.6), "cut"),
    # ---- DROP (31,7 s): momento heroico da cerveja
    ("vcenter", 3, F_("08DC7867", 12.0, zoom=(1.02, 1.12)), "flash"),
    ("vcenter", 1, F_("IMG_2664", 3.0, speed=0.7), "whip"),
    ("full", 1, F_("IMG_2656", 1.6), "cut"),
    ("vcenter", 1, F_("IMG_2398", 3.5), "whip"),
    ("tri", 1, [F_("IMG_2657", 1.0), F_("IMG_2659", 2.0), F_("IMG_2661", 1.0)], "cut"),
    ("full", 1, F_("IMG_2666", 1.6), "punch"),
    ("full", 1, F_("IMG_2662", 1.0), "cut"),
    ("full", 1, F_("IMG_2660", 1.2), "cut"),
    ("full", 1, F_("IMG_2665", 1.6), "whip"),
    ("vcenter", 2, F_("IMG_2396", 2.0, zoom=(1.0, 1.1)), "punch"),
    ("quad", 2, [F_("IMG_2593", 1.0), F_("IMG_2594", 3.0), F_("IMG_2595", 14.6), F_("root_IMG_1184", 2.0)], "cut"),
    # ---- 6: preparado para você, associado
    ("full", 2, F_("IMG_2598", 7.5), "whip"),
    ("full", 1, F_("IMG_2599", 0.4), "cut"),
    ("tri", 1, [F_("IMG_2602", 2.0), F_("IMG_2603", 2.0), F_("IMG_2604", 6.0)], "cut"),
    ("full", 1, F_("IMG_2601", 1.0), "punch"),
    ("full", 2, F_("IMG_2600", 0.3), "cut"),
    # ---- CELEBRAÇÃO
    ("full", 2, F_("IMG_2652", 38.3), "flash"),
    ("vcenter", 1, F_("IMG_2605", 1.5), "whip"),
    ("tri", 1, [F_("IMG_2638", 0), F_("IMG_2639", 0), F_("IMG_2628", 0)], "cut"),
    ("full", 1, F_("root_IMG_1185", 7.0), "punch"),
    ("full", 1, F_("IMG_2651", 0.5), "cut"),
    ("tri", 1, [F_("IMG_2629", 0), F_("IMG_2637", 0), F_("IMG_2397", 20.0)], "cut"),
    # ---- 7: Porquê, somos a indústria!
    ("full", 2, F_("IMG_2701", 2.4, zoom=(1.08, 1.0)), "whip"),
    ("full", 2, F_("IMG_2598", 28.0), "punch"),
    ("vcenter", 2, F_("IMG_2395", 4.0), "whip"),
    # ---- 8: SIMESPI 35 anos — preenche até a cartela
    ("full", 2, F_("IMG_2666", 0.3), "cut"),
    ("vcenter", 2, F_("B399EA75", 14.0), "punch"),
    ("tri", 1, [F_("IMG_2395", 7.0), F_("IMG_2396", 7.5), F_("IMG_2398", 5.5)], "cut"),
    ("full", 2, F_("IMG_2655", 1.0, speed=0.6), "whip"),
    ("full", 2, F_("IMG_2656", 3.0), "punch"),
]
CARD_BEAT = None  # calculado

def build_timeline():
    t = 0.0; k = 0; out = []
    for item in SEQ:
        nb = item[1]; t0 = tb(k); t1 = tb(k + nb)
        out.append((t0, t1) + item); k += nb
    return out, k

TEXTS = []  # preenchido em setup_texts(vo)

def main():
    tl, kend = build_timeline()
    card_t0 = tb(kend); END = 58.0
    print(f"cenas: {len(tl)} | cartela em {card_t0:.2f}s")
    # checagem: todas as imagens usadas
    used = set()
    for r in tl:
        c = r[4]
        for s in (c if isinstance(c, list) else [c]): used.add(s[0])
    allf = {os.path.basename(p).rsplit('.', 1)[0] for p in glob.glob(f"{H}/*") + glob.glob(f"{V}/*") if not p.endswith('.txt')}
    allf -= {"PC_zoom"}
    missing = sorted(allf - used); print("faltando:", missing)
    texts = json.load(open(f"{S}/n/texts.json")) if os.path.exists(f"{S}/n/texts.json") else []
    TX = [Text(**{**x, 'lines': [[(w, tuple(c)) for w, c in ln] for ln in x['lines']], 'pos': tuple(x['pos'])}) for x in texts]
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{HH}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-preset", "medium" if not PREVIEW else "veryfast", "-crf", "16" if not PREVIEW else "26",
                            "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", OUT], stdin=subprocess.PIPE)
    fidx = 0; total = int(END * FPS)
    for idx, (t0, t1, kind, nb, content, trans) in enumerate(tl):
        f0, f1 = int(round(t0 * FPS)), int(round(t1 * FPS)); n = f1 - f0
        if kind == "full": frs = L_full(content, n)
        elif kind == "vcenter": frs = L_vcenter(content, n)
        elif kind == "tri": frs = L_panels(content, n, 1)
        elif kind == "quad": frs = L_panels(content, n, 2)
        if trans == "punch": frs = punch(frs)
        elif trans == "flash": frs = flash(punch(frs, 5, 1.08))
        elif trans == "whip": frs = whip(frs, "in", 1)
        # saída em chicote se o próximo entra em chicote
        if idx + 1 < len(tl) and tl[idx + 1][5] == "whip": frs = whip(frs, "out", 1, 3)
        for i, fr in enumerate(frs):
            tt = (f0 + i) / FPS
            for tx in TX: fr = tx.draw(fr, tt)
            enc.stdin.write(np.ascontiguousarray(fr).tobytes()); fidx += 1
        print(f"  {idx:02d} {t0:5.2f}-{t1:5.2f} {kind:7s} {trans}", flush=True)
    # cartela
    while fidx < total:
        tt = fidx / FPS; fr = card_frame(tt - card_t0)
        if tt - card_t0 < 0.12: fr = flash([fr], 1, 0.4)[0]
        enc.stdin.write(fr.tobytes()); fidx += 1
    enc.stdin.close(); enc.wait(); print("ok", OUT, fidx / FPS)

if __name__ == "__main__":
    main()
