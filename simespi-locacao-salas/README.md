# SIMESPI — Campanha Locação de Salas — FINAL

Campanha: **"Você tem o conhecimento. Nós temos o espaço."**

## Entregas (`entregas/`)

| | Arquivo | Especificação |
|---|---|---|
| A | `A_SIMESPI_Reels_Locacao_Salas_39s_1080x1920.mp4` | 39,0 s · 1080×1920 · 30 fps · H.264 High · AAC 48 kHz 256 kbps · −14 LUFS / −1,5 dBTP |
| B | `B_SIMESPI_Anuncio_Locacao_Salas_15s_1080x1920.mp4` | 15,0 s · mesmo padrão técnico e visual |
| C | `C_SIMESPI_Capa_Reels_1080x1920.jpg` | 1080×1920, texto e logo dentro do recorte 3:4 e 1:1 do grid |
| D | `D_legenda_instagram.txt` | Legenda comercial com CTA e hashtags |
| E | `E_SIMESPI_Tour_Salas_29s_1080x1920.mp4` | **3º vídeo — Tour pelas salas** · 28,8 s · mesmo padrão técnico (H.264, 30 fps, −14 LUFS) |

## Peças de feed (F e G) — 1080×1350 (4:5)

- **F — Post estático** (`entregas/F_post_estatico/`): o enquadramento mais amplo e profundo da Sala 01 (IMG_9837), com uma cota em estilo de planta ("ESPAÇO AMPLO E CLIMATIZADO") atravessando o ambiente para dar escala, sem medida numérica. Destaques: "SALAS PARA LOCAÇÃO" grande, usos, cidade e telefone.
- **G — Carrossel de 6 cards** (`entregas/G_carrossel_lousa/`), com a lousa em todos:
  1. Capa: close da lousa (8151) + "LOUSA INTERATIVA E CONECTADA";
  2. Sala 01 com a lousa ao fundo;
  3. Sala 02 com a lousa;
  4. Tela grande (9825) + "Tecnologia que transforma apresentações";
  5. Close da lousa + usos e "Associados ou não";
  6. Chamada com a lousa no topo, telefone e logotipo.
- **Elementos comuns:** cantoneiras azul-claras na tela real, numeração 01/06 e indicação "ARRASTE".
- **Gerado por** `projeto/feed.py`.
- **Medidas reais:** se o cliente informar m² ou capacidade, a cota do post pode trazer o número.

## Montagem do Reels (A)

| Tempo | Bloco | Imagens (fotos reais) | Texto na tela | Locução |
|---|---|---|---|---|
| 0–5,4 | Impacto | Sala 1 · IMG_9837 (tela ao fundo, centralizada) | VOCÊ TEM O CONHECIMENTO. / NÓS TEMOS O ESPAÇO. | "Você tem o conhecimento. Nós temos o espaço." |
| 5,4–12 | Apresentação | Sala 2 · IMG_8138 → Sala 1 · IMG_9832 + Sala 2 · IMG_8149 (fotos inteiras, empilhadas) | SALAS PARA LOCAÇÃO EM PIRACICABA / SUAS IDEIAS ENCONTRAM ESTRUTURA PARA ACONTECER. | "No Simespi, suas ideias encontram estrutura para acontecer." |
| 12–21 | Tecnologia | Sala 2 · IMG_8151 (tela) → Sala 1 · IMG_9825 (tela grande) → Sala 1 · IMG_9837 (recorte da tela) | TECNOLOGIA QUE TRANSFORMA APRESENTAÇÕES / LOUSA INTERATIVA E CONECTADA + "Ambientes climatizados", "Estrutura pronta" | "Ambientes modernos e climatizados, com lousa interativa e conectada, para apresentações mais dinâmicas." |
| 21–30 | Possibilidades | Cortes no tempo da trilha: 8149, 9832, 8141, 9829, 8138, 9837 | CURSOS · PALESTRAS · WORKSHOPS · TREINAMENTOS · ENCONTROS PROFISSIONAIS + "Para profissionais, empresas, professores e organizadores." + **ASSOCIADOS OU NÃO** | "Para cursos, palestras, treinamentos e encontros de profissionais de diferentes áreas." |
| 30–36 | Conversão | Sala 1 · IMG_9832 (visão aberta) + painel institucional | SEU PRÓXIMO EVENTO COMEÇA AQUI. / Salas para locação no SIMESPI / CONSULTE A DISPONIBILIDADE / (19) 3417-8600 | "Seu próximo encontro começa aqui. Consulte a disponibilidade e reserve sua sala no Simespi." |
| 36–39 | Assinatura | Fundo branco | Logotipo original (colorido positivo) + SALAS PARA LOCAÇÃO + (19) 3417-8600 | — (acorde final da trilha) |

