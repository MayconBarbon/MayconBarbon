// Carrosséis Storymaker Oficial — 3 × 10 slides, 1080×1350 (4:5).
// Fotos: quadros de clipes Mixkit (Mixkit Stock Video Free License). Textos: aprovados pelo fundador.
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const OUT = process.argv[2];
const F = id => 'data:image/jpeg;base64,' + fs.readFileSync(path.join(__dirname, 'fotos', id + '.jpg')).toString('base64');

// tipos: CAPA (foto + título), FOTO (foto + texto), TIPO (fundo sólido: off | gra | ora), GRADE (4 faixas), CTA
const C = {
 'c1-quem-contou-a-historia': [
  { t: 'CAPA', foto: '51529', pos: '50% 40%', titulo: 'O evento aconteceu. Mas quem contou a <b>história?</b>', txt: 'O evento estava acontecendo. As redes já estavam cheias de imagens. Mas a versão da organização ainda não tinha aparecido.' },
  { t: 'FOTO', foto: '5227', pos: '55% 50%', txt: 'Em eventos grandes, o organizador precisa cuidar de muita coisa ao mesmo tempo: <b>equipe, convidados, horários, estrutura e imprevistos.</b>' },
  { t: 'TIPO', bg: 'off', txt: 'A imagem acaba ficando <b>para depois</b> — justamente quando o público já começou a publicar o que está vendo.' },
  { t: 'FOTO', foto: '41222', pos: '45% 50%', txt: 'Foi assim que surgiu uma necessidade real para a equipe: um cliente precisava mostrar o que estava acontecendo <b>enquanto o momento ainda estava vivo.</b>' },
  { t: 'FOTO', foto: '4915', pos: '55% 50%', txt: 'No começo, foram feitas algumas imagens com celular, montadas rapidamente e <b>publicadas nos stories.</b>' },
  { t: 'TIPO', bg: 'ora', txt: 'O cliente gostou. E surgiu uma nova pergunta: e se a cobertura fosse pensada desde o início para entregar conteúdo <b>no próprio dia?</b>' },
  { t: 'FOTO', foto: '1741', pos: '40% 50%', txt: 'A resposta não era simplesmente gravar mais. Era entender <b>o objetivo do evento, quem precisava aparecer, o que não podia faltar</b> e onde aquele conteúdo seria publicado.' },
  { t: 'FOTO', foto: '5224', pos: '45% 50%', txt: 'Porque uma imagem bonita pode registrar o evento. Mas uma sequência pensada ajuda a contar <b>por que aquele momento importa.</b>' },
  { t: 'TIPO', bg: 'gra', txt: 'Esse é o trabalho do <b>Storymaker</b>: observar, interpretar, escolher e organizar imagens para que a história chegue às pessoas no tempo certo.' },
  { t: 'CTA', txt: 'Se você trabalha com imagem ou redes sociais e quer aprender a fazer essa leitura na prática, <b>existe um caminho para começar.</b>' },
 ],
 'c2-a-programacao-mudou': [
  { t: 'CAPA', foto: '4632', pos: '60% 50%', titulo: 'O briefing estava pronto. A programação <b>mudou.</b>', txt: 'O roteiro estava organizado. A programação mudou. E a equipe descobriu quando já estava no evento.' },
  { t: 'FOTO', foto: '34486', pos: '50% 35%', txt: 'Era uma cobertura de <b>mais de um dia</b>, com diferentes pessoas, horários e entregas previstas.' },
  { t: 'FOTO', foto: '4953', pos: '50% 55%', txt: 'A equipe tinha conversado com os clientes, entendido preferências e <b>organizado os períodos de captação.</b>' },
  { t: 'TIPO', bg: 'gra', txt: 'Mas os horários das palestras <b>mudaram</b> sem que essa alteração chegasse até a equipe.' },
  { t: 'FOTO', foto: '44069', pos: '55% 45%', txt: 'Uma pessoa que seria gravada em determinado horário passou para outro. Nesse novo horário, <b>já havia outra cobertura prevista.</b>' },
  { t: 'TIPO', bg: 'off', txt: 'A agenda começou a se desorganizar. E o combinado de entregar cada material logo após a palestra <b>deixou de ser possível.</b>' },
  { t: 'FOTO', foto: '43266', pos: '50% 45%', txt: 'A equipe <b>explicou a situação ao contratante</b>, alinhou o que ainda conseguiria entregar e combinou o envio de parte dos materiais no dia seguinte e dos demais ao longo da semana.' },
  { t: 'TIPO', bg: 'ora', txt: 'Nem tudo saiu como planejado. Mas a <b>comunicação</b> evitou que a mudança virasse uma surpresa na entrega.' },
  { t: 'TIPO', bg: 'off', txt: 'O roteiro ajuda a equipe a começar <b>com direção.</b> A conversa ajuda a equipe a se reorganizar <b>quando o evento muda.</b>' },
  { t: 'CTA', txt: 'Storymaker também é saber <b>explicar, negociar prioridades e conduzir a cobertura</b> quando o plano precisa mudar.' },
 ],
 'c3-o-valor-de-um-profissional': [
  { t: 'CAPA', foto: '34408', pos: '50% 50%', titulo: 'Uma habilidade que mudou o valor de um <b>profissional</b>', txt: 'Ele já sabia fazer imagens. O próximo passo foi aprender a contar uma história com elas.' },
  { t: 'TIPO', bg: 'off', grande: 'R$ 150', txt: 'No início, um integrante da equipe cobrava <b>R$ 150</b> por um trabalho.' },
  { t: 'FOTO', foto: '1505', pos: '50% 45%', txt: 'Ele continuou praticando, estudando e prestando mais atenção à <b>seleção das cenas.</b>' },
  { t: 'FOTO', foto: '18204', pos: '50% 50%', txt: 'Começou a pensar não só em “o que ficou bonito”, mas também em <b>como uma imagem se conecta à seguinte.</b>' },
  { t: 'GRADE', faixas: [['5217', 'ABERTO', '50% 45%'], ['41222', 'MÉDIO', '50% 45%'], ['5206', 'DETALHE', '35% 40%'], ['51540', 'REAÇÃO', '60% 40%']], txt: 'Plano aberto, plano médio, detalhe, reação. <b>Cada escolha precisava ajudar a construir o vídeo.</b>' },
  { t: 'FOTO', foto: '50406', pos: '30% 50%', txt: 'A edição automática podia acelerar o processo, mas só funcionava bem quando <b>as cenas certas tinham sido captadas.</b>' },
  { t: 'TIPO', bg: 'ora', grande: 'R$ 500', txt: 'Com a prática, ele passou a contar histórias com mais intenção e seu cachê chegou a <b>R$ 500.</b>' },
  { t: 'TIPO', bg: 'gra', aviso: true, txt: 'Esse é o percurso de <b>uma pessoa da equipe.</b> Não é uma promessa de quanto alguém vai ganhar: cada trabalho, cliente, cidade e profissional tem sua realidade.' },
  { t: 'FOTO', foto: '5227', pos: '50% 50%', txt: 'O aprendizado foi entender que <b>o olhar, a leitura do evento e a sequência das imagens</b> também fazem parte do serviço.' },
  { t: 'CTA', txt: 'Se você já trabalha com fotografia, vídeo ou redes sociais, desenvolver esse olhar pode <b>ampliar o que você consegue oferecer.</b>' },
 ],
};

