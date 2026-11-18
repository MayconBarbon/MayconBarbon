"""Lista de todos os eventos citados, para a DocMe reunir o material.
Gera docs/lista-de-eventos.xlsx (para preencher) e docs/lista-de-eventos.pdf (para consultar).
Uso: python3 produtos/lista_eventos.py
"""
import subprocess
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation

RAIZ = Path(__file__).resolve().parent.parent
DOCS = RAIZ / "docs"

# (grupo, evento como foi citado, nome genérico para os materiais, o que já sabemos, onde procurar no Drive, pergunta em aberto)
EVENTOS = [
    ("Congressos e workshops", "Best-Seller (Guarujá)", "Congresso de negócios",
     "5 palestrantes clientes, equipe de 4 a 5 pessoas; programação mudou sem aviso; entregas renegociadas.", "Rede Best Seller", "Ano do evento"),
    ("Congressos e workshops", "CIDE 2026 (São Paulo)", "Congresso em São Paulo",
     "10 e 11/06/2026; roteiro com 15 stories por dia; teste do Igor (15 cenas, 30 s no CapCut); aftermovie.", "CIDE 2026 (Dia 1, Dia 2, AFTER MOVIE)", "É o evento de grande porte do artigo 10?"),
    ("Congressos e workshops", "Congresso ACIPI 2025 (19º)", "Congresso empresarial regional",
     "Storymaker e vídeo pós-evento (confirmado).", "19º Congresso Acipi", "A edição de 2024 também teve storymaker?"),
    ("Congressos e workshops", "Workshop Karla Corrente", "Workshop de dois dias",
     "2 dias de storymaker, gravado e editado no mesmo dia; depoimentos em vídeo da cliente.", "Karla Corrente (Workshop, Workshop2)", "Autorização para usar os depoimentos"),
    ("Corporativo", "APEX Brasil (no SIMESPI)", "Evento nacional",
     "Evento nacional; o cliente pediu um vídeo na hora.", "APEX", "Data e o que foi entregue"),
    ("Corporativo", "Expo ESG", "Feira de sustentabilidade",
     "Storymaker e after movie.", "Expo ESG 2023, 2024 e 2025", "Quais edições tiveram storymaker"),
    ("Corporativo", "Celebra", "Confraternização de fim de ano",
     "4 stories de ~30 s: fachada/decoração, recepção, atrações; elogios \"arrasou\", \"tá demais\".", "CELEBRA 2025", "Foi 2025 ou 2026?"),
    ("Corporativo", "Inauguração da clínica da Débora (SP)", "Inauguração de clínica",
     "Provável storymaker.", "FOTOS DEBORA E CIBELE (talvez)", "Nome completo e se teve storymaker"),
    ("Corporativo", "Evento de grande porte (artigo 10)", "Evento corporativo de grande porte",
     "~3 meses de preparo, equipe de ~25 pessoas, ~13 mil pessoas, em média 25 palestrantes, 2 storymakers com 5 celulares.", "—", "Qual evento foi"),
    ("Corporativo", "Evento com 3 patrocinadores (artigo 11)", "Evento com patrocinadores",
     "Stories em tempo real mostrando os patrocinadores; depoimentos de pessoas-chave para o aftermovie.", "—", "Qual evento foi"),
    ("Festivais e comunitários", "Dia das Crianças (ACIPI, Unimed e SIMESPI)", "Evento infantil",
     "~13 mil pessoas, 10 personalidades; vídeo do dia 10 mil views; aftermovie 1.500 views.", "Dia das crianças video; Fotos dia das crianças", "Papel de cada realizador"),
    ("Festivais e comunitários", "Festa do Frango", "Festa tradicional da cidade",
     "Storymaker e after movie.", "Festa do Frango 2024 e 2025", "Quais edições"),
    ("Festivais e comunitários", "Festa da Batata", "Festa tradicional da cidade",
     "Storymaker e after movie.", "Festa da Batata 2024 e 2025", "Quais edições"),
    ("Festivais e comunitários", "Comida na Rua (Piracicaba)", "Circuito gastronômico",
     "14 restaurantes; checklist foto/vídeo/enviado; cliente aprovava e publicava pelo grupo.", "Checklist_Comida_na_Rua", "Links e resultados"),
    ("Festivais e comunitários", "PiraBeer 2024", "Evento regional",
     "Teve storymaker.", "Procurar por PiraBeer", "Material e links"),
    ("Ações beneficentes", "McDia Feliz — Casa Ronald McDonald SP", "Ação beneficente",
     "Teve storymaker.", "Casa Ronald; MCDIA", "Ano da cobertura"),
    ("Ações beneficentes", "Pizza do Bem", "Ação beneficente",
     "Teve storymaker.", "Pizza do bem 2024", "É ação da Casa Ronald?"),
    ("Ações beneficentes", "Feijoada do Bem", "Ação beneficente",
     "Teve storymaker.", "Feijoada do bem", "É ação da Casa Ronald?"),
    ("Ações beneficentes", "Dia de Doar", "Ação beneficente",
     "Teve storymaker.", "Dia de Doar 2025", "Links"),
    ("Casamentos e celebrações", "Casamento da Aninha", "Casamento",
     "Teve storymaker.", "#Casamento Aninha Barros", "Autorização da cliente"),
    ("Casamentos e celebrações", "Casamento da Carol Sampaio (Para Sempre)", "Casamento com mais de 30 atrações",
     "Mais de 30 stories, inclusive fotos únicas (pamonha, caldo de cana).", "Não encontrado", "Onde está o material"),
    ("Casamentos e celebrações", "Casamento em que a mãe da noiva atrasou", "Casamento com atraso",
     "Cerimônia parada ~1 h; equipe seguiu produzindo.", "—", "Qual casamento foi"),
    ("Casamentos e celebrações", "Casamento em que os noivos deixaram o celular", "Casamento com publicação pela equipe",
     "Noiva e noivo deixaram os celulares; postagem em tempo real.", "—", "Qual casamento foi (é o mesmo do atraso?)"),
    ("Casamentos e celebrações", "Casamento de 16 horas", "Casamento longo",
     "Cobertura de ~16 horas (exemplo de preço).", "—", "Qual casamento foi"),
    ("Casamentos e celebrações", "15 anos", "Festa de 15 anos",
     "Exemplo de entrega: 5 stories de vídeo + 5 de foto.", "—", "Qual festa foi"),
    ("Pequenos negócios", "Artesã da flor no cachepô", "Artesã de feira",
     "Vídeo feito em 5 minutos de conversa, CapCut, entregue na hora; ela sempre reposta.", "Não encontrado", "Achar o vídeo; nome e autorização"),
    ("Pequenos negócios", "Salão de beleza vizinho ao escritório", "Salão de beleza do bairro",
     "Colaboração voluntária: 10 vídeos e 50 fotos, conteúdo para 2 a 3 meses.", "—", "Nome do salão e autorização"),
    ("Pedidos rápidos", "Pedido urgente de stories (contrato de vídeo)", "Pedido urgente de stories",
     "Cliente queria publicar antes da imprensa; 10 imagens montadas no CapCut.", "—", "Qual evento foi"),
    ("Pedidos rápidos", "Evento curto (40 min a 1 h)", "Cobertura rápida",
     "10 fotos e vídeo de ~1min30 em ~10 min de captação; \"era exatamente o que eu queria\".", "—", "Qual evento foi"),
    ("Pedidos rápidos", "Evento de meia hora", "Cobertura de meia hora",
     "Exemplo de duração curta (comparado com o casamento de 16 h).", "—", "Qual evento foi"),
    ('Corporativo', 'Festa da Imprensa 2026 (SIMESPI)', 'Festa de entidade de classe', 'Reel no perfil do SIMESPI.', 'Instagram', 'Detalhes do case'),
    ('Festivais e comunitários', 'PedalaPira 2026', 'Passeio ciclístico', 'Post no Instagram.', 'Instagram', 'Detalhes do case'),
    ('Congressos e workshops', 'Workshop Exposição de Inovação e Sustentabilidade na Construção Civil', 'Workshop de construção civil', 'Post no Instagram.', 'Instagram', 'Ano e detalhes'),
    ('Corporativo', 'Inauguração CT PiraOlímpica 2025', 'Inauguração de centro esportivo', 'Post no Instagram.', 'Instagram', 'Detalhes do case'),
    ('Congressos e workshops', 'Palestra da jornalista Lilian Geraldini', 'Palestra com jornalista', 'Post no Instagram.', 'Instagram', 'Ano e detalhes'),
    ('Festivais e comunitários', 'Corrida ESG — Chelso Sports', 'Corrida de rua', 'Post no Instagram.', 'Instagram', 'Ano e detalhes'),
    ('Festivais e comunitários', 'Jornada Caipira', 'Festa caipira', 'Reel no Instagram.', 'Instagram', 'Ano e detalhes'),
]
MATERIAIS = ["Data / ano", "Link dos stories ou vídeo do dia", "Link do aftermovie", "3 a 5 fotos",
             "Prints de elogios", "Métricas (visualizações etc.)", "O que deu errado e como resolveram", "Autorização de uso"]