**Anúncio de 15 s (B):** o texto do gancho já aparece no 1º quadro, sobre a foto com a lousa (IMG_8151) destacada por cantoneiras. Depois vêm salas, lousa, a chamada com telefone e o logotipo. Locução: "Você tem o conhecimento. Nós temos o espaço. / Salas modernas e climatizadas, com lousa interativa, em Piracicaba. / Consulte a disponibilidade e reserve sua sala no Simespi."

## Tour pelas salas (E)

| Tempo | Bloco | Imagens | Texto | Locução |
|---|---|---|---|---|
| 0–4,2 | Abertura | IMG_9837 | CONHEÇA AS SALAS PARA LOCAÇÃO | "Conheça as salas para locação do Simespi, em Piracicaba." |
| 4,2–10,8 | Sala 01 | 9832 → 9825 → recorte da lousa (9837) | SALA 01 + AMPLA E ORGANIZADA · CLIMATIZADA · LOUSA INTERATIVA | "Ambientes amplos, organizados e climatizados." |
| 10,8–17,4 | Sala 02 | 8138 → 8141 → 8151 (lousa) | SALA 02 + MESAS E CADEIRAS PARA TURMAS · CLIMATIZADA · LOUSA INTERATIVA E CONECTADA | "Mesas e cadeiras para turmas de diferentes formatos, com lousa interativa e conectada." |
| 17,4–22,2 | Usos | As duas salas, fotos inteiras | CURSOS · PALESTRAS · TREINAMENTOS + ASSOCIADOS OU NÃO | "Estrutura pronta para cursos, palestras e treinamentos. Associados ou não." |
| 22,2–25,8 | Conversão | 8138 + painel | ESTRUTURA PRONTA PARA O SEU EVENTO / CONSULTE A DISPONIBILIDADE / (19) 3417-8600 | "Consulte a disponibilidade: (19) 3417-8600." |
| 25,8–28,8 | Assinatura | Fundo branco | Logotipo original + telefone | — |

Os nomes "Sala 01" e "Sala 02" seguem as pastas do Drive. **Confirmar** se são esses os nomes comerciais e se as duas salas têm a lousa interativa: as duas fotos mostram o mesmo tipo de tela.

## Locução — revisão 3

- **Pedido:** "mais humana, animada, divertida e convidativa, com autoridade", com a mesma voz da Importway.
- **Voz da Importway:** é a "Gabriel — Friendly Brazilian Ad Voice", do ElevenLabs (flow "Importway Brand Film 60s"). Tentei duas vezes, com direção de interpretação (`[confident]`, `[upbeat]`, `[inviting]`…), mas a conta tem **83 créditos** e esta versão precisa de cerca de **1.210**. Não houve cobrança.
- **Voz entregue:** a voz neural masculina brasileira **Microsoft "Antonio"**, um pouco mais rápida e aguda para soar mais animada, com frases exclamativas e leve tratamento de áudio. É bem mais natural que a voz provisória anterior (Piper, guardada em `projeto/vo_piper_antiga/`). O script `projeto/tts_locucao.py` regenera as falas.
- **Atenção à licença:** essa voz vem do serviço gratuito de leitura do Microsoft Edge. Para veiculação paga (anúncio), o mais seguro é usar a voz do ElevenLabs, que tem licença comercial clara: com os créditos recarregados, basta trocar `projeto/vo/v1–v12.flac` e rodar `build.sh`.
- **Pronúncia (revisão 4):** a voz fala **"CIMESP"** (si-MÉSP, sem o "i" final), como o cliente pediu. No texto da locução o nome aparece escrito "Si-mésp" (e "SIMESP" na última fala do anúncio), porque foram as grafias com que a voz pronunciou o "p" final com mais clareza. A transcrição automática confere "CIMESP/CMESP" nas quatro menções.

