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
        clips.append(frames(name, t0, n, w, h, o.get("speed", 1.0), o.get("zoom", (1.0, 1.06)), o.get("focus", (0.5, 0.5))))
    for i in range(n):
        c = np.zeros((HH, W, 3), np.uint8); c[:] = NAVY
        for j, ((x, y, w, h), cl) in enumerate(zip(cells, clips)):
            # entrada escalonada: painel desliza de baixo nos 5 primeiros quadros
            d = i; off = 0 if d >= 3 else int((1 - ease(d / 3)) * (h * 0.12))
            f = cl[i]
            if off: c[y + off:y + h, x:x + w] = f[:h - off]
            else: c[y:y + h, x:x + w] = f
        canvas.append(c)
    return canvas


# ---------------- HERO do produto (mockup oficial animado)
_BOT = Image.open(f"{S}/mock/bottle.png").convert("RGBA")
_rng = np.random.default_rng(5)
_PART = _rng.random((70, 4))  # x, fase, velocidade, tamanho
def L_hero(spec, n):
    o = spec[2] if len(spec) > 2 else {}
    cx = o.get("cx", 0.5); variant = o.get("v", 1)
    yy, xx = np.mgrid[0:HH, 0:W].astype(np.float32)
    out = []
    bh = int(HH * 0.88); bw = int(_BOT.width * bh / _BOT.height)
    base = _BOT.resize((bw, bh), Image.LANCZOS)
    A = np.array(base)[:, :, 3].astype(np.float32) / 255
    for i in range(n):
        t = i / FPS; p = min(1, t / 0.55); e = 1 - (1 - p) ** 3
        # fundo: gradiente radial marinho + feixe de luz girando
        r = np.sqrt(((xx - W * cx) / W) ** 2 + ((yy - HH * 0.45) / HH) ** 2)
        g = np.clip(1 - r * 1.6, 0, 1) ** 1.5
        ang = np.arctan2(yy - HH * 1.1, xx - W * cx)
        rays = (0.5 + 0.5 * np.cos(ang * 14 + t * 1.2)) ** 6 * np.clip(1 - r * 1.2, 0, 1) * 0.35
        bg = np.zeros((HH, W, 3), np.float32)
        for c in range(3):
            if variant == 2: bg[:, :, c] = 226 + 29 * g + (CYAN[c] - 255) * rays * 0.15
            else: bg[:, :, c] = NAVY[c] * 0.55 + (BLUE[c] * 1.1 - NAVY[c] * 0.55) * g + CYAN[c] * rays
        # partículas (bolhas) subindo
        for px, ph, sp, sz in _PART:
            x = int((px * 0.9 + 0.05) * W); y = int(HH * (1.05 - ((ph + t * (0.15 + sp * 0.35)) % 1.1)))
            rr = int(2 + sz * 6); cv2.circle(bg, (x, y), rr, (150, 205, 225) if variant == 2 else (200, 235, 245), -1, cv2.LINE_AA)
        bg = cv2.GaussianBlur(bg, (0, 0), 0.8)
        # garrafa: entrada de baixo com escala e leve rotação; flutuação suave
        sc = 1.18 - 0.18 * e; rot = (-6 + 6 * e) + 0.8 * math.sin(t * 2.2)
        dy = (1 - e) * HH * 0.45 + 6 * math.sin(t * 2.6)
        b = base.resize((max(1, int(bw * sc)), max(1, int(bh * sc))), Image.LANCZOS).rotate(rot, Image.BICUBIC, expand=True)
        ba = np.array(b).astype(np.float32); al = ba[:, :, 3:] / 255 * min(1, t / 0.25)
        # brilho diagonal correndo pelo vidro
        hh_, ww_ = ba.shape[:2]; gy, gx = np.mgrid[0:hh_, 0:ww_].astype(np.float32)
        pos = ((t - 0.35) / 0.9) * (ww_ + hh_) - hh_ * 0.3
        band = np.exp(-((gx + gy * 0.45 - pos) / (ww_ * 0.09)) ** 2)[:, :, None] * 0.55
        col = np.clip(ba[:, :, :3] + 255 * band, 0, 255)
        x0 = int(W * cx - ww_ / 2); y0 = int(HH * 0.5 - hh_ / 2 + dy)
        # sombra suave
        sh = np.zeros((HH, W), np.float32)
        cv2.ellipse(sh, (int(W * cx), int(HH * 0.5 + bh * sc / 2 + dy - 4)), (int(bw * 0.55), 18), 0, 0, 360, 1, -1)
        sh = cv2.GaussianBlur(sh, (0, 0), 14) * (0.30 if variant == 2 else 0.55) * e
        bg *= (1 - sh[:, :, None])
        X0, Y0 = max(0, x0), max(0, y0); X1, Y1 = min(W, x0 + ww_), min(HH, y0 + hh_)
        if X1 > X0 and Y1 > Y0:
            sub = (slice(Y0 - y0, Y1 - y0), slice(X0 - x0, X1 - x0))
            reg = bg[Y0:Y1, X0:X1]; a_ = al[sub]
            bg[Y0:Y1, X0:X1] = reg * (1 - a_) + col[sub] * a_
        # halo ciano atrás no impacto
        out.append(np.clip(bg, 0, 255).astype(np.uint8))
    return out

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
        # faixa translúcida (marinho) para leitura sobre mosaicos
        band = Image.new("RGBA", pil.size, (0, 0, 0, 0)); bd = ImageDraw.Draw(band)
        ba = min(1, max(0, (t - self.t0) / 0.15)) * fade_out
        bx0 = min(x0s) - 50; bx1 = max(x0 + wd for x0, wd in zip(x0s, widths)) + 40
        by0 = y0 - 40; by1 = y0 + tot_h + (int(self.size * 0.42) + 30 if self.sub else 20)
        bd.rounded_rectangle((bx0, by0, bx1, by1), radius=18, fill=NAVY + (int(150 * ba),))
        band = band.filter(ImageFilter.GaussianBlur(14))
        pil = Image.alpha_composite(pil, band)
        sh = sh.filter(ImageFilter.GaussianBlur(7))
        pil = Image.alpha_composite(pil, sh); pil = Image.alpha_composite(pil, lay)
        return np.array(pil.convert("RGB"))


