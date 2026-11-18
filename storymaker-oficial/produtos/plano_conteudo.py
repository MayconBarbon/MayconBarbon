"""Plano de conteúdo de 3 meses (3 posts por semana) para Instagram e TikTok.
Gera docs/plano-de-conteudo-3-meses.xlsx e .pdf.  Uso: python3 produtos/plano_conteudo.py

Regras: eventos com nome genérico (marcar o cliente só com autorização); nada de preto nas letras;
palavras-chave da pesquisa de 18/11/2026 (docs/palavras-chave.md); sem promessa de renda.
Formatos: Reels (mesmo vídeo vai para o TikTok), Carrossel (no TikTok, modo foto), Stories.
"""
import datetime as dt, subprocess
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation

RAIZ = Path(__file__).resolve().parent.parent
INICIO = dt.date(2026, 11, 23)  # segunda-feira
DIAS = {"Seg": 0, "Qua": 2, "Sex": 4}
FASES = {1: "Aquecimento", 2: "Aquecimento", 3: "Abertura das vendas", 4: "Vendas + fim de ano", 5: "Fim de ano",
         6: "Fim de ano", 7: "Relançamento 2027", 8: "Relançamento 2027", 9: "Portas por público", 10: "Portas por público",
         11: "Novos produtos", 12: "Novos produtos", 13: "Balanço e próximo ciclo"}

