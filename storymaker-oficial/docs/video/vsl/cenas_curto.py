"""VSL curta (mesmo roteiro, condensado) — fonte única. Gera cenas.json para narrar_gabriel.py e v2.py."""
import json, re
CENAS = [
 ("1. As dificuldades", "Você conhece essa cena?", "[warmly] Você chega ao evento... e tudo acontece ao mesmo tempo."),
 ("1. As dificuldades", "Por onde começar?", "[curious] Por onde começar? O que gravar primeiro?"),
 ("1. As dificuldades", "Imagens bonitas…", "Você faz imagens bonitas. Mas elas não viram uma história."),
 ("1. As dificuldades", "O que o cliente espera?", "O que o cliente espera, de verdade? Quem precisa aparecer?"),
 ("1. As dificuldades", "A edição que não termina", "Na edição, você se perde. E a entrega não sai."),
 ("1. As dificuldades", "O momento que não volta", "[pause] E bate aquele medo: perder a fala, a entrada, o parabéns."),
 ("1. As dificuldades", "Falta de método", "[warmly] Nada disso é falta de talento. É falta de método. E método se aprende."),
 ("2. O que muda quando você planeja", "Começa antes do evento", "Tudo começa antes de ligar a câmera: uma boa conversa com o cliente."),
 ("2. O que muda quando você planeja", "Aberto, médio, detalhe", "No evento, você alterna plano aberto, médio e detalhe. É assim que a sequência conta a história."),
 ("3. A ferramenta ajuda, a escolha é sua", "A edição não escolhe por você", "O aplicativo de edição ajuda. Mas depende das cenas que você escolheu."),
 ("4. A trilha de materiais", "Materiais práticos", "[curious] Por isso, o Storymaker Oficial organizou o método em materiais práticos. Para storymakers, social medias e socialmakers."),
 ("4. A trilha de materiais", "Do checklist ao e-book", "Checklists, modelo de briefing, planilha de custos, contrato e o e-book Do briefing à história. E o Kit Lançamento reúne quatro deles."),
 ("5. Comece pequeno e pratique", "Comece pequeno", "[warmly] Comece pequeno: um negócio do bairro, uma comemoração. E pratique."),
 ("5. Comece pequeno e pratique", "Do simples ao grande", "Nesta página, você vê coberturas reais, do simples ao grande."),
 ("6. Convite", "Escolha por onde começar", "[warmly] Escolha o material da etapa em que você está. A compra e a entrega são pela Kiwify. [pause] Storymaker Oficial."),
]
LIMPA = lambda t: re.sub(r"\[[a-z ]+\]\s*", "", t).replace("...", ",").strip()
out = []
for i, (b, t, f) in enumerate(CENAS, 1):
    out.append({"n": i, "bloco": b, "titulo": t, "fala": f, "clip": None if i == len(CENAS) else -1,
                "legendas": [{"texto": s} for s in re.split(r"(?<=[.?!:])\s+", LIMPA(f)) if s]})
json.dump(out, open("cenas.json", "w"), ensure_ascii=False, indent=1)
print(len(out), "cenas,", sum(len(LIMPA(c['fala']).split()) for c in out), "palavras")
