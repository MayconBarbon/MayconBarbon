// VSL v3 — renderização quadro a quadro das animações tipográficas (estilo da referência:
// digitação com cursor, troca de palavras, lista que rola, cortes de cor, guias geométricas).
// Saída: v3/f<cena>/%05d.png (transparente nas cenas com vídeo; opaco nas cenas tipográficas).
const { chromium } = require('playwright'); const fs = require('fs');
const plano = JSON.parse(fs.readFileSync('v3/plano.json', 'utf8'));
const FPS = 30;
const html = `<!doctype html><html><head><style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@500&family=Sora:wght@700;800&display=swap');
*{margin:0;box-sizing:border-box} html,body{width:1080px;height:1920px;overflow:hidden;background:transparent}
#s{position:absolute;inset:0;font-family:Inter,sans-serif}
.lbl{position:absolute;top:150px;font:500 22px 'IBM Plex Mono',monospace;letter-spacing:.14em;text-transform:uppercase;opacity:.75}
.lbl.l{left:90px}.lbl.r{right:90px}
.cur{display:inline-block;width:7px;height:.95em;background:#e7570c;vertical-align:-.1em;margin-left:6px}
.tit{position:absolute;left:70px;right:70px;top:330px;text-align:center;color:#fff;font:500 96px/1.04 Inter;letter-spacing:-.035em;text-shadow:0 4px 28px rgba(27,26,31,.85),0 1px 3px rgba(27,26,31,.7)}
.tit b{font-weight:800;color:#fff}
.cap{position:absolute;left:70px;right:70px;top:1180px;text-align:center;color:#fff;font:600 70px/1.12 Inter;letter-spacing:-.025em;text-shadow:0 4px 26px rgba(27,26,31,.95),0 2px 4px rgba(27,26,31,.9)}
.cap b{font-weight:800;color:#e7570c}
.cap span{display:inline-block}
.tile{position:absolute;left:60px;font:500 24px 'IBM Plex Mono',monospace;letter-spacing:.16em;color:#fff;background:rgba(27,26,31,.72);padding:10px 16px;border-radius:6px}
.mid{position:absolute;left:80px;right:80px;top:0;bottom:0;display:flex;align-items:center;justify-content:center;text-align:center}
.frase{font:500 104px/1.05 Inter;letter-spacing:-.04em}
.frase b{font-weight:800}
.mark{display:inline-block;width:20px;height:20px;background:#e7570c;position:relative;top:-.62em;margin-left:6px;vertical-align:baseline}
.wheel{position:absolute;left:0;right:0;top:0;bottom:0}
.wi{position:absolute;left:470px;white-space:nowrap;font:500 62px Inter;letter-spacing:-.03em}
.wl{position:absolute;left:90px;font:600 52px Inter;letter-spacing:-.02em}
.dot{display:inline-block;width:14px;height:14px;border-radius:50%;background:#e7570c;margin-left:14px;vertical-align:.25em}
.logo{font:800 96px Sora;letter-spacing:-.03em}
.logo i{font-style:normal;color:#e7570c}
.btn{display:inline-block;margin-top:56px;font:700 40px Inter;color:#fff;background:#c2410c;padding:24px 46px;border-radius:999px}
.mini{position:absolute;left:0;right:0;bottom:120px;text-align:center;font:500 18px Inter;color:#8b8a91}
</style></head><body><div id="s"></div></body></html>`;

