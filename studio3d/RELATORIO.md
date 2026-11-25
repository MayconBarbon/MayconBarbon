# Vídeo Imóvel Studio 3D · relatório e proposta de operação

Status: **publicada** em 25/11/2026 em https://videoimovel.com.br/construtoras/ (página 625). Política de privacidade publicada em /politica-de-privacidade/ (página 632).

## 1. O que foi entregue

| Item | Onde | Status |
|---|---|---|
| Página /construtoras com 10 blocos (hero, tour, etapas, serviços, comparador, portfólio, como funciona, para quem é, fidelidade técnica, briefing, FAQ, CTA final) | WordPress, página 625 (rascunho), fonte em `videoimovel-site/construtoras/index.body.html` | Pronta para revisão |
| Tour 3D com 2 projetos de demonstração: apartamento tipo em edifício conceitual (planta 3) e casa térrea (planta 2) | `studio3d/tour/` (`tour.js`, `plans/`, `build.py`) | Testado |
| Modos do tour: Planta 2D, Estrutura, Decorado, Passeio (1ª pessoa com colisão e minimapa "você está aqui"), Tour guiado, Edifício (só apartamento), luz da manhã à noite | idem | Testado |
| Formulário de briefing em 6 etapas (blocos A–K), com upload de até 6 MB por arquivo, campo de link para arquivos grandes, protocolo VI3D-AAMMDD-XXXX e aviso de sucesso só depois do envio confirmado | Contact Form 7, ID 615 | Criado. Falta o teste de envio real |
| SEO: title, meta description, um único H1, schema (Service, BreadcrumbList, FAQPage) | Página 625 + SEOPress | Configurado |
| Plantas 2D redesenhadas no estilo Vídeo Imóvel | `studio3d/tour/planta.svg`, `planta-apto.svg` | Pronto |

As plantas que você enviou foram **redesenhadas** e não publicadas como imagem. A planta 1 tinha marca-d'água de outra empresa. Todo o material traz o aviso "Projeto de demonstração" e "não é empreendimento à venda". O vídeo do Maison D'or aparece como **captação real com drone**, não como render.

## 2. Testes feitos (prévia logada, Chromium)

| Teste | Desktop 1366 | iPhone 13 |
|---|---|---|
| Página carrega, 1 H1, sem rolagem horizontal | ✅ | ✅ |
| Tour carrega sob demanda (three.js r128, cdnjs) e troca de modos | ✅ | ✅ |
| Modo Edifício e Planta 2D | ✅ | ✅ |
| Formulário: bloqueia avanço com campo obrigatório vazio | ✅ | ✅ |
| Formulário: avança da etapa 1 para a 2 depois de preenchida | ✅ | ✅ |
| Erros de JavaScript na página | nenhum | nenhum |
| Contraste dos textos (WCAG AA) | ✅ menor razão 5,4:1 | — |
| Envio real do formulário no site publicado (visitante, com PDF anexado) | ✅ protocolo VI3D-261125-WEHH, salvo no Flamingo | — |
| Etapa de vídeo pulada quando o Cinematic não é marcado | ✅ | — |
| Lighthouse (performance) na página publicada | ⏳ depende da publicação | ⏳ |

Observação: com o administrador logado, o widget de suporte da Hostinger cobre a tela no celular. Visitantes não veem esse widget.

## 3. Feito após a autorização (25/11/2026)
- Página /construtoras publicada, com SEO (title, description, canonical) conferido na versão pública.
- Flamingo instalado e ativo: cada briefing fica em Flamingo › Mensagens recebidas, com nome, e-mail e o assunto "Briefing [protocolo] · empresa · tipo".
- Política de privacidade publicada e ligada no aceite do formulário, no rodapé da página e no rodapé da home.
- Home: botão "Ainda na planta? Conheça o Studio 3D" na seção de construtoras e link no rodapé. Cache do LiteSpeed limpo.
- Correção encontrada no teste: o CF7 tratava as perguntas de escolha única como obrigatórias. Elas viraram caixas de escolha única opcionais.

## Pendente
- **Anti-spam:** criar um widget gratuito do Cloudflare Turnstile (site key + secret key) e colar as chaves em WordPress › Contato › Integração › Cloudflare Turnstile. As chaves não devem ser enviadas pelo chat. Depois disso, ativar o e-mail de confirmação ao solicitante (mail_2, já escrito).
- Revisão jurídica da política de privacidade (o texto é uma versão inicial).
- Lighthouse da página publicada.

## 4. Proposta de operação

### Fluxos de trabalho
- **A · Essencial / Acabamentos (rápido):** briefing → conferência da planta (até 1 dia útil) → proposta → modelagem da estrutura → validação → materiais → entrega das imagens. Uma rodada de ajustes incluída.
- **B · Decorado + tour:** fluxo A + mobiliário e decoração → imagens na altura dos olhos → montagem do tour (o mesmo motor desta página, com a planta do cliente) → entrega com código para o site do empreendimento.
- **C · Cinematic:** fluxo B + roteiro de cenas → animação de câmera → trilha, lettering e assinatura → versões vertical e horizontal. Com o prédio pronto, a captação passa a ser real com drone (o produto que já existe).

### Ferramentas sugeridas
- Modelagem: SketchUp ou Blender, com importação de DWG/DXF.
- Render: Blender Cycles/Eevee (gratuito) ou D5 Render / Twinmotion.
- Tour web: o motor deste projeto (`studio3d/tour`), que recebe a planta como dados.
- Gestão: o CF7 + Flamingo para entrada dos pedidos e uma planilha ou quadro para o andamento.

### Estrutura de preço (sem valores definidos)
Não defini preços. A sugestão é cobrar por **unidade de planta** (cada tipologia), com estes fatores:
- área e número de ambientes;
- nível (Essencial < Acabamentos < Decorado < Cinematic);
- quantidade de imagens extras e segundos de vídeo;
- prazo (taxa de urgência);
- reaproveitamento: tipologias espelhadas ou repetidas no mesmo prédio saem com desconto.

As faixas do formulário (até R$ 3 mil, de R$ 3 mil a R$ 8 mil, de R$ 8 mil a R$ 20 mil, acima de R$ 20 mil) servem só para qualificar o pedido. Elas não aparecem como preço na página.

### Arquitetura do painel (admin)
- Hoje: o CF7 (formulário 615) envia o e-mail com os anexos e o protocolo para o e-mail do administrador do site.
- Próximo passo: o Flamingo guarda cada envio (com o protocolo) no painel.
- Futuro: um tipo de post "Projetos 3D" com status (novo, proposta enviada, em modelagem, em validação, entregue).

## 5. Ideias de artigos para o blog
1. Planta 3D ou render: qual usar no lançamento?
2. Como apresentar um apartamento na planta para quem nunca leu uma planta.
3. Tour 3D no site do empreendimento: o que muda na conversão.
4. Checklist de arquivos para pedir uma planta 3D.

## 6. Como atualizar o tour
1. Edite `studio3d/tour/plans/*.js` ou `plans/apto.json` e `tour.js`.
2. Rode `python3 studio3d/tour/build.py`. Ele gera o `tour.build.js` e bloqueia o operador `&&`, que o WordPress quebra.
3. Republique o rascunho com `studio3d/pub_construtoras.py`. Ele precisa da sessão do WordPress, que fica fora do repositório.
