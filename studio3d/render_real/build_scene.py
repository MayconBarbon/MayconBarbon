# Vídeo Imóvel Studio 3D · cena fotorrealista (Blender Cycles) a partir da MESMA planta (plans/apto.json)
# uso: blender -b -P build_scene.py -- <saida.png> <amostras> [largura altura] [camera]
import bpy, json, math, os, sys
from mathutils import Vector

ARGS = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = ARGS[0] if ARGS else '/tmp/teste.png'
SAMPLES = int(ARGS[1]) if len(ARGS) > 1 else 64
RW, RH = (int(ARGS[2]), int(ARGS[3])) if len(ARGS) > 3 else (1080, 1920)
CAMNAME = ARGS[4] if len(ARGS) > 4 else 'estar'
BASE = os.path.dirname(os.path.abspath(__file__))
FILM = os.path.join(BASE, '..', 'film')
P = json.load(open(os.path.join(BASE, '..', 'tour', 'plans', 'apto.json')))
H = P['H']; T = P['T']

# ---------- limpeza
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

# coordenadas: planta/three (x, y=altura, z) -> Blender (x, -z, y)
def B(x, y, z): return (x, -z, y)

# ---------- materiais
def tex_node(nt, path, non_color=False, scale=1.0):
    n = nt.nodes.new('ShaderNodeTexImage'); n.image = bpy.data.images.load(path, check_existing=True)
    if non_color: n.image.colorspace_settings.name = 'Non-Color'
    m = nt.nodes.new('ShaderNodeMapping'); m.inputs['Scale'].default_value = (scale, scale, scale)
    c = nt.nodes.new('ShaderNodeTexCoord'); nt.links.new(c.outputs['Object'], m.inputs['Vector']); nt.links.new(m.outputs['Vector'], n.inputs['Vector'])
    return n

