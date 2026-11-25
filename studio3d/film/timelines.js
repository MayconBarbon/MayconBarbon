/* Roteiros dos quatro vídeos (tempo em segundos → estado da cena, câmera e textos). */
(function () {
  'use strict';
  var F = window.FILM, Y = F.aptY;
  var C = [4.45, 0, 4.05];
  function cl(x) { return Math.max(0, Math.min(1, x)); }
  function E(x) { x = cl(x); return x * x * (3 - 2 * x); }
  function E2(x) { x = cl(x); return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; }
  function seg(t, a, b) { return cl((t - a) / (b - a)); }
  function lerp(a, b, k) { return a + (b - a) * k; }
  function lerp3(a, b, k) { return [lerp(a[0], b[0], k), lerp(a[1], b[1], k), lerp(a[2], b[2], k)]; }
  function cr(p0, p1, p2, p3, t) { var t2 = t * t, t3 = t2 * t; return 0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3); }
  // caminho suave por quadros-chave [{t, p, l, fov}]
  function path(keys, t, easeAll) {
    var a = keys[0].t, b = keys[keys.length - 1].t;
    var u = easeAll === false ? cl((t - a) / (b - a)) : E2((t - a) / (b - a));
    var tt = a + (b - a) * u, i = 0;
    while (i < keys.length - 2) { if (tt <= keys[i + 1].t) break; i++; }
    var k0 = keys[Math.max(0, i - 1)], k1 = keys[i], k2 = keys[i + 1], k3 = keys[Math.min(keys.length - 1, i + 2)];
    var s = (tt - k1.t) / (k2.t - k1.t);
    function c3(f) { return [0, 1, 2].map(function (j) { return cr(k0[f][j], k1[f][j], k2[f][j], k3[f][j], s); }); }
    return {p: c3('p'), l: c3('l'), fov: lerp(k1.fov, k2.fov, s)};
  }
  function lin(a, b, t, t0, t1, fov, ez) { var k = ez === false ? seg(t, t0, t1) : E(seg(t, t0, t1)); return {p: lerp3(a.p, b.p, k), l: lerp3(a.l, b.l, k), fov: fov}; }
  function orbit(az, r, h, look, fov) { return {p: [C[0] + r * Math.sin(az), h, C[2] + r * Math.cos(az)], l: look || [C[0], 0.4, C[2]], fov: fov || 35}; }
  function dist(c) { var d = [c.p[0] - c.l[0], c.p[1] - c.l[1], c.p[2] - c.l[2]]; return Math.hypot(d[0], d[1], d[2]); }
  // textos: [t0, t1, kicker, título]
  function txt(t, list) {
    for (var i = 0; i < list.length; i++) {
      var x = list[i]; if (t >= x[0] - 0.01) { if (t <= x[1]) {
        var a = E(seg(t, x[0], x[0] + 0.7)), b = 1 - E(seg(t, x[1] - 0.6, x[1]));
        return {k: x[2], t: x[3], op: Math.min(a, b), dy: (1 - a) * 18, line: a};
      } }
    }
    return {op: 0};
  }
  function label(r) { return {name: r.name, dim: (r.w.toFixed(2) + ' × ' + r.d.toFixed(2) + ' m').replace(/\./g, ',')}; }
  var LABELS = F.rooms.filter(function (r) { return !r.nolabel; }).map(function (r) { return {pt: [r.x + r.w / 2, 0.08, r.y + r.d / 2], txt: label(r)}; });
  var VERT = F.H > F.W;
  var PO = VERT ? [0, 0, 2.4] : [-3.4, 0, 0]; // desloca a planta para deixar o texto sobre o fundo escuro
  function topv(h) { return {p: [4.45 + PO[0], h, 4.12 + PO[2]], l: [4.45 + PO[0], 0, 4.05 + PO[2]], fov: 38}; }
  var TOP = {p: [4.45, 15.2, 4.12], l: [4.45, 0, 4.05], fov: 38};
  var az0 = Math.atan2(13.5 - 4.45, 13.2 - 4.05);

  var V = {};
  // ===================== NÍVEL 1 · 3D ESSENCIAL (25 s)
  V.essencial = {dur: 25, level: 'Nível 1 · 3D Essencial', frame: function (t) {
    var s = {light: 'studio', bg: 'dark', plan: 1 - E(seg(t, 5.6, 9.4)), rise: E2(seg(t, 4.5, 8.8)), finishFloor: 0, finishWall: 0};
    var c;
    if (t < 4) c = topv(lerp(19.5, 18.2, E(t / 4)));
    else if (t < 10) c = path([{t: 4, p: topv(18.2).p, l: topv(18.2).l, fov: 38}, {t: 7, p: [8.8, 12.6, 11.4], l: [4.45, 0.2, 4.05], fov: 36}, {t: 10, p: orbit(az0, 13.4, 9.6).p, l: [4.45, 0.4, 4.05], fov: 35}], t);
    else if (t < 18) c = orbit(az0 + 1.55 * E(seg(t, 10, 18.2)) * 0.98 + 0.0, 13.4 - 0.6 * seg(t, 10, 18), 9.6 - 0.4 * seg(t, 10, 18));
    else c = path([{t: 18, p: orbit(az0 + 1.52, 12.8, 9.2).p, l: [4.45, 0.4, 4.05], fov: 35}, {t: 21, p: [4.45, 14.6, 4.6], l: [4.45, 0, 4.05], fov: 38}, {t: 22.5, p: [4.45, 14.3, 4.5], l: [4.45, 0, 4.05], fov: 38}], t);
    return {s: s, c: c,
      txt: txt(t, [[0.5, 3.8, 'Nível 1 · 3D Essencial', 'Tudo começa com uma planta.'], [4.8, 9.6, 'Nível 1 · 3D Essencial', 'Seu projeto ganha forma.'], [10.6, 17.4, 'Distribuição dos ambientes', 'Compreensão espacial.'], [18.2, 21.8, 'Vista superior', 'Volumetria e distribuição.']]),
      labels: {op: Math.min(E(seg(t, 10.4, 11.2)), 1 - E(seg(t, 17.2, 17.9))) + Math.min(E(seg(t, 19.6, 20.4)), 1 - E(seg(t, 21.6, 22.1))), list: LABELS},
      end: E(seg(t, 22, 22.8)), brand: E(seg(t, 0.3, 1.2)) * (1 - E(seg(t, 22, 22.6)))};
  }};
  // ===================== NÍVEL 2 · 3D COM ACABAMENTOS (30 s)
  V.acabamentos = {dur: 30, level: 'Nível 2 · 3D com Acabamentos', frame: function (t) {
    var s = {light: 'day', bg: 'dark', rise: 1, finishFloor: E(seg(t, 4.3, 9.8)), finishWall: E(seg(t, 10.2, 15.6)), basic: seg(t, 12, 17.4)};
    var c;
    if (t < 10) c = orbit(az0 + 0.35 * E(seg(t, 0, 10)) - 0.05, 13.2 - 0.8 * E(seg(t, 0, 10)), 9.4 - 1.0 * E(seg(t, 0, 10)));
    else if (t < 16) c = path([{t: 10, p: orbit(az0 + 0.3, 12.4, 8.4).p, l: [4.45, 0.4, 4.05], fov: 35}, {t: 16, p: [11.6, 6.4, 11.0], l: [4.6, 0.6, 4.4], fov: 36}], t);
    else if (t < 19.5) c = lin({p: [11.6, 6.4, 11.0], l: [4.6, 0.6, 4.4]}, {p: [10.2, 4.9, 9.3], l: [4.1, 0.5, 4.7]}, t, 16, 19.5, 38, false);
    else if (t < 23) c = lin({p: [9.2, 8.2, -3.6], l: [4.3, 0.3, 1.8]}, {p: [8.0, 7.6, -3.2], l: [4.0, 0.3, 1.8]}, t, 19.5, 23, 38, false);
    else c = lin(orbit(az0 + 0.7, 13.6, 10.2), orbit(az0 + 0.95, 13.2, 9.8), t, 23, 27.5, 35, false);
    return {s: s, c: c,
      txt: txt(t, [[0.5, 3.9, 'Nível 2 · 3D com Acabamentos', 'O projeto ganha identidade.'], [4.6, 9.8, 'Pisos e revestimentos', 'Materiais, texturas e acabamentos.'], [10.4, 15.8, 'Paredes e esquadrias', 'Cada detalhe começa a fazer sentido.'], [16.4, 22.6, 'Ambientes com materiais aplicados', 'Escolhas visíveis antes da obra.'], [23.3, 26.9, 'Vista geral', 'Visualize antes de construir.']]),
      end: E(seg(t, 27, 27.8)), brand: E(seg(t, 0.3, 1.2)) * (1 - E(seg(t, 27, 27.6))), fade: Math.max(0, 1 - Math.abs(t - 19.5) / 0.25) * 0.85};
  }};
  // ===================== NÍVEL 3 · 3D DECORADO (40 s)
  var INT = {ceiling: true, bg: 'hdri'};
  function sc(o, extra) { var r = {}; Object.keys(o).forEach(function (k) { r[k] = o[k]; }); Object.keys(extra || {}).forEach(function (k) { r[k] = extra[k]; }); return r; }
  V.decorado = {dur: 40, level: 'Nível 3 · 3D Decorado', frame: function (t) {
    var base = {light: 'afternoon', bg: 'dark', rise: 1, finishFloor: 1, finishWall: 1, basic: 1, decor: E(seg(t, 4.2, 9.9)), lampsOn: 0.15};
    var s = base, c, cap = null;
    if (t < 10) c = orbit(az0 + 0.1 + 0.45 * E(seg(t, 0, 10)), 12.4 - 1.2 * E(seg(t, 0, 10)), 8.6 - 1.2 * E(seg(t, 0, 10)));
    else if (t < 14) { s = sc(base, INT); s.lampsOn = 0.3; c = lin({p: [3.25, 1.52, 6.35], l: [7.0, 1.0, 4.1]}, {p: [4.2, 1.48, 5.85], l: [7.6, 1.0, 3.9]}, t, 10, 14, 52, false); cap = 'Estar e jantar'; }
    else if (t < 18) { s = sc(base, INT); s.lampsOn = 0.3; c = lin({p: [7.6, 1.46, 3.95], l: [3.6, 0.95, 5.35]}, {p: [7.35, 1.42, 4.85], l: [3.4, 0.95, 4.6]}, t, 14, 18, 54, false); cap = 'Estar e jantar'; }
    else if (t < 21.5) { s = sc(base, INT); s.lampsOn = 0.35; c = lin({p: [3.65, 1.55, 3.62], l: [0.6, 1.0, 5.0]}, {p: [3.25, 1.5, 4.05], l: [0.5, 1.0, 5.45]}, t, 18, 21.5, 55, false); cap = 'Cozinha integrada'; }
    else if (t < 25) { s = sc(base, INT); s.lampsOn = 0.45; c = lin({p: [4.75, 1.22, 5.9], l: [3.8, 0.9, 4.9]}, {p: [4.6, 1.16, 5.62], l: [3.8, 0.88, 4.9]}, t, 21.5, 25, 46, false); c.dof = [dist(c), 0.00012, 0.006]; cap = 'Jantar'; }
    else if (t < 28.5) { s = sc(base, INT); s.lampsOn = 0.45; c = lin({p: [5.32, 1.52, 2.98], l: [7.6, 0.6, 1.3]}, {p: [5.6, 1.46, 2.62], l: [7.7, 0.6, 1.4]}, t, 25, 28.5, 56, false); cap = 'Dormitório casal'; }
    else if (t < 32) { s = sc(base, INT); s.lampsOn = 0.45; c = lin({p: [2.48, 1.52, 2.8], l: [0.6, 0.7, 0.9]}, {p: [2.25, 1.46, 2.48], l: [0.6, 0.7, 0.8]}, t, 28.5, 32, 58, false); cap = 'Dormitório'; }
    else { s = sc(base, {lampsOn: 0.75}); c = orbit(az0 + 0.55 + 0.35 * E(seg(t, 32, 37.5)), 12.6, 8.8); }
    var f = 0; [10, 14, 18, 21.5, 25, 28.5, 32].forEach(function (k) { f = Math.max(f, (1 - Math.abs(t - k) / 0.22) * 0.9); });
    return {s: s, c: c,
      txt: txt(t, [[0.5, 3.9, 'Nível 3 · 3D Decorado', 'Mais do que visualizar.'], [4.6, 9.8, 'Mobiliário e decoração', 'Imagine viver aqui.'], [10.6, 17.6, cap || 'Estar e jantar', 'Ambientes que despertam desejo.'], [18.4, 21.3, 'Cozinha integrada', ''], [21.8, 24.8, 'Jantar', ''], [25.3, 28.3, 'Dormitório casal', ''], [28.8, 31.8, 'Dormitório', ''], [32.4, 36.9, 'Vista geral decorada', 'Apresente hoje o que será construído amanhã.']]),
      end: E(seg(t, 37, 37.8)), brand: E(seg(t, 0.3, 1.2)) * (1 - E(seg(t, 37, 37.6))), fade: Math.max(0, f)};
  }};
  // ===================== NÍVEL 4 · CINEMATIC (60 s)
  V.cinematic = {dur: 60, level: 'Nível 4 · Cinematic', bars: true, frame: function (t) {
    var s, c, disc = null, cap = null;
    var IN = {light: 'golden', bg: 'sky', ceiling: true, tower: true, rise: 1, finishFloor: 1, finishWall: 1, basic: 1, decor: 1, lampsOn: 0.25, exposure: 1.05};
    if (t < 5) {
      s = {light: 'golden', bg: 'dark', plan: 1 - E(seg(t, 1.2, 2.4)), rise: E2(seg(t, 0.9, 2.5)), finishFloor: E(seg(t, 2.1, 3.3)), finishWall: E(seg(t, 2.6, 3.8)), basic: seg(t, 3.1, 4.3), decor: seg(t, 3.6, 5.0), lampsOn: 0.2};
      c = path([{t: 0, p: topv(19).p, l: topv(19).l, fov: 38}, {t: 2.4, p: [8.0, 13.0, 10.0], l: [4.45, 0.2, 4.05], fov: 36}, {t: 5, p: orbit(az0 + 0.3, 12.2, 8.4).p, l: [4.45, 0.5, 4.05], fov: 35}], t);
    } else if (t < 12) {
      s = sc(IN, {ceiling: false, shadowFar: true, exposure: 1.0}); disc = 'Edifício conceitual · imagem ilustrativa';
      var k = E(seg(t, 5, 12)), az = 2.18 + 0.3 * k, r = 78 - 8 * k;
      c = {p: [-2.6 + r * Math.sin(az), lerp(6, 26, k), 7.4 + r * Math.cos(az)], l: [-2.6, lerp(18, 21, k), 7.4], fov: 34};
    } else if (t < 22) {
      s = sc(IN, {}); disc = 'Edifício conceitual · imagem ilustrativa';
      c = path([{t: 12, p: [30, Y + 7, -7], l: [8.8, Y + 1.2, 5.0], fov: 34}, {t: 15.5, p: [17, Y + 2.6, 5.4], l: [8.8, Y + 1.25, 5.3], fov: 40}, {t: 18.3, p: [10.4, Y + 1.55, 5.68], l: [6.0, Y + 1.1, 5.2], fov: 50}, {t: 20.2, p: [8.0, Y + 1.5, 5.68], l: [4.5, Y + 1.05, 5.0], fov: 54}, {t: 22, p: [7.05, Y + 1.45, 5.3], l: [3.6, Y + 1.0, 4.8], fov: 54}], t);
    } else if (t < 32) {
      s = sc(IN, {lampsOn: 0.45});
      if (t < 25.3) { c = lin({p: [4.62, Y + 1.36, 5.78], l: [3.8, Y + 0.96, 4.9]}, {p: [4.45, Y + 1.3, 5.56], l: [3.8, Y + 0.94, 4.9]}, t, 22, 25.3, 44, false); cap = 'Iluminação'; }
      else if (t < 28.6) { c = lin({p: [5.95, Y + 0.78, 3.92], l: [6.6, Y + 0.5, 5.6]}, {p: [6.65, Y + 0.74, 3.98], l: [6.5, Y + 0.5, 5.65]}, t, 25.3, 28.6, 44, false); cap = 'Mobiliário'; }
      else { c = lin({p: [2.78, Y + 1.16, 3.7], l: [1.6, Y + 0.92, 5.0]}, {p: [2.62, Y + 1.12, 4.12], l: [1.55, Y + 0.92, 5.1]}, t, 28.6, 32, 44, false); cap = 'Materiais'; }
      c.dof = [dist(c), 0.00016, 0.008];
    } else if (t < 42) {
      s = sc(IN, {lampsOn: 0.5});
      if (t < 36) { c = lin({p: [5.3, Y + 1.46, 2.96], l: [7.7, Y + 0.65, 1.3]}, {p: [5.72, Y + 1.4, 2.5], l: [7.75, Y + 0.65, 1.4]}, t, 32, 36, 54, false); cap = 'Dormitório casal'; }
      else if (t < 39.5) { c = lin({p: [2.48, Y + 1.5, 2.82], l: [0.5, Y + 0.7, 0.8]}, {p: [2.12, Y + 1.45, 2.42], l: [0.5, Y + 0.7, 0.75]}, t, 36, 39.5, 56, false); cap = 'Dormitório'; }
      else { c = lin({p: [3.72, Y + 1.6, 2.75], l: [3.5, Y + 0.95, 0.5]}, {p: [3.74, Y + 1.56, 2.45], l: [3.55, Y + 0.95, 0.45]}, t, 39.5, 42, 58, false); cap = 'Banheiro'; }
    } else if (t < 50) {
      var dk = E(seg(t, 42, 44.5));
      s = sc(IN, {light: dk > 0.5 ? 'dusk' : 'golden', lampsOn: lerp(0.5, 1.0, dk), exposure: lerp(1.05, 1.12, dk)});
      if (t < 46) c = lin({p: [0.95, Y + 1.45, 6.1], l: [8.6, Y + 1.25, 4.2]}, {p: [1.45, Y + 1.45, 5.75], l: [8.6, Y + 1.25, 4.3]}, t, 42, 46, 58, false);
      else { s.ceiling = true; c = path([{t: 46, p: [6.9, Y + 1.5, 5.4], l: [3.6, Y + 1.0, 4.6], fov: 54}, {t: 48, p: [9.0, Y + 1.6, 5.68], l: [4.2, Y + 1.05, 4.8], fov: 50}, {t: 50, p: [14.5, Y + 3.0, 6.2], l: [4.8, Y + 1.2, 4.8], fov: 42}], t); disc = 'Edifício conceitual · imagem ilustrativa'; }
    } else {
      s = sc(IN, {light: 'dusk', lampsOn: 1.0, ceiling: true, shadowFar: true, exposure: 1.12}); disc = 'Edifício conceitual · imagem ilustrativa';
      var k2 = E(seg(t, 50, 55.5)), az2 = 2.3 + 0.16 * k2, r2 = lerp(52, 64, k2);
      c = {p: [-2.6 + r2 * Math.sin(az2), lerp(Y + 2, Y + 8, k2), 7.4 + r2 * Math.cos(az2)], l: [0.0, lerp(Y - 2, Y - 3, k2), 6.0], fov: 36};
    }
    var f = 0; [22, 25.3, 28.6, 32, 36, 39.5, 42].forEach(function (k) { f = Math.max(f, (1 - Math.abs(t - k) / 0.2) * 0.95); });
    f = Math.max(f, (1 - Math.abs(t - 5) / 0.3), (1 - Math.abs(t - 12) / 0.25) * 0.9, (1 - Math.abs(t - 50) / 0.3) * 0.9);
    return {s: s, c: c, disc: disc,
      txt: txt(t, [[0.8, 4.6, 'Da planta ao cinematic', 'Antes mesmo de existir.'], [6.0, 11.6, 'Edifício conceitual', 'Seu empreendimento já pode despertar desejo.'], [15.6, 21.6, 'Ambientes sociais', 'Arquitetura em movimento.'], [22.4, 25.0, 'Iluminação', ''], [25.7, 28.3, 'Mobiliário', ''], [29.0, 31.7, 'Materiais', ''], [32.6, 41.6, cap || 'Ambientes privativos', 'Experiências que antecipam o futuro.'], [50.6, 54.8, 'Vídeo Imóvel Studio 3D', 'Da planta à emoção.']]),
      end: E(seg(t, 55, 55.9)), brand: E(seg(t, 0.4, 1.3)) * (1 - E(seg(t, 55, 55.6))), fade: Math.max(0, f)};
  }};

  // ===================== aplicação de um quadro
  var D = document, el = function (id) { return D.getElementById(id); };
  var labelEls = [];
  var vert = F.H > F.W;
  var U = (vert ? F.W / 1080 : F.H / 1080) * 26;
  D.documentElement.style.setProperty('--u', U + 'px');
  D.documentElement.style.setProperty('--m', (U * 3.2) + 'px');
  if (vert) { el('txt').style.maxWidth = '86%'; el('txt').style.bottom = (U * 9) + 'px'; }
  function adapt(c, interior) {
    if (!vert) return c;
    var h = 2 * Math.atan(Math.tan(c.fov * Math.PI / 360) * 16 / 9), want = h * (interior ? 0.62 : 0.66);
    var v = 2 * Math.atan(Math.tan(want / 2) * 16 / 9) * 180 / Math.PI, maxV = interior ? 78 : 70;
    var o = {p: c.p.slice(), l: c.l.slice(), fov: Math.min(v, maxV), dof: c.dof, local: c.local};
    if (!interior) { if (v > maxV) {
      var f = Math.tan(v * Math.PI / 360) / Math.tan(maxV * Math.PI / 360);
      o.p = [0, 1, 2].map(function (j) { return c.l[j] + (c.p[j] - c.l[j]) * f; });
      if (o.dof) o.dof = [o.dof[0] * f, o.dof[1], o.dof[2]];
    } }
    return o;
  }
  window.RENDER = function (id, t) {
    var v = V[id], r = v.frame(t);
    F.setState(r.s);
    var interior = !!(r.s.ceiling);
    var cam = adapt(r.c, interior);
    if (cam.dof) cam.dof = [dist(cam), cam.dof[1], cam.dof[2]];
    F.frame(cam);
    // textos
    var tx = r.txt || {op: 0};
    el('txt').style.opacity = tx.op; el('txt').style.transform = 'translateY(' + (tx.dy || 0) + 'px)';
    if (tx.op > 0) { D.querySelector('#txt .k').textContent = tx.k || ''; D.querySelector('#txt .t').textContent = tx.t || ''; D.querySelector('#txt .t').style.display = tx.t ? 'block' : 'none'; D.querySelector('#txt .k').style.setProperty('--line', tx.line); }
    el('level').textContent = v.level; el('level').style.opacity = r.brand === undefined ? 1 : r.brand;
    el('brand').style.opacity = r.brand === undefined ? 1 : r.brand;
    el('disc').textContent = r.disc || 'Projeto de demonstração · imagens ilustrativas';
    el('disc').style.opacity = 1 - (r.end || 0);
    el('end').style.opacity = r.end || 0; el('end').style.setProperty('--el', E(((r.end || 0) - 0.3) / 0.7));
    el('fade').style.opacity = r.fade || 0;
    var bar = (v.bars && !vert) ? Math.round((F.H - F.W / 2.39) / 2) : 0;
    el('bars').style.setProperty('--bar', bar + 'px'); el('bars').style.opacity = bar ? 1 - (r.end || 0) : 0;
    if (bar) { el('brand').style.top = (bar + U * 1.2) + 'px'; el('level').style.top = (bar + U * 1.4) + 'px'; el('txt').style.bottom = (bar + U * 1.6) + 'px'; el('disc').style.bottom = (bar * 0.5 - U * 0.3) + 'px'; el('disc').style.color = 'rgba(245,245,247,.6)'; }
    // rótulos dos ambientes
    var L = r.labels;
    if (L) { if (L.op > 0) {
      var pts = F.project(L.list.map(function (x) { return x.pt; }));
      while (labelEls.length < L.list.length) { var d = D.createElement('div'); d.className = 'lb'; d.innerHTML = '<b></b><i></i>'; el('labels').appendChild(d); labelEls.push(d); }
      L.list.forEach(function (x, i) { var e = labelEls[i]; e.style.left = pts[i].x + 'px'; e.style.top = pts[i].y + 'px'; e.style.opacity = pts[i].vis ? L.op : 0; e.firstChild.textContent = x.txt.name; e.lastChild.textContent = x.txt.dim; });
    } }
    if (!L || !(L.op > 0)) labelEls.forEach(function (e) { e.style.opacity = 0; });
    return true;
  };
  window.VIDEOS = V;
})();
