const { chromium } = require('playwright');
const shots = [
  ['Fim de ano', 'Natal e Réveillon: o que gravar com o celular', true],
  ['Natal', 'A preparação em casa'],
  ['Natal', 'A ceia sendo servida'],
  ['Natal', 'Os detalhes da mesa'],
  ['Natal', 'O brinde de quem você ama'],
  ['Réveillon', 'Amigos e pessoas próximas'],
  ['Réveillon', 'O brinde da virada'],
  ['Réveillon', 'Os fogos e quem está com você'],
];
const css = `@import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700&family=Sora:wght@700;800&display=swap');
*{margin:0;box-sizing:border-box} html,body{width:1080px;height:1920px;background:transparent;font-family:Inter,sans-serif}
.marca{position:absolute;top:70px;left:70px;font:700 34px Sora;color:#fff;text-shadow:0 2px 12px rgba(0,0,0,.45)} .marca b{color:#ff8a4c}
.grad{position:absolute;left:0;right:0;bottom:0;height:900px;background:linear-gradient(to top,rgba(27,26,31,.88),rgba(27,26,31,0))}
.txt{position:absolute;left:70px;right:70px;bottom:230px}
.chip{display:inline-block;background:#c2410c;color:#fff;font:700 30px Inter;letter-spacing:.12em;text-transform:uppercase;padding:12px 24px;border-radius:999px;margin-bottom:26px}
h1{font:800 96px/1.04 Sora;color:#fff;letter-spacing:-.02em} h1.hook{font-size:104px}
.ilu{position:absolute;right:70px;bottom:120px;font:500 26px Inter;color:rgba(255,255,255,.72)}
.fim{width:1080px;height:1920px;background:radial-gradient(900px 700px at 80% 15%,rgba(255,150,80,.55),transparent 60%),#e7570c;padding:160px 90px;display:flex;flex-direction:column}
.fim .sel{font:700 30px Inter;letter-spacing:.14em;text-transform:uppercase;color:#1f1e24;margin-top:auto}
.fim h1{font-size:120px;margin:24px 0 36px} .fim p{font:600 44px/1.35 Inter;color:#1f1e24}
.fim .assina{margin-top:auto;font:600 32px Inter;color:#1f1e24} .fim .ilu2{font:500 26px Inter;color:#1f1e24;margin-top:18px;opacity:.85}`;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  for (let i = 0; i < shots.length; i++) {
    const [chip, t, hook] = shots[i];
    await p.setContent(`<style>${css}</style><div class="marca">Storymaker <b>Oficial</b></div><div class="grad"></div><div class="txt"><span class="chip">${chip}</span><h1 class="${hook ? 'hook' : ''}">${t}</h1></div><div class="ilu">Imagem ilustrativa</div>`, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: `ov${i + 1}.png`, omitBackground: true });
  }
  await p.setContent(`<style>${css}</style><div class="fim"><p class="sel">Storymaker Oficial · Material novo</p><h1>Roteiro de fim de ano</h1><p>Confraternização, Natal e Réveillon: o que gravar, em que ordem e como entregar no mesmo dia.</p><div class="assina">Método desenvolvido pela DocMe Comunicação.<div class="ilu2">Imagens ilustrativas · banco gratuito Mixkit</div></div></div>`, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: 'fim.png' });
  await b.close(); console.log('overlays ok');
})();
