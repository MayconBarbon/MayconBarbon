#!/usr/bin/env python3
"""DocMe — Confraternizações 2026. Reel 1080x1920 @30fps, 25.0 s.
usage: render.py out_video_noaudio.mp4   (PREVIEW="1.2,5,..." -> stills only)"""
import os, sys, subprocess, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance

S = "/tmp/claude-0/-home-user-MayconBarbon/e50a6a57-cde3-5f78-9f29-1a0320ad8079/scratchpad"
SRC = S + "/src"
W, H, FPS, DUR = 1080, 1920, 30, 25.0
NF = int(DUR * FPS)
ORANGE = (233, 87, 13); DARK = (38, 38, 40); WHITE = (255, 255, 255)
F = lambda w, s: ImageFont.truetype(f"{S}/fonts/Poppins-{w}.ttf", s)

# ---------------------------------------------------------------- shot list
# (start, end, kind, file, in_point, tag)
V, P = "v", "p"
SHOTS = [
    # 0-3 hook
    (0.00, 1.00, V, "hy_sp/IMG_3879.MOV", 1.6, None),
    (1.00, 2.00, V, "hy_sp/IMG_3784.MOV", 0.6, None),
    (2.00, 3.00, V, "hy_sp/IMG_3842.MOV", 0.4, None),
    # 3-9 foto e video
    (3.00, 3.75, V, "man_integ/IMG_7154.MOV", 0.5, None),
    (3.75, 4.50, P, "avita_f/IMG_9362.jpg", 0, None),
    (4.50, 5.25, V, "hy_sp/IMG_3832.MOV", 2.6, None),
    (5.25, 6.00, V, "man_integ/IMG_7312.MOV", 0.6, None),
    (6.00, 6.75, V, "avita_v/IMG_7197.MOV", 14.6, None),
    (6.75, 7.50, P, "hy_fimdeano/DSC09065.jpg", 0, None),
    (7.50, 8.25, V, "man_integ/IMG_7332.MOV", 0.8, None),
    (8.25, 9.00, V, "hy_sp/IMG_3854.MOV", 1.6, None),
    # 9-18 eventos
    (9.00, 10.00, V, "hy_sp/IMG_3829.MOV", 1.5, "HYUNDAI"),
    (10.00, 10.75, V, "hy_sp/IMG_3766.MOV", 2.0, "HYUNDAI"),
    (10.75, 11.50, P, "manifesta/1 (8).jpg", 0, "MANIFESTA · TERRAÇO"),
    (11.50, 12.25, V, "man_integ/IMG_7347.MOV", 0.6, "MANIFESTA · TERRAÇO"),
    (12.25, 13.00, V, "man_integ/IMG_7338.MOV", 0.5, "MANIFESTA · TERRAÇO"),
    (13.00, 14.00, V, "avita_v/IMG_7196.MOV", 25.0, "ECOTERRA · ESPAÇO AVITA"),
    (14.00, 14.75, V, "avita_v/IMG_7192.MOV", 9.6, "ECOTERRA · ESPAÇO AVITA"),
    (14.75, 15.50, V, "avita_v/IMG_7191.MOV", 6.0, "ECOTERRA · ESPAÇO AVITA"),
    (15.50, 16.25, P, "hy_fimdeano/DSC09192.jpg", 0, "HYUNDAI"),
    (16.25, 17.00, P, "hy_fimdeano/DSC09258.jpg", 0, "HYUNDAI"),
    (17.00, 18.00, V, "man_integ/IMG_7329.MOV", 0.6, "MANIFESTA"),
    # 18-22 interacao
    (18.00, 18.75, V, "man_integ/IMG_7320.MOV", 0.6, None),
    (18.75, 19.50, V, "avita_v/IMG_7197.MOV", 20.6, None),
    (19.50, 20.25, V, "man_integ/IMG_7345.MOV", 0.8, None),
    (20.25, 21.00, V, "hy_sp/IMG_3842.MOV", 2.6, None),
    (21.00, 21.50, V, "man_integ/IMG_7348.MOV", 0.6, None),
    (21.50, 22.00, V, "hy_sp/IMG_3879.MOV", 3.6, None),
    # 22-25 end card background (dark, blurred)
    (22.00, 25.00, V, "hy_sp/IMG_3829.MOV", 0.2, None),
]

# ---------------------------------------------------------------- frame sources
OS = 1.10  # oversize for punch-in / ken burns
BW, BH = int(W * OS) // 2 * 2, int(H * OS) // 2 * 2

