"""Trilha original da Vídeo Imóvel Studio 3D, sintetizada do zero (sem amostras de terceiros).
Gera uma faixa por vídeo, com eventos sincronizados aos cortes do roteiro.
uso: python3 music.py  -> audio/<video>.wav"""
import numpy as np, os
from scipy.signal import fftconvolve, butter, sosfilt

SR = 48000
BPM = 96.0
BEAT = 60.0 / BPM
rng = np.random.default_rng(7)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audio')
os.makedirs(OUT, exist_ok=True)

def hz(n): return 440.0 * 2 ** ((n - 69) / 12.0)
# progressão em Ré maior: Dmaj9 – Bm9 – Gmaj7(#11) – Asus
CHORDS = [[50, 57, 62, 64, 66, 69], [47, 54, 59, 61, 62, 66], [43, 50, 55, 59, 61, 66], [45, 52, 57, 59, 62, 64]]
BASS = [38, 35, 31, 33]

def env_adsr(n, a, d, s, r, sr=SR):
    e = np.ones(n) * s
    A, D, Rr = int(a * sr), int(d * sr), int(r * sr)
    A = min(A, n); e[:A] = np.linspace(0, 1, A, endpoint=False) if A else e[:A]
    D2 = min(D, max(0, n - A)); e[A:A + D2] = np.linspace(1, s, D2, endpoint=False) if D2 else e[A:A + D2]
    if Rr and n > Rr: e[-Rr:] *= np.linspace(1, 0, Rr)
    return e

def lp(x, fc, order=2):
    sos = butter(order, min(fc, SR / 2 - 100) / (SR / 2), 'low', output='sos'); return sosfilt(sos, x, axis=0)
def hp(x, fc, order=2):
    sos = butter(order, fc / (SR / 2), 'high', output='sos'); return sosfilt(sos, x, axis=0)

def saw(f, t): return 2 * ((t * f) % 1.0) - 1

def pad(dur, chords_at, level=0.16, bright=1800):
    n = int(dur * SR); out = np.zeros((n, 2))
    for (t0, t1, ch) in chords_at:
        a, b = int(t0 * SR), min(n, int((t1 + 1.6) * SR)); m = b - a
        if m <= 0: continue
        tt = np.arange(m) / SR; sig = np.zeros((m, 2))
        for i, note in enumerate(ch):
            for det, pan in ((-0.09, 0.2), (0.0, 0.5), (0.11, 0.8)):
                f = hz(note) * 2 ** (det / 12)
                w = saw(f, tt + rng.random()) * 0.5 + np.sin(2 * np.pi * f * tt) * 0.5
                sig[:, 0] += w * (1 - pan); sig[:, 1] += w * pan
        e = env_adsr(m, 1.4, 0.5, 0.85, 1.6)
        sig = lp(sig, bright) * e[:, None] * level / len(ch)
        out[a:b] += sig
    return out

def pluck(f, dur=1.2, bright=1.0):
    n = int(dur * SR); t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * k * t) * (0.6 ** (k - 1)) * np.exp(-t * (3 + k * 2.2 / bright)) for k in range(1, 6))
    return s * np.minimum(1, t / 0.004)

def piano(f, dur=2.6):
    n = int(dur * SR); t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * k * (1 + 0.0004 * k * k) * t) * (0.55 ** (k - 1)) * np.exp(-t * (1.1 + k * 0.9)) for k in range(1, 8))
    return s * np.minimum(1, t / 0.003)

def kick(dur=0.5):
    n = int(dur * SR); t = np.arange(n) / SR
    f = 46 + 90 * np.exp(-t * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7.5)

def shaker(dur=0.09):
    n = int(dur * SR); t = np.arange(n) / SR
    return hp(rng.standard_normal(n), 6000) * np.exp(-t * 55)

def riser(dur):
    n = int(dur * SR); t = np.arange(n) / SR
    noise = rng.standard_normal(n)
    out = np.zeros(n); seg = 2048
    for i in range(0, n, seg):
        fc = 300 + 7000 * (i / n) ** 2
        out[i:i + seg] = lp(noise[i:i + seg], fc, 1)
    return out * (t / dur) ** 2 * 0.5

def impact(dur=3.5):
    n = int(dur * SR); t = np.arange(n) / SR
    boom = np.sin(2 * np.pi * (38 + 40 * np.exp(-t * 6)) * t) * np.exp(-t * 1.6)
    hit = lp(rng.standard_normal(n), 1800) * np.exp(-t * 9) * 0.6
    return boom + hit

