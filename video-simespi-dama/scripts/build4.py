"""V2 — SIMESPI x Dama Bier (16:9, <= 90 s): locução integral (3 trechos levemente condensados),
drones de Piracicaba e de indústrias associadas, respiros só com trilha."""
import os, subprocess, sys, json

S = os.path.dirname(os.path.abspath(__file__))
H, R, G, VO = f"{S}/h", f"{S}/ref", f"{S}/gfx", f"{S}/vo7"
OUT = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else f"{S}/out/simespi_dama_v4.mp4"
os.makedirs(os.path.dirname(OUT), exist_ok=True)
END = 89.9

# Recortes para esconder GCs / legendas / selos dos vídeos prontos (aplicados antes do scale p/ 1920x1080)
C_S26 = "crop=1520:855:80:40"          # SIMESPI 2026: tira selo 35 (sup. dir.) e legenda (inferior)
C_S24 = "crop=1440:810:240:0"          # SIMESPI 2024: tira janela de Libras e legenda
C_DP = "crop=3072:1728:384:0"          # DanPower 4K: tira legenda
C_EB = "crop=1227:690:300:210"         # EB Bombas: área ativa do letterbox
C_AG = "crop=1080:608:0:560"           # Águia (vertical): faixa horizontal com helicóptero e rio
C_NONE = None

# (início na timeline, arquivo, ponto de entrada, transição de entrada, tipo, recorte)
#  tipo: hlg = iPhone HDR (tone-map) | sdr
R4 = "rotate=4*PI/180:ow=iw:oh=ih,scale=iw*1.125:ih*1.125,crop=1920:1080"     # endireitar (+4°)
R43 = "rotate=4.3*PI/180:ow=iw:oh=ih,scale=iw*1.135:ih*1.135,crop=1920:1080"  # endireitar (+4,3°)
SHOTS = [
    # ABERTURA A FRIO — o brinde (só trilha)
    (0.0,  f"{H}/IMG_2652.mov",      38.30, 0.0,  "hlg", R4),      # ela ri com a taça (endireitado)
    (2.0,  f"{H}/IMG_2655.mov",      0.05,  0.1,  "hlg", C_NONE),  # garrafas 35 anos
    (3.0,  f"{H}/IMG_2598.mov",      28.00, 0.1,  "hlg", C_NONE),  # ele com garrafa e taça
    (4.3,  f"{H}/IMG_2666.mov",      0.30,  0.1,  "hlg", C_NONE),  # selos 35 anos
    # 1 — Piracicaba
    (5.0,  f"{R}/paques.mp4",        0.20,  0.3,  "sdr", C_NONE),
    (7.3,  f"{R}/simespi2026.mp4",   166.70, 0.1, "sdr", C_S26),
    (9.1,  f"{R}/simespi2026.mp4",   158.00, 0.1, "sdr", C_S26),   # rio Piracicaba
    (10.5, f"{H}/IMG_2701.mov",      0.15,  0.3,  "hlg", C_NONE),
    # 2 — chegada e fábrica
    (11.8, f"{H}/IMG_2606.mov",      1.00,  0.1,  "hlg", C_NONE),  # anfitrião abre a porta
    (13.6, f"{H}/IMG_2608.mov",      2.00,  0.1,  "hlg", R43),     # entrada (endireitado)
    (15.4, f"{H}/IMG_2669.mov",      0.60,  0.1,  "hlg", C_NONE),
    (16.9, f"{H}/IMG_2671.mov",      6.00,  0.1,  "hlg", C_NONE),
    (18.4, f"{H}/IMG_2676.mov",      5.00,  0.1,  "hlg", C_NONE),
    # QUEBRA 1 — o passeio
    (21.0, f"{H}/IMG_2611.mov",      0.30,  0.1,  "hlg", C_NONE),
    (22.4, f"{H}/IMG_2617.mov",      5.60,  0.1,  "hlg", C_NONE),
    # 3 — cadeia produtiva
    (23.4, f"{H}/IMG_2687.mov",      0.30,  0.1,  "hlg", C_NONE),
    (25.0, f"{R}/uninorte_drone1.mp4", 23.0, 0.1, "sdr", C_NONE),
    (27.0, f"{R}/danpower.mp4",      2.90,  0.1,  "sdr", C_DP),
    (28.6, f"{R}/simespi2026.mp4",   106.30, 0.1, "sdr", C_S26),
    (30.6, f"{R}/simespi2026.mp4",   87.85, 0.1,  "sdr", C_S26),
    (31.7, f"{H}/IMG_2673.mov",      0.40,  0.1,  "hlg", C_NONE),
    # 4 — cervejaria / CPL Cerva
    (33.0, f"{H}/IMG_2617.mov",      0.30,  0.3,  "hlg", C_NONE),
    (35.6, f"{H}/IMG_2688.mov",      0.50,  0.1,  "hlg", C_NONE),
    (37.2, f"{H}/IMG_2696.mov",      8.50,  0.1,  "hlg", C_NONE),
    (38.8, f"{H}/IMG_2698.mov",      0.50,  0.1,  "hlg", C_NONE),
    (41.4, f"{H}/IMG_2622.mov",      0.30,  0.1,  "hlg", C_NONE),
    # 5 — parceria / linha
    (44.8, f"{H}/IMG_2641.mov",      0.30,  0.3,  "hlg", C_NONE),
    (47.0, f"{H}/IMG_2621.mov",      0.30,  0.1,  "hlg", C_NONE),
    (48.8, f"{H}/IMG_2623.mov",      0.30,  0.1,  "hlg", C_NONE),
    (50.6, f"{H}/IMG_2642.mov",      0.30,  0.1,  "hlg", C_NONE),
    (52.6, f"{H}/IMG_2634.mov",      9.50,  0.1,  "hlg", C_NONE),  # operador (trecho sem o zoom)
    (53.55, f"{H}/IMG_2653.mov",     0.30,  0.1,  "hlg", C_NONE),
    (55.15, f"{H}/IMG_2646.mov",     0.00,  0.1,  "hlg", C_NONE),
    (56.95, f"{H}/IMG_2662.mov",     0.30,  0.1,  "hlg", C_NONE),
    # QUEBRA 2 — a construção do rótulo
    (59.1, f"{H}/PC_zoom.mp4",       0.00,  0.3,  "sdr", C_NONE),  # quadro fixo + zoom-in suave
    (61.5, f"{H}/IMG_2656.mov",      1.40,  0.1,  "hlg", C_NONE),
    (62.3, f"{H}/IMG_2665.mov",      1.20,  0.1,  "hlg", C_NONE),
    # 6 — a revelação / o presente
    (63.2, f"{H}/root_IMG_1184.MOV", 2.00,  0.1,  "hlg", C_NONE),
    (65.0, f"{H}/root_IMG_1185.MOV", 6.50,  0.1,  "hlg", C_NONE),
    (67.0, f"{H}/IMG_2598.mov",      7.50,  0.1,  "hlg", C_NONE),
    (69.2, f"{H}/IMG_2599.mov",      0.30,  0.1,  "hlg", C_NONE),
    (70.5, f"{H}/IMG_2598.mov",      16.00, 0.1,  "hlg", C_NONE),
    # QUEBRA 3 — celebração
    (73.0, f"{H}/IMG_2652.mov",      31.80, 0.1,  "hlg", C_NONE),
    (74.8, f"{H}/IMG_2600.mov",      0.30,  0.1,  "hlg", C_NONE),
    # 7 — Porquê somos a indústria!
    (76.0, f"{R}/paques.mp4",        80.50, 0.3,  "sdr", C_NONE),
    (78.4, f"{R}/simespi2024.mp4",   7.20,  0.3,  "sdr", C_S24),
    (80.6, f"{R}/simespi2026.mp4",   52.00, 0.3,  "sdr", C_S26),
    # 8 — cartela
    (83.0, "CARD", 0.0, 0.5, "card", C_NONE),
]
GAPS = [5.0, 0.3, 2.6, 0.3, 0.3, 4.0, 3.0, 0.4]

