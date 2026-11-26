"""v4 renderer: 2.5D parallax from depth maps + fast speed-ramped camera moves,
motion blur (sub-frame accumulation), whip / zoom-through transitions, captions,
and the day->night timelapse closing shot.
usage: python3 render4.py <scratch_dir> <out.mp4>   (STILLS=1 for a framing contact sheet)"""
import sys, os, subprocess, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S, OUT = sys.argv[1], sys.argv[2]
FPS, W, H = 30, 1080, 1920
AR = W / H
SUB = int(os.environ.get('SUB', 3))          # motion-blur sub-frames

# file, t0, t1, cx0, cx1, cy0, cy1, z0, z1, dolly0, dolly1, px0, px1, py0, py1, ease, out_transition, label
# dolly = depth-dependent magnification (near grows faster than far);  px/py = parallax shift in output px
SHOTS = [
    ("0483", 0.0, 3.0, .58, .56, .53, .47, 1.00, 1.40, 0, .20, 0, -30, 0, 0, "ramp", "whipR", "Gancho: fachada - dolly-in rápido pelo caminho + paralaxe"),
    ("0489", 3.0, 4.5, .22, .60, .56, .56, 1.12, 1.12, 0, .04, 0, -110, 0, 0, "smooth", "cut", "Pátio - travelling lateral com paralaxe"),
    ("0742", 4.5, 6.0, .47, .41, .52, .48, 1.00, 1.52, 0, .26, 0, 0, 0, 0, "accel", "cut", "Hall - dolly-in acelerando até a porta"),
    ("0492", 6.0, 8.0, .54, .80, .46, .46, 1.02, 1.10, 0, .05, 0, 70, 0, 0, "smooth", "zoom", "Logo - travelling lateral sobre o painel"),
    ("0501", 8.0, 10.0, .70, .22, .55, .55, 1.14, 1.14, 0, .05, 0, 120, 0, 0, "ramp", "whipL", "Recepção - travelling lateral rápido + paralaxe"),
    ("0543", 10.0, 11.5, .55, .57, .56, .54, 1.00, 1.48, 0, .26, 0, 0, 0, 0, "accel", "zoom", "Corredor - dolly-in acelerando (zoom-through)"),
    ("0507", 11.5, 13.5, .38, .70, .56, .56, 1.12, 1.12, 0, .05, 0, -120, 0, 0, "ramp", "cut", "Sala de espera - travelling lateral + paralaxe"),
    ("0555", 13.5, 15.5, .46, .46, .33, .54, 1.34, 1.04, .10, -.06, 0, 0, 60, -40, "ramp", "cut", "Sala de reunião - crane down + afastamento"),
    ("0549", 15.5, 17.5, .26, .66, .60, .60, 1.12, 1.12, 0, .04, 0, -120, 0, 0, "smooth", "whipR", "Sala de atendimento - travelling lateral + paralaxe"),
    ("0526", 17.5, 19.0, .46, .55, .55, .52, 1.00, 1.40, 0, .22, 0, 0, 0, 0, "ramp", "cut", "Sala pedagógica - dolly-in rápido"),
    ("0606", 19.0, 20.5, .26, .62, .52, .52, 1.12, 1.12, 0, .04, 0, -120, 0, 0, "smooth", "cut", "Sala psicomotora - travelling lateral + paralaxe"),
    ("0702", 20.5, 22.0, .44, .44, .64, .38, 1.30, 1.36, 0, .06, 0, 0, -70, 60, "accel", "zoom", "Escada de cordas - tilt up com paralaxe"),
    ("0585", 22.0, 24.5, .62, .50, .70, .55, 1.55, 1.00, .14, -.04, 0, 0, 0, 0, "ramp", "whipL", "Virada: sala sensorial - pull-out explosivo"),
    ("0717", 24.5, 27.0, .70, .40, .58, .56, 1.12, 1.12, 0, .05, 0, 130, 0, 0, "smooth", "cut", "Sala sensorial 2 - travelling lateral + paralaxe"),
    ("0603", 27.0, 30.0, .50, .50, .50, .50, 1.00, 1.50, 0, .24, 0, 0, 0, 0, "accel", "zoom", "Chamada: ginásio rumo ao jardim - dolly-in"),
    ("0642", 30.0, 32.0, .50, .50, .57, .53, 1.00, 1.38, 0, .20, 0, 0, 0, 0, "ramp", "whipR", "Jardim sensorial - dolly-in rápido"),
    ("0711", 32.0, 34.5, .24, .60, .60, .60, 1.06, 1.06, 0, .04, 0, -120, 0, 0, "smooth", "xfade", "Piscina - travelling lateral + paralaxe"),
    ("TL", 34.5, 42.5, .31, .35, .52, .49, 1.00, 1.18, 0, .07, 0, -30, 0, 0, "smooth", "end", "Jardim (0648) - timelapse dia > noite"),
]
TOTAL = SHOTS[-1][2]
FADE_OUT = (41.85, 42.5)


