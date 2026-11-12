"""Monta um episodio a partir da sequencia 'lote 2' (XML FCP7 do Premiere) + transcricao.
Uso: python3 build_ep.py lote2.xml transcricao.txt episodio.json saida.xml
"""
import sys, json, copy, re
import xml.etree.ElementTree as ET

SRC, TXT, CFG, OUT = sys.argv[1:5]
cfg = json.load(open(CFG))
FPS = 30  # timebase NTSC (29,97)

def tc2f(tc):  # drop-frame 29,97
    h, m, s, f = map(int, re.split('[;:]', tc))
    tm = h * 60 + m
    return (h * 3600 + m * 60 + s) * 30 + f - 2 * (tm - tm // 10)

# --- transcricao
lines = open(TXT, encoding='utf-8').read().splitlines()
segs = []
for i, l in enumerate(lines):
    m = re.match(r'(\d\d;\d\d;\d\d;\d\d) - (\d\d;\d\d;\d\d;\d\d)', l.strip())
    if m:
        segs.append((tc2f(m[1]), tc2f(m[2]), lines[i + 1].strip() if i + 1 < len(lines) else ''))

tree = ET.parse(SRC); root = tree.getroot()
seq = root.find('sequence')
vtracks = seq.findall('media/video/track')
atracks = seq.findall('media/audio/track')
src_v = vtracks[0].findall('clipitem')
src_a1 = atracks[0].findall('clipitem'); src_a2 = atracks[1].findall('clipitem')
clips = [(int(c.findtext('start')), int(c.findtext('end')), int(c.findtext('in'))) for c in src_v]

def locate(f):
    for k, (s, e, i) in enumerate(clips):
        if s <= f < e: return k
    raise ValueError(f)

# --- trechos -> pedacos (corta pausas longas dentro do mesmo take)
GAP_KEEP, PAD = cfg.get('gap_keep', 18), cfg.get('pad', 5)
pieces = []  # (seq_in, seq_out, zoom_flag, label)
for blk in cfg['blocks']:
    a, b = tc2f(blk['from']), tc2f(blk['to'])
    ss = [s for s in segs if s[0] >= a - 2 and s[1] <= b + 2]
    if blk.get('raw'): ss = [(a, b, blk.get('label', ''))]
    cur = None; bp = []
    for s0, s1, t in ss:
        if cur and s0 - cur[1] <= GAP_KEEP: cur[1] = s1; cur[2] += ' ' + t
        else:
            if cur: bp.append(cur)
            cur = [s0, s1, t]
    bp.append(cur)
    for j, p in enumerate(bp): p.append(bool(blk.get('zoom_in')) and j == 0)
    pieces += bp
# padding sem invadir vizinhos
for i, p in enumerate(pieces):
    lo = pieces[i - 1][1] if i and pieces[i - 1][1] <= p[0] and pieces[i-1][1] > p[0] - 60 else -1
    p[0] = max(p[0] - PAD, lo)
    nxt = pieces[i + 1][0] if i + 1 < len(pieces) and pieces[i + 1][0] >= p[1] and pieces[i+1][0] < p[1] + 60 else 10**9
    p[1] = min(p[1] + PAD, nxt)

# divide pedacos que cruzam fronteira de clipe
final = []
for s0, s1, t, z in pieces:
    while locate(s0) != locate(s1 - 1):
        e = clips[locate(s0)][1]; final.append((s0, e, t, z)); s0 = e
    final.append((s0, s1, t, z))

# --- monta nova timeline
LEAD, TAIL = round(cfg.get('intro_s', 8) * 29.97), round(cfg.get('outro_s', 4) * 29.97)
WIDE, CLOSE = cfg.get('wide', 90), cfg.get('close', 105)

def motion(scale0, scale1=None, kin=0, kout=0):
    f = ET.Element('filter'); e = ET.SubElement(f, 'effect')
    for k, v in [('name', 'Basic Motion'), ('effectid', 'basic'), ('effectcategory', 'motion'),
                 ('effecttype', 'motion'), ('mediatype', 'video')]:
        ET.SubElement(e, k).text = v
    p = ET.SubElement(e, 'parameter', authoringApp='PremierePro')
    for k, v in [('parameterid', 'scale'), ('name', 'Scale'), ('valuemin', '0'), ('valuemax', '1000')]:
        ET.SubElement(p, k).text = v
    ET.SubElement(p, 'value').text = str(scale0)
    if scale1 is not None:
        for w, v in [(kin, scale0), (kout, scale1)]:
            kf = ET.SubElement(p, 'keyframe'); ET.SubElement(kf, 'when').text = str(w); ET.SubElement(kf, 'value').text = str(v)
    return f

for tr in (vtracks + atracks):
    for c in tr.findall('clipitem'): tr.remove(c)

emitted_files = set(); pos = LEAD; n = 0; close = False; report = []
prev_end = None
for s0, s1, t, z in final:
    k = locate(s0); cs, ce, cin = clips[k]
    src_in = cin + (s0 - cs); dur = s1 - s0
    # alterna zoom a cada corte (nao alterna se for continuacao direta do mesmo trecho)
    if prev_end is not None and prev_end != s0: close = not close
    prev_end = s1
    n += 1
    ids = {'v': f'clipitem-v{n}', 'a1': f'clipitem-a{n}', 'a2': f'clipitem-b{n}'}
    for key, srcl, tr in [('v', src_v, vtracks[0]), ('a1', src_a1, atracks[0]), ('a2', src_a2, atracks[1])]:
        c = copy.deepcopy(srcl[k]); c.set('id', ids[key])
        for tag in ('pproTicksIn', 'pproTicksOut'):
            e = c.find(tag); c.remove(e) if e is not None else None
        c.find('start').text = str(pos); c.find('end').text = str(pos + dur)
        c.find('in').text = str(src_in); c.find('out').text = str(src_in + dur)
        fe = c.find('file'); fid = fe.get('id')
        if fid in emitted_files:
            for ch in list(fe): fe.remove(ch)
        else:
            if len(fe) == 0:  # pega definicao completa do arquivo
                full = next(x for x in root.iter('file') if x.get('id') == fid and len(x))
                c.remove(fe); fe = copy.deepcopy(full); c.insert(list(c).index(c.find('out')) + 1, fe)
            emitted_files.add(fid)
        for l in c.findall('link'): c.remove(l)
        for lk, mt, ti in [('v', 'video', 1), ('a1', 'audio', 1), ('a2', 'audio', 2)]:
            L = ET.SubElement(c, 'link')
            ET.SubElement(L, 'linkclipref').text = ids[lk]; ET.SubElement(L, 'mediatype').text = mt
            ET.SubElement(L, 'trackindex').text = str(ti); ET.SubElement(L, 'clipindex').text = str(n)
            if mt == 'audio': ET.SubElement(L, 'groupindex').text = '1'
        if key == 'v':
            if z:
                c.append(motion(WIDE, CLOSE, src_in, src_in + dur - 1)); close = True
            else:
                c.append(motion(CLOSE if close else WIDE))
        tr.append(c)
    report.append((pos, dur, k, 'ZOOM' if z else ('close' if close else 'aberto'), t))
    pos += dur

total = pos + TAIL
seq.find('duration').text = str(total)
seq.find('name').text = cfg['name']
seq.find('uuid').text = cfg.get('uuid', '00000000-0000-4000-8000-0000000000%02d' % cfg.get('ep', 1))
for a in list(seq.attrib):
    if a.startswith(('MZ.Work', 'MZ.EditLine', 'Monitor.', 'TL.SQTimePerPixel')): del seq.attrib[a]
# marcadores para as vinhetas
for nm, st in [('VINHETA ABERTURA (8s)', 0), ('VINHETA FECHAMENTO (4s)', pos)]:
    mk = ET.SubElement(seq, 'marker')
    ET.SubElement(mk, 'name').text = nm; ET.SubElement(mk, 'comment').text = ''
    ET.SubElement(mk, 'in').text = str(st); ET.SubElement(mk, 'out').text = '-1'
tree.write(OUT, encoding='UTF-8', xml_declaration=True)
txt = open(OUT, encoding='utf-8').read().replace("<?xml version='1.0' encoding='UTF-8'?>", '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>')
open(OUT, 'w', encoding='utf-8').write(txt)

def f2s(f): s = f / 29.97; return f'{int(s // 60)}:{s % 60:05.2f}'
for p, d, k, z, t in report:
    print(f'{f2s(p):>8} +{d/29.97:5.1f}s  clip{3728+k}  {z:6}  {t[:90]}')
print('TOTAL', f2s(total), '| fala', f2s(pos - LEAD))
