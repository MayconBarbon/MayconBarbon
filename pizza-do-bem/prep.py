#!/usr/bin/env python3
"""Pizza do Bem 2018-2025 - classificação e tratamento das fotografias.

Uso: python3 prep.py <pasta_origem> <pasta_trabalho>

1. Classifica cada foto pelo ano (EXIF DateTimeOriginal), com exceções
   conferidas visualmente pelo uniforme (ver MANUAL_YEAR).
2. Remove bordas pretas artificiais.
3. Corrige exposição/contraste/temperatura de forma suave (mesma curva nos
   3 canais + balanço de branco parcial) para preservar as cores dos uniformes.
4. Detecta rostos (YuNet) e escolhe o recorte 16:9 que mantém todos os rostos
   dentro da área segura do zoom de 5%. Se não for possível sem cortar rostos
   (ou a foto for vertical), usa a foto inteira sobre fundo desfocado dela mesma.
5. Grava placas 2400x1350 (16:9) + manifest.json.
"""
import json, os, sys, shutil
import numpy as np
from PIL import Image, ImageOps, ImageFilter
import cv2

SRC, WORK = sys.argv[1], sys.argv[2]
MODEL = os.environ.get("YUNET", os.path.join(os.path.dirname(__file__), "yunet.onnx"))
PW, PH = 2400, 1350           # placa 16:9 (folga para zoom 105% em 1920x1080)
SAFE = 0.04                   # margem segura (zoom de 5% corta 2,4% por lado)

# Referências de uniforme enviadas pelo cliente: não entram no vídeo.
REFERENCE_PREFIX = "WhatsApp Image"
# Duplicata exata (cmp idêntico) de "Cópia de DSC_8321.JPG".
DUPLICATES = {"DSC_8321.JPG"}
# Fotos sem EXIF, conferidas visualmente: camiseta verde "Pizza do Bem 10 anos",
# mesma câmera/resolução (6240x4160) e sequência numérica do lote 2023.
MANUAL_YEAR = {"Cópia de IMG_0769.jpg": 2023, "Cópia de IMG_1319.jpg": 2023}

det = cv2.FaceDetectorYN.create(MODEL, "", (320, 320), 0.75, 0.3, 5000)


def exif_info(im):
    e = im.getexif(); ex = e.get_ifd(0x8769)
    d = ex.get(36867) or e.get(306) or ""
    return d, ((e.get(271) or "") + " " + (e.get(272) or "")).strip()


def trim_black(a):
    """Remove faixas pretas uniformes nas bordas (mín. 3 px)."""
    g = a.mean(axis=2)
    def edge(lines):
        # Borda artificial = faixa praticamente constante (máx <= 8) terminando
        # numa transição brusca. Fundos de palco/tetos escuros têm transição
        # gradual e não são removidos.
        n = 0
        for row in lines:
            if row.max() <= 8: n += 1
            else: break
        if n < 3 or n >= len(lines) - 4:
            return 0
        return n if lines[n:n + 3].mean() > 25 else 0
    t = edge(g); b = edge(g[::-1]); l = edge(g.T); r = edge(g.T[::-1])
    h, w = g.shape
    return a[t:h - b, l:w - r], (t, b, l, r)


def correct(a):
    """Correção suave: níveis comuns aos 3 canais + 40% de balanço de branco."""
    f = a.astype(np.float32)
    lum = f @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    lo, hi = np.percentile(lum, [0.4, 99.6])
    lo = min(lo, 18.0); hi = max(hi, 225.0)          # nunca esticar demais
    f = (f - lo) * (255.0 / (hi - lo))
    # balanço de branco parcial (gray-world limitado) – preserva uniformes
    m = f.reshape(-1, 3).mean(0); gain = m.mean() / np.maximum(m, 1)
    gain = 1 + np.clip(gain - 1, -0.10, 0.10) * 0.4
    f *= gain
    # leve gamma para fotos subexpostas
    mean = (np.clip(f, 0, 255) @ np.array([0.2126, 0.7152, 0.0722])).mean() / 255
    if mean < 0.36:
        gam = np.interp(mean, [0.18, 0.36], [0.82, 1.0])
        f = 255 * (np.clip(f, 0, 255) / 255) ** gam
    # contraste suave em S
    x = np.clip(f, 0, 255) / 255
    x = x + 0.06 * (x - 0.5) * (1 - np.abs(2 * x - 1))
    return (np.clip(x, 0, 1) * 255 + 0.5).astype(np.uint8)


def faces(a):
    h, w = a.shape[:2]; s = 1600 / max(h, w)
    sm = cv2.resize(a, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA)
    bgr = cv2.cvtColor(sm, cv2.COLOR_RGB2BGR)
    det.setInputSize((bgr.shape[1], bgr.shape[0]))
    _, res = det.detect(bgr)
    out = []
    if res is not None:
        for r in res:
            x, y, fw, fh = (r[:4] / s).tolist()
            if fw * fh > (w * h) * 0.00004:          # ignora micro-rostos do fundo
                out.append([x, y - 0.25 * fh, fw, fh * 1.45])  # inclui cabelo/queixo
    return out


