"""Trilha instrumental sintetizada: piano suave + cordas/pad + baixo, Ré maior, 80 BPM, 60 s."""
import numpy as np, soundfile as sf
from scipy.signal import fftconvolve, butter, sosfilt

SR = 48000
DUR = 60.5
BAR = 3.0           # 80 BPM, 4/4
rng = np.random.default_rng(7)
N = int(SR * DUR)
L = np.zeros(N); R = np.zeros(N)

def midi(n): return 440.0 * 2 ** ((n - 69) / 12)

# Progressão (repetida): Dmaj9 | Bm9 | Gmaj9 | Asus4 -> A
D, B, G, A = 50, 47, 43, 45
chords = [
    dict(root=D, pad=[62, 66, 69, 73, 76], arp=[62, 66, 69, 73, 76, 73, 69, 66]),
    dict(root=B, pad=[59, 62, 66, 69, 73], arp=[59, 62, 66, 69, 73, 69, 66, 62]),
    dict(root=G, pad=[59, 62, 66, 69, 71], arp=[55, 59, 62, 66, 69, 66, 62, 59]),
    dict(root=A, pad=[57, 61, 64, 69, 71], arp=[57, 62, 64, 69, 71, 69, 64, 61]),
]
NBARS = 20

def add(sig, start, pan=0.0, gain=1.0):
    i = int(start * SR)
    if i < 0:
        sig = sig[-i:]; i = 0
    if i >= N: return
    s = sig[: N - i] * gain
    l = np.cos((pan + 1) * np.pi / 4); r = np.sin((pan + 1) * np.pi / 4)
    L[i:i + len(s)] += s * l; R[i:i + len(s)] += s * r

def piano(freq, dur, vel):
    t = np.arange(int(SR * dur)) / SR
    out = np.zeros_like(t)
    for k in range(1, 9):
        f = freq * k * np.sqrt(1 + 0.0004 * k * k)
        if f > 9000: break
        amp = vel / k ** 1.6
        dec = 1.6 + 1.1 * k
        out += amp * np.sin(2 * np.pi * f * t + rng.uniform(0, 6.28)) * np.exp(-dec * t)
    att = np.minimum(1, t / 0.006)
    rel = np.minimum(1, (dur - t) / 0.25).clip(0, 1)
    # leve "feltro": suaviza o ataque
    return out * att * rel

def pad(freqs, dur, gain):
    t = np.arange(int(SR * dur)) / SR
    out = np.zeros_like(t)
    for f in freqs:
        for det in (-0.12, 0.0, 0.11):
            ff = f * 2 ** (det / 12)
            vib = 1 + 0.0015 * np.sin(2 * np.pi * 4.8 * t + rng.uniform(0, 6))
            ph = 2 * np.pi * np.cumsum(ff * vib) / SR
            out += (np.sin(ph) + 0.28 * np.sin(2 * ph) + 0.10 * np.sin(3 * ph)) / 3
    env = np.minimum(1, t / 1.1) * np.minimum(1, (dur - t) / 1.2).clip(0, 1)
    return out * env * gain / len(freqs)

def bass(freq, dur, gain):
    t = np.arange(int(SR * dur)) / SR
    s = np.sin(2 * np.pi * freq * t) + 0.25 * np.sin(4 * np.pi * freq * t)
    env = np.minimum(1, t / 0.04) * np.exp(-0.45 * t) * np.minimum(1, (dur - t) / 0.3).clip(0, 1)
    return s * env * gain

def intensity(bar):
    # arco: entrada suave, crescimento, "brinde" (~40-51 s), resolução
    return {0: .55, 1: .6, 2: .65, 3: .7, 4: .75, 5: .78, 6: .8, 7: .82, 8: .84, 9: .85,
            10: .86, 11: .88, 12: .9, 13: .97, 14: 1.0, 15: 1.0, 16: .95, 17: .82, 18: .7, 19: .6}[bar]

for b in range(NBARS):
    c = chords[b % 4]
    t0 = b * BAR
    I = intensity(b)
    last = b == NBARS - 1
    if last:
        c = chords[0]
    # pad / cordas
    add(pad([midi(n) for n in c["pad"]], BAR + 1.6 + (2.5 if last else 0), 0.16 * I), t0 - 0.3, pan=-0.15)
    add(pad([midi(n - 12) for n in c["pad"][:3]], BAR + 1.6 + (2.5 if last else 0), 0.10 * I), t0 - 0.3, pan=0.2)
    # baixo a partir do compasso 4
    if b >= 4:
        add(bass(midi(c["root"] - 12 if c["root"] > 45 else c["root"]), BAR, 0.20 * I), t0, pan=0)
    # piano
    step = BAR / 8
    if b < 3 or last:
        pattern = [0, 2, 4, 6]  # semínimas
    elif b < 6 or b >= 18:
        pattern = [0, 2, 3, 4, 6]
    else:
        pattern = list(range(8))
    for j in pattern:
        n = c["arp"][j]
        vel = 0.10 * I * (1.15 if j == 0 else 1.0) * rng.uniform(0.85, 1.05)
        tt = t0 + j * step + rng.normal(0, 0.006)
        add(piano(midi(n), 2.2, vel), tt, pan=rng.uniform(-0.35, 0.35))
        if 13 <= b <= 16 and j in (0, 4):  # oitava no "brinde"
            add(piano(midi(n + 12), 1.8, vel * 0.45), tt + 0.01, pan=0.3)
    if last:
        add(piano(midi(74), 4.0, 0.07), t0 + BAR * 0.75, pan=0.2)

# Reverb (IR sintética estéreo)
irlen = int(SR * 2.6)
tt = np.arange(irlen) / SR
def ir():
    n = rng.normal(0, 1, irlen) * np.exp(-tt / 0.62)
    sos = butter(2, 5500, 'low', fs=SR, output='sos')
    n = sosfilt(sos, n); n[: int(0.012 * SR)] = 0
    return n / np.sqrt(np.sum(n ** 2))
wetL = fftconvolve(L, ir())[:N]; wetR = fftconvolve(R, ir())[:N]
outL = 0.72 * L + 0.42 * wetL; outR = 0.72 * R + 0.42 * wetR
# corte de graves/agudos extremos
sos = butter(2, [45, 12000], 'band', fs=SR, output='sos')
outL = sosfilt(sos, outL); outR = sosfilt(sos, outR)
# fade-in / fade-out finais
t = np.arange(N) / SR
fade = np.minimum(1, t / 1.5) * np.clip((DUR - t) / 4.0, 0, 1) ** 1.5
outL *= fade; outR *= fade
st = np.stack([outL, outR], 1)
st /= np.max(np.abs(st)) / 0.89
sf.write(__import__('sys').argv[1], st, SR, subtype='PCM_24')
print("ok", st.shape[0] / SR)