PW = 760
def wrap_lines(words, fnt, maxw, d):
    lines=[[]]; cur=0
    for w,col in words:
        ww=d.textlength(w+" ",font=fnt)
        if lines[-1] and cur+ww>maxw: lines.append([]); cur=0
        lines[-1].append((w,col)); cur+=ww
    return lines
def panel_text(img, tx, t, p):
    """desenha o texto dentro do painel marinho [0, PW*p]."""
    pil=Image.fromarray(img).convert("RGBA"); lay=Image.new("RGBA",pil.size,(0,0,0,0)); d=ImageDraw.Draw(lay)
    words=[w for ln in tx.lines for w in ln]; size=int(tx.size*0.82)
    while True:
        fnt=font(tx.weight,size); lines=wrap_lines(words,fnt,PW-150,d)
        if len(lines)<=4 or size<44: break
        size-=4
    lh=int(size*1.12); tot=lh*len(lines)+(int(size*1.1)+20 if tx.sub else 0)
    x0=int(80-(1-p)*PW); y0=int(HH/2-tot/2)
    fade=min(1,max(0,(tx.t1-t)/0.18)); k=0
    bw=int(110*ease(min(1,(t-tx.t0)/0.3)))
    d.rectangle((x0,y0-36,x0+bw,y0-26),fill=CYAN+(int(255*fade),))
    for li,ln in enumerate(lines):
        x=x0; y=y0+li*lh
        for w,col in ln:
            dt=t-tx.t0-0.12-k*0.05; k+=1; a=min(1,max(0,dt/0.15))*fade
            if a>0:
                dy=int((1-ease(min(1,dt/0.2)))*34)
                d.text((x,y+dy),w,font=fnt,fill=col+(int(255*a),))
            x+=d.textlength(w+" ",font=fnt)
    if tx.sub:
        sf_=font("SemiBold",int(size*0.42)); a=min(1,max(0,(t-tx.t0-0.35)/0.2))*fade
        sl=wrap_lines([(w,WHITE) for w in tx.sub.split()],sf_,PW-150,d)
        for j,ln in enumerate(sl):
            d.text((x0+2,y0+lh*len(lines)+14+j*int(size*0.52))," ".join(w for w,_ in ln),font=sf_,fill=WHITE+(int(230*a),))
    return np.array(Image.alpha_composite(pil,lay).convert("RGB"))
