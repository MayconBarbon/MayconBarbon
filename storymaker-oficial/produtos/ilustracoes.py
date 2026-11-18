"""Ilustrações vetoriais (sem nomes de eventos: regra do fundador) (SVG) da coleção Storymaker Oficial.

Todas usam a paleta da marca: laranja #e7570c, laranja escuro #c2410c,
grafite #2b2a30, cinza #5d5c63 e fundo creme #fff4ec.
Esquemas marcados como "ilustrativo" simplificam um caso real.
"""

# Nos desenhos, áreas com texto branco usam o laranja escuro (#c2410c, 5,2:1) e o terracota (#9a3412, 7:1)
# para o texto pequeno ficar legível; o laranja da marca (#e7570c) fica para formas sem texto.
L, LE, G, C, CR, B = "#c2410c", "#9a3412", "#2b2a30", "#5d5c63", "#fff4ec", "#ffffff"
LM = "#e7570c"
FONT = "font-family:Sora,Inter,sans-serif"


def fig(svg, legenda):
    return f'<figure class="ilustra">{svg}<figcaption>{legenda}</figcaption></figure>'


def _box(x, y, w, h, fill, r=14, stroke=None):
    s = f' stroke="{stroke}" stroke-width="2"' if stroke else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{s}/>'


def _t(x, y, txt, size=13, fill=G, weight=600, anchor="middle"):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}" style="{FONT}">{txt}</text>'


def metodo():
    passos = ["Entender o cliente", "Decidir a publicação", "Mapear o evento",
              "Captar com intenção", "Editar e publicar", "Fechar a história"]
    fases = ["ANTES", "ANTES", "DURANTE", "DURANTE", "DURANTE", "DEPOIS"]
    out = []
    for i, p in enumerate(passos):
        col, row = i % 3, i // 3
        x, y = 10 + col * 140, 14 + row * 110
        cor = L if fases[i] == "DURANTE" else (G if fases[i] == "ANTES" else LE)
        out.append(_box(x, y, 124, 92, cor))
        out.append(_t(x + 20, y + 30, f"0{i+1}", 20, B, 800, "start"))
        out.append(_t(x + 20, y + 48, fases[i], 9, B, 700, "start"))
        w = p.split(" ")
        out.append(_t(x + 20, y + 68, " ".join(w[:2]), 12, B, 600, "start"))
        if len(w) > 2:
            out.append(_t(x + 20, y + 83, " ".join(w[2:]), 12, B, 600, "start"))
        if col < 2:
            out.append(f'<path d="M{x+128} {y+46} l8 0" stroke="{C}" stroke-width="2"/><path d="M{x+134} {y+42} l4 4 l-4 4" fill="none" stroke="{C}" stroke-width="2"/>')
    svg = f'<svg viewBox="0 0 430 240" role="img" aria-label="Os seis passos do Método DocMe">{"".join(out)}</svg>'
    return fig(svg, "O Método DocMe em seis passos: dois antes do evento, três durante e um depois.")


def blocos():
    nomes = ["Objetivo", "Público e espaço", "Publicação", "Programação", "Pessoas",
             "Não pode faltar", "Gosto e referências", "Mudanças e prazos", "Entrega"]
    out = []
    for i, n in enumerate(nomes):
        col, row = i % 3, i // 3
        x, y = 10 + col * 140, 10 + row * 64
        out.append(_box(x, y, 128, 52, CR if i % 2 else B, 12, L))
        out.append(f'<circle cx="{x+22}" cy="{y+26}" r="13" fill="{L}"/>')
        out.append(_t(x + 22, y + 31, str(i + 1), 13, B, 800))
        out.append(_t(x + 42, y + 31, n, 11.5, G, 600, "start"))
    svg = f'<svg viewBox="0 0 430 205" role="img" aria-label="Os nove blocos do roteiro de briefing">{"".join(out)}</svg>'
    return fig(svg, "O roteiro de briefing em nove blocos. Siga a ordem: cada bloco prepara o seguinte.")


