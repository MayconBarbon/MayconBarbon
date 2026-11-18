"""Gera o blog do site a partir de docs/blog/11-artigos-original.md.

Uso: python3 blog/gerar_blog.py

Saída:
  site/blog/index.html                 (lista da série)
  site/blog/<slug>/index.html          (um por artigo, com SEO e dados estruturados)
  site/sitemap.xml e site/robots.txt

Ajustes de SEO (palavra-chave e título) e correções ficam nos dicionários abaixo,
com o motivo registrado em docs/palavras-chave.md. Fotos: blog/imagens.json.
Datas: blog/datas.json (só preencha com a data real de publicação).
"""
import html, json, re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
# Cada série tem a numeração própria (ARTIGO 01...); o "deslocamento" vira a numeração única do blog.
FONTES = [(RAIZ / "docs" / "blog" / "11-artigos-original.md", 0), (RAIZ / "docs" / "blog" / "6-artigos-original.md", 11)]
SITE = RAIZ / "site"
DOMINIO = "https://storymakeroficial.com.br"
ASSINATURA = "Método desenvolvido pela DocMe Comunicação."

# Pesquisa de 18/11/2026 (sugestões Google/YouTube). Ver docs/palavras-chave.md.
SEO = {
    3: dict(chave="storymaker mobile", titulo="Fotógrafo também pode ser Storymaker mobile",
            apoio_extra=["Storymaker para fotógrafos"]),
    5: dict(chave="storymaker para eventos", titulo="Storymaker para eventos: como montar uma sequência de stories"),
    10: dict(chave="storymaker evento corporativo", titulo="Storymaker em evento corporativo de grande porte"),
    16: dict(chave="microfone para casamento", titulo="Microfone para casamento: o backup de áudio do Storymaker",
             apoio_extra=["áudio para Storymaker em eventos", "como gravar áudio para vídeo"]),
    11: dict(chave="aftermovie o que é", titulo="Aftermovie: o que é e como se diferencia do Storymaker",
             apoio_extra=["diferença entre aftermovie e Storymaker", "aftermovie de evento"]),
}
# Correções de fato (o material já existe)
# Regra do fundador: nos artigos, eventos sempre com nomes genéricos (nunca o nome real do evento).
CORRECOES = {
    3: [("O teste do Igor no Congresso da CID Brasil", "O teste do Igor em um congresso nacional"),
        ("Durante uma cobertura do Congresso da CID Brasil,", "Durante a cobertura de um congresso nacional,")],
    5: [("No Celebra 2026, por exemplo,", "Em uma festa corporativa, por exemplo,")],
    6: [("O Storymaker Oficial terá uma planilha de custos para ajudar nesse cálculo.",
         "O Storymaker Oficial tem uma planilha de custos pronta para ajudar nesse cálculo.")],
    7: [("Na cobertura do Comida na Rua,", "Na cobertura de um circuito gastronômico,")],
    13: [("O Storymaker Oficial está organizando materiais para ensinar cada etapa com exemplos reais da DocMe. Acompanhe a construção da formação e escolha o primeiro tema para praticar.",
          "O Storymaker Oficial já reúne materiais práticos para cada etapa, com exemplos reais da DocMe. Escolha o primeiro tema e comece a praticar.")],
    10: [("Nesse evento, havia mais de 25 palestrantes vindos de diferentes regiões do Brasil,",
          "Nesse evento, com cerca de 13 mil pessoas, havia em média 25 palestrantes vindos de diferentes regiões do Brasil,")],
}
# Nomes de eventos que nunca podem aparecer nos artigos publicados (checagem automática)
PROIBIDOS = ["CID", "CIDE", "Celebra", "Comida na Rua", "Best-Seller", "Bestseller", "Expo ESG", "APEX", "Apex",
             "ACIPI", "Pirabir", "PiraBeer", "McDia", "Ronald", "Pizza do Bem", "Feijoada do Bem", "Dia de Doar",
             "Festa do Frango", "Festa da Batata", "Karla Corrente", "Carol Sampaio", "Aninha", "Engenho", "SIMESPI", "Festa da Imprensa", "PedalaPira", "PiraOlímpica", "Lilian Geraldini", "Chelso", "Jornada Caipira", "Carol e Daniel"]
