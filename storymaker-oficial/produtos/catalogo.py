"""Catálogo de produtos Storymaker Oficial: gera produtos/catalogo/catalogo.html, .pdf e .png.

Regra de preço: quanto maior e mais denso o material, maior o preço.
- Checklists: 2 páginas A4 -> R$9
- Guias e modelos: 3 a 6 páginas A4 -> R$19
- Planilha e contrato: ferramentas -> R$39 a R$49
- E-books: a partir de 20 páginas A5, ilustrados -> R$39 a R$99, conforme páginas e densidade
Os preços são proposta inicial; mantenha iguais em site/assets/js/config.js e na planilha.
"""
import json, subprocess
from pathlib import Path

AQUI = Path(__file__).resolve().parent
OUT = AQUI / "catalogo"

# status: pronto | rascunho | a-fazer
PRODUTOS = [
    # grupo, nome, formato, páginas, preço, status, observação, capa
    ("E-books", "E-book 1 — Fundamentos do Storymaker", "PDF A5 ilustrado", "24 a 28 (meta)", 39, "a-fazer",
     "Abre com a artesã da flor no cachepô (nível básico). Sumário pronto.", None),
    ("E-books", "E-book 2 — Do briefing à história", "PDF A5 ilustrado", "47", 99, "pronto",
     "16 capítulos, 10 ilustrações. Faltam fotos e prints da DocMe nos espaços marcados.", "ebook-02.png"),
    ("E-books", "E-book 3 — Olhar e narrativa", "PDF A5 ilustrado", "32 a 40 (meta)", 69, "a-fazer",
     "Leitura do evento, planos, sequência. Cases: feira de sustentabilidade, festas tradicionais, ações beneficentes.", None),
    ("E-books", "E-book 4 — Cobertura e edição ágil", "PDF A5 ilustrado", "32 a 40 (meta)", 69, "a-fazer",
     "Tempo real, CapCut, Reels x aftermovie. Cases: congresso em São Paulo, workshop de dois dias, evento nacional.", None),
    ("E-books", "E-book 5 — Operação profissional", "PDF A5 ilustrado", "40+ (meta)", 99, "a-fazer",
     "Proposta, preço, custos, contrato, portfólio. Usa a planilha e o contrato.", None),
    ("Checklists", "Checklist de pré-produção", "PDF A4 para imprimir", "2", 9, "pronto",
     "Antes do evento, véspera e chegada ao local.", "checklist-pre-producao.png"),
    ("Checklists", "Checklist de cobertura", "PDF A4 para imprimir", "2", 9, "pronto",
     "Durante o evento: sequência, pessoas A/B/C, controle foto/vídeo/enviado e o que fazer quando algo sai do plano.", "checklist-de-cobertura.png"),
    ("Checklists", "Checklist de pós-produção", "PDF A4 para imprimir", "1", 9, "pronto",
     "Aprovação de vídeo e legenda, entrega, saldo e a revisão: a equipe coube no valor?", "checklist-pos-producao.png"),
    ("Checklists", "Checklist: seu evento é amanhã (gratuito)", "PDF A4", "2", 0, "pronto",
     "Isca de cadastro: dez perguntas urgentes, prioridades, equipamentos e modelos de mensagem. Capta o e-mail de quem está prestes a pegar um trabalho.", "checklist-evento-amanha.png"),
    ("Checklists", "Checklist de áudio", "PDF A4 para imprimir", "1", 9, "pronto",
     "Fonte principal, backup, teste de som e cópia de segurança. Da prática DocMe: sempre duas fontes.", "checklist-de-audio.png"),
    ("Guias e modelos", "Roteiro de fim de ano (sazonal)", "PDF A4", "3", 19, "pronto",
     "Confraternização, Natal, Réveillon e Réveillon em bares e hotéis. Oferta de dezembro; fora do Pacote Completo.", "roteiro-de-fim-de-ano.png"),
    ("Guias e modelos", "Guia rápido: sequência de stories", "PDF A4", "4 a 6", 19, "a-fazer",
     "Lugar, pessoas, atrações, momentos, com exemplos reais.", None),
    ("Guias e modelos", "Modelo de briefing", "PDF A4 preenchível", "3", 19, "pronto",
     "Formulário de 10 seções para a reunião com o cliente.", "modelo-de-briefing.png"),
    ("Guias e modelos", "Roteiro de cobertura", "PDF A4", "4 a 6", 19, "a-fazer",
     "Modelo baseado no roteiro real de um congresso em São Paulo, com campos em branco.", None),
    ("Ferramentas", "Planilha de custos e horas", "Excel (6 abas)", "—", 49, "pronto",
     "6 abas: custos, pacotes básico x completo, equipe e margem, hora extra.", "planilha.png"),
    ("Ferramentas", "Modelo de contrato", "PDF A4 + versão editável", "4", 39, "rascunho",
     "11 cláusulas para storymaker. Revisar com os modelos da DocMe e um advogado.", "modelo-de-contrato.png"),
    ("Acompanhamento", "Trilha com avaliação e lives mensais", "12 meses: avaliação + 1 live por mês", "—", 297, "a-fazer",
     "Avaliação do vídeo e do portfólio e uma live por mês com a equipe DocMe para casos reais. A vivência ao vivo.", None),
    ("Para empresas", "Treinamento para equipes de agência", "Encontros ao vivo + materiais", "—", None, "a-fazer",
     "Venda para agências e empresas: o método DocMe aplicado à equipe do cliente. Preço a definir.", None),
]
PACOTES = [("Kit Lançamento", "checklist de pré-produção, modelo de contrato, planilha de custos e e-book 2 (os 4 prontos)", 127), ("Pacote Completo", "os 14 produtos digitais + trilha com avaliação e lives mensais por 12 meses", 697)]
KIT = {"Checklist de pré-produção", "Modelo de contrato", "Planilha de custos e horas", "E-book 2 — Do briefing à história"}

