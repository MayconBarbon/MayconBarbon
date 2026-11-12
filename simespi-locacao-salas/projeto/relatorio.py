"""Relatório PDF da produção — SIMESPI Campanha Locação de Salas."""
import sys, os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
                                Image, PageBreak, KeepTogether)

ROOT = '/tmp/claude-0/-home-user-MayconBarbon/de497f97-c14b-5dad-b9ea-664a26e57efd/scratchpad'
OUT = sys.argv[1]
THUMBS = sys.argv[2]

for w, n in ((300, 'Mont-L'), (500, 'Mont-M'), (600, 'Mont-SB'), (700, 'Mont-B'), (800, 'Mont-XB')):
    pdfmetrics.registerFont(TTFont(n, f'{ROOT}/fonts/Montserrat-{w}.ttf'))

NAVY = colors.HexColor('#083642'); BLUE = colors.HexColor('#276E85'); CYAN = colors.HexColor('#5BC2D6')
INK = colors.HexColor('#1d2a2e'); GREY = colors.HexColor('#5f6b6e'); LIGHT = colors.HexColor('#eef5f7')

st = {
    'h1': ParagraphStyle('h1', fontName='Mont-XB', fontSize=22, leading=27, textColor=NAVY, spaceAfter=4),
    'h2': ParagraphStyle('h2', fontName='Mont-B', fontSize=13.5, leading=18, textColor=NAVY, spaceBefore=12, spaceAfter=6),
    'h3': ParagraphStyle('h3', fontName='Mont-SB', fontSize=10.5, leading=14, textColor=BLUE, spaceBefore=8, spaceAfter=3),
    'p': ParagraphStyle('p', fontName='Mont-M', fontSize=9, leading=13.2, textColor=INK, spaceAfter=4),
    'small': ParagraphStyle('s', fontName='Mont-M', fontSize=7.8, leading=11, textColor=GREY),
    'cell': ParagraphStyle('c', fontName='Mont-M', fontSize=8, leading=10.8, textColor=INK),
    'cellb': ParagraphStyle('cb', fontName='Mont-SB', fontSize=8, leading=10.8, textColor=INK),
    'th': ParagraphStyle('th', fontName='Mont-B', fontSize=8, leading=10.5, textColor=colors.white),
    'kpi': ParagraphStyle('k', fontName='Mont-XB', fontSize=20, leading=22, textColor=NAVY, alignment=TA_CENTER),
    'kpil': ParagraphStyle('kl', fontName='Mont-SB', fontSize=7.5, leading=9.5, textColor=GREY, alignment=TA_CENTER),
    'cap': ParagraphStyle('cap', fontName='Mont-M', fontSize=7, leading=9, textColor=GREY, alignment=TA_CENTER),
}
P = lambda t, s='p': Paragraph(t, st[s])

def header_footer(c, doc):
    W, H = A4
    c.saveState()
    c.setFillColor(NAVY); c.rect(0, H - 14 * mm, W, 14 * mm, fill=1, stroke=0)
    c.setFillColor(CYAN); c.rect(0, H - 14.8 * mm, W, 0.8 * mm, fill=1, stroke=0)
    logo = f'{ROOT}/logo/logo_neg.png'
    c.drawImage(logo, 15 * mm, H - 11.6 * mm, width=26 * mm, height=26 * mm * 487 / 1091, mask='auto')
    c.setFont('Mont-SB', 8); c.setFillColor(colors.white)
    c.drawRightString(W - 15 * mm, H - 8.6 * mm, 'RELATÓRIO DE PRODUÇÃO · CAMPANHA LOCAÇÃO DE SALAS')
    c.setFont('Mont-M', 7); c.setFillColor(GREY)
    c.drawString(15 * mm, 9 * mm, 'Horários em Brasília (UTC−3), apurados pelo histórico de versões e pelos registros dos arquivos.')
    c.drawRightString(W - 15 * mm, 9 * mm, f'Página {doc.page}')
    c.restoreState()

