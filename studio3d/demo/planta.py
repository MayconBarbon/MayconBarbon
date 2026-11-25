# Gera a planta 2D (SVG) a partir da MESMA geometria de plan.js
import json, re, os
D = os.path.dirname(os.path.abspath(__file__))
js = open(os.path.join(D, 'plan.js')).read()
obj = js[js.find('{'):js.rfind('}') + 1]
obj = re.sub(r'//[^\n]*', '', obj)
obj = re.sub(r'(\w+):', r'"\1":', obj).replace("'", '"')
P = json.loads(obj)
S = 80; ox, oy = 70, 70; T = P['T']
X = lambda x: round(ox + x * S, 1)
Y = lambda y: round(oy + y * S, 1)
br = lambda v: f'{v:.2f}'.replace('.', ',')
Wpx, Hpx = int(P['W'] * S + 170), int(P['D'] * S + 170)
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {Wpx} {Hpx}" font-family="Inter,Arial,sans-serif">',
       '<rect width="100%" height="100%" fill="#fbfaf7"/>',
       '<defs><pattern id="g" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="#ebe8e1" stroke-width="1"/></pattern></defs>',
       f'<rect x="{ox-30}" y="{oy-30}" width="{P["W"]*S+60}" height="{P["D"]*S+60}" fill="url(#g)"/>']
for i, (x1, y1, x2, y2) in enumerate(P['walls']):
    L = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** .5; ux, uy = (x2 - x1) / L, (y2 - y1) / L
    ops = sorted([o for o in P['openings'] if o['w'] == i], key=lambda o: o['a'])
    def seg(a, b):
        if b - a <= 0: return
        out.append(f'<line x1="{X(x1+ux*a)}" y1="{Y(y1+uy*a)}" x2="{X(x1+ux*b)}" y2="{Y(y1+uy*b)}" stroke="#1d1d1f" stroke-width="{T*S}" stroke-linecap="square"/>')
    cur = 0
    for o in ops:
        seg(cur, o['a'])
        ax, ay = x1 + ux * o['a'], y1 + uy * o['a']; bx, by = x1 + ux * o['b'], y1 + uy * o['b']
        if o['type'] == 'window':
            nx, ny = -uy * T / 2, ux * T / 2
            for k in (-1, 0, 1):
                out.append(f'<line x1="{X(ax+nx*k)}" y1="{Y(ay+ny*k)}" x2="{X(bx+nx*k)}" y2="{Y(by+ny*k)}" stroke="#3a7ca5" stroke-width="2"/>')
        else:
            w = o['b'] - o['a']
            # folha abre para dentro do apartamento / para o lado da sala
            px, py = (-uy, ux) if i != 2 else (uy * -1, -ux * -1)
            if i == 2: px, py = 0, -1
            if i == 4: px, py = -1, 0
            lx, ly = ax + px * w, ay + py * w
            cross = (lx - ax) * (by - ay) - (ly - ay) * (bx - ax)
            sweep = 1 if cross < 0 else 0
            out.append(f'<line x1="{X(ax)}" y1="{Y(ay)}" x2="{X(lx)}" y2="{Y(ly)}" stroke="#1d1d1f" stroke-width="2"/>')
            out.append(f'<path d="M{X(lx)} {Y(ly)} A{w*S} {w*S} 0 0 {sweep} {X(bx)} {Y(by)}" fill="none" stroke="#9a9aa0" stroke-width="1.5" stroke-dasharray="4 3"/>')
        cur = o['b']
    seg(cur, L)
for r in P['rooms']:
    cx, cy = X(r['x'] + r['w'] / 2), Y(r['y'] + r['d'] / 2)
    out.append(f'<text x="{cx}" y="{cy-4}" text-anchor="middle" font-size="17" font-weight="600" fill="#1d1d1f">{r["name"]}</text>')
    out.append(f'<text x="{cx}" y="{cy+20}" text-anchor="middle" font-size="14" fill="#6b6b73">{br(r["w"])} × {br(r["d"])} m · ≈{r["w"]*r["d"]:.0f} m²</text>')
yd = Y(P['D']) + 60
out.append(f'<line x1="{X(0)}" y1="{yd}" x2="{X(P["W"])}" y2="{yd}" stroke="#6b6b73" stroke-width="1.2"/>')
for x in (0, 6, P['W']): out.append(f'<line x1="{X(x)}" y1="{yd-8}" x2="{X(x)}" y2="{yd+8}" stroke="#6b6b73" stroke-width="1.2"/>')
out.append(f'<text x="{X(3)}" y="{yd-10}" text-anchor="middle" font-size="14" fill="#6b6b73">6,00</text><text x="{X(8)}" y="{yd-10}" text-anchor="middle" font-size="14" fill="#6b6b73">4,00</text>')
xd = X(P['W']) + 45
out.append(f'<line x1="{xd}" y1="{Y(0)}" x2="{xd}" y2="{Y(P["D"])}" stroke="#6b6b73" stroke-width="1.2"/>')
for y in (0, 4, P['D']): out.append(f'<line x1="{xd-8}" y1="{Y(y)}" x2="{xd+8}" y2="{Y(y)}" stroke="#6b6b73" stroke-width="1.2"/>')
out.append(f'<text x="{xd+12}" y="{Y(2)+5}" font-size="14" fill="#6b6b73">4,00</text><text x="{xd+12}" y="{Y(5.5)+5}" font-size="14" fill="#6b6b73">3,00</text>')
out.append(f'<text x="{ox-30}" y="{oy-44}" font-size="13" fill="#9a9aa0" letter-spacing="2">PLANTA CONCEITUAL · DEMONSTRAÇÃO · MEDIDAS EM METROS</text>')
out.append('</svg>')
open(os.path.join(D, 'planta.svg'), 'w').write('\n'.join(out))
print(Wpx, Hpx)
