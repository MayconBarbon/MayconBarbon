"""SIMESPI — Locação de salas. Renderizador de quadros (PIL) -> ffmpeg.
Uso: python render.py main|ad|cover|stills OUT
"""
import sys, os, subprocess, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

ROOT = os.path.dirname(os.path.abspath(__file__)) + '/..'
SRC = ROOT + '/src'
W, H, FPS = 1080, 1920, 30

# Paleta (manual de marca 2017 + site simespi.com.br)
NAVY = (8, 54, 66)        # #083642  azul-petróleo escuro (site / manual 85-40-35-70)
BLUE = (39, 110, 133)     # #276E85  azul institucional (site / manual 80-40-30-20)
CYAN = (91, 194, 214)     # #5BC2D6  azul claro do manual (65-5-15-0) — destaque
WHITE = (255, 255, 255)
INK = (19, 21, 21)        # #131515

FONT = {w: ROOT + f'/fonts/Montserrat-{w}.ttf' for w in (300, 500, 600, 700, 800)}
_fc = {}
def font(w, s):
    k = (w, s)
    if k not in _fc: _fc[k] = ImageFont.truetype(FONT[w], s)
    return _fc[k]

def ease(p):            # easeOutCubic
    p = min(max(p, 0.0), 1.0); return 1 - (1 - p) ** 3
def ease_io(p):
    p = min(max(p, 0.0), 1.0); return 3 * p * p - 2 * p * p * p

