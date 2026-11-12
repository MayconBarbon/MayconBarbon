import sys,re,json,html
S=sys.argv[1]; sys.path.insert(0,S)
from blog_articles import ARTS
home=open('/home/user/MayconBarbon/videoimovel-site/index.body.html').read()
css=re.search(r'<style>([\s\S]*?)</style>',home).group(1)
nav=re.search(r'<header class="nav">[\s\S]*?</header>',home).group(0)
foot=re.search(r'<footer>[\s\S]*?</footer>',home).group(0)
WA='https://wa.me/5519998612626?text=Ol%C3%A1!%20Vim%20pelo%20blog%20do%20V%C3%ADdeo%20Im%C3%B3vel%20e%20quero%20um%20or%C3%A7amento.'
nav=nav.replace('href="#topo"','href="/"').replace('href="#','href="/#')
nav=nav.replace('href="/#/blog/"','href="/blog/"')
if '/blog/' not in nav: nav=nav.replace('<li><a href="/#duvidas">Dúvidas</a></li>','<li><a href="/#duvidas">Dúvidas</a></li>\n      <li><a href="/blog/">Blog</a></li>')
blogcss='''
/* blog */
.post-wrap{max-width:760px;margin:0 auto;padding-left:max(20px,env(safe-area-inset-left,0px));padding-right:max(20px,env(safe-area-inset-right,0px))}
.crumb{font-size:.85rem;color:var(--muted);padding-top:28px}
.crumb a{color:var(--muted)}
.post-head{display:grid;gap:18px;padding-block:20px 28px}
.post-head h1{font-size:clamp(2.1rem,4.6vw,3.3rem)}
.post-cover{margin:0 auto 8px;max-width:1120px;padding-left:max(20px,env(safe-area-inset-left,0px));padding-right:max(20px,env(safe-area-inset-right,0px))}
.post-cover img{width:100%;height:auto;border-radius:var(--r);aspect-ratio:16/10;object-fit:cover}
.post-cover figcaption{font-size:.85rem;color:var(--muted);margin-top:10px;max-width:760px}
.post-body{padding-block:28px 40px;display:grid;gap:18px;font-size:1.08rem;line-height:1.7}
.post-body h2{font-size:clamp(1.45rem,2.6vw,1.9rem);margin-top:22px}
.post-body p{max-width:68ch}
.cta-box{background:var(--ink);color:var(--ink-fg);border-radius:var(--r);padding:32px 28px;display:grid;gap:14px;margin-block:12px 8px}
.cta-box h2{margin:0;font-size:1.5rem}.cta-box p{color:var(--ink-muted)}
.cta-box .actions .btn-primary{--brand:#f5f5f7;--brand-fg:#0d1a2e}
.cta-box .btn-ghost{color:var(--ink-fg);border-color:rgba(255,255,255,.3)}
.related{padding-block:24px 72px}
.related h2{font-size:1.4rem;margin-bottom:18px}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.card{background:var(--card);border:1px solid var(--line);border-radius:18px;overflow:hidden;display:grid;grid-template-rows:auto 1fr;text-decoration:none;color:inherit;min-width:0;transition:transform .2s ease}
.card:hover{transform:translateY(-2px)}
.card img{width:100%;height:auto;aspect-ratio:16/10;object-fit:cover}
.card div{padding:18px 18px 22px;display:grid;gap:8px;align-content:start}
.card h3{font-size:1.08rem;line-height:1.25}
.card p{font-size:.93rem;color:var(--muted)}
.card span{font-weight:600;color:var(--accent);font-size:.92rem}
@media (max-width:900px){.cards{grid-template-columns:1fr 1fr}}
@media (max-width:560px){.cards{grid-template-columns:1fr}}
'''
def style(): return '<style>\nbody.elementor-template-canvas{margin:0}\n'+css+blogcss+'</style>\n'
def excerpt(a):
    t=a['intro'][0]; s=re.split(r'(?<=\.)\s',t); return s[0]
def img(a,U,eager=False,sizes='(max-width: 1120px) 100vw, 1120px'):
    n=a['n']; return f'<img src="{U["blog-%d-1600.webp"%n]}" srcset="{U["blog-%d-800.webp"%n]} 800w, {U["blog-%d-1600.webp"%n]} 1600w" sizes="{sizes}" width="1600" height="1000" alt="{html.escape(a["alt"])}" {"fetchpriority=\"high\"" if eager else "loading=\"lazy\""} decoding="async">'