def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))
vo_starts, t = [], 0.0
for i in range(8):
    t += GAPS[i]; vo_starts.append(round(t, 3)); t += dur(f"{VO}/a_{i+1}.wav")
vo_end = t
assert vo_end + 1.5 <= END, vo_end

TONEMAP = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,"
           "zscale=t=bt709:m=bt709:r=tv,format=yuv420p,eq=gamma=1.05:saturation=1.03")
SDR = "format=yuv420p,eq=saturation=1.02"

args = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-stats"]
filt, n = [], len(SHOTS)
full = []
for i, (b, f, inp, tr, kind, crop) in enumerate(SHOTS):
    nb = SHOTS[i + 1][0] if i + 1 < n else END
    L = nb - b + tr
    if kind == "card":
        args += ["-loop", "1", "-t", f"{L:.3f}", "-framerate", "30", "-i", f"{G}/card_bg.png"]
    else:
        d = dur(f)
        assert inp + L <= d + 0.05, (f, inp, L, d)
        args += ["-ss", f"{inp:.3f}", "-t", f"{L + 0.1:.3f}", "-i", f]
    full.append((b, f, inp, tr, kind, crop, L))

gfx = {}
for name in ["lt_cpl", "txt_industria", "card_div", "card_simespi", "card_35", "card_dama"]:
    gfx[name] = n + len(gfx)
    args += ["-loop", "1", "-framerate", "30", "-t", f"{END + 2}", "-i", f"{G}/{name}.png"]
a0 = n + len(gfx)
for i in range(8):
    args += ["-i", f"{VO}/a_{i+1}.wav"]
