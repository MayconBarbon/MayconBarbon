# Ajustes para a página `/materiais/` (Hostinger)

18/11/2026. A página está na Hostinger: aplique cada trecho no `materiais/index.html` (e no `materiais.css`). Faça uma cópia do arquivo antes.

Arquivos para subir na pasta `materiais/`:
- `vsl-storymaker-9x16-v3-web.mp4` (vídeo, 8 MB) — em `docs/video/vsl/`
- `capa-vsl-v3.jpg` (capa do player) — em `docs/video/vsl/`

---

## 1. Vídeo de apresentação com capa

**a) Link do vídeo.** A própria página já está preparada: em `materiais.js`, preencha a URL do vídeo:

```js
// em materiais.js, no objeto MATERIAIS
video: { url: "vsl-storymaker-9x16-v3-web.mp4" },
```

**b) Capa.** No fim do `materiais.css`, acrescente:

```css
/* capa da VSL: imagem e título, para o player não parecer vazio */
.video__capa {
  background: linear-gradient(180deg, rgba(27,26,31,.15), rgba(27,26,31,.55)), url("capa-vsl-v3.jpg") center / cover no-repeat;
}
```

E troque o texto do aviso, que hoje diz "Vídeo de apresentação em breve":

```html
<p class="video__aviso" id="video-aviso">Assista à apresentação · 1min31</p>
```

Se o vídeo não carregar, deixe o bloco escondido até resolver: acrescente `hidden` em `<div class="video" id="video" hidden>`.

---

## 2. Portfólio compacto (no lugar dos 4 blocos "Do simples ao grande")

**Remova** as quatro seções `<section class="pv" ...>` (de "Do simples ao grande · 1 de 4" até "4 de 4") e as faixas `<div class="frase">` que vinham logo depois de cada uma.

**Cole** esta seção logo **depois da trilha de produtos** (antes de "Quem está por trás do método"). Ela usa os mesmos botões `pv__card`, então o player de vídeo que a página já tem continua funcionando:

```html
<!-- PORTFÓLIO COMPACTO: coberturas reais, do simples ao grande -->
<section class="secao pvc" id="na-pratica" aria-labelledby="pvc-t">
  <div class="wrap">
    <p class="eyebrow">Do simples ao grande</p>
    <h2 id="pvc-t">O método aplicado em coberturas reais.</h2>
    <p class="secao__intro">De um pequeno negócio a um congresso de dois dias. Toque para assistir.</p>
    <div class="pvc__faixa">
      <button type="button" class="pv__card" data-video="https://www.instagram.com/p/DadDsgCJ8RL/" data-titulo="Pequeno negócio · 5 minutos">
        <img src="../assets/img/portfolio/artesa-flor-cachepo.jpg" alt="" loading="lazy" decoding="async" width="640" height="1136">
        <span class="pv__play" aria-hidden="true"></span>
        <span class="pv__rot">Pequeno negócio · 5 minutos<span class="sr">: assistir ao vídeo</span></span>
      </button>
      <button type="button" class="pv__card" data-video="https://drive.google.com/file/d/1te6QaN_UHfWkvrhM9ymQHC4IYRNbJo-C/view" data-titulo="Aniversário infantil · cobertura mobile">
        <img src="../assets/img/portfolio/aniversario-natan.jpg" alt="" loading="lazy" decoding="async" width="640" height="1136">
        <span class="pv__play" aria-hidden="true"></span>
        <span class="pv__rot">Aniversário infantil · cobertura mobile<span class="sr">: assistir ao vídeo</span></span>
      </button>
      <button type="button" class="pv__card" data-video="https://drive.google.com/file/d/1UwI8WC2gYbtXWOg1BK1brZL7M5h91pNz/view" data-titulo="Workshop de dois dias">
        <img src="../assets/img/portfolio/workshop-karla-corrente.jpg" alt="" loading="lazy" decoding="async" width="640" height="1136">
        <span class="pv__play" aria-hidden="true"></span>
        <span class="pv__rot">Workshop de dois dias<span class="sr">: assistir ao vídeo</span></span>
      </button>
      <button type="button" class="pv__card" data-video="https://drive.google.com/file/d/1DO8NUObWF1CBNUZWhwQBii-xsJ4UvoXI/view" data-titulo="Lançamento de livro">
        <img src="../assets/img/portfolio/lancamento-livro.jpg" alt="" loading="lazy" decoding="async" width="640" height="1136">
        <span class="pv__play" aria-hidden="true"></span>
        <span class="pv__rot">Lançamento de livro<span class="sr">: assistir ao vídeo</span></span>
      </button>
      <button type="button" class="pv__card" data-video="https://www.instagram.com/cide.brasil/reel/DZbVCdtMLhh/" data-titulo="Congresso de dois dias">
        <img src="../assets/img/portfolio/cide-2026.jpg" alt="" loading="lazy" decoding="async" width="640" height="1136">
        <span class="pv__play" aria-hidden="true"></span>
        <span class="pv__rot">Congresso de dois dias<span class="sr">: assistir ao vídeo</span></span>
      </button>
    </div>
    <p class="nota">Coberturas reais da equipe DocMe Comunicação. Cada evento tem o seu briefing, e os resultados não se repetem iguais.</p>
  </div>
</section>
```