def table(data, widths, head=True, zebra=True):
    rows = []
    for i, r in enumerate(data):
        rows.append([P(x, 'th' if (head and i == 0) else ('cellb' if j == 0 else 'cell')) if isinstance(x, str) else x
                     for j, x in enumerate(r)])
    t = Table(rows, colWidths=widths, repeatRows=1 if head else 0)
    s = [('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 5), ('RIGHTPADDING', (0, 0), (-1, -1), 5),
         ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
         ('LINEBELOW', (0, 0), (-1, -1), 0.3, colors.HexColor('#d5e2e6'))]
    if head: s += [('BACKGROUND', (0, 0), (-1, 0), NAVY)]
    if zebra:
        for i in range(1 if head else 0, len(rows)):
            if i % 2 == 0: s.append(('BACKGROUND', (0, i), (-1, i), LIGHT))
    t.setStyle(TableStyle(s))
    return t

def kpis(items):
    cells = [[P(v, 'kpi') for v, _ in items], [P(l, 'kpil') for _, l in items]]
    t = Table(cells, colWidths=[180 * mm / len(items)] * len(items))
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), LIGHT), ('LINEABOVE', (0, 0), (-1, 0), 2, CYAN),
                           ('TOPPADDING', (0, 0), (-1, 0), 9), ('BOTTOMPADDING', (0, 1), (-1, 1), 9),
                           ('INNERGRID', (0, 0), (-1, -1), 0, colors.white), ('BOX', (0, 0), (-1, -1), 0, colors.white),
                           ('LINEAFTER', (0, 0), (-2, -1), 0.6, colors.white)]))
    return t

story = []
story += [Spacer(1, 4 * mm), P('Relatório de produção', 'h1'),
          P('<font color="#276E85">SIMESPI · Campanha "Você tem o conhecimento. Nós temos o espaço."</font>', 'h3'),
          P('Levantamento do tempo de produção, das solicitações de ajuste e das alterações feitas da primeira entrega até a versão final, '
            'enviada em pacote único para o cliente.'), Spacer(1, 3 * mm)]

story += [kpis([('≈ 1h34', 'TEMPO ATIVO DE PRODUÇÃO'), ('9', 'RODADAS<br/>(1 entrega + 8 ajustes)'),
                ('3 + 9', 'VÍDEOS + ARTES<br/>ESTÁTICAS'), ('R$ 0', 'CUSTO EM SERVIÇOS<br/>PAGOS')]), Spacer(1, 5 * mm)]

story += [P('1. Resumo', 'h2'),
          P('Produção feita entre <b>09/11/2026, 22h30</b> e <b>10/11/2026, 13h39</b> (horário de Brasília). Nesse intervalo houve pausas '
            'aguardando o retorno do cliente; o <b>tempo efetivo de trabalho</b>, somando as rodadas, foi de aproximadamente '
            '<b>1 hora e 34 minutos</b>. Todo o material foi produzido com as <b>8 fotografias reais</b> das salas e o <b>logotipo oficial</b> do Drive, '
            'sem banco de imagens e sem alterar os ambientes.'),
          P('O pacote final tem <b>3 vídeos verticais</b> (Reels 39 s, anúncio 15 s e Tour 29 s), <b>1 capa de Reels</b>, '
            '<b>1 post estático</b>, <b>1 carrossel de 6 cards</b>, <b>3 legendas</b> e um guia LEIA-ME: 21 arquivos, 55 MB.')]