def mat(name, color=(0.8, 0.8, 0.8), rough=0.6, metal=0.0, tex=None, tex_scale=1.0, tint=None, normal=None, nstr=0.6, emit=None, emit_str=0.0, transmission=0.0, alpha=1.0, sheen=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; bs = nt.nodes['Principled BSDF']
    bs.inputs['Base Color'].default_value = (*color, 1); bs.inputs['Roughness'].default_value = rough; bs.inputs['Metallic'].default_value = metal
    if tex:
        t = tex_node(nt, os.path.join(FILM, 'assets', 'tex', tex + '_diff.jpg'), scale=tex_scale)
        if tint:
            mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.blend_type = 'MULTIPLY'; mix.inputs['Factor'].default_value = 1.0
            nt.links.new(t.outputs['Color'], mix.inputs[6]); mix.inputs[7].default_value = (*tint, 1); nt.links.new(mix.outputs[2], bs.inputs['Base Color'])
        else: nt.links.new(t.outputs['Color'], bs.inputs['Base Color'])
        r = tex_node(nt, os.path.join(FILM, 'assets', 'tex', tex + '_rough.jpg'), True, tex_scale)
        rm = nt.nodes.new('ShaderNodeMath'); rm.operation = 'MULTIPLY'; rm.inputs[1].default_value = rough * 1.4
        nt.links.new(r.outputs['Color'], rm.inputs[0]); nt.links.new(rm.outputs[0], bs.inputs['Roughness'])
    nm = normal or (tex if tex else None)
    if nm:
        nn = tex_node(nt, os.path.join(FILM, 'assets', 'tex', nm + '_nor_gl.jpg'), True, tex_scale)
        nmap = nt.nodes.new('ShaderNodeNormalMap'); nmap.inputs['Strength'].default_value = nstr
        nt.links.new(nn.outputs['Color'], nmap.inputs['Color']); nt.links.new(nmap.outputs['Normal'], bs.inputs['Normal'])
    if emit:
        bs.inputs['Emission Color'].default_value = (*emit, 1); bs.inputs['Emission Strength'].default_value = emit_str
    if transmission: bs.inputs['Transmission Weight'].default_value = transmission
    if sheen: bs.inputs['Sheen Weight'].default_value = sheen
    if alpha < 1: bs.inputs['Alpha'].default_value = alpha; m.blend_method = 'BLEND'
    return m

M = {
    'wall': mat('parede', (0.86, 0.83, 0.78), 0.85),
    'ceilW': mat('forro_branco', (0.9, 0.89, 0.86), 0.9),
    'wood': mat('madeira', tex='laminate_floor_02', tex_scale=0.55, rough=0.5, tint=(1.0, 0.86, 0.7)),
    'woodDark': mat('madeira_escura', tex='laminate_floor_02', tex_scale=0.7, rough=0.45, tint=(0.62, 0.46, 0.33)),
    'floor': mat('porcelanato', (0.80, 0.75, 0.68), 0.14, normal='slab_tiles', nstr=0.08),
    'floorWood': mat('piso_madeira', tex='laminate_floor_02', tex_scale=0.6, rough=0.4, nstr=0.4),
    'tile': mat('revestimento', tex='long_white_tiles', tex_scale=0.9, rough=0.3),
    'deck': mat('deck', tex='wood_floor_deck', tex_scale=0.8, rough=0.6, tint=(0.9, 0.82, 0.72)),
    'sofa': mat('sofa_verde', (0.075, 0.09, 0.045), 0.95, normal='wool_boucle', nstr=0.8, sheen=0.6),
    'cushion': mat('almofada', (0.06, 0.075, 0.035), 0.95, normal='wool_boucle', nstr=0.8, sheen=0.6),
    'rug': mat('tapete', (0.74, 0.68, 0.58), 0.98, normal='knitted_fleece', nstr=1.0, sheen=0.4),
    'linen': mat('linho', (0.85, 0.82, 0.76), 0.95, normal='rough_linen', nstr=0.6, sheen=0.4),
    'leather': mat('couro', (0.32, 0.17, 0.09), 0.45),
    'cane': mat('palhinha', (0.72, 0.6, 0.42), 0.7, normal='knitted_fleece', nstr=1.2),
    'black': mat('preto', (0.02, 0.02, 0.02), 0.35, 0.5),
    'metal': mat('metal', (0.6, 0.58, 0.55), 0.25, 1.0),
    'stone': mat('pedra', (0.88, 0.86, 0.82), 0.2, tex='marble_01', tex_scale=0.5),
    'ceramic': mat('ceramica', (0.88, 0.85, 0.8), 0.35),
    'green': mat('folhas', (0.08, 0.16, 0.05), 0.6, sheen=0.3),
    'terracotta': mat('terracota', (0.55, 0.32, 0.22), 0.8),
    'led': mat('led', (1, 0.8, 0.55), 0.5, emit=(1.0, 0.72, 0.42), emit_str=14.0),
    'screen': mat('tela', (0.01, 0.02, 0.05), 0.1, emit=(0.05, 0.25, 0.85), emit_str=1.6),
    'frame': mat('esquadria', (0.06, 0.06, 0.065), 0.4, 0.6),
    'glass': None, 'sheer': None,
}
g = bpy.data.materials.new('vidro'); g.use_nodes = True; bs = g.node_tree.nodes['Principled BSDF']
bs.inputs['Transmission Weight'].default_value = 1.0; bs.inputs['Roughness'].default_value = 0.0; bs.inputs['IOR'].default_value = 1.45; M['glass'] = g
sh = bpy.data.materials.new('voil'); sh.use_nodes = True; nt = sh.node_tree; out = nt.nodes['Material Output']; nt.nodes.remove(nt.nodes['Principled BSDF'])
tr = nt.nodes.new('ShaderNodeBsdfTranslucent'); tr.inputs['Color'].default_value = (1.0, 0.98, 0.94, 1)
tp = nt.nodes.new('ShaderNodeBsdfTransparent'); df = nt.nodes.new('ShaderNodeBsdfDiffuse'); df.inputs['Color'].default_value = (0.92, 0.91, 0.88, 1)
m1 = nt.nodes.new('ShaderNodeMixShader'); m1.inputs[0].default_value = 0.5; nt.links.new(tr.outputs[0], m1.inputs[1]); nt.links.new(df.outputs[0], m1.inputs[2])
m2 = nt.nodes.new('ShaderNodeMixShader'); m2.inputs[0].default_value = 0.45; nt.links.new(m1.outputs[0], m2.inputs[1]); nt.links.new(tp.outputs[0], m2.inputs[2])
nt.links.new(m2.outputs[0], out.inputs['Surface']); sh.blend_method = 'BLEND'; M['sheer'] = sh

# ---------- primitivas (dimensões no sistema da planta: w ao longo de x, h altura, d ao longo de z)
def box(name, w, h, d, x, y, z, m, bevel=0.0, seg=3, subdiv=0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=B(x, y, z))
    o = bpy.context.active_object; o.name = name; o.scale = (w, d, h)
    bpy.ops.object.transform_apply(scale=True)
    if bevel:
        bm = o.modifiers.new('bevel', 'BEVEL'); bm.width = bevel; bm.segments = seg; bm.limit_method = 'NONE'
    if subdiv:
        sd = o.modifiers.new('sub', 'SUBSURF'); sd.levels = subdiv; sd.render_levels = subdiv
    if m: o.data.materials.append(m)
    for p in o.data.polygons: p.use_smooth = bool(bevel or subdiv)
    return o

def cyl(name, r, h, x, y, z, m, verts=48, bevel=0.0):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h, vertices=verts, location=B(x, y, z))
    o = bpy.context.active_object; o.name = name
    if bevel: bm = o.modifiers.new('bevel', 'BEVEL'); bm.width = bevel; bm.segments = 3
    o.data.materials.append(m); return o

