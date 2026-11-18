const { chromium } = require('playwright'); const fs = require('fs');
const cenas = JSON.parse(fs.readFileSync('cenas.json', 'utf8'));
const css = `@import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700&family=Sora:wght@700;800&display=swap');
*{margin:0;box-sizing:border-box} html,body{width:1080px;height:1920px;background:transparent;font-family:Inter,sans-serif;color:#fff}
.marca{position:absolute;top:110px;left:0;right:0;text-align:center;font:700 36px Sora;text-shadow:0 2px 12px rgba(0,0,0,.5)} .marca b{color:#ff8a4c}
.topo{position:absolute;top:250px;left:90px;right:90px;text-align:center}
.chip{display:inline-block;background:#c2410c;font:700 26px Inter;letter-spacing:.12em;text-transform:uppercase;padding:10px 22px;border-radius:999px;margin-bottom:22px}
h1{font:800 72px/1.06 Sora;letter-spacing:-.02em;text-shadow:0 3px 18px rgba(0,0,0,.55)}
.leg{position:absolute;left:90px;right:90px;top:1250px;text-align:center}
.leg span{display:inline;font:700 54px/1.42 Inter;background:rgba(27,26,31,.86);box-decoration-break:clone;-webkit-box-decoration-break:clone;padding:6px 18px;border-radius:14px}
.ilu{position:absolute;left:0;right:0;top:1590px;text-align:center;font:500 24px Inter;color:rgba(255,255,255,.7)}
.vert .topo{top:260px} .vert .grad{position:absolute;inset:0;background:linear-gradient(to bottom,rgba(27,26,31,.7),rgba(27,26,31,0) 32%,rgba(27,26,31,0) 55%,rgba(27,26,31,.75))}
.fim{width:1080px;height:1920px;background:radial-gradient(900px 700px at 80% 15%,rgba(255,150,80,.5),transparent 60%),#1b1a1f;padding:300px 100px;display:flex;flex-direction:column;align-items:center;text-align:center}
.fim .logo{font:700 44px Sora} .fim .logo b{color:#ff8a4c}
.fim h1{font-size:96px;margin:120px 0 40px} .fim p{font:600 40px/1.4 Inter;color:#d9d7de}
.fim .seta{margin-top:70px;font:700 34px Inter;background:#c2410c;padding:22px 40px;border-radius:999px}
.fim .assina{margin-top:auto;font:600 30px Inter;color:#d9d7de}
.fim .ilu2{margin-top:14px;font:500 24px Inter;color:#a9a7b0}`;
const VERT = new Set([22738, 4953, 34408]);
const esc = s => s.replace(/&/g,'&amp;').replace(/</g,'&lt;');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  fs.mkdirSync('ov', { recursive: true });
  for (const c of cenas) {
    const chip = c.bloco.replace(/^\d+\.\s*/, '');
    for (let k = 0; k < c.legendas.length; k++) {
      const leg = c.legendas[k].texto; let html;
      if (c.clip === null) {
        html = `<div class="fim"><div class="logo">Storymaker <b>Oficial</b></div><h1>${esc(c.titulo)}</h1><p>Checklists, modelos, planilha e e-book para contar histórias com o celular.</p><div class="seta">Veja os materiais abaixo ↓</div><div class="assina">Método desenvolvido pela DocMe Comunicação.<div class="ilu2">Imagens ilustrativas · banco Mixkit</div></div></div><div class="leg" style="top:1380px"><span>${esc(leg)}</span></div>`;
      } else {
        html = `<div class="${VERT.has(c.clip) ? 'vert' : ''}" style="position:absolute;inset:0">${VERT.has(c.clip) ? '<div class="grad"></div>' : ''}<div class="marca">Storymaker <b>Oficial</b></div><div class="topo"><span class="chip">${esc(chip)}</span><h1>${esc(c.titulo)}</h1></div><div class="leg"><span>${esc(leg)}</span></div><div class="ilu">Imagem ilustrativa · Mixkit</div></div>`;
      }
      await p.setContent(`<style>${css}</style>${html}`, { waitUntil: 'networkidle' });
      await p.evaluate(() => document.fonts.ready);
      await p.screenshot({ path: `ov/c${c.n}_${k}.png`, omitBackground: c.clip !== null });
    }
  }
  await b.close(); console.log('overlays ok');
})();
