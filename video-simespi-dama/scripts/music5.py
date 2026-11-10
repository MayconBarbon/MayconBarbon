"""Trilha corporativa vibrante, 120 BPM, Ré maior (I–V–vi–IV), seções sincronizadas com o vídeo v3."""
import sys, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000
BPM = 120; BEAT = 60 / BPM; BAR = 4 * BEAT; S16 = BEAT / 4
DUR = 90.5
N = int(SR * DUR)
rng = np.random.default_rng(11)
L = np.zeros(N); R = np.zeros(N)
bus = {k: [np.zeros(N), np.zeros(N)] for k in ("drums", "bass", "music", "fx")}

# Mapa de seções (s): (início, fim, nome)
SECT = [(0, 4.5, "full"), (4.5, 5.0, "fill"), (5.0, 20.5, "verse"), (20.5, 21.0, "fill"),
        (21.0, 23.0, "full"), (23.0, 33.0, "verse"), (33.0, 58.5, "verse2"), (58.5, 62.5, "build"),
        (62.5, 72.5, "chorus"), (72.5, 75.5, "big"), (75.5, 83.0, "chorus"), (83.0, 90.5, "outro")]
IMPACTS = [0.0, 5.0, 21.0, 62.5, 72.5, 83.0]

def sect(t):
    for a, b, n in SECT:
        if a <= t < b: return n
    return "outro"

def midi(n): return 440.0 * 2 ** ((n - 69) / 12)
def put(name, sig, t, pan=0.0, g=1.0):
    i = int(round(t * SR))
    if i < 0: sig = sig[-i:]; i = 0
    if i >= N or len(sig) == 0: return
    s = sig[: N - i] * g
    l = np.cos((pan + 1) * np.pi / 4); r = np.sin((pan + 1) * np.pi / 4)
    bus[name][0][i:i + len(s)] += s * l; bus[name][1][i:i + len(s)] += s * r

def env(n, a, d):  # attack/decay exp
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)

def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, a, b, o=2): return sosfilt(butter(o, [a, b], 'band', fs=SR, output='sos'), x)

def saw(freq, dur, detune=(0,), cutoff=3000):
    t = np.arange(int(dur * SR)) / SR
    out = np.zeros_like(t)
    for d in detune:
        f = freq * 2 ** (d / 1200)
        ph = (t * f + rng.uniform()) % 1.0
        out += 2 * ph - 1
    return lp(out / len(detune), cutoff)

# --- instrumentos
def kick():
    n = int(0.45 * SR); t = np.arange(n) / SR
    f = 45 + 95 * np.exp(-t / 0.035)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t / 0.18) + 0.25 * lp(rng.normal(0, 1, n), 4000) * np.exp(-t / 0.006)
def clap():
    n = int(0.35 * SR); t = np.arange(n) / SR
    nz = bp(rng.normal(0, 1, n), 900, 5000)
    e = np.zeros(n)
    for k, off in enumerate((0, 0.011, 0.022)):
        i = int(off * SR); e[i:] += np.exp(-(t[: n - i]) / (0.012 if k < 2 else 0.13))
    return nz * e * 0.6
def snare():
    n = int(0.25 * SR); t = np.arange(n) / SR
    return (0.6 * bp(rng.normal(0, 1, n), 1500, 7000) * np.exp(-t / 0.07) +
            0.5 * np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.05))
def hat(open_=False):
    n = int((0.25 if open_ else 0.05) * SR); t = np.arange(n) / SR
    return hp(rng.normal(0, 1, n), 7500, 4) * np.exp(-t / (0.08 if open_ else 0.012)) * 0.35
def crash():
    n = int(2.8 * SR); t = np.arange(n) / SR
    return hp(rng.normal(0, 1, n), 4500, 2) * np.exp(-t / 0.9) * 0.35
def boom():
    n = int(2.0 * SR); t = np.arange(n) / SR
    f = 32 + 60 * np.exp(-t / 0.08)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.7) * 0.9