def sphere(name, r, x, y, z, m, sx=1, sy=1, sz=1):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=B(x, y, z), segments=32, ring_count=16)
    o = bpy.context.active_object; o.name = name; o.scale = (sx, sz, sy); o.data.materials.append(m)
    for p in o.data.polygons: p.use_smooth = True
    return o

# ---------- pisos
floorMat = {'wood': M['floorWood'], 'porc': M['floor'], 'tile': M['tile'], 'deck': M['deck'], 'stone': M['floor']}
for r in P['rooms']:
    fm = floorMat.get(r['floor'], M['floor'])
    if r['name'] in ('Estar', 'Jantar', 'Cozinha'): fm = M['floor']  # área social em porcelanato claro (como a referência)
    box('piso_' + r['name'], r['w'], 0.04, r['d'], r['x'] + r['w'] / 2, -0.02, r['y'] + r['d'] / 2, fm)
box('laje_externa', 40, 0.1, 40, 4, -0.12, 4, mat('laje', (0.3, 0.3, 0.3), 0.9))

# ---------- paredes com vãos (mesmo algoritmo do tour e dos vídeos)
glassObjs = []
for i, w in enumerate(P['walls']):
    x1, y1, x2, y2 = w; L = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / L, (y2 - y1) / L; horiz = abs(ux) > 0.5
    def seg(a, b, y0, h):
        if b - a < 0.01 or h <= 0.001: return
        mx, mz = x1 + ux * (a + b) / 2, y1 + uy * (a + b) / 2
        box('parede_%d' % i, (b - a) if horiz else T, h, T if horiz else (b - a), mx, y0 + h / 2, mz, M['wall'])
    ops = sorted([o for o in P['openings'] if o['w'] == i], key=lambda o: o['a']); cur = 0
    for o in ops:
        seg(cur, o['a'], 0, H)
        mx, mz = x1 + ux * (o['a'] + o['b']) / 2, y1 + uy * (o['a'] + o['b']) / 2; ln = o['b'] - o['a']
        if o['type'] == 'window':
            seg(o['a'], o['b'], 0, o['sill']); seg(o['a'], o['b'], o['sill'] + o['h'], H - o['sill'] - o['h'])
            glassObjs.append(box('vidro_%d' % i, ln if horiz else 0.01, o['h'], 0.01 if horiz else ln, mx, o['sill'] + o['h'] / 2, mz, M['glass']))
            for (fw, fh, fx, fy) in ((ln, 0.04, 0, o['sill'] + 0.02), (ln, 0.04, 0, o['sill'] + o['h'] - 0.02)):
                box('caixilho', fw if horiz else 0.06, fh, 0.06 if horiz else fw, mx, fy, mz, M['frame'])
        else:
            top = o.get('h', 2.1); seg(o['a'], o['b'], top, H - top)
            if o.get('slide'):
                box('trilho', ln if horiz else 0.07, 0.05, 0.07 if horiz else ln, mx, top - 0.025, mz, M['frame'])
                for k, off in ((0, -ln / 4), (1, ln / 4 - ln * 0.18)):
                    px, pz = mx + ux * off + (0 if horiz else (0.03 if k else -0.03)), mz + uy * off
                    glassObjs.append(box('porta_vidro', (ln / 2 - 0.06) if horiz else 0.012, top - 0.1, 0.012 if horiz else (ln / 2 - 0.06), px, top / 2, pz, M['glass']))
                    for e in (-1, 1): box('montante', 0.05, top - 0.08, 0.05, px + ux * e * (ln / 4 - 0.02), top / 2, pz + uy * e * (ln / 4 - 0.02), M['frame'])
        cur = o['b']
    seg(cur, L, 0, H)

