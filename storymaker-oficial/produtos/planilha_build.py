import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule

OUT = sys.argv[1]
LARANJA, CINZA = "E7570C", "5D5C63"
INPUT_FILL = PatternFill("solid", fgColor="FFF4EC")   # campos para preencher
CALC_FILL = PatternFill("solid", fgColor="F1F1F3")    # resultados calculados
HEAD_FILL = PatternFill("solid", fgColor=LARANJA)
HEAD_FONT = Font(bold=True, color="FFFFFF")
TITLE_FONT = Font(bold=True, size=16, color=LARANJA)
SUB_FONT = Font(italic=True, color=CINZA)
thin = Side(style="thin", color="D9D9DE")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
BRL = 'R$ #,##0.00'
PCT = '0.0%'

wb = Workbook()

def header(ws, row, cols):
    for i, c in enumerate(cols, 1):
        cell = ws.cell(row=row, column=i, value=c)
        cell.fill, cell.font, cell.border = HEAD_FILL, HEAD_FONT, BORDER
        cell.alignment = Alignment(wrap_text=True, vertical="center")

def style(cell, kind, fmt=None):
    cell.fill = INPUT_FILL if kind == "in" else CALC_FILL
    cell.border = BORDER
    if fmt:
        cell.number_format = fmt

# ---------------- Leia primeiro ----------------
ws = wb.active
ws.title = "Leia primeiro"
ws["A1"] = "Storymaker Oficial — Planilha de produtos e custos"
ws["A1"].font = TITLE_FONT
ws["A2"] = "Método desenvolvido pela DocMe Comunicação."
ws["A2"].font = SUB_FONT
linhas = [
    "",
    "COMO USAR",
    "• Células em LARANJA CLARO são para você preencher. Células em CINZA são calculadas — não digite nelas.",
    "",
    "ABA “Catálogo”: todos os produtos digitais, com preço avulso, taxas e valor líquido.",
    "   – Os preços já preenchidos são uma PROPOSTA INICIAL dentro das faixas definidas no briefing (guias R$9–19,",
    "     e-books R$29–99, planilha e contrato R$39–49). Não são pesquisa de mercado: ajuste à vontade.",
    "   – Taxas da plataforma: consulte a taxa vigente do seu plano no Mercado Pago e preencha (percentual e fixa).",
    "   – Marque “Sim” nas colunas de pacote para incluir o produto em cada pacote.",
    "",
    "ABA “Pacotes”: soma automática dos preços avulsos dos itens marcados, preço do pacote, economia e desconto.",
    "   – O desconto é sempre calculado a partir dos preços avulsos reais (transparência exigida pelo Procon/CDC).",
    "   – Só divulgue “de R$X por R$Y” se os produtos estiverem de fato à venda avulsos por esses preços.",
    "",
    "ABA “Custos de cobertura”: ferramenta para o storymaker montar o orçamento de um evento.",
    "   – Lógica DocMe: a reunião de briefing (~1h), a pesquisa da página do cliente, a busca de referências e a",
    "     escolha de trilhas e efeitos entram no orçamento, mesmo que você não anuncie isso ao cliente.",
    "   – Some deslocamento, alimentação, horas no evento, edição, upload/entrega e equipe.",
    "   – As horas preenchidas são um EXEMPLO de evento; os valores em R$ ficam em branco para você definir.",
    "   – O resultado mostra o preço mínimo sugerido e, ao informar o valor proposto, quanto você ganha por hora real.",
    "",
    "Esta aba “Custos de cobertura” também pode ser vendida como produto separado (planilha de custos e horas).",
    "",
    "ABAS DA VIVÊNCIA DOCME: “Pacotes de serviço” (básico x completo), “Equipe e margem” (a equipe cabe no contrato?) e “Hora extra”.",
]
for i, t in enumerate(linhas, 4):
    ws.cell(row=i, column=1, value=t)
    if t in ("COMO USAR",):
        ws.cell(row=i, column=1).font = Font(bold=True, color=CINZA)
