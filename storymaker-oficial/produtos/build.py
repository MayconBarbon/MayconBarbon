"""Gera os PDFs diagramados dos produtos Storymaker Oficial.

Uso:  python3 produtos/build.py            (gera todos)
      python3 produtos/build.py ebook-02   (gera só um)

Entrada: os textos em ebooks/*.md
Saída:   produtos/pdf/*.pdf  e  produtos/html/*.html (versão para conferir no navegador)

Precisa de: pip install markdown  e  Playwright com Chromium (node).
"""
import json, re, subprocess, sys
from pathlib import Path
import markdown

sys.path.insert(0, str(Path(__file__).parent))
import ilustracoes as il

RAIZ = Path(__file__).resolve().parent.parent
EBOOKS = RAIZ / "ebooks"
OUT_HTML = RAIZ / "produtos" / "html"
OUT_PDF = RAIZ / "produtos" / "pdf"
CSS = (RAIZ / "produtos" / "produto.css").read_text(encoding="utf-8")
ASSINATURA = "Método desenvolvido pela DocMe Comunicação."

PRODUTOS = {
    "ebook-02": dict(fonte="ebook-02-briefing-e-planejamento.md", formato="ebook",
                     titulo="Do briefing à história",
                     subtitulo="Como planejar uma cobertura de Storymaker antes de ligar a câmera",
                     selo="E-book 2", ilustracoes=il.EBOOK2),
    "checklist-pre-producao": dict(fonte="checklist-pre-producao.md", formato="ficha",
                                   titulo="Checklist de pré-produção", selo="Checklist"),
    "checklist-de-cobertura": dict(fonte="checklist-de-cobertura.md", formato="ficha",
                                   titulo="Checklist de cobertura", selo="Checklist"),
    "checklist-pos-producao": dict(fonte="checklist-pos-producao.md", formato="ficha",
                                   titulo="Checklist de pós-produção", selo="Checklist"),
    "checklist-de-audio": dict(fonte="checklist-de-audio.md", formato="ficha",
                               titulo="Checklist de áudio", selo="Checklist"),
    "roteiro-de-fim-de-ano": dict(fonte="roteiro-de-fim-de-ano.md", formato="ficha",
                                  titulo="Roteiro de fim de ano", selo="Roteiro sazonal"),
    "checklist-evento-amanha": dict(fonte="checklist-evento-amanha.md", formato="ficha",
                                    titulo="Seu evento é amanhã", selo="Checklist gratuito"),
    "modelo-de-briefing": dict(fonte="modelo-de-briefing.md", formato="ficha",
                               titulo="Modelo de briefing", selo="Modelo"),
    "modelo-de-contrato": dict(fonte="modelo-de-contrato.md", formato="ficha",
                               titulo="Modelo de contrato", selo="Contrato"),
}


def texto_puro(html):
    return re.sub(r"<[^>]+>", "", html).strip()


def md_para_html(md):
    return markdown.markdown(md, extensions=["tables", "sane_lists"])


def tirar_cabecalho(md):
    """Remove o bloco inicial (título, marca, assinatura) até a primeira linha '---'; a capa/cabeçalho substitui."""
    partes = re.split(r"^---\s*$", md, maxsplit=1, flags=re.M)
    return partes[1] if len(partes) == 2 else md


def pos_processar(html, ilustracoes=None):
    # [PREENCHER ...] em parágrafo próprio vira um espaço reservado para material da DocMe
    html = re.sub(r"<p>\s*\[(PREENCHER[^\]]*)\]\s*</p>",
                  r'<div class="reservado"><span class="reservado__ico" aria-hidden="true"></span><div><b>Espaço para material DocMe</b><br>\1</div></div>', html)
    html = re.sub(r"\[(PREENCHER[^\]]*|CONFIRMAR[^\]]*)\]", r'<mark class="falta">[\1]</mark>', html)
    # caixas de marcação
    html = re.sub(r"<li>\s*\[ \]\s*", '<li class="check"><span class="box" aria-hidden="true"></span>', html)
    html = re.sub(r'(<li class="check"><span class="box" aria-hidden="true"></span>)(.*?)</li>', r'\1<span>\2</span></li>', html, flags=re.S)
    html = html.replace("( )", '<span class="opt" aria-hidden="true"></span>')
    html = re.sub(r"<hr\s*/?>", "", html)

    # capítulos: abertura em página nova, com número grande
    def cap(m):
        n, titulo = m.group(1), m.group(2)
        return (f'<section class="capitulo"><div class="cap__num">{int(n):02d}</div>'
                f'<p class="cap__rot">Capítulo {n}</p><h2>{titulo}</h2></section>')
    html = re.sub(r"<h2>Capítulo (\d+)\s*[—-]\s*(.+?)</h2>", cap, html)
    html = re.sub(r"<h2>(Para quem é este e-book|Antes de começar[^<]*|Sumário)</h2>",
                  r'<h2 class="quebra">\1</h2>', html)

    # ilustrações depois do título correspondente (primeira ocorrência)
    for titulo, func in (ilustracoes or {}).items():
        padrao = re.compile(r"(<h[234][^>]*>" + re.escape(titulo) + r"</h[234]>(?:</section>)?)")
        if not padrao.search(html):
            print(f"  ! ilustração sem lugar: {titulo}")
            continue
        html = padrao.sub(lambda m: m.group(1) + func(), html, count=1)
    return html