def video_frames(path, t_in, dur):
    n = int(round(dur * FPS))
    cmd = ["ffmpeg", "-v", "error", "-ss", str(t_in), "-i", path, "-t", str(dur + 0.2),
           "-vf", f"scale={BW}:{BH}:force_original_aspect_ratio=increase,crop={BW}:{BH},fps={FPS}",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    out, last = [], None
    for _ in range(n):
        b = p.stdout.read(BW * BH * 3)
        if len(b) < BW * BH * 3:
            out.append(last); continue
        last = Image.frombytes("RGB", (BW, BH), b); out.append(last)
    p.stdout.close(); p.wait()
    return out

def photo_frames(path, dur):
    n = int(round(dur * FPS))
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    k = max(BW / im.width, BH / im.height)
    im = im.resize((math.ceil(im.width * k), math.ceil(im.height * k)), Image.LANCZOS)
    x0, y0 = (im.width - BW) // 2, (im.height - BH) // 2
    return [im.crop((x0, y0, x0 + BW, y0 + BH))] * n  # motion applied in place()

def place(img, u, kind, idx):
    """u in [0,1] progress within the shot. Punch-in at cut (video) / slow push (photo)."""
    if kind == V:
        z = 1.0 + 0.09 * (1 - u) ** 3 + 0.0  # snap in, settle
    else:
        z = 1.0 + 0.09 * u
    cw, ch = W * OS / z / OS, H * OS / z / OS  # region in base units of W,H scaled
    cw, ch = BW / (OS * z) * 1.0, BH / (OS * z) * 1.0
    # photos drift sideways a bit, alternating direction
    dx = ((u - 0.5) * 40 * (1 if idx % 2 else -1)) if kind == P else 0
    cx, cy = BW / 2 + dx, BH / 2
    box = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
    return img.resize((W, H), Image.BICUBIC, box=box)

# ---------------------------------------------------------------- grading
_vig = None
def grade(im):
    global _vig
    im = ImageEnhance.Contrast(im).enhance(1.06)
    im = ImageEnhance.Color(im).enhance(1.08)
    if _vig is None:
        yy, xx = np.mgrid[0:H, 0:W]
        d = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
        _vig = Image.fromarray((np.clip(1 - 0.32 * np.clip(d - 0.55, 0, None) ** 1.5, 0, 1) * 255).astype(np.uint8))
    blk = Image.new("RGB", (W, H), (0, 0, 0))
    return Image.composite(im, blk, _vig)

# ---------------------------------------------------------------- text
def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3

def text_block(lines, font, hl=None, pad=(34, 16), gap=14, radius=14):
    """lines: list of str. hl: set of words to colour orange. Returns RGBA image of stacked pills."""
    hl = hl or set()
    rows = []
    for ln in lines:
        words = ln.split(" ")
        sp = font.getlength(" ")
        wsz = [font.getlength(w) for w in words]
        tw = sum(wsz) + sp * (len(words) - 1)
        asc, desc = font.getmetrics()
        th = asc + desc
        rows.append((words, wsz, sp, tw, th, asc))
    bw = int(max(r[3] for r in rows) + 2 * pad[0])
    rh = [r[4] + 2 * pad[1] for r in rows]
    bh = int(sum(rh) + gap * (len(rows) - 1))
    img = Image.new("RGBA", (bw, bh), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    y = 0
    for (words, wsz, sp, tw, th, asc), h in zip(rows, rh):
        x0 = (bw - (tw + 2 * pad[0])) / 2
        d.rounded_rectangle((x0, y, x0 + tw + 2 * pad[0], y + h), radius, fill=(20, 20, 22, 215))
        x = x0 + pad[0]
        for w, ww in zip(words, wsz):
            col = ORANGE if w.strip(".,?!").lower() in hl else WHITE
            d.text((x, y + pad[1] - 2), w, font=font, fill=col)
            x += ww + sp
        y += h + gap
    return img

def paste_anim(base, blk, cx, cy, t, t0, t1, style="up"):
    if t < t0 or t > t1: return
    a_in = ease((t - t0) / 0.28); a_out = 1 - ease((t - (t1 - 0.22)) / 0.22)
    a = min(a_in, a_out)
    if a <= 0: return
    off = int((1 - a_in) * 60) if style == "up" else 0
    sc = 0.85 + 0.15 * a_in if style == "pop" else 1.0
    b = blk
    if sc != 1.0:
        b = blk.resize((max(1, int(blk.width * sc)), max(1, int(blk.height * sc))), Image.BICUBIC)
    if a < 1:
        al = b.getchannel("A").point(lambda v: int(v * a)); b = b.copy(); b.putalpha(al)
    base.paste(b, (int(cx - b.width / 2), int(cy - b.height / 2 + off)), b)

FX = F("ExtraBold", 82); FT = F("Bold", 40)
T_HOOK = text_block(["A confraternização", "da firma está", "chegando?"], FX, {"confraternização", "chegando"})
T_FOTO = text_block(["Foto e vídeo", "para guardar", "cada momento"], FX, {"foto", "vídeo"})
T_EQUIPE = text_block(["Sua equipe merece", "uma lembrança", "especial"], FX, {"lembrança", "especial"})
TAGS = {}
def tag_img(s):
    if s not in TAGS:
        f = FT; tw = f.getlength(s); im = Image.new("RGBA", (int(tw + 80), 80), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((0, 0, im.width - 1, 79), 40, fill=ORANGE + (240,))
        d.text((40, 14), s, font=f, fill=WHITE); TAGS[s] = im
    return TAGS[s]

logo = Image.open(f"{SRC}/brand/DocMe nova versão-4.pdf.png").convert("RGBA"); logo = logo.crop(logo.getbbox())
LOGO = logo.resize((820, round(logo.height * 820 / logo.width)), Image.LANCZOS)
LOGO_S = logo.resize((250, round(logo.height * 210 / logo.width)), Image.LANCZOS)
FEND = F("ExtraBold", 92)
T_END1 = text_block(["Ainda dá tempo."], FEND, set())
T_END2 = text_block(["DocMe."], FEND, {"docme"})
FSUB = F("SemiBold", 40)
def sub_img(s):
    tw = FSUB.getlength(s); im = Image.new("RGBA", (int(tw + 10), 60), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((5, 4), s, font=FSUB, fill=(230, 230, 232)); return im
T_SUB = sub_img("Foto e vídeo para confraternizações")

def overlay(base, t):
    # small logo watermark top-left through the edit (not on end card)
    if t < 22.0:
        a = min(ease(t / 0.4), 1 - ease((t - 21.8) / 0.2))
        lg = LOGO_S.copy(); lg.putalpha(lg.getchannel("A").point(lambda v: int(v * 0.92 * a)))
        base.paste(lg, (60, 210), lg)
    paste_anim(base, T_HOOK, W / 2, 820, t, 0.15, 2.95, "up")
    paste_anim(base, T_FOTO, W / 2, 820, t, 3.10, 8.95, "up")
    paste_anim(base, T_EQUIPE, W / 2, 820, t, 18.10, 21.95, "up")
    for (s0, s1, k, f, tin, tag) in SHOTS:
        if tag and s0 <= t < s1:
            im = tag_img(tag); base.paste(im, (int(W / 2 - im.width / 2), 1330), im)
    if t >= 22.0:
        u = t - 22.0
        # logo
        a = ease(u / 0.45); sc = 0.9 + 0.1 * a
        lg = LOGO.resize((int(LOGO.width * sc), int(LOGO.height * sc)), Image.LANCZOS)
        lg.putalpha(lg.getchannel("A").point(lambda v: int(v * a)))
        base.paste(lg, (int(W / 2 - lg.width / 2), int(700 - lg.height / 2)), lg)
        paste_anim(base, T_END1, W / 2, 1060, t, 22.30, 25.5, "up")
        paste_anim(base, T_END2, W / 2, 1210, t, 23.35, 25.5, "pop")
        # orange underline grows
        g = ease((u - 1.6) / 0.5)
        if g > 0:
            d = ImageDraw.Draw(base); L = int(420 * g)
            d.rounded_rectangle((W / 2 - L / 2, 1320, W / 2 + L / 2, 1332), 6, fill=ORANGE)
        paste_anim(base, T_SUB, W / 2, 1410, t, 23.9, 25.5, "up")
    return base

def endcard_bg(im, u):
    im = im.filter(ImageFilter.GaussianBlur(18))
    dk = Image.new("RGB", (W, H), DARK)
    return Image.blend(im, dk, 0.55 + 0.33 * ease(u / 0.6))

# ---------------------------------------------------------------- render
def frames():
    for idx, (s0, s1, k, f, tin, tag) in enumerate(SHOTS):
        f0, f1 = round(s0 * FPS), round(s1 * FPS); dur = (f1 - f0) / FPS; path = f"{SRC}/{f}"
        fr = video_frames(path, tin, dur) if k == V else photo_frames(path, dur)
        n = len(fr)
        for i, im in enumerate(fr):
            t = (f0 + i) / FPS; u = i / max(1, n - 1)
            if s0 >= 22.0:
                out = endcard_bg(im.resize((W, H), Image.BICUBIC), t - 22.0)
            else:
                out = grade(place(im, u, k, idx))
                # white flash on section starts
                if s0 in (3.0, 9.0, 18.0) and i < 3:
                    out = Image.blend(out, Image.new("RGB", (W, H), WHITE), [0.55, 0.3, 0.12][i])
            yield t, overlay(out, t)

if __name__ == "__main__":
    prev = os.environ.get("PREVIEW")
    if prev:
        want = [float(x) for x in prev.split(",")]
        got = {}
        for t, im in frames():
            for w in want:
                if w not in got and abs(t - w) < 0.5 / FPS + 1e-6:
                    got[w] = im.copy()
            if len(got) == len(want): break
        for w, im in got.items():
            im.resize((540, 960)).save(f"{S}/prev/p_{w:05.2f}.jpg", quality=85)
        sys.exit()
    out = sys.argv[1]
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                          "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    n = 0
    for t, im in frames():
        p.stdin.write(im.tobytes()); n += 1
    p.stdin.close(); p.wait(); print("frames", n)