ws["A26"] = "Legenda:"
ws["A26"].font = Font(bold=True)
ws["A27"] = "Preencher"; style(ws["A27"], "in")
ws["A28"] = "Calculado"; style(ws["A28"], "calc")
ws.column_dimensions["A"].width = 115

# ---------------- Catálogo ----------------
cat = wb.create_sheet("Catálogo")
cat["A1"] = "Catálogo de produtos"; cat["A1"].font = TITLE_FONT
cat["A2"] = "Preços = proposta inicial editável. Taxas: preencha conforme seu plano no Mercado Pago."; cat["A2"].font = SUB_FONT
cols = ["Produto", "Tipo", "Descrição", "Preço avulso", "Pacote Completo?", "Kit Lançamento?",
        "Custo de produção", "Taxa plataforma (%)", "Taxa fixa (R$)", "Preço líquido", "Link de checkout", "Status"]
header(cat, 4, cols)
produtos = [
    ("E-book 1 — Fundamentos do Storymaker", "E-book", "O que faz um storymaker e como transformar o olhar de imagem em serviço", 39, "Sim", "Não"),
    ("E-book 2 — Do briefing à história", "E-book", "Reunião com o cliente, perguntas, canais, prioridades e planejamento", 99, "Sim", "Sim"),
    ("E-book 3 — Olhar e narrativa", "E-book", "Leitura do evento, lista de cenas, variação de planos e sequência", 69, "Sim", "Não"),
    ("E-book 4 — Cobertura e edição ágil", "E-book", "Tempo real, CapCut, aprovação, atrasos, bateria e aftermovie", 69, "Sim", "Não"),
    ("E-book 5 — Operação profissional", "E-book", "Proposta, preço, custos, contrato, portfólio e primeiros trabalhos", 99, "Sim", "Não"),
    ("Checklist de pré-produção", "Checklist", "Antes do evento, véspera e chegada ao local", 9, "Sim", "Sim"),
    ("Checklist de cobertura", "Checklist", "Durante o evento: sequência, pessoas A/B/C, bateria", 9, "Sim", "Não"),
    ("Checklist de áudio", "Checklist", "Fonte principal, backup e teste de som", 9, "Sim", "Não"),
    ("Checklist: seu evento é amanhã (gratuito)", "Checklist", "Isca de cadastro (lead)", 0, "Não", "Não"),
    ("Roteiro de fim de ano (sazonal)", "Roteiro", "Confraternização, Natal e Réveillon; oferta de dezembro", 19, "Não", "Não"),
    ("Checklist de pós-produção", "Checklist", "Reels final, legenda, upload e entrega", 9, "Sim", "Não"),
    ("Guia rápido: sequência de stories", "Guia", "Estrutura que funciona: espaço, recepção, atrações, encerramento", 19, "Sim", "Não"),
    ("Modelo de briefing", "Modelo de briefing", "Formulário para a reunião com o cliente", 19, "Sim", "Não"),
    ("Roteiro de cobertura", "Roteiro", "Modelo de roteiro com prioridades e horários", 19, "Sim", "Não"),
    ("Planilha de custos e horas", "Planilha", "Monte o orçamento contando todas as horas reais", 49, "Sim", "Sim"),
    ("Modelo de contrato", "Contrato", "Contrato editável para coberturas de storymaker", 39, "Sim", "Sim"),
    ("Trilha com avaliação e lives mensais", "Outro", "12 meses: avaliação do portfólio e 1 live por mês com a equipe DocMe", 297, "Sim", "Não"),
]
first = 5
for r, p in enumerate(produtos, first):
    for c, v in enumerate(p, 1):
        cell = cat.cell(row=r, column=c, value=v)
        style(cell, "in", BRL if c == 4 else None)
    for c, v, fmt in ((7, 0, BRL), (8, 0, PCT), (9, 0, BRL)):
        style(cat.cell(row=r, column=c, value=v), "in", fmt)
    cat.cell(row=r, column=10, value=f"=D{r}-D{r}*H{r}-I{r}")
    style(cat.cell(row=r, column=10), "calc", BRL)
    style(cat.cell(row=r, column=11, value="[colar link do Mercado Pago]"), "in")
    style(cat.cell(row=r, column=12, value="Rascunho"), "in")
