# Vídeo Imóvel Studio 3D · Da planta ao Cinematic

Quatro demonstrações audiovisuais feitas com **uma única planta e uma única modelagem 3D**, uma para cada nível de serviço da página https://videoimovel.com.br/construtoras.

## 1. Análise do material

| Item | Situação |
|---|---|
| Plantas recebidas | 4 imagens (25/11/2026). A planta 1 tem marca-d'água de outra empresa e não foi usada. |
| Planta escolhida | **Planta 3**: 8,10 × 6,70 m, com 2 dormitórios, banheiro, circulação, cozinha, jantar e estar integrados. Ela já estava adaptada como **apartamento tipo**, a seu pedido ("como se fosse um apartamento que será construído por uma construtora"), e é a mesma do tour 3D da página. |
| Adaptação | A área lateral virou varanda (1,40 × 3,70 m), com guarda-corpo de vidro e porta de correr. A entrada passou a ser pelo hall do andar. Ambientes, cotas internas e aberturas seguem a planta redesenhada (`studio3d/tour/plans/apto.json`). |
| Memorial descritivo | **Não existe.** Acabamentos, cores, mobiliário e decoração são uma **proposta conceitual**, identificada como ilustrativa em todos os vídeos e imagens. |
| Pé-direito | **Não informado na planta.** Adotei 2,70 m, um padrão residencial. Precisa ser confirmado num projeto real. |
| Fachada | Não existe. O edifício do Cinematic é **conceitual** (12 pavimentos-tipo, 4 unidades por andar) e aparece com o aviso "Edifício conceitual · imagem ilustrativa". |
| Captação real com drone | **Não usada.** Não há material aéreo real deste projeto. Nenhuma imagem simula drone real. |

## 2. Como foi feito

- **Base única:** a modelagem 3D é gerada pelo mesmo arquivo de geometria nos quatro níveis: mesmas paredes, portas, janelas, proporções e posições.
- **Motor:** `studio3d/film/` usa three.js (WebGL). Cada quadro é desenhado de forma determinística e capturado a 24 fps.
- **Materiais:** texturas CC0 do Poly Haven (piso laminado, porcelanato, revestimentos, deck e tecidos) e iluminação baseada em HDRI.
- **Transformações:**
  - A planta vira volumetria: as paredes sobem a partir do desenho técnico.
  - Os acabamentos entram por uma varredura com linha dourada: primeiro os pisos, depois paredes e esquadrias.
  - O mobiliário e a decoração entram em sequência.
- **Trilha:** composição **original**, sintetizada em código (`studio3d/film/music.py`). Não usa amostras nem músicas de terceiros, então não depende de licença externa. Volume normalizado em −16 LUFS.
- **Identidade visual:** fundo escuro, detalhes dourados, tipografia Manrope e Inter, e a assinatura Vídeo Imóvel Studio 3D, como na página.

## 3. Entregas

| Pasta | Conteúdo |
|---|---|
| `01-essencial/` | Vídeo de 25 s: original e versão web, 1920×1080 e 1080×1920, H.264 + AAC; capa em WebP e PNG |
| `02-acabamentos/` | Vídeo de 30 s, mesmos formatos |
| `03-decorado/` | Vídeo de 40 s, mesmos formatos |
| `04-cinematic/` | Vídeo de 60 s, horizontal (com faixas cinema 2,39:1) e vertical |
| `comparativo/` | 5 imagens no mesmo enquadramento: planta, essencial, acabamentos, decorado e cinematic (PNG e WebP) |

O original sai com mais qualidade, para campanhas e reedições. A versão web é otimizada para o site.

Tour navegável do Nível 3: está na própria página (seção "Entre no apartamento antes de ele existir"), com a mesma planta, modos Planta, Estrutura, Decorado, Passeio e Edifício, minimapa e tour guiado.

## 4. Limitações e próximos passos

- **Visual:** é uma visualização arquitetônica em tempo real (WebGL), não uma renderização fotorrealista por *path tracing*. Para lançamentos reais, o fluxo recomendado é:
  1. modelar no SketchUp ou Revit a partir do DWG;
  2. renderizar em D5, Twinmotion ou Blender Cycles, com o memorial descritivo;
  3. montar com a mesma direção de arte destes vídeos.
- **Tour da página:** usa a mesma planta, mas com mobiliário mais simples que o dos vídeos, para carregar rápido no celular. Para igualar os dois, é preciso exportar o modelo decorado em GLB com texturas comprimidas (KTX2).
- **Pé-direito e acabamentos:** precisam ser confirmados com o memorial de cada empreendimento real.

## 5. Como refazer

```bash
cd studio3d/film
python3 music.py            # trilhas
./render_all.sh             # quadros (4 processos em paralelo)
./encode.sh essencial acabamentos decorado cinematic   # MP4 em ../../portfolio/construtoras/
node stills.js              # comparativo e capas
```