def panel_windows(TX, gap=1.3):
    w=[]
    for tx in sorted(TX,key=lambda z:z.t0):
        a,b=tx.t0-0.22,tx.t1+0.22
        if w and a-w[-1][1]<gap: w[-1][1]=max(w[-1][1],b)
        else: w.append([a,b])
    return w
def compose_panel(fr, TX, t, alt=None):
    win=[w for w in panel_windows(TX) if w[0]<=t<w[1]]
    if not win: return fr
    a,b=win[0]
    act=[tx for tx in TX if tx.t0<=t<tx.t1]
    tx=act[0] if act else None
    p=ease(min(1,max(0,(t-a)/0.22)))*ease(min(1,max(0,(b-t)/0.22)))
    x0=int(PW*p)
    out=np.zeros_like(fr); out[:]=NAVY
    if W-x0>0: out[:,x0:]=cover(alt,W-x0,HH,(0.5,0.5)) if alt is not None else cover(fr,W-x0,HH,(0.6,0.5))
    out[:,max(0,x0-6):x0]=CYAN
    if tx is not None: out=panel_text(out,tx,t,p)
    return out

def wd(s, col=WHITE): return [(w, col) for w in s.split()]

# ---------------- cartela final animada
def logo(path, h):
    im = Image.open(path).convert("RGBA"); im = im.crop(im.getbbox())
    return im.resize((round(im.width * h / im.height), h), Image.LANCZOS)
LOGOS = [logo(f"{B}/simespi_small_crop.png", 168), logo(f"{B}/logo35_crop.png", 270), logo(f"{B}/Logo_Dama_Horizontal_t_crop.png", 172)]
def card_frame(t):  # t desde o início da cartela
    c = Image.new("RGBA", (W, HH), (255, 255, 255, 255)); d = ImageDraw.Draw(c)
    gap = 120; tot = sum(l.width for l in LOGOS) + 2 * gap; x = (W - tot) // 2; cy = HH // 2
    for i, lg in enumerate(LOGOS):
        dt = t - 0.10 - i * IBI / 2  # entra no contratempo
        a = min(1, max(0, dt / 0.18))
        if a > 0:
            s = 0.86 + 0.14 * (1 - (1 - min(1, dt / 0.3)) ** 3) + 0.04 * math.sin(min(1, dt / 0.3) * math.pi)
            im = lg.resize((max(1, int(lg.width * s)), max(1, int(lg.height * s))), Image.LANCZOS)
            im.putalpha(im.getchannel("A").point(lambda v: int(v * a)))
            c.alpha_composite(im, (int(x + (lg.width - im.width) / 2), int(cy - im.height / 2)))
        x += lg.width + gap
    fo = min(1, max(0, (t - 5.2) / 0.5))
    out = np.array(c.convert("RGB")).astype(np.float32)
    return (out * (1 - fo) + 255 * fo).astype(np.uint8)