last = first + len(produtos) - 1 + 7   # 7 linhas livres para novos produtos
for r in range(first + len(produtos), last + 1):
    for c in range(1, 13):
        style(cat.cell(row=r, column=c), "in", {4: BRL, 7: BRL, 8: PCT, 9: BRL}.get(c))
    cat.cell(row=r, column=10, value=f'=IF(D{r}="","",D{r}-D{r}*H{r}-I{r})')
    style(cat.cell(row=r, column=10), "calc", BRL)
tot = last + 1
cat.cell(row=tot, column=1, value="TOTAL (soma de todos os avulsos)").font = Font(bold=True)
cat.cell(row=tot, column=4, value=f"=SUM(D{first}:D{last})")
style(cat.cell(row=tot, column=4), "calc", BRL)
cat.cell(row=tot, column=4).font = Font(bold=True)

dv_sn = DataValidation(type="list", formula1='"Sim,Não"', allow_blank=True)
dv_tipo = DataValidation(type="list", formula1='"E-book,Checklist,Guia,Modelo de briefing,Roteiro,Planilha,Contrato,Outro"', allow_blank=True)
dv_status = DataValidation(type="list", formula1='"Rascunho,Ativo,Pausado"', allow_blank=True)
dv_pct = DataValidation(type="decimal", operator="between", formula1="0", formula2="1", allow_blank=True,
                        error="Digite o percentual entre 0% e 100% (ex.: 4,99%)")
for dv in (dv_sn, dv_tipo, dv_status, dv_pct):
    cat.add_data_validation(dv)
dv_sn.add(f"E{first}:F{last}"); dv_tipo.add(f"B{first}:B{last}")
dv_status.add(f"L{first}:L{last}"); dv_pct.add(f"H{first}:H{last}")
for col, w in zip("ABCDEFGHIJKL", (38, 18, 60, 13, 12, 12, 14, 14, 12, 13, 32, 12)):
    cat.column_dimensions[col].width = w
cat.row_dimensions[4].height = 32
cat.freeze_panes = "B5"

# ---------------- Pacotes ----------------
pk = wb.create_sheet("Pacotes")
pk["A1"] = "Pacotes promocionais"; pk["A1"].font = TITLE_FONT
pk["A2"] = "Itens do pacote = produtos marcados “Sim” na aba Catálogo. Preencha só o preço do pacote."; pk["A2"].font = SUB_FONT
header(pk, 4, ["Pacote", "Coluna no Catálogo", "Qtd. de itens", "Soma dos avulsos", "Preço do pacote",
               "Economia (R$)", "Desconto (%)", "Taxas estimadas", "Valor líquido", "Custo de produção", "Margem estimada"])
rng = lambda col: f"Catálogo!${col}${first}:${col}${last}"
# taxa média ponderada do catálogo aplicada ao preço do pacote: usa % e fixa do 1º produto como referência editável
pacotes = [("Pacote Completo", "E", 697), ("Kit Lançamento", "F", 127)]
for i, (nome, col, preco) in enumerate(pacotes, 5):
    style(pk.cell(row=i, column=1, value=nome), "in")
    style(pk.cell(row=i, column=2, value=col), "calc")
    pk.cell(row=i, column=3, value=f'=COUNTIF({rng(col)},"Sim")')
    pk.cell(row=i, column=4, value=f'=SUMIF({rng(col)},"Sim",{rng("D")})')
    style(pk.cell(row=i, column=5, value=preco), "in", BRL)
    pk.cell(row=i, column=6, value=f"=D{i}-E{i}")
    pk.cell(row=i, column=7, value=f'=IF(D{i}=0,0,F{i}/D{i})')
    pk.cell(row=i, column=8, value=f"=E{i}*$B$10+$B$11")
    pk.cell(row=i, column=9, value=f"=E{i}-H{i}")
    pk.cell(row=i, column=10, value=f'=SUMIF({rng(col)},"Sim",{rng("G")})')
    pk.cell(row=i, column=11, value=f'=IF(E{i}=0,0,(I{i}-J{i})/E{i})')
    for c, fmt in ((3, None), (4, BRL), (6, BRL), (7, PCT), (8, BRL), (9, BRL), (10, BRL), (11, PCT)):
        style(pk.cell(row=i, column=c), "calc", fmt)
