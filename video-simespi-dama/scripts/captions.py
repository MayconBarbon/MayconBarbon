"""Legendas no estilo da referência (Silvana Marques): frase curta centralizada embaixo,
palavra-chave em serifada itálica grande + demais palavras em sans limpa; branco, sem caixa, sombra suave.
Tempo de cada palavra vem da transcrição da própria locução."""
import os, sys, json, re, unicodedata, difflib, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S = os.path.dirname(os.path.abspath(__file__))
VO = f"{S}/vo9"; F = f"{S}/fonts"; W, H, FPS = 1920, 1080, 30
END = float(sys.argv[2]) if len(sys.argv) > 2 else 89.9
starts = json.load(open(f"{S}/timeline10.json"))["vo_starts"]

SCRIPT = [
 "A história de Piracicaba carrega as marcas da indústria! Uma trajetória construída pelo trabalho de gerações.",
 "Na fábrica, cada etapa revela o que muitos não veem. Máquinas em movimento, processos cuidadosamente executados, profissionais especializados.",
 "É a expressão de uma extensa cadeia produtiva, que conecta empresas, movimenta diferentes setores, promove crescimento, renda e novas oportunidades!",
 "Nesse contexto, a indústria cervejeira também se destaca, e encontra no CPL Cerva, projeto do SIMESPI, um importante incentivo à integração e ao fortalecimento de sua cadeia produtiva.",
 "Foi dessa conexão que nasceu a parceria do SIMESPI com a Dama Bier: indústria piracicabana reconhecida pela excelência de sua produção, onde o rigor técnico se revela em cada detalhe, com precisão, tecnologia e compromisso com a qualidade.",
 "E o resultado está neste brinde, preparado especialmente para você, associado ao SIMESPI! Um produto que carrega a identidade e a força industrial da nossa região.",
 "Porque, somos a indústria! Fazemos o trabalho que transforma, todos os dias, o presente e o futuro de Piracicaba.",
 "SIMESPI. Há 35 anos, representando e fortalecendo a indústria!",
]
KEY = {"história", "indústria", "gerações", "fábrica", "veem", "máquinas", "especializados", "cadeia", "conecta",
       "crescimento", "oportunidades", "cervejeira", "cerva", "fortalecimento", "parceria", "bier", "excelência",
       "detalhe", "tecnologia", "qualidade", "brinde", "você", "identidade", "força", "indústria", "transforma",
       "futuro", "piracicaba", "35", "fortalecendo", "simespi", "precisão", "integração", "região", "trajetória"}
PRIORITY = ["parceria", "bier", "brinde", "indústria", "cervejeira", "35", "fortalecendo", "excelência", "qualidade",
            "tecnologia", "precisão", "cerva", "transforma", "futuro", "oportunidades", "crescimento", "cadeia",
            "gerações", "história", "fábrica", "máquinas", "especializados", "você", "identidade", "força", "veem",
            "detalhe", "conecta", "integração", "fortalecimento", "região", "trajetória", "piracicaba", "simespi"]

