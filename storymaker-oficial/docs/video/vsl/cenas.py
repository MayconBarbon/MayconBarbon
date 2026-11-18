"""Fonte única do VSL: gera cenas.json (montagem), legendas .srt e o roteiro em Markdown."""
import json, re, sys

# (bloco, clipe Mixkit, início no clipe (s), título na tela, narração com marcações de tom, plano, termos de busca)
CENAS = [
 ("1. As dificuldades", 4632, 1.0, "Você conhece essa cena?", "[warmly] Você chega ao evento. Tem gente chegando, música começando, alguém testando o microfone.", "Detalhe", "microfone em salão de festa; party hall microphone"),
 ("1. As dificuldades", 5227, 1.0, "Tudo ao mesmo tempo", "E tudo acontece ao mesmo tempo. Por onde começar? O que gravar primeiro?", "Aberto (de cima)", "festa vista de cima; gala party from above"),
 ("1. As dificuldades", 4915, 1.0, "O celular na mão", "O celular está na mão. A vontade de fazer bonito também. Mas a cabeça fica cheia de dúvidas.", "Detalhe (mãos)", "mãos no celular; hands typing on phone"),
 ("1. As dificuldades", 5224, 0.5, "Imagens bonitas…", "Você faz imagens bonitas: a mesa, a decoração, os detalhes.", "Médio / detalhe", "mesa decorada de casamento; decorated wedding table"),
 ("1. As dificuldades", 22738, 0.5, "…mas cadê a história?", "Só que, no fim do dia, elas não viram uma história. Ficam soltas na galeria.", "Fechado (vertical)", "brinde de taças; toast glasses vertical"),
 ("1. As dificuldades", 4809, 3.0, "O que o cliente espera?", "E tem o cliente. O que ele espera, de verdade? Quem precisa aparecer? Quem aprova antes de publicar?", "Médio", "reunião de trabalho; business meeting"),
 ("1. As dificuldades", 44071, 2.0, "A edição que não termina", "Na hora de editar, você se perde. O evento acabou, e a entrega ainda não saiu.", "Médio", "editando vídeo no computador; editing video"),
 ("1. As dificuldades", 4663, 2.0, "O momento que não volta", "[pause] E existe aquele medo: perder a fala, a entrada, o parabéns. Momentos que não se repetem.", "Médio", "apagando velas de aniversário; blowing birthday candles"),
 ("2. O que muda quando você planeja", 4953, 0.5, "Começa antes do evento", "[warmly] A boa notícia: quase tudo isso se resolve antes de ligar a câmera.", "Médio (vertical)", "pessoa escrevendo no caderno; writing notepad vertical"),
 ("2. O que muda quando você planeja", 1741, 3.0, "Briefing", "Começa com uma conversa com o cliente. Objetivo, público, programação, as pessoas mais importantes e o que não pode faltar.", "Detalhe", "anotações em café; writing notebook coffee shop"),
 ("2. O que muda quando você planeja", 5217, 0.5, "Plano aberto", "No evento, você passa a ler o espaço. Um plano aberto mostra onde a história acontece.", "Aberto", "cerimônia de casamento; wedding ceremony"),
 ("2. O que muda quando você planeja", 5206, 1.0, "Plano médio", "O plano médio mostra quem está ali e o que está fazendo.", "Médio", "noiva e noivo; bride hand on groom shoulder"),
 ("2. O que muda quando você planeja", 18204, 0.5, "Detalhe", "E o detalhe dá emoção e ritmo. Aberto, médio, fechado: é assim que uma sequência começa a contar.", "Fechado", "buquê em close; bridal bouquet close-up"),
 ("2. O que muda quando você planeja", 5117, 0.5, "Uma ordem que conta", "Com uma ordem simples: o lugar, as pessoas, as atrações, o momento principal e o encerramento.", "Médio", "bolo no centro da mesa; cake party table"),
 ("3. A ferramenta ajuda, a escolha é sua", 50406, 0.5, "O celular grava bem", "O celular grava muito bem. E os aplicativos de edição ajudam bastante.", "Médio (celular em cena)", "celular gravando pessoa; smartphone recording"),
 ("3. A ferramenta ajuda, a escolha é sua", 44074, 2.0, "A edição não escolhe por você", "Mas a edição não escolhe por você. Ela depende das cenas que você captou e da ordem que você pensou.", "Detalhe", "close de edição de vídeo; close shot editing video"),
 ("3. A ferramenta ajuda, a escolha é sua", 50410, 0.0, "Planejar, captar, editar", "Quem planeja, capta melhor. E quem capta melhor, edita mais rápido.", "Detalhe (celular)", "celular com ring light gravando; smartphone light ring"),
 ("4. A trilha de materiais", 4919, 1.0, "Materiais práticos", "[curious] Foi para isso que a DocMe Comunicação organizou o método em materiais práticos, feitos a partir de coberturas reais.", "Médio", "pequeno negócio e redes sociais; social media serving coffee"),
 ("4. A trilha de materiais", 5106, 0.5, "Checklists", "Os checklists acompanham você antes, durante e depois do evento. E um deles é só sobre áudio, para não perder nenhuma fala.", "Detalhe (celular)", "fotografando mesa com celular; taking picture birthday table smartphone"),
 ("4. A trilha de materiais", 3574, 0.5, "Modelo de briefing", "O modelo de briefing conduz a conversa com o cliente, pergunta por pergunta.", "Detalhe", "servindo café; serving coffee coffee shop"),
 ("4. A trilha de materiais", 34408, 0.5, "Orçamento e contrato", "A planilha de custos e horas ajuda a colocar reunião, deslocamento, cobertura e edição no orçamento. E o modelo de contrato deixa tudo combinado por escrito.", "Médio (vertical)", "fotógrafo montando câmera; photographer setting up camera vertical"),
 ("4. A trilha de materiais", 1505, 0.5, "E-book Do briefing à história", "O e-book Do briefing à história explica o planejamento com calma, com exemplos e um exercício prático.", "Detalhe", "fotógrafo revisando fotos; photographer reviewing shots"),
 ("4. A trilha de materiais", 44069, 2.0, "Kit Lançamento", "E o Kit Lançamento reúne quatro desses materiais por um valor menor do que a soma deles.", "Médio", "gravando com câmera em set; recording camera set"),
 ("5. Comece pequeno e pratique", 50053, 0.0, "Comece pequeno", "[warmly] Você não precisa começar por um grande evento. Um negócio do bairro, uma comemoração, um evento perto de você.", "Detalhe", "confeiteira decorando bolo; pastry chef decorating cake"),
 ("5. Comece pequeno e pratique", 46874, 0.5, "Pratique", "Combine antes o que vai ser gravado e peça as autorizações. Depois: observe, planeje, capte, selecione, edite e revise.", "Médio", "amigos dançando em festa; friends dancing party"),
 ("5. Comece pequeno e pratique", 4151, 1.0, "A prática faz o resto", "Os materiais mostram o caminho. O resultado vem da sua prática, evento após evento.", "Aberto", "fogos no céu; fireworks sky"),
 ("6. Convite", None, 0, "Escolha por onde começar", "[warmly] Escolha o material da etapa em que você está. Os links estão logo abaixo deste vídeo. Método desenvolvido pela DocMe Comunicação.", "Cartão da marca", "—"),
]

