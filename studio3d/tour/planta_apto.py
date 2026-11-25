# Planta 2D (SVG) do apartamento de demonstração, gerada da MESMA geometria do tour (plans/apto.json)
import json, os, math
D = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(D, 'plans/apto.json'), encoding='utf-8'))
S, T = 70, P['T']; x0, z0, x1, z1 = P['bounds']
ox, oy = 90 - x0 * S, 110
X = lambda x: round(ox + x * S, 1); Y = lambda y: round(oy + y * S, 1)
br = lambda v: f'{v:.2f}'.replace('.', ',')
Wpx, Hpx = int((x1 - x0) * S + 250), int((z1 - z0) * S + 190)
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {Wpx} {Hpx}" font-family="Inter,Arial,sans-serif">', '<rect width="100%" height="100%" fill="#fbfaf7"/>']
for r in P['rooms']:
    fill = {'deck': '#efe6d6', 'stone': '#ecebe7', 'tile': '#eef0f0', 'porc': '#f1efeb'}.get(r['floor'], '#fbfaf7')
    if fill != '#fbfaf7': o.append(f'<rect x="{X(r["x"])}" y="{Y(r["y"])}" width="{r["w"]*S}" height="{r["d"]*S}" fill="{fill}"/>')
    if r['floor'] == 'deck':
        k = r['x']
        while k < r['x'] + r['w']: o.append(f'<line x1="{X(k)}" y1="{Y(r["y"])}" x2="{X(k)}" y2="{Y(r["y"]+r["d"])}" stroke="#e2d4bb"/>'); k += 0.15
# guarda-corpo da varanda
o.append(f'<path d="M{X(8.1)} {Y(3.0)}H{X(9.5)}V{Y(6.7)}H{X(8.1)}" fill="none" stroke="#3a7ca5" stroke-width="2.5"/>')
for i, (a1, b1, a2, b2) in enumerate(P['walls']):
    L = math.hypot(a2 - a1, b2 - b1); ux, uy = (a2 - a1) / L, (b2 - b1) / L
    ops = sorted([q for q in P['openings'] if q['w'] == i], key=lambda q: q['a'])
    def seg(a, b):
        if b - a > 0: o.append(f'<line x1="{X(a1+ux*a)}" y1="{Y(b1+uy*a)}" x2="{X(a1+ux*b)}" y2="{Y(b1+uy*b)}" stroke="#1d1d1f" stroke-width="{T*S}" stroke-linecap="square"/>')
    cur = 0
    for q in ops:
        seg(cur, q['a'])
        ax, ay = a1 + ux * q['a'], b1 + uy * q['a']; bx, by = a1 + ux * q['b'], b1 + uy * q['b']
        nx, ny = -uy, ux
        if q['type'] == 'window':
            for s in (-1, 0, 1): o.append(f'<line x1="{X(ax+nx*T/2*s)}" y1="{Y(ay+ny*T/2*s)}" x2="{X(bx+nx*T/2*s)}" y2="{Y(by+ny*T/2*s)}" stroke="#3a7ca5" stroke-width="2"/>')
        elif q.get('slide'):
            mx, my = (ax + bx) / 2, (ay + by) / 2
            o.append(f'<line x1="{X(ax+nx*0.04)}" y1="{Y(ay+ny*0.04)}" x2="{X(mx+ux*0.1+nx*0.04)}" y2="{Y(my+uy*0.1+ny*0.04)}" stroke="#3a7ca5" stroke-width="3"/>')
            o.append(f'<line x1="{X(mx-ux*0.1-nx*0.04)}" y1="{Y(my-uy*0.1-ny*0.04)}" x2="{X(bx-nx*0.04)}" y2="{Y(by-ny*0.04)}" stroke="#3a7ca5" stroke-width="3"/>')
        else:
            sw = q.get('swing', 1); w = q['b'] - q['a']
            lx, ly = bx + nx * w * sw, by + ny * w * sw
            o.append(f'<line x1="{X(bx)}" y1="{Y(by)}" x2="{X(lx)}" y2="{Y(ly)}" stroke="#1d1d1f" stroke-width="2"/>')
            cross = (lx - bx) * (ay - by) - (ly - by) * (ax - bx)
            o.append(f'<path d="M{X(lx)} {Y(ly)} A{w*S} {w*S} 0 0 {1 if cross > 0 else 0} {X(ax)} {Y(ay)}" fill="none" stroke="#9a9aa0" stroke-width="1.5" stroke-dasharray="4 3"/>')
        cur = q['b']
    seg(cur, L)