# Termos de tendência pedidos pelo fundador, distribuídos sem repetição forçada.
TERMOS_TENDENCIA = ["cobertura mobile", "cobertura com celular", "storymaker mobile", "conteúdo em tempo real"]
TEXTO = {
    1: [("duas bases importantes do Storymaker.", "duas bases importantes do Storymaker e da cobertura mobile.")],
    2: [("fotografias e vídeos curtos.", "fotografias e vídeos curtos feitos com o celular.")],
    3: [("Essas habilidades ajudam muito no Storymaker,", "Essas habilidades ajudam muito no Storymaker mobile, a cobertura feita com o celular,"),
        ("para aprender Storymaker.", "para aprender cobertura mobile.")],
    4: [("por que o cliente quer contratar Storymaker.", "por que o cliente quer contratar Storymaker, a cobertura mobile do evento.")],
    5: [("Uma sequência simples pode apresentar o espaço", "Na cobertura mobile, uma sequência simples pode apresentar o espaço")],
    6: [("Antes da cobertura, pode haver", "Antes da cobertura mobile, pode haver")],
    7: [("pergunte quem vai selecionar e publicar os conteúdos.", "pergunte quem vai selecionar e publicar os conteúdos em tempo real."),
        ("o Storymaker pode se concentrar em captar e editar", "o Storymaker mobile pode se concentrar em captar e editar")],
    8: [("O Storymaker pode captar padrinhos", "Na cobertura com celular, o Storymaker pode captar padrinhos")],
    9: [("Em um congresso de negócios, a equipe fez briefing", "Em um congresso de negócios com cobertura mobile, a equipe fez briefing")],
    10: [("Era produzir conteúdo vertical em ritmo compatível com as redes", "Era produzir conteúdo em tempo real, vertical, em ritmo compatível com as redes"),
         ("Dois Storymakers trabalhavam com cinco celulares.", "Dois Storymakers mobile trabalhavam com cinco celulares.")],
    11: [("O Storymaker acompanha o evento enquanto ele acontece.", "O Storymaker faz a cobertura mobile do evento enquanto ele acontece.")],
    12: [("Durante o evento, o Storymaker observa", "Durante a cobertura mobile do evento, o Storymaker observa")],
    13: [("Uma formação de Storymaker precisa mostrar", "Uma formação de Storymaker mobile precisa mostrar")],
    14: [("Uma cobertura pode começar com os preparativos", "Uma cobertura com celular pode começar com os preparativos")],
    15: [("ajuda a equipe a registrar o que o casal espera", "ajuda a equipe de cobertura mobile a registrar o que o casal espera")],
    16: [("O celular perto da ação nem sempre capta a voz com clareza", "Na cobertura com celular, o aparelho perto da ação nem sempre capta a voz com clareza")],
    18: [("Ainda dá para fazer uma boa cobertura,", "Ainda dá para fazer uma boa cobertura mobile,")],
    17: [("Em trabalhos maiores, distribua a captação", "Em trabalhos maiores de cobertura mobile, distribua a captação")],
}
DESCRICAO = {
    1: "Veja como uma foto feita com o celular pode ser o primeiro exercício de cobertura mobile e abrir conversa com um comércio do seu bairro.",
    2: "Um caso da DocMe mostra como planejar uma sessão simples de cobertura com celular e gerar fotos e vídeos para um salão usar por meses.",
    3: "Veja como o olhar fotográfico ajuda na cobertura mobile: stories e vídeos feitos com o celular, com um exemplo real da DocMe.",
    4: "Perguntas para entender o objetivo do evento e as prioridades do cliente e planejar a cobertura mobile antes de ligar o celular.",
    5: "Abertura, pessoas, atrações e detalhes: a sequência de stories que faz a cobertura com celular de um evento contar uma história.",
    6: "Quanto cobrar por uma cobertura mobile: some briefing, pesquisa, deslocamento, horas no evento, edição e entrega antes do preço.",
    7: "Dois fluxos de publicação de conteúdo em tempo real usados pela DocMe: publicação pela equipe ou envio ao cliente para aprovar.",
    8: "Como adaptar a cobertura mobile de um casamento quando uma pessoa importante atrasa e a cerimônia precisa esperar.",
    9: "Um caso real de cobertura mobile: como a equipe da DocMe reagiu quando os horários das palestras mudaram sem aviso.",
    10: "Como a cobertura mobile se integra a um evento corporativo de grande porte, com transmissão, podcast, telões e várias equipes.",
    11: "Aftermovie: o que é e como se diferencia da cobertura mobile, que publica conteúdo em tempo real durante o evento.",
    12: "Storymaker: o que é e o que faz. O profissional da cobertura mobile que capta e organiza imagens para contar o evento em tempo real.",
    16: "Microfone para casamento e eventos: como planejar a fonte principal, o teste de som e o backup de áudio na cobertura com celular.",
}

