"""Trilha 'corporate lounge' sintetizada (100 BPM). Uso: python music.py main|ad out.wav"""
import sys, numpy as np, wave

SR = 44100
BPM = 100
BEAT = 60 / BPM          # 0.6 s
BAR = 4 * BEAT           # 2.4 s
rng = np.random.default_rng(7)

def mtof(m): return 440.0 * 2 ** ((m - 69) / 12)

CH = {  # baixo, voicing
    'F':  (41, [57, 60, 64, 67]),
    'Am': (45, [55, 59, 60, 64]),
    'Dm': (38, [53, 57, 60, 64]),
    'Bb': (46, [57, 60, 62, 65]),
    'C':  (48, [55, 57, 62, 64]),
}

def env_adsr(n, a=0.005, d=0.3, s=0.6, r=0.3, hold=None):
    t = np.arange(n) / SR
    hold = hold if hold is not None else t[-1] - r
    e = np.where(t < a, t / a, s + (1 - s) * np.exp(-(t - a) / d))
    rel = np.clip((t - hold) / r, 0, 1)
    return e * (1 - rel)

def rhodes(f, dur, vel=0.5):
    n = int((dur + 1.2) * SR); t = np.arange(n) / SR
    idx = 2.2 * vel * np.exp(-t * 3.0) + 0.25
    mod = np.sin(2 * np.pi * f * t) * idx
    car = np.sin(2 * np.pi * f * t + mod)
    tine = 0.12 * np.sin(2 * np.pi * f * 7.0 * t) * np.exp(-t * 18)
    e = np.exp(-t * 1.1) * np.clip(1 - (t - dur) / 1.0, 0, 1) * np.clip(t / 0.003, 0, 1)
    trem = 1 + 0.12 * np.sin(2 * np.pi * 4.8 * t)
    return (car + tine) * e * trem * vel

def pad(f, dur):
    n = int((dur + 1.5) * SR); t = np.arange(n) / SR
    s = np.zeros(n)
    for det in (-0.08, 0.0, 0.07):
        ph = 2 * np.pi * f * (2 ** (det / 12)) * t
        s += np.sin(ph) + 0.3 * np.sin(2 * ph) + 0.12 * np.sin(3 * ph)
    e = np.clip(t / 0.9, 0, 1) * np.clip(1 - (t - dur) / 1.5, 0, 1)
    return s * e / 3

def bass(f, dur):
    n = int((dur + 0.05) * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t)
    s = np.tanh(1.6 * s)
    e = np.clip(t / 0.008, 0, 1) * np.clip((dur - t) / 0.05, 0, 1)
    return s * e

def kick():
    n = int(0.45 * SR); t = np.arange(n) / SR
    f = 45 + 90 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 7.5) + 0.15 * rng.standard_normal(n) * np.exp(-t * 120)

def hat(open_=False):
    n = int((0.25 if open_ else 0.06) * SR); t = np.arange(n) / SR
    x = rng.standard_normal(n)
    x = np.diff(np.concatenate([[0], x]))       # high-pass rudimentar
    x = np.diff(np.concatenate([[0], x]))
    x = np.convolve(x, [0.25,0.5,0.25], 'same')
    return x * np.exp(-t * (14 if open_ else 70)) * 0.10

def clap():
    n = int(0.35 * SR); t = np.arange(n) / SR
    x = rng.standard_normal(n)
    x = np.convolve(x, np.ones(4) / 4, 'same') - np.convolve(x, np.ones(40) / 40, 'same')
    e = np.zeros(n)
    for o in (0, 0.011, 0.022):
        e += np.where(t >= o, np.exp(-(t - o) * 60), 0)
    e += 0.5 * np.exp(-t * 12)
    return x * e * 0.22

def swell(dur):
    n = int(dur * SR); t = np.arange(n) / SR
    x = rng.standard_normal(n)
    # passa-baixa que abre ao longo do tempo
    y = np.zeros(n); a0 = 0.02; acc = 0.0
    alpha = a0 + (0.5 - a0) * (t / dur) ** 2
    for i in range(n):
        acc += alpha[i] * (x[i] - acc); y[i] = acc
    return y * (t / dur) ** 2.2 * 0.5

def add(buf, sig, at, gain=1.0):
    i = int(at * SR)
    if i >= len(buf): return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[:j - i] * gain

def reverb(x, secs=2.2, mix=0.22):
    n = int(secs * SR); t = np.arange(n) / SR
    ir = rng.standard_normal(n) * np.exp(-t * 3.2)
    ir = np.convolve(ir, np.ones(30) / 30, 'same'); ir /= np.sqrt(np.sum(ir ** 2))
    L = len(x) + n
    N = 1 << int(np.ceil(np.log2(L)))
    wet = np.fft.irfft(np.fft.rfft(x, N) * np.fft.rfft(ir, N), N)[:len(x)]
    return x + mix * wet

