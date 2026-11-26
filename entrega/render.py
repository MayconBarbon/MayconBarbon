import sys, subprocess, numpy as np, cv2

S = sys.argv[1]
OUT = sys.argv[2]
FPS = 30
W, H = 1080, 1920
AR = W / H

# (file, start, end, cx0, cx1, cy0, cy1, z0, z1, label)
# cx/cy = normalized window centre in source; z = zoom (1 = full source height)
SHOTS = [
    ("0483", 0.0, 3.0, .58, .56, .52, .46, 1.00, 1.18, "Fachada/jardim de entrada - push-in pelo caminho"),
    ("0489", 3.0, 5.0, .26, .66, .56, .56, 1.06, 1.06, "Pátio inferior - travelling lateral E->D"),
    ("0742", 5.0, 8.0, .42, .36, .52, .48, 1.00, 1.26, "Hall de entrada - dolly-in até a porta"),
    ("0501", 8.0, 10.0, .68, .22, .55, .55, 1.06, 1.06, "Recepção - travelling lateral D->E"),
    ("0492", 10.0, 12.0, .54, .79, .46, .46, 1.00, 1.04, "Painel/logo - travelling lateral sobre o logo"),
    ("0543", 12.0, 13.5, .55, .57, .56, .54, 1.00, 1.20, "Corredor - dolly-in"),
    ("0507", 13.5, 15.5, .40, .68, .56, .56, 1.06, 1.06, "Sala de espera - travelling lateral"),
    ("0555", 15.5, 18.0, .46, .46, .36, .52, 1.22, 1.02, "Sala de reunião - tilt down + afastamento"),
    ("0564", 18.0, 19.5, .47, .47, .62, .62, 1.10, 1.30, "Detalhe orquídea - aproximação"),
    ("0549", 19.5, 21.5, .28, .64, .60, .60, 1.06, 1.06, "Sala de atendimento - travelling lateral"),
    ("0526", 21.5, 23.0, .46, .54, .55, .53, 1.00, 1.16, "Sala pedagógica - push-in"),
    ("0699", 23.0, 24.0, .45, .47, .56, .54, 1.12, 1.26, "Detalhe livros - push-in rápido"),
    ("0585", 24.0, 26.5, .62, .50, .68, .55, 1.30, 1.00, "Sala sensorial - pull-out revelando"),
    ("0603", 26.5, 28.5, .50, .50, .50, .50, 1.00, 1.24, "Ginásio - dolly-in no eixo"),
    ("0606", 28.5, 30.0, .28, .60, .52, .52, 1.06, 1.06, "Sala psicomotora - travelling lateral"),
    ("0702", 30.0, 31.5, .44, .44, .60, .40, 1.25, 1.25, "Escada de cordas - tilt up"),
    ("0681", 31.5, 33.0, .30, .52, .56, .56, 1.06, 1.06, "Quarto de descanso - travelling lateral"),
    ("0621", 33.0, 34.0, .34, .24, .52, .50, 1.00, 1.20, "Ginásio -> abertura para o jardim - push-in"),
    ("0642", 34.0, 36.0, .50, .50, .56, .54, 1.00, 1.16, "Jardim sensorial - dolly-in"),
    ("0711", 36.0, 38.5, .26, .58, .60, .60, 1.02, 1.02, "Piscina - travelling lateral contemplativo"),
    ("0648", 38.5, 42.5, .38, .41, .50, .50, 1.26, 1.00, "Jardim e casa - pull-out final"),
]
RADIAL = [8.0, 24.0, 34.0]   # zoom-radial transitions (block changes)
XFADE = {19: 0.5}            # dissolve into shot index 20 (pool -> final)
FADE_OUT = (41.4, 42.5)
TOTAL = SHOTS[-1][2]


def grade(img):
    f = img.astype(np.float32) / 255.0
    # partial gray-world white balance (harmonise, keep real look)
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


src = {}
for sh in SHOTS:
    k = sh[0]
    if k not in src:
        im = cv2.imread(f"{S}/img/IMG_{k}.jpg")
        src[k] = grade(im)

yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
VIG = (1 - 0.16 * np.clip(r - 0.55, 0, 1) ** 1.6)[..., None].astype(np.float32)


def shot_frame(i, t, extra_zoom=1.0):
    k, a, b, cx0, cx1, cy0, cy1, z0, z1, _ = SHOTS[i]
    img = src[k]
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
    if t > FADE_OUT[0]:
        f *= max(0.0, 1 - (t - FADE_OUT[0]) / (FADE_OUT[1] - FADE_OUT[0]))
    ff.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes())
    if n % 150 == 0:
        print(f"frame {n}/{N}", flush=True)
ff.stdin.close()
ff.wait()
print("done")