def riser(dur):
    n = int(dur * SR); t = np.arange(n) / SR
    x = rng.normal(0, 1, n)
    # varredura de filtro por blocos
    out = np.zeros(n); blk = 2048
    for i in range(0, n, blk):
        fc = 300 + 9000 * (i / n) ** 2
        out[i:i + blk] = bp(x[i:i + blk + 0], max(200, fc * 0.6), min(20000, fc * 1.4), 1)[: len(out[i:i + blk])]
    tone = np.sin(2 * np.pi * np.cumsum(220 * 2 ** (2 * t / dur)) / SR) * 0.15
    return (out * 0.5 + tone) * (t / dur) ** 1.5
def pluck(freq, dur=0.35, vel=1.0):
    s = saw(freq, dur, (-6, 6), cutoff=min(9000, freq * 8))
    return s * env(len(s), 0.002, 0.11) * vel
def bass_note(freq, dur):
    s = saw(freq, dur, (0,), cutoff=420) + 0.6 * np.sin(2 * np.pi * freq * np.arange(int(dur * SR)) / SR)
    return s * env(len(s), 0.004, dur * 0.9) * np.minimum(1, (dur - np.arange(len(s)) / SR) / 0.02).clip(0, 1)
def pad(freqs, dur, cutoff=2200):
    out = sum(saw(f, dur, (-12, 0, 11), cutoff) for f in freqs) / len(freqs)
    t = np.arange(len(out)) / SR
    return out * np.minimum(1, t / 0.25) * np.minimum(1, (dur - t) / 0.4).clip(0, 1)
def piano(freq, dur, vel):
    t = np.arange(int(SR * dur)) / SR; out = np.zeros_like(t)
    for k in range(1, 8):
        out += vel / k ** 1.5 * np.sin(2 * np.pi * freq * k * t) * np.exp(-(1.4 + 1.2 * k) * t)
    return out * np.minimum(1, t / 0.004)
def bell(freq, dur, vel):
    t = np.arange(int(SR * dur)) / SR
    return vel * (np.sin(2 * np.pi * freq * t) + 0.4 * np.sin(2 * np.pi * freq * 2.76 * t) * np.exp(-3 * t)) * np.exp(-2.2 * t)

# Progressão: D | A | Bm | G   (raízes MIDI) e acordes
PROG = [(38, [62, 66, 69, 74]), (45, [61, 64, 69, 73]), (47, [62, 66, 71, 74]), (43, [62, 67, 71, 74])]
ARP = [[74, 69, 66, 69, 78, 74, 69, 74], [73, 69, 64, 69, 76, 73, 69, 73],
       [74, 71, 66, 71, 78, 74, 71, 74], [74, 71, 67, 71, 79, 74, 71, 74]]
LEAD = [78, 76, 74, 76, 81, 78, 76, 74]  # motivo para os momentos "big"

nbars = int(DUR / BAR) + 1
for bi in range(nbars):
    t0 = bi * BAR
    root, ch = PROG[bi % 4]
    s = sect(t0 + 0.01)
    if s == "outro" and t0 >= 85: root, ch = PROG[0]
    full = s in ("full", "big", "chorus")
    # PAD / acordes
    if s != "build":
        g = {"full": .22, "big": .26, "chorus": .2, "verse": .12, "verse2": .14, "fill": .18, "outro": .2}[s]
        put("music", pad([midi(n) for n in ch], BAR + 0.3, 2600 if full else 1600), t0, -0.1, g)
    # BAIXO em colcheias
    if s in ("full", "big", "chorus", "verse", "verse2"):
        for k in range(8):
            if s.startswith("verse") and k % 2: continue
            put("bass", bass_note(midi(root + (12 if (k == 6 and full) else 0)), BEAT / 2 * 0.95), t0 + k * BEAT / 2, 0, .45)
    # PLUCK arpejo em semicolcheias (verso: colcheias)
    if s != "build" and not (s == "outro" and t0 > 87):
        step = S16 if s in ("full", "big", "chorus", "verse2") else BEAT / 2
        cnt = int(BAR / step)
        for k in range(cnt):
            n = ARP[bi % 4][k % 8]
            put("music", pluck(midi(n), 0.3, 0.5 if k % 4 == 0 else 0.33), t0 + k * step, 0.35 if k % 2 else -0.35, .55)
    # PIANO nos tempos 1 e 3 (calor)
    if s in ("verse", "verse2", "outro", "chorus"):
        for k in (0, 2):
            for n in ch[:3]:
                put("music", piano(midi(n - 12), 1.2, .09), t0 + k * BEAT, 0.1)
    # LEAD nos momentos altos
    if s in ("full", "big"):
        for k, n in enumerate(LEAD):
            put("music", bell(midi(n), 0.9, .16), t0 + k * BEAT / 2, 0.2)
    # BATERIA
    for b in range(4):
        tb = t0 + b * BEAT; sb = sect(tb + 0.01)
        if sb in ("full", "big", "chorus", "verse", "verse2"):
            put("drums", kick(), tb, 0, .85 if sb in ("full", "big", "chorus") else .6)
        if sb in ("full", "big", "chorus", "verse2") and b in (1, 3):
            put("drums", clap(), tb, 0, .7)
        if sb in ("full", "big", "chorus", "verse", "verse2"):
            for h in range(4 if sb != "verse" else 2):
                th = tb + h * (S16 if sb != "verse" else BEAT / 2)
                put("drums", hat(open_=(h == 2 and sb in ("full", "big"))), th, 0.3, .8 if h % 2 == 0 else .5)