story += [P('2. Linha do tempo e tempo gasto por rodada', 'h2')]
rounds = [
    ['#', 'Data / horário', 'Solicitação do cliente', 'O que foi feito', 'Tempo'],
    ['0', '09/11 · 22h30–23h03', 'Briefing completo: Reels 35–40 s, anúncio 15 s, capa e legenda',
     'Download e análise das 8 fotos, do logo e do manual; paleta conferida no site; trilha composta; locução; montagem e render do '
     'Reels (39 s) e do anúncio (15 s); capa; legenda; auditoria; projeto de edição; pasta no Drive', '33 min'],
    ['1', '09/11 · 23h03–23h07', '"Cadê os 3 vídeos?"',
     'Criação do 3º vídeo: Tour pelas salas (29 s), com Sala 01, Sala 02, usos e chamada', '4 min'],
    ['2', '09/11 · 23h07–23h12', '"Foque na TV e pode dar movimento"',
     'Aproximações da câmera em direção à TV e movimentos laterais em todos os planos; moldura acompanhando a tela; capa reenquadrada', '5 min'],
    ['3', '09/11 · 23h12–23h33', 'Mesma voz da Importway; locução mais humana, animada e convidativa',
     'Voz da Importway identificada (ElevenLabs "Gabriel"), mas sem créditos. Nova voz neural brasileira (Antonio), mais animada; '
     'textos ressincronizados', '21 min'],
    ['4', '09/11 · 23h33–23h39', '"Corrija a fala para CIMESP"',
     '8 grafias testadas por transcrição automática; escolhida "Si-mésp"; final da fala ajustado no anúncio', '6 min'],
    ['5', '09/11 · 23h39–23h46', 'Imagem estática com a dimensão da sala + carrossel destacando a lousa',
     'Post 4:5 com cota de amplitude; carrossel de 6 cards com a lousa em todos; legendas; upload ao Drive', '7 min'],
    ['6', '10/11 · 09h45–09h53', 'Pronúncia "Si-MÉS-pi"; centralizar o texto do painel; corrigir a moldura da TV',
     'Falas regravadas; textos do painel centralizados nos 3 vídeos; telas medidas de novo nas fotos e moldura centralizada em todas as peças', '8 min'],
    ['7', '10/11 · 09h53–09h59', 'Logo do SIMESPI no painel isolado de baixo',
     'Logo oficial no rodapé do painel dos 3 vídeos e do card 6; logo duplicado removido', '6 min'],
    ['8', '10/11 · 13h35–13h39', 'Tudo em uma única pasta para o cliente',
     'Pasta organizada (vídeos, capa, post, carrossel, legendas, LEIA-ME) e ZIP verificado', '4 min'],
    ['', '', '', '<b>Total de tempo ativo</b>', '<b>≈ 1h34</b>'],
]
story += [P('O tempo de cada rodada vai do início do trabalho até o registro da versão no histórico. Os intervalos entre rodadas '
            '(espera pelo retorno do cliente) não entram na soma.', 'small'), Spacer(1, 2 * mm),
          table(rounds, [8 * mm, 31 * mm, 44 * mm, 79 * mm, 18 * mm])]

story += [P('3. Alterações em cada peça até a versão final', 'h2')]
changes = [
    ['Peça', 'Versão inicial', 'Alterações até a final'],
    ['Reels principal (39 s)', 'Fotos com escala sutil, textos animados, voz sintética provisória',
     'Câmera se aproximando da TV · moldura acompanhando a tela · voz mais humana e animada · pronúncia "Si-MÉS-pi" · '
     'moldura centralizada · painel final centralizado · logo no painel'],
    ['Anúncio (15 s)', 'Frase de abertura e lousa no 1º quadro, chamada e logo',
     'Mesmas alterações do Reels · fala final antecipada e transição da trilha removida para o "p" de SIMESPI não sumir'],
    ['Tour pelas salas (29 s)', 'Não existia (criado na rodada 1)',
     'Movimento focado na TV · nova voz · pronúncia · painel centralizado · logo no painel'],
    ['Capa do Reels', 'Foto da Sala 01 + "Seu conhecimento merece esse espaço."', 'Reenquadrada com a TV em destaque'],
    ['Post estático', 'Criado na rodada 5', 'Moldura da TV recentralizada (rodada 6)'],
    ['Carrossel (6 cards)', 'Criado na rodada 5', 'Moldura recentralizada · card 6 centralizado com o logo no painel e sem o logo duplicado do topo'],
    ['Legendas', 'Legenda do Reels', 'Legendas novas para o carrossel e o post estático'],
]
story += [table(changes, [36 * mm, 52 * mm, 92 * mm])]

