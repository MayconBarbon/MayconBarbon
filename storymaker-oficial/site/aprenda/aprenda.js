/*
 * Página de campanha /aprenda/ — Storymaker Oficial
 * ------------------------------------------------------------
 * NOMES, PREÇOS E LINKS DE CHECKOUT vêm SEMPRE de ../assets/js/config.js
 * (a mesma fonte do site institucional). Este arquivo NÃO repete preço.
 *
 * Aqui ficam só:
 *  - VSL: o endereço do vídeo de vendas (vazio = espaço reservado, sem vídeo);
 *  - DOCME_URL: o site institucional para o link "Conheça a DocMe";
 *  - PRONTO: quais materiais têm arquivo final no projeto (produtos/pdf);
 *  - DETALHES: etapa, conteúdo e perfil de cada material, tirados dos
 *    próprios arquivos (ebooks/*.md e a planilha). Nada inventado.
 *
 * Regra de botão: só aparece "Quero este material" quando o produto
 * está ativo no config, tem arquivo pronto E tem link de checkout.
 * Nos outros casos, o botão aparece como "Em breve" (sem link).
 */
(function () {
  "use strict";

  // [PENDENTE] Cole aqui o link do vídeo de vendas (MP4 próprio ou embed do YouTube/Vimeo).
  // Ex.: { tipo: "mp4", src: "../assets/video/vsl.mp4", capa: "../assets/video/vsl-capa.jpg" }
  //      { tipo: "embed", src: "https://www.youtube-nocookie.com/embed/ID_DO_VIDEO" }
  var VSL = { tipo: "", src: "", capa: "" };

  // [PENDENTE] Site institucional. Vazio = usa a página inicial deste mesmo site.
  var DOCME_URL = "";

  // Materiais com arquivo final em produtos/pdf (conferido em 18/11/2026).
  var PRONTO = ["evento-amanha", "check-pre", "check-cob", "check-pos", "check-audio",
    "roteiro-fim-de-ano", "modelo-briefing", "contrato", "planilha", "ebook-2"];

  var DETALHES = {
    "evento-amanha": { etapa: "Quando o convite chega em cima da hora", formato: "PDF, 2 páginas",
      inclui: "Dez perguntas urgentes para o cliente, equipamentos, quadro de prioridades, roteiro rápido, cuidados antes de dizer o preço e modelos de mensagem de confirmação e de aprovação.",
      paraQuem: "Quem foi chamado hoje para trabalhar amanhã e quer chegar organizado." },
    "check-pre": { etapa: "Antes do evento", formato: "PDF, 2 páginas",
      inclui: "Na semana: briefing, publicação, escopo e valor. Na véspera: equipe e equipamento. Na chegada: sinal de internet, mapa do evento e caminho de captação com planos aberto, médio e fechado.",
      paraQuem: "Quem está começando e quer um passo a passo para não esquecer nada." },
    "check-cob": { etapa: "Durante o evento", formato: "PDF, 2 páginas",
      inclui: "Primeiros 15 minutos, a sequência que conta a história, controle de pessoas e momentos, publicação em tempo real e o que fazer quando algo sai do plano (atraso, bateria).",
      paraQuem: "Quem chega ao evento e fica em dúvida sobre o que gravar primeiro." },
    "check-pos": { etapa: "Depois do evento", formato: "PDF, 1 página",
      inclui: "Reels final antes de ir embora, aprovação do vídeo e da legenda, encerramento, entrega no dia seguinte e o que guardar para o portfólio.",
      paraQuem: "Quem quer fechar a entrega no mesmo dia sem se perder." },
    "check-audio": { etapa: "Som da fala e dos momentos", formato: "PDF, 1 página",
      inclui: "Áudio no briefing, na véspera, no local antes de começar, durante e depois: fonte principal, backup, teste de som e cópia de segurança.",
      paraQuem: "Quem tem receio de perder uma fala, um discurso ou um parabéns por falha de áudio." },
    "roteiro-fim-de-ano": { etapa: "Datas de fim de ano", formato: "PDF, 3 páginas",
      inclui: "Quem contrata no fim de ano, confraternização de empresa, Natal em família, Réveillon (inclusive em bares, restaurantes e hotéis) e entrega no mesmo dia.",
      paraQuem: "Quem quer atender confraternizações e festas de fim de ano." },
    "modelo-briefing": { etapa: "Entender o cliente", formato: "PDF, 3 páginas",
      inclui: "Dados básicos, objetivo, público e espaço, publicação, programação, lista A/B/C de pessoas importantes, o que não pode faltar, mudanças e imprevistos, entrega e estrutura.",
      paraQuem: "Quem tem dificuldade para entender o que o cliente espera." },
    "contrato": { etapa: "Combinar por escrito", formato: "Modelo editável, 4 páginas",
      inclui: "Objeto, escopo e quantidades, briefing, fluxo de publicação, mudança de programação e horas extras, prazos e entrega, pagamento, cancelamento, direito de imagem e uso em portfólio, equipamento e foro.",
      paraQuem: "Quem já vai atender e quer deixar escopo, prazos e imprevistos combinados." },
    "planilha": { etapa: "Montar o orçamento", formato: "xlsx, 5 abas",
      inclui: "Custos de cobertura com todas as horas reais (reunião, pesquisa, referências, deslocamento, evento, edição, upload e revisões), pacotes de serviço, equipe e margem e hora extra.",
      paraQuem: "Quem não sabe como colocar reunião, pesquisa, deslocamento e pós-produção no orçamento." },
    "ebook-2": { etapa: "Planejar a cobertura", formato: "PDF, 48 páginas",
      inclui: "A reunião de briefing, tempo real ou não, lista A/B/C, o que não pode faltar, roteiro previsto, quem publica e quem aprova, mudança de programação, atrasos, bateria e equipamento, equipe e grade de horários, exercício prático e glossário.",
      paraQuem: "Fotógrafos, videomakers e iniciantes que querem planejar antes de ligar a câmera." }
  };

  // Degraus: do mais acessível ao mais completo. Só ids que existem no config entram.
  var DEGRAUS = [
    { n: "Comece por aqui", titulo: "Material gratuito", texto: "Para conhecer o método sem pagar nada.", ids: ["evento-amanha"] },
    { n: "Degrau 1", titulo: "Checklists", texto: "Uma página ou duas para levar no celular: antes, durante e depois do evento.", ids: ["check-pre", "check-cob", "check-pos", "check-audio"] },
    { n: "Degrau 2", titulo: "Guias e modelos", texto: "Para entender o cliente e organizar o roteiro.", ids: ["modelo-briefing", "roteiro-fim-de-ano", "guia-seq", "roteiro"] },
    { n: "Degrau 3", titulo: "Para atender com segurança", texto: "Orçamento e contrato.", ids: ["planilha", "contrato"] },
    { n: "Degrau 4", titulo: "E-books", texto: "O método explicado com calma, com exemplos e exercícios.", ids: ["ebook-1", "ebook-2", "ebook-3", "ebook-4", "ebook-5"] }
  ];

  var C = window.SITE_CONFIG || { produtos: [], pacotes: [] };
  var porId = {};
  (C.produtos || []).forEach(function (p) { porId[p.id] = p; });

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function brl(n) { return n === 0 ? "Grátis" : n.toLocaleString("pt-BR", { style: "currency", currency: "BRL" }); }
  function vende(p) { return !!(p && p.ativo && p.checkout && PRONTO.indexOf(p.id) > -1); }
  function botao(p, rotulo) {
    if (vende(p)) return '<a class="btn" href="' + esc(p.checkout) + '" rel="noopener" data-produto="' + esc(p.id) + '">' + esc(rotulo) + "</a>";
    return '<span class="btn btn--off" aria-disabled="true">Em breve</span>';
  }

  // ---------- link institucional ----------
  var docme = document.querySelectorAll("[data-docme]");
  for (var i = 0; i < docme.length; i++) docme[i].href = DOCME_URL || C.docmeSite || "../index.html";

  // ---------- produtos ----------
  var alvo = document.getElementById("degraus");
  if (alvo) {
    alvo.innerHTML = DEGRAUS.map(function (d) {
      var itens = d.ids.map(function (id) { return porId[id]; }).filter(function (p) { return p && p.ativo; });
      if (!itens.length) return "";
      return '<div class="degrau"><div class="degrau__cab"><span class="degrau__n">' + esc(d.n) + "</span><h3>" + esc(d.titulo) + "</h3><p>" + esc(d.texto) + "</p></div>" +
        '<div class="produtos">' + itens.map(function (p) {
          var x = DETALHES[p.id];
          var pronto = PRONTO.indexOf(p.id) > -1;
          var rotulo = p.preco === 0 ? "Quero o material grátis" : "Quero este material";
          return '<article class="prod' + (pronto ? "" : " prod--breve") + '" id="p-' + esc(p.id) + '">' +
            '<span class="prod__tipo">' + esc(p.tipo) + (x ? " · " + esc(x.formato) : "") + "</span>" +
            "<h4>" + esc(p.titulo) + "</h4><p>" + esc(p.resumo) + "</p>" +
            (x ? '<p class="prod__etapa"><b>Etapa:</b> ' + esc(x.etapa) + " · <b>Indicado para:</b> " + esc(x.paraQuem) + "</p>" +
              '<details class="prod__mais"><summary>O que tem dentro</summary><p>' + esc(x.inclui) + "</p></details>"
              : '<p class="prod__etapa"><b>Em produção.</b> Os detalhes aparecem aqui quando o material estiver pronto.</p>') +
            '<div class="prod__pe"><span class="preco" data-preco="' + esc(p.preco) + '">' + brl(p.preco) + "</span>" + botao(p, rotulo) + "</div></article>";
        }).join("") + "</div></div>";
    }).join("");
  }

  // ---------- Kit Lançamento e Pacote Completo (dados do config, economia calculada) ----------
  function oferta(idPacote, elId) {
    var el = document.getElementById(elId);
    var pac = (C.pacotes || []).filter(function (p) { return p.id === idPacote; })[0];
    if (!el) return;
    if (!pac || !pac.ativo) { el.hidden = true; return; }
    var itens = pac.itens.map(function (id) { return porId[id]; });
    if (itens.some(function (p) { return !p || typeof p.preco !== "number"; })) { el.hidden = true; return; }
    var soma = itens.reduce(function (a, p) { return a + p.preco; }, 0);
    var eco = soma - pac.preco;
    var tudoPronto = itens.every(function (p) { return PRONTO.indexOf(p.id) > -1; });
    var pode = pac.checkout && tudoPronto;
    el.hidden = false;
    el.innerHTML =
      '<div><p class="eyebrow">' + (idPacote === "kit-lancamento" ? "Oferta em conjunto" : "Tudo em um só lugar") + "</p>" +
        "<h3>" + esc(pac.titulo) + "</h3><p>" + esc(pac.resumo) + "</p>" +
        "<ul>" + itens.map(function (p) { return "<li>" + esc(p.titulo) + " <span class=\"nota\">(" + brl(p.preco) + " avulso)</span></li>"; }).join("") + "</ul></div>" +
      '<div class="oferta__preco"><span class="oferta__soma">Comprando separado: <s>' + brl(soma) + "</s></span>" +
        '<span class="preco" data-preco="' + esc(pac.preco) + '">' + brl(pac.preco) + "</span>" +
        (eco > 0 ? '<span class="oferta__eco">Você economiza ' + brl(eco) + "</span>" : "") +
        (pode ? '<a class="btn btn--bloco" href="' + esc(pac.checkout) + '" rel="noopener" data-produto="' + esc(pac.id) + '">Quero o ' + esc(pac.titulo) + "</a>"
              : '<span class="btn btn--off btn--bloco" aria-disabled="true">Em breve</span>') + "</div>";
  }
  oferta("kit-lancamento", "kit");
  oferta("pacote-completo", "pacote");

  // ---------- CTA principal: primeiro produto à venda; sem nenhum, rola até a trilha ----------
  var primeiro = DEGRAUS.reduce(function (a, d) { return a.concat(d.ids); }, []).map(function (id) { return porId[id]; }).filter(vende)[0];
  var ctas = document.querySelectorAll("[data-cta-primeiro]");
  for (var j = 0; j < ctas.length; j++) {
    if (primeiro) { ctas[j].hidden = false; ctas[j].href = primeiro.checkout; ctas[j].textContent = primeiro.preco === 0 ? "Pegar o material grátis" : "Começar pelo " + primeiro.titulo; }
    else ctas[j].hidden = true;
  }

  // ---------- VSL: nada carrega antes do clique; sem autoplay com som ----------
  var caixa = document.getElementById("vsl");
  if (caixa) {
    var capa = caixa.querySelector(".vsl__capa");
    if (!VSL.src) {
      capa.disabled = true;
      capa.querySelector(".vsl__info").textContent = "Vídeo de apresentação em produção.";
    } else {
      if (VSL.capa) caixa.style.backgroundImage = "url(" + VSL.capa + ")";
      caixa.style.backgroundSize = "cover";
      capa.addEventListener("click", function () {
        var m;
        if (VSL.tipo === "mp4") {
          m = document.createElement("video");
          m.src = VSL.src; m.controls = true; m.playsInline = true; m.preload = "metadata";
        } else {
          m = document.createElement("iframe");
          m.src = VSL.src + (VSL.src.indexOf("?") > -1 ? "&" : "?") + "autoplay=1";
          m.title = "Vídeo de apresentação dos materiais Storymaker Oficial";
          m.allow = "autoplay; encrypted-media; picture-in-picture"; m.allowFullscreen = true;
        }
        caixa.replaceChild(m, capa);
        if (m.play) m.play().catch(function () {});
      });
    }
  }

  var ano = document.getElementById("ano");
  if (ano) ano.textContent = new Date().getFullYear();
})();
