"""SIMESPI — peças estáticas de feed (1080x1350): post único + carrossel com foco na lousa.
Uso: python feed.py OUTDIR"""
import sys, os
import render as R
from PIL import Image, ImageDraw

R.W, R.H = 1080, 1350
W, H = R.W, R.H
NAVY, BLUE, CYAN, WHITE = R.NAVY, R.BLUE, R.CYAN, R.WHITE
T = 5.0   # instante "final" das animações: tudo visível

class Frame:
    """Recorte 4:5 de foto real: zoom z, ponto focal f (normalizado na foto) posto em p (normalizado no quadro)."""
    def __init__(self, name, z=1.0, f=(0.5, 0.5), p=(0.5, 0.5)):
        self.src = R.photo(name); sw, sh = self.src.size
        ch = sh / z; cw = ch * W / H
        if cw > sw: cw = sw; ch = cw * H / W
        x0 = min(max(f[0] * sw - p[0] * cw, 0), sw - cw); y0 = min(max(f[1] * sh - p[1] * ch, 0), sh - ch)
        self.box = (x0, y0, cw, ch)
    def render(self):
        x0, y0, cw, ch = self.box
        return self.src.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch)).convert('RGBA')
    def map_pt(self, nx, ny):
        sw, sh = self.src.size; x0, y0, cw, ch = self.box
        return ((nx * sw - x0) / cw * W, (ny * sh - y0) / ch * H)

def draw_all(fr, els):
    for e in els: e.draw(fr, T)

def tv(fr, frame, box, label=None, side='below'):
    """Cantoneiras na tela real + etiqueta opcional."""
    R.brackets(fr, frame, box, -10, T)
    if label:
        (x0, y0) = frame.map_pt(box[0], box[1]); (x1, y1) = frame.map_pt(box[2], box[3])
        y = int(y1 + 40) if side == 'below' else int(y0 - 100)
        c = R.Chip(label, int(max(x0 - 18, 48)), y, -10, 99, fg=NAVY, bg=CYAN, border=None, s=28, w=800, pad=(26, 16))
        c.draw(fr, T)

def footer(fr, n, total, swipe=True):
    d = ImageDraw.Draw(fr)
    t = R.text_img(f'{n:02d}/{total:02d}', 600, 26, WHITE, 0.12)
    fr.alpha_composite(t, (W - 72 - t.width, 72))
    if swipe:
        a = R.text_img('ARRASTE', 700, 24, WHITE, 0.2)
        x = W - 72 - a.width - 60; y = H - 96
        fr.alpha_composite(a, (x, y))
        d.line((W - 120, y + 16, W - 76, y + 16), fill=CYAN, width=4)
        d.polygon([(W - 72, y + 16), (W - 86, y + 7), (W - 86, y + 25)], fill=CYAN)

def wm(fr, x=72, y=64, w=210):
    L = R.logo('neg', w); fr.alpha_composite(L, (x, y))