# ---------- forro: madeira na área social (como a referência), gesso branco no restante
box('forro_madeira', 8.1, 0.03, 3.5, 4.05, H + 0.015, 4.95, M['woodDark'])
box('forro_intimo', 8.1, 0.03, 3.2, 4.05, H + 0.015, 1.6, M['ceilW'])
box('forro_varanda', 1.4, 0.06, 3.7, 8.8, H + 0.03, 4.85, M['woodDark'])
for (x, z) in ((5.4, 4.2), (7.2, 4.2), (5.4, 5.8), (7.2, 5.8), (3.0, 4.2), (3.0, 5.8), (1.2, 4.9)):
    cyl('spot', 0.04, 0.01, x, H - 0.005, z, mat('spot', (1, 1, 1), 0.3, emit=(1, 0.85, 0.65), emit_str=30))
    bpy.ops.object.light_add(type='SPOT', location=B(x, H - 0.03, z)); L_ = bpy.context.active_object
    L_.data.energy = 85; L_.data.color = (1.0, 0.82, 0.62); L_.data.spot_size = math.radians(70); L_.data.spot_blend = 0.6; L_.data.shadow_soft_size = 0.05
    L_.rotation_euler = (0, 0, 0)

# ---------- estante iluminada na parede da TV (parede z = 3,2, lado do estar)
zW = 3.2 + T / 2
box('estante_fundo', 3.2, 2.3, 0.02, 6.45, 1.15 + 0.05, zW + 0.01, M['wood'])
for k in range(5):  # prateleiras laterais (vão central livre para a TV)
    y = 0.45 + k * 0.45
    for (cx, w) in ((5.27, 0.82), (7.62, 0.82)):
        box('prateleira', w, 0.03, 0.34, cx, y, zW + 0.17, M['wood'])
        box('led', w - 0.06, 0.006, 0.012, cx, y - 0.018, zW + 0.31, M['led'])
    if k in (0, 4): box('prateleira_c', 1.5, 0.03, 0.34, 6.45, y if k == 4 else 0.45, zW + 0.17, M['wood']); box('led', 1.44, 0.006, 0.012, 6.45, (y if k == 4 else 0.45) - 0.018, zW + 0.31, M['led'])