story += [P('4. Recursos e custos', 'h2')]
cost = [
    ['Recurso', 'Uso', 'Custo'],
    ['ElevenLabs (voz "Gabriel", trilha)', '4 pedidos de voz (6 gerações) e 1 de trilha (2 gerações), todos recusados por saldo: 83 créditos, contra ~1.210 necessários para a locução completa', 'R$ 0 (nada cobrado)'],
    ['Microsoft Edge · voz neural "Antonio"', 'Locução final: 12 falas e várias regravações de pronúncia', 'Gratuito*'],
    ['Piper TTS (voz "faber")', 'Locução provisória das rodadas 0 a 2', 'Gratuito (código aberto)'],
    ['Trilha sonora', 'Composta e sintetizada em código (100 BPM), versões de 39, 15 e 29 s', 'Gratuito, sem direitos de terceiros'],
    ['Fonte Montserrat', 'Títulos e textos de todas as peças', 'Gratuito (licença OFL)'],
    ['Whisper (transcrição)', 'Checagem automática da pronúncia e da clareza da voz', 'Gratuito (código aberto)'],
    ['Google Drive / GitHub', 'Fontes, entregas e histórico de versões', 'Sem custo adicional'],
]
story += [table(cost, [52 * mm, 96 * mm, 32 * mm]),
          P('* A voz neural da Microsoft vem do serviço gratuito de leitura do Edge, cuja licença comercial não é clara. Para anúncio pago, '
            'recomenda-se recarregar o ElevenLabs (~1.300 créditos) e gerar a mesma narração com a voz "Gabriel", sem refazer a edição.', 'small')]

vol_head = P('5. Volume de produção', 'h2')
vol = [
    ['Item', 'Quantidade'],
    ['Versões registradas no histórico', '8'],
    ['Renderizações completas de vídeo (1080×1920, 30 fps)', '14 (até 3.204 quadros por rodada com os 3 vídeos)'],
    ['Falas de locução geradas, incluindo testes de pronúncia', '≈ 50'],
    ['Artes estáticas finais', '8 (capa, post, 6 cards)'],
    ['Arquivos no pacote do cliente', '21 (55 MB)'],
]
story += [KeepTogether([vol_head, table(vol, [110 * mm, 70 * mm])])]

story += [P('6. Pontos para validar com o cliente', 'h2'),
          P('• <b>Locução:</b> ouvir a versão final antes de publicar (a revisão foi por medição e transcrição automática).<br/>'
            '• <b>Lousa nas duas salas:</b> as fotos mostram o mesmo tipo de tela nas duas; confirmar se as duas têm o equipamento.<br/>'
            '• <b>Nomes "Sala 01" e "Sala 02":</b> seguem as pastas do Drive; confirmar se são os nomes usados comercialmente.<br/>'
            '• <b>Medidas:</b> se o cliente informar m² ou capacidade, o post estático pode trazer o número na cota.<br/>'
            '• <b>Instagram @simespi:</b> o perfil exige login e não pôde ser analisado; a identidade seguiu o manual de marca e o site oficial.')]

if os.path.isdir(THUMBS):
    story += [PageBreak(), P('7. Versão final: peças entregues', 'h2')]
    items = [('reels.jpg', 'Reels 39 s'), ('ad.jpg', 'Anúncio 15 s'), ('tour.jpg', 'Tour 29 s'), ('capa.jpg', 'Capa do Reels')]
    row = [Image(f'{THUMBS}/{f}', width=40 * mm, height=71 * mm) for f, _ in items]
    cap = [P(c, 'cap') for _, c in items]
    t = Table([row, cap], colWidths=[45 * mm] * 4); t.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER')]))
    story += [t, Spacer(1, 5 * mm)]
    items = [('post.jpg', 'Post estático')] + [(f'c{i}.jpg', f'Carrossel {i:02d}/06') for i in range(1, 7)]
    imgs = [Image(f'{THUMBS}/{f}', width=40 * mm, height=50 * mm) for f, _ in items]
    caps = [P(c, 'cap') for _, c in items]
    rows = [imgs[0:4], caps[0:4], imgs[4:8] + [''] * (4 - len(imgs[4:8])), caps[4:8] + [''] * (4 - len(caps[4:8]))]
    t = Table(rows, colWidths=[45 * mm] * 4); t.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('BOTTOMPADDING', (0, 1), (-1, 1), 8)]))
    story += [t]

doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=15 * mm, rightMargin=15 * mm, topMargin=22 * mm, bottomMargin=16 * mm,
                      title='SIMESPI — Relatório de produção', author='Produção audiovisual')
doc.addPageTemplates([PageTemplate(id='p', frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='f')],
                                   onPage=header_footer)])
doc.build(story)
print('ok', OUT)