LIMPA = lambda t: re.sub(r"\[[a-z ]+\]\s*", "", t).strip()

def pedacos(texto):
    """Divide a fala em legendas curtas (no máximo ~11 palavras), respeitando frases."""
    frases = re.split(r"(?<=[.?!:])\s+", LIMPA(texto))
    out = []
    for f in frases:
        w = f.split()
        while len(w) > 11:
            corte = 8 if len(w) > 14 else len(w) // 2
            out.append(" ".join(w[:corte])); w = w[corte:]
        if w: out.append(" ".join(w))
    return out

def dur(leg):  # leitura confortável de legenda + fala pausada (~2,3 palavras/s)
    return round(max(2.4, len(leg.split()) / 2.3 + 0.6), 2)

def main():
    cenas, t = [], 0.0
    for i, (bloco, clip, ss, titulo, fala, plano, busca) in enumerate(CENAS, 1):
        legs = [{"texto": l, "dur": dur(l)} for l in pedacos(fala)]
        if clip is None: legs[-1]["dur"] += 2.0
        d = round(sum(l["dur"] for l in legs), 2)
        cenas.append({"n": i, "bloco": bloco, "clip": clip, "ss": ss, "titulo": titulo, "fala": fala, "plano": plano, "busca": busca, "legendas": legs, "inicio": round(t, 2), "dur": d})
        t += d
    json.dump(cenas, open("cenas.json", "w"), ensure_ascii=False, indent=1)
    # SRT
    def ts(x):
        h, r = divmod(x, 3600); m, s = divmod(r, 60)
        return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}"
    srt, k, t = [], 1, 0.0
    for c in cenas:
        for l in c["legendas"]:
            srt.append(f"{k}\n{ts(t)} --> {ts(t + l['dur'] - 0.05)}\n{l['texto']}\n"); k += 1; t += l["dur"]
    open("vsl.srt", "w").write("\n".join(srt))
    print(f"{len(cenas)} cenas, {sum(len(c['legendas']) for c in cenas)} legendas, duração {t:.1f}s ({int(t//60)}min{int(t%60):02d}s)")

if __name__ == "__main__":
    main()