# viradas de caixa antes dos impactos
for a, b, n in SECT:
    if n == "fill":
        k = 0; t = a
        while t < b - 1e-6:
            put("drums", snare(), t, 0, .5 + .5 * (t - a) / (b - a)); t += S16
    if n == "build":
        put("fx", riser(b - a), a, 0, .9)
        t = a; step = BEAT
        while t < b - 1e-6:
            put("drums", snare(), t, 0, .25 + .65 * (t - a) / (b - a))
            if t - a > (b - a) * 0.5: step = S16
            elif t - a > (b - a) * 0.25: step = BEAT / 2
            t += step
        # pad filtrado subindo
        root, ch = PROG[0]
        put("music", pad([midi(n) for n in ch], b - a, 900), a, 0, .12)
for t in IMPACTS:
    put("fx", crash(), t, 0.2, 1.0); put("fx", boom(), t, 0, .8)
put("fx", riser(1.5), 3.5, 0, .5)        # antes da entrada da voz
put("fx", riser(1.5), 19.5, 0, .4)
put("fx", riser(2.0), 70.5, 0, .55)
put("fx", riser(1.6), 81.4, 0, .4)
# acorde final sustentado
put("music", pad([midi(n) for n in PROG[0][1]] + [midi(50)], 5.5, 2200), 85.0, 0, .22)
for n in (62, 66, 69, 74, 78):
    put("music", bell(midi(n), 4.0, .12), 85.0 + 0.04 * (n - 62) / 4, 0.1)

# side-chain "pumping" do kick no baixo/música
pump = np.ones(N)
for bi in range(int(DUR / BEAT)):
    tb = bi * BEAT
    if sect(tb + 0.01) in ("full", "big", "chorus", "verse", "verse2"):
        i = int(tb * SR); m = min(N - i, int(0.35 * SR))
        tt = np.arange(m) / SR
        pump[i:i + m] = np.minimum(pump[i:i + m], 0.45 + 0.55 * (1 - np.exp(-tt / 0.08)))
for k in ("bass", "music"):
    bus[k][0] *= pump; bus[k][1] *= pump

# reverb leve na música
irn = int(1.6 * SR); ti = np.arange(irn) / SR
def ir():
    x = lp(rng.normal(0, 1, irn), 6000) * np.exp(-ti / 0.4); x[: int(0.01 * SR)] = 0
    return x / np.sqrt(np.sum(x ** 2))
for k in ("music", "fx"):
    for c in (0, 1):
        bus[k][c] = bus[k][c] + 0.25 * fftconvolve(bus[k][c], ir())[:N]

mix = {"drums": 0.9, "bass": 0.8, "music": 0.75, "fx": 0.6}
for k, g in mix.items():
    L += bus[k][0] * g; R += bus[k][1] * g
L = hp(L, 30); R = hp(R, 30)
t = np.arange(N) / SR
fade = np.clip((DUR - t) / 3.0, 0, 1)
st = np.stack([L * fade, R * fade], 1)
st = np.tanh(st / np.max(np.abs(st)) * 1.6) / np.tanh(1.6) * 0.9   # saturação suave
sf.write(sys.argv[1], st, SR, subtype="PCM_24")
print("ok", DUR)
