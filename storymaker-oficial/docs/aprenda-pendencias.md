# Página de campanha `/aprenda/` — relatório e pendências

18/11/2026. Página independente para tráfego de anúncios, separada do site institucional.

## Rota e arquivos

- **Rota:** `site/aprenda/index.html` → `/aprenda/` quando o site estiver no ar. Hoje abre direto pelo arquivo.
- **Criados:**
  - `site/aprenda/index.html` (página)
  - `site/aprenda/aprenda.css` (visual próprio: fundo grafite, laranja e branco/cinza; não carrega o `style.css` do site)
  - `site/aprenda/aprenda.js` (monta os produtos a partir do `config.js`, a VSL e os links)
  - `docs/vsl-roteiro.md` (locução, storyboard, termos de busca, trilha, licenças)
  - `docs/video/vsl/` (vídeo v1 9:16, legendas `.srt`, capa provisória e scripts de montagem)
  - `docs/aprenda-pendencias.md` (este relatório)
- **Alterados:** nenhum arquivo do site institucional. Conferido por hash SHA-256 dos 33 arquivos de `site/` (fora de `aprenda/`), antes e depois: idênticos.
- A página **não está no menu** do site e tem `noindex` até a revisão final.

## Produtos exibidos (nomes, preços e links vindos de `site/assets/js/config.js`, sem alteração)

| Produto | Preço | Checkout no config | Arquivo pronto | Botão hoje |
|---|---|---|---|---|
| Seu evento é amanhã (grátis) | Grátis | vazio | sim | Em breve |
| Checklist de pré-produção | R$ 9 | vazio | sim | Em breve |
| Checklist de cobertura | R$ 9 | vazio | sim | Em breve |
| Checklist de pós-produção | R$ 9 | vazio | sim | Em breve |
| Checklist de áudio | R$ 9 | vazio | sim | Em breve |
| Modelo de briefing | R$ 19 | vazio | sim | Em breve |
| Roteiro de fim de ano | R$ 19 | vazio | sim | Em breve |
| Guia rápido: sequência de stories | R$ 19 | vazio | **não** | Em breve |
| Roteiro de cobertura | R$ 19 | vazio | **não** | Em breve |
| Planilha de custos e horas | R$ 49 | vazio | sim | Em breve |
| Modelo de contrato | R$ 39 | vazio | sim | Em breve |
| Fundamentos do Storymaker | R$ 39 | vazio | **não** | Em breve |
| Do briefing à história | R$ 99 | vazio | sim | Em breve |
| Olhar e narrativa | R$ 69 | vazio | **não** | Em breve |
| Cobertura e edição ágil | R$ 69 | vazio | **não** | Em breve |
| Operação profissional | R$ 99 | vazio | **não** | Em breve |
| **Kit Lançamento** | R$ 127 | vazio | sim (4 itens) | Em breve. Economia exibida: R$ 69 (avulsos R$ 196, calculado) |
| **Pacote Completo** | R$ 697 | vazio | inativo no config | **Oculto** (a página só mostra quando `ativo: true`) |

Regra do botão "Quero este material": produto ativo **e** com arquivo pronto **e** com link de checkout. Os materiais sem arquivo aparecem como "Em produção", sem conteúdo descrito.

## Pendências

1. **Links de checkout.** Todos os campos `checkout` estão vazios. Definir a plataforma (Kiwify ou Mercado Pago: o README cita Mercado Pago) e colar os links em `site/assets/js/config.js`. Ao colar, os botões passam a funcionar na página e no site institucional ao mesmo tempo.
2. **Condições de compra.** O FAQ remete à página de pagamento para formas de pagamento, acesso e arrependimento. Quando a plataforma estiver definida, conferir e, se quiser, copiar as condições exatas.
3. **URL da VSL.** Colar em `site/aprenda/aprenda.js`, constante `VSL`. Enquanto estiver vazia, o player aparece desativado ("Vídeo de apresentação em produção") e nada é carregado.
4. **VSL v1 sem narração.** O ElevenLabs estava desconectado nesta sessão (reconectar nas configurações de conectores do claude.ai). A v1 tem legendas e trilha; falta gravar a voz do Gabriel e aprovar os direitos antes de publicar.
5. **URL institucional.** `docmeSite` está vazio no config; o link "Conheça a DocMe" aponta para a página inicial deste site (`../index.html`). Para usar outro endereço, preencher `DOCME_URL` em `aprenda.js`.
6. **Pacote Completo.** Está inativo e inclui a trilha com lives (também inativa). Avulsos com a trilha: R$ 853 (economia de R$ 156). **Sem a trilha, os avulsos somam R$ 556, menos que o pacote.** Revisar a composição antes de ativar.
7. **Seis materiais sem arquivo** (e-books 1, 3, 4 e 5, Guia de sequência e Roteiro de cobertura) estão `ativo: true` no config e aparecem como "Em breve" no site institucional também.
8. **"Seu evento é amanhã"**: o resumo diz que o link é o cadastro na plataforma; falta esse link.

## O que não foi inventado

Nenhum preço, nome, link, depoimento, avaliação, número, garantia, bônus, prazo ou promessa foi criado. A única prova usada é a já aprovada no site: foto do fundador com a legenda "Fundador da DocMe Comunicação" e "+100 eventos produzidos pela DocMe". A economia do Kit é calculada pelos preços do config. Não há pop-up, contador, escassez, formulário de e-mail, Instagram ou localização.

## Testes feitos (Playwright, Chromium)

- **Celular (iPhone 13) e computador (1366×900):** sem erros de JavaScript; sem rolagem horizontal; 16 cards; Kit visível com economia de R$ 69; Pacote oculto.
- **Preços:** cada card exibido conferido com o `config.js`: todos iguais.
- **CTAs sem checkout:** todos "Em breve" (sem link); o botão "Começar" do topo fica oculto.
- **CTAs com checkout de teste** (links fictícios injetados só no teste): cada botão aponta para o link do próprio produto; os 6 sem arquivo continuam "Em breve"; o Kit vira "Quero o Kit Lançamento"; o CTA do topo leva ao material grátis.
- **Teclado:** Tab passa por "Pular para o conteúdo", logo, "Conheça a DocMe", "Ver os materiais" e os botões, com contorno de foco visível.
- **VSL:** sem URL, botão desativado e nenhum vídeo carregado. Com um MP4 de teste (cópia temporária da página, já apagada): nenhum download antes do toque; o vídeo só começa depois do clique, com controles.
- **Site institucional:** hashes idênticos antes e depois.

Nada foi publicado e nenhuma configuração de domínio, DNS ou hospedagem foi alterada.