# (semana, dia, formato, pilar, público, gancho na tela, roteiro (cenas), legenda, chamada, palavras-chave)
P = [
 (1,"Seg","Reels","Ensino","Todos","O que é storymaker (e o que ele NÃO é)",
  "1) Celular gravando vertical no evento 2) Texto: não é só postar stories 3) Briefing com cliente 4) Edição rápida no CapCut 5) Reels final aprovado",
  "Storymaker conta a história do evento enquanto ela acontece: planeja, capta, edita e publica. Não é só apertar o REC.","Siga para aprender o método","storymaker o que é, story maker o que faz"),
 (1,"Qua","Carrossel","Prova","Todos","30 eventos. 1 método.",
  "Capa com mosaico de coberturas; 1 slide por tipo de evento (congresso, casamento, festa, ação beneficente); slide final: o método em 6 passos",
  "Congressos, casamentos, festas tradicionais, ações beneficentes. Cada evento é diferente, o raciocínio é o mesmo.","Salve para lembrar dos 6 passos","storymaker eventos, storymaker para eventos"),
 (1,"Sex","Reels","Bastidores","Todos","Como é um dia de storymaker em um congresso",
  "Timelapse da chegada; credenciamento; palco; plateia; edição no corredor; story publicado; fim do dia",
  "Bastidores de um congresso em São Paulo: 15 stories por dia, tudo planejado antes.","Comente STORY se quer ver o roteiro","storymaker evento corporativo"),
 (2,"Seg","Reels","Ensino","Iniciante","Comece com a padaria do bairro",
  "1) Fachada da padaria 2) Conversa com a dona 3) Pão saindo do forno 4) Plano aberto x detalhe 5) Foto escolhida",
  "Você não precisa de um grande evento para começar. Precisa de intenção, conversa e uma boa foto.","Leia o artigo completo no blog (link na bio)","como começar como storymaker, storymaker iniciante"),
 (2,"Qua","Carrossel","Ensino","Todos","As 9 perguntas do briefing que salvam a cobertura",
  "Capa; 9 slides com um bloco cada (objetivo, público, publicação, programação, pessoas, não pode faltar, gosto, mudanças, entrega); final: modelo de briefing",
  "O resultado começa antes de ligar a câmera. Use estas perguntas na próxima reunião.","Salve e use na próxima reunião","briefing storymaker"),
 (2,"Sex","Reels","Erros","Todos","A programação mudou e ninguém avisou",
  "1) Grade planejada na tela 2) Palestrante fora do horário 3) Equipe conversando com o contratante 4) Novo prazo combinado 5) Entrega pelo Drive",
  "Num congresso de negócios, a grade mudou em cima da hora. O que salvou foi conversar cedo e renegociar o prazo.","Comente se já passou por isso","imprevistos evento"),
 (3,"Seg","Reels","Oferta","Todos","Está no ar: o método DocMe em materiais práticos",
  "1) Mãos folheando o e-book no celular 2) Checklist impresso 3) Planilha calculando 4) Contrato 5) Texto: link na bio",
  "Abrimos os primeiros materiais: e-book Do briefing à história, checklist, planilha de custos e modelo de contrato.","Link na bio","storymaker curso"),
 (3,"Qua","Carrossel","Dinheiro","Todos","Quanto cobrar como storymaker: as horas que você não conta",
  "Capa; briefing 1h; pesquisa; referências e trilhas; deslocamento; horas no evento; edição; entrega; slide final: some tudo",
  "O preço não começa quando o evento abre. Some todas as horas antes de responder o orçamento.","Planilha de custos no link da bio","quanto cobrar storymaker, storymaker valor"),
 (3,"Sex","Reels","Bastidores","Videomaker","Do evento ao Reels em 10 minutos",
  "Cronômetro na tela; 15 cenas captadas; CapCut montando; ajuste de ordem; publicado",
  "Quem tem olhar de imagem aprende rápido. A ferramenta acelera, o olhar escolhe.","Siga para mais bastidores","storymaker mobile, edição capcut"),
 (4,"Seg","Reels","Ensino","Todos","Abertos com aberto não funcionam",
  "Mesmo trecho editado de 2 jeitos: só planos abertos x aberto-médio-fechado intercalados",
  "Varie planos e assuntos. É isso que faz o vídeo respirar.","Salve este exemplo","storymaker dicas"),
 (4,"Qua","Carrossel","Ensino","Todos","Confraternização de fim de ano da empresa: o roteiro em 4 stories",
  "1 O lugar (fachada, decoração) 2 As pessoas (recepção) 3 As atrações (banda, comida) 4 Os momentos (brinde, fala)",
  "Época de confraternizações: use esta sequência que a DocMe aplicou numa festa corporativa.","Mande para quem vai cobrir uma festa este mês","storymaker para eventos"),
 (4,"Sex","Reels","Prova","Todos","O que os clientes dizem",
  "Prints de WhatsApp sem identificação, um por vez, com o vídeo entregue ao fundo",
  "Mensagens reais, do jeito que chegaram. Sem nome, com autorização.","Conheça o portfólio (link na bio)","storymaker"),
 (5,"Seg","Reels","Ensino","Todos","Natal e Réveillon: o que gravar com o celular",
  "VÍDEO PRONTO (docs/video/natal-reveillon-30s.mp4): preparação, ceia, detalhes, brinde em família; amigos, brinde da virada, fogos; cartão do Roteiro de fim de ano",
  "Natal é família, momentos e fotos. Réveillon é amigos e quem está do seu lado. O que gravar, em que ordem e como entregar no mesmo dia. Imagens ilustrativas.","Roteiro de fim de ano no link","stories de natal instagram, confraternização de fim de ano"),
 (5,"Qua","Carrossel","Erros","Todos","O casamento atrasou 1 hora. E agora?",
  "Mãe da noiva atrasada; espera; padrinhos; detalhes; noivos; cerimônia",
  "O atraso muda a ordem, não interrompe a história. Tenha sempre uma lista de cenas que não dependem do horário.","Salve para o próximo casamento","storymaker casamento, storymaker casamento dicas"),
 (5,"Sex","Reels","Erros","Todos","Perdemos os arquivos do evento. E agora?",
  "1) Tela preta: arquivos perdidos 2) Ligação para o cliente contando o que aconteceu 3) Sobrou o áudio 4) Proposta: fotos animadas no ritmo da fala 5) Nomes de quem falava 6) Cliente aprova a solução criativa",
  "Os vídeos se perderam, sobrou o áudio. Contamos ao cliente e propusemos uma solução criativa: fotos animadas, o áudio do evento e os nomes no momento certo. Transparência primeiro, criatividade depois.","Comente se já perdeu um arquivo","cobertura mobile, storymaker"),
 (6,"Seg","Reels","Oferta","Todos","Seu bar no Réveillon, contado em tempo real",
  "1) Fachada do bar ao entardecer 2) Equipe preparando drinks 3) Casa enchendo 4) Contagem e brinde com os clientes 5) Texto: ofereça este serviço",
  "Bares, restaurantes e hotéis querem mostrar a casa cheia na virada. O roteiro de fim de ano traz a sequência pronta para você oferecer esse serviço. Imagens ilustrativas.","Roteiro de fim de ano no link","cobertura de eventos, conteúdo em tempo real"),
 (6,"Qua","Carrossel","Dinheiro","Todos","Storymaker é profissão?",
  "Capa; o que faz; quem contrata; formatos de entrega; como cobrar; como começar",
  "Sim. Com método, contrato e postura, vira serviço profissional.","Leia a série no blog","storymaker profissão"),
 (6,"Sex","Reels","Bastidores","Todos","Frases no telão em 5 minutos (e sem pendrive)",
  "1) Praça de alimentação lotada 2) Pedido do cliente: avisos no painel de LED 3) Edição no celular, cronômetro 4) Sem pendrive 5) Uma empresa do evento leva o pendrive 6) Frase no telão",
  "O cliente precisava organizar a praça de alimentação. Cinco minutos de edição, um pendrive emprestado e o recado estava no telão.","Siga para mais bastidores reais","conteúdo em tempo real, cobertura de eventos"),
 (7,"Seg","Reels","Oferta","Todos","Quer oferecer um novo serviço em 2027?",
  "Pessoa abrindo agenda 2027; e-book; planilha; contrato; texto: comece com método",
  "Comece 2027 com método: planejamento, captação, preço e contrato. Sem promessa mágica, com prática.","Link na bio","storymaker curso"),
 (7,"Qua","Reels","Ensino","Todos","Te chamaram hoje para trabalhar amanhã? Respira.",
  "1) Notificação do WhatsApp: evento amanhã 2) Briefing rápido pelo WhatsApp 3) Programação na tela 4) Celular e power bank carregando 5) Checklist sendo marcado 6) Cobertura no dia seguinte",
  "Você não precisa saber tudo sobre o evento. Precisa fazer as perguntas certas. Cliente de última hora não precisa significar trabalho improvisado.","O evento é amanhã. Você está preparado para dizer sim? Baixe grátis o checklist (link na bio)","cobertura de evento de última hora, storymaker como começar"),
 (7,"Sex","Reels","Prova","Todos","O que a equipe aprendeu na DocMe",
  "Depoimento curto de um integrante da equipe (João, Gu, Henrique ou Eric)",
  "Quem aprendeu storymaker na prática conta como foi.","Conheça o método","storymaker"),
 (8,"Seg","Reels","Dinheiro","Todos","De R$150 para R$500: o que mudou",
  "Eric conta: celular, forma de editar, estudo, mais conteúdo no mesmo tempo",
  "Experiência individual, não promessa. Mostra o que prática e método mudam.","Planilha de custos no link","storymaker valor, quanto cobrar storymaker"),
 (8,"Qua","Carrossel","Ensino","Videomaker","Aftermovie: o que é e quando usar",
  "Storymaker = no dia, vertical, rápido; aftermovie = depois, narrativa completa; quando vender os dois juntos",
  "Dois formatos, dois tempos. Juntos, valem mais para o cliente.","Leia o artigo 11","aftermovie o que é, aftermovie evento"),
 (8,"Sex","Reels","Bastidores","Todos","O que tem na nossa mochila (e por que sempre em dobro)",
  "Unboxing: 5 celulares, 2 power banks, estabilizador, microfone, iluminação, rádio comunicador, gravador extra para a caixa de som",
  "Se é uma câmera, levamos duas. Áudio da mesa? Um gravador extra na caixa de som. Redundância é o que garante a entrega.","Checklist no link","kit filmagem com celular, filmagem com celular"),
 (9,"Seg","Reels","Ensino","Fotógrafo","Fotógrafo: seu olhar já está pronto. Falta o vertical.",
  "Fotógrafo com câmera; troca para o celular; mesma cena em foto e em story",
  "Enquadramento, luz e momento você já domina. O passo novo é a sequência.","Artigo 03 no blog","storymaker mobile, fotógrafo"),
 (9,"Qua","Carrossel","Ensino","Fotógrafo","5 cenas para transformar fotos em stories",
  "Ambiente, preparação, ação, detalhe, reação; exemplo de cada",
  "Pense em sequência, não em foto solta.","Salve","storymaker para eventos"),
 (9,"Sex","Reels","Oferta","Fotógrafo","Kit para fotógrafo começar no storymaker",
  "Checklist + e-book + contrato na tela do celular",
  "Para quem recebe pedido de stories no evento e quer cobrar do jeito certo.","Link na bio","storymaker curso"),
 (10,"Seg","Reels","Ensino","Videomaker","Videomaker: entregue no mesmo dia",
  "Câmera grande x celular; pedido do cliente por stories na hora; entrega no fim do evento",
  "Cliente quer ver o evento enquanto ele acontece. Você já tem a técnica, falta o ritmo.","Artigo 11 no blog","storymaker evento corporativo"),
 (10,"Qua","Carrossel","Dinheiro","Videomaker","Como vender storymaker junto com o vídeo",
  "Proposta com 3 opções; storymaker como adicional; prazo; contrato",
  "Aumente o valor da proposta sem trabalhar o dobro: planeje as duas entregas juntas.","Modelo de contrato no link","storymaker valor"),
 (10,"Sex","Reels","Ensino","Iniciante","Seu primeiro portfólio em um fim de semana",
  "Salão de beleza do bairro: 10 vídeos e 50 fotos em um dia de colaboração",
  "Uma parceria com começo e fim definidos ensina e vira portfólio.","Artigo 02 no blog","conteúdo para salão de beleza, ideias de conteudo para salao de beleza"),
 (11,"Seg","Reels","Oferta","Todos","Novos materiais: checklists de cobertura e pós-produção",
  "Checklist impresso sendo marcado durante e depois do evento",
  "Dois novos checklists para usar no próximo evento.","Link na bio","storymaker"),
 (11,"Qua","Carrossel","Ensino","Todos","Storymaker de 15 anos: o que não pode faltar",
  "Entrada, valsa, família, decoração, festa; 5 stories de vídeo + 5 de foto",
  "Uma festa de 15 anos pede um roteiro próprio. Aqui está o básico.","Salve","storymaker 15 anos"),
 (11,"Sex","Reels","Ensino","Todos","Storymaker de casamento: o roteiro em 1 minuto",
  "Making of, cerimônia, entrada dos noivos, festa, detalhes, encerramento",
  "O que gravar e em que ordem, num casamento.","Salve para o próximo casamento","storymaker casamento"),
 (12,"Seg","Reels","Bastidores","Todos","Um evento de 13 mil pessoas: como dividimos a equipe",
  "Mapa do evento; equipe por área; prioridades; personalidades",
  "Num evento infantil gigante, a divisão por prioridade é o que garante o conteúdo.","Siga","storymaker para eventos"),
 (12,"Qua","Carrossel","Dinheiro","Todos","Contrato de storymaker: 6 cláusulas que evitam dor de cabeça",
  "Escopo; hora extra; mudança de programação; publicação; prazo; cancelamento",
  "Modelo de referência, a validar com o seu advogado.","Modelo de contrato no link","contrato storymaker"),
 (12,"Sex","Reels","Oferta","Agências","Treinamento de storymaker para equipes de agência",
  "Equipe de agência em reunião; celular; método; texto: lista de interesse",
  "Agências e empresas: treine sua equipe com o método DocMe.","Mande DM para a lista de interesse","storymaker evento corporativo"),
 (13,"Seg","Reels","Dinheiro","Todos","\"Você dá conta?\" A pergunta que todo cliente faz",
  "1) Cliente pergunta 2) Resposta: por que não? 3) Celular mostrando vídeos de eventos que o cliente conhece 4) Estudar o cliente antes da reunião 5) Contrato fechado",
  "Nossos clientes chegam por indicação. Quando perguntam se damos conta, mostramos eventos que eles conhecem. Atendimento começa antes da reunião.","Planilha e contrato no link","como conseguir clientes videomaker, como conseguir os primeiros clientes na fotografia"),
 (13,"Qua","Carrossel","Prova","Todos","Antes e depois: stories do dia x aftermovie",
  "Mesmo evento nos dois formatos; o que cada um entrega",
  "No dia: 10 mil visualizações. Uma semana depois: 1.500. Dois vídeos com propostas diferentes.","Leia o artigo 11","aftermovie evento"),
 (13,"Sex","Reels","Oferta","Todos","Os materiais do método DocMe, num só lugar",
  "Todos os produtos na tela; pacote; link",
  "Do briefing ao contrato: tudo o que usamos na prática.","Link na bio","storymaker curso"),
]