pk["A9"] = "Taxas aplicadas aos pacotes"; pk["A9"].font = Font(bold=True, color=CINZA)
pk["A10"] = "Taxa plataforma (%)"; style(pk["B10"], "in", PCT); pk["B10"] = 0
pk["A11"] = "Taxa fixa por venda (R$)"; style(pk["B11"], "in", BRL); pk["B11"] = 0
pk.add_data_validation(dv_pct2 := DataValidation(type="decimal", operator="between", formula1="0", formula2="1", allow_blank=True))
dv_pct2.add("B10")
pk["A13"] = "Os preços dos pacotes (R$697 e R$127) são proposta inicial para teste. A economia exibida no site deve sair desta aba."
pk["A13"].font = SUB_FONT
pk["A14"] = "Para criar outro pacote: adicione uma coluna “Sim/Não” no Catálogo e copie uma linha acima, trocando a letra da coluna nas fórmulas."
pk["A14"].font = SUB_FONT
for col, w in zip("ABCDEFGHIJK", (24, 14, 11, 15, 15, 14, 12, 14, 14, 15, 14)):
    pk.column_dimensions[col].width = w
pk.row_dimensions[4].height = 32

# ---------------- Custos de cobertura ----------------
cc = wb.create_sheet("Custos de cobertura")
cc["A1"] = "Custos de cobertura — orçamento de um evento"; cc["A1"].font = TITLE_FONT
cc["A2"] = "Preencha as células laranja. Horas já preenchidas são um exemplo; R$ ficam para você definir."; cc["A2"].font = SUB_FONT

cc["A4"] = "Evento / cliente"; style(cc["B4"], "in"); cc["B4"] = "[nome do evento]"
cc["A5"] = "Data"; style(cc["B5"], "in")
cc["A6"] = "Valor da SUA hora (R$)"; style(cc["B6"], "in", BRL)
for a in ("A4", "A5", "A6"):
    cc[a].font = Font(bold=True)

header(cc, 8, ["Etapa (suas horas)", "Horas", "Custo (R$)", "Observação"])
etapas = [
    ("Reunião de briefing com o cliente", 1, "~1h. Não precisa anunciar que está contando, mas entra no orçamento."),
    ("Pesquisa da página e das redes do cliente", 0.5, ""),
    ("Busca de referências", 0.5, ""),
    ("Seleção de trilhas e efeitos", 0.5, ""),
    ("Planejamento, checklist e roteiro", 0.5, "Exemplo DocMe: só a pré-produção já soma ~3h."),
    ("Deslocamento (ida e volta)", 1, "Mínimo ~30min por trecho, mesmo perto."),
    ("Horas no evento", 4, "Já houve evento de 30min e casamento de 16h."),
    ("Edição final (Reels / aftermovie) e legenda", 2, ""),
    ("Upload no Drive / envio por WhatsApp", 0.5, ""),
    ("Revisões", 0.5, ""),
]
r0 = 9
for i, (nome, h, obs) in enumerate(etapas, r0):
    cc.cell(row=i, column=1, value=nome).border = BORDER
    style(cc.cell(row=i, column=2, value=h), "in", '0.0')
    cc.cell(row=i, column=3, value=f"=B{i}*$B$6"); style(cc.cell(row=i, column=3), "calc", BRL)
    cc.cell(row=i, column=4, value=obs).font = SUB_FONT
