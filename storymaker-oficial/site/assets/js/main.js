(function () {
  "use strict";
  var C = window.SITE_CONFIG || {}, CASES = window.CASES || [];
  var $ = function (s, el) { return (el || document).querySelector(s); };

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  // texto ou marcador visível de conteúdo faltando
  function txt(v, falta) {
    if (v && String(v).trim()) {
      return esc(v).replace(/\[(PREENCHER|CONFIRMAR)[^\]]*\]/g, function (m) { return '<mark class="falta">' + m + "</mark>"; });
    }
    return '<mark class="falta">[PREENCHER' + (falta ? ": " + esc(falta) : "") + "]</mark>";
  }
  function brl(n) { return n === 0 ? "Grátis" : n.toLocaleString("pt-BR", { style: "currency", currency: "BRL" }); }
  function num(n) { return n.toLocaleString("pt-BR"); }
  function slugCat(c) { return c.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/\s+/g, "-"); }

  window.SM = { esc: esc, txt: txt, brl: brl, num: num, slugCat: slugCat };

  // ---------- tema ----------
  var temaUrl = new URLSearchParams(location.search).get("tema");
  var tema = (temaUrl === "laranja" || temaUrl === "grafite") ? temaUrl : (C.tema || "grafite");
  document.documentElement.setAttribute("data-tema", tema);

  // ---------- comum ----------
  document.querySelectorAll("[data-assinatura]").forEach(function (el) { el.textContent = C.assinatura || ""; });
  document.querySelectorAll("[data-ano]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  var btn = $(".menu-btn"), menu = $("#menu");
  if (btn && menu) {
    btn.addEventListener("click", function () {
      var open = btn.getAttribute("aria-expanded") === "true";
      btn.setAttribute("aria-expanded", String(!open));
      menu.classList.toggle("aberto", !open);
    });
    menu.addEventListener("click", function (e) {
      if (e.target.tagName === "A") { btn.setAttribute("aria-expanded", "false"); menu.classList.remove("aberto"); }
    });
  }
  var topo = $("#topo");
  if (topo) {
    var onScroll = function () { topo.classList.toggle("rolou", window.scrollY > 20); };
    window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
  }

  // ---------- portfólio ----------
  function cardCase(c) {
    var thumb = c.thumb
      ? '<img src="' + esc(c.thumb) + '" alt="" loading="lazy">'
      : '<div class="thumb-ph" data-cat="' + slugCat(c.categoria) + '"><span>' + esc(c.titulo) + "</span></div>";
    return '<a class="case" href="case.html?id=' + encodeURIComponent(c.id) + '" data-cat="' + esc(c.categoria) + '">' +
      '<div class="case__thumb">' + thumb + (c.desafio ? '<span class="case__flag">Desafio</span>' : "") + (c.nivelBasico ? '<span class="case__flag case__flag--basico">Feito na hora</span>' : "") + (c.instagram && c.instagram.length ? '<span class="case__flag case__flag--ig">No Instagram</span>' : "") + "</div>" +
      '<div class="case__body"><p class="case__meta">' + esc(c.categoria) + (c.ano ? " · " + esc(String(c.ano).replace(/\s*\[.*\]/, "")) : "") + "</p>" +
      "<h3>" + esc(c.titulo) + "</h3>" +
      (c.chamada ? "<p>" + txt(c.chamada) + "</p>" : "") + "</div></a>";
  }

  var grid = $("#grid-cases"), filtros = $("#filtros");
  if (grid && filtros) {
    var cats = ["Todos"].concat(window.CATEGORIAS || []);
    filtros.innerHTML = cats.map(function (c, i) {
      return '<button type="button" class="chip" aria-pressed="' + (i === 0) + '" data-f="' + esc(c) + '">' + esc(c) + "</button>";
    }).join("");
    var render = function (f) {
      var lista = CASES.filter(function (c) { return f === "Todos" || c.categoria === f; });
      grid.innerHTML = lista.length ? lista.map(cardCase).join("") : '<p class="vazio">Nenhum trabalho nesta categoria ainda.</p>';
    };
    filtros.addEventListener("click", function (e) {
      var b = e.target.closest(".chip"); if (!b) return;
      filtros.querySelectorAll(".chip").forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
      render(b.dataset.f);
    });
    render("Todos");
  }

  // ---------- no dia x depois ----------
  var compara = $("#compara");
  if (compara) {
    var ref = CASES.filter(function (c) { return c.comparativo; })[0];
    if (ref) {
      var max = Math.max(ref.comparativo.dia, ref.comparativo.depois);
      var bar = function (rot, sub, v, cls) {
        return '<div class="cmp ' + cls + '"><div class="cmp__top"><span class="cmp__rot">' + rot + '</span><span class="cmp__v">' + num(v) + '</span></div>' +
          '<div class="cmp__track"><div class="cmp__fill" style="--w:' + (v / max * 100).toFixed(1) + '%"></div></div><p>' + sub + "</p></div>";
      };
      compara.innerHTML =
        bar("No dia", "Vídeo publicado no encerramento do evento. Visualizações.", ref.comparativo.dia, "cmp--dia") +
        bar("Depois", "Aftermovie publicado uma semana depois. Visualizações.", ref.comparativo.depois, "cmp--depois") +
        '<a class="link-seta" href="case.html?id=' + encodeURIComponent(ref.id) + '">Ver o case completo</a>';
    }
  }

  // ---------- desafios ----------
  var ld = $("#lista-desafios");
  if (ld) {
    ld.innerHTML = CASES.filter(function (c) { return c.desafio; }).map(function (c) {
      return '<article class="desafio"><p class="case__meta">' + esc(c.categoria) + "</p><h3>" + esc(c.chamada || c.titulo) + "</h3>" +
        '<dl><dt>O que aconteceu</dt><dd>' + txt(c.mudou) + "</dd><dt>Como a equipe resolveu</dt><dd>" + txt(c.reacao) +
        '</dd><dt>Aprendizado</dt><dd class="aprendizado">' + txt(c.aprendizado) + "</dd></dl>" +
        '<a class="link-seta" href="case.html?id=' + encodeURIComponent(c.id) + '">' + esc(c.titulo) + ": case completo</a></article>";
    }).join("");
  }

  // ---------- equipe ----------
  var le = $("#lista-equipe");
  if (le) {
    le.innerHTML = (window.EQUIPE || []).map(function (p) {
      var media = p.video
        ? (/\.(mp4|webm)$/i.test(p.video)
          ? '<video controls preload="none" playsinline' + (p.poster ? ' poster="' + esc(p.poster) + '"' : "") + ' src="' + esc(p.video) + '"></video>'
          : '<a class="video-link" href="' + esc(p.video) + '" target="_blank" rel="noopener">Assistir depoimento</a>')
        : '<div class="video-ph"><span class="play" aria-hidden="true"></span><mark class="falta">[PREENCHER: vídeo]</mark></div>';
      return '<article class="pessoa">' + media + "<h3>" + esc(p.nome) + "</h3>" +
        (p.funcao ? '<p class="case__meta">' + esc(p.funcao) + "</p>" : "") +
        (p.frase ? "<blockquote>“" + esc(p.frase) + "”</blockquote>" : "") +
        (p.nota ? '<p class="pessoa__nota">' + esc(p.nota) + "</p>" : "") + "</article>";
    }).join("");
  }

  // ---------- elogios ----------
  var lel = $("#lista-elogios");
  if (lel) {
    var el = window.ELOGIOS || [];
    lel.innerHTML = el.length
      ? el.map(function (e) { return '<figure class="print"><img src="' + esc(e.imagem) + '" alt="' + esc(e.alt) + '" loading="lazy"><figcaption>' + esc(e.evento || "") + "</figcaption></figure>"; }).join("")
      : [1, 2, 3, 4].map(function () { return '<figure class="print print--ph"><mark class="falta">[PREENCHER: print de cliente]</mark></figure>'; }).join("");
  }

  // ---------- produtos ----------
  var prods = (C.produtos || []).filter(function (p) { return p.ativo; });
  var byId = {}; (C.produtos || []).forEach(function (p) { byId[p.id] = p; });
  function botao(link, rotulo) {
    return link
      ? '<a class="btn" href="' + esc(link) + '" target="_blank" rel="noopener">' + rotulo + "</a>"
      : '<span class="btn btn--off" aria-disabled="true">Em breve</span>';
  }

  var lp = $("#lista-pacotes");
  if (lp) {
    lp.innerHTML = (C.pacotes || []).filter(function (p) { return p.ativo; }).map(function (p, i) {
      var itens = p.itens.map(function (id) { return byId[id]; }).filter(Boolean);
      var soma = itens.reduce(function (a, x) { return a + x.preco; }, 0);
      var eco = soma - p.preco, pct = soma ? Math.round(eco / soma * 100) : 0;
      return '<article class="pacote' + (i === 0 ? " pacote--top" : "") + '">' +
        '<div class="pacote__head"><h3>' + esc(p.titulo) + "</h3><p>" + esc(p.resumo) + "</p></div>" +
        '<ul class="pacote__itens">' + itens.map(function (x) { return "<li>" + esc(x.titulo) + "</li>"; }).join("") + "</ul>" +
        '<div class="pacote__preco">' +
        (eco > 0 ? '<p class="pacote__soma">Avulsos somam <s>' + brl(soma) + "</s></p>" : "") +
        '<p class="preco">' + brl(p.preco) + "</p>" +
        (eco > 0 ? '<p class="pacote__eco">Você economiza ' + brl(eco) + " (" + pct + "%)</p>" : "") +
        (p.beneficio ? '<p class="pacote__ben">' + esc(p.beneficio) + "</p>" : "") +
        botao(p.checkout, "Comprar pacote") + "</div></article>";
    }).join("");
  }

  var lprod = $("#lista-produtos"), fprod = $("#filtros-produtos");
  if (lprod) {
    var grupos = ["Todos", "E-books", "Checklists e guias", "Modelos e ferramentas"];
    var grupoDe = function (t) { return t === "E-book" ? "E-books" : (t === "Checklist" || t === "Guia") ? "Checklists e guias" : "Modelos e ferramentas"; };
    var renderP = function (g) {
      lprod.innerHTML = prods.filter(function (p) { return g === "Todos" || grupoDe(p.tipo) === g; }).map(function (p) {
        return '<article class="produto' + (p.destaque ? " produto--destaque" : "") + '">' +
          '<p class="produto__tipo">' + esc(p.tipo) + (p.destaque ? ' · <b>Comece por aqui</b>' : "") + "</p>" +
          "<h3>" + esc(p.titulo) + "</h3><p>" + esc(p.resumo) + "</p>" +
          '<div class="produto__pe"><span class="preco preco--sm">' + brl(p.preco) + "</span>" + botao(p.checkout, p.preco === 0 ? "Baixar grátis" : "Comprar") + "</div></article>";
      }).join("");
    };
    if (fprod) {
      fprod.innerHTML = grupos.map(function (g, i) { return '<button type="button" class="chip" aria-pressed="' + (i === 0) + '" data-f="' + g + '">' + g + "</button>"; }).join("");
      fprod.addEventListener("click", function (e) {
        var b = e.target.closest(".chip"); if (!b) return;
        fprod.querySelectorAll(".chip").forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
        renderP(b.dataset.f);
      });
    }
    renderP("Todos");
  }
})();