def dimension_line(fr, x0, x1, y, label):
    """Cota estilo planta arquitetônica (sem medida numérica) para evidenciar a amplitude."""
    d = ImageDraw.Draw(fr)
    d.line((x0, y, x1, y), fill=WHITE, width=3)
    for x in (x0, x1):
        d.line((x, y - 22, x, y + 22), fill=WHITE, width=3)
    for x, s in ((x0, 1), (x1, -1)):
        d.polygon([(x + 2 * s, y), (x + 20 * s, y - 9), (x + 20 * s, y + 9)], fill=WHITE)
    t = R.text_img(label, 700, 26, NAVY, 0.18)
    pw, ph = t.width + 40, t.height + 14
    cx = (x0 + x1) // 2
    d.rounded_rectangle((cx - pw // 2, y - ph // 2, cx + pw // 2, y + ph // 2), radius=ph // 2, fill=CYAN)
    fr.alpha_composite(t, (cx - t.width // 2, y - t.height // 2 - 2))

# ------------------------------------------------------------------ POST ÚNICO
def post(out):
    fr0 = Frame('S1_9837', z=1.0, f=(0.48, 0.5), p=(0.5, 0.5))
    fr = fr0.render()
    fr.alpha_composite(R.grad(0, 380, 0.80, 0.0)); fr.alpha_composite(R.grad(700, 1150, 0.0, 0.92))
    wm(fr)
    tv(fr, fr0, R.SCREEN_9837)
    dimension_line(fr, 70, W - 70, 820, 'ESPAÇO AMPLO E CLIMATIZADO')
    els = [
        R.Bar(72, 905, 120, 8, CYAN, -1, 99),
        R.Text('SALAS PARA', 800, 104, WHITE, 72, 930, -1, 99),
        R.Text('LOCAÇÃO', 800, 104, CYAN, 72, 1044, -1, 99),
        R.Text('Cursos, palestras, treinamentos e workshops', 500, 34, WHITE, 72, 1170, -1, 99),
        R.Text('em Piracicaba  ·  (19) 3417-8600', 700, 34, WHITE, 72, 1218, -1, 99),
    ]
    draw_all(fr, els)
    fr.convert('RGB').save(out, quality=95)

# ------------------------------------------------------------------ CARROSSEL
def carousel(outdir):
    N = 6
    # 1 — capa: lousa em close
    f1 = Frame('S2_8151', z=1.55, f=R.TV51, p=(0.5, 0.30))
    fr = f1.render(); fr.alpha_composite(R.grad(0, 330, 0.75, 0.0)); fr.alpha_composite(R.grad(640, 1120, 0.0, 0.92))
    wm(fr); tv(fr, f1, R.SCREEN_8151)
    draw_all(fr, [
        R.Chip('SALAS PARA LOCAÇÃO · SIMESPI', 72, 800, -1, 99, bg=BLUE, border=None, s=28, w=700),
        R.Text('LOUSA', 800, 112, WHITE, 72, 880, -1, 99),
        R.Text('INTERATIVA', 800, 112, WHITE, 72, 1002, -1, 99),
        R.Text('E CONECTADA', 800, 112, CYAN, 72, 1124, -1, 99),
    ])
    footer(fr, 1, N); fr.convert('RGB').save(f'{outdir}/carrossel_01.jpg', quality=95)

    # 2 — Sala 01: visão ampla com a lousa ao fundo
    f2 = Frame('S1_9837', z=1.15, f=R.TV37, p=(0.5, 0.36))
    fr = f2.render(); fr.alpha_composite(R.grad(0, 330, 0.75, 0.0)); fr.alpha_composite(R.grad(760, 1180, 0.0, 0.92))
    wm(fr); tv(fr, f2, R.SCREEN_9837, 'LOUSA INTERATIVA', side='below')
    draw_all(fr, [
        R.Text('SALA', 700, 44, WHITE, 72, 960, -1, 99, track=0.3),
        R.Text('01', 800, 150, WHITE, 66, 1000, -1, 99),
        R.Text('Ampla, organizada e climatizada,', 500, 36, WHITE, 300, 1036, -1, 99),
        R.Text('com a tecnologia no centro', 500, 36, WHITE, 300, 1082, -1, 99),
        R.Text('da apresentação.', 500, 36, CYAN, 300, 1128, -1, 99),
    ])
    footer(fr, 2, N); fr.convert('RGB').save(f'{outdir}/carrossel_02.jpg', quality=95)

    # 3 — Sala 02: visão ampla com a lousa
    f3 = Frame('S2_8151', z=1.05, f=R.TV51, p=(0.5, 0.24))
    fr = f3.render(); fr.alpha_composite(R.grad(0, 330, 0.75, 0.0)); fr.alpha_composite(R.grad(760, 1180, 0.0, 0.92))
    wm(fr); tv(fr, f3, R.SCREEN_8151, 'LOUSA INTERATIVA E CONECTADA', side='below')
    draw_all(fr, [
        R.Text('SALA', 700, 44, WHITE, 72, 960, -1, 99, track=0.3),
        R.Text('02', 800, 150, WHITE, 66, 1000, -1, 99),
        R.Text('Mesas e cadeiras para turmas', 500, 36, WHITE, 300, 1036, -1, 99),
        R.Text('de diferentes formatos, com', 500, 36, WHITE, 300, 1082, -1, 99),
        R.Text('lousa sempre à vista.', 500, 36, CYAN, 300, 1128, -1, 99),
    ])
    footer(fr, 3, N); fr.convert('RGB').save(f'{outdir}/carrossel_03.jpg', quality=95)

    # 4 — tela grande (Sala 01, IMG_9825)
    f4 = Frame('S1_9825', z=1.0, f=R.TV25, p=(0.72, 0.36))
    fr = f4.render(); fr.alpha_composite(R.grad(0, 330, 0.75, 0.0)); fr.alpha_composite(R.grad(640, 1120, 0.0, 0.92))
    wm(fr)
    draw_all(fr, [
        R.Bar(72, 850, 120, 8, CYAN, -1, 99),
        R.Text('TECNOLOGIA QUE', 800, 84, WHITE, 72, 880, -1, 99),
        R.Text('TRANSFORMA', 800, 84, WHITE, 72, 974, -1, 99),
        R.Text('APRESENTAÇÕES', 800, 84, CYAN, 72, 1068, -1, 99),
        R.Text('Lousa interativa e conectada para aulas', 500, 34, WHITE, 72, 1180, -1, 99),
        R.Text('e palestras mais dinâmicas.', 500, 34, WHITE, 72, 1226, -1, 99),
    ])
    footer(fr, 4, N); fr.convert('RGB').save(f'{outdir}/carrossel_04.jpg', quality=95)

    # 5 — usos: close da lousa + lista
    f5 = Frame('S1_9837', z=1.9, f=R.TV37, p=(0.5, 0.30))
    fr = f5.render(); fr.alpha_composite(R.grad(0, 300, 0.75, 0.0)); fr.alpha_composite(R.grad(560, 1000, 0.0, 0.94))
    wm(fr); tv(fr, f5, R.SCREEN_9837)
    y = 760
    els = [R.Bar(72, y - 30, 120, 8, CYAN, -1, 99)]
    for i, wd in enumerate(['CURSOS', 'PALESTRAS', 'WORKSHOPS', 'TREINAMENTOS']):
        els.append(R.Text(wd, 800, 76, WHITE if i < 3 else CYAN, 72, y + i * 86, -1, 99))
    els.append(R.Chip('ASSOCIADOS OU NÃO', 72, 1130, -1, 99, bg=BLUE, border=None, s=30, w=700, pad=(30, 18)))
    draw_all(fr, els)
    footer(fr, 5, N); fr.convert('RGB').save(f'{outdir}/carrossel_05.jpg', quality=95)

    # 6 — CTA: lousa no topo + painel institucional
    f6 = Frame('S2_8151', z=1.35, f=R.TV51, p=(0.5, 0.22))
    fr = f6.render(); fr.alpha_composite(R.grad(0, 300, 0.75, 0.0))
    d = ImageDraw.Draw(fr); d.rectangle((0, 660, W, H), fill=NAVY); d.rectangle((0, 660, W, 666), fill=CYAN)
    tv(fr, f6, R.SCREEN_8151)
    L = R.logo('neg', 300)
    draw_all(fr, [
        R.Text('SEU PRÓXIMO EVENTO', 800, 72, WHITE, 0, 710, -1, 99, align='center'),
        R.Text('COMEÇA AQUI.', 800, 72, CYAN, 0, 790, -1, 99, align='center'),
        R.Chip('CONSULTE A DISPONIBILIDADE', 0, 910, -1, 99, fg=NAVY, bg=CYAN, border=None, s=32, w=800, pad=(34, 20), align='center'),
        R.Text('(19) 3417-8600', 800, 76, WHITE, 0, 1016, -1, 99, align='center'),
    ])
    fr.alpha_composite(L, ((W - L.width) // 2, 1150))
    footer(fr, 6, N, swipe=False); fr.convert('RGB').save(f'{outdir}/carrossel_06.jpg', quality=95)

if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    R.init_grads()
    post(f'{out}/post_dimensao_sala.jpg')
    carousel(out)