r1 = r0 + len(etapas) - 1
rt = r1 + 1
cc.cell(row=rt, column=1, value="Subtotal suas horas").font = Font(bold=True)
cc.cell(row=rt, column=2, value=f"=SUM(B{r0}:B{r1})"); style(cc.cell(row=rt, column=2), "calc", '0.0')
cc.cell(row=rt, column=3, value=f"=SUM(C{r0}:C{r1})"); style(cc.cell(row=rt, column=3), "calc", BRL)

# Equipe
re_ = rt + 2
header(cc, re_, ["Equipe extra (nome / função)", "Horas", "Valor/hora (R$)", "Custo (R$)"])
eq0 = re_ + 1
for i in range(eq0, eq0 + 4):
    style(cc.cell(row=i, column=1), "in")
    style(cc.cell(row=i, column=2), "in", '0.0')
    style(cc.cell(row=i, column=3), "in", BRL)
    cc.cell(row=i, column=4, value=f"=N(B{i})*N(C{i})"); style(cc.cell(row=i, column=4), "calc", BRL)
eq1 = eq0 + 3
eqt = eq1 + 1
cc.cell(row=eqt, column=1, value="Subtotal equipe").font = Font(bold=True)
cc.cell(row=eqt, column=4, value=f"=SUM(D{eq0}:D{eq1})"); style(cc.cell(row=eqt, column=4), "calc", BRL)

# Custos diretos
rd = eqt + 2
header(cc, rd, ["Custos diretos", "Valor (R$)", "", "Observação"])
diretos = [
    ("Transporte (combustível, app, estacionamento)", "Inclui o deslocamento de ida e volta."),
    ("Alimentação", "Às vezes é preciso almoçar fora para chegar no horário."),
    ("Equipamentos, acessórios e baterias (desgaste/aluguel)", "Celulares extras, power banks, estabilizador, microfone."),
    ("Apps e assinaturas (parcela do mês)", "Ex.: CapCut pago."),
    ("Outros", ""),
]
d0 = rd + 1
for i, (nome, obs) in enumerate(diretos, d0):
    cc.cell(row=i, column=1, value=nome).border = BORDER
    style(cc.cell(row=i, column=2), "in", BRL)
    cc.cell(row=i, column=4, value=obs).font = SUB_FONT
d1 = d0 + len(diretos) - 1
dt = d1 + 1
cc.cell(row=dt, column=1, value="Subtotal custos diretos").font = Font(bold=True)
cc.cell(row=dt, column=2, value=f"=SUM(B{d0}:B{d1})"); style(cc.cell(row=dt, column=2), "calc", BRL)

# Parâmetros e resultado
rp = dt + 2
cc.cell(row=rp, column=1, value="Parâmetros").font = Font(bold=True, color=CINZA)
cc.cell(row=rp + 1, column=1, value="Impostos e taxas sobre o valor cobrado (%)")
style(cc.cell(row=rp + 1, column=2, value=0), "in", PCT)
cc.cell(row=rp + 2, column=1, value="Margem de lucro desejada (%)")
style(cc.cell(row=rp + 2, column=2, value=0), "in", PCT)
cc.add_data_validation(dv_pct3 := DataValidation(type="decimal", operator="between", formula1="0", formula2="0.95", allow_blank=True,
                                                  error="Use um percentual entre 0% e 95%."))
dv_pct3.add(f"B{rp+1}:B{rp+2}")
imp, mar = f"B{rp+1}", f"B{rp+2}"