# =====================================================================
# ROTEIRO DE IMAGENS (em batidas da trilha; 1 batida = 0,488 s)
# tipo, batidas, conteúdo, transição de entrada
def F_(n, t, **o): return (n, t, o)
SEQ = [
    # ---- GANCHO (0–2,5 s): a novidade
    ("tri", 1, [F_("IMG_2396", 0.5), F_("IMG_2398", 1.0), F_("08DC7867", 17.2)], "flash"),
    ("tri", 1, [F_("IMG_2664", 2.0), F_("IMG_2667", 1.5), F_("IMG_2664", 6.5)], "whip"),
    ("tri", 1, [F_("IMG_2397", 31.0), F_("IMG_2395", 0.3), F_("08DC7867", 0.2)], "punch"),
    ("tri", 2, [F_("IMG_2395", 5.0), F_("08DC7867", 2.0, zoom=(1.0, 1.08)), F_("IMG_2397", 14.0)], "whip"),
    # ---- 1: uma cerveja criada para o SIMESPI
    ("tri", 2, [F_("IMG_2397", 8.5), F_("B399EA75", 5.0), F_("IMG_2604", 12.0)], "punch"),
    ("tri", 2, [F_("IMG_2604", 7.0), F_("IMG_2397", 6.0), F_("IMG_2395", 6.5)], "whip"),
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
    ("tri", 1, [F_("IMG_2697", 3.0), F_("IMG_2663", 9.6), F_("IMG_2633", 22.0)], "cut"),
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
    ("quad", 2, [F_("IMG_2636", 4.6), F_("IMG_2700", 1.0), F_("IMG_2642", 0.4), F_("IMG_2646", 0.0)], "cut"),
    ("full", 1, F_("IMG_2653", 0.4), "punch"),
    ("full", 1, F_("IMG_2654", 0.6), "cut"),
    ("tri", 2, [F_("IMG_2643", 3.0), F_("IMG_2644", 2.0), F_("IMG_2658", 1.0)], "cut"),
    ("tri", 2, [F_("IMG_2625_2", 0), F_("IMG_2626", 0), F_("IMG_2627", 0)], "cut"),
    # ---- TENSÃO (silêncio da trilha): a construção do rótulo
    ("tri", 2, [F_("IMG_2592", 2.0), F_("IMG_2592", 14.0, zoom=(1.0, 1.15)), F_("IMG_2592", 19.0)], "whip"),
    ("full", 1, F_("PC_zoom", 1.6), "cut"),
    # ---- DROP (31,7 s): momento heroico da cerveja
    ("tri", 4, [F_("IMG_2396", 4.0), F_("08DC7867", 12.0, zoom=(1.02, 1.12)), F_("IMG_2398", 3.5)], "flash"),
    ("tri", 1, [F_("IMG_2667", 0.5), F_("IMG_2664", 3.0, speed=0.7), F_("IMG_2664", 8.5)], "whip"),
    ("full", 1, F_("IMG_2656", 1.6), "cut"),
    ("tri", 1, [F_("08DC7867", 20.0), F_("IMG_2398", 3.5), F_("IMG_2396", 6.5)], "whip"),
    ("tri", 1, [F_("IMG_2657", 1.0), F_("IMG_2659", 2.0), F_("IMG_2661", 1.0)], "cut"),
    ("full", 1, F_("IMG_2666", 1.6), "punch"),
    ("full", 1, F_("IMG_2662", 1.0), "cut"),
    ("full", 1, F_("IMG_2660", 1.2), "cut"),
    ("full", 1, F_("IMG_2665", 1.6), "whip"),
    ("tri", 2, [F_("IMG_2398", 0.3), F_("IMG_2396", 2.0, zoom=(1.0, 1.1)), F_("08DC7867", 18.2)], "punch"),
    ("quad", 2, [F_("IMG_2593", 1.0), F_("IMG_2594", 3.0), F_("IMG_2595", 14.6), F_("root_IMG_1184", 2.0)], "cut"),
    # ---- 6: preparado para você, associado
    ("full", 2, F_("IMG_2598", 7.5), "whip"),
    ("full", 1, F_("IMG_2599", 0.4), "cut"),
    ("tri", 1, [F_("IMG_2602", 2.0), F_("IMG_2603", 2.0), F_("IMG_2604", 6.0)], "cut"),
    ("full", 1, F_("IMG_2601", 1.0), "punch"),
    ("full", 2, F_("IMG_2600", 0.3), "cut"),
    # ---- CELEBRAÇÃO
    ("full", 2, F_("IMG_2652", 38.3), "flash"),
    ("tri", 1, [F_("IMG_2397", 33.0), F_("IMG_2605", 1.5), F_("IMG_2395", 1.2)], "whip"),
    ("tri", 1, [F_("IMG_2638", 0), F_("IMG_2639", 0), F_("IMG_2628", 0)], "cut"),
    ("full", 1, F_("root_IMG_1185", 7.0), "punch"),
    ("full", 1, F_("IMG_2651", 0.5), "cut"),
    ("tri", 1, [F_("IMG_2629", 0), F_("IMG_2637", 0), F_("IMG_2397", 20.0)], "cut"),
    # ---- 7: Porquê, somos a indústria!
    ("hero", 3, ("MOCKUP", 0, {"cx": 0.5, "v": 2}), "whip"),
    ("full", 1, F_("IMG_2598", 28.0), "punch"),
    ("tri", 2, [F_("IMG_2397", 20.0), F_("IMG_2395", 4.0), F_("IMG_2604", 15.0)], "whip"),
    # ---- 8: SIMESPI 35 anos — preenche até a cartela
    ("full", 2, F_("IMG_2666", 0.3), "cut"),
    ("tri", 2, [F_("IMG_2397", 24.0), F_("B399EA75", 14.0), F_("IMG_2395", 7.2)], "punch"),
    ("tri", 1, [F_("IMG_2395", 7.0), F_("IMG_2396", 7.5), F_("IMG_2398", 5.5)], "cut"),
    ("full", 2, F_("IMG_2655", 1.0, speed=0.6), "whip"),
    ("full", 2, F_("IMG_2656", 3.0), "punch"),
]
CARD_BEAT = None  # calculado