for x in (4.86, 5.7, 7.2, 8.04): box('montante_est', 0.03, 2.3, 0.34, x, 1.15 + 0.05, zW + 0.17, M['wood'])
box('aparador', 2.6, 0.42, 0.42, 6.45, 0.21, zW + 0.21, M['wood'], bevel=0.01)
box('tv', 1.35, 0.78, 0.04, 6.45, 1.28, zW + 0.06, M['screen'], bevel=0.004)
for (x, y, h, r) in ((5.1, 0.52, 0.22, 0.06), (5.35, 0.52, 0.3, 0.05), (7.6, 0.97, 0.26, 0.07), (5.3, 1.42, 0.2, 0.08), (7.4, 1.87, 0.3, 0.05), (5.5, 1.87, 0.16, 0.09)):
    cyl('vaso', r, h, x, y + h / 2, zW + 0.16, M['ceramic'], 32, 0.01)
for (x, y) in ((5.05, 0.97), (5.45, 1.87), (7.85, 0.52), (7.45, 1.42)): cyl('vaso2', 0.05, 0.18, x, y + 0.09, zW + 0.16, M['terracotta'], 32, 0.01)
for k in range(9): box('livro', 0.03, 0.24, 0.2, 7.2 + k * 0.035, 1.55, zW + 0.15, [M['linen'], M['leather'], M['ceramic']][k % 3])

# ---------- tapete, sofá curvo, poltrona, mesa orgânica
box('tapete', 3.0, 0.012, 2.2, 6.4, 0.006, 4.85, M['rug'], bevel=0.005)
# sofá: módulos arredondados formando um "C" aberto voltado para a TV
for k in range(4):  # assento em gomos
    box('sofa_gomo', 0.62, 0.44, 0.92, 5.45 + k * 0.6, 0.22, 5.82, M['sofa'], bevel=0.2, seg=8)
    box('sofa_encosto', 0.62, 0.52, 0.3, 5.45 + k * 0.6, 0.64, 6.18, M['sofa'], bevel=0.14, seg=8)
for k in range(3):
    box('sofa_gomo2', 0.92, 0.44, 0.6, 7.5, 0.22, 5.1 - k * 0.58, M['sofa'], bevel=0.2, seg=8)
    box('sofa_encosto2', 0.3, 0.52, 0.6, 7.86, 0.64, 5.1 - k * 0.58, M['sofa'], bevel=0.14, seg=8)
for (x, z, sx, sz) in ((5.5, 6.0, 0.46, 0.16), (6.1, 6.0, 0.46, 0.16), (7.68, 4.6, 0.16, 0.46), (7.68, 5.15, 0.16, 0.46)):
    box('almofada', sx, 0.4, sz, x, 0.74, z, M['cushion'], bevel=0.08, seg=5)
# poltrona de palhinha
box('poltrona_assento', 0.62, 0.08, 0.6, 5.1, 0.42, 4.25, M['linen'], bevel=0.03)
box('poltrona_encosto', 0.62, 0.42, 0.05, 5.1, 0.68, 3.97, M['cane'], bevel=0.01)
for (dx, dz) in ((-0.28, -0.27), (0.28, -0.27), (-0.28, 0.27), (0.28, 0.27)):
    box('perna', 0.035, 0.42, 0.035, 5.1 + dx, 0.21, 4.25 + dz, M['woodDark'], bevel=0.008)
for dx in (-0.31, 0.31): box('braco', 0.04, 0.04, 0.62, 5.1 + dx, 0.62, 4.22, M['woodDark'], bevel=0.015)
# mesa de centro orgânica em madeira
cyl('mesa_centro', 0.5, 0.32, 6.35, 0.16, 4.75, M['woodDark'], 64, 0.04).scale = (1.25, 0.8, 1)
sphere('fruta_deco', 0.12, 6.2, 0.38, 4.7, M['terracotta'], 1.4, 0.6, 1.0)
box('livro_mesa', 0.32, 0.03, 0.24, 6.6, 0.335, 4.8, M['linen'])
# luminária de piso
cyl('lum_piso_haste', 0.01, 1.55, 7.75, 0.78, 6.45, M['black'])
sphere('lum_piso', 0.11, 7.75, 1.56, 6.45, mat('cupula', (1, 0.95, 0.85), 0.6, emit=(1, 0.78, 0.5), emit_str=6))

