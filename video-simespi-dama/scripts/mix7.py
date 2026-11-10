"""Mixagem v6: trilha ElevenLabs (m3), locução Gabriel (voA) recortada por parágrafo, SFX sintetizados nos cortes."""
import os, json, subprocess, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
S = os.path.dirname(os.path.abspath(__file__)); N = f"{S}/n"; SR = 48000; END = 58.0
g = {'__file__': f"{S}/comp.py", '__name__': 'x'}
exec(open(f"{S}/comp.py").read().replace('if __name__ == "__main__":\n    main()', ''), g)
tl, kend = g['build_timeline']()

def load(p):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", p, "-ar", str(SR), "-ac", "2", "/tmp/_m.wav"], check=True)
    x, _ = sf.read("/tmp/_m.wav"); return x
mus = load(f"{N}/m3.mp3"); vo = load(f"{N}/voA.mp3")[:, 0]
n = int(END * SR)
M = np.zeros((n, 2)); M[:min(n, len(mus))] = mus[:n]
# locução: parágrafos (cortes nos mínimos de energia) -> posição na trilha
cuts = [0.0, 3.13, 7.75, 16.53, 27.07, 31.49, 35.15, 37.39, len(vo) / SR]
place = [2.46, 5.90, 10.45, 18.85, 33.20, 38.10, 45.75, 50.20]
VO = np.zeros(n)
for k in range(8):
    a, b = int(cuts[k] * SR), int(cuts[k + 1] * SR); seg = vo[a:b].copy()
    f = int(0.008 * SR); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    i = int(place[k] * SR); VO[i:i + len(seg)] += seg[:n - i]
# EQ/compressão leve na voz via ffmpeg
sf.write("/tmp/_vo.wav", VO, SR)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "/tmp/_vo.wav", "-af",
                "highpass=f=80,equalizer=f=180:t=q:w=1:g=1.5,equalizer=f=3200:t=q:w=1.4:g=2,acompressor=threshold=-18dB:ratio=3:attack=6:release=90:makeup=2",
                "/tmp/_vo2.wav"], check=True)
VO, _ = sf.read("/tmp/_vo2.wav")
# ducking da trilha pela voz (envelope suave)
env = np.abs(VO); w = int(0.05 * SR)
env = np.convolve(env, np.ones(w) / w, mode="same")
duck = 1.0 - 0.55 * np.clip(env / 0.03, 0, 1)
k = int(0.25 * SR); duck = np.convolve(duck, np.ones(k) / k, mode="same")
M *= duck[:, None]
# SFX
rng = np.random.default_rng(3)
def bp(x, a, b): return sosfilt(butter(2, [a, b], 'band', fs=SR, output='sos'), x)
def whoosh(d=0.32):
    m = int(d * SR); t = np.arange(m) / SR; x = rng.normal(0, 1, m)
    out = np.zeros(m); blk = 1024
    for i in range(0, m, blk):
        p = i / m; fc = 600 + 5200 * np.sin(np.pi * p)
        out[i:i + blk] = bp(x[i:i + blk], fc * 0.5, min(20000, fc * 1.6))[:len(out[i:i + blk])]
    return out * np.sin(np.pi * t / d) ** 2 * 0.35
def impact():
    m = int(1.6 * SR); t = np.arange(m) / SR
    boom = np.sin(2 * np.pi * np.cumsum(38 + 70 * np.exp(-t / 0.06)) / SR) * np.exp(-t / 0.45)
    crack = sosfilt(butter(2, 3000, 'high', fs=SR, output='sos'), rng.normal(0, 1, m)) * np.exp(-t / 0.08) * 0.25
    return (boom * 0.8 + crack) * 0.55
def riser(d):
    m = int(d * SR); t = np.arange(m) / SR; x = rng.normal(0, 1, m); out = np.zeros(m); blk = 1024
    for i in range(0, m, blk):
        fc = 400 + 7000 * (i / m) ** 2
        out[i:i + blk] = bp(x[i:i + blk], fc * 0.7, min(20000, fc * 1.3))[:len(out[i:i + blk])]
    tone = np.sin(2 * np.pi * np.cumsum(180 * 2 ** (2.5 * t / d)) / SR) * 0.08
    return (out * 0.3 + tone) * (t / d) ** 1.8
def clink():
    m = int(1.4 * SR); t = np.arange(m) / SR
    return sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t / dcy) for f, a, dcy in
               ((3150, .5, .35), (4720, .3, .25), (6890, .2, .15), (2210, .25, .5))) * 0.18
SFX = np.zeros(n)
def put(sig, t, gdb=0):
    i = int(t * SR)
    if i >= n: return
    s = sig[:n - i] * 10 ** (gdb / 20); SFX[i:i + len(s)] += s
for (t0, t1, kind, nb, content, trans) in tl:
    if trans == "whip": put(whoosh(), t0 - 0.16, -15)
    if trans == "flash": put(impact(), t0, -15)
put(impact(), 0.0, -15); put(riser(2.0), 29.7, -15); put(impact(), 31.72, -15)
put(clink(), 42.50, -2); put(impact(), g['tb'](kend), -15)
SFXs = np.stack([SFX, SFX], 1)
mix = M * 0.9 + np.stack([VO, VO], 1) * 1.0 + SFXs
mix[-int(0.6 * SR):] *= np.linspace(1, 0, int(0.6 * SR))[:, None]
sf.write(f"{S}/out/v7_mix_raw.wav", mix, SR, subtype="PCM_24")
# normalização linear para -14 LUFS / -1 dBTP
o = subprocess.run(["ffmpeg", "-hide_banner", "-i", f"{S}/out/v7_mix_raw.wav", "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"],
                   capture_output=True, text=True).stderr
j = json.loads(o[o.rindex("{"):o.rindex("}") + 1])
gain = -14 - float(j["input_i"])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{S}/out/v7_mix_raw.wav", "-af",
                f"volume={gain:.2f}dB,alimiter=limit=0.89:attack=4:release=60:level=0", "-ar", "48000", f"{S}/out/v7_mix.wav"], check=True)
print("VO:", list(zip(place, np.round(np.diff(cuts), 2))), "| ganho", round(gain, 2))
