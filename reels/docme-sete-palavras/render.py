#!/usr/bin/env python3
"""DocMe Reel — 'Um pedido de sete palavras virou esse vídeo.'  1080x1920 @30fps, 22.0 s."""
import sys, os, glob, math, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

S = "/tmp/claude-0/-home-user-MayconBarbon/14558cd3-e9d2-53c0-bc97-8331b175cad2/scratchpad"
W, H, FPS = 1080, 1920, 30
DUR = 22.0
ORANGE = (233, 87, 13)
DARK = (38, 38, 40)
DARK2 = (28, 28, 30)
LIGHT = (179, 179, 182)
WHITE = (255, 255, 255)

REQUEST = sys.argv[1] if len(sys.argv) > 1 else "Preciso divulgar meu negócio."
OUT = sys.argv[2] if len(sys.argv) > 2 else S + "/out/reel.mp4"
PREVIEW = os.environ.get("PREVIEW")  # comma list of times -> png stills only

F = lambda w, s: ImageFont.truetype(f"{S}/fonts/Poppins-{w}.ttf", s)
FB, FX, FS, FM = F("Bold", 80), F("ExtraBold", 84), F("SemiBold", 40), F("Medium", 32)

def ease(x):  # easeOutCubic, clamped
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3

# ---------- assets ----------
def seq(name):
    return [p for p in sorted(glob.glob(f"{S}/work/seg/{name}/*.jpg"))]
SEQ = {n: seq(n) for n in ["hook1", "hook2", "prep", "cap1", "cap2", "cap3", "cap4", "cap5"] + [f"v{i}" for i in range(1, 7)]}
_cache = {}
def frame(name, i):
    fs = SEQ[name]; p = fs[min(i, len(fs) - 1)]
    if p not in _cache:
        if len(_cache) > 60: _cache.clear()
        _cache[p] = Image.open(p).convert("RGB")
    return _cache[p]

logo = Image.open(f"{S}/src/logo_v4.png").convert("RGBA"); logo = logo.crop(logo.getbbox())
def logo_w(w):
    return logo.resize((w, round(logo.height * w / logo.width)), Image.LANCZOS)
LOGO_S, LOGO_L = logo_w(300), logo_w(560)

# planning pages: blurred so client-specific body text is not legible (headings remain readable)
# only generic, non-client regions stay sharp (orig 130-dpi page coords); everything else heavily blurred
def page(i, width, sharp):
    im = Image.open(f"{S}/work/pg-0{i}.png").convert("RGB"); k = width / im.width
    im = im.resize((width, round(im.height * k)), Image.LANCZOS)
    out = im.filter(ImageFilter.GaussianBlur(9))
    for (x0, y0, x1, y1) in sharp:
        b = tuple(round(v * k) for v in (x0, y0, x1, y1)); out.paste(im.crop(b), b[:2])
    return out.point(lambda v: int(v * 0.86))
PG1 = page(1, 1400, [(0, 125, 1075, 512)])
PG2 = page(2, 1900, [(60, 112, 1075, 168), (60, 405, 1000, 650)])


# ---------- drawing helpers ----------
def grad(img, top=True, h=900, a=190):
    g = Image.new("L", (1, h))
    for y in range(h):
        g.putpixel((0, y), int(a * (1 - y / h) ** 1.6) if top else int(a * (y / h) ** 1.6))
    g = g.resize((W, h)); blk = Image.new("RGB", (W, h), (0, 0, 0))
    img.paste(blk, (0, 0 if top else H - h), g)

