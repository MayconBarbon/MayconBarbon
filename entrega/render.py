import sys, subprocess, numpy as np, cv2

S = sys.argv[1]
OUT = sys.argv[2]
FPS = 30
W, H = 1080, 1920
AR = W / H

# (file, start, end, cx0, cx1, cy0, cy1, z0, z1, label)
# cx/cy = normalized window centre in source; z = zoom (1 = full source height)
SHOTS = [
    # GANCHO 0-3
    ("0483", 0.0, 3.0, .58, .56, .52, .46, 1.00, 1.18, "Gancho: fachada/jardim - push-in pelo caminho"),
    # CONTEXTO 3-8
    ("0489", 3.0, 4.5, .26, .60, .56, .56, 1.06, 1.06, "Pátio de acesso - travelling lateral"),
    ("0742", 4.5, 6.0, .42, .37, .52, .49, 1.00, 1.20, "Hall de entrada - dolly-in até a porta"),
    ("0492", 6.0, 8.0, .54, .79, .46, .46, 1.00, 1.04, "Logo do centro - travelling sobre o painel"),
    # TOUR 8-22
    ("0501", 8.0, 10.0, .68, .22, .55, .55, 1.06, 1.06, "Recepção - travelling lateral"),
    ("0543", 10.0, 11.5, .55, .57, .56, .54, 1.00, 1.20, "Corredor - dolly-in"),
    ("0507", 11.5, 13.5, .40, .68, .56, .56, 1.06, 1.06, "Sala de espera - travelling lateral"),
    ("0555", 13.5, 15.5, .46, .46, .36, .52, 1.22, 1.02, "Sala de reunião - tilt down + afastamento"),
    ("0549", 15.5, 17.5, .28, .64, .60, .60, 1.06, 1.06, "Sala de atendimento - travelling lateral"),
    ("0526", 17.5, 19.0, .46, .54, .55, .53, 1.00, 1.16, "Sala pedagógica - push-in"),
    ("0606", 19.0, 20.5, .28, .60, .52, .52, 1.06, 1.06, "Sala psicomotora - travelling lateral"),
    ("0702", 20.5, 22.0, .44, .44, .60, .40, 1.25, 1.25, "Escada de cordas - tilt up"),
    # VIRADA 22-27
    ("0585", 22.0, 24.5, .62, .50, .68, .55, 1.30, 1.00, "Virada: sala sensorial - pull-out revelando"),
    ("0717", 24.5, 27.0, .66, .42, .58, .56, 1.04, 1.04, "Sala sensorial (2º ângulo) - lateral + afastamento"),
    # CHAMADA 27-30
    ("0603", 27.0, 30.0, .50, .50, .50, .50, 1.00, 1.22, "Chamada: ginásio rumo ao jardim - dolly-in"),
    # FECHAMENTO EXTERNO 30-42.5
    ("0642", 30.0, 32.0, .50, .50, .56, .54, 1.00, 1.16, "Jardim sensorial - dolly-in"),
    ("0711", 32.0, 34.5, .26, .58, .60, .60, 1.02, 1.02, "Piscina - travelling lateral"),
    ("TL", 34.5, 42.5, .31, .34, .52, .50, 1.00, 1.12, "Jardim e casa (0648) - timelapse dia > pôr do sol > noite, push-in lento"),
]
RADIAL = [8.0, 22.0, 30.0]
XFADE = {16: 0.5}            # dissolve piscina -> timelapse
FADE_OUT = (41.85, 42.5)
TOTAL = SHOTS[-1][2]


def grade(img, wb=True):
    f = img.astype(np.float32) / 255.0
    # partial gray-world white balance (harmonise, keep real look)
    if wb:
        m = f.reshape(-1, 3).mean(0)
        g = m.mean()
        f = f * (1 + 0.18 * (g / m - 1))
    # gentle saturation reduction (sources are punchy HDR)
    lum = (f * np.array([0.114, 0.587, 0.299], np.float32)).sum(2, keepdims=True)
    f = lum + (f - lum) * 0.90
    # soft S-curve + highlight roll-off
    f = np.clip(f, 0, 1)
    s = f * f * (3 - 2 * f)
    f = 0.82 * f + 0.18 * s
    f = 1 - (1 - f) ** 1.0
    f = np.minimum(f, 0.97 + 0.03 * f)
    return np.clip(f * 255, 0, 255).astype(np.uint8)


def ease(t):
    t = min(max(t, 0.0), 1.0)
    sm = t * t * t * (t * (6 * t - 15) + 10)
    return 0.45 * t + 0.55 * sm