import re as _re
RISCO = _re.compile(r"R\$|renda|ganh|fatur|lucro|dinheiro|cachê", _re.I)


def anuncio(g, leg, pil):
    """Política de anúncios da Meta: nada de promessa de ganho nem valores de renda."""
    if RISCO.search(g + " " + leg):
        return "Só orgânico (valores ou renda)"
    if pil == "Oferta":
        return "Sim, anúncio de oferta"
    return "Sim" if pil in ("Ensino", "Bastidores", "Erros", "Prova") else "Opcional"


def data(sem, dia):
    return INICIO + dt.timedelta(weeks=sem - 1, days=DIAS[dia])


def planilha():
    wb = Workbook(); ws = wb.active; ws.title = "Calendário"
    L, T, CR = "E7570C", "2B2A30", "FFF4EC"
    ws["A1"] = "Plano de conteúdo — 3 meses, 3 posts por semana (Instagram + TikTok)"; ws["A1"].font = Font(bold=True, size=14, color=L)
    ws["A2"] = "Eventos citados com nome genérico. Marque o cliente só com autorização. Datas são sugestão; ajuste à agenda."; ws["A2"].font = Font(italic=True, color="5D5C63")
    cab = ["Semana", "Fase", "Data", "Dia", "Formato", "Pilar", "Público", "Gancho (texto na tela)", "Roteiro / cenas", "Legenda (base)", "Chamada", "Palavras-chave", "Material DocMe necessário", "Pode virar anúncio?", "Status"]
    for c, v in enumerate(cab, 1):
        x = ws.cell(row=4, column=c, value=v); x.font = Font(bold=True, color="FFFFFF"); x.fill = PatternFill("solid", fgColor=T); x.alignment = Alignment(wrap_text=True, vertical="center")
    dv = DataValidation(type="list", formula1='"A fazer,Gravado,Editado,Publicado"', allow_blank=True); ws.add_data_validation(dv)
    thin = Side(style="thin", color="D9D8DD")
    for i, (s, d, fmt, pil, pub, g, rot, leg, cta, kw) in enumerate(P, 5):
        mat = "Vídeos e fotos do Drive" if pil in ("Bastidores", "Prova", "Erros") else ("Prints sem identificação" if "clientes" in g else "Gravação nova (mãos/tela)")
        vals = [s, FASES[s], data(s, d).strftime("%d/%m/%Y"), d, fmt, pil, pub, g, rot, leg, cta, kw, mat, anuncio(g, leg, pil), "A fazer"]
        for c, v in enumerate(vals, 1):
            x = ws.cell(row=i, column=c, value=v); x.alignment = Alignment(wrap_text=True, vertical="top"); x.border = Border(bottom=thin)
            x.font = Font(color=T, bold=(c == 8))
        ws.cell(row=i, column=15).fill = PatternFill("solid", fgColor=CR); dv.add(f"O{i}")
    for col, w in zip("ABCDEFGHIJKLMNO", (8, 18, 11, 5, 10, 13, 11, 34, 48, 48, 26, 28, 24, 20, 11)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "H5"; ws.row_dimensions[4].height = 30
    r = wb.create_sheet("Resumo")
    r["A1"] = "Distribuição"; r["A1"].font = Font(bold=True, size=14, color=L)
    from collections import Counter
    for col, titulo, idx in ((1, "Pilar", 3), (4, "Público", 4), (7, "Formato", 2)):
        r.cell(row=3, column=col, value=titulo).font = Font(bold=True, color=T)
        for j, (k, v) in enumerate(Counter(p[idx] for p in P).most_common(), 4):
            r.cell(row=j, column=col, value=k); r.cell(row=j, column=col + 1, value=v)
    out = RAIZ / "docs" / "plano-de-conteudo-3-meses.xlsx"; wb.save(out); return out


def pdf():
    css = (RAIZ / "produtos" / "produto.css").read_text(encoding="utf-8")
    blocos = []
    for s in range(1, 14):
        itens = "".join(
            f"<tr><td class='d'>{data(s, d).strftime('%d/%m')}<br><small>{d}</small></td><td><span class='tag'>{fmt}</span><br><small>{pil} · {pub}</small></td>"
            f"<td><b>{g}</b><br><small>{rot}</small></td><td><small>{leg}<br><i>{cta}</i></small><br><span class='kw'>{kw}</span><br><span class='ad'>Anúncio: {anuncio(g, leg, pil)}</span></td></tr>"
            for (ss, d, fmt, pil, pub, g, rot, leg, cta, kw) in P if ss == s)
        blocos.append(f"<h2>Semana {s} · {FASES[s]}</h2><table><tr><th>Data</th><th>Formato</th><th>Gancho e roteiro</th><th>Legenda, chamada e palavras-chave</th></tr>{itens}</table>")
    html = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@600;700;800&display=swap" rel="stylesheet">
<style>{css} table{{font-size:8pt}} td.d{{font:700 9pt Sora,sans-serif;color:#c2410c;width:13mm}} .tag{{background:#2b2a30;color:#fff;border-radius:999px;padding:1px 6px;font-size:7.5pt;font-weight:700}}
small{{color:#5d5c63}} .kw{{color:#9a3412;font-size:7.5pt;font-weight:600}} .ad{{color:#5d5c63;font-size:7pt;font-style:italic}} td:nth-child(2){{width:24mm}}</style></head>
<body class="fmt-ficha"><header class="ficha__topo"><div><p class="ficha__selo">Plano de conteúdo · Instagram e TikTok</p><h1>3 meses, 3 posts por semana</h1></div>
<p class="ficha__assina">{len(P)} posts · início em {INICIO.strftime('%d/%m/%Y')}</p></header><main>
<p><b>Ritmo:</b> segunda, Reels de ensino · quarta, carrossel · sexta, bastidores, prova ou oferta. O mesmo Reels vai para o TikTok; o carrossel vai no modo foto.</p>
<p><b>Regra:</b> eventos com nome genérico; marque o cliente só com autorização. Rosto: equipe DocMe, mãos e bastidores.</p>
{''.join(blocos)}</main></body></html>"""
    h = RAIZ / "docs" / "_plano.html"; h.write_text(html, encoding="utf-8"); out = RAIZ / "docs" / "plano-de-conteudo-3-meses.pdf"
    node = "const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://'+process.argv[1],{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);await p.pdf({path:process.argv[2],preferCSSPageSize:true,printBackground:true});await b.close();})();"
    subprocess.run(["node", "-e", node, str(h), str(out)], check=True); h.unlink(); return out


if __name__ == "__main__":
    assert len(P) == 39, len(P)
    print(planilha()); print(pdf())