def label(img, lines, x, y, t, size=84, gap=14, stagger=0.08, dur=0.28):
    """lines: list of (text, style) style 'box' = white on orange box, 'plain' = white text w/ shadow."""
    d = ImageDraw.Draw(img); font = F("ExtraBold", size)
    for k, (txt, style) in enumerate(lines):
        p = ease((t - k * stagger) / dur)
        if p <= 0: break
        bb = d.textbbox((0, 0), txt, font=font); tw, th = bb[2] - bb[0], bb[3] - bb[1]
        padx, pady = 26, 16
        yy = y + k * (th + 2 * pady + gap) + (1 - p) * 40
        alpha = int(255 * p)
        lay = Image.new("RGBA", (tw + 2 * padx + 20, th + 2 * pady + 20), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        if style == "box":
            ld.rectangle([0, 0, tw + 2 * padx, th + 2 * pady], fill=ORANGE + (alpha,))
            ld.text((padx - bb[0], pady - bb[1]), txt, font=font, fill=(255, 255, 255, alpha))
        else:
            ld.text((padx - bb[0] + 3, pady - bb[1] + 4), txt, font=font, fill=(0, 0, 0, int(alpha * .45)))
            ld.text((padx - bb[0], pady - bb[1]), txt, font=font, fill=(255, 255, 255, alpha))
        img.paste(lay, (int(x - padx), int(yy)), lay)

def kenburns(src, t, z0, z1, cx0, cy0, cx1, cy1):
    """crop a W x H window from src, zoom & pan; c = window centre in src px."""
    p = t; z = z0 + (z1 - z0) * p
    cw, ch = W / z, H / z
    cx = cx0 + (cx1 - cx0) * p; cy = cy0 + (cy1 - cy0) * p
    box = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
    return src.transform((W, H), Image.EXTENT, box, Image.BICUBIC)

def vid(name, lt, zoom=(1.0, 1.06)):
    i = int(lt * FPS); im = frame(name, i)
    n = len(SEQ[name]); p = min(1, i / max(1, n - 1)); z = zoom[0] + (zoom[1] - zoom[0]) * p
    if z == 1: return im.copy()
    return kenburns(im, 0, z, z, W / 2, H / 2, W / 2, H / 2)

# ---------- scenes ----------
def s_hook(t):  # 0–2
    img = vid("hook1", t) if t < 1.2 else vid("hook2", t - 1.2)
    grad(img, True, 1000, 200)
    label(img, [("Um pedido de", "plain"), ("sete palavras", "box"), ("virou esse vídeo.", "plain")], 90, 250, t + 0.25)
    return img

def s_request(t):  # 2–4
    img = Image.new("RGB", (W, H), DARK); d = ImageDraw.Draw(img)
    words = REQUEST.split(); font = F("Bold", 96)
    # wrap into lines that fit 860 px
    lines, cur = [], ""
    for w_ in words:
        test = (cur + " " + w_).strip()
        if d.textlength("“" + test, font=font) > 860 and cur: lines.append(cur); cur = w_
        else: cur = test
    lines.append(cur)
    full = "\n".join(lines)
    n = max(1, int(len(full) * ease(t / 0.9)))
    shown = full[:n]
    # orange quote mark
    d.text((86, 560), "“", font=F("ExtraBold", 260), fill=ORANGE)
    d.multiline_text((96, 820), shown, font=font, fill=WHITE, spacing=18)
    if t < 1.2 and int(t * 4) % 2 == 0:  # caret while typing
        bb = d.multiline_textbbox((96, 820), shown, font=font, spacing=18)
        d.rectangle([bb[2] + 8, bb[3] - 90, bb[2] + 16, bb[3]], fill=ORANGE)
    # honesty tag: illustrative example, not a client quote
    a = ease((t - 0.9) / 0.4)
    if a > 0:
        d.text((100, 1330), "exemplo ilustrativo", font=FM, fill=tuple(int(c * a + DARK[i] * (1 - a)) for i, c in enumerate(LIGHT)))
    d.rectangle([0, H - 14, int(W * min(1, t / 2.0)), H], fill=ORANGE)  # thin progress accent
    return img

def s_strategy(t):  # 4–8
    if t < 1.35:
        p = t / 1.35; img = kenburns(PG1, p, 1.0, 1.05, 560, 990, 580, 985)
    elif t < 2.65:
        p = (t - 1.35) / 1.3; img = kenburns(PG2, p, 1.0, 1.05, 920, 1250, 1120, 1230)
    else:
        img = vid("prep", t - 2.65)
    grad(img, False, 1100, 245)
    label(img, [("Primeiro,", "plain"), ("a estratégia.", "box")], 90, 1110, t)
    return img

CAP = [("cap1", 1.3), ("cap2", 1.1), ("cap3", 0.8), ("cap4", 1.0), ("cap5", 0.8)]
def s_capture(t):  # 8–13
    acc = 0
    for name, d_ in CAP:
        if t < acc + d_ or name == "cap5": img = vid(name, t - acc); break
        acc += d_
    grad(img, False, 900, 200)
    label(img, [("Depois,", "plain"), ("a captação.", "box")], 90, 1110, t)
    return img

THUMBS = None
def s_edit(t):  # 13–17  graphic timeline built from the real footage above
    global THUMBS
    if THUMBS is None:
        THUMBS = []
        for name in ["hook1", "prep", "cap1", "cap2", "cap3", "cap4", "cap5", "hook2"]:
            f_ = frame(name, len(SEQ[name]) // 2)
            THUMBS.append((name, f_.resize((86, 153), Image.LANCZOS), f_.resize((330, 587), Image.LANCZOS)))
    img = Image.new("RGB", (W, H), DARK2); d = ImageDraw.Draw(img)
    label(img, [("Edição para dar", "plain"), ("forma à ideia.", "box")], 90, 250, t, size=78)
    # timeline panel
    tx0, tx1, ty = 90, 990, 1090
    d.rounded_rectangle([60, ty - 40, 1020, ty + 330], 18, fill=(48, 48, 51))
    for k in range(0, 10):  # ruler ticks
        x = tx0 + k * (tx1 - tx0) / 9; d.line([x, ty - 22, x, ty - 10], fill=(110, 110, 115), width=2)
    n = len(THUMBS); cw = (tx1 - tx0) / n
    for k, (name, th, big) in enumerate(THUMBS):
        p = ease((t - 0.15 - k * 0.12) / 0.3)
        if p <= 0: continue
        x = int(tx0 + k * cw); y = int(ty + (1 - p) * -120)
        # V1 clip with thumbnail strip
        clip = Image.new("RGB", (int(cw) - 6, 110), (70, 70, 74))
        th_c = ImageOps.fit(th, (int(cw) - 6, 110)); clip.paste(th_c, (0, 0))
        img.paste(clip, (x, y + 70)); d.rectangle([x, y + 70, x + int(cw) - 7, y + 179], outline=LIGHT, width=2)
        # A1 waveform
        for j in range(0, int(cw) - 10, 7):
            amp = 10 + 26 * abs(math.sin(k * 1.7 + j * 0.21)) * abs(math.cos(j * 0.05 + k))
            d.rectangle([x + j + 2, y + 255 - amp, x + j + 5, y + 255 + amp], fill=(120, 120, 126))
    # V2 text/graphics blocks (orange) — the on-screen titles of this reel
    for k, (a0, a1) in enumerate([(0, 1), (1, 2), (2, 4), (4, 6), (6, 7)]):
        p = ease((t - 0.9 - k * 0.12) / 0.3)
        if (a1 - a0) * cw * p > 20:
            d.rounded_rectangle([tx0 + a0 * cw, ty + 20, tx0 + a0 * cw + (a1 - a0) * cw * p - 6, ty + 56], 6, fill=ORANGE)
    # playhead
    ph = tx0 + (tx1 - tx0) * ease((t - 0.5) / 3.3)
    d.polygon([(ph - 12, ty - 40), (ph + 12, ty - 40), (ph, ty - 22)], fill=ORANGE)
    d.line([ph, ty - 30, ph, ty + 320], fill=ORANGE, width=4)
    # program monitor shows the clip under the playhead
    k = min(n - 1, max(0, int((ph - tx0) / cw)))
    mon = THUMBS[k][2]; mx, my = (W - mon.width) // 2, 480
    d.rectangle([mx - 6, my - 6, mx + mon.width + 5, my + mon.height + 5], fill=(60, 60, 64))
    img.paste(mon, (mx, my))
    return img

def s_result(t):  # 17–22
    img = Image.new("RGB", (W, H), DARK); d = ImageDraw.Draw(img)
    if t < 2.7:  # finished vertical videos from the Drive, full-bleed, 0.45 s each
        k = min(5, int(t / 0.45)); lt = t - k * 0.45
        img = vid(f"v{k + 1}", lt, zoom=(1.04, 1.0))
        grad(img, True, 520, 170)
        d = ImageDraw.Draw(img)
        label(img, [("Conteúdo pronto.", "box")], 90, 250, t + 1, size=70)
        for j in range(6):  # progress dots
            d.ellipse([92 + j * 30, 385, 108 + j * 30, 401], fill=ORANGE if j <= k else (200, 200, 205))
        return img
    q = t - 2.7
    if q < 1.4:
        font = F("ExtraBold", 82); y = 430
        rows = [[("Qual parte mais", WHITE)], [("trava você:", WHITE)],
                [("ideia", ORANGE), (", ", WHITE), ("gravação", ORANGE)], [("ou ", WHITE), ("edição", ORANGE), ("?", WHITE)]]
        for r, row in enumerate(rows):
            p = ease((q - r * 0.12) / 0.3)
            if p <= 0: break
            x = 90; yy = y + r * 120 + (1 - p) * 30
            for txt, col in row:
                colp = tuple(int(c * p + DARK[i] * (1 - p)) for i, c in enumerate(col))
                d.text((x, yy), txt, font=font, fill=colp); x += d.textlength(txt, font=font)
        img.paste(LOGO_S, (90, 1290), LOGO_S)
        return img
    e = q - 1.4
    label(img, [("Comenta aqui.", "box")], 90, 700, e + 0.1, size=104)
    a = ease(e / 0.3)
    ay = int(960 + 20 * math.sin(e * 9))
    d.polygon([(150, ay + 110), (110, ay + 50), (190, ay + 50)], fill=tuple(int(255 * a + DARK[i] * (1 - a)) for i in range(3)))
    d.rectangle([140, ay, 160, ay + 55], fill=tuple(int(255 * a + DARK[i] * (1 - a)) for i in range(3)))
    img.paste(LOGO_L, ((W - LOGO_L.width) // 2, 1210), LOGO_L)
    return img

SCENES = [(0, 2, s_hook), (2, 4, s_request), (4, 8, s_strategy), (8, 13, s_capture), (13, 17, s_edit), (17, 22, s_result)]
def render(t):
    for a, b, fn in SCENES:
        if a <= t < b or (fn is s_result and t >= a): return fn(t - a)

if PREVIEW:
    os.makedirs(S + "/out/prev", exist_ok=True)
    for ts in PREVIEW.split(","):
        render(float(ts)).save(f"{S}/out/prev/t{float(ts):05.2f}.jpg", quality=85)
    sys.exit()

os.makedirs(os.path.dirname(OUT), exist_ok=True)
N = int(DUR * FPS)
cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
       "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
       "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-profile:v", "high", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-b:a", "128k", "-t", str(DUR), "-movflags", "+faststart", OUT]
pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
for i in range(N):
    pr.stdin.write(render(i / FPS).tobytes())
pr.stdin.close(); pr.wait(); print("done", OUT, pr.returncode)