EXTRAS = [("Depoimentos em vídeo da equipe", "João, Gu, Henrique e Eric: o que aprenderam na DocMe."),
          ("Prints de elogios de clientes", "Para a fileira de mensagens reais do site."),
          ("Logo e arquivos da marca DocMe", "Referência visual para a identidade Storymaker Oficial."),
          ("Outros modelos de contrato", "Para revisar o modelo de contrato."),
          ("Eventos que ainda não estão na lista", "Anote abaixo e me mande junto.")]


def planilha():
    wb = Workbook(); ws = wb.active; ws.title = "Eventos"
    L, T, CR = "E7570C", "2B2A30", "FFF4EC"
    ws["A1"] = "Storymaker Oficial — eventos para reunir material"; ws["A1"].font = Font(bold=True, size=15, color=L)
    ws["A2"] = "Preencha os links e marque o que já separou. Células laranja claro são para preencher."; ws["A2"].font = Font(italic=True, color="5D5C63")
    cab = ["#", "Grupo", "Evento (como foi citado)", "Nome genérico nos materiais", "O que já sabemos", "Onde procurar no Drive", "Pergunta em aberto", "Resposta"] + MATERIAIS
    thin = Side(style="thin", color="D9D8DD")
    for c, v in enumerate(cab, 1):
        cell = ws.cell(row=4, column=c, value=v); cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor=T); cell.alignment = Alignment(wrap_text=True, vertical="center")
    dv = DataValidation(type="list", formula1='"Separado,Falta,Não existe"', allow_blank=True); ws.add_data_validation(dv)
    for i, e in enumerate(EVENTOS, 5):
        vals = [i - 4] + list(e)
        for c, v in enumerate(vals, 1):
            cell = ws.cell(row=i, column=c, value=v); cell.alignment = Alignment(wrap_text=True, vertical="top")
            cell.border = Border(bottom=thin); cell.font = Font(color=T, bold=(c == 3))
        for c in range(8, 8 + 1 + len(MATERIAIS)):
            cell = ws.cell(row=i, column=c); cell.fill = PatternFill("solid", fgColor=CR); cell.border = Border(bottom=thin, left=thin)
        dv.add(f"{ws.cell(row=i, column=9).coordinate}:{ws.cell(row=i, column=8 + len(MATERIAIS)).coordinate}")
    for col, w in zip("ABCDEFGH", (4, 18, 30, 26, 46, 28, 28, 28)):
        ws.column_dimensions[col].width = w
    for c in range(9, 9 + len(MATERIAIS)):
        ws.column_dimensions[ws.cell(row=4, column=c).column_letter].width = 16
    ws.row_dimensions[4].height = 44; ws.freeze_panes = "D5"
    w2 = wb.create_sheet("Outros materiais")
    w2["A1"] = "Outros materiais para mandar"; w2["A1"].font = Font(bold=True, size=14, color=L)
    for c, v in enumerate(["Material", "Para quê", "Situação", "Link / observação"], 1):
        cell = w2.cell(row=3, column=c, value=v); cell.font = Font(bold=True, color="FFFFFF"); cell.fill = PatternFill("solid", fgColor=T)
    dv2 = DataValidation(type="list", formula1='"Separado,Falta,Não existe"', allow_blank=True); w2.add_data_validation(dv2)
    for i, (m, p) in enumerate(EXTRAS, 4):
        w2.cell(row=i, column=1, value=m).font = Font(bold=True, color=T); w2.cell(row=i, column=2, value=p).font = Font(color=T)
        for c in (3, 4): w2.cell(row=i, column=c).fill = PatternFill("solid", fgColor=CR)
        dv2.add(f"C{i}")
    for col, w in zip("ABCD", (34, 50, 14, 50)): w2.column_dimensions[col].width = w
    out = DOCS / "lista-de-eventos.xlsx"; wb.save(out); return out