const css = `@import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700;800&family=IBM+Plex+Mono:wght@500&family=Sora:wght@800&display=swap');
*{margin:0;box-sizing:border-box} body{width:1080px;height:1350px;overflow:hidden;font-family:Inter,sans-serif}
.s{position:relative;width:1080px;height:1350px;overflow:hidden}
.ph{position:absolute;inset:0;background-size:cover}
.sc{position:absolute;inset:0;background:linear-gradient(180deg,rgba(27,26,31,.55) 0%,rgba(27,26,31,.05) 26%,rgba(27,26,31,.1) 45%,rgba(27,26,31,.88) 74%,rgba(27,26,31,.96) 100%)}
.lb{position:absolute;top:64px;left:72px;right:72px;display:flex;justify-content:space-between;font:500 22px 'IBM Plex Mono',monospace;letter-spacing:.14em;text-transform:uppercase;z-index:3}
.cx{position:absolute;left:72px;right:72px;bottom:120px;z-index:3}
.txt{font:500 52px/1.18 Inter;letter-spacing:-.025em;color:#fff}
.txt b{font-weight:800;color:#e7570c}
.cap h1{font:500 92px/1.02 Inter;letter-spacing:-.045em;color:#fff;margin-bottom:34px}
.cap h1 b{font-weight:800;color:#e7570c}
.cap .txt{font-size:40px;color:#e4e2e8}
.cap .txt b{color:#fff}
.arr{position:absolute;right:72px;bottom:56px;font:600 26px Inter;color:#fff;z-index:3;display:flex;gap:12px;align-items:center}
.arr i{display:inline-block;width:46px;height:2px;background:#e7570c;position:relative}.arr i:after{content:'';position:absolute;right:-2px;top:-7px;border-left:12px solid #e7570c;border-top:8px solid transparent;border-bottom:8px solid transparent}
.tipo{display:flex;flex-direction:column;justify-content:center;padding:0 80px}
.tipo .txt{font-size:70px;line-height:1.08;letter-spacing:-.04em}
.off{background:#ece8e3}.off .txt{color:#2b2a30}.off .txt b{color:#e7570c}.off .lb{color:#2b2a30}
.gra{background:#1b1a1f}.gra .lb{color:#d9d7de}
.ora{background:#e7570c}.ora .txt{color:#fff}.ora .txt b{color:#fff;text-decoration:underline;text-decoration-thickness:6px;text-underline-offset:10px;text-decoration-color:#1f1e24}.ora .lb{color:#1f1e24}
.grande{font:800 220px/0.9 Inter;letter-spacing:-.06em;margin-bottom:40px}
.off .grande{color:#e7570c}.ora .grande{color:#fff}
.av{font:500 24px 'IBM Plex Mono',monospace;letter-spacing:.12em;text-transform:uppercase;color:#e7570c;margin-bottom:30px}
.mark{display:inline-block;width:22px;height:22px;background:#e7570c;margin-left:10px;vertical-align:.7em}
.ora .mark{background:#fff}
.guia{position:absolute;border:2px solid rgba(231,87,12,.35);border-radius:50%}
.off .guia{border-color:rgba(43,42,48,.12)}
.grade{position:absolute;left:0;right:0;top:130px;height:800px;display:grid;grid-template-rows:repeat(4,1fr);gap:8px;background:#1b1a1f}
.grade div{background-size:cover;position:relative}
.grade span{position:absolute;right:24px;bottom:16px;font:500 22px 'IBM Plex Mono',monospace;letter-spacing:.16em;color:#fff;background:rgba(27,26,31,.72);padding:8px 14px;border-radius:6px}
.cta{background:#e7570c;display:flex;flex-direction:column;justify-content:center;padding:0 80px}
.cta .txt{font-size:64px;line-height:1.1;letter-spacing:-.04em;color:#fff}
.cta .txt b{color:#fff;font-weight:800}
.cta .lb{color:#1f1e24}
.marca{margin-top:70px;padding-top:34px;border-top:2px solid rgba(31,30,36,.35)}
.marca .lg{font:800 48px Sora;letter-spacing:-.03em;color:#fff}
.marca p{margin-top:12px;font:600 30px Inter;color:#1f1e24}
.cred{position:absolute;left:72px;bottom:56px;font:500 18px Inter;color:rgba(255,255,255,.55);z-index:3}
.cta .cred{color:rgba(31,30,36,.7)}`;