args += ["-i", f"{S}/music4.wav"]
mus = a0 + 8

for i, (b, f, inp, tr, kind, crop, L) in enumerate(full):
    if kind == "card":
        filt.append(
            f"[{i}:v]format=rgba,fps=30,setsar=1[cb];"
            f"[{gfx['card_div']}:v]format=rgba,fade=in:st=0.2:d=0.5:alpha=1[d0];"
            f"[{gfx['card_simespi']}:v]format=rgba,fade=in:st=0.35:d=0.6:alpha=1[d1];"
            f"[{gfx['card_35']}:v]format=rgba,fade=in:st=0.7:d=0.6:alpha=1[d2];"
            f"[{gfx['card_dama']}:v]format=rgba,fade=in:st=1.05:d=0.6:alpha=1[d3];"
            f"[cb][d0]overlay=shortest=1[c1];[c1][d1]overlay=shortest=1[c2];[c2][d2]overlay=shortest=1[c3];"
            f"[c3][d3]overlay=shortest=1,trim=duration={L:.3f},fade=out:st={L-0.6:.3f}:d=0.6:color=white,"
            f"format=yuv420p,setpts=PTS-STARTPTS,settb=1/30[v{i}]")
    else:
        pre = TONEMAP if kind == "hlg" else SDR
        cr = f"{crop}," if crop else ""
        filt.append(f"[{i}:v]{pre},{cr}scale=1920:1080:flags=lanczos,fps=30,setsar=1,"
                    f"trim=duration={L:.3f},setpts=PTS-STARTPTS,settb=1/30[v{i}]")
prev = "v0"
for i in range(1, n):
    b, f, inp, tr, kind, crop, L = full[i]
    filt.append(f"[{prev}][v{i}]xfade=transition=fade:duration={tr:.3f}:offset={b - tr:.3f}[x{i}]")
    prev = f"x{i}"

def ov(src, name, t0, t1, fi=0.5, fo=0.5):
    k = gfx[name]
    filt.append(f"[{k}:v]format=rgba,trim=duration={t1:.2f},fade=in:st={t0:.2f}:d={fi}:alpha=1,"
                f"fade=out:st={t1 - fo:.2f}:d={fo}:alpha=1,setpts=PTS-STARTPTS[g_{name}]")
    filt.append(f"[{src}][g_{name}]overlay=eof_action=pass:enable='between(t,{t0},{t1})'[o_{name}]")
    return f"o_{name}"
v = ov(prev, "lt_cpl", 38.0, 43.0)
v = ov(v, "txt_industria", vo_starts[6] + 0.1, vo_starts[6] + 5.4, 0.6, 0.6)
filt.append(f"[{v}]trim=duration={END},format=yuv420p[vout]")

lbl = []
for i in range(8):
    d = int(vo_starts[i] * 1000)
    filt.append(f"[{a0+i}:a]aresample=48000,aformat=channel_layouts=mono,adelay={d}|{d}[vo{i}]")
    lbl.append(f"[vo{i}]")
filt.append(f"{''.join(lbl)}amix=inputs=8:normalize=0,"
            f"highpass=f=75,equalizer=f=200:t=q:w=1.2:g=1.5,equalizer=f=3500:t=q:w=1.5:g=1.2,"
            f"acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2,"
            f"apad=whole_dur={END},aformat=channel_layouts=stereo,asplit=2[vomix][vosc]")
filt.append(f"[{mus}:a]atrim=duration={END},volume=-9dB,afade=t=out:st={END-2.0}:d=2.0[mus0]")
filt.append(f"[mus0][vosc]sidechaincompress=threshold=0.02:ratio=5:attack=60:release=700:makeup=1[musd]")
filt.append(f"[vomix][musd]amix=inputs=2:normalize=0,volume=GAINdB,alimiter=limit=0.84:attack=5:release=80:level=0,"
            f"atrim=duration={END},afade=t=out:st={END-0.8}:d=0.8,aresample=48000[aout]")

GAIN = os.environ.get("GAIN", "0")
filt = [x.replace("GAINdB", f"{GAIN}dB") for x in filt]
fc = f"{S}/filter4.txt"
open(fc, "w").write(";\n".join(filt))
args += ["-filter_complex_script", fc, "-map", "[vout]", "-map", "[aout]",
         "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-profile:v", "high", "-pix_fmt", "yuv420p",
         "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
         "-r", "30", "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-movflags", "+faststart",
         "-t", f"{END}", OUT]
json.dump(dict(vo_starts=vo_starts, vo_end=vo_end,
               shots=[(s[0], os.path.basename(s[1]), s[2], s[6]) for s in full]),
          open(f"{S}/timeline4.json", "w"), indent=1)
print("VO starts:", vo_starts, "VO end:", round(vo_end, 2))
if "--dry" in sys.argv: sys.exit()
subprocess.run(args, check=True)
print("done", OUT)