G = S + '/gen/'
TLD = grade(cv2.imread(G + 'day_al.jpg')).astype(np.float32)
TLG = grade(cv2.imread(G + 'golden.jpg'), wb=False).astype(np.float32)
TLN = grade(cv2.imread(G + 'night_al.jpg'), wb=False).astype(np.float32)
_lm = cv2.imread(G + 'lightmask.png', 0)
_nl, _lab, _st, _cent = cv2.connectedComponentsWithStats((_lm > 0).astype(np.uint8))
# group lights left->right into 7 groups; each switches on at its own moment
_order = sorted(range(1, _nl), key=lambda i: _cent[i][0])
NG = 7
LGROUPS, LT = [], []
for gi in range(NG):
    ids = _order[gi * len(_order) // NG:(gi + 1) * len(_order) // NG]
    mk = np.isin(_lab, ids).astype(np.float32)
    LGROUPS.append(cv2.GaussianBlur(mk, (0, 0), 6)[..., None])
    LT.append(4.35 + [0.0, 0.5, 0.15, 0.65, 0.3, 0.8, 0.95][gi])
MALL = np.clip(sum(LGROUPS), 0, 1)
TLN_OFF = TLN * (1 - 0.72 * MALL)


def sm(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def tl_frame(t):
    u = t - SHOTS[-1][1]
    a1 = sm((u - 0.9) / 2.3)   # day -> golden
    a2 = sm((u - 3.1) / 2.2)   # golden -> night (lights off)
    f = TLD * (1 - a1) + TLG * a1
    f = f * (1 - a2) + TLN_OFF * a2
    if a2 > 0:
        for mk, ts in zip(LGROUPS, LT):
            on = sm((u - ts) / 0.18)
            if on > 0:
                f += (TLN - TLN_OFF) * (mk * (on * a2))
    return np.clip(f, 0, 255).astype(np.uint8)


src = {}
for sh in SHOTS:
    k = sh[0]
    if k == 'TL':
        continue
    if k not in src:
        im = cv2.imread(f"{S}/img/IMG_{k}.jpg")
        src[k] = grade(im)

yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
VIG = (1 - 0.16 * np.clip(r - 0.55, 0, 1) ** 1.6)[..., None].astype(np.float32)


def shot_frame(i, t, extra_zoom=1.0):
    k, a, b, cx0, cx1, cy0, cy1, z0, z1, _ = SHOTS[i]
    img = tl_frame(t) if k == 'TL' else src[k]
    sh_, sw_ = img.shape[:2]
    p = ease((t - a) / (b - a))
    z = (z0 + (z1 - z0) * p) * extra_zoom
    wh = sh_ / z
    ww = wh * AR
    cx = (cx0 + (cx1 - cx0) * p) * sw_
    cy = (cy0 + (cy1 - cy0) * p) * sh_
    cx = min(max(cx, ww / 2), sw_ - ww / 2)
    cy = min(max(cy, wh / 2), sh_ - wh / 2)
    s = H / wh
    M = np.array([[s, 0, W / 2 - s * cx], [0, s, H / 2 - s * cy]], np.float32)
    return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)


def radial_blur(fr, strength, n=12):
    if strength < 0.004:
        return fr
    acc = np.zeros(fr.shape, np.float32)
    for j in range(n):
        sc = 1 + strength * j / (n - 1)
        M = cv2.getRotationMatrix2D((W / 2, H / 2), 0, sc)
        acc += cv2.warpAffine(fr, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return (acc / n).astype(np.uint8)


def shot_index(t):
    for i, sh in enumerate(SHOTS):
        if sh[1] <= t < sh[2]:
            return i
    return len(SHOTS) - 1


import os
if os.environ.get('STILLS'):
    tiles = []
    for i, sh in enumerate(SHOTS):
        for t in (sh[1] + 0.01, sh[2] - 0.01):
            f = cv2.resize(shot_frame(i, t), (270, 480))
            cv2.putText(f, f"{i+1} {sh[0]}", (8, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            tiles.append(f)
    rows = [np.hstack(tiles[k:k + 12]) for k in range(0, len(tiles), 12)]
    rows[-1] = np.hstack([rows[-1], np.zeros((480, 270 * 12 - rows[-1].shape[1], 3), np.uint8)])
    for k, rw in enumerate(rows):
        cv2.imwrite(f"{OUT}_{k}.jpg", rw)
    sys.exit()

from PIL import Image, ImageDraw, ImageFont, ImageFilter
FD = S + '/fonts/PlayfairItalic.ttf'
INTER_L = '/usr/share/fonts/opentype/inter/Inter-Light.otf'
INTER_SB = '/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'


def text_patch(txt, font, size, track=0):
    f = ImageFont.truetype(font, size)
    pad = 40
    if track:
        w = sum(f.getlength(c) + track for c in txt) - track
    else:
        w = f.getlength(txt)
    asc, desc = f.getmetrics()
    im = Image.new('L', (int(w) + 2 * pad, asc + desc + 2 * pad), 0)
    d = ImageDraw.Draw(im)
    if track:
        x = pad
        for c in txt:
            d.text((x, pad), c, font=f, fill=255); x += f.getlength(c) + track
    else:
        d.text((pad, pad), txt, font=f, fill=255)
    a = np.asarray(im, np.float32) / 255
    sh = np.asarray(im.filter(ImageFilter.GaussianBlur(10)), np.float32) / 255
    return a, sh, pad


# (text, font, size, tracking, x, y_baseline_top, t_in, t_out)
TEXTS = [
    ("Parece só uma casa…", FD, 96, 0, 90, 1150, 0.25, 2.80),
    ("até você entrar.", FD, 96, 0, 90, 1270, 1.05, 2.80),
    ("AURORA TEHABILITAR", INTER_SB, 30, 6, 94, 1130, 27.25, 29.80),
    ("Conheça", FD, 112, 0, 90, 1180, 27.45, 29.80),
    ("nosso espaço.", FD, 112, 0, 90, 1310, 27.75, 29.80),
    ("Aurora TeHabilitar", FD, 92, 0, 90, 1200, 39.9, 42.5),
    ("CENTRO DE NEURODESENVOLVIMENTO", INTER_L, 30, 5, 94, 1330, 40.25, 42.5),
]
TP = [text_patch(t[0], t[1], t[2], t[3]) for t in TEXTS]
TEXT_WINDOWS = [(0.25, 2.8), (27.25, 29.8), (39.9, 42.5)]
GY = np.clip((np.arange(H, dtype=np.float32) / H - 0.45) / 0.30, 0, 1)
GY = (GY * GY * (3 - 2 * GY))[:, None, None]


def draw_texts(f, t):
    # readability gradient
    g = 0.0
    for a, b in TEXT_WINDOWS:
        if a - 0.3 <= t <= b + 0.3:
            g = max(g, min(1, (t - (a - 0.3)) / 0.5, (b + 0.3 - t) / 0.4))
    if g > 0:
        f *= (1 - 0.42 * g * GY)
    for (txt, font, size, tr, x, y, ti, to), (a, sh, pad) in zip(TEXTS, TP):
        if not (ti <= t <= to):
            continue
        u = min(1, (t - ti) / 0.55)
        u = u * u * (3 - 2 * u)
        o = u * min(1, (to - t) / 0.3)
        yy0 = int(y + 26 * (1 - u)) - pad
        xx0 = x - pad
        h_, w_ = a.shape
        reg = f[yy0:yy0 + h_, xx0:xx0 + w_]
        hh, ww = reg.shape[:2]
        A = a[:hh, :ww, None] * o; SH = sh[:hh, :ww, None] * o * 0.55
        reg *= (1 - SH)
        reg[:] = reg * (1 - A) + 250 * A
    return f


RT = 0.30  # half-length of radial transition (s)
ff = subprocess.Popen(
    ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS),
     "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", OUT],
    stdin=subprocess.PIPE)

N = int(round(TOTAL * FPS))
for n in range(N):
    t = (n + 0.5) / FPS
    i = shot_index(t)
    ez, blur = 1.0, 0.0
    for c in RADIAL:
        d = t - c
        if -RT < d < 0:      # outgoing: accelerate in
            u = (d + RT) / RT
            ez, blur = 1 + 0.18 * u ** 2, 0.16 * u ** 2
        elif 0 <= d < RT:    # incoming: settle out
            u = 1 - d / RT
            ez, blur = 1 + 0.18 * u ** 2, 0.16 * u ** 2
    fr = shot_frame(i, t, ez)
    # dissolve
    for j, dur in XFADE.items():
        c = SHOTS[j][2]
        if c - dur / 2 <= t < c + dur / 2:
            a = (t - (c - dur / 2)) / dur
            a = a * a * (3 - 2 * a)
            fa = shot_frame(j, t)
            fb = shot_frame(j + 1, t)
            fr = cv2.addWeighted(fa, 1 - a, fb, a, 0)
    fr = radial_blur(fr, blur)
    f = fr.astype(np.float32) * VIG
    f = draw_texts(f, t)
    if t > FADE_OUT[0]:
        f *= max(0.0, 1 - (t - FADE_OUT[0]) / (FADE_OUT[1] - FADE_OUT[0]))
    ff.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes())
    if n % 150 == 0:
        print(f"frame {n}/{N}", flush=True)
ff.stdin.close()
ff.wait()
print("done")