# ---------------------------------------------------------------- texto
_tc = {}
def text_img(text, w, s, fill, track=0.0):
    """Linha de texto em RGBA com tracking (em fração do corpo)."""
    k = (text, w, s, fill, track)
    if k in _tc: return _tc[k]
    f = font(w, s)
    asc, desc = f.getmetrics()
    sp = track * s
    widths = [f.getlength(ch) for ch in text]
    tw = int(sum(widths) + sp * max(len(text) - 1, 0)) + 8
    im = Image.new('RGBA', (tw, asc + desc + 6), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x = 2
    if track == 0:
        d.text((2, 2), text, font=f, fill=fill)
    else:
        for ch, cw in zip(text, widths):
            d.text((x, 2), ch, font=f, fill=fill); x += cw + sp
    bb = im.getbbox() or (0, 0, 1, 1)
    im = im.crop((0, 0, max(bb[2] + 2, 1), im.height))
    _tc[k] = im
    return im

class Text:
    """Linha com revelação por máscara (sobe dentro da própria caixa) e saída em fade."""
    def __init__(self, text, w, s, fill, x, y, t0, t1, track=0.0, dur=0.55, align='left', delay=0.0, out=0.3):
        self.im = text_img(text, w, s, fill, track)
        self.x = x if align == 'left' else (W - self.im.width) // 2 if align == 'center' else x - self.im.width
        self.y, self.t0, self.t1, self.dur, self.out = y, t0 + delay, t1, dur, out
    def draw(self, fr, t):
        if t < self.t0 or t > self.t1: return
        p = ease((t - self.t0) / self.dur)
        a = 1.0
        if self.t1 - t < self.out: a = max(0.0, (self.t1 - t) / self.out)
        h = self.im.height
        dy = int(round((1 - p) * h))
        if h - dy <= 0: return
        part = self.im.crop((0, 0, self.im.width, h - dy))
        if a < 1:
            al = part.getchannel('A').point(lambda v: int(v * a)); part = part.copy(); part.putalpha(al)
        fr.alpha_composite(part, (self.x, self.y + dy))

class Bar:
    """Fio de destaque que cresce da esquerda."""
    def __init__(self, x, y, w, h, color, t0, t1, dur=0.6, out=0.3, align='left'):
        self.x, self.y, self.w, self.h, self.c, self.t0, self.t1, self.dur, self.out, self.align = x, y, w, h, color, t0, t1, dur, out, align
    def draw(self, fr, t):
        if t < self.t0 or t > self.t1: return
        p = ease((t - self.t0) / self.dur); a = 1.0
        if self.t1 - t < self.out: a = max(0.0, (self.t1 - t) / self.out)
        ww = int(self.w * p)
        if ww < 1: return
        x = self.x if self.align == 'left' else (W - ww) // 2
        layer = Image.new('RGBA', (ww, self.h), self.c + (int(255 * a),))
        fr.alpha_composite(layer, (x, self.y))

class Chip:
    """Etiqueta com contorno (aparece com fade + leve subida)."""
    def __init__(self, text, x, y, t0, t1, fg=WHITE, border=CYAN, bg=None, s=30, w=600, pad=(26, 14), align='left'):
        ti = text_img(text, w, s, fg, 0.08)
        cw, ch = ti.width + pad[0] * 2, ti.height + pad[1] * 2 - 6
        im = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((0, 0, cw - 1, ch - 1), radius=ch // 2, fill=(bg + (235,)) if bg else (8, 54, 66, 150),
                            outline=border + (255,) if border else None, width=3)
        im.alpha_composite(ti, (pad[0], pad[1] - 4))
        self.im, self.y, self.t0, self.t1 = im, y, t0, t1
        self.x = x if align == 'left' else (W - cw) // 2
    def draw(self, fr, t):
        if t < self.t0 or t > self.t1: return
        p = ease((t - self.t0) / 0.45); a = p
        if self.t1 - t < 0.3: a = min(a, (self.t1 - t) / 0.3)
        im = self.im
        if a < 1:
            im = im.copy(); im.putalpha(im.getchannel('A').point(lambda v: int(v * a)))
        fr.alpha_composite(im, (self.x, self.y + int((1 - p) * 18)))

class Img:
    """Imagem RGBA estática (logo) com fade + leve subida."""
    def __init__(self, im, x, y, t0, t1, rise=16, fade=0.6, out=0.0):
        self.im, self.x, self.y, self.t0, self.t1, self.rise, self.fade, self.out = im, x, y, t0, t1, rise, fade, out
    def draw(self, fr, t):
        if t < self.t0 or t > self.t1: return
        p = ease((t - self.t0) / self.fade) if self.fade > 0 else 1; a = p
        if self.out and self.t1 - t < self.out: a = min(a, (self.t1 - t) / self.out)
        im = self.im
        if a < 1:
            im = im.copy(); im.putalpha(im.getchannel('A').point(lambda v: int(v * a)))
        fr.alpha_composite(im, (self.x, self.y + int((1 - p) * self.rise)))

# ---------------------------------------------------------------- fotos
_src = {}
def photo(name):
    if name not in _src:
        _src[name] = ImageOps.exif_transpose(Image.open(f'{SRC}/{name}.jpg')).convert('RGB')
    return _src[name]

class Shot:
    """Recorte 9:16 de uma fotografia real com movimento de câmera (push-in / pan).
    Keyframes: zoom z0->z1; ponto focal f0->f1 (normalizado na foto) posicionado em p0->p1 (normalizado no quadro).
    Nada é acrescentado à imagem: só enquadramento e movimento."""
    def __init__(self, name, t0, t1, cx=0.5, cy=0.5, zoom=1.0, s0=1.0, s1=1.025, marks=None,
                 z=None, f=None, f1=None, p=(0.5, 0.5), p1=None):
        if z is None:
            z = (zoom * s0, zoom * s1); f = (cx, cy); p = (0.5, 0.5)
        self.z0, self.z1 = z
        self.f0 = f; self.f1 = f1 or f; self.p0 = p; self.p1 = p1 or p
        self.t0, self.t1, self.name = t0, t1, name
        self.marks = marks or []
        self.src = photo(name)
    def box_at(self, t):
        q = ease_io((t - self.t0) / max(self.t1 - self.t0, 1e-6))
        L = lambda a, b: a + (b - a) * q
        z = self.z0 * (self.z1 / self.z0) ** q
        fx, fy = L(self.f0[0], self.f1[0]), L(self.f0[1], self.f1[1])
        px, py = L(self.p0[0], self.p1[0]), L(self.p0[1], self.p1[1])
        sw, sh = self.src.size
        ch = sh / z; cw = ch * 9 / 16
        if cw > sw: cw = sw; ch = cw * 16 / 9
        x0 = min(max(fx * sw - px * cw, 0), sw - cw); y0 = min(max(fy * sh - py * ch, 0), sh - ch)
        return x0, y0, cw, ch
    def render(self, t):
        x0, y0, cw, ch = self.box = self.box_at(t)
        return self.src.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch)).convert('RGBA')
    def map_pt(self, nx, ny):
        sw, sh = self.src.size; x0, y0, cw, ch = self.box
        return ((nx * sw - x0) / cw * W, (ny * sh - y0) / ch * H)

