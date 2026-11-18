# Instruções permanentes — DocMe Comunicação (todos os projetos deste repositório)

## Locução padrão DocMe

- **Voz padrão de todas as locuções da DocMe e das marcas dela** (Storymaker Oficial, vídeos de clientes, VSLs, anúncios, vídeos de ensino sem rosto): **Gabriel — Friendly Brazilian Ad Voice** (ElevenLabs).
- `voice_id`: `WPgqgCVa3mD38JuyODU6` · modelo `eleven_v4` · `language_code: "pt"`.
- É a mesma voz dos vídeos Importway Brand Film 60s e SIMESPI x Dama Bier.
- Estilo: marcações de tom como `[warmly]`, `[curious]`, `[pause]`, `[long pause]`; frases curtas; nomes difíceis escritos como se pronunciam só no texto enviado à voz (ex.: "Siméspi", "Bí-er", "Dóc Mi", "Kiuí-fai"); a legenda mantém a grafia normal.
- Depois de gerar, transcrever o áudio (ElevenLabs speech-to-text, `scribe_v1`) e conferir se as falas saíram certas e se nenhuma marcação foi lida em voz alta.
- Se o conector do ElevenLabs estiver desconectado, usar a API `api.elevenlabs.io` com a chave salva como segredo de rede da sessão (nunca colar a chave no chat nem no código).
- Exceção: avatar de IA com o rosto do fundador usa a voz dele (clonada com autorização), não a do Gabriel.