def plate_crop(a, fs):
    """Recorte 16:9 preservando rostos. None -> usar fundo desfocado."""
    h, w = a.shape[:2]; ar = 16 / 9
    if abs(w / h / ar - 1) < 0.01:                    # já é 16:9 (Sony 3008x1688)
        return (0, 0, w, h)
    if w / h >= ar:                                   # mais largo: corta laterais
        cw, ch = int(round(h * ar)), h
        axis_len, win = w, cw
        lo_f = [f[0] for f in fs]; hi_f = [f[0] + f[2] for f in fs]
    else:                                             # mais alto: corta topo/base
        if h / w > 1.0:                               # foto vertical
            return None
        cw, ch = w, int(round(w / ar))
        axis_len, win = h, ch
        lo_f = [f[1] for f in fs]; hi_f = [f[1] + f[3] for f in fs]
    if not fs:
        off = (axis_len - win) * (0.5 if axis_len == w else 0.42)
    else:
        m = SAFE * win
        need_lo, need_hi = min(lo_f) - m, max(hi_f) + m
        if need_hi - need_lo > win:
            return None
        c = (need_lo + need_hi) / 2
        pref = (axis_len - win) * (0.5 if axis_len == w else 0.42) + win / 2
        lo_c, hi_c = need_hi - win / 2, need_lo + win / 2   # faixa válida do centro
        c = min(max(pref, lo_c), hi_c)
        off = c - win / 2
    off = int(round(min(max(off, 0), axis_len - win)))
    return (off, 0, off + cw, ch) if axis_len == w else (0, off, cw, off + ch)


def blur_plate(im):
    bg = ImageOps.fit(im, (PW, PH), Image.LANCZOS)
    bg = bg.resize((PW // 8, PH // 8), Image.LANCZOS).filter(ImageFilter.GaussianBlur(6))
    bg = bg.resize((PW, PH), Image.LANCZOS)
    bg = Image.eval(bg, lambda v: int(v * 0.55))
    fg = im.copy(); fg.thumbnail((int(PW * 0.94), int(PH * 0.94)), Image.LANCZOS)
    bg.paste(fg, ((PW - fg.width) // 2, (PH - fg.height) // 2))
    return bg


def main():
    plates = os.path.join(WORK, "plates"); os.makedirs(plates, exist_ok=True)
    man = []
    for fn in sorted(os.listdir(SRC)):
        p = os.path.join(SRC, fn)
        im = Image.open(p); date, cam = exif_info(im)
        rec = {"file": fn, "exif_date": date, "camera": cam}
        if fn.startswith(REFERENCE_PREFIX):
            rec.update(year=None, status="referencia_uniforme"); man.append(rec); continue
        if fn in DUPLICATES:
            rec.update(year=None, status="duplicata"); man.append(rec); continue
        if fn in MANUAL_YEAR:
            year, how = MANUAL_YEAR[fn], "visual (uniforme verde 10 anos) + sequência/câmera"
        elif date[:4].isdigit():
            year, how = int(date[:4]), "EXIF"
        else:
            rec.update(year=None, status="nao_confirmada"); man.append(rec); continue
        im = ImageOps.exif_transpose(im).convert("RGB")
        a, borders = trim_black(np.asarray(im))
        a = correct(a)
        fs = faces(a)
        box = plate_crop(a, fs)
        img = Image.fromarray(a)
        if box is None:
            out = blur_plate(img); mode = "fundo_desfocado"
            fcen = (0.5, 0.5)
        else:
            out = img.crop(box).resize((PW, PH), Image.LANCZOS); mode = "recorte_16x9"
            if fs:
                sx = PW / (box[2] - box[0]); sy = PH / (box[3] - box[1])
                xs = [(f[0] + f[2] / 2 - box[0]) * sx / PW for f in fs]
                ys = [(f[1] + f[3] / 2 - box[1]) * sy / PH for f in fs]
                fcen = (float(np.mean(xs)), float(np.mean(ys)))
            else:
                fcen = (0.5, 0.5)
        name = f"{year}_{os.path.splitext(fn)[0].replace(' ', '_')}.jpg"
        out.save(os.path.join(plates, name), quality=96, subsampling=0)
        rec.update(year=year, status="ok", method=how, plate=name, mode=mode,
                   faces=len(fs), borders_removed=borders, focus=fcen,
                   size=list(im.size))
        man.append(rec); print(year, mode, len(fs), borders, fn, flush=True)
    json.dump(man, open(os.path.join(WORK, "manifest.json"), "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
