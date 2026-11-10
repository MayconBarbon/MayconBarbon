"""Gera os grafismos: lower-third CPL Cerva, frase 'Porque somos a indústria!' e camadas da cartela final."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = os.path.dirname(os.path.abspath(__file__))
B, F, O = f"{S}/brand", f"{S}/fonts", f"{S}/gfx"
os.makedirs(O, exist_ok=True)
W, H = 1920, 1080
# Paleta oficial (manual SIMESPI)
AZUL_CLARO = (59, 185, 216)   # #3bb9d8
AZUL_MEDIO = (39, 110, 132)   # #276e84
AZUL_ESC = (10, 54, 67)       # #0a3643

def font(w, s): return ImageFont.truetype(f"{F}/Montserrat-{w}.ttf", s)

def gradient(height, max_alpha, top=False):
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = g.load()
    for y in range(H):
        d = (y - (H - height)) / height if not top else (height - y) / height
        if 0 <= d <= 1:
            a = int(max_alpha * (d ** 1.6))
            for x in range(W):
                px[x, y] = (AZUL_ESC[0] // 3, AZUL_ESC[1] // 3, AZUL_ESC[2] // 3, a)
    return g

def soft_text(img, xy, text, f, fill, anchor="la", shadow=110):
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((xy[0], xy[1] + 2), text, font=f, fill=(0, 0, 0, shadow), anchor=anchor)
    sh = sh.filter(ImageFilter.GaussianBlur(6))
    img.alpha_composite(sh)
    ImageDraw.Draw(img).text(xy, text, font=f, fill=fill, anchor=anchor)

# 1) Lower-third CPL Cerva
g = gradient(380, 150)
x, y = 130, 868
d = ImageDraw.Draw(g)
d.rectangle((x, y - 24, x + 64, y - 20), fill=AZUL_CLARO + (255,))
soft_text(g, (x, y), "CPL Cerva", font("SemiBold", 52), (255, 255, 255, 255))
soft_text(g, (x + 2, y + 70), "Projeto do SIMESPI", font("Light", 30), (255, 255, 255, 235))
g.save(f"{O}/lt_cpl.png")

# 2) Frase de assinatura
g = gradient(420, 165)
fnt = font("SemiBold", 66)
soft_text(g, (W // 2, 905), "Porque somos a indústria!", fnt, (255, 255, 255, 255), anchor="mm", shadow=130)
d = ImageDraw.Draw(g)
d.rectangle((W // 2 - 36, 958, W // 2 + 36, 962), fill=AZUL_CLARO + (255,))
g.save(f"{O}/txt_industria.png")

# 3) Cartela final: fundo branco + 3 logos oficiais (sem alteração de cor/proporção)
bg = Image.new("RGB", (W, H), (255, 255, 255))
bg.save(f"{O}/card_bg.png")

def fit(path, h):
    im = Image.open(path).convert("RGBA")
    im = im.crop(im.getbbox())
    w = round(im.width * h / im.height)
    return im.resize((w, h), Image.LANCZOS)

simespi = fit(f"{B}/simespi_small_crop.png", 168)
l35 = fit(f"{B}/logo35_crop.png", 270)
dama = fit(f"{B}/Logo_Dama_Horizontal_t_crop.png", 172)
gap = 120
total = simespi.width + l35.width + dama.width + 2 * gap
x0 = (W - total) // 2
cy = H // 2 - 10
pos = []
xx = x0
for im in (simespi, l35, dama):
    pos.append((xx, cy - im.height // 2)); xx += im.width + gap
for name, im, p in zip(("card_simespi", "card_35", "card_dama"), (simespi, l35, dama), pos):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); layer.alpha_composite(im, p); layer.save(f"{O}/{name}.png")
# divisórias finas
div = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(div)
for i in range(2):
    xd = pos[i + 1][0] - gap // 2
    d.rectangle((xd, cy - 95, xd + 1, cy + 95), fill=(200, 210, 216, 255))
div.save(f"{O}/card_div.png")
prev = bg.convert("RGBA")
for n in ("card_div", "card_simespi", "card_35", "card_dama"):
    prev.alpha_composite(Image.open(f"{O}/{n}.png"))
prev.convert("RGB").save(f"{O}/card_preview.png")
print("ok", pos, simespi.size, l35.size, dama.size)