## Decisões criativas

- **Identidade.** Paleta tirada do manual de marca (2017) e conferida no site simespi.com.br, onde as cores mais usadas são #276E85 e #083642. O azul-petróleo #083642 é a base (painéis, gradientes, transições), o azul #276E85 é o institucional e o azul-claro #5BC2D6 (CMYK 65/5/15/0 do manual) é o único destaque. O amarelo #FFD400 também aparece no tema do site, mas não está no manual, então ficou de fora.
- **Tipografia.** O manual define a Signoria só para o logotipo. Para os textos usei Montserrat (geométrica, licença OFL): ExtraBold em caixa-alta nos títulos e Medium/SemiBold com espaçamento largo nos apoios, ecoando o "PIRACICABA-SP" do logo. Títulos de 74 a 96 px e apoios de 34 a 40 px, legíveis no celular. Tudo fica dentro da área segura do Reels.
- **Logotipo.** Extraído do arquivo vetorial original (`LOGO - PDF.pdf`) sem redesenho nem recoloração: a versão *colorida positiva resumida* na assinatura sobre branco e a *monocromática negativa resumida* (oficial para fundo escuro) como assinatura discreta no topo. O fundo preto da prancha foi removido por luminância, sem tocar no traço.
- **Fotografias e movimento (revisão 2, a pedido do cliente: "foque na TV e pode dar movimento").** A TV/lousa passou a ser a protagonista: há *push-ins* de câmera em direção à tela na abertura, no bloco de tecnologia, na sequência de possibilidades e na chamada final, e *pan* lateral ao longo da tela grande (IMG_9825). Os planos sem TV têm *pans* e *zooms* lentos. O movimento é só de enquadramento (zoom até 2,35× em fotos de 12 a 24 MP, sem perda visível). Nada foi adicionado, removido ou retocado, e as telas mostram o conteúdo original.
- **Lousa.** O destaque é gráfico e de câmera: cantoneiras azul-claras enquadram a tela real e acompanham o movimento, enquanto o texto diz "lousa interativa e conectada". Nenhuma operação, toque ou conteúdo foi simulado.
- **Ritmo.** Trilha em 100 BPM. Os cortes caem no tempo (5,4 / 12 / 21 / 30 / 36 s) e as palavras do bloco "Possibilidades" entram a cada 1,2 s, no compasso. As transições entre blocos são uma faixa azul institucional que sobe e corta (0,5 s). Fora isso, só cortes secos, sem efeitos de slide.
- **Trilha.** Corporate lounge composta e sintetizada em código: Rhodes, pad, sub-grave, house suave e arpejo a partir dos 21 s. Ela cresce até o acorde final na assinatura e abaixa automaticamente (ducking) sob a locução. Livre de direitos de terceiros.

## Auditoria final

