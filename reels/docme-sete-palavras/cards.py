"""Prepare WhatsApp print cards: crop, neutralise search highlight, blur name, orange highlight on key words."""
from PIL import Image, ImageFilter, ImageDraw
import pickle
S = "/tmp/claude-0/-home-user-MayconBarbon/14558cd3-e9d2-53c0-bc97-8331b175cad2/scratchpad"
P = S + "/prints"
ORANGE = (233, 87, 13)
# (file, crop box or None, [highlight boxes in cropped coords], [blur boxes])
SPEC = [
    ("p5.jpg", (0, 0, 920, 386), [(80, 72, 252, 140), (296, 72, 446, 140), (252, 162, 424, 225), (80, 297, 215, 360)], []),
    ("p3.jpg", (0, 0, 905, 224), [(550, 2, 800, 68), (205, 72, 378, 138)], []),
    ("p1.jpg", (40, 0, 845, 207), [(440, 82, 622, 148), (655, 82, 775, 148)], []),
    ("p4.jpg", (40, 335, 910, 968), [(325, 108, 470, 168), (310, 250, 490, 305), (245, 393, 425, 450)], []),
    ("p2c.png", (0, 15, 870, 290), [(50, 175, 235, 240)], []),
    ("p6.jpg", (40, 0, 860, 427), [], [(40, 110, 260, 180)]),
]
cards = []
for f, crop, hls, blurs in SPEC:
    im = Image.open(f"{P}/{f}").convert("RGB")
    if crop: im = im.crop(crop)
    px = im.load()
    for y in range(im.height):            # neutralise WhatsApp's beige search highlight
        for x in range(im.width):
            r, g, b = px[x, y]
            if r > 110 and r - b > 45 and g > 70 and r < 200:
                lum = (r + g + b) / 3
                px[x, y] = (54, 54, 56) if lum < 150 else (r, g, b)
    for bx in blurs:
        reg = im.crop(bx).filter(ImageFilter.GaussianBlur(14)); im.paste(reg, bx[:2])
    hl = im.copy()
    for bx in hls:
        reg = im.crop(bx); L = reg.convert("L")
        mask = L.point(lambda v: 255 if v > 165 else (0 if v < 110 else int((v - 110) * 255 / 55)))
        base = Image.new("RGB", reg.size, ORANGE); base.paste(Image.new("RGB", reg.size, (255, 255, 255)), (0, 0), mask)
        hl.paste(base, bx[:2])
    cards.append((im, hl, hls))
pickle.dump([(a.tobytes(), a.size, b.tobytes(), h) for a, b, h in cards], open(S + "/work/cards.pkl", "wb"))
prev = Image.new("RGB", (900, sum(c[1].height for c in cards) + 10 * len(cards)), "white"); y = 0
for a, b, h in cards: prev.paste(b, (0, y)); y += b.height + 10
prev.save(S + "/work/cards_prev.jpg"); print("ok")