ROT = {"pronto": "Pronto", "rascunho": "Rascunho pronto", "a-fazer": "A produzir"}


def brl(v):
    return "Sob consulta" if v is None else ("Grátis" if v == 0 else f"R$ {v:,.0f}".replace(",", "."))


def html():
    grupos = []
    for g in dict.fromkeys(p[0] for p in PRODUTOS):
        cards = []
        for _, nome, fmt, pags, preco, st, obs, capa in [p for p in PRODUTOS if p[0] == g]:
            if capa:
                vis = f'<img src="capas/{capa}" alt="">'
            else:
                tipo = "ebook" if g == "E-books" else "ficha"
                vis = f'<div class="ph ph--{tipo}"><span>{nome.split(" — ")[-1]}</span></div>'
            cards.append(f'''<article class="card st-{st}"><div class="vis">{vis}</div><div class="info">
<span class="chip">{ROT[st]}</span><h3>{nome}</h3>
<dl><dt>Formato</dt><dd>{fmt}</dd><dt>Páginas</dt><dd>{pags}</dd></dl>
<p>{obs}</p><p class="preco">{brl(preco)}</p></div></article>''')
        grupos.append(f'<section><h2>{g}</h2><div class="grid">{"".join(cards)}</div></section>')
    soma = sum(p[4] for p in PRODUTOS if p[4] and 'sazonal' not in p[1])
    soma_kit = sum(p[4] for p in PRODUTOS if p[1] in KIT)
    pac = "".join(
        f'<div class="pac"><h3>{n}</h3><p>{d}</p><p class="de">avulsos somam {brl(s)}</p><p class="preco">{brl(v)}</p><p class="eco">economia de {brl(s-v)} ({round((s-v)/s*100)}%)</p></div>'
        for (n, d, v), s in zip(PACOTES, [soma_kit, soma]))
    prontos = sum(1 for p in PRODUTOS if p[5] != "a-fazer")
    lanc = {"Checklist de pré-produção", "Modelo de contrato", "Planilha de custos e horas", "E-book 2 — Do briefing à história"}
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Catálogo de produtos | Storymaker Oficial</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@600;700;800&display=swap" rel="stylesheet">
<style>
:root{{--l:#e7570c;--le:#c2410c;--t:#2b2a30;--s:#5d5c63;--cr:#fff4ec;--li:#e7e6ea}}
*{{box-sizing:border-box}} body{{margin:0;font:400 13px/1.5 Inter,sans-serif;color:var(--t);background:#f6f5f3;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
header{{background:var(--l);padding:40px 48px 34px}} header h1{{font:800 34px/1.1 Sora,sans-serif;margin:6px 0 8px;color:#fff}}
.sel{{font:700 11px Inter;letter-spacing:.14em;text-transform:uppercase;color:#1f1e24}} header p{{margin:0;color:#1f1e24;max-width:70ch}}
.res{{display:flex;gap:12px;margin-top:18px;flex-wrap:wrap}} .res span{{background:rgba(43,42,48,.1);border-radius:999px;padding:6px 12px;font-weight:600;color:#1f1e24}}
main{{padding:10px 48px 40px}} h2{{font:700 20px Sora,sans-serif;margin:28px 0 12px;padding-bottom:6px;border-bottom:3px solid var(--l)}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}
.card{{background:#fff;border-radius:14px;display:flex;gap:14px;padding:14px;break-inside:avoid;border:1px solid var(--li)}}
.vis{{flex:none;width:96px}} .vis img{{width:96px;border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,.15);display:block}}
.ph{{width:96px;border-radius:6px;display:flex;align-items:flex-end;padding:8px;font:700 10px/1.2 Sora,sans-serif}}
.ph--ebook{{aspect-ratio:148/210;background:repeating-linear-gradient(135deg,#f6c3a5 0 6px,#f9d6c1 6px 12px);color:var(--le);border:2px dashed #e0a27f}}
.ph--ficha{{aspect-ratio:210/297;background:repeating-linear-gradient(135deg,#ecebef 0 6px,#f4f3f6 6px 12px);color:var(--s);border:2px dashed #cfcdd3}}
.info{{min-width:0}} h3{{font:700 13.5px/1.25 Sora,sans-serif;margin:6px 0}}
.chip{{display:inline-block;font:700 9.5px Inter;letter-spacing:.06em;text-transform:uppercase;border-radius:999px;padding:4px 8px}}
.st-pronto .chip{{background:#2b2a30;color:#fff}} .st-rascunho .chip{{background:var(--le);color:#fff}} .st-a-fazer .chip{{background:var(--li);color:var(--s)}}
dl{{display:grid;grid-template-columns:auto 1fr;gap:1px 8px;margin:4px 0;font-size:11.5px}} dt{{color:var(--s)}} dd{{margin:0;font-weight:600}}
.info p{{margin:4px 0;font-size:11.5px;color:var(--s)}} .preco{{font:800 18px Sora,sans-serif!important;color:var(--le)!important;margin-top:6px!important}}
.pacs{{display:grid;grid-template-columns:1fr 1fr;gap:14px}} .pac{{background:var(--cr);border:2px solid var(--l);border-radius:14px;padding:16px}}
.pac h3{{font-size:16px}} .pac p{{margin:2px 0}} .de{{color:var(--s)}} .eco{{font-weight:700;color:var(--le)}}
.nota{{color:var(--s);font-size:11.5px;margin-top:20px}}
</style></head><body>
<header><p class="sel">Storymaker Oficial · Método desenvolvido pela DocMe Comunicação.</p><h1>Catálogo de produtos</h1>
<p>Do mais curto ao mais completo: quanto maior e mais denso o material, maior o preço. E-books a partir de 20 páginas, todos ilustrados.</p>
<div class="res"><span>{len([p for p in PRODUTOS if p[4]])} produtos digitais + treinamento para empresas</span><span>{prontos} prontos ou em rascunho</span><span>avulsos somam {brl(soma)}</span></div></header>
<main>{"".join(grupos)}<section><h2>Pacotes</h2><div class="pacs">{pac}</div></section>
<p class="nota">Preços são proposta inicial para validar. Capas tracejadas = produto ainda a produzir. O desconto dos pacotes é sempre calculado sobre os preços avulsos reais.</p></main></body></html>"""


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    h = OUT / "catalogo.html"
    h.write_text(html(), encoding="utf-8")
    node = """const { chromium } = require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1240,height:900},deviceScaleFactor:2});
await p.goto('file://'+process.argv[1],{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
await p.screenshot({path:process.argv[2],fullPage:true});await p.pdf({path:process.argv[3],width:'1240px',height:(await p.evaluate(()=>document.body.scrollHeight))+'px',printBackground:true});await b.close();})();"""
    subprocess.run(["node", "-e", node, str(h), str(OUT / "catalogo.png"), str(OUT / "catalogo.pdf")], check=True)
    print("ok", OUT)
