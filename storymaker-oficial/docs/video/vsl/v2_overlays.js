const { chromium } = require('playwright'); const fs = require('fs');
const plano = JSON.parse(fs.readFileSync('v2/plano.json', 'utf8'));
const css = `@import url('https://fonts.googleapis.com/css2?family=Inter:wght@700;800&family=Sora:wght@700;800&display=swap');
*{margin:0;box-sizing:border-box} html,body{background:transparent;color:#fff}
.tit{width:1080px;padding:40px 70px;text-align:center}
.tit .chip{display:inline-block;background:#c2410c;font:800 30px Inter;letter-spacing:.12em;text-transform:uppercase;padding:12px 26px;border-radius:999px;margin-bottom:26px}
.tit h1{font:800 118px/1.0 Sora;letter-spacing:-.03em;text-shadow:0 6px 30px rgba(0,0,0,.75),0 0 2px rgba(0,0,0,.6);-webkit-text-stroke:2px rgba(27,26,31,.25)}
.tit h1 em{font-style:normal;color:#ff8a4c}
.cap{width:1080px;height:360px;display:flex;align-items:center;justify-content:center;padding:0 60px;text-align:center}
.cap p{font:800 78px/1.12 Inter;letter-spacing:-.01em;text-transform:uppercase;text-shadow:0 5px 0 rgba(27,26,31,.9),0 0 28px rgba(0,0,0,.7);-webkit-text-stroke:3px #1b1a1f;paint-order:stroke fill}
.cap b{color:#ff8a4c;font-weight:800}
.card{width:1080px;height:1920px;background:radial-gradient(900px 700px at 80% 12%,rgba(255,138,76,.55),transparent 60%),radial-gradient(700px 600px at 10% 95%,rgba(194,65,12,.45),transparent 60%),#1b1a1f;padding:260px 90px;display:flex;flex-direction:column;align-items:center;text-align:center}
.card .logo{font:800 50px Sora} .card .logo b{color:#ff8a4c}
.card h1{font:800 120px/1.0 Sora;letter-spacing:-.03em;margin:130px 0 40px} .card h1 em{font-style:normal;color:#ff8a4c}
.card .sub{font:700 40px/1.35 Inter;color:#e4e2e8}
.card .seta{margin-top:70px;font:800 38px Inter;background:#c2410c;padding:24px 44px;border-radius:999px}
.card .ilu{margin-top:auto;font:700 26px Inter;color:#a9a7b0}`;
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
function tituloHTML(t) { const w = t.split(' '); const last = w.pop(); return esc(w.join(' ')) + (w.length ? ' ' : '') + '<em>' + esc(last) + '</em>'; }
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  async function shot(html, path, w, h, transp = true) {
    await p.setViewportSize({ width: w, height: h });
    await p.setContent(`<style>${css}</style>${html}`, { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
    const el = await p.$('body > *'); await el.screenshot({ path, omitBackground: transp });
  }
  for (const c of plano) {
    const n = String(c.n).padStart(2, '0');
    if (c.layout === 'CARD') {
      await shot(`<div class="card"><div class="logo">Storymaker <b>Oficial</b></div><h1>${tituloHTML(c.titulo)}</h1><p class="sub">Checklists, modelos, planilha, contrato e e-book para contar histórias com o celular.</p><div class="seta">Veja os materiais abaixo ↓</div><p class="ilu">Método desenvolvido pela DocMe Comunicação<br>Imagens ilustrativas de banco (Mixkit)</p></div>`, 'v2/card.png', 1080, 1920, false);
    } else {
      await shot(`<div class="tit"><span class="chip">${esc(c.bloco.replace(/^\d+\.\s*/, ''))}</span><h1>${tituloHTML(c.titulo)}</h1></div>`, `v2/t${n}.png`, 1080, 900);
    }
    for (let j = 0; j < c.caps.length; j++) {
      const cap = c.caps[j]; const ws = cap.texto.split(' ');
      const html = ws.map((w, i) => i === cap.hl ? `<b>${esc(w)}</b>` : esc(w)).join(' ');
      await shot(`<div class="cap"><p>${html}</p></div>`, `v2/l${n}_${j}.png`, 1080, 360);
    }
  }
  await b.close(); console.log('overlays v2 ok');
})();
