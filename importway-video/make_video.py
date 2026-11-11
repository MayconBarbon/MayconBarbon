"""Animação institucional ImportWay — apenas zoom/pan digital sobre a foto original.
Uso: python3 make_video.py  (gera importway_institucional.mp4)"""
import subprocess, math, wave, os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "parede-importway.webp")
OUT = os.path.join(HERE, "importway_institucional.mp4")
W, H, FPS, DUR = 1920, 1080, 30, 15.0
AR = W / H

img = Image.open(SRC).convert("RGB")
IW, IH = img.size
# super-amostragem (lanczos) para reamostragem final mais limpa
SS = 2
big = img.resize((IW * SS, IH * SS), Image.LANCZOS)

FULL = (IW / 2, IH / 2, IW)  # (centro x, centro y, largura do quadro em px da foto)
# keyframes: (tempo, cx, cy, largura) — coordenadas na foto original 1672x941
KEYS = [
    (0.0,  *FULL),
    (0.5,  *FULL),
    (3.0,  465, 245, 1000),  # zoom-in moderado: área "NOSSAS MARCAS" (todas as marcas no quadro)
    (3.5,  445, 250, 900),   # 1º grupo: Starke / BrinQway / LifeWay
    (5.7,  490, 250, 900),   # deslocamento horizontal discreto
    (6.5,  490, 262, 880),   # 2º grupo: Alumiway / Way Sound / Femax
    (8.7,  445, 262, 860),   # zoom progressivo leve
    (9.5,  470, 272, 880),   # licenciadas + frase (BLACK+DECKER / Real Madrid sempre visíveis)
    (11.8, 470, 276, 860),
    (14.3, *FULL),           # zoom-out revelando toda a parede
    (15.0, *FULL),
]

def ease(u):  # ease-in/ease-out (smootherstep)
    return u * u * u * (u * (u * 6 - 15) + 10)

def cam(t):
    for (t0, x0, y0, w0), (t1, x1, y1, w1) in zip(KEYS, KEYS[1:]):
        if t <= t1:
            u = ease(0 if t1 == t0 else (t - t0) / (t1 - t0))
            w = math.exp(math.log(w0) + (math.log(w1) - math.log(w0)) * u)  # zoom perceptualmente uniforme
            return x0 + (x1 - x0) * u, y0 + (y1 - y0) * u, w
    return FULL

def frame(t):
    cx, cy, w = cam(t)
    w = min(w, IW); h = w / AR
    if h > IH: h = IH; w = h * AR
    x0 = min(max(cx - w / 2, 0), IW - w)
    y0 = min(max(cy - h / 2, 0), IH - h)
    box = tuple(v * SS for v in (x0, y0, x0 + w, y0 + h))
    return big.resize((W, H), Image.BICUBIC, box=box, reducing_gap=None)

# ---------- trilha instrumental sintetizada (moderna, elegante, ritmo crescente) ----------
SR = 48000
def make_music(path):
    n = int(SR * DUR); t = np.arange(n) / SR
    out = np.zeros(n)
    bpm = 112; beat = 60 / bpm
    chords = [[57, 60, 64, 69], [53, 57, 60, 65], [48, 55, 60, 64], [55, 59, 62, 67]]  # Am F C G
    f = lambda m: 440 * 2 ** ((m - 69) / 12)
    bar = beat * 4
    intensity = np.clip(t / 12.0, 0, 1) ** 1.3
    for i in range(int(DUR / bar) + 1):
        ch = chords[i % 4]; s = int(i * bar * SR); e = min(n, int((i + 1) * bar * SR + 0.3 * SR))
        if s >= n: break
        tt = t[s:e] - t[s]
        env = np.minimum(1, tt / 0.6) * np.exp(-tt * 0.35)
        for m in ch:  # pad suave (detune)
            for d in (-0.08, 0.08):
                out[s:e] += 0.035 * env * np.sin(2 * np.pi * f(m + d) * tt + 0.4 * np.sin(2 * np.pi * 0.3 * tt))
        bass = f(ch[0] - 12)
        out[s:e] += 0.10 * env * np.sin(2 * np.pi * bass * tt)
    # arpejo pluck (entra aos 3s)
    step = beat / 2
    for k in range(int(DUR / step)):
        st = k * step
        if st < 3.0: continue
        ch = chords[int(st / bar) % 4]; m = ch[[0, 2, 1, 3, 2, 3, 1, 2][k % 8]] + 12
        s = int(st * SR); e = min(n, s + int(0.5 * SR)); tt = t[s:e] - st
        out[s:e] += 0.06 * (0.5 + 0.5 * intensity[s]) * np.exp(-tt * 9) * (np.sin(2*np.pi*f(m)*tt) + 0.3*np.sin(4*np.pi*f(m)*tt))
    # kick + hats (entram aos 6s / 9s)
    rng = np.random.default_rng(7)
    for k in range(int(DUR / beat)):
        st = k * beat
        if st >= 6.0 and st < 14.0:
            s = int(st * SR); e = min(n, s + int(0.35 * SR)); tt = t[s:e] - st
            out[s:e] += 0.32 * intensity[s] * np.exp(-tt * 14) * np.sin(2 * np.pi * (48 + 90 * np.exp(-tt * 35)) * tt)
        for off in (0.5,):
            hs = st + off * beat
            if 9.0 <= hs < 14.0:
                s = int(hs * SR); e = min(n, s + int(0.06 * SR)); tt = t[s:e] - hs
                noise = rng.standard_normal(e - s); noise = np.diff(noise, prepend=0)
                out[s:e] += 0.05 * np.exp(-tt * 70) * noise
    # acorde final sustentado
    s = int(13.0 * SR); tt = t[s:] - 13.0
    for m in [57, 64, 69, 72, 76]:
        out[s:] += 0.03 * np.minimum(1, tt / 0.4) * np.sin(2 * np.pi * f(m) * tt)
    fade = np.ones(n); fi = int(0.4 * SR); fo = int(1.8 * SR)
    fade[:fi] = np.linspace(0, 1, fi); fade[-fo:] = np.linspace(1, 0, fo) ** 2
    out *= fade
    out = np.tanh(out * 1.4); out /= np.max(np.abs(out)) / 0.89
    st = np.stack([out, np.roll(out, int(0.012 * SR)) * 0.97], 1)  # leve largura estéreo
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype("<i2").tobytes())

wav = os.path.join(HERE, "_trilha.wav")
make_music(wav)

cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
       "-r", str(FPS), "-i", "-", "-i", wav,
       "-c:v", "libx264", "-preset", "slow", "-b:v", "20M", "-maxrate", "30M", "-bufsize", "40M",
       "-profile:v", "high", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
       "-c:a", "aac", "-b:a", "320k", "-shortest", "-movflags", "+faststart", OUT]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
for i in range(int(DUR * FPS)):
    p.stdin.write(frame(i / FPS).tobytes())
p.stdin.close(); p.wait()
os.remove(wav)
print("ok", OUT)
