# Storymaker Oficial

Formação em storymaker com chancela da DocMe Comunicação.
**Método desenvolvido pela DocMe Comunicação.**

## O que tem aqui

| Pasta | Conteúdo |
|---|---|
| `docs/briefing-mestre.md` | Todas as decisões do projeto (marca, método, cases, produtos, preços, fases). Comece por aqui. |
| `docs/conversa-chatgpt-original.md` | A entrevista completa feita no ChatGPT, para consulta. |
| `site/` | Site da fase 1 (HTML/CSS/JS, sem dependências). |
| `ebooks/` | Sumário da coleção, e-book 2 completo, checklist de pré-produção e modelo de briefing. |
| `planilha/` | Planilha Excel: catálogo de produtos, pacotes com desconto e custos de cobertura. |
| `produtos/` | Produtos diagramados: `pdf/` (e-book 2, checklist, briefing, contrato), `catalogo/` (vitrine de todos os produtos) e os scripts que geram tudo. |

## Site

### Ver no computador

Abra `site/index.html` no navegador. Ou, dentro da pasta `site`, rode `python3 -m http.server` e acesse `http://localhost:8000`.

### O que editar

- **Preços, produtos, pacotes e links do Mercado Pago:** `site/assets/js/config.js`. Cole o link de pagamento no campo `checkout` de cada produto. Sem link, o botão aparece como "Em breve".
- **Portfólio e cases:** `site/assets/js/cases.js`. Cada case tem os campos do roteiro (objetivo, planejamento, o que mudou, como a equipe reagiu, no dia, aftermovie, aprendizado). Campo vazio aparece no site como **[PREENCHER]**, em amarelo.
- **Depoimentos da equipe** (`EQUIPE`) e **prints de clientes** (`ELOGIOS`): no fim do mesmo `cases.js`.
- **Imagens e vídeos:** coloque em `site/assets/img/` e aponte o caminho no campo `thumb`, `video` ou `imagem`.
- **Imagem de compartilhamento:** crie `site/assets/img/og.jpg` (1200×630).

### Antes de publicar

1. Registrar `storymakeroficial.com.br` e pesquisar a marca no INPI.
2. Preencher todos os **[PREENCHER]** e **[CONFIRMAR]** com material real.
3. Confirmar preços (estão como proposta inicial) e colar os links do Mercado Pago.
4. Configurar a entrega por e-mail depois do pagamento. O link do Mercado Pago cobra, mas não envia o PDF sozinho. É preciso uma integração (ex.: plataforma de produtos digitais ou automação via webhook).
5. Hospedar a pasta `site/`. Por ser estática, funciona em qualquer hospedagem (Hostinger, Netlify, Vercel, GitHub Pages).

### Fase 2 (ainda não feita)

Área do aluno, formulário de conhecimento, envio do vídeo de ~1min30, análise com IA e revisão humana, convite para lives e entrega automatizada.

## Planilha

`planilha/storymaker-oficial-produtos-e-custos.xlsx`. As células laranja claro são para preencher e as cinza são calculadas. A aba **Leia primeiro** explica cada parte. A aba **Custos de cobertura** também pode ser vendida como produto.

## Produtos (PDFs)

- Texto de cada produto: `ebooks/*.md`. Edite ali.
- Gerar os PDFs de novo: `python3 produtos/build.py` (precisa de `pip install markdown` e do Playwright).
- Gerar o catálogo: `python3 produtos/catalogo.py`. Preços e situação de cada produto ficam no topo desse arquivo.
- Gerar a planilha: `python3 produtos/planilha_build.py planilha/storymaker-oficial-produtos-e-custos.xlsx`.
- E-books: formato A5 (bom para ler no celular), a partir de 20 páginas, com ilustrações em `produtos/ilustracoes.py`.
- Os quadros tracejados "Espaço para material DocMe" marcam onde entram fotos, prints e frames reais.
- Mantenha os preços iguais em três lugares: `produtos/catalogo.py`, `site/assets/js/config.js` e `produtos/planilha_build.py`.

## Blog

- Texto original dos 11 artigos: `docs/blog/11-artigos-original.md`.
- Gerar as páginas: `python3 blog/gerar_blog.py` → `site/blog/`, `site/sitemap.xml` e `site/robots.txt`.
- Ajustes de palavra-chave e título SEO ficam no topo do script, com o motivo em `docs/palavras-chave.md`.
- Fotos dos artigos: crie `blog/imagens.json` no formato `{"slug-do-artigo": "assets/img/blog/foto.jpg"}`.
- Datas: crie `blog/datas.json` (`{"slug": {"publicado": "2026-12-01"}}`) só com datas reais de publicação.
