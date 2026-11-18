/*
 * CONFIGURAÇÃO DO SITE — Storymaker Oficial
 * ------------------------------------------------------------
 * Este é o único arquivo que você precisa editar para:
 *  - trocar preços;
 *  - colar os links de pagamento do Mercado Pago (campo "checkout");
 *  - ativar/pausar produtos;
 *  - montar os pacotes.
 *
 * Regras:
 *  - Preço do pacote: a economia mostrada no site é calculada
 *    automaticamente a partir dos preços avulsos abaixo (nunca digite
 *    um "preço original" inventado).
 *  - Produto sem link de checkout aparece com o botão "Em breve".
 *  - Os preços atuais são PROPOSTA INICIAL (mesmos da planilha
 *    storymaker-oficial-produtos-e-custos.xlsx). Ajuste antes de lançar.
 */
window.SITE_CONFIG = {
  // Tema visual: "grafite" (abertura escura) ou "laranja" (laranja como cor principal).
  // Para testar sem editar: abra o site com ?tema=laranja ou ?tema=grafite no endereço.
  tema: "laranja",

  marca: "Storymaker Oficial",
  assinatura: "Método desenvolvido pela DocMe Comunicação.",
  dominio: "https://storymakeroficial.com.br",
  instagram: "", // [PREENCHER] ex.: https://instagram.com/storymakeroficial
  emailContato: "", // [PREENCHER]
  docmeSite: "", // [PREENCHER] site da DocMe Comunicação

  produtos: [
    { id: "ebook-1", tipo: "E-book", titulo: "Fundamentos do Storymaker", resumo: "O que faz um storymaker e como transformar o seu olhar de imagem em um novo serviço.", preco: 39, checkout: "", ativo: true },
    { id: "ebook-2", tipo: "E-book", titulo: "Do briefing à história", resumo: "A reunião com o cliente, as perguntas certas, os canais, as prioridades e o plano da cobertura.", preco: 99, checkout: "", ativo: true, destaque: true },
    { id: "ebook-3", tipo: "E-book", titulo: "Olhar e narrativa", resumo: "Leitura do evento, lista de cenas, variação de planos e a sequência que conta uma história.", preco: 69, checkout: "", ativo: true },
    { id: "ebook-4", tipo: "E-book", titulo: "Cobertura e edição ágil", resumo: "Tempo real, CapCut, aprovação com o cliente, atrasos, bateria e o Reels final.", preco: 69, checkout: "", ativo: true },
    { id: "ebook-5", tipo: "E-book", titulo: "Operação profissional", resumo: "Proposta, preço, custos, contrato, portfólio e os primeiros trabalhos.", preco: 99, checkout: "", ativo: true },
    { id: "check-pre", tipo: "Checklist", titulo: "Checklist de pré-produção", resumo: "Antes do evento, véspera e chegada ao local.", preco: 9, checkout: "", ativo: true },
    { id: "check-cob", tipo: "Checklist", titulo: "Checklist de cobertura", resumo: "Durante o evento: sequência, pessoas prioritárias e bateria.", preco: 9, checkout: "", ativo: true },
    { id: "check-pos", tipo: "Checklist", titulo: "Checklist de pós-produção", resumo: "Reels final, legenda, upload e entrega.", preco: 9, checkout: "", ativo: true },
    { id: "evento-amanha", tipo: "Checklist", titulo: "Seu evento é amanhã (grátis)", resumo: "Te chamaram hoje para trabalhar amanhã? Dez perguntas urgentes, prioridades, equipamentos e modelos de mensagem. Gratuito: o link é o cadastro na plataforma.", preco: 0, checkout: "", ativo: true },
    { id: "roteiro-fim-de-ano", tipo: "Guia", titulo: "Roteiro de fim de ano", resumo: "Confraternização, Natal e Réveillon (inclusive em bares e hotéis): o que gravar, em que ordem e como entregar no mesmo dia.", preco: 19, checkout: "", ativo: true, destaque: true },
    { id: "check-audio", tipo: "Checklist", titulo: "Checklist de áudio", resumo: "Fonte principal, backup, teste de som e cópia de segurança: nunca dependa de uma fonte só.", preco: 9, checkout: "", ativo: true },
    { id: "guia-seq", tipo: "Guia", titulo: "Guia rápido: sequência de stories", resumo: "Espaço, recepção, atrações e encerramento: a estrutura que funciona.", preco: 19, checkout: "", ativo: true },
    { id: "modelo-briefing", tipo: "Modelo", titulo: "Modelo de briefing", resumo: "O formulário para conduzir a reunião com o cliente.", preco: 19, checkout: "", ativo: true },
    { id: "roteiro", tipo: "Modelo", titulo: "Roteiro de cobertura", resumo: "Prioridades, horários e pessoas em uma página.", preco: 19, checkout: "", ativo: true },
    { id: "planilha", tipo: "Planilha", titulo: "Planilha de custos e horas", resumo: "Monte o orçamento contando todas as horas reais do trabalho.", preco: 49, checkout: "", ativo: true },
    { id: "contrato", tipo: "Contrato", titulo: "Modelo de contrato", resumo: "Contrato editável para coberturas de storymaker.", preco: 39, checkout: "", ativo: true },
    { id: "trilha", tipo: "Acompanhamento", titulo: "Trilha com avaliação e lives mensais", resumo: "12 meses: avaliação do seu vídeo e do portfólio e uma live por mês com a equipe DocMe para casos reais.", preco: 297, checkout: "", ativo: false }
  ],

  pacotes: [
    {
      id: "pacote-completo",
      // Ativar quando os 14 produtos estiverem prontos (ativo: true).
      titulo: "Pacote Completo",
      resumo: "Os cinco e-books, todos os materiais práticos e 12 meses de trilha com avaliação e lives mensais.",
      itens: ["ebook-1", "ebook-2", "ebook-3", "ebook-4", "ebook-5", "check-pre", "check-cob", "check-pos", "check-audio", "guia-seq", "modelo-briefing", "roteiro", "planilha", "contrato", "trilha"],
      preco: 697,
      checkout: "",
      beneficio: "Inclui a avaliação do seu portfólio e as lives mensais com a equipe DocMe.",
      ativo: false
    },
    {
      id: "kit-lancamento",
      titulo: "Kit Lançamento",
      resumo: "Os quatro materiais prontos: checklist, contrato, planilha e o e-book Do briefing à história.",
      itens: ["check-pre", "contrato", "planilha", "ebook-2"],
      preco: 127,
      checkout: "",
      ativo: true
    }
  ]
};