rr = rp + 4
header(cc, rr, ["Resultado", "Valor", "", ""])
res = [
    ("Total de horas trabalhadas (você + equipe)", f"=B{rt}+SUM(B{eq0}:B{eq1})", '0.0'),
    ("Custo total (horas + equipe + diretos)", f"=C{rt}+D{eqt}+B{dt}", BRL),
    ("PREÇO MÍNIMO SUGERIDO", f"=IF(({imp}+{mar})>=1,0,B{rr+2}/(1-{imp}-{mar}))", BRL),
]
for i, (nome, f, fmt) in enumerate(res, rr + 1):
    cc.cell(row=i, column=1, value=nome).border = BORDER
    cc.cell(row=i, column=2, value=f); style(cc.cell(row=i, column=2), "calc", fmt)
cc.cell(row=rr + 3, column=1).font = Font(bold=True, color=LARANJA)
cc.cell(row=rr + 3, column=2).font = Font(bold=True, color=LARANJA)
vp = rr + 4
cc.cell(row=vp, column=1, value="Valor que você vai propor ao cliente (R$)").font = Font(bold=True)
style(cc.cell(row=vp, column=2), "in", BRL)
cc.cell(row=vp + 1, column=1, value="Impostos e taxas sobre o valor proposto").border = BORDER
cc.cell(row=vp + 1, column=2, value=f"=N(B{vp})*{imp}"); style(cc.cell(row=vp + 1, column=2), "calc", BRL)
cc.cell(row=vp + 2, column=1, value="Lucro bruto estimado").border = BORDER
cc.cell(row=vp + 2, column=2, value=f"=N(B{vp})-B{vp+1}-B{rr+2}"); style(cc.cell(row=vp + 2, column=2), "calc", BRL)
cc.cell(row=vp + 3, column=1, value="Quanto sobra por hora SUA (lucro + valor das suas horas) ÷ suas horas").border = BORDER
cc.cell(row=vp + 3, column=2, value=f"=IF(B{rt}=0,0,(B{vp+2}+C{rt})/B{rt})"); style(cc.cell(row=vp + 3, column=2), "calc", BRL)
cc.cell(row=vp + 4, column=1, value="Alerta").border = BORDER
cc.cell(row=vp + 4, column=2,
        value=f'=IF(N(B{vp})=0,"Preencha o valor proposto",IF(B{vp}<B{rr+3},"Abaixo do preço mínimo sugerido","OK"))')
style(cc.cell(row=vp + 4, column=2), "calc")
red = PatternFill("solid", fgColor="FADBD8")
cc.conditional_formatting.add(f"B{vp+4}", FormulaRule(formula=[f'B{vp+4}="Abaixo do preço mínimo sugerido"'], fill=red))

cc.column_dimensions["A"].width = 58
cc.column_dimensions["B"].width = 26
cc.column_dimensions["C"].width = 16
cc.column_dimensions["D"].width = 62
cc.freeze_panes = "A9"


# ---------------- Pacotes de serviço (vivência DocMe) ----------------
ps = wb.create_sheet("Pacotes de serviço")
ps["A1"] = "Pacotes de serviço — o que muda de um trabalho simples para um completo"; ps["A1"].font = TITLE_FONT
ps["A2"] = "Exemplo real DocMe nas colunas B e C. Monte o seu na coluna D e use esta tabela para explicar o valor ao cliente."; ps["A2"].font = SUB_FONT
header(ps, 4, ["Item", "Básico (exemplo)", "Completo (exemplo)", "Seu pacote"])
linhas_pac = [
    ("Valor cobrado", 300, 1800),
    ("Pessoas na equipe", "1", "2 (storymaker + auxiliar)"),
    ("Celulares", "1", "5, para não perder nenhum momento"),
    ("Iluminação", "Não", "Sim, kit completo"),
    ("Power banks", "Se tiver", "Sim, vários"),
    ("Se algo falhar", "Sem reserva", "O auxiliar assume a câmera principal: o evento não se perde"),
    ("Captação", "Imagens com o celular", "Imagens com o celular + backstage de produtora"),
    ("Entrega", "Um vídeo curto", "Stories combinados (3 a 10; evento grande pode passar de 30) + Reels final"),
    ("Horas", "Horas do evento", "Horas do evento"),
    ("Prazo", "No dia", "No dia"),
    ("Deslocamento", "Incluso no raio da sua região", "Incluso no raio da sua região (carro e km já no valor)"),
    ("Pagamento", "50% antes, 50% após a entrega", "50% antes, 50% após a entrega"),
]
for i, (item, b, c) in enumerate(linhas_pac, 5):
    ps.cell(row=i, column=1, value=item).border = BORDER
    for col, v in ((2, b), (3, c)):
        cell = ps.cell(row=i, column=col, value=v); cell.border = BORDER
        if isinstance(v, (int, float)): cell.number_format = BRL
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    style(ps.cell(row=i, column=4), "in", BRL if i == 5 else None)
    ps.cell(row=i, column=4).alignment = Alignment(wrap_text=True, vertical="top")
