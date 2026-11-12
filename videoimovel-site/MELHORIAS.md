# Novo site — Vídeo Imóvel

Proposta estática (HTML + CSS, sem dependências) para substituir a home atual de videoimovel.com.br (WordPress + Elementor).
Abra `index.html` no navegador. Para publicar: suba a pasta inteira (`index.html` + `assets/`) para qualquer hospedagem estática,
ou use como referência para reconstruir no Elementor.

## Roteiro aplicado (os 7 passos do post de referência)

1. **Planta do site** — uma página, uma ação: mandar as fotos pelo WhatsApp. Ordem: promessa → para quem é → prova (antes e depois) → como funciona → portfólio → captação no local → planos → dúvidas → chamada final.
2. **A primeira coisa que o visitante vê** — título curto ("Suas fotos. O vídeo que o seu imóvel merece."), prazo de 48 h e um vídeo vertical real tocando dentro de um celular.
3. **Como o site se move** — animações discretas: entrada do hero, leve subida dos blocos ao rolar (só em navegadores compatíveis) e o comparador arrastável de antes e depois. Tudo é desligado para quem pede menos movimento no sistema.
4. **O texto** — frases curtas, sem promessas que não dá para comprovar. A frase da marca aparece no portfólio e no fechamento: "A melhor imagem do seu imóvel está aqui."
5. **Plano de construção** — HTML e CSS puros, fontes Manrope e Inter (Google Fonts), imagens em WebP (2,2 MB no total), modo claro e escuro automático, layout responsivo do celular ao desktop.
6. **Auditoria de conversão** — o WhatsApp aparece no menu, no hero, em cada plano e no fechamento, sempre com mensagem pronta. O número também fica visível como texto.
7. **Plano de lançamento** — veja "Antes de publicar".

## O que mudou em relação ao site atual

- **Visual**: muito espaço em branco, uma cor de destaque (o verde-água do play do logo) e o azul-marinho do logo nas faixas escuras. Saíram os blocos coloridos e as fontes em caixa alta.
- **Prova visual**: o "antes e depois" virou um comparador interativo com uma sala real. A simulação com IA está sinalizada.
- **Banco de vídeos**: carrossel com 9 vídeos verticais (toca sozinho quando aparece, sem som; toque para pausar). Os feitos com IA têm selo.
- **Planos sem preço**: cada plano leva a "Pedir orçamento".
- **Portfólio**: 7 trabalhos reais do acervo no lugar de exemplos genéricos.
- **Textos removidos ou suavizados**, porque não dá para comprovar (regras do CDC/CONAR e do Google Ads): "Vende e aluga mais rápido" e "o investimento se paga já na primeira visita".
- **Depoimentos**: ficaram de fora até a equipe confirmar que são de clientes reais e que eles autorizam o uso (nome e função).
- **"SÃO PAULO" no topo**: removido. Fica "Atendimento em todo o Brasil", como no texto de contato do site atual.

## Antes de publicar

- [ ] Confirmar o WhatsApp +55 19 99861-2626 e a mensagem pronta.
- [ ] Preços removidos a pedido: os planos levam a "Pedir orçamento" no WhatsApp.
- [ ] Banco de vídeos: incluir o vídeo do condomínio de alto padrão em São Paulo (pasta privada no Drive; ver observação na conversa).
- [ ] Confirmar a autorização de uso das imagens de clientes no portfólio (RJ, Casa Paulo, Bazzanelli, Rieti, Canadá).
- [ ] Trocar o vídeo do hero por um corte oficial, se preferirem (`assets/hero.mp4`, 12 s, sem áudio).
- [ ] Configurar o Pixel da Meta e o Google Analytics/Tag Manager para medir os cliques no WhatsApp (campanhas de tráfego).
- [ ] Adicionar política de privacidade se o site passar a coletar dados.
