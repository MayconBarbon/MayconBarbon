import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether)
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

S = "/tmp/claude-0/-home-user-MayconBarbon/e50a6a57-cde3-5f78-9f29-1a0320ad8079/scratchpad"
for n, f in [("P", "Medium"), ("PB", "Bold"), ("PX", "ExtraBold"), ("PS", "SemiBold")]:
    pdfmetrics.registerFont(TTFont(n, f"{S}/fonts/Poppins-{f}.ttf"))
from reportlab.lib.fonts import addMapping
for b,i,f in [(0,0,"P"),(1,0,"PB"),(0,1,"P"),(1,1,"PB")]: addMapping("P",b,i,f)
OR = colors.HexColor("#E9570D"); DK = colors.HexColor("#262628"); GR = colors.HexColor("#6b6b70"); LG = colors.HexColor("#f3f3f4")
st = lambda **k: ParagraphStyle("x", **k)
H1 = st(fontName="PX", fontSize=22, leading=27, textColor=DK, spaceAfter=4)
H2 = st(fontName="PB", fontSize=13.5, leading=18, textColor=OR, spaceBefore=12, spaceAfter=5)
B = st(fontName="P", fontSize=9.2, leading=13.4, textColor=DK)
BS = st(fontName="P", fontSize=8, leading=11, textColor=GR)
TH = st(fontName="PB", fontSize=8.4, leading=11, textColor=colors.white)
TD = st(fontName="P", fontSize=8.2, leading=11.2, textColor=DK)
TDB = st(fontName="PS", fontSize=8.2, leading=11.2, textColor=DK)

def tbl(rows, widths, head=True):
    data = [[Paragraph(str(c), TH if (head and i == 0) else (TDB if j == 0 else TD)) for j, c in enumerate(r)] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if head else 0)
    s = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
         ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
         ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.HexColor("#dddde0"))]
    if head: s += [("BACKGROUND", (0, 0), (-1, 0), DK)]
    for i in range(1 if head else 0, len(rows)):
        if i % 2 == 0: s.append(("BACKGROUND", (0, i), (-1, i), LG))
    t.setStyle(TableStyle(s)); return t

def footer(c, d):
    c.saveState(); c.setFillColor(OR); c.rect(0, A4[1] - 6, A4[0], 6, fill=1, stroke=0)
    c.setFont("P", 7.5); c.setFillColor(GR)
    c.drawString(18 * mm, 10 * mm, "DocMe · Reel Confraternizações · Relatório de produção")
    c.drawRightString(A4[0] - 18 * mm, 10 * mm, f"pág. {d.page}"); c.restoreState()

doc = SimpleDocTemplate(sys.argv[1], pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm, bottomMargin=18 * mm,
                        title="Relatório de produção — Reel DocMe Confraternizações", author="DocMe")
W = A4[0] - 36 * mm
E = []
E += [Image(f"{S}/pdf/logo_plate.png", width=52 * mm, height=52 * mm * 1085 / 3114, hAlign="LEFT"),
      Spacer(1, 6),
      Paragraph("Relatório de produção", H1),
      Paragraph("Reel Instagram 9:16 · 25 s · Cobertura de foto e vídeo para confraternizações", st(fontName="PS", fontSize=11, leading=15, textColor=GR)),
      Spacer(1, 4),
      Paragraph("Período: 11/11/2026, das 10h19 às 13h33 (horário de Brasília). Este relatório foi emitido em 12/11/2026.", BS),
      Spacer(1, 10)]

E += [Paragraph("Resumo", H2),
      tbl([["Item", "Valor"],
           ["Versão final", "v3 Deep House: <b>DocMe_Confra_DeepHouse_25s_locucao.mp4</b> (e a versão só com trilha)"],
           ["Rodadas de pedido", "5 (v1 original › v2 balada › v3 lounge house › abertura nova › deep house)"],
           ["Tempo total de trabalho", "<b>cerca de 1h20</b> de produção ativa, distribuída em cerca de 3h14 corridas (com intervalos de revisão do cliente)"],
           ["Vídeos entregues", "6 MP4 (3 versões × com locução / só trilha) + trilhas e prévias"],
           ["Gasto ElevenLabs", "<b>~2.237 créditos (~US$ 0,41)</b>: locução, música e transcrição"],
           ["Outros custos", "Nenhum. Trilhas v1, v2 e v3-lounge sintetizadas em código; fonte Poppins (licença livre OFL)"],
           ["Formato", "1080×1920, 30 fps, H.264 + AAC, −14 LUFS (padrão Reels), 22–24 MB por arquivo"]],
          [42 * mm, W - 42 * mm])]