fim = 5 + len(linhas_pac) + 1
ps.cell(row=fim, column=1, value="Como explicar ao cliente").font = Font(bold=True, color=LARANJA)
ps.cell(row=fim + 1, column=1, value="No básico, você recebe imagens e um vídeo curto. No completo, há equipe com reserva, cinco celulares, luz e backstage: se algo acontecer com a câmera principal, o auxiliar assume e o seu evento não se perde.")
ps.merge_cells(start_row=fim + 1, start_column=1, end_row=fim + 1, end_column=4)
ps.cell(row=fim + 1, column=1).alignment = Alignment(wrap_text=True); ps.row_dimensions[fim + 1].height = 48
for col, w in zip("ABCD", (24, 30, 46, 34)): ps.column_dimensions[col].width = w

# ---------------- Equipe e margem ----------------
em = wb.create_sheet("Equipe e margem")
em["A1"] = "Equipe e margem — a equipe cabe no contrato?"; em["A1"].font = TITLE_FONT
em["A2"] = "Antes de aumentar a equipe, confira a margem. Se cair, avise o contratante e renegocie ANTES de contratar mais gente."; em["A2"].font = SUB_FONT
em["A4"] = "Valor do contrato (R$)"; em["A4"].font = Font(bold=True); style(em["B4"], "in", BRL); em["B4"] = 1800
em["A5"] = "Impostos e taxas (%)"; style(em["B5"], "in", PCT); em["B5"] = 0
em["A6"] = "Margem mínima aceitável (%)"; style(em["B6"], "in", PCT); em["B6"] = 0.3
header(em, 8, ["Função", "Quantidade", "Forma de pagamento", "Valor unitário (R$)", "Horas ou dias", "Custo (R$)"])
equipe = [("Storymaker", 1, "Por evento", 350, 1), ("Assistente", 1, "Por dia", 200, 1), ("Pessoa reserva (eventualidades)", 0, "Por dia", 200, 1),
          ("Cinegrafista / outros", 0, "Por dia", 0, 1), ("", 0, "Por evento", 0, 1), ("", 0, "Por hora", 0, 1)]
dvf = DataValidation(type="list", formula1='"Por hora,Por dia,Por evento"', allow_blank=True); em.add_data_validation(dvf)
e0 = 9
for i, (f, q, forma, v, h) in enumerate(equipe, e0):
    for c, val, fmt in ((1, f, None), (2, q, "0"), (3, forma, None), (4, v, BRL), (5, h, "0.0")):
        style(em.cell(row=i, column=c, value=val), "in", fmt)
    em.cell(row=i, column=6, value=f'=B{i}*D{i}*IF(C{i}="Por evento",1,E{i})'); style(em.cell(row=i, column=6), "calc", BRL)
    dvf.add(f"C{i}")