def canais():
    out = [_box(10, 10, 200, 190, L), _box(220, 10, 200, 190, CR, 14, C)]
    out.append(_t(110, 42, "NA HORA", 15, B, 800))
    out.append(_t(110, 62, "tempo real", 11, B, 500))
    out.append(_t(320, 42, "PODE SER DEPOIS", 15, G, 800))
    out.append(_t(320, 62, "conteúdo mais elaborado", 11, C, 500))
    for i, n in enumerate(["Instagram", "TikTok"]):
        y = 84 + i * 48
        out.append(_box(30, y, 160, 36, B, 18))
        out.append(f'<circle cx="52" cy="{y+18}" r="6" fill="{L}"/>')
        out.append(_t(118, y + 23, n, 13, G, 700))
    for i, n in enumerate(["LinkedIn", "YouTube", "Facebook"]):
        y = 78 + i * 40
        out.append(_box(240, y, 160, 32, B, 16, "#e7e6ea"))
        out.append(_t(320, y + 21, n, 12.5, G, 600))
    svg = f'<svg viewBox="0 0 430 210" role="img" aria-label="Canais que pedem tempo real e canais que aceitam publicação depois">{"".join(out)}</svg>'
    return fig(svg, "Decisão por canal. Mas a regra só vale se o público do evento estiver nesse canal.")


def abc():
    out = []
    niveis = [("A", "Entram no roteiro, com momento definido", L, 150),
              ("B", "Você busca durante a cobertura", LE, 250),
              ("C", "Você aproveita quando aparecem", C, 350)]
    for i, (letra, txt, cor, w) in enumerate(niveis):
        x = 215 - w / 2
        y = 12 + i * 66
        out.append(_box(x, y, w, 56, cor, 12))
        out.append(_t(215, y + 26, letra, 22, B, 800))
        out.append(_t(215, y + 45, txt, 10.5, B, 500))
    svg = f'<svg viewBox="0 0 430 212" role="img" aria-label="Lista A, B e C de pessoas">{"".join(out)}</svg>'
    return fig(svg, "Lista A/B/C: as cerca de dez pessoas mais importantes do evento, por prioridade.")


def sequencia():
    blocos_ = [("1", "O lugar", "fachada, decoração, localização"),
               ("2", "As pessoas", "recepção, personalidades"),
               ("3", "As atrações", "banda, comida, bebida"),
               ("4", "Os momentos", "abertura, fala, homenagem")]
    out = []
    for i, (n, t, s) in enumerate(blocos_):
        x = 8 + i * 106
        out.append(_box(x, 8, 92, 164, G, 16))
        out.append(_box(x + 6, 14, 80, 152, L if i % 2 == 0 else LE, 12))
        out.append(f'<rect x="{x+12}" y="22" width="{68*(1 if i < 3 else .4)}" height="3" rx="1.5" fill="{B}"/>')
        out.append(_t(x + 46, 80, n, 34, B, 800))
        out.append(_t(x + 46, 108, t, 12, B, 700))
        out.append(_t(x + 46, 150, "~30 s", 10, B, 600))
        words = s.split(", ")
        for j, w in enumerate(words[:3]):
            out.append(_t(x + 46, 190 + j * 13, w, 9.5, C, 500))
    svg = f'<svg viewBox="0 0 430 232" role="img" aria-label="Sequência de quatro stories">{"".join(out)}</svg>'
    return fig(svg, "A sequência que funciona: do espaço para as pessoas, das pessoas para as experiências.")