# Links internos sugeridos -> artigos reais (por número)
LINKS = {1: [12, 4, 2], 2: [1, 4], 3: [5, 6], 4: [7, 8, 18], 5: [4, 7, 11], 6: [4, 1, 13], 7: [4, 5],
         8: [4, 5, 9, 15], 9: [4, 8, 6, 17], 10: [4, 9, 7], 11: [4, 5, 7, 12],
         12: [1, 4, 11], 13: [12, 4, 6], 18: [4, 7, 6], 14: [4, 5, 11], 15: [4, 7, 16], 16: [15, 17, 11], 17: [16, 5, 11]}
ETAPAS = [("A profissão", [12, 13]), ("Começar", [1, 2, 3]), ("Planejar e contar", [4, 5, 6]),
          ("Operar no evento", [7, 8, 9, 18]), ("Casamentos e festas", [14, 15]),
          ("Som, imprevistos e plano B", [16, 17]), ("Eventos de grande porte", [10, 11])]
# Ordem de leitura (numeração exibida ao leitor)
ORDEM = [n for _, nums in ETAPAS for n in nums]
POS = {n: i + 1 for i, n in enumerate(ORDEM)}
CAMPOS = {"Palavra-chave principal": "chave", "Termos de apoio": "apoio", "URL sugerida": "url",
          "Título SEO": "titulo_seo", "Meta description": "descricao", "Texto alternativo sugerido": "alt"}


def ler_artigos():
    artigos = []
    for fonte, desloc in FONTES:
        artigos += _ler(fonte, desloc)
    return artigos


def _ler(fonte, desloc):
    txt = fonte.read_text(encoding="utf-8").split("Referências para publicação")[0]
    blocos = re.split(r"^ARTIGO (\d+)\s*$", txt, flags=re.M)[1:]
    artigos = []
    for num, corpo in zip(blocos[::2], blocos[1::2]):
        n = int(num) + desloc
        linhas = [l.strip() for l in corpo.strip().splitlines() if l.strip()]
        a = dict(n=n, h1=linhas[0], blocos=[])
        i = 1
        while i < len(linhas) and linhas[i] != ASSINATURA:
            k, _, v = linhas[i].partition(":")
            if k in CAMPOS:
                a[CAMPOS[k]] = v.strip()
            i += 1
        for linha in linhas[i + 1:]:
            if linha.startswith("Links internos sugeridos:"):
                break
            for antes, depois in CORRECOES.get(n, []) + TEXTO.get(n, []):
                if antes in linha:
                    linha = linha.replace(antes, depois)
                    a.setdefault("aplicadas", set()).add(antes)
            titulo = len(linha) < 100 and not re.search(r"[.?!:]$", linha)
            a["blocos"].append(("h2" if titulo else "p", linha))
        faltou = [x for x, _ in CORRECOES.get(n, []) + TEXTO.get(n, []) if x not in a.get("aplicadas", set())]
        if faltou:
            raise SystemExit(f"ERRO: artigo {n:02d}, trecho não encontrado: {faltou}")
        if n in DESCRICAO:
            a["descricao"] = DESCRICAO[n]
        a["slug"] = a["url"].strip("/").split("/")[-1]
        a["apoio"] = [t.strip() for t in a["apoio"].split(";")] + TERMOS_TENDENCIA
        if n in SEO:
            a["chave_original"] = a["chave"]
            a["chave"] = SEO[n]["chave"]
            a["titulo_seo"] = SEO[n]["titulo"]
            a["apoio"] += SEO[n].get("apoio_extra", [])
        artigos.append(a)
    return artigos


def carregar(nome):
    p = RAIZ / "blog" / nome
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


E = html.escape


def topo(base):
    return f"""<a class="skip" href="#conteudo">Pular para o conteúdo</a>
<header class="topo rolou" id="topo"><div class="wrap topo__in">
<a class="logo" href="{base}index.html" aria-label="Storymaker Oficial, início"><span class="logo__mark" aria-hidden="true"></span><span class="logo__txt">Storymaker<b>Oficial</b></span></a>
<button class="menu-btn" aria-expanded="false" aria-controls="menu"><span class="sr">Abrir menu</span><span aria-hidden="true"></span></button>
<nav id="menu" class="menu" aria-label="Principal"><a href="{base}index.html#portfolio">Portfólio</a><a href="{base}index.html#como-fazemos">Como fazemos</a><a href="{base}blog/index.html">Blog</a><a class="btn btn--sm" href="{base}index.html#aprenda">Aprenda com a DocMe</a></nav>
</div></header>"""