e1 = e0 + len(equipe) - 1
r = e1 + 2
em.cell(row=r, column=1, value="Outros custos (deslocamento fora do raio, alimentação, aluguel de equipamento)"); style(em.cell(row=r, column=6), "in", BRL); em.cell(row=r, column=6).value = 0
res = [("Custo da equipe", f"=SUM(F{e0}:F{e1})", BRL), ("Custo total", f"=F{r+2}+F{r}", BRL),
       ("Impostos e taxas", f"=B4*B5", BRL), ("Lucro", f"=B4-F{r+3}-F{r+4}", BRL),
       ("Margem", f"=IF(B4=0,0,F{r+5}/B4)", PCT),
       ("Sinal (50% antes)", "=B4*0.5", BRL), ("Saldo (50% após a entrega)", "=B4*0.5", BRL),
       ("Alerta", f'=IF(B4=0,"Preencha o valor",IF(F{r+6}<B6,"MARGEM BAIXA: avise o contratante e renegocie antes de aumentar a equipe","OK"))', None)]
for k, (nome, f, fmt) in enumerate(res, r + 2):
    em.cell(row=k, column=1, value=nome).border = BORDER
    em.cell(row=k, column=6, value=f); style(em.cell(row=k, column=6), "calc", fmt)
alerta = r + 2 + len(res) - 1
em.conditional_formatting.add(f"F{alerta}", FormulaRule(formula=[f'LEFT(F{alerta},6)="MARGEM"'], fill=PatternFill("solid", fgColor="FADBD8")))
em.cell(row=alerta + 2, column=1, value="Lição de quem já viveu").font = Font(bold=True, color=LARANJA)
em.cell(row=alerta + 3, column=1, value="Num evento grande, a equipe foi crescendo conforme a grandiosidade do evento aparecia, sem renegociar o contrato. No fim, praticamente 100% do valor ficou com a equipe e a produção: sobrou menos de 3% de lucro. O que faltou: avisar o contratante que seria preciso uma equipe maior e cobrar isso dele antes.")
em.merge_cells(start_row=alerta + 3, start_column=1, end_row=alerta + 3, end_column=6)
em.cell(row=alerta + 3, column=1).alignment = Alignment(wrap_text=True); em.row_dimensions[alerta + 3].height = 48
em.cell(row=alerta + 4, column=1, value="Exemplo DocMe: storymaker de R$350 a R$800 por evento; assistente R$200 por dia; sempre uma pessoa a mais escalada.").font = SUB_FONT
for col, w in zip("ABCDEF", (52, 12, 18, 18, 14, 40)): em.column_dimensions[col].width = w

# ---------------- Hora extra ----------------
he = wb.create_sheet("Hora extra")
he["A1"] = "Hora extra — combine antes, cobre só se acontecer"; he["A1"].font = TITLE_FONT
he["A2"] = "O valor do pacote já considera o previsível. Hora extra só a partir da tolerância combinada."; he["A2"].font = SUB_FONT
campos_he = [("Horas de atraso / excedentes", 0, "0.0"), ("Tolerância sem cobrança (horas)", 2, "0.0"),
             ("Pessoas na equipe (1 ou 2)", 1, "0"), ("Valor por hora extra — 1 pessoa (R$)", 350, BRL), ("Valor por hora extra — 2 pessoas (R$)", 890, BRL)]
for i, (n, v, fmt) in enumerate(campos_he, 4):
    he.cell(row=i, column=1, value=n).border = BORDER; style(he.cell(row=i, column=2, value=v), "in", fmt)
he["A10"] = "Horas cobradas"; he["B10"] = "=MAX(0,B4-B5)"; style(he["B10"], "calc", "0.0")
he["A11"] = "Valor da hora extra"; he["B11"] = "=IF(B6>=2,B8,B7)*B10"; style(he["B11"], "calc", BRL)
he["A11"].font = Font(bold=True, color=LARANJA)
he["A13"] = "Exemplo DocMe: por hora, a partir de 2 horas de atraso; 1 pessoa R$350, 2 pessoas R$890. A hora extra é da produtora: a equipe não recebe a mais, porque isso não faz parte do combinado com ela."; he["A13"].font = SUB_FONT
he.column_dimensions["A"].width = 46; he.column_dimensions["B"].width = 18

for s in wb.worksheets:
    s.sheet_view.showGridLines = False
wb.save(OUT)
print("ok", OUT)