No fim do `materiais.css`:

```css
/* portfólio compacto: uma faixa que rola para o lado no celular */
.pvc__faixa { display: grid; grid-auto-flow: column; grid-auto-columns: minmax(160px, 200px); gap: 14px; overflow-x: auto; padding: 6px 2px 14px; scroll-snap-type: x mandatory; -webkit-overflow-scrolling: touch; }
.pvc__faixa .pv__card { scroll-snap-align: start; }
@media (min-width: 900px) { .pvc__faixa { grid-auto-flow: row; grid-template-columns: repeat(5, 1fr); grid-auto-columns: auto; overflow: visible; } }
```

Os títulos ficaram genéricos, sem nome de cliente nem de criança. Se quiser manter "CIDE 2026" como prova social, troque só esse rótulo.

---

## 3. Aniversário infantil sem nome da criança

Se mantiver o bloco antigo em vez do compacto, troque nos dois lugares (`data-titulo` e `pv__rot`):

- de: `Aniversário infantil | Natan 6 anos`
- para: `Aniversário infantil · cobertura mobile`

Confirme com os pais a autorização para usar o vídeo em página de vendas.

---

## 4. "Quem está por trás do método", mais curto

Troque o parágrafo:

```html
<p>O método foi criado pelo fundador da DocMe Comunicação a partir de coberturas reais: congressos, casamentos, festas tradicionais e eventos com milhares de pessoas. A equipe aplica, erra, corrige e ensina o que funciona.</p>
```

por:

```html
<p>Coberturas reais de congressos, casamentos, festas e pequenos negócios. Método desenvolvido pela DocMe Comunicação.</p>
```

---

## 5. Pergunta frequente sem o Pacote Completo

Troque a pergunta e a resposta:

```html
<summary>Qual é a diferença entre os materiais individuais e o Kit Lançamento?</summary>
<p>Os materiais individuais são vendidos separadamente. O <b>Kit Lançamento</b> reúne quatro deles: Checklist de pré-produção, Modelo de contrato, Planilha de custos e horas e o e-book Do briefing à história.</p>
```

Quando o Pacote Completo for ativado, a pergunta volta com a descrição dele.

---

## 6. Frase das dores, menos definitiva

Na seção `#dores`, troque:

```html
<p class="secao__intro">Nada disso é falta de talento. É falta de método, e método se aprende. Ao lado de cada situação, o material que trata dela.</p>
```

por:

```html
<p class="secao__intro">Não é falta de talento. Na maioria das vezes, é falta de método, e método se aprende. Ao lado de cada situação, o material que trata dela.</p>
```

A VSL v3 já foi atualizada com a mesma frase.