def rodape(base):
    return f"""<footer class="rodape"><div class="wrap rodape__in"><div>
<a class="logo" href="{base}index.html"><span class="logo__mark" aria-hidden="true"></span><span class="logo__txt">Storymaker<b>Oficial</b></span></a>
<p class="assinatura" data-assinatura></p></div>
<nav aria-label="Rodapé" class="rodape__nav"><a href="{base}index.html#portfolio">Portfólio</a><a href="{base}blog/index.html">Blog</a><a href="{base}index.html#produtos">Materiais</a></nav>
<p class="rodape__mini">© <span data-ano></span> Storymaker Oficial. Conteúdos e portfólio DocMe Comunicação.</p></div></footer>
<script src="{base}assets/js/config.js"></script><script src="{base}assets/js/cases.js"></script><script src="{base}assets/js/main.js"></script>"""


def head(titulo, descricao, url, base, extra=""):
    return f"""<!doctype html><html lang="pt-BR" data-tema="laranja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(titulo if len(titulo) > 40 else titulo + " | Storymaker Oficial")}</title>
<meta name="description" content="{E(descricao)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:title" content="{E(titulo)}">
<meta property="og:description" content="{E(descricao)}"><meta property="og:url" content="{url}">
<meta property="og:locale" content="pt_BR"><meta property="og:site_name" content="Storymaker Oficial">
<meta name="theme-color" content="#e7570c">
<link rel="icon" href="{base}assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Sora:wght@500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}assets/css/style.css">{extra}</head>"""


def pagina_artigo(a, por_n, imagens, datas):
    base = "../../"
    url = f"{DOMINIO}/blog/{a['slug']}/"
    img = imagens.get(a["slug"])
    figura = (f'<figure class="art__img"><img src="{base}{E(img)}" alt="{E(a["alt"])}" width="1200" height="675"></figure>' if img else
              f'<figure class="art__img art__img--ph" role="img" aria-label="{E(a["alt"])}"><span><b>Foto a definir</b><br>{E(a["alt"])}</span></figure>')
    corpo, cta = [], None
    blocos = a["blocos"]
    for idx, (tipo, txt) in enumerate(blocos):
        if tipo == "h2" and txt == "Continue aprendendo":
            cta = " ".join(t for _, t in blocos[idx + 1:])
            break
        corpo.append(f"<{tipo}>{E(txt)}</{tipo}>")
    leia = "".join(f'<li><a href="../{por_n[m]["slug"]}/index.html"><span>Artigo {POS[m]:02d}</span>{E(por_n[m]["h1"])}</a></li>' for m in LINKS.get(a["n"], []))
    ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": a["titulo_seo"],
          "description": a["descricao"], "inLanguage": "pt-BR", "mainEntityOfPage": url,
          "keywords": ", ".join([a["chave"]] + a["apoio"]),
          "author": {"@type": "Organization", "name": "DocMe Comunicação"},
          "publisher": {"@type": "Organization", "name": "Storymaker Oficial", "logo": {"@type": "ImageObject", "url": f"{DOMINIO}/assets/img/favicon.svg"}},
          "isPartOf": {"@type": "CreativeWorkSeries", "name": "Storymaker Oficial: do primeiro conteúdo local ao grande evento"}}
    if img:
        ld["image"] = f"{DOMINIO}/{img}"
    d = datas.get(a["slug"], {})
    if d.get("publicado"):
        ld["datePublished"] = d["publicado"]
        ld["dateModified"] = d.get("atualizado", d["publicado"])
    data_html = f'<time datetime="{d["publicado"]}">{d["publicado"]}</time> · ' if d.get("publicado") else ""
    i = ORDEM.index(a["n"])
    prev_n = ORDEM[i - 1] if i > 0 else None
    next_n = ORDEM[i + 1] if i + 1 < len(ORDEM) else None
    nav = '<nav class="art__serie" aria-label="Série">' + \
          (f'<a href="../{por_n[prev_n]["slug"]}/index.html">← Artigo {POS[prev_n]:02d}</a>' if prev_n in por_n else "<span></span>") + \
          '<a href="../index.html">Todos os artigos</a>' + \
          (f'<a href="../{por_n[next_n]["slug"]}/index.html">Artigo {POS[next_n]:02d} →</a>' if next_n in por_n else "<span></span>") + "</nav>"
    extra = f'\n<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
    return head(a["titulo_seo"], a["descricao"], url, base, extra) + f"""<body>{topo(base)}
<main id="conteudo"><article class="art">
<header class="art__head"><div class="wrap estreito">
<p class="eyebrow"><a href="../index.html">Blog</a> · Artigo {POS[a['n']]:02d} de {len(por_n)}</p>
<h1>{E(a['h1'])}</h1>
<p class="art__resumo">{E(a['descricao'])}</p>
<p class="art__meta">{data_html}Por DocMe Comunicação · {ASSINATURA}</p>
</div></header>
<div class="wrap estreito art__corpo">{figura}{''.join(corpo)}
{f'<aside class="art__cta"><h2>Continue aprendendo</h2><p>{E(cta)}</p><p class="art__cta-sub">Materiais práticos de storymaker mobile e cobertura com celular, criados a partir das coberturas reais da DocMe.</p><a class="btn" href="{base}index.html#produtos">Ver os materiais</a></aside>' if cta else ''}
{f'<section class="art__leia"><h2>Leia também</h2><ul>{leia}</ul></section>' if leia else ''}
{nav}</div></article></main>
{rodape(base)}</body></html>"""