function slide(s, i, n) {
  const num = `${String(i + 1).padStart(2, '0')} / ${String(n).padStart(2, '0')}`;
  const lb = (cor) => `<div class="lb" style="color:${cor || '#fff'}"><span>Storymaker Oficial</span><span>${num}</span></div>`;
  const arr = i < n - 1 ? `<div class="arr">${i === 0 ? 'Arraste' : ''}<i></i></div>` : '';
  if (s.t === 'CAPA') return `<div class="s cap"><div class="ph" style="background-image:url(${F(s.foto)});background-position:${s.pos}"></div><div class="sc"></div>${lb()}<div class="cx"><h1>${s.titulo}</h1><p class="txt">${s.txt}</p></div>${arr}</div>`;
  if (s.t === 'FOTO') return `<div class="s"><div class="ph" style="background-image:url(${F(s.foto)});background-position:${s.pos}"></div><div class="sc"></div>${lb()}<div class="cx"><p class="txt">${s.txt}</p></div>${arr}</div>`;
  if (s.t === 'GRADE') return `<div class="s" style="background:#1b1a1f"><div class="grade">${s.faixas.map(([f, r, p]) => `<div style="background-image:url(${F(f)});background-position:${p}"><span>${r}</span></div>`).join('')}</div>${lb()}<div class="cx"><p class="txt">${s.txt}</p></div>${arr}</div>`;
  if (s.t === 'TIPO') {
    const g = s.bg === 'off' ? '<div class="guia" style="width:900px;height:900px;right:-420px;top:-300px"></div>' : '<div class="guia" style="width:760px;height:760px;left:-380px;bottom:-320px"></div>';
    return `<div class="s tipo ${s.bg}">${g}${lb(s.bg === 'off' ? '#2b2a30' : s.bg === 'ora' ? '#1f1e24' : '#d9d7de')}${s.aviso ? '<p class="av">Caso real · não é promessa</p>' : ''}${s.grande ? `<p class="grande">${s.grande}</p>` : ''}<p class="txt">${s.txt}<span class="mark"></span></p>${arr}</div>`;
  }
  if (s.t === 'CTA') return `<div class="s cta">${lb('#1f1e24')}<p class="txt">${s.txt}</p><div class="marca"><div class="lg">Storymaker Oficial</div><p>Conheça os materiais · link na bio</p></div><div class="cred">Imagens ilustrativas de banco gratuito (Mixkit)</div></div>`;
}

(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  for (const [nome, ss] of Object.entries(C)) {
    const dir = path.join(OUT, nome); fs.mkdirSync(dir, { recursive: true });
    for (let i = 0; i < ss.length; i++) {
      await p.setContent(`<style>${css}</style>${slide(ss[i], i, ss.length)}`, { waitUntil: 'networkidle' });
      await p.evaluate(() => document.fonts.ready);
      await p.screenshot({ path: path.join(dir, `${String(i + 1).padStart(2, '0')}.png`) });
    }
    console.log(nome, ss.length, 'slides');
  }
  await b.close();
})();
