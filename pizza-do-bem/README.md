# Pizza do Bem 2018–2025: retrospectiva para o telão

Slideshow da Casa Ronald McDonald feito com as fotos da pasta do Google Drive
**"Telão pizza do bem"** (é a mesma pasta que você baixou em `F:\#2026\#Casa Ronald\Novembro\...`).

## Conferência da classificação

O ano de cada foto saiu da data do EXIF (data e hora em que a câmera tirou a foto). Depois conferi tudo
olhando os uniformes nas folhas de contato.

| Ano | Fotos | Uniforme conferido | Câmeras (EXIF) | Data do evento |
|---|---|---|---|---|
| 2018 | 22 | Rosa | Canon EOS 60D | 11/11/2018 |
| 2019 | 23 | Camiseta preta/azul-marinho | Canon EOS 60D + Sony ILCE-6300 | 24/11/2019 |
| 2020 | 0 | Nenhuma foto, bloco não criado | n/a | n/a |
| 2021 | 0 | Nenhuma foto, bloco não criado | n/a | n/a |
| 2022 | 41 | Roxo | Canon 5D Mark III + Nikon D610 | 23/10/2022 |
| 2023 | 38 | Verde ("10 anos") | Canon EOS RP | 12/11/2023 |
| 2024 | 0 | Nenhuma foto, bloco não criado | n/a | n/a |
| 2025 | 15 | Vinho | (arquivos "Cesar_Cinato…MOEMA_2025") | 30/11/2025 |

São 139 fotos no vídeo: todas as fotos da pasta, sem exceção.

Casos especiais:

- **`Cópia de IMG_0769.jpg` e `Cópia de IMG_1319.jpg`** não têm EXIF. Coloquei as duas em **2023** por três motivos:
  - têm a camiseta verde "10 anos";
  - a apresentadora está com o mesmo vestido laranja das outras fotos de 2023;
  - têm a mesma resolução de câmera (6240×4160) e a numeração está dentro da sequência de 2023.
- **`DSC_8321.JPG`** é igual, byte a byte, a `Cópia de DSC_8321.JPG`. Por pedido, as duas entram, em pontos diferentes do bloco de 2022.
- **As 9 imagens "WhatsApp Image 2026-11-11…"** vieram como referências de uniforme e não têm EXIF.
  - Por pedido, entraram no vídeo, classificadas visualmente.
  - **2018:** `(8)`, o grupo de uniforme rosa. Fecha o bloco de 2018.
  - **2019:** as outras 8, pela camiseta preta, pelo salão com cortinas vermelhas e verdes e pela mesma convidada de vestido preto rendado das fotos de 2019.
  - O grupo de preto abre 2019.
  - Elas têm só 1280 px de largura, então ficam um pouco menos nítidas no telão.
- **`Cópia de IMG_0259.jpg` (2023)** mostra a equipe de produção com camisetas roxas/pretas ("Eu não, nós").
  - Não é o uniforme roxo de 2022.
  - O EXIF é de 12/11/2023 e a câmera é a mesma do resto de 2023, então a foto ficou em 2023.
- **Nenhuma foto ficou com data indefinida.**

## Tratamento (`prep.py`)

- **Bordas pretas:** o script procura faixas pretas uniformes com corte seco. Nenhuma foto da pasta tem esse tipo de borda.
  - Os fundos escuros de palco e de teto fazem parte da cena e foram mantidos.
- **Exposição e cor:**
  - os níveis e a curva de contraste são os mesmos nos 3 canais;
  - o balanço de branco é parcial, limitado a ±4%, para manter as cores reais dos uniformes;
  - as fotos escuras recebem um gamma suave.
- **Enquadramento 16:9:**
  - os rostos são detectados (YuNet) e o recorte é escolhido para manter todos eles dentro da área segura do zoom de 5%;
  - quando o recorte cortaria algum rosto, a foto entra inteira sobre uma versão ampliada e desfocada dela mesma. Isso vale também para foto vertical;
  - esse tratamento foi usado em 3 fotos: `1L8A8073`, `Cópia de DSC_8027` e `Cópia de IMG_0724` (a vertical).
- Rostos, pessoas e logomarcas não foram alterados.

## Montagem (`render.py`)

- **Formato:** 1920×1080, 30 fps, H.264 High, CRF 17, BT.709, MP4 com faststart.
- **Duração:** cada foto fica 4,4 s em tela, mais 0,8 s de cross dissolve.
- **Movimento:**
  - zoom in de 100 para 105% e zoom out de 105 para 100%, um em cada foto;
  - o movimento é suave no início e no fim e segue o centro do grupo de rostos.