E += [Paragraph("Linha do tempo (horário de Brasília, 11/11/2026)", H2),
      tbl([["Horário", "Duração", "Etapa", "O que foi feito"],
           ["10h19–10h40", "~21 min", "Pesquisa do material", "Busca no Google Drive das pastas Hyundai, Manifesta, Avita/Ecoterra e Pax. A Pax não foi encontrada. Teste do limite de download (10 MB) e pergunta ao cliente sobre Pax e compartilhamento."],
           ["10h40–10h43", "~3 min", "Download e triagem", "Fotos e clipes baixados; prévias em folha de contato para escolher as cenas"],
           ["10h43", "~1 min", "Locução", "ElevenLabs, voz Gabriel (pt-BR), 2 takes"],
           ["10h44–10h54", "~10 min", "Montagem v1", "Roteiro em 5 blocos, trilha sintetizada, mixagem, revisão quadro a quadro e entrega"],
           ["", "", "<i>Intervalo: revisão do cliente</i>", ""],
           ["12h24–12h42", "~18 min", "v2 \"balada\"", "Nova pesquisa (Best/Guarujá, Churras da Gratidão, Hyundai), cerca de 30 clipes da Hyundai SP 2024, layout novo, trilha club e entrega"],
           ["12h43–12h49", "~6 min", "v3 lounge house", "Trilha lounge house; final assinado só com a logo"],
           ["12h50–12h53", "~3 min", "Abertura nova", "\"Foto e vídeo para o seu evento\" em 0–2 s; textos e locução deslocados"],
           ["", "", "<i>Intervalo</i>", ""],
           ["13h28–13h33", "~5 min", "Trilha deep house", "Geração no ElevenLabs Music (2 versões), análise de BPM e energia, checagem de voz e mixagem final"],
           ["12/11", "~10 min", "Este relatório", "Levantamento de horários, custos e alterações; PDF"]],
          [24 * mm, 17 * mm, 34 * mm, W - 75 * mm]),
      Paragraph("Durações com \"~\" são aproximadas e foram reconstruídas a partir dos horários de commits, arquivos e gerações. O tempo de produção ativa soma cerca de 1h20 (incluindo este relatório), incluindo a pesquisa e as renderizações.", BS)]

E += [Paragraph("Histórico de versões e alterações", H2)]
thumbs = Table([[Image(f"{S}/pdf/v1.jpg", 30 * mm, 53 * mm), Image(f"{S}/pdf/v2.jpg", 30 * mm, 53 * mm),
                 Image(f"{S}/pdf/v3_0.6.jpg", 30 * mm, 53 * mm), Image(f"{S}/pdf/v3_9.6.jpg", 30 * mm, 53 * mm), Image(f"{S}/pdf/v3_24.6.jpg", 30 * mm, 53 * mm)],
                [Paragraph(x, BS) for x in ["v1 · texto sobre a imagem", "v2 · tela dividida", "v3 · abertura nova", "v3 · cena sobre cena", "v3 · assinatura com a logo"]]],
               colWidths=[W / 5] * 5)
thumbs.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER")]))
E += [thumbs, Spacer(1, 6)]
E += [tbl([["Versão", "Pedido do cliente", "Alterações feitas"],
           ["v1<br/>10h54", "Reel de 25 s com Hyundai, Pax, Manifesta e Ecoterra/Avita; textos e locução definidos",
            "Montagem em 5 blocos, com 29 planos, selos por evento, textos sobre a imagem, trilha house elegante (código) e locução. Pax ausente no Drive."],
           ["v2<br/>12h42", "Textos fora da imagem, no terço de baixo; sem Manifesta; mais pessoas comemorando; mais balada, mais cortes, tela quebrada, cena sobre cena; incluir Best (Guarujá) e Churras da Gratidão",
            "Imagens nos 2/3 de cima e painel de texto embaixo; 37 planos de 0,25 a 1 s; tela dividida em 2 e em 3 e picture-in-picture; textos cinéticos (PISTA CHEIA, ENCONTROS, SHOW, DRINKS, SORRISOS); trilha club; só material Hyundai SP 2024. Best e Churras não encontrados."],
           ["v3<br/>12h49", "Música mais house/lounge house agitada; final assinado só com a logo, sem escrever \"DocMe\"",
            "Trilha lounge house nova; texto \"DocMe.\" removido; a logo entra em 23,3 s, junto com a voz"],
           ["v3.1<br/>12h53", "Nos 2 primeiros segundos, algo como \"foto e vídeo para o seu evento\"",
            "Abertura \"Foto e vídeo para o seu evento\" (0–2 s); pergunta em 2–4,6 s; \"Para guardar cada momento\" em 4,6–9 s; locução deslocada"],
           ["v3.2 (final)<br/>13h33", "Música mais eletrônica e agitada, deep house",
            "Trilha deep house gerada por IA (ElevenLabs Music, ~121 BPM, instrumental confirmado por transcrição); remixagem com a locução"]],
          [22 * mm, 62 * mm, W - 84 * mm])]