def fluxos():
    out = []
    def lane(y, titulo, passos, cor):
        out.append(_t(10, y + 4, titulo, 12, cor, 800, "start"))
        x = 10
        for i, p in enumerate(passos):
            w = 78
            fill = cor if i == len(passos) - 1 else B
            tc = B if i == len(passos) - 1 else G
            out.append(_box(x, y + 14, w, 44, fill, 10, None if fill == cor else "#d9d8dd"))
            parts = p.split("|")
            for j, pp in enumerate(parts):
                out.append(_t(x + w / 2, y + 34 + j * 13 - (len(parts) - 1) * 6, pp, 10.5, tc, 600))
            if i < len(passos) - 1:
                out.append(f'<path d="M{x+w+2} {y+36} l6 0" stroke="{C}" stroke-width="2"/>')
            x += w + 10
    lane(10, "FLUXO A — o storymaker publica", ["Capta", "Edita no|celular", "Publica no|perfil do cliente"], L)
    lane(92, "FLUXO B — o cliente aprova e publica", ["Capta", "Edita no|celular", "Envia ao|grupo", "Cliente|aprova", "Cliente|publica"], LE)
    svg = f'<svg viewBox="0 0 450 170" role="img" aria-label="Dois fluxos de publicação">{"".join(out)}</svg>'
    return fig(svg, "Os dois fluxos de publicação. Quem escolhe é sempre o cliente; os dois funcionam.")


def bestseller():
    out = []
    x0, x1, h0, h1 = 70, 420, 9, 17  # 9h às 17h
    def px(h):
        return x0 + (h - h0) / (h1 - h0) * (x1 - x0)
    for h in range(h0, h1 + 1, 2):
        out.append(f'<line x1="{px(h)}" y1="26" x2="{px(h)}" y2="196" stroke="#e7e6ea"/>')
        out.append(_t(px(h), 18, f"{h}h", 10, C, 600))
    out.append(_t(8, 58, "PLANEJADO", 10, G, 800, "start"))
    out.append(_t(8, 150, "NO DIA", 10, LE, 800, "start"))
    plan = [("Palestrante 1", 9, 11), ("Palestrante 2", 11.5, 13.5), ("Palestrante 3", 14, 16)]
    for i, (n, a, b) in enumerate(plan):
        y = 32 + i * 22
        out.append(_box(px(a), y, px(b) - px(a), 18, G, 6))
        out.append(_t((px(a) + px(b)) / 2, y + 13, n, 9.5, B, 600))
    real = [("Palestrante 1", 9, 11, G), ("Palestrante 2 ?", 11.5, 13.5, "#bdbcc2"), ("Palestrante 3", 14, 16, G), ("Palestrante 2", 14, 16, L)]
    ys = [118, 140, 162, 182]
    for (n, a, b, cor), y in zip(real, ys):
        out.append(_box(px(a), y, px(b) - px(a), 16, cor, 6))
        out.append(_t((px(a) + px(b)) / 2, y + 12, n, 9, B, 600))
    out.append(f'<path d="M{px(13.6)} 148 C {px(15)} 150, {px(14.2)} 170, {px(14.6)} 182" fill="none" stroke="{L}" stroke-width="2" stroke-dasharray="4 3"/>')
    out.append(_t(px(16.1), 194, "conflito", 10, L, 800, "start"))
    svg = f'<svg viewBox="0 0 430 206" role="img" aria-label="Grade planejada e grade real no congresso de negócios">{"".join(out)}</svg>'
    return fig(svg, "Esquema ilustrativo do congresso de negócios: a palestra mudou de horário sem aviso e caiu em cima da grade de outro palestrante.")


def barras():
    out = [_t(10, 20, "Visualizações", 11, C, 600, "start")]
    dados = [("No dia", "vídeo publicado no fim do evento", 10000, L), ("Depois", "aftermovie, uma semana depois", 1500, C)]
    for i, (rot, sub, v, cor) in enumerate(dados):
        y = 36 + i * 70
        w = 300 * v / 10000
        out.append(_t(10, y + 14, rot, 13, G, 800, "start"))
        out.append(_t(10, y + 30, sub, 9.5, C, 500, "start"))
        out.append(f'<rect x="10" y="{y+38}" width="300" height="18" rx="9" fill="#efeef1"/>')
        out.append(f'<rect x="10" y="{y+38}" width="{max(w, 18)}" height="18" rx="9" fill="{cor}"/>')
        out.append(_t(322, y + 52, f"{v:,}".replace(",", "."), 18, G, 800, "start"))
    svg = f'<svg viewBox="0 0 430 180" role="img" aria-label="10 mil visualizações no dia contra 1.500 no aftermovie">{"".join(out)}</svg>'
    return fig(svg, "Evento infantil: dois vídeos, duas propostas. O horário de publicação não é a única explicação para a diferença.")


