"""Troca nomes de eventos por nomes genéricos nos materiais vendidos e publicados.
Regra do fundador: nenhum material (blog, e-books, guias) cita o evento pelo nome.
Uso: python3 produtos/nomes_genericos.py ebooks/*.md
"""
import re, sys

PARES = [
    # frases inteiras primeiro
    (r"Coberturas como CIDE 2026.*?13 mil pessoas", "Coberturas como congressos em São Paulo e no interior, uma confraternização de fim de ano, casamentos, um circuito gastronômico, eventos nacionais e um evento infantil com 13 mil pessoas"),
    (r"No \*\*Best-Seller\*\*, no Guarujá,", "Num **congresso de negócios** no litoral paulista,"),
    (r"No Dia das Crianças coberto pela DocMe no Engenho,", "No evento infantil coberto pela DocMe,"),
    (r"No \*\*Dia das Crianças\*\* no Engenho,", "No **evento infantil**,"),
    (r"o casamento da Carol Sampaio \(Para Sempre\)", "um casamento com mais de 30 atrações"),
    (r"\*\*Casamento da Carol Sampaio \(Para Sempre\):\*\*", "**Casamento com mais de 30 atrações:**"),
    (r"casamento Carol Sampaio \(mais de 30\)", "casamento com mais de 30 atrações"),
    (r"\*\*Dia das Crianças, Carol Sampaio, 15 anos:\*\*", "**Evento infantil, casamento com mais de 30 atrações e 15 anos:**"),
    (r"\*\*15 anos e Carol Sampaio:\*\*", "**15 anos e casamento com mais de 30 atrações:**"),
    (r"\*\*Casamento Carol Sampaio:\*\*", "**Casamento com mais de 30 atrações:**"),
    (r"\(Carol Sampaio\)", "(um casamento)"),
    (r"casamento da Carol Sampaio", "casamento com mais de 30 atrações"),
    (r"\*\*Expo ESG, Festa do Frango, Festa da Batata, Congresso ACIPI\*\*", "**Feira de sustentabilidade, festas tradicionais da cidade e congresso empresarial regional**"),
    (r"\*\*McDia Feliz, Pizza do Bem, Feijoada do Bem, Dia de Doar\*\*", "**Ações beneficentes**"),
    (r"\*\*Casamento da Aninha\*\*", "**Outro casamento**"),
    (r"\*\*Workshop Karla Corrente\*\*", "**Workshop de dois dias**"),
    (r"Karla Corrente", "workshop de dois dias"),
    # Best-Seller
    (r"o caso Best-Seller", "o caso do congresso de negócios"),
    (r"\(Caso Best-Seller\.\)", "(Caso do congresso de negócios.)"),
    (r"Case central Best-Seller", "Case central: congresso de negócios"),
    (r"\*\*Best-Seller \(Guarujá\):\*\*", "**Congresso de negócios:**"),
    (r"\*\*Best-Seller:\*\*", "**Congresso de negócios:**"),
    (r"\bNo Best-Seller\b", "No congresso de negócios"),
    (r"Best-Seller", "congresso de negócios"),
    # Celebra
    (r"\bNo Celebra 2026\b", "Na confraternização de fim de ano"),
    (r"do cliente do Celebra 2026", "do cliente da confraternização de fim de ano"),
    (r"do \*\*Celebra 2026\*\*", "da **confraternização de fim de ano**"),
    (r"\(ex\. Celebra 2026\)", "(ex.: confraternização de fim de ano)"),
    (r"\*\*Celebra 2026:\*\*", "**Confraternização de fim de ano:**"),
    (r"(?m)(^\d+\. \*\*[^*]+\*\* )Celebra 2026:", r"\1Confraternização de fim de ano:"),
    (r"Celebra 2026", "confraternização de fim de ano"),
    # Dia das Crianças
    (r"o caso Dia das Crianças", "o caso do evento infantil"),
    (r"\(Caso Dia das Crianças\.\)", "(Caso do evento infantil.)"),
    (r"Case Dia das Crianças", "Case do evento infantil"),
    (r"\*\*Dia das Crianças \(Engenho\):\*\*", "**Evento infantil:**"),
    (r"\*\*Dia das Crianças:\*\*", "**Evento infantil:**"),
    (r"\(Dia das Crianças\)", "(evento infantil)"),
    (r"como o Dia das Crianças", "como o evento infantil"),
    (r"(?m)(\*\* )Dia das Crianças:", r"\1Evento infantil:"),
    (r"Dia das Crianças", "evento infantil"),
    # CIDE / ACIPI / APEX
    (r"No \*\*CIDE 2026\*\*", "Num **congresso em São Paulo**"),
    (r"\*\*Igor \(CIDE 2026\):\*\*", "**Igor (congresso em São Paulo):**"),
    (r"\*\*CIDE 2026\*\*", "**Congresso em São Paulo**"),
    (r"do CIDE 2026", "do congresso em São Paulo"),
    (r"\*\*CIDE 2026 / Congresso ACIPI:\*\*", "**Congresso em São Paulo e congresso empresarial regional:**"),
    (r"CIDE 2026", "congresso em São Paulo"),
    (r"\*\*APEX Brasil e Congresso ACIPI:\*\*", "**Evento nacional e congresso empresarial regional:**"),
    (r"\*\*APEX Brasil / Congresso ACIPI:\*\*", "**Evento nacional e congresso empresarial regional:**"),
    (r"\*\*APEX\*\*", "**Evento nacional**"),
    (r"\*\*APEX Brasil\*\*", "**um evento nacional**"),
    (r"APEX Brasil", "evento nacional"),
    (r"\*\*Congresso ACIPI\*\*", "**um congresso empresarial regional**"),
    (r"Congresso ACIPI", "congresso empresarial regional"),
    # Comida na Rua e outros
    (r"\*\*Exemplo real: Comida na Rua\.\*\*", "**Exemplo real: circuito gastronômico.**"),
    (r"do Comida na Rua", "do circuito gastronômico"),
    (r"\*\*Comida na Rua\*\*", "**Circuito gastronômico**"),
    (r"\*\*Comida na Rua:\*\*", "**Circuito gastronômico:**"),
    (r"\*\*Comida na Rua e casamento", "**Circuito gastronômico e casamento"),
    (r"Comida na Rua", "circuito gastronômico"),
    (r"\*\*Pira[Bb](?:eer|ir) 2024:\*\*", "**Festival de cerveja regional (2024):**"),
    (r"Pira[Bb](?:eer|ir) 2024", "festival de cerveja regional de 2024"),
    (r"\s*\(Engenho\)", ""), (r" no Engenho", ""), (r" no Guarujá", " no litoral paulista"),
    # cases incluídos com os links do Instagram
    (r"Festa da Imprensa( 2026)?", "festa de entidade de classe"),
    (r"PedalaPira( 2026)?", "passeio ciclístico"),
    (r"Workshop Exposição de Inovação e Sustentabilidade na Construção Civil", "workshop de construção civil"),
    (r"(Inauguração do )?CT PiraOlímpica( 2025)?", "inauguração de centro esportivo"),
    (r"[Pp]alestra( da jornalista)? Lilian Geraldini", "palestra com jornalista"),
    (r"Corrida ESG( — Chelso Sports)?", "corrida de rua"),
    (r"Jornada Caipira", "festa caipira"),
    (r"[Cc]asamento Carol e Daniel", "casamento com mais de 30 atrações"),
]
PROIBIDOS = r"Best-Seller|Bestseller|Celebra|Comida na Rua|\bCIDE?\b|APEX|ACIPI|Carol Sampaio|Para Sempre|Engenho|Guarujá|Karla|Expo ESG|Festa d[oa]|Pirabir|PiraBeer|Pirabeer|McDia|Ronald|Pizza do Bem|Feijoada|Dia de Doar|Aninha|SIMESPI|Unimed|Dia das Crianças"

if __name__ == "__main__":
    for f in sys.argv[1:]:
        s = open(f, encoding="utf-8").read()
        for a, b in PARES:
            s = re.sub(a, b, s)
        open(f, "w", encoding="utf-8").write(s)
        restos = sorted(set(re.findall(PROIBIDOS, s)))
        print(f, "| restantes:", restos or "nenhum")
