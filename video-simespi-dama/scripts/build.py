"""Monta o vídeo SIMESPI x Dama Bier (16:9, <= 60 s) com ffmpeg."""
import os, subprocess, sys, json

S = os.path.dirname(os.path.abspath(__file__))
H, G, VO = f"{S}/h", f"{S}/gfx", f"{S}/vo2"
OUT = sys.argv[1] if len(sys.argv) > 1 else f"{S}/out/simespi_dama.mp4"
os.makedirs(os.path.dirname(OUT), exist_ok=True)
END = 59.6

# (início na timeline, arquivo, ponto de entrada no clipe, transição de entrada em s)
SHOTS = [
    (0.0,  "IMG_2701.mov", 0.15, 0.0),   # fachada Dama Bier / céu
    (3.9,  "IMG_2700.mov", 0.40, 0.15),  # fachada e jardim
    (7.7,  "IMG_2669.mov", 0.60, 0.50),  # tanques, panorâmica
    (10.3, "IMG_2671.mov", 6.00, 0.15),  # moagem / clarificação
    (12.7, "IMG_2676.mov", 5.00, 0.15),  # profissional despejando malte
    (16.2, "IMG_2687.mov", 0.30, 0.50),  # sacos de malte (fornecedores)
    (18.4, "IMG_2677.mov", 0.80, 0.15),  # malte na moega
    (20.6, "IMG_2673.mov", 0.40, 0.15),  # fileira de fermentadores
    (23.0, "IMG_2688.mov", 0.50, 0.50),  # tanques DAMA
    (25.6, "IMG_2696.mov", 8.50, 0.15),  # interior da tina
    (28.0, "IMG_2698.mov", 0.50, 0.15),  # cervejeiro operando
    (31.2, "IMG_2610.mov", 6.20, 0.50),  # visita SIMESPI na fábrica
    (34.6, "IMG_2642.mov", 0.30, 0.15),  # linha de envase
    (36.6, "IMG_2653.mov", 0.30, 0.15),  # garrafas na esteira
    (38.4, "IMG_2662.mov", 0.30, 0.15),  # rotuladora com rótulos 35 anos
    (40.3, "IMG_2652.mov", 35.3, 0.50),  # brinde: taça, garrafa, tela Dama + SIMESPI
    (43.2, "IMG_2656.mov", 1.60, 0.15),  # bobina do rótulo comemorativo
    (44.6, "IMG_2600.mov", 0.30, 0.15),  # garrafa nas mãos
    (46.3, "IMG_2666.mov", 0.30, 0.15),  # gargalos com selo 35 anos
    (48.2, "IMG_2598.mov", 26.8, 0.15),  # entrega do kit (garrafa e taças)
    (52.4, "CARD", 0.0, 0.70),           # cartela final
]

# Locução: trecho -> início (s)
GAPS = [0.5, 0.55, 0.5, 0.5, 0.55, 0.6, 0.6, 0.55]
def wavdur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))
vo_starts, t = [], 0.0
for i in range(8):
    t += GAPS[i]; vo_starts.append(round(t, 3)); t += wavdur(f"{VO}/a_{i+1}.wav")
vo_end = t

TONEMAP = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,"
           "zscale=t=bt709:m=bt709:r=tv,format=yuv420p,eq=gamma=1.05:saturation=1.03")

args = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-stats"]
filt = []
n = len(SHOTS)
for i, (b, f, inp, tr) in enumerate(SHOTS):
    nb = SHOTS[i + 1][0] if i + 1 < n else END
    L = nb - b + tr
    if f == "CARD":
        args += ["-loop", "1", "-t", f"{L:.3f}", "-framerate", "30", "-i", f"{G}/card_bg.png"]
    else:
        args += ["-ss", f"{inp:.3f}", "-t", f"{L + 0.1:.3f}", "-i", f"{H}/{f}"]
    SHOTS[i] = (b, f, inp, tr, L)

# grafismos
gfx_inputs = {}
for name in ["lt_cpl", "txt_industria", "card_div", "card_simespi", "card_35", "card_dama"]:
    gfx_inputs[name] = len(SHOTS) + len(gfx_inputs)
    args += ["-loop", "1", "-framerate", "30", "-t", "62", "-i", f"{G}/{name}.png"]
# áudio
a0 = len(SHOTS) + len(gfx_inputs)
for i in range(8):
    args += ["-i", f"{VO}/a_{i+1}.wav"]
args += ["-i", f"{S}/music.wav"]
mus = a0 + 8