def grade(img, wb=True):
    f = img.astype(np.float32) / 255.0
    if wb:
        m = f.reshape(-1, 3).mean(0)
        f = f * (1 + 0.18 * (m.mean() / m - 1))
    lum = (f * np.array([0.114, 0.587, 0.299], np.float32)).sum(2, keepdims=True)
    f = lum + (f - lum) * 0.90
    f = np.clip(f, 0, 1)
    f = 0.82 * f + 0.18 * f * f * (3 - 2 * f)
    f = np.minimum(f, 0.97 + 0.03 * f)
    return np.clip(f * 255, 0, 255).astype(np.uint8)


def ease(t, kind):
    t = min(max(t, 0.0), 1.0)
    if kind == "ramp":      # fast start, long settle (speed ramp)
        return 1 - (1 - t) ** 2.8
    if kind == "accel":     # builds speed into the next transition
        return 0.25 * t + 0.75 * t ** 2.4
    sm = t * t * t * (t * (6 * t - 15) + 10)
    return 0.45 * t + 0.55 * sm


def sm(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


# ---------- sources + depth ----------
src, disp = {}, {}
for sh in SHOTS:
    k = sh[0]
    if k == "TL" or k in src:
        continue
    hi = grade(cv2.imread(f"{S}/imghi/IMG_{k}.jpg"))
    lo = cv2.resize(hi, (3000, 2000), interpolation=cv2.INTER_AREA)
    d = np.load(f"{S}/depth/IMG_{k}.npy").astype(np.float32)
    src[k] = (hi, lo)
    disp[k] = (cv2.resize(d, (hi.shape[1], hi.shape[0]), interpolation=cv2.INTER_LINEAR), d)

G = S + "/gen/"
TLD = grade(cv2.imread(G + "day_al.jpg")).astype(np.float32)
TLG = grade(cv2.imread(G + "golden.jpg"), wb=False).astype(np.float32)
TLN = grade(cv2.imread(G + "night_al.jpg"), wb=False).astype(np.float32)
_dtl = np.load(f"{S}/depth/day_al.npy").astype(np.float32)
disp["TL"] = (_dtl, _dtl)
_lm = cv2.imread(G + "lightmask.png", 0)
_nl, _lab, _st, _cent = cv2.connectedComponentsWithStats((_lm > 0).astype(np.uint8))
_order = sorted(range(1, _nl), key=lambda i: _cent[i][0])
NG = 7
LGROUPS, LT = [], []
for gi in range(NG):
    ids = _order[gi * len(_order) // NG:(gi + 1) * len(_order) // NG]
    LGROUPS.append(cv2.GaussianBlur(np.isin(_lab, ids).astype(np.float32), (0, 0), 6)[..., None])
    LT.append(4.35 + [0.0, 0.5, 0.15, 0.65, 0.3, 0.8, 0.95][gi])
MALL = np.clip(sum(LGROUPS), 0, 1)
TLN_OFF = TLN * (1 - 0.72 * MALL)


def tl_image(t):
    u = t - SHOTS[-1][1]
    a1 = sm((u - 0.9) / 2.3)
    a2 = sm((u - 3.1) / 2.2)
    f = TLD * (1 - a1) + TLG * a1
    f = f * (1 - a2) + TLN_OFF * a2
    if a2 > 0:
        for mk, ts in zip(LGROUPS, LT):
            on = sm((u - ts) / 0.18)
            if on > 0:
                f += (TLN - TLN_OFF) * (mk * (on * a2))
    return np.clip(f, 0, 255).astype(np.uint8)


UU, VV = np.meshgrid(np.arange(W, dtype=np.float32) - W / 2, np.arange(H, dtype=np.float32) - H / 2)


def shot_frame(i, t, extra_zoom=1.0, shift=(0.0, 0.0)):
    k, a, b, cx0, cx1, cy0, cy1, z0, z1, d0, d1, px0, px1, py0, py1, ek = SHOTS[i][:16]
    p = ease((t - a) / (b - a), ek)
    L = lambda u0, u1: u0 + (u1 - u0) * p
    z = L(z0, z1) * extra_zoom
    lvl = 0 if z >= 1.30 else 1            # pyramid level: avoid moire when downscaling
    img = tl_image(t) if k == "TL" else src[k][lvl]
    dm = disp[k][lvl]
    sh_, sw_ = img.shape[:2]
    wh = sh_ / z
    ww = wh * AR
    cx = min(max(L(cx0, cx1) * sw_, ww / 2), sw_ - ww / 2)
    cy = min(max(L(cy0, cy1) * sh_, wh / 2), sh_ - wh / 2)
    s = H / wh
    X = cx + (UU - shift[0]) / s
    Y = cy + (VV - shift[1]) / s
    dol, px, py = L(d0, d1), L(px0, px1), L(py0, py1)
    if abs(dol) > 1e-4 or abs(px) > 0.05 or abs(py) > 0.05:
        dc = float(dm[int(cy), int(cx)])          # focus plane = frame centre stays put
        Xs, Ys = X, Y
        for _ in range(2):                         # fixed-point: sample depth where we land
            dd = cv2.remap(dm, Xs, Ys, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT) - dc
            mag = 1 + dol * dd
            Xs = cx + (X - cx) / mag + px * dd / s
            Ys = cy + (Y - cy) / mag + py * dd / s
        X, Y = Xs, Ys
    return cv2.remap(img, X, Y, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)


# ---------- transitions ----------
RT = 0.28
WT = 0.16


def radial_blur(fr, strength, n=10):
    if strength < 0.004:
        return fr
    acc = np.zeros(fr.shape, np.float32)
    for j in range(n):
        M = cv2.getRotationMatrix2D((W / 2, H / 2), 0, 1 + strength * j / (n - 1))
        acc += cv2.warpAffine(fr, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return (acc / n).astype(np.uint8)


def hblur(fr, n):
    n = int(n)
    if n < 3:
        return fr
    k = np.ones((1, n), np.float32) / n
    return cv2.filter2D(fr, -1, k, borderType=cv2.BORDER_REFLECT)


def shot_index(t):
    for i, sh in enumerate(SHOTS):
        if sh[1] <= t < sh[2]:
            return i
    return len(SHOTS) - 1


def raw_frame(t):
    i = shot_index(t)
    # zoom-through around a cut
    for j, sh in enumerate(SHOTS[:-1]):
        c, tr = sh[2], sh[16]
        if tr == "zoom" and -RT < t - c < RT:
            d = t - c
            u = (d + RT) / RT if d < 0 else 1 - d / RT
            fr = shot_frame(i, t, 1 + 0.22 * u ** 2)
            return radial_blur(fr, 0.20 * u ** 2)
        if tr in ("whipL", "whipR") and -WT < t - c < WT:
            d = t - c
            sg = 1 if tr == "whipR" else -1         # direction content travels
            u = (d + WT) / WT if d < 0 else 1 - d / WT
            off = 0.55 * W * u ** 2.2
            if d < 0:
                fr = shot_frame(i, t, 1.0, (-sg * off, 0))
            else:
                fr = shot_frame(i, t, 1.0, (sg * off, 0))
            return hblur(fr, 170 * u ** 1.5)
        if tr == "xfade" and -0.25 <= t - c < 0.25:
            a = sm((t - c + 0.25) / 0.5)
            return cv2.addWeighted(shot_frame(j, t), 1 - a, shot_frame(j + 1, t), a, 0)
    return shot_frame(i, t)


# ---------- captions ----------
FD = S + "/fonts/PlayfairItalic.ttf"
INTER_L = "/usr/share/fonts/opentype/inter/Inter-Light.otf"
INTER_SB = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"


def text_patch(txt, font, size, track=0):
    f = ImageFont.truetype(font, size)
    pad = 40
    w = (sum(f.getlength(c) + track for c in txt) - track) if track else f.getlength(txt)
    asc, desc = f.getmetrics()
    im = Image.new("L", (int(w) + 2 * pad, asc + desc + 2 * pad), 0)
    d = ImageDraw.Draw(im)
    if track:
        x = pad
        for c in txt:
            d.text((x, pad), c, font=f, fill=255); x += f.getlength(c) + track
    else:
        d.text((pad, pad), txt, font=f, fill=255)
    return (np.asarray(im, np.float32) / 255,
            np.asarray(im.filter(ImageFilter.GaussianBlur(10)), np.float32) / 255, pad)


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
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
VIG = (1 - 0.16 * np.clip(r - 0.55, 0, 1) ** 1.6)[..., None].astype(np.float32)


def finish(f, t):
    g = 0.0
    for a, b in TEXT_WINDOWS:
        if a - 0.3 <= t <= b + 0.3:
            g = max(g, min(1, (t - (a - 0.3)) / 0.5, (b + 0.3 - t) / 0.4))
    if g > 0:
        f *= (1 - 0.42 * g * GY)
    for (txt, font, size, tr, x, y, ti, to), (a, shd, pad) in zip(TEXTS, TP):
        if not (ti <= t <= to):
            continue
        u = sm((t - ti) / 0.55)
        o = u * min(1, (to - t) / 0.3)
        y0, x0 = int(y + 26 * (1 - u)) - pad, x - pad
        h_, w_ = a.shape
        reg = f[y0:y0 + h_, x0:x0 + w_]
        hh, ww = reg.shape[:2]
        A = a[:hh, :ww, None] * o
        reg *= (1 - shd[:hh, :ww, None] * o * 0.55)
        reg[:] = reg * (1 - A) + 250 * A
    if t > FADE_OUT[0]:
        f *= max(0.0, 1 - (t - FADE_OUT[0]) / (FADE_OUT[1] - FADE_OUT[0]))
    return np.clip(f, 0, 255).astype(np.uint8)


def frame(n):
    t = (n + 0.5) / FPS
    acc = np.zeros((H, W, 3), np.float32)
    for k in range(SUB):                       # 180-degree shutter
        ts = t + ((k + 0.5) / SUB - 0.5) * 0.5 / FPS
        acc += raw_frame(min(ts, TOTAL - 1e-3))
    return finish(acc / SUB * VIG, t)


if os.environ.get("STILLS"):
    tiles = []
    for i, sh in enumerate(SHOTS):
        for t in (sh[1] + 0.02, (sh[1] + sh[2]) / 2, sh[2] - 0.02):
            f = cv2.resize(shot_frame(i, t), (216, 384))
            cv2.putText(f, f"{i+1} {sh[0]}", (6, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            tiles.append(f)
    per = 15
    rows = [np.hstack(tiles[k:k + per]) for k in range(0, len(tiles), per)]
    rows[-1] = np.hstack([rows[-1], np.zeros((384, 216 * per - rows[-1].shape[1], 3), np.uint8)])
    cv2.imwrite(OUT, np.vstack(rows))
    sys.exit()

N = int(round(TOTAL * FPS))
a0 = int(os.environ.get("FROM", 0)); a1 = int(os.environ.get("TO", N))
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                       "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "17",
                       "-pix_fmt", "yuv420p", OUT], stdin=subprocess.PIPE)
for n in range(a0, a1):
    ff.stdin.write(frame(n).tobytes())
    if n % 100 == 0:
        print(f"frame {n}/{a1}", flush=True)
ff.stdin.close(); ff.wait()
print("done")