def lowpass(x, a):
    y = np.empty_like(x); acc = 0.0
    # vetorizado via lfilter-like recursion em blocos simples
    from itertools import accumulate
    for i, v in enumerate(x):
        acc += a * (v - acc); y[i] = acc
    return y

def build(mode):
    if mode == 'main':
        total = 40.0
        prog = ['F', 'Am', 'Dm', 'Bb'] * 3 + ['F', 'Am', 'Bb', 'C']   # 16 compassos = 38.4 s
        final_at = 36.0
        prog = prog[:15]                                             # compasso 16 = acorde final
        sec = dict(hats=4.8, kick=12.0, clap=21.6, arp=21.6, drop=final_at)
        swells = [(10.8, 1.2), (19.8, 1.2)]
    else:  # ad 15 s
        total = 15.2
        prog = ['F', 'Am', 'Dm', 'Bb', 'C']
        final_at = 12.0
        sec = dict(hats=0.0, kick=2.4, clap=4.8, arp=4.8, drop=final_at)
        swells = [(1.8, 0.6), (10.8, 1.2)]
    nb = int(total * SR)
    keys = np.zeros(nb); pads = np.zeros(nb); bs = np.zeros(nb); dr = np.zeros(nb); fx = np.zeros(nb)

    for b, name in enumerate(prog):
        t0 = b * BAR
        if t0 >= final_at: break
        root, voic = CH[name]
        grow = 0.55 + 0.45 * min(1, t0 / final_at)        # crescente
        for m in voic:
            add(pads, pad(mtof(m), BAR), t0, 0.05 * grow)
        # rhodes: tempo 1 e contratempo do 2
        for off, vel, dur in ((0, 0.55, 1.1), (1.5 * BEAT, 0.38, 0.5), (3 * BEAT, 0.3, 0.5)):
            for k, m in enumerate(voic):
                add(keys, rhodes(mtof(m), dur, vel), t0 + off + 0.006 * k, 0.16 * grow)
        if t0 >= (4.8 if mode == 'main' else 0.0):
            for off, mm, d in ((0, 0, 0.5), (1.5 * BEAT, 12, 0.25), (2 * BEAT, 0, 0.5), (3.5 * BEAT, 7, 0.25)):
                add(bs, bass(mtof(root - 12 + mm), d), t0 + off, 0.15)
        if t0 >= sec['arp']:
            arp = voic + [voic[1] + 12]
            for s16 in range(16):
                m = arp[(s16 * 3) % len(arp)] + 12
                add(keys, rhodes(mtof(m), 0.12, 0.25), t0 + s16 * BEAT / 4, 0.05)
        for beat in range(4):
            tb = t0 + beat * BEAT
            if tb >= sec['kick']: add(dr, kick(), tb, 0.32)
            if tb >= sec['clap'] and beat in (1, 3): add(dr, clap(), tb, 0.45)
            if tb >= sec['hats']:
                add(dr, hat(), tb + BEAT / 2, 0.55)
                if tb >= sec['clap']: add(dr, hat(True), tb + BEAT / 2, 0.25); add(dr, hat(), tb, 0.25)
    # acorde final
    root, voic = CH['F']
    for k, m in enumerate(voic + [72]):
        add(keys, rhodes(mtof(m), 3.0, 0.5), final_at + 0.01 * k, 0.13)
        add(pads, pad(mtof(m), 3.2), final_at, 0.06)
    add(bs, bass(mtof(root - 12), 1.6) * np.linspace(1, 0, int(1.65 * SR)), final_at, 0.32)
    add(dr, kick(), final_at, 0.5)
    for at, d in swells: add(fx, swell(d), at, 0.10)

    pads = lowpass(pads, 0.08)
    mix = 1.0 * reverb(keys, 2.4, 0.30) + pads + bs + reverb(dr, 1.2, 0.08) + reverb(fx, 1.5, 0.3)
    fade = np.ones(nb); fl = int(1.2 * SR); fade[-fl:] = np.linspace(1, 0, fl)
    mix *= fade
    mix = np.tanh(mix / np.max(np.abs(mix)) * 1.3) * 0.8
    # estéreo simples: leve diferença de atraso no reverb das teclas
    L = mix; R = np.concatenate([np.zeros(18), mix[:-18]]) * 0.98 + 0.02 * mix
    return np.stack([L, R], 1)

if __name__ == '__main__':
    mode, out = sys.argv[1], sys.argv[2]
    st = build(mode)
    with wave.open(out, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(st, -1, 1) * 32767).astype('<i2').tobytes())
    print(out, st.shape[0] / SR, 's')