def pagina_indice(artigos, por_n):
    base = "../"
    url = f"{DOMINIO}/blog/"
    titulo = "Blog Storymaker mobile: cobertura com celular, do bairro ao grande evento"
    desc = f"{len(artigos)} artigos sobre storymaker e cobertura mobile: o que é, como começar, briefing, stories de evento, quanto cobrar, casamento, 15 anos, áudio e aftermovie."
    grupos = []
    for nome, nums in ETAPAS:
        itens = "".join(f'<li><a class="blog__item" href="{por_n[n]["slug"]}/index.html"><span class="blog__n">{POS[n]:02d}</span><span><b>{E(por_n[n]["h1"])}</b><small>{E(por_n[n]["descricao"])}</small></span></a></li>' for n in nums)
        grupos.append(f'<section class="blog__etapa"><h2>{nome}</h2><ol>{itens}</ol></section>')
    ld = {"@context": "https://schema.org", "@type": "Blog", "name": "Blog Storymaker Oficial", "url": url, "inLanguage": "pt-BR",
          "publisher": {"@type": "Organization", "name": "Storymaker Oficial"},
          "blogPost": [{"@type": "BlogPosting", "headline": a["titulo_seo"], "url": f"{DOMINIO}/blog/{a['slug']}/"} for a in artigos]}
    extra = f'\n<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
    return head(titulo, desc, url, base, extra).replace('content="article"', 'content="website"') + f"""<body>{topo(base)}
<main id="conteudo"><header class="art__head"><div class="wrap estreito">
<p class="eyebrow">Blog · Storymaker mobile e cobertura com celular</p><h1>Do primeiro conteúdo local à produção de um grande evento</h1>
<p class="lead">Uma série prática, baseada em situações reais da DocMe, para fotógrafos, videomakers e iniciantes que querem criar conteúdo mobile com intenção. Leia na ordem: cada artigo prepara o próximo.</p>
</div></header>
<div class="wrap estreito blog">{''.join(grupos)}</div></main>
{rodape(base)}</body></html>"""


if __name__ == "__main__":
    artigos = ler_artigos()
    por_n = {a["n"]: a for a in artigos}
    imagens, datas = carregar("imagens.json"), carregar("datas.json")
    for a in artigos:
        destino = SITE / "blog" / a["slug"]
        destino.mkdir(parents=True, exist_ok=True)
        (destino / "index.html").write_text(pagina_artigo(a, por_n, imagens, datas), encoding="utf-8")
        h2 = sum(1 for t, _ in a["blocos"] if t == "h2")
        print(f"{a['n']:02d} {a['slug']}  |  {len(a['titulo_seo'])} car. título  |  {len(a['descricao'])} car. descrição  |  {h2} subtítulos")
    (SITE / "blog" / "index.html").write_text(pagina_indice(artigos, por_n), encoding="utf-8")
    for a in artigos:
        texto = a["h1"] + " " + " ".join(t for _, t in a["blocos"])
        achados = [n for n in PROIBIDOS if re.search(r"\b" + re.escape(n) + r"\b", texto)]
        if achados:
            raise SystemExit(f"ERRO: artigo {a['n']:02d} cita evento pelo nome: {achados}")
    urls = [f"{DOMINIO}/", f"{DOMINIO}/blog/"] + [f"{DOMINIO}/blog/{a['slug']}/" for a in artigos]
    (SITE / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
                                      "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
    (SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {DOMINIO}/sitemap.xml\n", encoding="utf-8")
    print(f"ok: {len(artigos)} artigos, índice, sitemap e robots")