- **Abertura de cada ano:** começa com uma foto que mostra o uniforme. Depois as fotos seguem em ordem cronológica.
- **Encerramento:** a última foto é a das voluntárias de vinho (`…-5767`). Ela fica uns 4 s em tela e termina com fade out.
- **Ano na tela:** por pedido, os vídeos saem **sem a identificação dos anos**. Para reativar, use `SHOW_YEAR = True` em `render.py`.
- Não há telas pretas entre os anos, e as fotos seguem a ordem cronológica.
- **Versão LOOP:**
  - sem fade de abertura nem de encerramento;
  - 2025 se dissolve de volta para 2018;
  - o primeiro quadro do arquivo continua exatamente o último, então a repetição não tem emenda.

## Trilha sonora

**Os vídeos estão sem áudio.** Não consigo licenciar música, e o briefing pede trilha licenciada para o evento.

Para colocar a trilha escolhida (piano e cordas):

```bash
ffmpeg -i PizzaDoBem_Retrospectiva_2018-2025.mp4 -i trilha.mp3 -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -af "afade=t=out:st=$(( $(ffprobe -v error -show_entries format=duration -of csv=p=0 PizzaDoBem_Retrospectiva_2018-2025.mp4 | cut -d. -f1) - 3 )):d=3" -shortest saida_com_trilha.mp4
```

Com uma trilha de andamento constante, a 4,4 s por foto as trocas caem a cada 2 compassos em ~109 BPM,
ou a cada compasso em ~54,5 BPM.

## Como gerar os vídeos no seu computador (Windows)

### 1. Instale os programas (só uma vez)

- **Python 3:** baixe em [python.org/downloads](https://www.python.org/downloads/). Na instalação, **marque a opção "Add python.exe to PATH"**.
- **ffmpeg:** abra o *Prompt de Comando* e rode:

```bash
winget install Gyan.FFmpeg
```

Depois **feche e abra** o Prompt de Comando, para o Windows enxergar o ffmpeg.

### 2. Baixe os scripts

Baixe o ZIP deste branch:
[MayconBarbon-claude-amazing-mccarthy-i8o263.zip](https://github.com/MayconBarbon/MayconBarbon/archive/refs/heads/claude/amazing-mccarthy-i8o263.zip)

Descompacte e entre na pasta `pizza-do-bem`. Ela tem `GERAR_VIDEOS.bat`, `prep.py`, `render.py` e `yunet.onnx`.

### 3. Gere os vídeos

Dê **duplo clique em `GERAR_VIDEOS.bat`**. Quando ele pedir, arraste para a janela a pasta das fotos e tecle Enter, por exemplo:

```text
F:\#2026\#Casa Ronald\Novembro\Telão pizza do bem-20261111T133446Z-1-001\Telão pizza do bem
```

O script vai, nesta ordem:
1. instalar as bibliotecas necessárias (Pillow, NumPy, OpenCV);
2. classificar e tratar as 139 fotos, mostrando no final quantas fotos entraram em cada ano. Se alguma foto não for identificada, ela aparece como **"entre os anos"** e entra no vídeo entre 2023 e 2025;
3. renderizar o vídeo principal e a versão loop.

Cada vídeo leva de **20 a 60 minutos**, conforme o computador. Ao terminar, a pasta `SAIDA` abre sozinha com:

- `PizzaDoBem_Retrospectiva_2018-2025.mp4`, o principal;
- `PizzaDoBem_Retrospectiva_2018-2025_LOOP.mp4`, para repetição contínua;
- um `*_timeline.csv` para cada vídeo (abre no Excel), com a ordem das fotos;
- `trabalho\plates`, com as fotos já tratadas em 16:9.

Precisa de uns 4 GB livres em disco. Feche outros programas pesados durante a renderização.

`yunet.onnx` é o modelo de detecção de rostos YuNet, do OpenCV Zoo, com licença MIT.

## Como gerar de novo

```bash
python3 prep.py <pasta_fotos> <pasta_trabalho>      # YUNET=<caminho>/face_detection_yunet_2023mar.onnx
```

```bash
python3 render.py <pasta_trabalho> principal PizzaDoBem_Retrospectiva_2018-2025.mp4 4
```

```bash
python3 render.py <pasta_trabalho> loop PizzaDoBem_Retrospectiva_2018-2025_LOOP.mp4 4
```

Junto com cada MP4 sai um `*_timeline.csv` com a ordem, o ano, o tempo e o movimento de cada foto.
Para mudar a ordem, edite `OPENER`/`CLOSER` em `render.py`. Para tirar uma foto, apague a placa dela em `plates/`.
