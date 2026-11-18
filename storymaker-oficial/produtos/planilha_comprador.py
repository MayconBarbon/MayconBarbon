"""Gera a versão da planilha que é VENDIDA: sem as abas internas (Catálogo e Pacotes).
Uso: python3 produtos/planilha_comprador.py  ->  produtos/pdf/planilha-de-custos-e-horas.xlsx
"""
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.styles import Font

RAIZ = Path(__file__).resolve().parent.parent
wb = load_workbook(RAIZ / "planilha" / "storymaker-oficial-produtos-e-custos.xlsx")
for aba in ("Catálogo", "Pacotes"):
    del wb[aba]
ws = wb["Leia primeiro"]
for row in ws.iter_rows(min_row=1, max_row=ws.max_row):
    for c in row:
        c.value = None
textos = [
    ("Planilha de custos e horas — Storymaker Oficial", Font(bold=True, size=16, color="E7570C")),
    ("Método desenvolvido pela DocMe Comunicação.", Font(italic=True, color="5D5C63")),
    ("", None),
    ("COMO USAR", Font(bold=True, color="2B2A30")),
    ("• Células em LARANJA CLARO são para você preencher. Células em CINZA são calculadas: não digite nelas.", None),
    ("", None),
    ("ABA “Custos de cobertura”: monte o orçamento de um evento contando TODAS as horas reais.", None),
    ("   – Briefing, pesquisa do cliente, referências, trilhas e efeitos entram no orçamento, mesmo que você não anuncie isso ao cliente.", None),
    ("   – Some deslocamento, alimentação, horas no evento, edição, upload e entrega.", None),
    ("   – O resultado mostra o preço mínimo sugerido e quanto sobra por hora sua.", None),
    ("", None),
    ("ABA “Pacotes de serviço”: compare um trabalho básico e um completo e explique o valor ao cliente.", None),
    ("ABA “Equipe e margem”: confira se a equipe cabe no contrato ANTES de contratar mais gente.", None),
    ("ABA “Hora extra”: calcule a hora extra a partir da tolerância combinada.", None),
    ("", None),
    ("Os exemplos são da prática da DocMe e não são tabela de preço. Ajuste aos seus custos e à sua região.", Font(italic=True, color="5D5C63")),
]
for i, (t, f) in enumerate(textos, 1):
    ws.cell(row=i, column=1, value=t)
    if f: ws.cell(row=i, column=1).font = f
out = RAIZ / "produtos" / "pdf" / "planilha-de-custos-e-horas.xlsx"
wb.save(out); print("ok", out, wb.sheetnames)
