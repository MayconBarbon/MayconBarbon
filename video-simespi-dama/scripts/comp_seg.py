"""Rerenderiza só o trecho do brinde (41,96–46,35 s) da v9 de lançamento, com as taças do brinde (logos SIMESPI e 35)."""
import os, sys, json, subprocess
S = os.path.dirname(os.path.abspath(__file__))
sys.argv = ['comp.py', '--x']
g = {'__file__': f"{S}/comp.py", '__name__': 'x'}
exec(open(f"{S}/comp.py").read().replace('if __name__ == "__main__":\n    main()', ''), g)
F_ = g['F_']; SEQ = g['SEQ']
i0 = next(i for i, x in enumerate(SEQ) if x[0] == "full" and x[2][0] == "IMG_2600")
i1 = next(i for i, x in enumerate(SEQ) if x[0] == "hero")
assert sum(x[1] for x in SEQ[i0:i1]) == 9
NEW = [   # brinde em câmera lenta 0,5x (BRS_* = G_* com setpts 2x + minterpolate)
    ("tri", 4, [F_("BRS_2808", 1.82), F_("BRS_2806", 2.20), F_("BRS_2805", 2.34)], "flash"),   # tilintar 0,4 s após o corte
    ("tri", 3, [F_("BRS_2806", 3.60), F_("BRS_2808", 3.20), F_("BRS_2805", 4.40)], "cut"),
    ("tri", 2, [F_("BRS_2805", 5.60), F_("BRS_2806", 4.40), F_("BRS_2808", 4.80)], "cut"),
]
SEQ[i0:i1] = NEW
g['V'] = f"{S}/v_br"  # src_path procura BR_* aqui
tl, kend = g['build_timeline']()
texts = json.load(open(f"{S}/n/texts.json"))
TX = [g['Text'](**{**x, 'lines': [[(w, tuple(c)) for w, c in ln] for ln in x['lines']], 'pos': tuple(x['pos'])}) for x in texts]
FPS, W, PW = g['FPS'], g['W'], g['PW']
rows = [r for r in tl if r[2] == "tri" and isinstance(r[4], list) and r[4][0][0].startswith("BR")]
F0 = int(round(rows[0][0] * FPS)); F1 = int(round(rows[-1][1] * FPS))
out = sys.argv_out if hasattr(sys, 'argv_out') else f"{S}/out/brinde_seg.mp4"
enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{g['HH']}", "-r", str(FPS), "-i", "-",
                        "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", out],
                       stdin=subprocess.PIPE)
idxs = [tl.index(r) for r in rows]
for idx in idxs:
    t0, t1, kind, nb, content, trans = tl[idx]
    f0, f1 = int(round(t0 * FPS)), int(round(t1 * FPS)); n = f1 - f0
    nxt = idx + 1 < len(tl) and tl[idx + 1][5] == "whip"
    frs = g['render'](kind, content, n, trans, nxt, W)
    overl = any(a < t1 and b > t0 for a, b in g['panel_windows'](TX))
    alt = g['render'](kind, content, n, trans, nxt, W - PW) if overl else None
    for i, fr in enumerate(frs):
        fr = g['compose_panel'](fr, TX, (f0 + i) / FPS, alt[i] if alt is not None else None)
        enc.stdin.write(fr.tobytes())
enc.stdin.close(); enc.wait()
json.dump({"F0": F0, "F1": F1, "clink": rows[0][0] + 0.40}, open(f"{S}/out/brinde_seg.json", "w"))
print("ok", F0, F1, F0 / FPS, F1 / FPS)