def place(buf, sig, t, gain=1.0, pan=0.5):
    a = int(t * SR); b = min(len(buf), a + len(sig))
    if a >= len(buf) or b <= a: return
    s = sig[:b - a] * gain
    buf[a:b, 0] += s * (1 - pan) * 1.4; buf[a:b, 1] += s * pan * 1.4

def reverb(x, secs=3.2, mix=0.28):
    n = int(secs * SR); t = np.arange(n) / SR
    ir = rng.standard_normal((n, 2)) * np.exp(-t * (6.9 / secs))[:, None]
    ir = lp(ir, 5000); ir /= np.sqrt((ir ** 2).sum(axis=0))
    wet = np.stack([fftconvolve(x[:, c], ir[:, c])[:len(x)] for c in range(2)], axis=1)
    return x * (1 - mix) + wet * mix * 1.6

def chords_timeline(dur, start=0.0, bars_per=2):
    out = []; t = start; i = 0; L = BEAT * 4 * bars_per
    while t < dur: out.append((t, min(dur, t + L), CHORDS[i % 4])); t += L; i += 1
    return out

def arpeggio(buf, t0, t1, level=0.06, step=0.5, bright=1.0, pan_sw=True):
    t = t0; k = 0; L = BEAT * 8
    while t < t1:
        ch = CHORDS[int((t / L)) % 4]; note = ch[[1, 2, 3, 4, 3, 2][k % 6]] + 12
        place(buf, pluck(hz(note), 1.4, bright), t, level, 0.3 + 0.4 * ((k % 4) / 3) if pan_sw else 0.5)
        t += BEAT * step; k += 1

def melody(buf, notes, level=0.09):
    for (t, n, d) in notes: place(buf, piano(hz(n), d), t, level, 0.45)

def drums(buf, t0, t1, level=0.5, shk=0.07, four=True):
    t = t0; k = 0
    while t < t1:
        if four or k % 2 == 0: place(buf, kick(), t, level, 0.5)
        place(buf, shaker(), t + BEAT / 2, shk, 0.65); place(buf, shaker(), t + BEAT * 0.75, shk * 0.5, 0.35)
        t += BEAT; k += 1

def bassline(buf, t0, t1, level=0.22):
    L = BEAT * 8; t = t0
    while t < t1:
        root = BASS[int(t / L) % 4]; n = int(min(L, t1 - t) * SR); tt = np.arange(n) / SR
        s = np.sin(2 * np.pi * hz(root) * tt) + 0.25 * np.sin(2 * np.pi * hz(root) * 2 * tt)
        s *= env_adsr(n, 0.05, 0.3, 0.8, 0.4)
        place(buf, s, t, level, 0.5); t += L

def endcard(buf, t, dur_total, level=0.2):
    # acorde final aberto + brilho
    ch = [50, 57, 62, 66, 69, 74]
    for i, n in enumerate(ch): place(buf, piano(hz(n), dur_total - t + 1), t + i * 0.06, level * 0.7, 0.3 + i * 0.08)
    place(buf, impact(2.5) * 0.35, t, 0.6)

def master(buf, dur, fade_in=0.6, fade_out=1.8):
    n = int(dur * SR); buf = buf[:n]
    buf = reverb(buf)
    buf = hp(buf, 28)
    fi, fo = int(fade_in * SR), int(fade_out * SR)
    buf[:fi] *= np.linspace(0, 1, fi)[:, None]; buf[-fo:] *= np.linspace(1, 0, fo)[:, None]
    peak = np.abs(buf).max(); buf = buf / peak * 0.89
    return np.tanh(buf * 1.1) / np.tanh(1.1)

