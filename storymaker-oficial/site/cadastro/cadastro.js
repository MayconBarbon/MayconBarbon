/* Cadastro de portfólios: formulário em etapas. Sem JavaScript, o formulário aparece inteiro e envia normalmente. */
(function () {
  "use strict";
  document.documentElement.classList.add("js");
  var form = document.getElementById("form"); if (!form) return;
  var etapas = [].slice.call(form.querySelectorAll(".etapa"));
  var i = 0;
  var btnV = document.getElementById("voltar"), btnA = document.getElementById("avancar"), btnE = document.getElementById("enviar");
  var barra = document.getElementById("barra"), n = document.getElementById("etapa-n"), caixaErros = document.getElementById("erros");
  document.getElementById("t").value = String(Date.now());

  function mostrar(k, foco) {
    i = k;
    etapas.forEach(function (e, j) { e.classList.toggle("ativa", j === i); });
    btnV.hidden = i === 0; btnA.hidden = i === etapas.length - 1;
    btnE.classList.toggle("mostra", i === etapas.length - 1);
    barra.style.width = ((i + 1) / etapas.length * 100) + "%";
    n.textContent = "Etapa " + (i + 1) + " de " + etapas.length + ": " + etapas[i].getAttribute("data-titulo");
    if (foco) { var f = etapas[i].querySelector("input,select,textarea"); if (f) f.focus(); }
  }

  function val(nome) { var el = form.elements[nome]; return el ? String(el.value || "").trim() : ""; }
  function marcados(nome) { return [].slice.call(form.querySelectorAll('input[name="' + nome + '"]:checked')); }
  function erro(lista, cond, msg, campo) {
    if (cond) { lista.push(msg); if (campo && form.elements[campo]) form.elements[campo].setAttribute("aria-invalid", "true"); }
  }

  function validar(k) {
    var e = [];
    etapas[k].querySelectorAll("[aria-invalid]").forEach(function (c) { c.removeAttribute("aria-invalid"); });
    if (k === 0) {
      erro(e, val("nome_profissional").length < 2, "Informe seu nome profissional.", "nome_profissional");
      erro(e, val("cidade").length < 2, "Informe sua cidade.", "cidade");
      erro(e, !val("uf"), "Escolha o estado.", "uf");
      erro(e, val("regioes").length < 2, "Conte em quais regiões ou cidades você aceita trabalhar.", "regioes");
    } else if (k === 1) {
      erro(e, !marcados("areas[]").length, "Escolha pelo menos uma área de atuação.");
      erro(e, !/^(https?:\/\/)?[^\s\/]+\.[^\s]+$/i.test(val("portfolio")), "Informe um link válido para o seu portfólio.", "portfolio");
      erro(e, !/^@?[A-Za-z0-9._]{1,30}$/.test(val("instagram").replace(/^(https?:\/\/)?(www\.)?instagram\.com\//i, "").replace(/\/$/, "")), "Informe o @ do seu Instagram profissional.", "instagram");
      erro(e, val("outra_rede") && !/^(https?:\/\/)?[^\s\/]+\.[^\s]+$/i.test(val("outra_rede")), "O link da outra rede não parece um endereço válido.", "outra_rede");
      erro(e, val("apresentacao").length < 20, "Escreva uma breve apresentação (pelo menos uma frase).", "apresentacao");
    } else if (k === 2) {
      var em = val("contato_email"), wa = val("contato_whatsapp").replace(/\D/g, "");
      erro(e, !em && !wa, "Informe um e-mail ou WhatsApp para contato.", "contato_email");
      erro(e, em && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(em), "O e-mail não parece válido.", "contato_email");
      erro(e, wa && (wa.length < 10 || wa.length > 13), "O WhatsApp precisa ter DDD e número.", "contato_whatsapp");
    } else if (k === 3) {
      erro(e, !form.elements.consent_analise.checked, "Para analisarmos o cadastro, marque a autorização A (análise do cadastro).");
      erro(e, form.elements.consent_publicacao.checked && !marcados("campos_publicaveis[]").length, "Escolha quais campos podem aparecer no diretório, ou desmarque a autorização B.");
      var canal = form.querySelector('input[name="canal_novidades"]:checked');
      erro(e, form.elements.consent_novidades.checked && !canal, "Escolha por onde quer receber novidades (autorização D).");
      if (canal && canal.value === "email") erro(e, !val("contato_email"), "Para receber novidades por e-mail, volte à etapa 3 e informe seu e-mail.");
      if (canal && canal.value === "whatsapp") erro(e, !val("contato_whatsapp"), "Para receber novidades por WhatsApp, volte à etapa 3 e informe seu WhatsApp.");
    }
    return e;
  }

  function mostrarErros(lista) {
    if (!lista.length) { caixaErros.hidden = true; caixaErros.innerHTML = ""; return; }
    caixaErros.innerHTML = "<b>Confira antes de continuar:</b><ul>" + lista.map(function (x) { var li = document.createElement("li"); li.textContent = x; return li.outerHTML; }).join("") + "</ul>";
    caixaErros.hidden = false; caixaErros.focus && caixaErros.setAttribute("tabindex", "-1"); caixaErros.focus();
  }

  btnA.addEventListener("click", function () {
    var e = validar(i); mostrarErros(e); if (e.length) return;
    mostrar(i + 1, true); form.scrollIntoView({ behavior: "smooth", block: "start" });
  });
  btnV.addEventListener("click", function () { mostrarErros([]); mostrar(i - 1, true); });

  // Opções que só aparecem quando a autorização é marcada
  form.querySelectorAll("[data-abre]").forEach(function (cb) {
    var alvo = document.getElementById(cb.getAttribute("data-abre"));
    function sync() { alvo.hidden = !cb.checked; if (!cb.checked) alvo.querySelectorAll("input").forEach(function (x) { x.checked = false; }); }
    cb.addEventListener("change", sync); sync();
  });

  var ta = form.elements.apresentacao, conta = document.querySelector('[data-conta="apresentacao"]');
  ta.addEventListener("input", function () { conta.textContent = ta.value.length; });

  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    for (var k = 0; k < etapas.length; k++) { var e = validar(k); if (e.length) { mostrar(k, false); mostrarErros(e); return; } }
    btnE.disabled = true; btnE.textContent = "Enviando…";
    fetch(form.action, { method: "POST", body: new FormData(form), headers: { Accept: "application/json" }, credentials: "same-origin" })
      .then(function (r) { return r.json().catch(function () { return { ok: false, mensagem: "Não conseguimos salvar seu cadastro agora. Tente novamente em alguns minutos." }; }); })
      .then(function (res) {
        if (res.ok) {
          form.hidden = true; document.querySelector(".cad-progresso").hidden = true; n.hidden = true; caixaErros.hidden = true;
          var ok = document.getElementById("ok"); ok.hidden = false; ok.focus();
        } else {
          mostrarErros(res.erros && res.erros.length ? res.erros : [res.mensagem]);
        }
      })
      .catch(function () { mostrarErros(["Sem conexão no momento. Seus dados continuam no formulário: tente enviar de novo."]); })
      .then(function () { btnE.disabled = false; btnE.textContent = "Enviar cadastro"; });
  });

  form.addEventListener("change", function () { if (!caixaErros.hidden) mostrarErros([]); });
  mostrar(0, false);
})();