class Stack:
    """Duas fotografias inteiras (sem recorte agressivo) empilhadas sobre fundo azul institucional."""
    def __init__(self, a, b, t0, t1):
        self.t0, self.t1 = t0, t1
        self.a = photo(a).resize((W, int(W * photo(a).size[1] / photo(a).size[0])), Image.LANCZOS)
        self.b = photo(b).resize((W, int(W * photo(b).size[1] / photo(b).size[0])), Image.LANCZOS)
        self.ya, self.yb = 300, 300 + self.a.height + 14
    def render(self, t):
        fr = Image.new('RGBA', (W, H), NAVY + (255,))
        for k, (im, y) in enumerate(((self.a, self.ya), (self.b, self.yb))):
            p = ease((t - self.t0 - 0.22 * k) / 0.7)
            ww = int(W * p)
            if ww > 0:
                fr.paste(im.crop((0, 0, ww, im.height)), (0, y))
                if ww < W:
                    ImageDraw.Draw(fr).rectangle((ww, y, ww + 5, y + im.height - 1), fill=CYAN)
        return fr

class Plain:
    def __init__(self, color, t0, t1): self.c, self.t0, self.t1 = color, t0, t1
    def render(self, t): return Image.new('RGBA', (W, H), self.c + (255,))

# ---------------------------------------------------------------- sobreposições
def grad(h0, h1, a0, a1, color=NAVY, vertical=True):
    """Gradiente full-frame entre as linhas h0..h1 (alfa a0->a1); fora do intervalo mantém o extremo."""
    if vertical:
        y = np.arange(H, dtype=np.float32)
        p = np.clip((y - h0) / (h1 - h0), 0, 1); p = p * p * (3 - 2 * p)
        a = (a0 + (a1 - a0) * p)[:, None] * np.ones((1, W), np.float32)
    else:
        x = np.arange(W, dtype=np.float32)
        p = np.clip((x - h0) / (h1 - h0), 0, 1); p = p * p * (3 - 2 * p)
        a = np.ones((H, 1), np.float32) * (a0 + (a1 - a0) * p)[None, :]
    arr = np.zeros((H, W, 4), np.uint8); arr[..., :3] = color; arr[..., 3] = (a * 255).astype(np.uint8)
    return Image.fromarray(arr, 'RGBA')

G_BOTTOM = None; G_TOP = None; G_LEFT = None
def init_grads():
    global G_BOTTOM, G_TOP, G_LEFT
    G_BOTTOM = grad(940, 1600, 0.0, 0.84)
    G_TOP = grad(0, 520, 0.78, 0.0)
    G_LEFT = grad(0, 1000, 0.62, 0.0, vertical=False)