def write(name, buf):
    import wave
    x = (np.clip(buf, -1, 1) * 32767).astype('<i2')
    with wave.open(os.path.join(OUT, name + '.wav'), 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(x.tobytes())
    print(name, len(buf) / SR, 's')

def track(name, dur, build):
    buf = np.zeros((int((dur + 4) * SR), 2)); build(buf); write(name, master(buf, dur))

# ---------- NÍVEL 1 · 25 s: preciso, calmo
def b1(buf):
    buf += pad(29, chords_timeline(22.2), 0.14, 1400)
    place(buf, riser(1.6), 2.8, 0.35); place(buf, impact(3) * 0.25, 4.4)
    arpeggio(buf, 4.5, 21.5, 0.045, 1.0, 0.8)
    place(buf, riser(1.2), 8.8, 0.2); place(buf, riser(1.2), 16.8, 0.2)
    endcard(buf, 22.0, 25)
track_list = [('essencial', 25, b1)]

# ---------- NÍVEL 2 · 30 s: ganha textura e ritmo leve
def b2(buf):
    buf += pad(34, chords_timeline(27.2), 0.14, 1900)
    arpeggio(buf, 0.5, 27, 0.05, 0.5, 1.0)
    place(buf, riser(1.5), 2.6, 0.3); place(buf, impact(3) * 0.25, 4.2)
    place(buf, riser(1.5), 8.6, 0.3); place(buf, impact(3) * 0.25, 10.1)
    drums(buf, 10.1, 26.8, 0.0, 0.06)
    bassline(buf, 10.1, 27, 0.14)
    place(buf, riser(1.2), 18.4, 0.25); place(buf, riser(1.4), 21.7, 0.25)
    endcard(buf, 27.0, 30)
track_list.append(('acabamentos', 30, b2))

# ---------- NÍVEL 3 · 40 s: acolhedor, piano
def b3(buf):
    buf += pad(44, chords_timeline(37.2), 0.13, 2100)
    arpeggio(buf, 4.2, 37, 0.035, 0.5, 1.2)
    bassline(buf, 10, 37, 0.16)
    L = BEAT * 8
    mel = []
    for bar in range(int(10 / L), int(37 / L) + 1):
        t = bar * L; ch = CHORDS[bar % 4]
        mel += [(t, ch[3] + 12, 2.4), (t + BEAT * 1.5, ch[4] + 12, 2.0), (t + BEAT * 3, ch[5] + 12, 2.6), (t + BEAT * 5, ch[4] + 12, 2.2), (t + BEAT * 6.5, ch[2] + 12, 2.8)]
    melody(buf, [m for m in mel if 10 <= m[0] < 36.5], 0.075)
    place(buf, riser(1.6), 8.4, 0.3); place(buf, impact(3) * 0.22, 10.0)
    drums(buf, 18, 32, 0.0, 0.05)
    endcard(buf, 37.0, 40)
track_list.append(('decorado', 40, b3))

# ---------- NÍVEL 4 · 60 s: cinematic
def b4(buf):
    buf += pad(64, [(0, 5, [38, 45, 50, 57])], 0.12, 900)
    place(buf, riser(4.6), 0.4, 0.45); place(buf, impact(4), 5.0, 0.6)
    buf += pad(64, [(c[0] + 5, c[1] + 5, c[2]) for c in chords_timeline(37)], 0.13, 2300)
    arpeggio(buf, 5, 42, 0.04, 0.5, 1.3)
    place(buf, riser(2.4), 9.6, 0.4); place(buf, impact(3.5), 12.0, 0.5)
    bassline(buf, 12, 42, 0.2)
    drums(buf, 15.0, 22.0, 0.35, 0.05)
    drums(buf, 22.0, 42.0, 0.5, 0.07)
    L = BEAT * 8; mel = []
    for bar in range(int(22 / L), int(42 / L) + 1):
        t = bar * L; ch = CHORDS[bar % 4]
        mel += [(t, ch[4] + 12, 2.2), (t + BEAT * 2, ch[5] + 12, 2.0), (t + BEAT * 4, ch[3] + 12, 2.4), (t + BEAT * 6, ch[2] + 12, 2.6)]
    melody(buf, [m for m in mel if 22 <= m[0] < 41.6], 0.07)
    # pausa emocional
    buf += pad(64, [(42, 50, [43, 50, 55, 59, 62, 66])], 0.16, 1700)
    for i, n in enumerate([74, 71, 69, 66, 69, 71, 74, 76]): place(buf, piano(hz(n), 3.0), 42.4 + i * BEAT * 1.5, 0.085, 0.45)
    place(buf, riser(2.6), 47.4, 0.45); place(buf, impact(4.5), 50.0, 0.7)
    buf += pad(64, [(50, 55, [50, 57, 62, 66, 69, 74])], 0.16, 2600)
    endcard(buf, 55.0, 60, 0.24)
track_list.append(('cinematic', 60, b4))

if __name__ == '__main__':
    for name, dur, b in track_list: track(name, dur, b)
