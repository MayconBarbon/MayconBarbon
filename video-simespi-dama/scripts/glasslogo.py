"""Troca a logo Dama impressa nas taças pela logo colorida SIMESPI 35 anos, quadro a quadro.
1) detecta o 'D' vermelho cercado de cerveja em cada quadro; 2) liga em trilhas e suaviza no tempo;
3) apaga a logo antiga (preenchimento suave com cor da cerveja); 4) aplica a nova com curvatura do copo,
   luz do líquido por trás e brilhos do vidro por cima.
Uso: glasslogo.py entrada.MOV saida.mp4 [inicio] [duracao]   |   --test entrada.MOV t saida.png"""
import sys, os, subprocess, math
import numpy as np, cv2
S = os.path.dirname(os.path.abspath(__file__))
TM = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,"
      "zscale=t=bt709:m=bt709:r=tv,format=yuv420p")
W, H = 1080, 1920
LOGO = cv2.imread(f"{S}/up/logo_p-1.png", cv2.IMREAD_UNCHANGED)
ys, xs = np.where(LOGO[:, :, 3] > 10); LOGO = LOGO[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
SIM = cv2.imread(f"{S}/brand/simespi_small_crop.png", cv2.IMREAD_UNCHANGED)
ys, xs = np.where(SIM[:, :, 3] > 10); SIM = SIM[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

def hsvm(fr):
    hsv = cv2.cvtColor(fr, cv2.COLOR_BGR2HSV); h, s, v = cv2.split(hsv)
    beer = ((h >= 12) & (h <= 36) & (s > 90) & (v > 120))
    red = (((h < 10) | (h > 170)) & (s > 100) & (v > 60))
    return beer, red, hsv

def skin_mask(hsv):
    h, s, v = cv2.split(hsv)
    sk = (((h < 15) | (h > 168)) & (s > 55) & (s < 200) & (v < 200)).astype(np.uint8)
    ink = ((((h < 10) | (h > 170)) & (s >= 200) & (v > 60))).astype(np.uint8)
    ink = cv2.morphologyEx(ink, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    sk[cv2.dilate(ink, np.ones((5, 5), np.uint8)) > 0] = 0
    sk = cv2.morphologyEx(sk, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(sk)
    big = np.zeros_like(sk)
    for k in range(1, n):
        if st[k, 4] > 12000: big[lab == k] = 1
    big = cv2.morphologyEx(big, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    return big

def detect(fr):
    beer, red, hsv = hsvm(fr)
    skin = skin_mask(hsv)
    r8 = cv2.morphologyEx(red.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    n, lab, st, cen = cv2.connectedComponentsWithStats(r8)
    out = []
    for k in range(1, n):
        x, y, w, h, a = st[k]
        if a < 250 or w < 26 or h < 26 or w > 260 or h > 280 or w > 1.8 * h or h > 1.8 * w: continue
        m = (lab == k).astype(np.uint8)
        if hsv[:, :, 1][m > 0].mean() < 180 or skin[m > 0].mean() > 0.3: continue   # pele/mão não é o D impresso
        pad = int(max(w, h) * 0.35)
        ring = cv2.dilate(m, np.ones((2 * pad + 1, 2 * pad + 1), np.uint8)) - cv2.dilate(m, np.ones((9, 9), np.uint8))
        ring[:y, :] = 0  # só laterais e baixo (em cima pode ter espuma)
        frac = (beer & (ring > 0)).sum() / max(1, (ring > 0).sum())
        if frac < 0.25: continue
        out.append([x + w / 2, y + h / 2, float(w), float(h)])
    if out:
        mx = max(d[2] * d[3] for d in out); out = [d for d in out if d[2] * d[3] >= 0.25 * mx]
    return out

def tracks(dets, maxd=120):
    """liga detecções em trilhas; devolve lista de arrays (nfr, 4) com NaN quando ausente"""
    nf = len(dets); trs = []
    for f, ds in enumerate(dets):
        used = set()
        for t in trs:
            last = next((t[j] for j in range(f - 1, max(-1, f - 6), -1) if t[j] is not None), None)
            if last is None: continue
            best, bd = None, maxd
            for i, d in enumerate(ds):
                if i in used: continue
                dd = math.hypot(d[0] - last[0], d[1] - last[1])
                if dd < bd: best, bd = i, dd
            if best is not None: t[f] = ds[best]; used.add(best)
        for i, d in enumerate(ds):
            if i not in used:
                t = [None] * nf; t[f] = d; trs.append(t)
    res = []
    for t in trs:
        if sum(x is not None for x in t) < 8: continue
        a = np.array([x if x is not None else [np.nan] * 4 for x in t], float)
        idx = np.arange(nf); ok = ~np.isnan(a[:, 0])
        first, last = idx[ok][0], idx[ok][-1]
        for c in range(4): a[first:last + 1, c] = np.interp(idx[first:last + 1], idx[ok], a[ok, c])
        # suavização: posição leve (segue o movimento), tamanho forte
        b = a.copy()
        for c, s in ((0, 1.0), (1, 1.0), (2, 2.5), (3, 2.5)):
            seg = a[first:last + 1, c]; k = int(3 * s) * 2 + 1
            g = np.exp(-0.5 * (np.arange(k) - k // 2) ** 2 / s ** 2); g /= g.sum()
            p = np.pad(seg, k // 2, mode="edge"); b[first:last + 1, c] = np.convolve(p, g, "valid")
        res.append(b)
    return res

def angle_of(fr, cx, cy, w, h):
    """inclinação da logo: orientação (PCA) da palavra escura DAMA logo abaixo do D"""
    beer, _, hsv = hsvm(fr)
    x0, x1 = int(cx - w * 0.75), int(cx + w * 0.75); y0, y1 = int(cy + h * 0.42), int(cy + h * 1.0)
    x0, y0 = max(0, x0), max(0, y0); x1, y1 = min(W, x1), min(H, y1)
    if x1 - x0 < 20 or y1 - y0 < 10: return np.nan
    near = cv2.dilate(beer.astype(np.uint8), np.ones((15, 15), np.uint8))[y0:y1, x0:x1] > 0
    d = (hsv[y0:y1, x0:x1, 2] < 120) & near
    if d.sum() < 150: return np.nan
    yy, xx = np.nonzero(d); c = np.cov(np.vstack([xx, yy]))
    ev, evec = np.linalg.eigh(c); v = evec[:, 1]
    if ev[1] < 3 * ev[0]: return np.nan
    ang = math.degrees(math.atan2(v[1], v[0]))
    if ang > 90: ang -= 180
    if ang < -90: ang += 180
    return float(np.clip(-ang, -20, 20))

def fill_smooth(img, mask, sig):
    f = img.astype(np.float32); w = (1 - mask).astype(np.float32)
    num = cv2.GaussianBlur(f * w[..., None], (0, 0), sig); den = cv2.GaussianBlur(w, (0, 0), sig)[..., None]
    return num / np.maximum(den, 1e-3)

def prep_logo(lw, src_logo):
    lh = int(lw * src_logo.shape[0] / src_logo.shape[1])
    lg = cv2.resize(src_logo, (lw, lh), interpolation=cv2.INTER_AREA).astype(np.float32)
    u = np.linspace(-1, 1, lw)
    src = (np.arcsin(np.clip(u * 0.92, -1, 1)) / math.asin(0.92)) * 0.5 + 0.5   # cilindro
    mapx = np.tile((src * (lw - 1)).astype(np.float32), (lh, 1))
    mapy = np.tile(np.arange(lh, dtype=np.float32)[:, None], (1, lw)) + ((u ** 2) * lh * 0.05)[None, :].astype(np.float32)
    lg = cv2.remap(lg, mapx, mapy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    lg[:, :, :3] *= (0.80 + 0.20 * np.cos(u * math.pi / 2))[None, :, None]
    return lg

def place(fr, cx, cy, w, h, ang, logo=None):
    logo = LOGO if logo is None else logo
    beer, red, hsv = hsvm(fr)
    skin = skin_mask(hsv)
    # caixa da logo antiga (D + DAMA): rotacionada pela inclinação
    s = max(w, h)
    box = ((cx + math.sin(math.radians(ang)) * s * 0.30, cy + math.cos(math.radians(ang)) * s * 0.30), (s * 1.45, s * 1.75), -ang)
    reg = np.zeros((H, W), np.uint8); cv2.fillPoly(reg, [cv2.boxPoints(box).astype(np.int32)], 1)
    old = reg & (~beer).astype(np.uint8)
    old = cv2.morphologyEx(old, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    old = cv2.dilate(old, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
    # não apagar brilho forte do vidro nem a espuma
    spec = (hsv[:, :, 2] > 240) & (hsv[:, :, 1] < 40)
    old[spec] = 0
    old[skin > 0] = 0
    sm = fill_smooth(fr, old, max(6, s * 0.10))
    rng = np.random.default_rng(int(cx * 7 + cy))
    grain = rng.normal(0, 2.0, (H, W, 1)).astype(np.float32)
    mb = cv2.GaussianBlur(old.astype(np.float32), (0, 0), 2.5)[..., None]
    clean = fr.astype(np.float32) * (1 - mb) + (sm + grain) * mb
    # nova logo
    lw = int(s * (1.26 if logo is LOGO else 1.36)); lg = prep_logo(lw, logo); lh = lg.shape[0]
    pc = (cx + math.sin(math.radians(ang)) * s * 0.36, cy + math.cos(math.radians(ang)) * s * 0.36)
    M = cv2.getRotationMatrix2D((lw / 2, lh / 2), ang, 1.0); M[0, 2] += pc[0] - lw / 2; M[1, 2] += pc[1] - lh / 2
    wl = cv2.warpAffine(lg, M, (W, H), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
    wl = cv2.GaussianBlur(wl, (0, 0), 1.1)
    a = wl[:, :, 3] / 255.0 * 0.93
    # recorta no corpo do copo: cerveja ao redor fechada localmente
    gx0, gx1 = int(max(0, cx - s * 1.6)), int(min(W, cx + s * 1.6)); gy0, gy1 = int(max(0, cy - s * 0.9)), int(min(H, cy + s * 1.9))
    lb = beer[gy0:gy1, gx0:gx1].astype(np.uint8) | old[gy0:gy1, gx0:gx1]
    lb = cv2.morphologyEx(lb, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31)))
    n_, lab_, st_, _ = cv2.connectedComponentsWithStats(lb)
    body = np.zeros((H, W), np.float32)
    if n_ > 1:
        k_ = lab_[int(min(gy1 - gy0 - 1, cy - gy0)), int(min(gx1 - gx0 - 1, cx - gx0))]
        if k_ == 0: k_ = 1 + np.argmax(st_[1:, 4])
        bm = (lab_ == k_).astype(np.uint8)
        bm = cv2.erode(bm, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(s * 0.05) | 1, int(s * 0.05) | 1)))
        body[gy0:gy1, gx0:gx1] = cv2.GaussianBlur(bm.astype(np.float32), (0, 0), s * 0.05)
    a = a * body * (1 - cv2.GaussianBlur(skin.astype(np.float32), (0, 0), 1.5))
    lum = cv2.cvtColor(np.clip(sm, 0, 255).astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0
    lit = wl[:, :, :3] * (0.80 + 0.40 * lum[..., None])
    out = clean * (1 - a[..., None]) + lit * a[..., None]
    # brilhos especulares originais por cima da impressão
    hl = np.clip((hsv[:, :, 2].astype(np.float32) - 225) / 25, 0, 1) * np.clip((60 - hsv[:, :, 1].astype(np.float32)) / 40, 0, 1)
    hl = cv2.GaussianBlur(hl, (0, 0), 1.0)[..., None] * a[..., None]
    out = out * (1 - hl) + fr.astype(np.float32) * hl
    return out.clip(0, 255).astype(np.uint8)

def read_frames(path, t0, dur):
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t0}", "-t", f"{dur}", "-i", path, "-vf", TM + ",format=bgr24",
           "-f", "rawvideo", "-pix_fmt", "bgr24", "-"]
    raw = subprocess.run(cmd, stdout=subprocess.PIPE, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)

def run(frs):
    dets = [detect(f) for f in frs]
    trs = tracks(dets)
    outs = []
    angs = {}
    for ti, t in enumerate(trs):
        a = np.array([angle_of(frs[i], *t[i]) if not np.isnan(t[i, 0]) else np.nan for i in range(len(frs))])
        ok = ~np.isnan(a)
        if ok.any():
            k = 7; g = np.ones(k) / k; ai = a.copy(); ai[~ok] = np.interp(np.nonzero(~ok)[0], np.nonzero(ok)[0], a[ok])
            ai = np.convolve(np.pad(ai, k // 2, mode="edge"), g, "valid"); ai[~ok] = np.nan
        else: ai = a
        angs[ti] = np.nan_to_num(ai, nan=0.0) * 0.75
    # kit real: um copo SIMESPI e um copo 35 anos -> taça da esquerda SIMESPI, da direita 35 anos
    means = [np.nanmean(t[:, 0]) for t in trs]
    order = sorted(range(len(trs)), key=lambda k: -np.sum(~np.isnan(trs[k][:, 0])))[:2]
    mid = np.mean([means[k] for k in order]) if len(order) == 2 else W / 2
    which = {ti: (SIM if means[ti] < mid else LOGO) for ti in range(len(trs))}
    if os.environ.get("ONLY35"): which = {ti: LOGO for ti in range(len(trs))}
    for i, f in enumerate(frs):
        o = f.copy()
        for ti, t in enumerate(trs):
            if np.isnan(t[i, 0]): continue
            o = place(o, *t[i], angs[ti][i], which[ti])
        outs.append(o)
    return outs, trs

if __name__ == "__main__":
    if sys.argv[1] == "--test":
        t = float(sys.argv[3]); frs = read_frames(sys.argv[2], max(0, t - 0.3), 0.6)
        outs, trs = run(list(frs)); i = len(frs) // 2
        print("trilhas", len(trs), [tr[i].round(1).tolist() for tr in trs])
        cv2.imwrite(sys.argv[4], np.hstack([frs[i], outs[i]])); sys.exit()
    src, dst = sys.argv[1], sys.argv[2]
    t0 = float(sys.argv[3]) if len(sys.argv) > 3 else 0; dur = float(sys.argv[4]) if len(sys.argv) > 4 else 99
    frs = read_frames(src, t0, dur); outs, trs = run(list(frs))
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                            "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709",
                            "-colorspace", "bt709", dst], stdin=subprocess.PIPE)
    for o in outs: enc.stdin.write(o.tobytes())
    enc.stdin.close(); enc.wait(); print("ok", dst, len(frs), "trilhas", len(trs))