async function main() {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.setContent(html, { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
  await p.evaluate(() => {
    const OFF = '#ece8e3', GRA = '#1b1a1f', ORA = '#e7570c', TXT = '#2b2a30';
    const S = document.getElementById('s');
    const ease = x => 1 - Math.pow(1 - Math.min(1, Math.max(0, x)), 3);
    const fmt = s => s.replace(/\*\*(.+?)\*\*/g, '<b>$1</b>');
    function typed(md, t, cps = 26) {            // digitação: revela caracteres (mantendo o negrito)
      const plain = md.replace(/\*\*/g, ''); const n = Math.min(plain.length, Math.floor(t * cps));
      let out = '', k = 0, bold = false;
      for (let i = 0; i < md.length && k < n; i++) {
        if (md.startsWith('**', i)) { out += bold ? '</b>' : '<b>'; bold = !bold; i++; continue; }
        out += md[i]; k++;
      }
      if (bold) out += '</b>';
      const blink = n >= plain.length ? (Math.floor(t * 2.2) % 2 === 0) : true;
      return out + `<span class="cur" style="opacity:${blink ? 1 : 0}"></span>`;
    }
    function caption(c, t) {
      const cap = c.caps.find(x => t >= x.ini && t < x.fim); if (!cap) return '';
      const ws = cap.texto.split(' '); const lt = t - cap.ini;
      return '<div class="cap">' + ws.map((w, i) => {
        const a = ease((lt - i * 0.06) / 0.16); const y = (1 - a) * 26;
        const inner = i === cap.hl ? `<b>${w}</b>` : w;
        return `<span style="opacity:${a};transform:translateY(${y}px)">${inner}</span>`;
      }).join(' ') + '</div>';
    }
    function lbls(l, r, cor) { return `<div class="lbl l" style="color:${cor}">${l}</div><div class="lbl r" style="color:${cor}">${r}</div>`; }
    window.draw = (c, t) => {
      const d = c.dur; let h = '';
      if (c.tipo === 'FOOT') {
        const T = c.titulo_fim;
        if (t < T) { const fo = t > T - 0.2 ? (T - t) / 0.2 : 1; h += `<div class="tit" style="opacity:${fo}">${typed(c.tituloMd, t)}</div>`; }
        (c.rotulos || []).forEach((r, k) => { const a = ease((t - 0.3 - k * 0.12) / 0.25); h += `<div class="tile" style="top:${[60, 684, 1308][k]}px;opacity:${a}">${r}</div>`; });
        h += caption(c, t); S.style.background = 'transparent'; S.innerHTML = h; return;
      }
      if (c.tipo === 'WHEEL') {   // cena 2: "O que gravar primeiro?" + lista que rola
        S.style.background = OFF;
        const items = c.itens, step = (d - 1.0) / items.length, tt = Math.max(0, t - 0.9);
        const pos = Math.min(items.length - 1, tt / step); const idx = Math.round(pos);
        h += lbls('Storymaker', '01 / 04', TXT);
        h += `<div class="mid" style="align-items:flex-start;padding-top:420px"><div class="frase" style="color:${TXT};font-size:84px">${typed(c.tituloMd, t, 30)}</div></div>`;
        h += `<div class="wl" style="top:${1020 - 32}px;color:${TXT};opacity:${ease((t - 0.7) / 0.3)}">gravar<span class="dot"></span></div>`;
        items.forEach((it, i) => {
          const dy = (i - pos) * 96; const on = i === idx; const al = Math.max(0, 1 - Math.abs(i - pos) * 0.32) * ease((t - 0.7) / 0.3);
          h += `<div class="wi" style="top:${1020 - 40 + dy}px;opacity:${al};color:${on ? ORA : TXT};font-weight:${on ? 700 : 400};transform:rotate(${(i - pos) * -2}deg)">${it}</div>`;
        });
        S.innerHTML = h; return;
      }
      if (c.tipo === 'SWAP') {    // troca de frases em fundos alternados
        const fs = c.frases, n = fs.length, seg = d / n, i = Math.min(n - 1, Math.floor(t / seg)), lt = t - i * seg;
        const bgs = [OFF, GRA, ORA, OFF], bg = bgs[i % bgs.length]; S.style.background = bg;
        const cor = bg === OFF ? TXT : '#fff';
        const a = ease(lt / 0.18), y = (1 - a) * 40;
        h += lbls(c.rotulo, `${String(i + 1).padStart(2, '0')} / ${String(n).padStart(2, '0')}`, cor);
        h += `<div class="mid"><div class="frase" style="color:${cor};opacity:${a};transform:translateY(${y}px)">${fmt(fs[i])}<span class="mark" style="background:${bg === ORA ? '#fff' : ORA};transform:rotate(${lt * 90}deg)"></span></div></div>`;
        S.innerHTML = h; return;
      }
      if (c.tipo === 'LIST') {    // cena 12: lista de materiais em fundo grafite
        S.style.background = GRA;
        const items = c.itens, step = (d - 0.6) / items.length, tt = Math.max(0, t - 0.4);
        const pos = Math.min(items.length - 1, tt / step), idx = Math.round(pos);
        h += lbls('Materiais', `${String(idx + 1).padStart(2, '0')} / ${String(items.length).padStart(2, '0')}`, '#d9d7de');
        h += `<div class="wl" style="top:${960 - 32}px;color:#fff;left:70px;font-size:46px">materiais<span class="dot"></span></div>`;
        items.forEach((it, i) => {
          const dy = (i - pos) * 92, on = i === idx, al = Math.max(0, 1 - Math.abs(i - pos) * 0.3);
          h += `<div class="wi" style="left:400px;top:${960 - 40 + dy}px;opacity:${al};color:${on ? ORA : '#d9d7de'};font-weight:${on ? 700 : 400};font-size:${on ? 66 : 56}px;transform:rotate(${(i - pos) * -2.5}deg)">${it}</div>`;
        });
        // círculo-guia girando
        h += `<svg style="position:absolute;left:340px;top:540px" width="840" height="840"><circle cx="420" cy="420" r="400" fill="none" stroke="rgba(236,232,227,.14)" stroke-width="2"/><circle cx="${420 + 400 * Math.cos(t)}" cy="${420 + 400 * Math.sin(t)}" r="7" fill="${ORA}"/></svg>`;
        S.innerHTML = h; return;
      }
      if (c.tipo === 'FINAL') {   // cortes rápidos de cor + logo com guias + convite
        const flash = 1.6, cores = [ORA, OFF, GRA, ORA, OFF, GRA, ORA, OFF, GRA, ORA, OFF, GRA];
        if (t < flash) {
          const k = Math.floor(t / 0.133) % cores.length, bg = cores[k]; S.style.background = bg;
          const cor = bg === OFF ? TXT : '#fff', sz = [96, 60, 120, 76][k % 4];
          h = `<div class="mid"><div class="logo" style="color:${cor};font-size:${sz}px">Storymaker <i style="color:${bg === ORA ? '#fff' : ORA}">Oficial</i></div></div>`;
          S.innerHTML = h; return;
        }
        const lt = t - flash; S.style.background = GRA;
        const g = ease(lt / 0.9);
        h += `<svg style="position:absolute;inset:0" width="1080" height="1920">
          <line x1="540" y1="${520 - 300 * g}" x2="540" y2="${520 + 300 * g}" stroke="rgba(236,232,227,.18)" stroke-width="2"/>
          <line x1="${540 - 420 * g}" y1="620" x2="${540 + 420 * g}" y2="620" stroke="rgba(236,232,227,.18)" stroke-width="2"/>
          <circle cx="540" cy="620" r="330" fill="none" stroke="rgba(231,87,12,.5)" stroke-width="2" stroke-dasharray="2075" stroke-dashoffset="${2075 * (1 - g)}"/></svg>`;
        h += lbls('Storymaker Oficial', '2026', '#d9d7de');
        h += `<div class="mid" style="top:440px;bottom:auto;height:360px"><div class="logo" style="color:#fff;font-size:${96 - 20 * g}px">Storymaker <i>Oficial</i></div></div>`;
        const a2 = ease((lt - 0.5) / 0.3), a3 = ease((lt - 1.1) / 0.3), a4 = ease((lt - 1.8) / 0.3);
        h += `<div style="position:absolute;left:80px;right:80px;top:1020px;text-align:center">
          <div class="frase" style="color:#fff;font-size:92px;opacity:${a2};transform:translateY(${(1 - a2) * 30}px)">Escolha por onde <b style="color:${ORA}">começar.</b></div>
          <div style="opacity:${a3};font:500 40px/1.4 Inter;color:#d9d7de;margin-top:34px">Compra e entrega pela Kiwify.</div>
          <div class="btn" style="opacity:${a4};transform:scale(${0.9 + 0.1 * a4})">Veja os materiais abaixo ↓</div></div>`;
        h += `<div class="mini">Imagens ilustrativas · Mixkit</div>`;
        S.innerHTML = h; return;
      }
    };
  });
  const so = process.argv[2] ? process.argv[2].split(',').map(Number) : null;
  for (const c of plano) {
    if (so && !so.includes(c.n)) continue;
    const dir = `v3/f${String(c.n).padStart(2, '0')}`; fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
    const N = Math.round(c.dur * FPS);
    for (let f = 0; f < N; f++) {
      await p.evaluate(([c, t]) => window.draw(c, t), [c, f / FPS]);
      await p.screenshot({ path: `${dir}/${String(f).padStart(5, '0')}.png`, omitBackground: c.tipo === 'FOOT' });
    }
    console.log('cena', c.n, c.tipo, N, 'quadros');
  }
  await b.close();
}
main();