# ---------- cortinas de voil na porta da varanda (parede x = 8,1)
def curtain(z0, z1, x):
    n = int((z1 - z0) * 18)
    verts, faces = [], []
    for i in range(n + 1):
        z = z0 + (z1 - z0) * i / n; dx = math.sin(i * 1.7) * 0.035
        verts += [B(x + dx, 0.02, z), B(x + dx, H - 0.03, z)]
    for i in range(n): faces.append((2 * i, 2 * i + 2, 2 * i + 3, 2 * i + 1))
    me = bpy.data.meshes.new('voil'); me.from_pydata(verts, [], faces); me.update()
    o = bpy.data.objects.new('cortina', me); bpy.context.collection.objects.link(o); o.data.materials.append(M['sheer'])
    for p in o.data.polygons: p.use_smooth = True
curtain(3.3, 4.2, 7.98); curtain(5.4, 6.6, 7.98)

# ---------- jantar (atrás da câmera / lateral) e varanda
cyl('mesa_jantar', 0.5, 0.04, 3.8, 0.75, 4.9, M['wood'], 64, 0.01); cyl('pe_mesa', 0.18, 0.72, 3.8, 0.37, 4.9, M['black'])
for (x, z, rot) in ((3.15, 4.9, 'x-'), (4.45, 4.9, 'x+'), (3.8, 4.25, 'z-'), (3.8, 5.55, 'z+')):
    box('cadeira_assento', 0.44, 0.05, 0.44, x, 0.46, z, M['linen'], bevel=0.02)
    bx = {'x-': -0.2, 'x+': 0.2}.get(rot, 0); bz = {'z-': -0.2, 'z+': 0.2}.get(rot, 0)
    box('cadeira_encosto', 0.04 if bx else 0.42, 0.42, 0.42 if bx else 0.04, x + bx, 0.72, z + bz, M['cane'], bevel=0.01)
    for (dx, dz) in ((-0.19, -0.19), (0.19, -0.19), (-0.19, 0.19), (0.19, 0.19)): box('perna', 0.03, 0.45, 0.03, x + dx, 0.225, z + dz, M['woodDark'])
sphere('pendente', 0.22, 3.8, 2.0, 4.9, mat('pendente', (0.05, 0.05, 0.05), 0.4, 0.6), 1, 0.55, 1)
bpy.ops.object.light_add(type='POINT', location=B(3.8, 1.85, 4.9)); pl = bpy.context.active_object; pl.data.energy = 40; pl.data.color = (1, 0.78, 0.5); pl.data.shadow_soft_size = 0.1
for (x, z, s) in ((9.1, 6.2, 1.2), (9.1, 3.4, 0.9), (7.7, 3.55, 1.3)):
    cyl('vaso_planta', 0.18 * s, 0.4 * s, x, 0.2 * s, z, M['terracotta'], 32, 0.01)
    for k in range(16):
        a = k * 2.4; r = 0.06 + 0.012 * k; sphere('folha', 0.13 * s, x + math.cos(a) * r * s, (0.55 + 0.045 * k) * s, z + math.sin(a) * r * s, M['green'], 0.45, 1.5, 0.12)