def render(kind, content, n, trans, nxt_whip, width):
    global W
    oldW = W; W = width
    try:
        if kind == "full": frs = L_full(content, n)
        elif kind == "vcenter": frs = L_vcenter(content, n)
        elif kind == "tri":
            c = content if width >= 1700 else content[1:]   # área estreita: só os dois últimos, inteiros
            frs = L_panels(c, n, 1)
        elif kind == "quad": frs = L_panels(content, n, 2)
        elif kind == "hero": frs = L_hero(content, n)
        if trans == "punch": frs = punch(frs)
        elif trans == "flash": frs = flash(punch(frs, 5, 1.08))
        elif trans == "whip": frs = whip(frs, "in", 1)
        if nxt_whip: frs = whip(frs, "out", 1, 3)
    finally:
        W = oldW
    return frs

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
    allf -= {"PC_zoom"}; used.discard("MOCKUP")
    missing = sorted(allf - used); print("faltando:", missing)
    texts = json.load(open(f"{S}/n/texts.json")) if os.path.exists(f"{S}/n/texts.json") else []
    TX = [Text(**{**x, 'lines': [[(w, tuple(c)) for w, c in ln] for ln in x['lines']], 'pos': tuple(x['pos'])}) for x in texts]
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{HH}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-preset", "medium" if not PREVIEW else "veryfast", "-crf", "16" if not PREVIEW else "26",
                            "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", OUT], stdin=subprocess.PIPE)
    fidx = 0; total = int(END * FPS)
    for idx, (t0, t1, kind, nb, content, trans) in enumerate(tl):
        f0, f1 = int(round(t0 * FPS)), int(round(t1 * FPS)); n = f1 - f0
        nxt = idx + 1 < len(tl) and tl[idx + 1][5] == "whip"
        frs = render(kind, content, n, trans, nxt, W)
        overl = any(a < t1 and b > t0 for a, b in panel_windows(TX))
        alt = render(kind, content, n, trans, nxt, W - PW) if overl else None
        for i, fr in enumerate(frs):
            tt = (f0 + i) / FPS
            fr = compose_panel(fr, TX, tt, alt[i] if alt is not None else None)
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