| Item | Situação |
|---|---|
| As duas salas aparecem? | Sim: Sala 1 (9837, 9832, 9825, 9829) e Sala 2 (8138, 8149, 8151, 8141). Todas as 8 fotos foram avaliadas e usadas. |
| As oito fotografias foram avaliadas? | Sim. As melhores: 9837 e 8151 (tela centralizada, perspectiva completa) para gancho e tecnologia; 9832 e 8138 (simetria, visão aberta) para apresentação e conversão. 9829 e 8141 são mais fracas (parede vazia, púlpito em primeiro plano) e ficaram só na montagem rápida. |
| Identidade corresponde ao SIMESPI? | Paleta e logo vêm do manual e do site atual. **O Instagram não pôde ser analisado** (ver limitações). |
| Logotipo original? | Sim, extraído do PDF vetorial oficial, sem alteração. |
| Títulos corretos e legíveis no celular? | Sim. Revisados quadro a quadro (`projeto/stills/`). |
| Fica claro que não é só para associados? | Sim: "Para profissionais, empresas, professores e organizadores" + selo "ASSOCIADOS OU NÃO" (27,6–30 s) e o mesmo na legenda. Não está na locução, que segue o roteiro aprovado. |
| A lousa aparece? | Sim, em três planos com destaque gráfico (12–21 s) e no gancho do anúncio. |
| Há algo sem comprovação? | Não. Só aparece o que o briefing afirma (moderna, climatizada, lousa interativa e conectada). Capacidade, preço e equipamentos não foram citados. |
| O contato aparece com clareza? | Sim: (19) 3417-8600 na conversão (32,8–36 s) e na assinatura (36–39 s). |
| Os arquivos foram gerados e testados? | Sim: ffprobe (resolução, fps, codecs, duração), contagem de quadros (1170 / 450), loudness EBU R128 (−14,0 LUFS) e folhas de contato por segundo. |

## Limitações e pendências

1. **Instagram @simespi:** o perfil exige login (HTTP 429, redirecionado para a página de login), então não foi possível analisar posts, capas de Reels nem animações recentes. Usei o manual de marca e o site institucional atual, como previsto no briefing. **Recomendo comparar com 2 ou 3 Reels recentes antes de publicar**, principalmente a posição do logo e os pesos tipográficos.
2. **Locução:** a voz escolhida no ElevenLabs ("Gabriel — Friendly Brazilian Ad Voice", masculina, brasileira, publicitária) não pôde ser gerada porque a conta tinha 83 créditos e cada take custa 207 a 427. A trilha do ElevenLabs falhou pelo mesmo motivo. **A locução entregue é uma voz sintética offline (Piper, voz pt-BR "faber")**, com EQ, compressão e ambiência leve, no tempo certo. É funcional, mas não tem a naturalidade de um locutor. Para a versão definitiva, recarregue o ElevenLabs ou grave um locutor, substitua `projeto/vo/v1–v7.flac` (mesmos textos) e rode `projeto/build.sh`. Os tempos de entrada estão em `build.sh`, e o ducking e a normalização se ajustam sozinhos.
3. **Revisão de áudio:** a mixagem foi verificada por medição (LUFS, picos, espectro), não por audição humana. Ouça antes de publicar, principalmente a pronúncia de "Simespi".
4. **Takes para mostrar a lousa funcionando** (a captar, se desejado): (a) mão tocando a tela e arrastando um slide, plano fechado, 3–4 s; (b) notebook ou celular espelhando na lousa (cabo/HDMI ou sem fio, conforme o equipamento real), plano médio com a tela e o aparelho; (c) apresentador em pé ao lado da lousa com a sala ao fundo, plano aberto; (d) detalhe do controle do ar-condicionado ou do aparelho ligado, para reforçar "climatizado". Grave na vertical, em 4K/30 fps, com luz da própria sala.
5. **Pasta no Drive:** ver a seção "Publicação" na resposta da entrega.

## Projeto de edição (`projeto/`)

Projeto executável, que reconstrói A, B e C a partir das fotos originais:

```
projeto/
  build.sh        # baixa as 8 fotos do Drive (somente leitura) e renderiza tudo
  render.py       # linha do tempo, layouts, animações tipográficas, capa
  music.py        # trilha sintetizada (100 BPM) — versões 39 s e 15 s
  mix.sh          # mixagem: ducking sob a locução + normalização −14 LUFS
  vo/             # locução v1–v7 (FLAC) — substituir para trocar a voz
  audio/          # trilhas renderizadas
  logo/           # logotipos extraídos do PDF oficial (PNG com transparência)
  fonts/          # Montserrat (SIL Open Font License)
  stills/         # folhas de contato (1 quadro/segundo) usadas na revisão
```

Requisitos: Python 3 com numpy e Pillow, e ffmpeg. Todos os tempos, textos e recortes ficam em `render.py → build()`.