def pdf():
    css = (RAIZ / "produtos" / "produto.css").read_text(encoding="utf-8")
    grupos = []
    for g in dict.fromkeys(e[0] for e in EVENTOS):
        linhas = "".join(
            f"<tr><td class='n'>{EVENTOS.index(e)+1:02d}</td><td><b>{e[1]}</b><br><span class='gen'>nos materiais: {e[2]}</span></td>"
            f"<td>{e[3]}<br><span class='drive'>Drive: {e[4]}</span></td><td class='perg'>{e[5]}</td></tr>"
            for e in EVENTOS if e[0] == g)
        grupos.append(f"<h2>{g}</h2><table><tr><th>#</th><th>Evento</th><th>O que já sabemos</th><th>Pergunta em aberto</th></tr>{linhas}</table>")
    mats = "".join(f'<li class="check"><span class="box"></span><span>{m}</span></li>' for m in MATERIAIS)
    extras = "".join(f'<li class="check"><span class="box"></span><span><b>{m}:</b> {p}</span></li>' for m, p in EXTRAS)
    html = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@600;700;800&display=swap" rel="stylesheet">
<style>{css}
td.n{{font:800 11pt Sora,sans-serif;color:#c2410c;width:7mm}} .gen{{color:#5d5c63;font-size:8pt}} .drive{{color:#9a3412;font-size:8pt}}
.perg{{color:#9a3412;font-weight:600;width:38mm}} table{{font-size:8.4pt}} .duas{{columns:2;column-gap:10mm}} .fmt-ficha ul{{margin-bottom:2mm}}</style></head>
<body class="fmt-ficha"><header class="ficha__topo"><div><p class="ficha__selo">Uso interno · Storymaker Oficial</p><h1>Eventos para reunir material</h1></div>
<p class="ficha__assina">{len(EVENTOS)} eventos citados na conversa, nos artigos e no Drive.</p></header>
<main><p><b>Para cada evento, separe o que tiver:</b></p><ul class="duas">{mats}</ul>
<p>Os nomes reais ficam só neste documento interno. Nos e-books, no blog e no catálogo, cada evento aparece com o <b>nome genérico</b>.</p>
{''.join(grupos)}<h2>Outros materiais</h2><ul>{extras}</ul>
<p>Eventos que não estão na lista: ______________________________________________</p>
<p>______________________________________________________________________________</p></main></body></html>"""
    h = DOCS / "lista-de-eventos.html"; h.write_text(html, encoding="utf-8")
    out = DOCS / "lista-de-eventos.pdf"
    node = "const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://'+process.argv[1],{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);await p.pdf({path:process.argv[2],preferCSSPageSize:true,printBackground:true});await b.close();})();"
    subprocess.run(["node", "-e", node, str(h), str(out)], check=True); h.unlink(); return out


if __name__ == "__main__":
    print(planilha()); print(pdf()); print(len(EVENTOS), "eventos")