CAPA_SVG = """<svg class="capa__phone" viewBox="0 0 200 360" aria-hidden="true">
<rect x="6" y="6" width="188" height="348" rx="30" fill="#2b2a30"/>
<rect x="16" y="16" width="168" height="328" rx="22" fill="#3a393f"/>
<g fill="#fff"><rect x="28" y="30" width="34" height="3" rx="1.5"/><rect x="66" y="30" width="34" height="3" rx="1.5"/><rect x="104" y="30" width="16" height="3" rx="1.5"/></g>
<rect x="104" y="30" width="34" height="3" rx="1.5" fill="#fff" opacity=".35"/><rect x="142" y="30" width="30" height="3" rx="1.5" fill="#fff" opacity=".35"/>
<rect x="28" y="44" width="44" height="14" rx="3" fill="#fff"/><text x="50" y="54.5" font-size="8" font-weight="800" fill="#c2410c" text-anchor="middle" style="font-family:Inter">AO VIVO</text>
<rect x="28" y="230" width="120" height="10" rx="5" fill="#fff" opacity=".9"/><rect x="28" y="248" width="86" height="10" rx="5" fill="#fff" opacity=".6"/>
<circle cx="100" cy="140" r="38" fill="none" stroke="#e7570c" stroke-width="10"/><circle cx="100" cy="140" r="14" fill="#e7570c"/>
</svg>"""


def pagina(cfg, corpo):
    if cfg["formato"] == "ebook":
        topo = (f'<section class="capa"><div class="capa__marca"><span class="capa__logo"></span>Storymaker<b>Oficial</b></div>'
                f'<p class="capa__selo">{cfg["selo"]}</p><h1>{cfg["titulo"]}</h1><p class="capa__sub">{cfg["subtitulo"]}</p>'
                f'{CAPA_SVG}<p class="capa__assina">{ASSINATURA}</p></section>')
    else:
        topo = (f'<header class="ficha__topo"><div><p class="ficha__selo">{cfg["selo"]} · Storymaker Oficial</p>'
                f'<h1>{cfg["titulo"]}</h1></div><p class="ficha__assina">{ASSINATURA}</p></header>')
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<title>{cfg['titulo']} | Storymaker Oficial</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body class="fmt-{cfg['formato']}">{topo}<main>{corpo}</main></body></html>"""


def gerar(chave):
    cfg = PRODUTOS[chave]
    fonte = EBOOKS / cfg["fonte"]
    if not fonte.exists():
        print(f"- {chave}: texto ainda não existe ({fonte.name})"); return None
    md = tirar_cabecalho(fonte.read_text(encoding="utf-8"))
    if cfg["formato"] == "ficha":
        md = re.sub(r"^#\s.*$", "", md, count=1, flags=re.M)
    # lista colada num parágrafo (sem linha em branco) vira lista de verdade
    md = re.sub(r"^((?!\s*(?:[-*+] |\d+\. |\||>|#)).+)\n(?=[-*] )", r"\1\n\n", md, flags=re.M)
    html = pos_processar(md_para_html(md), cfg.get("ilustracoes"))
    OUT_HTML.mkdir(parents=True, exist_ok=True); OUT_PDF.mkdir(parents=True, exist_ok=True)
    h = OUT_HTML / f"{chave}.html"
    h.write_text(pagina(cfg, html), encoding="utf-8")
    return h, OUT_PDF / f"{chave}.pdf", cfg["formato"]


NODE = r"""
const { chromium } = require('playwright');
(async () => {
  const jobs = JSON.parse(process.argv[1]); const b = await chromium.launch();
  for (const [html, pdf] of jobs) {
    const p = await b.newPage();
    await p.goto('file://' + html, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.pdf({ path: pdf, preferCSSPageSize: true, printBackground: true });
    await p.close();
  }
  await b.close();
})();
"""

if __name__ == "__main__":
    alvos = sys.argv[1:] or list(PRODUTOS)
    jobs = []
    for a in alvos:
        r = gerar(a)
        if r: jobs.append([str(r[0]), str(r[1])])
    subprocess.run(["node", "-e", NODE, json.dumps(jobs)], check=True)
    for _, pdf in jobs:
        n = subprocess.run(["python3", "-c", f"import re;d=open('{pdf}','rb').read();print(len(re.findall(rb'/Type\\s*/Page[^s]', d)))"],
                           capture_output=True, text=True).stdout.strip()
        print(f"ok  {Path(pdf).name}: {n} páginas")