# ---------- mundo: HDRI do céu (vista pela varanda) + sol entrando pela porta
w = bpy.data.worlds.new('mundo'); sc.world = w; w.use_nodes = True; wn = w.node_tree
env = wn.nodes.new('ShaderNodeTexEnvironment'); env.image = bpy.data.images.load(os.path.join(FILM, 'assets', 'rooftop_day.hdr'))
mp = wn.nodes.new('ShaderNodeMapping'); tc = wn.nodes.new('ShaderNodeTexCoord'); mp.inputs['Rotation'].default_value = (0, 0, math.radians(110))
wn.links.new(tc.outputs['Generated'], mp.inputs['Vector']); wn.links.new(mp.outputs['Vector'], env.inputs['Vector'])
wn.links.new(env.outputs['Color'], wn.nodes['Background'].inputs['Color']); wn.nodes['Background'].inputs['Strength'].default_value = 1.4
bpy.ops.object.light_add(type='SUN', location=B(20, 10, 4)); sun = bpy.context.active_object
sun.data.energy = 4.0; sun.data.color = (1.0, 0.82, 0.62); sun.data.angle = math.radians(1.5)
sun.rotation_euler = (math.radians(62), 0, math.radians(-75))
# luz de preenchimento na abertura da varanda (simula céu claro entrando)
bpy.ops.object.light_add(type='AREA', location=B(8.6, 1.2, 4.7)); ar = bpy.context.active_object
ar.data.energy = 380; ar.data.size = 2.4; ar.data.size_y = 2.2; ar.data.shape = 'RECTANGLE'; ar.data.color = (0.92, 0.95, 1.0)
ar.rotation_euler = (0, math.radians(-90), 0)

# ---------- câmeras
CAMS = {
    'estar': ((3.15, 1.42, 6.35), (8.0, 1.0, 4.05), 15),
    'estar_h': ((3.3, 1.4, 3.55), (8.0, 1.0, 5.4), 18),
}
pos, look, lens = CAMS[CAMNAME]
bpy.ops.object.camera_add(location=B(*pos)); cam = bpy.context.active_object; sc.camera = cam; cam.data.lens = lens; cam.data.sensor_width = 36
d = Vector(B(*look)) - Vector(B(*pos)); cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
ANIM = os.environ.get('ANIM')
if ANIM:  # p0 -> p1 em N quadros, olhando de l0 para l1
    N = int(ANIM); fr = int(os.environ.get('FRAME', '0'))
    k = fr / max(1, N - 1); e = k * k * (3 - 2 * k)
    p0, p1 = Vector((2.75, 1.44, 6.5)), Vector((3.75, 1.38, 6.05)); l0, l1 = Vector((8.0, 1.0, 4.25)), Vector((8.0, 0.95, 3.75))
    pp = p0.lerp(p1, e); ll = l0.lerp(l1, e)
    cam.location = B(*pp); d = Vector(B(*ll)) - Vector(B(*pp)); cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
cam.data.shift_y = 0.0

# ---------- render
sc.render.engine = 'CYCLES'; cy = sc.cycles; cy.device = 'CPU'; cy.samples = SAMPLES; cy.use_adaptive_sampling = True; cy.adaptive_threshold = 0.02
cy.use_denoising = True
try: cy.denoiser = 'OPENIMAGEDENOISE'
except Exception: pass
cy.max_bounces = 8; cy.diffuse_bounces = 4; cy.glossy_bounces = 4; cy.transmission_bounces = 8; cy.transparent_max_bounces = 8
cy.caustics_reflective = False; cy.caustics_refractive = False; cy.blur_glossy = 1.0
sc.render.resolution_x = RW; sc.render.resolution_y = RH; sc.render.resolution_percentage = 100
sc.view_settings.view_transform = 'AgX' if 'AgX' in [v.name for v in bpy.types.ColorManagedViewSettings.bl_rna.properties['view_transform'].enum_items] else 'Filmic'
try: sc.view_settings.look = 'AgX - Medium High Contrast' if sc.view_settings.view_transform == 'AgX' else 'Medium High Contrast'
except Exception: pass
sc.view_settings.exposure = 0.45
sc.render.image_settings.file_format = 'PNG'; sc.render.filepath = OUT
if not os.environ.get('ANIM'): bpy.ops.wm.save_as_mainfile(filepath=os.path.join(BASE, 'cena_apto.blend'))
bpy.ops.render.render(write_still=True)
print('RENDER_OK', OUT)