def brackets(fr, shot, box, t_in, t, color=CYAN):
    """Cantoneiras que enquadram a tela existente na foto (não altera o conteúdo da tela)."""
    if t < t_in: return
    p = ease((t - t_in) / 0.6)
    (x0, y0) = shot.map_pt(box[0], box[1]); (x1, y1) = shot.map_pt(box[2], box[3])
    pad = 18; x0 -= pad; y0 -= pad; x1 += pad; y1 += pad
    L = max(36, min(x1 - x0, y1 - y0) * 0.22) * p
    d = ImageDraw.Draw(fr); w = 6
    for (cx, cy, sx, sy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        d.line((cx, cy, cx + sx * L, cy), fill=color, width=w)
        d.line((cx, cy, cx, cy + sy * L), fill=color, width=w)
    # pulso discreto do contorno
    q = (t - t_in - 0.6)
    if 0 < q < 1.0:
        a = int(110 * (1 - q))
        ov = Image.new('RGBA', fr.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        od.rectangle((x0, y0, x1, y1), outline=CYAN + (a,), width=3)
        fr.alpha_composite(ov)

def wipe(fr, t, tc, dur=0.5):
    """Transição gráfica: faixa azul institucional sobe e corta no ponto médio."""
    p = (t - (tc - dur / 2)) / dur
    if p <= 0 or p >= 1: return
    d = ImageDraw.Draw(fr)
    if p < 0.5:
        q = ease_io(p * 2); top = int(H * (1 - q))
        d.rectangle((0, top, W, H), fill=NAVY); d.rectangle((0, top, W, top + 8), fill=CYAN)
    else:
        q = ease_io((p - 0.5) * 2); bot = int(H * (1 - q))
        d.rectangle((0, 0, W, bot), fill=NAVY); d.rectangle((0, bot - 8, W, bot), fill=CYAN)

# ---------------------------------------------------------------- logos
def logo(kind, width):
    im = Image.open(f'{ROOT}/logo/logo_{kind}.png')
    return im.resize((width, int(im.height * width / im.width)), Image.LANCZOS)

# ---------------------------------------------------------------- telas (coord. normalizadas na foto original)
SCREEN_9837 = (0.398, 0.411, 0.542, 0.539)
SCREEN_8151 = (0.470, 0.191, 0.652, 0.340)
TV37 = (0.470, 0.475); TV51 = (0.561, 0.2655); TV25 = (0.92, 0.29)

def scene_end(t0, t1, phone_t=None):
    """Assinatura final: logotipo original (versão colorida positiva) sobre fundo branco."""
    L = logo('pos', 760)
    ly = 560
    els = [
        Img(L, (W - L.width) // 2, ly, t0 + 0.15, t1 + 1, rise=14, fade=0.8),
        Bar(0, ly + L.height + 70, 140, 6, CYAN, t0 + 0.55, t1 + 1, align='center'),
        Text('SALAS PARA LOCAÇÃO', 600, 40, NAVY, 0, ly + L.height + 120, t0 + 0.6, t1 + 1, track=0.18, align='center'),
        Text('(19) 3417-8600', 800, 84, NAVY, 0, ly + L.height + 190, t0 + 0.8, t1 + 1, align='center'),
        Text('CONSULTE A DISPONIBILIDADE', 500, 34, BLUE, 0, ly + L.height + 310, t0 + 1.0, t1 + 1, track=0.16, align='center'),
    ]
    return els

def build(mode):
    init_grads()
    shots, els, fx = [], [], []
    WM = logo('neg', 230)          # assinatura discreta no topo
    PL = logo('neg', 340)          # logo no painel da chamada final
    if mode == 'main':
        T = 39.0
        # 1) IMPACTO 0–5.4
        shots += [Shot('S1_9837', 0, 5.4, z=(1.0, 1.6), f=TV37, p=(0.5, 0.47), p1=(0.5, 0.36))]
        els += [
            Bar(72, 1088, 120, 8, CYAN, 0.3, 5.2),
            Text('VOCÊ TEM O', 800, 92, WHITE, 72, 1120, 0.45, 5.2),
            Text('CONHECIMENTO.', 800, 92, WHITE, 72, 1222, 0.6, 5.2),
            Text('NÓS TEMOS', 800, 92, WHITE, 72, 1352, 2.6, 5.2),
            Text('O ESPAÇO.', 800, 92, CYAN, 72, 1454, 2.75, 5.2),
        ]
        # 2) APRESENTAÇÃO 5.4–12.0
        shots += [Shot('S2_8138', 5.4, 7.8, z=(1.06, 1.12), f=(0.44, 0.5), f1=(0.56, 0.5)), Stack('S1_9832', 'S2_8149', 7.8, 12.0)]
        els += [
            Chip('SIMESPI · PIRACICABA-SP', 72, 1110, 5.55, 7.8, bg=BLUE, border=None, s=28, w=700),
            Text('SALAS PARA', 800, 96, WHITE, 72, 1200, 5.6, 7.8),
            Text('LOCAÇÃO', 800, 96, WHITE, 72, 1306, 5.72, 7.8),
            Text('EM PIRACICABA', 800, 96, CYAN, 72, 1412, 5.84, 7.8),
            # tela empilhada: as duas salas reais
            Text('SUAS IDEIAS ENCONTRAM', 800, 56, WHITE, 72, 120, 8.0, 12.0),
            Text('ESTRUTURA PARA ACONTECER.', 800, 56, CYAN, 72, 186, 8.12, 12.0),
        ]
        # 3) TECNOLOGIA 12.0–21.0
        s3a = Shot('S2_8151', 12.0, 14.4, z=(1.05, 1.75), f=TV51, p=(0.5, 0.32), p1=(0.5, 0.34))
        s3b = Shot('S1_9825', 14.4, 17.4, z=(1.1, 1.35), f=TV25, p=(0.62, 0.42), p1=(0.72, 0.36))
        s3c = Shot('S1_9837', 17.4, 21.0, z=(1.9, 2.35), f=TV37, p=(0.5, 0.36), p1=(0.5, 0.34))
        s3a.marks = [(SCREEN_8151, 12.35)]; s3c.marks = [(SCREEN_9837, 17.6)]
        shots += [s3a, s3b, s3c]
        els += [
            Bar(72, 1150, 120, 8, CYAN, 12.2, 14.4),
            Text('TECNOLOGIA QUE', 800, 84, WHITE, 72, 1180, 12.25, 14.4),
            Text('TRANSFORMA', 800, 84, WHITE, 72, 1274, 12.37, 14.4),
            Text('APRESENTAÇÕES', 800, 84, CYAN, 72, 1368, 12.49, 14.4),
            Bar(72, 1150, 120, 8, CYAN, 14.5, 21.0),
            Text('LOUSA INTERATIVA', 800, 84, WHITE, 72, 1180, 14.55, 21.0),
            Text('E CONECTADA', 800, 84, CYAN, 72, 1274, 14.67, 21.0),
            Text('Ambientes modernos e climatizados para', 500, 38, WHITE, 72, 1392, 14.9, 21.0),
            Text('apresentações mais dinâmicas.', 500, 38, WHITE, 72, 1440, 15.0, 21.0),
            Chip('AMBIENTES CLIMATIZADOS', 72, 996, 17.7, 21.0),
            Chip('ESTRUTURA PRONTA', 72, 1070, 17.9, 21.0),
        ]
        # 4) POSSIBILIDADES 21.0–30.0  (cortes no tempo da trilha: 1 palavra por compasso/2)
        cuts = [21.0, 22.8, 24.0, 25.2, 26.4, 27.6, 30.0]
        mk = [lambda a, b: Shot('S2_8151', a, b, z=(1.25, 1.45), f=TV51, p=(0.62, 0.30), p1=(0.66, 0.30)),
              lambda a, b: Shot('S1_9832', a, b, z=(1.04, 1.1), f=(0.42, 0.5), f1=(0.56, 0.5)),
              lambda a, b: Shot('S1_9837', a, b, z=(1.3, 1.5), f=TV37, p=(0.64, 0.30), p1=(0.68, 0.30)),
              lambda a, b: Shot('S2_8149', a, b, z=(1.04, 1.1), f=(0.5, 0.5), f1=(0.62, 0.5)),
              lambda a, b: Shot('S1_9825', a, b, z=(1.15, 1.35), f=TV25, p=(0.72, 0.30), p1=(0.78, 0.30)),
              lambda a, b: Shot('S2_8138', a, b, z=(1.06, 1.12), f=(0.44, 0.5), f1=(0.56, 0.5))]
        for m, a, b in zip(mk, cuts[:-1], cuts[1:]):
            shots.append(m(a, b))
        words = ['CURSOS', 'PALESTRAS', 'WORKSHOPS', 'TREINAMENTOS', 'ENCONTROS', 'PROFISSIONAIS']
        wt = [21.6, 22.8, 24.0, 25.2, 26.4, 26.55]
        y = 640
        for i, (wd, t0) in enumerate(zip(words, wt)):
            col = CYAN if i >= 4 else WHITE
            els.append(Text(wd, 800, 84, col, 72, y, t0, 30.0))
            y += 106
        els += [
            Bar(72, 610, 120, 8, CYAN, 21.4, 30.0),
            Text('PARA PROFISSIONAIS, EMPRESAS,', 600, 34, WHITE, 72, 1320, 27.6, 30.0, track=0.04),
            Text('PROFESSORES E ORGANIZADORES.', 600, 34, WHITE, 72, 1366, 27.7, 30.0, track=0.04),
            Chip('ASSOCIADOS OU NÃO', 72, 1430, 27.9, 30.0, bg=BLUE, border=None, s=32, w=700),
        ]
        # 5) CONVERSÃO 30.0–36.0
        shots += [Shot('S1_9837', 30.0, 36.0, z=(1.55, 1.15), f=TV37, p=(0.5, 0.24), p1=(0.5, 0.27))]
        fx.append(('panel', 30.0, 36.0))
        els += [
            Text('SEU PRÓXIMO EVENTO', 800, 74, WHITE, 0, 1090, 30.35, 36.0, align='center'),
            Text('COMEÇA AQUI.', 800, 74, CYAN, 0, 1172, 30.5, 36.0, align='center'),
            Text('Salas para locação no SIMESPI', 500, 40, WHITE, 0, 1278, 30.8, 36.0, align='center'),
            Chip('CONSULTE A DISPONIBILIDADE', 0, 1362, 32.4, 36.0, fg=NAVY, bg=CYAN, border=None, s=34, w=800, pad=(34, 20), align='center'),
            Text('(19) 3417-8600', 800, 72, WHITE, 0, 1476, 32.8, 36.0, align='center'),
            Img(PL, (W - PL.width) // 2, 1610, 33.2, 36.0, rise=12, fade=0.7),
        ]
        # 6) ASSINATURA 36.0–39.0
        shots += [Plain(WHITE, 36.0, T + 1)]
        els += scene_end(36.0, T)
        fx += [('wipe', 12.0), ('wipe', 21.0), ('wipe', 30.0), ('wipe', 36.0)]
        fx.append(('lgrad', 21.0, 30.0))
        wm_spans = [(0, 7.8), (12.0, 30.0)]
    elif mode == 'tour':   # TOUR PELAS SALAS ~29 s
        T = 28.8
        shots += [Shot('S1_9837', 0, 4.2, z=(1.0, 1.5), f=TV37, p=(0.5, 0.47), p1=(0.5, 0.36))]
        els += [
            Chip('SIMESPI · PIRACICABA-SP', 72, 1110, 0.3, 4.2, bg=BLUE, border=None, s=28, w=700),
            Text('CONHEÇA AS', 800, 96, WHITE, 72, 1200, 0.4, 4.2),
            Text('SALAS PARA', 800, 96, WHITE, 72, 1306, 0.52, 4.2),
            Text('LOCAÇÃO', 800, 96, CYAN, 72, 1412, 0.64, 4.2),
        ]
        # SALA 1
        d1 = Shot('S1_9837', 8.7, 10.8, z=(1.9, 2.3), f=TV37, p=(0.5, 0.3), p1=(0.5, 0.3)); d1.marks = [(SCREEN_9837, 8.85)]
        shots += [Shot('S1_9832', 4.2, 6.6, z=(1.04, 1.1), f=(0.42, 0.5), f1=(0.58, 0.5)), Shot('S1_9825', 6.6, 8.7, z=(1.1, 1.35), f=TV25, p=(0.62, 0.30), p1=(0.72, 0.26)), d1]
        els += [
            Text('SALA', 700, 44, WHITE, 72, 1004, 4.35, 10.8, track=0.3),
            Text('01', 800, 150, WHITE, 66, 1050, 4.4, 10.8),
            Chip('AMPLA E ORGANIZADA', 72, 1250, 4.8, 10.8),
            Chip('CLIMATIZADA', 72, 1330, 6.7, 10.8),
            Chip('LOUSA INTERATIVA', 72, 1410, 8.8, 10.8),
        ]
        # SALA 2
        d2 = Shot('S2_8151', 15.3, 17.4, z=(1.2, 1.8), f=TV51, p=(0.5, 0.26), p1=(0.5, 0.26)); d2.marks = [(SCREEN_8151, 15.45)]
        shots += [Shot('S2_8138', 10.8, 13.2, z=(1.06, 1.12), f=(0.44, 0.5), f1=(0.56, 0.5)), Shot('S2_8141', 13.2, 15.3, z=(1.05, 1.12), f=(0.33, 0.5), f1=(0.45, 0.5)), d2]
        els += [
            Text('SALA', 700, 44, WHITE, 72, 1004, 10.95, 17.4, track=0.3),
            Text('02', 800, 150, WHITE, 66, 1050, 11.0, 17.4),
            Chip('MESAS E CADEIRAS PARA TURMAS', 72, 1250, 11.4, 17.4),
            Chip('CLIMATIZADA', 72, 1330, 13.3, 17.4),
            Chip('LOUSA INTERATIVA E CONECTADA', 72, 1410, 15.4, 17.4),
        ]
        # USOS — as duas salas inteiras
        shots += [Stack('S1_9837', 'S2_8149', 17.4, 22.2)]
        els += [
            Text('CURSOS · PALESTRAS', 800, 56, WHITE, 72, 120, 17.6, 22.2),
            Text('TREINAMENTOS', 800, 56, CYAN, 72, 186, 17.75, 22.2),
            Chip('ASSOCIADOS OU NÃO', 72, 1700, 20.0, 22.2, bg=BLUE, border=None, s=34, w=700, pad=(34, 20)),
        ]
        # CONVERSÃO
        shots += [Shot('S2_8151', 22.2, 25.8, z=(1.6, 1.2), f=TV51, p=(0.5, 0.24), p1=(0.5, 0.27))]
        fx.append(('panel', 22.2, 25.8))
        els += [
            Text('ESTRUTURA PRONTA', 800, 74, WHITE, 0, 1110, 22.45, 25.8, align='center'),
            Text('PARA O SEU EVENTO.', 800, 74, CYAN, 0, 1192, 22.6, 25.8, align='center'),
            Chip('CONSULTE A DISPONIBILIDADE', 0, 1310, 22.9, 25.8, fg=NAVY, bg=CYAN, border=None, s=34, w=800, pad=(34, 20), align='center'),
            Text('(19) 3417-8600', 800, 72, WHITE, 0, 1430, 23.4, 25.8, align='center'),
            Img(PL, (W - PL.width) // 2, 1580, 23.8, 25.8, rise=12, fade=0.7),
        ]
        shots += [Plain(WHITE, 25.8, T + 1)]
        els += scene_end(25.8, T)
        fx += [('wipe', 4.2), ('wipe', 10.8), ('wipe', 17.4), ('wipe', 22.2), ('wipe', 25.8)]
        wm_spans = [(0, 17.4)]
    else:   # AD 15 s
        T = 15.0
        s1 = Shot('S2_8151', 0, 3.0, z=(1.3, 1.7), f=TV51, p=(0.5, 0.33), p1=(0.5, 0.33))
        s1.marks = [(SCREEN_8151, 0.6)]
        shots += [s1]
        els += [
            Bar(72, 1088, 120, 8, CYAN, -1.0, 3.0),
            Text('VOCÊ TEM O', 800, 92, WHITE, 72, 1120, -1.0, 3.0),
            Text('CONHECIMENTO.', 800, 92, WHITE, 72, 1222, -1.0, 3.0),
            Text('NÓS TEMOS', 800, 92, WHITE, 72, 1352, 2.2, 3.0),
            Text('O ESPAÇO.', 800, 92, CYAN, 72, 1454, 2.32, 3.0),
        ]
        shots += [Shot('S1_9837', 3.0, 5.4, z=(1.05, 1.4), f=TV37, p=(0.5, 0.45), p1=(0.5, 0.38)), Shot('S2_8149', 5.4, 6.6, z=(1.04, 1.1), f=(0.5, 0.5), f1=(0.6, 0.5))]
        els += [
            Text('SALAS PARA', 800, 96, WHITE, 72, 1200, 3.1, 6.6),
            Text('LOCAÇÃO', 800, 96, WHITE, 72, 1306, 3.22, 6.6),
            Text('EM PIRACICABA', 800, 96, CYAN, 72, 1412, 3.34, 6.6),
            Chip('MODERNAS E CLIMATIZADAS', 72, 1110 - 20, 3.6, 6.6),
        ]
        s3 = Shot('S1_9837', 6.6, 9.0, z=(1.9, 2.35), f=TV37, p=(0.5, 0.36), p1=(0.5, 0.34))
        s3.marks = [(SCREEN_9837, 6.75)]
        shots += [s3]
        els += [
            Bar(72, 1150, 120, 8, CYAN, 6.65, 9.0),
            Text('LOUSA INTERATIVA', 800, 84, WHITE, 72, 1180, 6.7, 9.0),
            Text('E CONECTADA', 800, 84, CYAN, 72, 1274, 6.82, 9.0),
        ]
        shots += [Shot('S2_8151', 9.0, 12.0, z=(1.6, 1.2), f=TV51, p=(0.5, 0.24), p1=(0.5, 0.27))]
        fx.append(('panel', 9.0, 12.0))
        els += [
            Text('SEU PRÓXIMO EVENTO', 800, 74, WHITE, 0, 1110, 9.15, 12.0, align='center'),
            Text('COMEÇA AQUI.', 800, 74, CYAN, 0, 1192, 9.27, 12.0, align='center'),
            Chip('CONSULTE A DISPONIBILIDADE', 0, 1310, 9.6, 12.0, fg=NAVY, bg=CYAN, border=None, s=34, w=800, pad=(34, 20), align='center'),
            Text('(19) 3417-8600', 800, 72, WHITE, 0, 1430, 9.8, 12.0, align='center'),
            Img(PL, (W - PL.width) // 2, 1580, 10.1, 12.0, rise=12, fade=0.6),
        ]
        shots += [Plain(WHITE, 12.0, T + 1)]
        els += scene_end(12.0, T)
        fx += [('wipe', 9.0), ('wipe', 12.0)]
        wm_spans = [(0, 9.0)]
    return T, shots, els, fx, WM, wm_spans

def frame_at(t, T, shots, els, fx, WM, wm_spans):
    sh = next(s for s in shots if s.t0 <= t < s.t1)
    fr = sh.render(t)
    if isinstance(sh, Shot):
        fr.alpha_composite(G_TOP)
        panel = any(f[0] == 'panel' and f[1] <= t < f[2] for f in fx)
        if panel:
            # painel institucional na metade inferior (máscara com fio ciano)
            p = next(f for f in fx if f[0] == 'panel' and f[1] <= t < f[2])
            q = ease((t - p[1] - 0.1) / 0.6)
            top = int(H - (H - 940) * q)
            ImageDraw.Draw(fr).rectangle((0, top, W, H), fill=NAVY)
            ImageDraw.Draw(fr).rectangle((0, top, W, top + 6), fill=CYAN)
        elif any(f[0] == 'lgrad' and f[1] <= t < f[2] for f in fx):
            fr.alpha_composite(G_LEFT); fr.alpha_composite(G_BOTTOM)
        else:
            fr.alpha_composite(G_BOTTOM)
        for box, tin in sh.marks:
            brackets(fr, sh, box, tin, t)
    for e in els: e.draw(fr, t)
    if any(a <= t < b for a, b in wm_spans):
        a = 1.0
        for s0, s1 in wm_spans:
            if s0 <= t < s1:
                if s0 > 0: a = min(a, (t - s0) / 0.5)
                a = min(a, (s1 - t) / 0.4)
        wm = WM
        if a < 1:
            wm = WM.copy(); wm.putalpha(WM.getchannel('A').point(lambda v: int(v * max(a, 0))))
        fr.alpha_composite(wm, ((W - WM.width) // 2, 150))
    for f in fx:
        if f[0] == 'wipe': wipe(fr, t, f[1])
    return fr.convert('RGB')

def render_video(mode, out):
    T, shots, els, fx, WM, sp = build(mode)
    n = int(round(T * FPS))
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                          '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p',
                          '-profile:v', 'high', '-tune', 'film', out], stdin=subprocess.PIPE)
    for i in range(n):
        t = i / FPS
        p.stdin.write(frame_at(t, T, shots, els, fx, WM, sp).tobytes())
        if i % 150 == 0: print(mode, i, '/', n, flush=True)
    p.stdin.close(); p.wait()

def stills(mode, outdir, times):
    T, shots, els, fx, WM, sp = build(mode)
    os.makedirs(outdir, exist_ok=True)
    for t in times:
        frame_at(t, T, shots, els, fx, WM, sp).save(f'{outdir}/{mode}_{t:05.2f}.jpg', quality=90)

def cover(out):
    init_grads()
    sh = Shot('S1_9837', 0, 1, z=(1.25, 1.25), f=TV37, p=(0.5, 0.4), p1=(0.5, 0.4))
    fr = sh.render(0)
    fr.alpha_composite(grad(700, 1500, 0.0, 0.9)); fr.alpha_composite(grad(0, 520, 0.6, 0.0))
    L = logo('neg', 330)
    fr.alpha_composite(L, ((W - L.width) // 2, 330))           # dentro do recorte 3:4 e 1:1 do grid
    y = 1000
    Bar(0, y - 34, 120, 8, CYAN, -1, 9, align='center').draw(fr, 5)
    for i, (txt, col) in enumerate((('SEU CONHECIMENTO', WHITE), ('MERECE', WHITE), ('ESSE ESPAÇO.', CYAN))):
        Text(txt, 800, 74, col, 0, y + i * 88, -1, 9, align='center').draw(fr, 5)
    Text('SALAS PARA LOCAÇÃO · PIRACICABA', 600, 32, WHITE, 0, y + 292, -1, 9, track=0.14, align='center').draw(fr, 5)
    fr.convert('RGB').save(out, quality=95)

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'cover': cover(sys.argv[2])
    elif mode == 'stills': stills(sys.argv[2], sys.argv[3], [float(x) for x in sys.argv[4:]])
    else: render_video(mode, sys.argv[2])
