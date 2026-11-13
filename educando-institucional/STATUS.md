# Educando pelo Esporte — "O que pode existir depois daqui?"
## Status da curadoria e montagem (atualizado em 13/11/2026)

### Fonte do material
Pasta do Drive **INSTITUCIONAL EDUCANDO PELO ESPORTE - DOC.ME** (compartilhada por link), com 441 clipes Sony FX3 (4K HEVC 59,94p, ~89,7 GB):

| Pasta | Dia | Clipes | Faixa | Analisados |
|---|---|---|---|---|
| 27.08 | Dia 1 | 86 | C0599–C0684 | 86 (100%) |
| 08.09 | Dia 2 | 164 | C1669–C1832 | 134 (C1802–C1811 e C1813–C1832 bloqueados) |
| 09.09 | Dia 3 | 191 | C1940–C2130 | 0 (bloqueado) |

**Impedimento atual:** depois de ~55 GB baixados, o Google Drive passou a responder *"Quota exceeded"* para downloads anônimos. Não contornei o limite. A análise continua quando a cota for liberada (em geral, em até 24 h).

Nenhum arquivo original foi modificado. Os clipes foram baixados temporariamente, analisados (quadros-chave + áudio) e apagados.

### O que existe no material analisado
**Dia 1 (27.08)**
- Chegada da personagem **Maíra** (menina de mochila) — C0605–C0614: muro com o logo, interfone, portão abrindo, pés com chuteira, caminhada ao lado do campo, abraço da educadora.
- Logo no vidro (C0599–C0600), refeitório e merendeira (C0601–C0604).
- Sala de instrumentos (C0618–C0626), roda com educador (C0617, C0627–C0633), aula de flauta (C0634–C0656).
- Treino de futebol infantil, inclusive chuteira sendo amarrada (C0657–C0675).
- Crianças dizendo "Meu sonho quando crescer é…" (C0676–C0682). **Não previsto no roteiro; não será usado sem autorização.**
- Aniversário (C0683–C0684).

**Dia 2 (08.09)**
- Tênis de mesa infantil (C1669–C1723, C1780–C1812).
- Mídias digitais: aula de animação em tablets e informática (C1724–C1779).

### Lacunas até agora (dependem do Dia 3 ou de material extra)
- Teatro (infantil e adolescente — obrigatório), flag, música adolescente, futebol adolescente.
- Competitivo Sub-09 / Sub-11 / Sub-15 / Sub-17 e flag competitivo.
- Violão 50+ e informática 50+.
- Entrevistas de Tiago, Cris e Ivan; depoimentos "Aqui foi a nossa segunda casa…", "Era meio rebelde, o Ivan me colocava nos eixos", "Você pode chegar onde você nem imagina".
- **Arquivo histórico desde 1997** (fotos antigas): não existe nas pastas do Drive.
- **Locução definitiva:** não existe. Há uma faixa-guia sintética (`locucao_guia/`), marcada como GUIA, com o texto do roteiro sem alterações.

### Trilha provisória
"Dreamer" — Kevin MacLeod (incompetech.com), licença Creative Commons BY 4.0. Exige crédito: *"Dreamer" Kevin MacLeod (incompetech.com) Licensed under Creative Commons: By Attribution 4.0 License*. Deve ser trocada pela trilha definitiva licenciada pela Doc.Me.

### Corte 1 — OFFLINE (13/11/2026)
`montagem/Educando_corte1_OFFLINE.mp4` (4:15, 1080p, H.264). É um **animatic de baixa resolução**: com o Drive bloqueado, foi montado a partir dos quadros-chave da análise (~1 quadro/s, ampliados), não dos originais 4K. Ele serve para aprovar estrutura, ordem, tempos e escolha de planos. **Não é a versão de entrega.**
- Segue os 10 blocos do roteiro, nas minutagens dele (B7 e B8 começam em 2:50 e 3:10, para não sobrepor os blocos anteriores).
- A locução é a guia sintética, sem alterações no texto. A trilha é provisória, com ducking sob a voz. O áudio está normalizado em −16 LUFS.
- Lacunas aparecem como tela preta com o texto amarelo **LACUNA · …**. Depoimentos e entrevistas que faltam aparecem como legenda **PENDENTE** na posição prevista.
- Planos reais do Instituto usados como substitutos (ex.: treino infantil no lugar do Sub-09/11/15/17) levam a marca **PROVISÓRIO**.
- Nenhuma imagem de banco foi usada.
- Os takes dirigidos da chegada da Maíra (C0605–C0614) estão sem som, porque têm voz da direção.

`montagem/corte1_premiere.xml`: sequência para o Premiere (Arquivo > Importar), 1920×1080, 29,97 fps. Os planos apontam para os **originais 4K** em `<pasta do projeto>/Dia 1|Dia 2/fx3 gabrielNNNN.MP4`, com escala de 50%. Lacunas viram *slugs*, e cada pendência tem um marcador na sequência. A locução-guia aponta para `projeto/claude_montagem/locucao_guia/` e a trilha para `projeto/claude_montagem/trilha/`. Se as mídias abrirem offline, use **Vincular mídia** para apontar para as pastas locais.

`montagem/RELATORIO.md`: tabela Bloco | Cena solicitada | Arquivo utilizado | Origem | Situação. São 49 cenas utilizadas, 8 provisórias e 34 pendentes.

### Arquivos desta pasta
- `curadoria/inventory.tsv` — inventário dos 441 clipes (dia, nome, id no Drive, tamanho).
- `curadoria/catalog_D1.tsv`, `catalog_D2.tsv` — catálogo plano a plano (tags, faixa etária, enquadramento, nota 1–5, melhor trecho, descrição).
- `curadoria/transcricoes.tsv` — transcrição automática das falas.
- `curadoria/pranchas/` — pranchas de miniaturas (8 clipes por imagem).
- `locucao_guia/` — locução-guia por frase.
- `scripts/` — pipeline de análise, render e geração do XML para o Premiere.