# elevadores
for ex in (0.35, 1.55): o.append(f'<rect x="{X(ex-0.45)}" y="{Y(7.95)}" width="{0.9*S}" height="{0.1*S}" fill="#9fa3a6"/>')
o.append(f'<text x="{X(0.95)}" y="{Y(8.1)+18}" text-anchor="middle" font-size="11" fill="#9a9aa0">elevadores</text>')
for r in P['rooms']:
    if r.get('nolabel'): continue
    cx, cy = X(r['x'] + r['w'] / 2), Y(r['y'] + r['d'] / 2)
    small = r['w'] < 2.3 or r['d'] < 1.6
    o.append(f'<text x="{cx}" y="{cy-4}" text-anchor="middle" font-size="{12 if small else 15}" font-weight="600" fill="#1d1d1f">{r["name"]}</text>')
    if r['name'] != 'Hall do andar': o.append(f'<text x="{cx}" y="{cy+14}" text-anchor="middle" font-size="11" fill="#6b6b73">{br(r["w"])} × {br(r["d"])}</text>')
def dim_h(xs, y, lab=True):
    o.append(f'<line x1="{X(xs[0])}" y1="{y}" x2="{X(xs[-1])}" y2="{y}" stroke="#6b6b73" stroke-width="1.1"/>')
    for x in xs: o.append(f'<line x1="{X(x)}" y1="{y-6}" x2="{X(x)}" y2="{y+6}" stroke="#6b6b73" stroke-width="1.1"/>')
    for a, b in zip(xs, xs[1:]): o.append(f'<text x="{(X(a)+X(b))/2}" y="{y-8}" text-anchor="middle" font-size="12" fill="#6b6b73">{br(b-a)}</text>')
def dim_v(zs, x):
    o.append(f'<line x1="{x}" y1="{Y(zs[0])}" x2="{x}" y2="{Y(zs[-1])}" stroke="#6b6b73" stroke-width="1.1"/>')
    for z in zs: o.append(f'<line x1="{x-6}" y1="{Y(z)}" x2="{x+6}" y2="{Y(z)}" stroke="#6b6b73" stroke-width="1.1"/>')
    for a, b in zip(zs, zs[1:]): o.append(f'<text x="{x+10}" y="{(Y(a)+Y(b))/2+4}" font-size="12" fill="#6b6b73">{br(b-a)}</text>')
dim_h(P['dims']['top'], Y(0) - 22); dim_h([0, 8.1], Y(0) - 46)
dim_v(P['dims']['right'], X(9.5) + 30); dim_v([3.0, 6.7], X(9.5) + 80)
o.append(f'<text x="{X(x0)}" y="34" font-size="12" fill="#9a9aa0" letter-spacing="2">PROJETO DE DEMONSTRAÇÃO · APARTAMENTO TIPO · REDESENHO VÍDEO IMÓVEL · MEDIDAS EM METROS</text>')
o.append(f'<text x="{X(x0)}" y="{Hpx-22}" font-size="12" fill="#6b6b73">Área de projeto ≈ {8.1*6.7:.0f} m² + varanda ≈ {1.4*3.7:.1f} m² · exemplo ilustrativo, não é empreendimento à venda</text>'.replace('.', ',', 1) if False else f'<text x="{X(x0)}" y="{Hpx-22}" font-size="12" fill="#6b6b73">Área interna de projeto ≈ 54 m² + varanda ≈ 5,2 m² · exemplo ilustrativo, não é empreendimento à venda</text>')
o.append('</svg>')
open(os.path.join(D, 'planta-apto.svg'), 'w', encoding='utf-8').write('\n'.join(o))
print(Wpx, Hpx)