def card(a,U,link):
    return f'<a class="card" href="{link}">{img(a,U,False,"(max-width: 560px) 100vw, (max-width: 900px) 50vw, 360px")}<div><h3>{html.escape(a["h1"])}</h3><p>{html.escape(excerpt(a))}</p><span>Ler artigo →</span></div></a>'
def article(a,U,L,url,date,logo):
    body=''.join(f'<p>{html.escape(p)}</p>' for p in a['intro'])
    for h,ps in a['sections']: body+=f'<h2>{html.escape(h)}</h2>'+''.join(f'<p>{html.escape(p)}</p>' for p in ps)
    body+=f'<aside class="cta-box" aria-label="Fale com o Vídeo Imóvel"><h2>{html.escape(a["cta_title"])}</h2><p>{html.escape(a["cta"])}</p><div class="actions"><a class="btn btn-primary" href="{WA}" target="_blank" rel="noopener">Falar no WhatsApp</a><a class="btn btn-ghost" href="/#servicos">Ver os serviços</a></div></aside>'
    rel=''.join(card(next(x for x in ARTS if x['n']==r),U,L[r]) for r in a['related'])
    ld={"@context":"https://schema.org","@type":"BlogPosting","headline":a['h1'],"description":a['meta'],"image":[U['blog-%d-og.jpg'%a['n']],U['blog-%d-1600.webp'%a['n']]],"datePublished":date,"dateModified":date,"mainEntityOfPage":url,"inLanguage":"pt-BR","author":{"@type":"Organization","name":"Vídeo Imóvel","url":"https://videoimovel.com.br/"},"publisher":{"@type":"Organization","name":"Vídeo Imóvel","logo":{"@type":"ImageObject","url":logo}}}
    return (style()+'<script type="application/ld+json">'+json.dumps(ld,ensure_ascii=False)+'</script>\n'+nav+
      f'\n<main id="topo"><div class="post-wrap"><nav class="crumb" aria-label="Você está em"><a href="/">Início</a> › <a href="/blog/">Blog</a></nav>'
      f'<header class="post-head"><p class="eyebrow">Blog Vídeo Imóvel</p><h1>{html.escape(a["h1"])}</h1><p class="lead">{html.escape(excerpt(a))}</p></header></div>'
      f'<figure class="post-cover">{img(a,U,True)}<figcaption>{html.escape(a["caption"])}</figcaption></figure>'
      f'<article class="post-wrap post-body">{body}</article>'
      f'<section class="wrap related" aria-labelledby="rel"><h2 id="rel">Leia também</h2><div class="cards">{rel}</div></section></main>\n'+foot)
def listing(U,L):
    cards=''.join(card(a,U,L[a['n']]) for a in ARTS)
    ld={"@context":"https://schema.org","@type":"Blog","name":"Blog Vídeo Imóvel","url":"https://videoimovel.com.br/blog/","inLanguage":"pt-BR","publisher":{"@type":"Organization","name":"Vídeo Imóvel","url":"https://videoimovel.com.br/"},"blogPost":[{"@type":"BlogPosting","headline":a['h1'],"url":L[a['n']]} for a in ARTS]}
    return (style()+'<script type="application/ld+json">'+json.dumps(ld,ensure_ascii=False)+'</script>\n'+nav+
      '\n<main id="topo"><section aria-labelledby="h1"><div class="wrap"><div class="head"><p class="eyebrow">Blog</p><h1 id="h1" style="font-size:clamp(2.4rem,5vw,3.8rem)">Blog Vídeo Imóvel</h1>'
      '<p class="lead">Dicas práticas para preparar, fotografar, filmar e divulgar imóveis e espaços comerciais, com a imagem fiel ao que eles são.</p></div>'
      f'<div class="cards">{cards}</div></div></section>'
      f'<section class="dark final" aria-labelledby="h-final"><div class="wrap"><p class="eyebrow">Vamos começar</p><h2 id="h-final">A melhor imagem do seu imóvel está aqui.</h2><p class="lead">Envie as fotos pelo WhatsApp e receba a proposta com a curadoria das imagens.</p><div class="contact"><a class="btn btn-primary" style="--brand:#f5f5f7;--brand-fg:#0d1a2e" href="{WA}" target="_blank" rel="noopener">Falar no WhatsApp</a><span class="num">+55 19 99861-2626</span></div></div></section></main>\n'+foot)