def bateria():
    out = []
    momentos = ["Chegada", "Recepção", "Momento-chave", "Intervalo", "Encerramento", "Edição"]
    nivel = [100, 72, 40, 85, 55, 35]
    x0, w = 30, 380
    pts = []
    for i, (m, n) in enumerate(zip(momentos, nivel)):
        x = x0 + i * w / (len(momentos) - 1)
        y = 150 - n * 1.1
        pts.append((x, y))
        out.append(_t(x, 176, m, 9.5, G if m != "Intervalo" else L, 700))
    out.append(f'<line x1="{x0}" y1="150" x2="{x0+w}" y2="150" stroke="#d9d8dd"/>')
    out.append(f'<line x1="{x0}" y1="{150-20*1.1}" x2="{x0+w}" y2="{150-20*1.1}" stroke="{LE}" stroke-dasharray="4 4"/>')
    out.append(_t(x0 + w, 150 - 20 * 1.1 - 6, "zona de risco (20%)", 9, LE, 600, "end"))
    d = "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts)
    out.append(f'<path d="{d}" fill="none" stroke="{G}" stroke-width="3" stroke-linejoin="round"/>')
    for (x, y), n, m in zip(pts, nivel, momentos):
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="{L if m == "Intervalo" else G}"/>')
    ix, iy = pts[3]
    out.append(_t(ix, iy - 12, "recarregar", 10, L, 800))
    svg = f'<svg viewBox="0 0 430 190" role="img" aria-label="Planejamento de bateria ao longo do evento">{"".join(out)}</svg>'
    return fig(svg, "Esquema ilustrativo: use os momentos de menor movimento para recarregar antes da zona de risco.")


def estrutura():
    out = [_box(10, 10, 200, 150, CR, 14), _box(220, 10, 200, 150, B, 14, "#e7e6ea")]
    out.append(_t(110, 36, "EQUIPE DOCME", 11, LE, 800))
    out.append(_t(320, 36, "STORYMAKER SOLO", 11, G, 800))
    for i in range(5):
        x = 28 + i * 34
        out.append(_box(x, 54, 24, 44, G, 5))
        out.append(_box(x + 3, 58, 18, 36, L, 3))
    for i in range(3):
        x = 50 + i * 40
        out.append(_box(x, 112, 30, 18, C, 4))
        out.append(f'<rect x="{x+30}" y="117" width="3" height="8" rx="1" fill="{C}"/>')
    out.append(_t(110, 148, "até 5 celulares e 3 power banks", 10, G, 600))
    out.append(_box(304, 54, 30, 54, G, 6))
    out.append(_box(308, 59, 22, 44, L, 4))
    out.append(_t(320, 130, "1 celular: planeje", 10, G, 600))
    out.append(_t(320, 144, "bateria e recargas", 10, G, 600))
    svg = f'<svg viewBox="0 0 430 170" role="img" aria-label="Estrutura de equipe e de quem trabalha sozinho">{"".join(out)}</svg>'
    return fig(svg, "A estrutura muda, o método não: quem trabalha sozinho compensa com planejamento.")


# Onde cada ilustração entra no e-book 2 (inserida logo depois do título indicado)
EBOOK2 = {
    "Antes de começar: de onde vem este método": metodo,
    "O roteiro de perguntas": blocos,
    "Decisão por canal": canais,
    "A lista A/B/C de pessoas": abc,
    "A sequência que funciona": sequencia,
    "Quem publica e quem aprova": fluxos,
    "O que aconteceu": bestseller,
    "O caso": barras,
    "A estrutura de uma equipe": estrutura,
    "Como planejar a bateria": bateria,
}
