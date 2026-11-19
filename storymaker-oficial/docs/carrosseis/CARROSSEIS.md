# Carrosséis Storymaker Oficial — Instagram (1080×1350, 4:5)

19/11/2026 · 3 carrosséis de 10 slides · textos aprovados pelo fundador · sem nomes de clientes, eventos ou profissionais.

| Pasta | Tema | Pode virar anúncio? |
|---|---|---|
| `c1-quem-contou-a-historia/` | A urgência de publicar enquanto o evento acontece | Sim |
| `c2-a-programacao-mudou/` | O imprevisto que muda a cobertura | Sim |
| `c3-o-valor-de-um-profissional/` | A evolução de uma pessoa da equipe (R$ 150 → R$ 500) | **Não. Só orgânico.** Cita valores de cachê (regra da política Meta). O slide 8 traz o aviso "Caso real · não é promessa". |

## Visual

- Mesmo estilo da VSL v3: fundos off-white `#ece8e3`, grafite `#1b1a1f` e laranja `#e7570c`; Inter regular + negrito; etiquetas em mono nos cantos ("Storymaker Oficial · 01 / 10"); seta "Arraste" na capa; quadradinho laranja no fim das frases dos slides tipográficos; círculo-guia discreto.
- Slides com foto alternados com slides só de texto, para dar ritmo ao arrastar.
- Slide 10 de cada carrossel: fundo laranja, chamada em branco, "Storymaker Oficial · Conheça os materiais · link na bio".

## Legendas sugeridas para o post

**C1:** O evento aconteceu. Mas quem contou a história? Enquanto o organizador cuida de tudo, o público já está publicando. Storymaker é quem pensa a cobertura para que a história certa chegue no tempo certo. Arraste para ver como isso começou. 👉 Materiais no link da bio.

**C2:** O briefing estava pronto. A programação mudou. O que fazer quando o plano muda no meio do evento? Arraste e veja como a equipe se reorganizou. 👉 Materiais no link da bio.

**C3:** Ele já sabia fazer imagens. O próximo passo foi aprender a contar uma história com elas. Um caso real de uma pessoa da equipe, não uma promessa: cada trabalho, cliente e cidade tem sua realidade. 👉 Materiais no link da bio.

Antes de publicar, pesquise as hashtags e palavras-chave do momento (regra do projeto) e registre em `docs/palavras-chave.md`.

## Imagens e licenças

Fotos = quadros extraídos de clipes do **Mixkit** (Mixkit Stock Video Free License, uso comercial permitido, sem atribuição obrigatória), conferidos em 18 e 19/11/2026. São imagens ilustrativas, não coberturas da DocMe; o slide 10 traz "Imagens ilustrativas de banco gratuito (Mixkit)".

Clipes usados: 51529, 5227, 41222, 4915, 1741, 5224, 4632, 34486, 4953, 44069, 43266, 34408, 1505, 18204, 5217, 5206, 51540, 50406 (páginas em `https://mixkit.co/free-stock-video/<nome>-<id>/`).

Os bancos de fotos (StockSnap, Pexels, Unsplash) não puderam ser baixados automaticamente daqui; por isso as fotos vieram do Mixkit.

## Como editar

Os textos e a escolha das fotos ficam em `carrosseis.js`. Para gerar de novo: `node carrosseis.js <pasta-de-saída>` (precisa das fotos em `fotos/`).
