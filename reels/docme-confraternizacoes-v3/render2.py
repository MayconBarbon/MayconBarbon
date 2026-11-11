#!/usr/bin/env python3
"""DocMe — Confraternizações v2 (balada). 1080x1920 @30fps, 25 s.
Footage lives in the top 2/3 (1080x1280) with split screens / picture-in-picture;
all text lives in its own panel in the bottom third (never over the images)."""
import os, sys, subprocess, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

S = "/tmp/claude-0/-home-user-MayconBarbon/e50a6a57-cde3-5f78-9f29-1a0320ad8079/scratchpad"
SRC = S + "/src/hy_sp/"
W, H, FPS, DUR = 1080, 1920, 30, 25.0
FH = 1280                      # footage area height
ORANGE = (233, 87, 13); DARK = (30, 30, 32); WHITE = (255, 255, 255); GAP = 10
F = lambda w, s: ImageFont.truetype(f"{S}/fonts/Poppins-{w}.ttf", s)

# layouts -> list of panel boxes (x, y, w, h) inside the footage area
LAY = {
    "full": [(0, 0, W, FH)],
    "h2":   [(0, 0, W, FH // 2 - GAP // 2), (0, FH // 2 + GAP // 2, W, FH // 2 - GAP // 2)],
    "v2":   [(0, 0, W // 2 - GAP // 2, FH), (W // 2 + GAP // 2, 0, W // 2 - GAP // 2, FH)],
    "t3":   [(0, 0, W, FH // 2 - GAP // 2), (0, FH // 2 + GAP // 2, W // 2 - GAP // 2, FH // 2 - GAP // 2),
             (W // 2 + GAP // 2, FH // 2 + GAP // 2, W // 2 - GAP // 2, FH // 2 - GAP // 2)],
    "pip":  [(0, 0, W, FH), (470, 470, 540, 720)],
}
C = lambda n, t: (f"IMG_{n}.MOV", t)
SEG = [
    # 0-3 hook (rapid)
    (0.0, 0.5, "full", [C(3903, 1.0)]),
    (0.5, 1.0, "full", [C(3880, 0.5)]),
    (1.0, 1.5, "h2", [C(3889, 0.5), C(3887, 1.0)]),
    (1.5, 2.0, "full", [C(3901, 0.8)]),
    (2.0, 2.5, "v2", [C(3886, 0.6), C(3860, 0.8)]),
    (2.5, 3.0, "full", [C(3879, 1.6)]),
    # 3-9 foto e video
    (3.0, 4.0, "t3", [C(3832, 2.5), C(3784, 0.6), C(3778, 0.8)]),
    (4.0, 4.5, "full", [C(3842, 0.4)]),
    (4.5, 5.0, "pip", [C(3829, 1.5), C(3898, 0.5)]),
    (5.0, 5.5, "h2", [C(3882, 0.5), C(3753, 0.6)]),
    (5.5, 6.0, "full", [C(3890, 0.5)]),
    (6.0, 7.0, "v2", [C(3880, 2.0), C(3901, 2.2)]),
    (7.0, 7.5, "full", [C(3683, 0.8)]),
    (7.5, 8.0, "h2", [C(3854, 1.5), C(3855, 1.5)]),
    (8.0, 9.0, "pip", [C(3903, 3.0), C(3886, 2.2)]),
    # 9-18 energia
    (9.0, 9.25, "full", [C(3889, 1.6)]),
    (9.25, 9.5, "full", [C(3880, 3.0)]),
    (9.5, 9.75, "full", [C(3887, 3.2)]),
    (9.75, 10.0, "full", [C(3901, 3.0)]),
    (10.0, 11.0, "t3", [C(3862, 2.0), C(3842, 2.4), C(3890, 2.0)]),
    (11.0, 11.5, "full", [C(3766, 2.5)]),
    (11.5, 12.0, "v2", [C(3861, 0.8), C(3898, 2.2)]),
    (12.0, 13.0, "h2", [C(3900, 1.0), C(3879, 3.6)]),
    (13.0, 13.5, "full", [C(3882, 1.6)]),
    (13.5, 14.0, "pip", [C(3832, 4.0), C(3860, 1.6)]),
    (14.0, 15.0, "t3", [C(3903, 4.5), C(3887, 0.3), C(3886, 2.8)]),
    (15.0, 15.5, "full", [C(3784, 2.2)]),
    (15.5, 16.0, "full", [C(3753, 1.6)]),
    (16.0, 17.0, "v2", [C(3901, 0.3), C(3880, 1.2)]),
    (17.0, 17.5, "full", [C(3890, 2.6)]),
    (17.5, 18.0, "h2", [C(3829, 3.5), C(3889, 0.2)]),
    # 18-22 equipe
    (18.0, 19.0, "pip", [C(3900, 2.8), C(3898, 1.3)]),
    (19.0, 19.5, "full", [C(3842, 3.2)]),
    (19.5, 20.0, "v2", [C(3887, 4.2), C(3901, 1.6)]),
    (20.0, 21.0, "t3", [C(3879, 0.3), C(3886, 1.2), C(3860, 0.2)]),
    (21.0, 21.5, "full", [C(3880, 3.3)]),
    (21.5, 22.0, "full", [C(3903, 5.3)]),
]
END_BG = [C(3903, 0.2)]  # blurred under end card

# ------------------------------------------------------------- decoding
def decode(fname, t_in, dur, w, h, over=1.08):
    bw, bh = int(w * over) // 2 * 2, int(h * over) // 2 * 2
    n = round(dur * FPS)
    cmd = ["ffmpeg", "-v", "error", "-ss", str(t_in), "-i", SRC + fname, "-t", str(dur + 0.2),
           "-vf", f"scale={bw}:{bh}:force_original_aspect_ratio=increase,crop={bw}:{bh},fps={FPS},eq=contrast=1.06:saturation=1.15",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    out, last = [], None
    for _ in range(n):
        b = p.stdout.read(bw * bh * 3)
        if len(b) == bw * bh * 3: last = Image.frombytes("RGB", (bw, bh), b)
        out.append(last)
    p.stdout.close(); p.wait()
    return out

def punch(img, w, h, u):
    z = 1.0 + 0.08 * (1 - min(1, u * 2.2)) ** 2   # quick snap-in at cut
    bw, bh = img.size
    cw, ch = bw / (1.08 * z), bh / (1.08 * z)
    box = ((bw - cw) / 2, (bh - ch) / 2, (bw + cw) / 2, (bh + ch) / 2)
    return img.resize((w, h), Image.BICUBIC, box=box)

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def ease_back(x):
    x = max(0.0, min(1.0, x)); c = 1.70158; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2

# ------------------------------------------------------------- bottom panel text
FX = F("ExtraBold", 84); FBIG = F("Black", 120); FS = F("SemiBold", 34)
logo = Image.open(f"{S}/src/brand/DocMe nova versão-4.pdf.png").convert("RGBA"); logo = logo.crop(logo.getbbox())
def lw(w): return logo.resize((w, round(logo.height * w / logo.width)), Image.LANCZOS)
LOGO_P, LOGO_END = lw(230), lw(800)

def words_img(lines, font, hl, color=WHITE):
    """render lines; returns list of (word_img, x, y) relative to block, and block size"""
    sp = font.getlength(" "); asc, desc = font.getmetrics(); lh = asc + desc + 6
    items, bw = [], 0
    for li, ln in enumerate(lines):
        ws = ln.split(" "); tw = sum(font.getlength(w) for w in ws) + sp * (len(ws) - 1); bw = max(bw, tw)
    for li, ln in enumerate(lines):
        ws = ln.split(" "); tw = sum(font.getlength(w) for w in ws) + sp * (len(ws) - 1)
        x = (bw - tw) / 2
        for w in ws:
            col = ORANGE if w.strip(".,?!").lower() in hl else color
            im = Image.new("RGBA", (int(font.getlength(w)) + 8, lh + 10), (0, 0, 0, 0))
            ImageDraw.Draw(im).text((2, 2), w, font=font, fill=col)
            items.append((im, x, li * lh)); x += font.getlength(w) + sp
    return items, (int(bw) + 8, len(lines) * lh)

def kinetic(base, items, size, cx, cy, t, t0, t1, stagger=0.09):
    if t < t0 or t > t1: return
    bx, by = cx - size[0] / 2, cy - size[1] / 2
    out_a = 1 - ease((t - (t1 - 0.18)) / 0.18)
    for k, (im, x, y) in enumerate(items):
        u = (t - t0 - k * stagger) / 0.22
        if u <= 0: continue
        a = min(ease(u), out_a)
        if a <= 0: continue
        s = 0.6 + 0.4 * ease_back(u)
        w2, h2 = max(1, int(im.width * s)), max(1, int(im.height * s))
        im2 = im.resize((w2, h2), Image.BICUBIC)
        if a < 1: im2.putalpha(im2.getchannel("A").point(lambda v: int(v * a)))
        base.paste(im2, (int(bx + x + (im.width - w2) / 2), int(by + y + (im.height - h2) / 2 + (1 - ease(u)) * 30)), im2)

TXT = [  # (t0, t1, lines, highlight, font)
    (0.10, 2.98, ["A confraternização", "da firma está chegando?"], {"confraternização", "chegando"}, FX),
    (3.05, 8.98, ["Foto e vídeo para", "guardar cada momento"], {"foto", "vídeo"}, FX),
    (9.00, 10.98, ["PISTA CHEIA"], {"cheia"}, FBIG),
    (11.00, 12.98, ["ENCONTROS"], set(), FBIG),
    (13.00, 14.98, ["SHOW"], {"show"}, FBIG),
    (15.00, 15.98, ["DRINKS"], set(), FBIG),
    (16.00, 17.98, ["SORRISOS"], {"sorrisos"}, FBIG),
    (18.05, 21.98, ["Sua equipe merece", "uma lembrança especial"], {"lembrança", "especial"}, FX),
]
def fit(lines, f, maxw=900):
    sz = f.size
    while max(f.getlength(l) for l in lines) > maxw and sz > 40:
        sz -= 2; f = ImageFont.truetype(f.path, sz)
    return f
TXT_R = [(a, b, *words_img(l, fit(l, f), hl)) for a, b, l, hl, f in TXT]
ITEMS_END1, SZ_END1 = words_img(["Ainda dá tempo."], F("ExtraBold", 96), set())
ITEMS_END2, SZ_END2 = words_img(["DocMe."], F("Black", 120), {"docme"})
SUBI, SUBS = words_img(["Foto e vídeo para confraternizações"], F("SemiBold", 40), set(), (225, 225, 228))

BEATS = [i * 0.5 for i in range(50)]
def panel(base, t):
    d = ImageDraw.Draw(base)
    d.rectangle((0, FH, W, H), fill=DARK)
    # beat-pulsing orange bar on the seam between footage and panel
    ph = (t % 0.5) / 0.5; pulse = 1 - ph if t >= 3 and t < 22 else 0.35
    d.rectangle((0, FH, W, FH + 10 + int(8 * pulse)), fill=ORANGE)
    # equalizer ticks under the text (beat-synced), decorative
    if t < 22:
        n = 18; x0 = W / 2 - n * 14 / 2
        for k in range(n):
            hh = 6 + 22 * abs(math.sin(t * 7.0 + k * 0.9)) * (0.4 + 0.6 * pulse)
            d.rounded_rectangle((x0 + k * 14, 1745 - hh, x0 + k * 14 + 7, 1745), 3, fill=(90, 90, 96))
        base.paste(LOGO_P, (int(W / 2 - LOGO_P.width / 2), 1770), LOGO_P)
    for (a, b, items, size) in TXT_R:
        kinetic(base, items, size, W / 2, 1490, t, a, b, stagger=0.07 if len(items) > 2 else 0.0)

# ------------------------------------------------------------- composite
def white_frame(im, b=10):
    out = Image.new("RGB", (im.width + 2 * b, im.height + 2 * b), WHITE); out.paste(im, (b, b)); return out

def frames():
    for (s0, s1, lay, clips) in SEG:
        f0, f1 = round(s0 * FPS), round(s1 * FPS); n = f1 - f0; dur = n / FPS
        boxes = LAY[lay]
        srcs = [decode(c[0], c[1], dur, bx[2], bx[3]) for c, bx in zip(clips, boxes)]
        for i in range(n):
            t = (f0 + i) / FPS; u = i / max(1, n - 1)
            base = Image.new("RGB", (W, H), (12, 12, 14))
            for k, (bx, fr) in enumerate(zip(boxes, srcs)):
                im = punch(fr[i], bx[2], bx[3], u)
                x, y = bx[0], bx[1]
                if lay == "pip" and k == 1:
                    # inset slides in from the right, tilted, white border
                    a = ease_back(i / 6)
                    im = white_frame(im).rotate(-4, Image.BICUBIC, expand=True, fillcolor=None)
                    x = int(W + 40 - (W + 40 - (bx[0] - 10)) * a); y = bx[1] - 40
                    sh = Image.new("RGBA", im.size, (0, 0, 0, 120)).filter(ImageFilter.GaussianBlur(4))
                    mask = Image.new("L", im.size, 0); ImageDraw.Draw(mask).rectangle((0, 0, *im.size), fill=255)
                    rot_mask = white_frame(Image.new("L", (bx[2], bx[3]), 255).convert("RGB")).convert("L").rotate(-4, Image.BICUBIC, expand=True)
                    base.paste(im, (x, y), rot_mask)
                    continue
                if lay != "full" and k > 0 and i < 4:
                    # secondary panels slide in on the cut
                    off = int((1 - ease(i / 4)) * (bx[2] if lay == "v2" else bx[3]) * 0.5)
                    im = im.crop((0, 0, bx[2], bx[3]))
                    if lay == "v2": x += off
                    else: y += off
                base.paste(im, (x, y))
            # downbeat flash at section starts
            if s0 in (3.0, 9.0, 18.0) and i < 3:
                fl = Image.new("RGB", (W, FH), WHITE)
                base.paste(Image.blend(base.crop((0, 0, W, FH)), fl, [0.6, 0.3, 0.1][i]), (0, 0))
            panel(base, t)
            yield t, base
    # end card 22-25
    f0, f1 = round(22.0 * FPS), round(DUR * FPS); n = f1 - f0
    bg = decode(END_BG[0][0], END_BG[0][1], n / FPS, W, H, 1.0)
    for i in range(n):
        t = (f0 + i) / FPS; u = t - 22.0
        im = bg[i].resize((W, H)).filter(ImageFilter.GaussianBlur(22))
        base = Image.blend(im, Image.new("RGB", (W, H), DARK), 0.6 + 0.3 * ease(u / 0.5))
        kinetic(base, ITEMS_END1, SZ_END1, W / 2, 700, t, 22.20, 25.5)
        # logo signs the piece when the voice says "DocMe" (~23.35 s)
        ul = t - 23.30
        if ul > 0:
            a = ease_back(ul / 0.45); s = 0.55 + 0.45 * a
            lg = LOGO_END.resize((max(1, int(LOGO_END.width * s)), max(1, int(LOGO_END.height * s))), Image.LANCZOS)
            al = min(1, ul / 0.2); lg.putalpha(lg.getchannel("A").point(lambda v: int(v * al)))
            base.paste(lg, (int(W / 2 - lg.width / 2), int(1000 - lg.height / 2)), lg)
        g = ease((u - 1.75) / 0.4)
        if g > 0:
            L = int(440 * g); ImageDraw.Draw(base).rounded_rectangle((W / 2 - L / 2, 1280, W / 2 + L / 2, 1294), 7, fill=ORANGE)
        kinetic(base, SUBI, SUBS, W / 2, 1380, t, 23.9, 25.5)
        yield t, base

if __name__ == "__main__":
    prev = os.environ.get("PREVIEW")
    if prev:
        want = sorted(float(x) for x in prev.split(",")); got = {}
        os.makedirs(f"{S}/prev2", exist_ok=True)
        for t, im in frames():
            for w in want:
                if w not in got and abs(t - w) < 0.5 / FPS + 1e-6:
                    got[w] = 1; im.resize((540, 960)).save(f"{S}/prev2/p_{w:05.2f}.jpg", quality=85)
            if len(got) == len(want): break
        sys.exit()
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                          "-pix_fmt", "yuv420p", sys.argv[1]], stdin=subprocess.PIPE)
    n = 0
    for t, im in frames(): p.stdin.write(im.tobytes()); n += 1
    p.stdin.close(); p.wait(); print("frames", n)