def norm(w):
    w = unicodedata.normalize("NFD", w.lower()); w = "".join(c for c in w if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", w)

def asr_words(path):
    from faster_whisper import WhisperModel
    import soundfile as sf
    global _m
    try: _m
    except NameError: _m = WhisperModel("small", device="cpu", compute_type="int8")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-ar", "16000", "-ac", "1", "/tmp/_c.wav"], check=True)
    x, _ = sf.read("/tmp/_c.wav")
    segs, _ = _m.transcribe(x.astype(np.float32), language="pt", word_timestamps=True)
    return [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]

def align(script_words, asr):
    a = [norm(w) for w in script_words]; b = [norm(w) for w, _, _ in asr]
    # equivalências fonéticas da locução
    b = [{"cimesp": "simespi", "simesp": "simespi", "cmesp": "simespi", "beer": "bier", "serva": "cerva", "porque": "porque", "mesp": "simespi"}.get(x, x) for x in b]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    t = [None] * len(a)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal" or (op == "replace" and i2 - i1 == j2 - j1):
            for k in range(i2 - i1): t[i1 + k] = (asr[j1 + k][1], asr[j1 + k][2])
        elif op == "replace":
            s0, s1 = asr[j1][1], asr[j2 - 1][2]
            for k in range(i2 - i1): t[i1 + k] = (s0 + (s1 - s0) * k / (i2 - i1), s0 + (s1 - s0) * (k + 1) / (i2 - i1))
    # interpolar lacunas
    for i in range(len(t)):
        if t[i] is None:
            p = next((t[j][1] for j in range(i - 1, -1, -1) if t[j]), 0.0)
            q = next((t[j][0] for j in range(i + 1, len(t)) if t[j]), p + 0.3)
            t[i] = (p, max(p + 0.05, q))
    return t

STOP = {"a","o","as","os","e","de","da","do","das","dos","se","no","na","que","sua","com","em","um","uma","ao","pela","pelo","para","nossa","cada","muitos","não"}
def chunks(words, times, maxw=5, maxdur=2.4):
    out = []; cur = []
    for w, (a, b) in zip(words, times):
        cur.append((w, a, b))
        brk = re.search(r"[.!?:;,]$", w) and len(cur) >= 2
        weak = norm(w) in {norm(x) for x in STOP} or norm(w) in ("cpl", "dama")
        over = len(cur) >= maxw or (cur[-1][2] - cur[0][1] > maxdur)
        glue = norm(w) in ("cpl", "dama")
        if not glue and (brk or (over and (not weak or len(cur) >= maxw + 3))):
            out.append(cur); cur = []
    if cur:
        if out and len(cur) <= 1: out[-1] += cur
        else: out.append(cur)
    return out

SANS = ImageFont.truetype(f"{F}/Montserrat-Medium.ttf", 50)
SERIF = ImageFont.truetype(f"{F}/pf-500-italic.woff", 84)
def render_chunk(ch, dark=False):
    words = [w for w, _, _ in ch]
    # escolhe a palavra-destaque pela prioridade
    hi = None
    for p in PRIORITY:
        for i, w in enumerate(words):
            if norm(w) == norm(p): hi = i; break
        if hi is not None: break
    disp = [w.rstrip(",;:") if i < len(words) - 1 else w.rstrip(",;:") for i, w in enumerate(words)]
    img = Image.new("RGBA", (W, 220), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    parts = [(w, SERIF if i == hi else SANS) for i, w in enumerate(disp)]
    sp = d.textlength(" ", font=SANS)
    widths = [d.textlength(w, font=f) for w, f in parts]
    tot = sum(widths) + sp * 1.2 * (len(parts) - 1); x = (W - tot) / 2; base = 150
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    for (w, f), wd in zip(parts, widths):
        ld.text((x, base), w, font=f, fill=((10, 54, 67, 255) if dark else (255, 255, 255, 255)), anchor="ls"); x += wd + sp * 1.2
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 0 if dark else 170), (0, 0), lay.split()[3])
    sh = sh.filter(ImageFilter.GaussianBlur(5))
    sh2 = Image.new("RGBA", img.size, (0, 0, 0, 0)); sh2.alpha_composite(sh, (2, 3))
    sh2.alpha_composite(lay)
    return sh2

def main():
    out = sys.argv[1]
    allc = []
    for k in range(8):
        words = SCRIPT[k].split()
        asr = asr_words(f"{VO}/a_{k+1}.wav")
        times = align(words, asr)
        for ch in chunks(words, times):
            t0 = starts[k] + ch[0][1] - 0.05; t1 = starts[k] + ch[-1][2] + 0.15
            allc.append([t0, t1, ch])
    # sem sobreposição: cada legenda termina quando a próxima começa
    for i in range(len(allc) - 1): allc[i][1] = min(allc[i][1] + 0.25, allc[i + 1][0])
    json.dump([(round(a, 2), round(b, 2), " ".join(w for w, _, _ in c)) for a, b, c in allc], open(f"{S}/captions10.json", "w"), ensure_ascii=False, indent=0)
    card = [x[0] for x in json.load(open(f"{S}/timeline10.json"))["shots"] if x[1] == "CARD"][0]
    imgs = [render_chunk(c, a >= card - 0.3) for a, _, c in allc]
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-c:v", "qtrle", "-pix_fmt", "argb", out], stdin=subprocess.PIPE)
    blank = np.zeros((H, W, 4), np.uint8); y0 = H - 220 - 40
    for fi in range(int(END * FPS)):
        t = fi / FPS; fr = blank
        for (a, b, c), im in zip(allc, imgs):
            if a <= t < b:
                p = min(1, (t - a) / 0.14); q = min(1, (b - t) / 0.12); al = min(p, q)
                dy = int((1 - p) * 14)
                arr = np.array(im).astype(np.float32); arr[:, :, 3] *= al
                fr = blank.copy(); fr[y0 + dy:y0 + dy + 220] = arr.astype(np.uint8)
                break
        enc.stdin.write(fr.tobytes())
    enc.stdin.close(); enc.wait()
    print("legendas:", len(allc))

if __name__ == "__main__":
    main()