# --- vídeo
for i, (b, f, inp, tr, L) in enumerate(SHOTS):
    if f == "CARD":
        ci = i
        chain = (f"[{i}:v]format=rgba,fps=30,setsar=1[cb];"
                 f"[{gfx_inputs['card_div']}:v]format=rgba,fade=in:st=0.5:d=0.8:alpha=1[d0];"
                 f"[{gfx_inputs['card_simespi']}:v]format=rgba,fade=in:st=0.8:d=0.8:alpha=1[d1];"
                 f"[{gfx_inputs['card_35']}:v]format=rgba,fade=in:st=1.3:d=0.8:alpha=1[d2];"
                 f"[{gfx_inputs['card_dama']}:v]format=rgba,fade=in:st=1.8:d=0.8:alpha=1[d3];"
                 f"[cb][d0]overlay=shortest=1[c1];[c1][d1]overlay=shortest=1[c2];[c2][d2]overlay=shortest=1[c3];"
                 f"[c3][d3]overlay=shortest=1,trim=duration={L:.3f},fade=out:st={L-0.6:.3f}:d=0.6:color=white,"
                 f"format=yuv420p,setpts=PTS-STARTPTS,settb=1/30[v{i}]")
        filt.append(chain)
    else:
        filt.append(f"[{i}:v]{TONEMAP},scale=1920:1080:flags=lanczos,fps=30,setsar=1,"
                    f"trim=duration={L:.3f},setpts=PTS-STARTPTS,settb=1/30[v{i}]")
prev = "v0"
for i in range(1, n):
    b, f, inp, tr, L = SHOTS[i]
    out = f"x{i}"
    filt.append(f"[{prev}][v{i}]xfade=transition=fade:duration={tr:.3f}:offset={b - tr:.3f}[{out}]")
    prev = out

def ov(src, name, t0, t1, fi=0.5, fo=0.5):
    k = gfx_inputs[name]
    filt.append(f"[{k}:v]format=rgba,trim=duration={t1:.2f},fade=in:st={t0:.2f}:d={fi}:alpha=1,"
                f"fade=out:st={t1 - fo:.2f}:d={fo}:alpha=1,setpts=PTS-STARTPTS[g_{name}]")
    filt.append(f"[{src}][g_{name}]overlay=eof_action=pass:enable='between(t,{t0},{t1})'[o_{name}]")
    return f"o_{name}"
v = ov(prev, "lt_cpl", 26.4, 30.9)
v = ov(v, "txt_industria", vo_starts[6] + 0.1, 52.0, 0.6, 0.6)
filt.append(f"[{v}]trim=duration={END},format=yuv420p[vout]")

# --- áudio
vo_lbls = []
for i in range(8):
    d = int(vo_starts[i] * 1000)
    filt.append(f"[{a0+i}:a]aresample=48000,aformat=channel_layouts=mono,adelay={d}|{d}[vo{i}]")
    vo_lbls.append(f"[vo{i}]")
filt.append(f"{''.join(vo_lbls)}amix=inputs=8:normalize=0,"
            f"highpass=f=75,equalizer=f=200:t=q:w=1.2:g=1.5,equalizer=f=3500:t=q:w=1.5:g=1.2,"
            f"acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2,"
            f"apad=whole_dur={END},aformat=channel_layouts=stereo,asplit=2[vomix][vosc]")
filt.append(f"[{mus}:a]atrim=duration={END},volume=-11dB,afade=t=out:st={END-1.8}:d=1.8[mus0]")
filt.append(f"[mus0][vosc]sidechaincompress=threshold=0.03:ratio=2.5:attack=150:release=1000:makeup=1[musd]")
filt.append(f"[vomix][musd]amix=inputs=2:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=9,"
            f"atrim=duration={END},afade=t=out:st={END-0.8}:d=0.8,aresample=48000[aout]")

fc_path = f"{S}/filter.txt"
open(fc_path, "w").write(";\n".join(filt))
args += ["-filter_complex_script", fc_path, "-map", "[vout]", "-map", "[aout]",
         "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-profile:v", "high", "-pix_fmt", "yuv420p",
         "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
         "-r", "30", "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-movflags", "+faststart",
         "-t", f"{END}", OUT]
json.dump(dict(vo_starts=vo_starts, vo_end=vo_end, shots=[s[:4] for s in SHOTS]),
          open(f"{S}/timeline.json", "w"), indent=1)
print("VO starts:", vo_starts, "VO end:", round(vo_end, 2))
subprocess.run(args, check=True)
print("done", OUT)