E += [Paragraph("Gastos com ferramentas (ElevenLabs)", H2),
      tbl([["Item", "Quantidade", "Créditos", "US$"],
           ["Locução (voz Gabriel, multilingual v2)", "2 takes de 9,7 s", "300", "0,05"],
           ["Música deep house (eleven_music_v2_5)", "2 versões de 25 s (1 usada)", "1.800", "0,33"],
           ["Transcrição de checagem (scribe v1)", "1 × 25 s", "138", "0,03"],
           ["<b>Total</b>", "", "<b>~2.237</b>", "<b>~0,41</b>"]],
          [72 * mm, 50 * mm, 25 * mm, W - 147 * mm]),
      Paragraph("Correção: na mensagem de entrega da trilha deep house informei \"cerca de 1.940 créditos\". O valor correto, somando também a locução, é ~2.237. Antes de gerar a música, a estimativa prévia indicava 3.300 créditos; a cobrança real foi menor. Verifique se o plano do ElevenLabs inclui licença comercial para a música gerada.", BS)]

E += [Paragraph("Material utilizado (versão final)", H2),
      Paragraph("Pasta <b>HYUNDAI - CONFRATERNIZAÇÃO SP - 2024 / VÍDEOS - BRUTOS</b>: IMG_3683, 3753, 3766, 3778, 3784, 3829, 3832, 3842, 3854, 3855, 3860, 3861, 3862, 3879, 3880, 3882, 3886, 3887, 3889, 3890, 3898, 3900, 3901, 3903. Também foram usados a logo \"DocMe nova versão-4.pdf.png\" e a fonte Poppins.", B),
      Paragraph("Na v1, foram usados também Hyundai Fim de Ano, Manifesta (Integração Colaboradores 2025) e Ecoterra/Avita (inauguração).", BS)]

E += [Paragraph("Pendências", H2),
      tbl([["#", "Ação", "Detalhe"],
           ["1", "Voltar links do Drive para \"Restrito\"", "21 arquivos foram deixados como \"qualquer pessoa com o link\" para permitir o download (o conector não desfaz isso). Hyundai SP: IMG_3766, 3829, 3832, 3842, 3854, 3855, 3862, 3879, 3880, 3886, 3887, 3900, 3901, 3903. Avita: IMG_7191, 7192, 7195, 7196, 7197. Manifesta: IMG_7349. Elring Klinger: After Movie V1.mp4."],
           ["2", "Autorização de imagem", "Confirmar com a Hyundai o uso das imagens de colaboradores em material de portfólio da DocMe"],
           ["3", "Best (Guarujá) e Churras da Gratidão", "Não localizados no Drive. Enviar o link das pastas para incluir numa próxima versão"],
           ["4", "Licença da música", "Verificar se o plano do ElevenLabs inclui uso comercial da trilha deep house"]],
          [8 * mm, 46 * mm, W - 54 * mm])]

E += [Paragraph("Arquivos entregues (repositório, branch claude/elegant-fermi-3t2kpw)", H2),
      tbl([["Pasta", "Arquivos"],
           ["reels/docme-confraternizacoes-v3/  <b>(final)</b>", "DocMe_Confra_DeepHouse_25s_locucao.mp4 · DocMe_Confra_DeepHouse_25s_so_trilha.mp4 · trilha_deep_house.mp3 · trilha_lounge_house.m4a · previa_final.jpg · RELATORIO.md · render2.py · music3.py"],
           ["reels/docme-confraternizacoes-v2/", "DocMe_Confra_Balada_25s_locucao.mp4 · ..._so_trilha.mp4 · trilha_balada.m4a · capa.jpg · previa_cenas.jpg · RELATORIO.md"],
           ["reels/docme-confraternizacoes/", "DocMe_Confraternizacoes_25s_locucao.mp4 · ..._so_trilha.mp4 · trilha_sintetizada.m4a · capa.jpg · previa_cenas.jpg · RELATORIO.md"]],
          [62 * mm, W - 62 * mm])]

doc.build(E, onFirstPage=footer, onLaterPages=footer)
