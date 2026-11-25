/* Vídeo Imóvel Studio 3D · motor de filmagem
   Uma única geometria (plans/apto.json) para os quatro níveis:
   planta → volumetria → acabamentos → decorado → cinematic.
   Cada quadro é desenhado sob demanda por FILM.frame(t) (determinístico). */
(function () {
  'use strict';
  var P = window.APTO, T = THREE;
  var W = window.innerWidth, H = window.innerHeight;
  var R = new T.WebGLRenderer({antialias: true, preserveDrawingBuffer: true});
  R.setPixelRatio(1); R.setSize(W, H);
  R.shadowMap.enabled = true; R.shadowMap.type = T.PCFSoftShadowMap;
  R.outputEncoding = T.sRGBEncoding; R.toneMapping = T.ACESFilmicToneMapping; R.toneMappingExposure = 1.0;
  R.localClippingEnabled = true;
  document.getElementById('stage').appendChild(R.domElement);
  var S = new T.Scene();
  var cam = new T.PerspectiveCamera(35, W / H, 0.05, 900);
  var Hh = P.H; // pé-direito adotado (não documentado na planta)

  // ---------- luz
  var hemi = new T.HemisphereLight(new T.Color(0xffffff), new T.Color(0xd9d2c4).convertSRGBToLinear(), 0.35); S.add(hemi);
  var sun = new T.DirectionalLight(0xfff2df, 2.2);
  sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048); sun.shadow.bias = -0.00035; sun.shadow.normalBias = 0.02;
  S.add(sun); S.add(sun.target);
  function shadowBox(cx, cz, half) {
    var c = sun.shadow.camera; c.left = -half; c.right = half; c.top = half; c.bottom = -half; c.near = 0.5; c.far = 220; c.updateProjectionMatrix();
    sun.target.position.set(cx, 0, cz);
  }
  shadowBox(4.5, 4, 8);

  // ---------- texturas
  var TL = new T.TextureLoader(), pending = [];
  function tex(id, map, rep, srgb) {
    var t, url = 'assets/tex/' + id + '_' + map + '.jpg';
    pending.push(new Promise(function (ok) { t = TL.load(url, function () { ok(); }, undefined, function () { console.error('textura', url); ok(); }); }));
    t.wrapS = t.wrapT = T.RepeatWrapping; t.repeat.set(rep[0], rep[1]); t.anisotropy = 8;
    if (srgb) t.encoding = T.sRGBEncoding; return t;
  }
  function pbr(id, rep, o) {
    o = o || {};
    var m = new T.MeshStandardMaterial({map: tex(id, 'diff', rep, true), normalMap: tex(id, 'nor_gl', rep), roughnessMap: tex(id, 'rough', rep), roughness: o.r === undefined ? 1 : o.r, metalness: 0});
    if (o.ns) m.normalScale.set(o.ns, o.ns);
    if (o.color) m.color.copy(lin(o.color));
    return m;
  }
  function lin(c) { return new T.Color(c).convertSRGBToLinear(); }
  function M(c, r, extra) { var m = new T.MeshStandardMaterial({color: lin(c), roughness: r === undefined ? 0.85 : r, metalness: 0}); if (extra) { var e = Object.assign({}, extra); if (e.emissive !== undefined) { m.emissive = lin(e.emissive); delete e.emissive; } Object.assign(m, e); } return m; }

  // ---------- planos de recorte para a aplicação progressiva (varredura diagonal)
  var sweepN = new T.Vector3(1, 0, 0.45).normalize();
  function clipPair() { return {fin: new T.Plane(sweepN.clone().negate(), 0), raw: new T.Plane(sweepN.clone(), 0)}; }
  var cpF = clipPair(), cpW = clipPair();
  function setSweep(cp, v) { cp.fin.constant = v; cp.raw.constant = -v; }

  // ---------- materiais (volumetria e acabamento)
  var CLAY = {wall: M(0xeceae5, 0.95), cap: M(0x1c1c20, 1), floor: M(0xdedbd4, 0.97), door: M(0xf4f2ee, 0.9), frame: M(0xd6d3cc, 0.8), fixture: M(0xf2f0ec, 0.9)};
  var FIN = {
    wall: M(0xefe9df, 0.92), accent: M(0xcbbfae, 0.95), bedroom: M(0xd9cfc2, 0.95), bath: pbr('long_white_tiles', [1, 1], {r: 0.5}),
    cap: M(0x1c1c20, 1),
    wood: pbr('laminate_floor_02', [1, 1], {ns: 0.6}), porc: pbr('slab_tiles', [1, 1], {color: 0xf2efe9}), tile: pbr('long_white_tiles', [1, 1], {color: 0xe9e6e1}),
    deck: pbr('wood_floor_deck', [1, 1], {color: 0xcdb9a3}), hall: pbr('slab_tiles', [1, 1], {color: 0xd8d4cc}),
    marble: M(0xece8e2, 0.25), door: M(0xf6f4ef, 0.55), oakDoor: M(0x8a6a4c, 0.6),
    frame: M(0x2a2a2c, 0.45, {metalness: 0.4}), lacquer: M(0xf3f1ec, 0.35), oak: M(0xb7997c, 0.55), walnut: M(0x6b5544, 0.5),
    metal: M(0xb9b4aa, 0.3, {metalness: 0.8}), blackm: M(0x1d1d1f, 0.4, {metalness: 0.5}), chrome: M(0xdedede, 0.15, {metalness: 1})
  };
  var glassMat = new T.MeshStandardMaterial({color: 0xdfeaf0, roughness: 0.04, metalness: 0.1, transparent: true, opacity: 0.16, envMapIntensity: 1.6, depthWrite: false});
  var floorMatOf = {wood: FIN.wood, porc: FIN.porc, tile: FIN.tile, deck: FIN.deck, stone: FIN.hall};

  // ---------- grupos
  var apt = new T.Group(); S.add(apt);           // tudo que pertence à unidade
  var gPlan = new T.Group(), gRaw = new T.Group(), gFin = new T.Group(), gRawF = new T.Group(), gFinF = new T.Group(), gCeil = new T.Group(), gGlass = new T.Group();
  var gBasic = new T.Group(), gDecor = new T.Group(), gTower = new T.Group(), gStudio = new T.Group();
  [gPlan, gRaw, gFin, gRawF, gFinF, gCeil, gGlass, gBasic, gDecor].forEach(function (g) { apt.add(g); });
  S.add(gTower); S.add(gStudio);

  function mesh(geo, mat, x, y, z, g, sh) {
    var m = new T.Mesh(geo, mat); m.position.set(x, y, z);
    m.castShadow = sh !== false; m.receiveShadow = true; (g || apt).add(m); return m;
  }
  function box(w, h, d, x, y, z, mat, g, sh) { return mesh(new T.BoxGeometry(w, h, d), mat, x, y, z, g, sh); }
  function uvScale(geo, w, h, d, unit) { // escala as UVs de cada face pelo tamanho real (1 repetição = unit metros)
    var uv = geo.attributes.uv, dims = [[d, h], [d, h], [w, d], [w, d], [w, h], [w, h]];
    for (var f = 0; f < 6; f++) for (var i = 0; i < 4; i++) { var k = f * 4 + i; uv.setXY(k, uv.getX(k) * dims[f][0] / unit, uv.getY(k) * dims[f][1] / unit); }
    uv.needsUpdate = true; return geo;
  }
  function rbox(w, h, d, r, x, y, z, mat, g) { return mesh(new T.RoundedBoxGeometry(w, h, d, 3, Math.min(r, w / 2, h / 2, d / 2)), mat, x, y, z, g); }
  function cyl(r1, r2, h, x, y, z, mat, g, seg) { return mesh(new T.CylinderGeometry(r1, r2, h, seg || 32), mat, x, y, z, g); }

  // ---------- planta técnica (mesma imagem da planta 2D do site, alinhada às coordenadas reais)
  var planTex; pending.push(new Promise(function (ok) { planTex = TL.load('assets/planta-apto-2x.png', function () { ok(); }); }));
  planTex.encoding = T.sRGBEncoding; planTex.anisotropy = 8;
  var PX0 = -132 / 70, PX1 = (957 - 132) / 70, PZ0 = -110 / 70, PZ1 = (757 - 110) / 70;
  var planMat = new T.MeshBasicMaterial({map: planTex, transparent: true, opacity: 1, toneMapped: false});
  var planMesh = new T.Mesh(new T.PlaneGeometry(PX1 - PX0, PZ1 - PZ0), planMat);
  planMesh.rotation.x = -Math.PI / 2; planMesh.position.set((PX0 + PX1) / 2, 0.03, (PZ0 + PZ1) / 2); gPlan.add(planMesh);

  // ---------- pisos
  function floors(g, raw) {
    P.rooms.forEach(function (r) {
      var mat = raw ? CLAY.floor : floorMatOf[r.floor];
      var f = mesh(uvScale(new T.BoxGeometry(r.w, 0.05, r.d), r.w, 0.05, r.d, r.floor === 'wood' ? 1.8 : 1.3), mat, r.x + r.w / 2, -0.025, r.y + r.d / 2, g); f.castShadow = false;
    });
  }
  // ---------- paredes com vãos
  var lintel = function (o) { return o.h || 2.1; };
  function walls(g, raw) {
    P.walls.forEach(function (w, i) {
      var x1 = w[0], y1 = w[1], x2 = w[2], y2 = w[3], L = Math.hypot(x2 - x1, y2 - y1), ux = (x2 - x1) / L, uy = (y2 - y1) / L, horiz = Math.abs(ux) > 0.5;
      function seg(a, b, y0, h) {
        if (b - a < 0.01) return; if (h <= 0.001) return;
        var mx = x1 + ux * (a + b) / 2, mz = y1 + uy * (a + b) / 2;
        var mats = wallMats(i, raw, horiz);
        var bw = horiz ? (b - a) : P.T, bd = horiz ? P.T : (b - a);
        var m = new T.Mesh(uvScale(new T.BoxGeometry(bw, h, bd), bw, h, bd, 0.9), mats);
        m.position.set(mx, y0 + h / 2, mz); m.castShadow = true; m.receiveShadow = true; m.userData.wall = true; g.add(m);
      }
      var ops = P.openings.filter(function (o) { return o.w === i; }).sort(function (a, b) { return a.a - b.a; });
      var cur = 0;
      ops.forEach(function (o) {
        seg(cur, o.a, 0, Hh);
        if (o.type === 'window') { seg(o.a, o.b, 0, o.sill); seg(o.a, o.b, o.sill + o.h, Hh - o.sill - o.h); }
        else seg(o.a, o.b, lintel(o), Hh - lintel(o));
        cur = o.b;
      });
      seg(cur, L, 0, Hh);
    });
  }
  // faces do BoxGeometry: +x, -x, +y, -y, +z, -z
  function wallMats(i, raw, horiz) {
    if (raw) return [CLAY.wall, CLAY.wall, CLAY.cap, CLAY.wall, CLAY.wall, CLAY.wall];
    var a = [FIN.wall, FIN.wall, FIN.cap, FIN.wall, FIN.wall, FIN.wall];
    if (i === 8) a[4] = FIN.accent;           // parede da TV (lado do estar)
    if (i === 1) a[1] = FIN.wall;
    if (i === 6) a[5] = FIN.bath;             // banheiro (lado de dentro)
    if (i === 4) a[0] = FIN.bath;             // banheiro: parede esquerda (lado leste)
    if (i === 5) { a[1] = FIN.bath; a[0] = FIN.bedroom; } // banheiro / dormitório casal
    if (i === 0) { a[4] = FIN.wall; }
    return a;
  }
  // ---------- esquadrias, portas e vidros
  function openingsBuild(g, raw) {
    P.openings.forEach(function (o) {
      var w = P.walls[o.w], x1 = w[0], y1 = w[1], x2 = w[2], y2 = w[3], L = Math.hypot(x2 - x1, y2 - y1), ux = (x2 - x1) / L, uy = (y2 - y1) / L, horiz = Math.abs(ux) > 0.5;
      var len = o.b - o.a, mx = x1 + ux * (o.a + o.b) / 2, mz = y1 + uy * (o.a + o.b) / 2;
      var fr = raw ? CLAY.frame : FIN.frame, ft = 0.045;
      function bar(along, h, y, off) { // barra ao longo da parede
        var px = mx + ux * off, pz = mz + uy * off;
        box(horiz ? along : 0.07, h, horiz ? 0.07 : along, px, y, pz, fr, g);
      }
      if (o.type === 'window') {
        bar(len, ft, o.sill + ft / 2, 0); bar(len, ft, o.sill + o.h - ft / 2, 0);
        bar(ft, o.h, o.sill + o.h / 2, -len / 2 + ft / 2); bar(ft, o.h, o.sill + o.h / 2, len / 2 - ft / 2);
        if (len > 1) bar(ft, o.h, o.sill + o.h / 2, 0);
        var gl = new T.Mesh(new T.BoxGeometry(horiz ? len : 0.012, o.h, horiz ? 0.012 : len), glassMat);
        gl.position.set(mx, o.sill + o.h / 2, mz); gl.userData.glass = true; gGlass.add(gl);
        // peitoril
        box(horiz ? len + 0.06 : 0.2, 0.03, horiz ? 0.2 : len + 0.06, mx, o.sill - 0.015, mz, raw ? CLAY.frame : FIN.marble, g);
      } else if (o.slide) {
        var hh = lintel(o);
        bar(len, ft, hh - ft / 2, 0);
        // duas folhas de correr: uma fechada, outra parcialmente aberta (sobreposta)
        [[-len / 4, -0.03], [len / 4 - len * 0.18, 0.03]].forEach(function (s) {
          var pw = len / 2, px = mx + ux * s[0] + (horiz ? 0 : s[1]), pz = mz + uy * s[0] + (horiz ? s[1] : 0);
          var gl = new T.Mesh(new T.BoxGeometry(horiz ? pw - 0.08 : 0.012, hh - 0.1, horiz ? 0.012 : pw - 0.08), glassMat);
          gl.position.set(px, hh / 2, pz); gGlass.add(gl);
          box(horiz ? pw : 0.05, 0.05, horiz ? 0.05 : pw, px, 0.03, pz, fr, g);
          box(horiz ? pw : 0.05, 0.05, horiz ? 0.05 : pw, px, hh - 0.08, pz, fr, g);
          box(horiz ? 0.05 : 0.05, hh - 0.1, horiz ? 0.05 : 0.05, px - ux * (pw / 2 - 0.025), hh / 2, pz - uy * (pw / 2 - 0.025), fr, g);
          box(horiz ? 0.05 : 0.05, hh - 0.1, horiz ? 0.05 : 0.05, px + ux * (pw / 2 - 0.025), hh / 2, pz + uy * (pw / 2 - 0.025), fr, g);
        });
      } else {
        var hd = lintel(o), sw = o.swing || 1, nx = -uy * sw, nz = ux * sw;
        var bx = x1 + ux * o.b, bz = y1 + uy * o.b;
        // batentes
        var dm = raw ? CLAY.door : FIN.lacquer;
        box(horiz ? len : P.T + 0.02, 0.05, horiz ? P.T + 0.02 : len, mx, hd + 0.025, mz, dm, g);
        // folha aberta a 90° (igual à planta 2D)
        var leafMat = raw ? CLAY.door : (o.w === 2 ? FIN.oakDoor : FIN.door);
        var lw = len - 0.04, lx = bx + nx * lw / 2, lz = bz + nz * lw / 2;
        var horizLeaf = Math.abs(nx) > 0.5;
        box(horizLeaf ? lw : 0.04, hd - 0.02, horizLeaf ? 0.04 : lw, lx, (hd - 0.02) / 2, lz, leafMat, g);
        if (!raw) { var hx = bx + nx * (lw - 0.08), hz = bz + nz * (lw - 0.08); box(horizLeaf ? 0.02 : 0.06, 0.02, horizLeaf ? 0.06 : 0.02, hx, 1.0, hz, FIN.chrome, g); }
      }
    });
  }
  floors(gRawF, true); walls(gRaw, true); openingsBuild(gRaw, true);
  floors(gFinF, false); walls(gFin, false); openingsBuild(gFin, false);
  // forro (só nas cenas internas)
  box(8.25, 0.08, 8.25, 3.75, Hh + 0.04, 4.05, M(0xf7f5f0, 0.95), gCeil, false).receiveShadow = true;
  box(1.4, 0.12, 3.7, 8.8, Hh + 0.06, 4.85, M(0xe9e6df, 0.9), gCeil);
  [[2.0, 1.6], [6.5, 1.6], [3.8, 4.9], [6.4, 4.9], [1.3, 4.9], [3.8, 0.9]].forEach(function (p) { cyl(0.05, 0.05, 0.015, p[0], Hh - 0.008, p[1], M(0xffffff, 0.3, {emissive: 0xfff3dc, emissiveIntensity: 0.6}), gCeil); });
  // guarda-corpo de vidro da varanda (arquitetura: aparece desde o nível 1)
  [[0.03, 1.05, 3.7, 9.48, 0.55, 4.85], [1.4, 1.05, 0.03, 8.8, 0.55, 3.02], [1.4, 1.05, 0.03, 8.8, 0.55, 6.68]].forEach(function (b) {
    var gl = new T.Mesh(new T.BoxGeometry(b[0], b[1], b[2]), glassMat); gl.position.set(b[3], b[4], b[5]); gGlass.add(gl);
  });
  [[0.05, 0.04, 3.72, 9.48, 1.1, 4.85], [1.42, 0.04, 0.05, 8.8, 1.1, 3.02], [1.42, 0.04, 0.05, 8.8, 1.1, 6.68]].forEach(function (b) { box(b[0], b[1], b[2], b[3], b[4], b[5], FIN.frame, gRaw); box(b[0], b[1], b[2], b[3], b[4], b[5], FIN.frame, gFin); });
  // portas dos elevadores (hall do andar)
  [0.35, 1.55].forEach(function (x) { box(0.9, 2.1, 0.03, x, 1.05, 8.0, CLAY.frame, gRaw); box(0.9, 2.1, 0.03, x, 1.05, 8.0, FIN.metal, gFin); });

  // ---------- mobiliário: cada item é um grupo com ordem de entrada (para a montagem progressiva)
  var items = [];
  function item(set, order, build) {
    var g = new T.Group(); (set === 'basic' ? gBasic : gDecor).add(g);
    var saved = apt; apt = g; build(); apt = saved;
    var c = new T.Box3().setFromObject(g).getCenter(new T.Vector3());
    // pivô no centro da base para a animação de escala
    g.children.forEach(function (ch) { ch.position.x -= c.x; ch.position.z -= c.z; });
    g.position.set(c.x, 0, c.z); g.userData = {set: set, order: order, base: g.position.clone()};
    items.push(g); return g;
  }
  function cloth(c, id, rep) { var m = M(c, 1); m.normalMap = tex(id, 'nor_gl', [rep, rep]); m.normalScale.set(0.8, 0.8); return m; }
  var fab = {
    sofa: cloth(0xcbc2b4, 'wool_boucle', 3), linen: cloth(0xf3efe8, 'rough_linen', 3), throw: cloth(0x8e7a63, 'knitted_fleece', 3),
    rugA: cloth(0xc9bda9, 'wool_boucle', 5), rugB: cloth(0xa99c88, 'knitted_fleece', 4),
    green: M(0x51693f, 0.85), green2: M(0x6c8551, 0.85), terracotta: M(0xa87862, 0.9), ceramic: M(0xe8e2d8, 0.4), black: M(0x1b1b1d, 0.6),
    sage: M(0x8f9b86, 0.95), caramel: M(0xb39274, 0.8), cream: M(0xefe6d6, 0.95)
  };
  var lampMat = new T.MeshStandardMaterial({color: 0xfff4e2, emissive: 0xffd9a8, emissiveIntensity: 0, roughness: 0.6});
  var lamps = [];
  function lampLight(x, y, z, dist) { var p = new T.PointLight(0xffc98a, 0, dist || 5, 2); p.position.set(x, y, z); apt.add(p); lamps.push(p); return p; }
  function plant(x, z, s, potMat) {
    s = s || 1;
    cyl(0.17 * s, 0.13 * s, 0.4 * s, x, 0.2 * s, z, potMat || fab.ceramic);
    var leaves = [[0, 0.75, 0, 0.3], [0.13, 0.95, 0.05, 0.22], [-0.12, 0.9, -0.06, 0.24], [0.04, 1.12, -0.04, 0.18], [-0.05, 0.62, 0.12, 0.2]];
    leaves.forEach(function (l, i) {
      var m = mesh(new T.IcosahedronGeometry(l[3] * s, 1), i % 2 ? fab.green : fab.green2, x + l[0] * s, l[1] * s, z + l[2] * s);
      m.scale.y = 1.15;
    });
  }
  function curtain(x0, z0, x1, z1, h, mat) { // painel pregueado do forro ao piso
    var L = Math.hypot(x1 - x0, z1 - z0), segs = Math.max(8, Math.round(L * 14));
    var geo = new T.PlaneGeometry(L, h, segs, 1), pos = geo.attributes.position;
    for (var i = 0; i < pos.count; i++) { pos.setZ(i, Math.sin(pos.getX(i) * 22) * 0.035); }
    geo.computeVertexNormals();
    var m = new T.Mesh(geo, mat); m.position.set((x0 + x1) / 2, h / 2, (z0 + z1) / 2); m.rotation.y = -Math.atan2(z1 - z0, x1 - x0);
    m.castShadow = true; m.receiveShadow = true; apt.add(m); return m;
  }
  var sheer = new T.MeshStandardMaterial({color: 0xf5f1ea, roughness: 1, transparent: true, opacity: 0.78, side: T.DoubleSide});
  var sheerSolid = new T.MeshStandardMaterial({color: 0xd9cfbf, roughness: 1, side: T.DoubleSide});
  function art(x, y, z, w, h, axis, colors) { // quadro com moldura
    var g = axis === 'x' || axis === 'x-';
    box(g ? w : 0.03, h, g ? 0.03 : w, x, y, z, fab.black);
    var c = document.createElement('canvas'); c.width = 256; c.height = Math.round(256 * h / w); var k = c.getContext('2d');
    k.fillStyle = colors[0]; k.fillRect(0, 0, c.width, c.height);
    k.fillStyle = colors[1]; k.beginPath(); k.arc(c.width * 0.38, c.height * 0.55, c.width * 0.26, 0, Math.PI * 2); k.fill();
    k.fillStyle = colors[2]; k.fillRect(c.width * 0.55, c.height * 0.18, c.width * 0.22, c.height * 0.64);
    var t = new T.CanvasTexture(c); t.encoding = T.sRGBEncoding;
    var pm = new T.MeshStandardMaterial({map: t, roughness: 0.9});
    var pl = new T.Mesh(new T.PlaneGeometry(w - 0.08, h - 0.08), pm); pl.position.set(x, y, z);
    if (axis === 'x') pl.position.z += 0.017; else if (axis === 'x-') { pl.rotation.y = Math.PI; pl.position.z -= 0.017; } else if (axis === 'z+') { pl.rotation.y = Math.PI / 2; pl.position.x += 0.017; } else { pl.rotation.y = -Math.PI / 2; pl.position.x -= 0.017; }
    apt.add(pl);
  }

  // ===== BÁSICO (nível 2: escala) — mesmas posições do tour do site
  // dormitório
  item('basic', 1, function () { box(0.95, 0.3, 1.95, 0.6, 0.15, 1.15, FIN.oak); rbox(0.9, 0.2, 1.9, 0.05, 0.6, 0.4, 1.17, fab.linen); });
  item('basic', 2, function () { box(0.6, 0.04, 1.1, 2.38, 0.75, 0.9, FIN.oak); box(0.04, 0.73, 1.0, 2.1, 0.37, 0.9, FIN.oak); });
  item('basic', 3, function () { box(1.8, 2.2, 0.58, 1.05, 1.1, 2.88, FIN.lacquer); });
  // banheiro
  item('basic', 4, function () {
    box(0.9, 0.02, 0.9, 4.4, 0.01, 0.5, M(0xbfc4c4, 0.2));
    var g = new T.Mesh(new T.BoxGeometry(0.012, 2.0, 0.9), glassMat); g.position.set(3.93, 1.0, 0.5); apt.add(g);
    box(0.02, 2.0, 0.02, 3.93, 1.0, 0.06, FIN.chrome); rbox(0.38, 0.4, 0.55, 0.08, 3.1, 0.2, 0.38, FIN.lacquer); rbox(0.38, 0.32, 0.16, 0.04, 3.1, 0.58, 0.1, FIN.lacquer);
    box(0.45, 0.5, 0.9, 2.95, 0.55, 1.4, FIN.walnut); box(0.47, 0.03, 0.92, 2.95, 0.815, 1.4, FIN.marble); cyl(0.16, 0.14, 0.12, 2.95, 0.88, 1.4, FIN.lacquer);
    box(0.02, 0.8, 0.7, 2.78, 1.5, 1.4, M(0xdfe9ee, 0.02, {metalness: 0.9}));
  });
  // dormitório casal
  item('basic', 5, function () { box(1.75, 0.3, 2.05, 7.05, 0.15, 1.6, FIN.oak); box(1.65, 0.3, 1.95, 7.02, 0.41, 1.6, fab.linen); });
  item('basic', 6, function () { box(0.6, 2.2, 1.9, 5.22, 1.1, 1.1, FIN.oak); });
  // cozinha
  item('basic', 7, function () {
    box(0.62, 0.86, 2.4, 0.31, 0.43, 4.6, FIN.lacquer); box(0.64, 0.04, 2.42, 0.32, 0.88, 4.6, FIN.marble);
    box(0.5, 0.012, 0.58, 0.32, 0.906, 3.9, fab.black); box(0.45, 0.02, 0.5, 0.32, 0.9, 5.2, FIN.metal);
    box(0.36, 0.7, 1.0, 0.18, 1.95, 3.95, FIN.lacquer);
    box(0.68, 1.95, 0.72, 0.36, 0.98, 6.25, M(0xcfd0d2, 0.25, {metalness: 0.6}));
    box(0.9, 0.88, 1.6, 1.85, 0.44, 4.85, FIN.walnut); box(1.0, 0.04, 1.7, 1.85, 0.9, 4.85, FIN.marble);
  });
  // jantar
  item('basic', 8, function () {
    cyl(0.5, 0.5, 0.04, 3.8, 0.75, 4.9, FIN.oak, null, 48); cyl(0.05, 0.18, 0.73, 3.8, 0.37, 4.9, fab.black);
    [[3.15, 4.9, 1], [4.45, 4.9, -1], [3.8, 4.25, 0], [3.8, 5.55, 2]].forEach(function (p) { rbox(0.44, 0.06, 0.44, 0.02, p[0], 0.46, p[1], fab.sofa); box(0.03, 0.44, 0.03, p[0], 0.22, p[1], fab.black); });
  });
  // estar
  item('basic', 9, function () {
    rbox(2.2, 0.42, 0.95, 0.08, 6.4, 0.21, 5.75, fab.sofa); rbox(2.2, 0.48, 0.22, 0.08, 6.4, 0.6, 6.13, fab.sofa);
    rbox(0.22, 0.6, 0.95, 0.08, 5.3, 0.3, 5.75, fab.sofa); rbox(0.22, 0.6, 0.95, 0.08, 7.5, 0.3, 5.75, fab.sofa);
  });
  item('basic', 10, function () { box(1.8, 0.45, 0.42, 6.5, 0.26, 3.45, FIN.walnut); box(1.4, 0.8, 0.04, 6.5, 1.12, 3.3, M(0x0c0c0d, 0.15)); });
  // varanda
  item('basic', 11, function () { cyl(0.3, 0.3, 0.03, 8.85, 0.72, 4.2, FIN.oak); cyl(0.03, 0.03, 0.7, 8.85, 0.35, 4.2, fab.black); });

  // ===== DECORADO (nível 3 e cinematic): o que transforma o espaço em lugar para viver
  // estar
  item('decor', 1, function () { box(2.7, 0.012, 2.0, 6.4, 0.006, 4.9, fab.rugA); });
  item('decor', 2, function () {
    rbox(0.95, 0.14, 0.78, 0.06, 5.88, 0.48, 5.68, fab.cream); rbox(0.95, 0.14, 0.78, 0.06, 6.9, 0.48, 5.68, fab.cream);
    rbox(0.45, 0.4, 0.14, 0.06, 5.55, 0.78, 6.0, fab.sage); rbox(0.45, 0.4, 0.14, 0.06, 7.2, 0.78, 6.0, fab.caramel); rbox(0.42, 0.38, 0.13, 0.06, 6.35, 0.76, 6.0, fab.cream);
    box(0.6, 0.03, 0.9, 7.15, 0.57, 5.65, fab.throw);
  });
  item('decor', 3, function () { cyl(0.42, 0.42, 0.04, 6.4, 0.38, 4.55, FIN.walnut, null, 48); cyl(0.36, 0.36, 0.34, 6.4, 0.17, 4.55, FIN.walnut, null, 48); box(0.3, 0.04, 0.22, 6.3, 0.42, 4.5, fab.cream); box(0.26, 0.04, 0.2, 6.31, 0.46, 4.5, fab.sage); cyl(0.07, 0.05, 0.2, 6.55, 0.5, 4.62, fab.ceramic); });
  item('decor', 4, function () { cyl(0.012, 0.012, 1.55, 5.05, 0.78, 6.4, fab.black); cyl(0.16, 0.16, 0.02, 5.05, 0.01, 6.4, fab.black); var s = mesh(new T.SphereGeometry(0.17, 24, 16), lampMat, 5.05, 1.6, 6.4); s.castShadow = false; lampLight(5.05, 1.55, 6.4, 4.5); });
  item('decor', 5, function () { art(6.5, 1.9, 3.29, 0.9, 0.6, 'x', ['#e8dfd1', '#c9a777', '#5f6b5a']); box(0.22, 0.25, 0.22, 7.1, 0.62, 3.45, fab.terracotta); cyl(0.06, 0.08, 0.3, 5.9, 0.64, 3.45, fab.ceramic); box(0.25, 0.06, 0.18, 6.0, 0.51, 3.45, fab.sage); });
  item('decor', 6, function () { curtain(8.0, 3.3, 8.0, 3.7, Hh - 0.02, sheer); curtain(8.0, 5.96, 8.0, 6.58, Hh - 0.02, sheer); });
  item('decor', 7, function () { plant(7.7, 3.6, 1.1, fab.terracotta); });
  // jantar
  item('decor', 8, function () { cyl(0.005, 0.005, 0.6, 3.8, Hh - 0.3, 4.9, fab.black); var s = mesh(new T.SphereGeometry(0.22, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2), M(0x1e1e20, 0.5, {side: T.DoubleSide}), 3.8, 2.05, 4.9); s.castShadow = false; var b = mesh(new T.SphereGeometry(0.07, 16, 12), lampMat, 3.8, 2.02, 4.9); b.castShadow = false; lampLight(3.8, 1.9, 4.9, 4); });
  item('decor', 9, function () { cyl(0.09, 0.07, 0.18, 3.75, 0.86, 4.85, fab.ceramic); [[0, 0], [0.05, 0.04], [-0.04, 0.05]].forEach(function (o) { mesh(new T.SphereGeometry(0.05, 10, 8), fab.green2, 3.75 + o[0], 1.0, 4.85 + o[1]); }); box(0.35, 0.01, 0.25, 3.55, 0.775, 5.1, fab.cream); });
  item('decor', 10, function () { box(0.9, 0.012, 1.4, 3.8, 0.006, 4.9, fab.rugB); });
  // cozinha
  item('decor', 11, function () { [4.4, 5.3].forEach(function (z) { cyl(0.18, 0.18, 0.05, 2.55, 0.66, z, fab.caramel); cyl(0.015, 0.015, 0.64, 2.55, 0.33, z, fab.black); cyl(0.17, 0.17, 0.01, 2.55, 0.01, z, fab.black); }); });
  item('decor', 12, function () { [4.4, 5.3].forEach(function (z) { cyl(0.004, 0.004, 0.75, 1.85, Hh - 0.37, z, fab.black); var s = mesh(new T.ConeGeometry(0.12, 0.2, 24, 1, true), M(0xc9a26a, 0.35, {metalness: 0.6, side: T.DoubleSide}), 1.85, 1.85, z); s.castShadow = false; lampLight(1.85, 1.75, z, 3); }); });
  item('decor', 13, function () { box(0.32, 0.03, 0.22, 0.32, 0.915, 4.4, FIN.walnut); cyl(0.05, 0.05, 0.18, 0.25, 0.99, 4.45, fab.ceramic); cyl(0.12, 0.1, 0.08, 1.85, 0.96, 4.95, fab.ceramic); [0, 1, 2].forEach(function (i) { mesh(new T.SphereGeometry(0.035, 10, 8), fab.terracotta, 1.82 + i * 0.04, 1.02, 4.95); }); });
  // dormitório casal
  item('decor', 14, function () {
    rbox(1.0, 0.05, 1.7, 0.03, 6.5, 0.58, 1.6, fab.throw);
    [1.25, 1.95].forEach(function (z) { rbox(0.2, 0.36, 0.55, 0.07, 7.82, 0.72, z, fab.cream); });
    [1.3, 1.9].forEach(function (z) { rbox(0.16, 0.3, 0.45, 0.07, 7.65, 0.69, z, fab.sage); });
    box(0.07, 1.15, 2.0, 8.03, 0.95, 1.6, M(0x8b7a66, 0.95));
  });
  item('decor', 15, function () { [0.45, 2.75].forEach(function (z) { box(0.42, 0.48, 0.42, 7.82, 0.24, z, FIN.walnut); cyl(0.07, 0.09, 0.22, 7.82, 0.6, z, fab.ceramic); var s = mesh(new T.CylinderGeometry(0.11, 0.13, 0.16, 24, 1, true), M(0xf3ead9, 0.9, {side: T.DoubleSide, emissive: 0xffd9a8, emissiveIntensity: 0}), 7.82, 0.78, z); s.userData.shade = true; lampLight(7.82, 0.85, z, 3); }); });
  item('decor', 16, function () { box(1.4, 0.012, 2.3, 6.1, 0.006, 1.6, fab.rugB); });
  item('decor', 17, function () { curtain(5.0, 0.08, 7.95, 0.08, Hh - 0.02, sheerSolid); });
  item('decor', 18, function () { art(5.55, 1.55, 3.11, 0.5, 0.7, 'x-', ['#ebe4d9', '#b8a68c', '#6e7b6a']); plant(5.65, 2.75, 0.9, fab.ceramic); });
  // dormitório
  item('decor', 19, function () { rbox(0.88, 0.05, 1.0, 0.03, 0.6, 0.53, 1.5, fab.sage); rbox(0.55, 0.12, 0.34, 0.05, 0.6, 0.58, 0.38, fab.cream); box(0.45, 0.5, 0.4, 1.35, 0.25, 0.3, FIN.walnut); var s = mesh(new T.SphereGeometry(0.09, 16, 12), lampMat, 1.35, 0.62, 0.3); s.castShadow = false; lampLight(1.35, 0.7, 0.3, 2.5); });
  item('decor', 20, function () { rbox(0.45, 0.45, 0.45, 0.06, 1.9, 0.23, 1.0, fab.caramel); box(0.03, 0.3, 0.45, 2.6, 1.0, 0.9, fab.black); box(0.2, 0.06, 0.3, 2.3, 0.8, 0.6, fab.cream); });
  item('decor', 21, function () { box(1.2, 0.012, 0.8, 1.5, 0.006, 1.3, fab.rugA); curtain(0.5, 0.08, 2.2, 0.08, Hh - 0.02, sheerSolid); art(0.08, 1.6, 1.15, 0.55, 0.75, 'z+', ['#efe9df', '#c69b6d', '#7c8a78']); });
  // banheiro
  item('decor', 22, function () { box(0.03, 0.5, 0.3, 2.74, 1.3, 0.55, fab.cream); cyl(0.04, 0.04, 0.16, 2.95, 0.92, 1.15, fab.black); plant(3.55, 1.75, 0.45, fab.ceramic); });
  // varanda
  item('decor', 23, function () { [3.6, 4.8].forEach(function (z) { rbox(0.46, 0.08, 0.46, 0.03, 8.85, 0.45, z, fab.cream); box(0.46, 0.4, 0.04, 8.85, 0.65, z + (z < 4.2 ? -0.21 : 0.21), FIN.oak); [[-0.2, -0.2], [0.2, -0.2], [-0.2, 0.2], [0.2, 0.2]].forEach(function (o) { box(0.03, 0.42, 0.03, 8.85 + o[0], 0.21, z + o[1], fab.black); }); }); });
  item('decor', 24, function () { plant(9.15, 6.3, 1.0, fab.terracotta); plant(9.15, 3.35, 0.75, fab.ceramic); cyl(0.12, 0.1, 0.12, 8.85, 0.8, 4.2, fab.ceramic); });
  // hall do andar
  item('decor', 25, function () { plant(7.75, 7.75, 0.8, fab.ceramic); });

  // ---------- estúdio (fundo escuro elegante nas vistas de cima)
  var studioFloor = new T.Mesh(new T.PlaneGeometry(400, 400), new T.ShadowMaterial({opacity: 0.55}));
  studioFloor.rotation.x = -Math.PI / 2; studioFloor.position.y = -0.06; studioFloor.receiveShadow = true; gStudio.add(studioFloor);
  var slab = box(10.4, 0.22, 8.4, 4.45, -0.16, 4.05, M(0x1a1a1d, 0.95, {envMapIntensity: 0.15}), gStudio); slab.castShadow = false;

  // ---------- torre conceitual (cinematic): o apartamento real fica no 7º andar
  var FLOORS = 12, FH = 2.9, BASE = 4.2, FEAT = 7, aptY = BASE + (FEAT - 1) * FH + 0.22;
  var towerGlass = [];
  (function () {
    var white = M(0xf1eee8, 0.7), slabM = M(0xe7e3dc, 0.85), concrete = M(0xcfcac2, 0.9);
    var gA = new T.MeshStandardMaterial({color: 0x52646f, roughness: 0.08, metalness: 0.5, emissive: 0xffc68a, emissiveIntensity: 0});
    var gB = new T.MeshStandardMaterial({color: 0x5d717d, roughness: 0.08, metalness: 0.5, emissive: 0xffc68a, emissiveIntensity: 0});
    towerGlass.push(gA, gB);
    var rail = new T.MeshStandardMaterial({color: 0xcfe0e6, transparent: true, opacity: 0.35, roughness: 0.05});
    var x0 = -13.3, x1 = 8.1, z0 = 0, z1 = 14.8, Wt = x1 - x0, Dt = z1 - z0, cx = (x0 + x1) / 2, cz = (z0 + z1) / 2;
    var ground = new T.Mesh(new T.PlaneGeometry(1200, 1200), M(0x3b4233, 1)); ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; gTower.add(ground);
    box(Wt + 20, 0.08, Dt + 18, cx, 0.04, cz, M(0xd2ccc2, 0.9), gTower);
    box(Wt - 1.2, BASE - 0.3, Dt - 1.2, cx, (BASE - 0.3) / 2, cz, gA, gTower);
    box(Wt + 0.6, 0.35, Dt + 0.6, cx, BASE - 0.15, cz, white, gTower);
    var bal = [[8.1, 9.5, 3.0, 6.7], [8.1, 9.5, 8.1, 11.8], [-14.7, -13.3, 3.0, 6.7], [-14.7, -13.3, 8.1, 11.8]];
    for (var f = 0; f < FLOORS; f++) {
      var y = BASE + f * FH, feat = f === FEAT - 1;
      box(Wt, 0.22, Dt, cx, y + 0.11, cz, slabM, gTower);
      if (feat) { // o andar da unidade: fecha só as outras três unidades e o núcleo
        box(Wt - 0.3 - 8.4, FH - 0.22, Dt - 0.3, cx - 4.2, y + 0.22 + (FH - 0.22) / 2, cz, gA, gTower);
        box(8.4, FH - 0.22, Dt - 0.3 - 8.4, 4.05, y + 0.22 + (FH - 0.22) / 2, cz + 4.2, gB, gTower);
      } else box(Wt - 0.3, FH - 0.22, Dt - 0.3, cx, y + 0.22 + (FH - 0.22) / 2, cz, (f * 7) % 3 === 0 ? gB : gA, gTower);
      bal.forEach(function (b, bi) {
        if (feat) { if (bi === 0) return; }
        box(b[1] - b[0], 0.18, b[3] - b[2], (b[0] + b[1]) / 2, y + 0.09, (b[2] + b[3]) / 2, slabM, gTower);
        var ox = b[0] < 0 ? b[0] : b[1];
        var gl = new T.Mesh(new T.BoxGeometry(0.04, 1.05, b[3] - b[2]), rail); gl.position.set(ox, y + 0.75, (b[2] + b[3]) / 2); gTower.add(gl);
      });
    }
    box(Wt, 0.22, Dt, cx, BASE + FLOORS * FH + 0.11, cz, slabM, gTower);
    for (var i = 0; i <= 15; i++) {
      var fx = x0 + 0.4 + i * (Wt - 0.8) / 15;
      box(0.16, FLOORS * FH, 0.45, fx, BASE + FLOORS * FH / 2, z0 - 0.24, white, gTower);
      box(0.16, FLOORS * FH, 0.45, fx, BASE + FLOORS * FH / 2, z1 + 0.24, white, gTower);
    }
    box(Wt + 0.6, 0.6, Dt + 0.6, cx, BASE + FLOORS * FH + 0.3, cz, white, gTower);
    box(6, 2.6, 5, -2.6, BASE + FLOORS * FH + 1.9, cz, concrete, gTower);
    [[-24, -8], [-10, -9], [4, -9], [16, 1], [16, 13], [-28, 10], [-6, 24], [9, 23], [-20, 22], [22, -6]].forEach(function (p, k) {
      var tr = new T.Mesh(new T.IcosahedronGeometry(2.3 + (k % 3) * 0.4, 1), k % 2 ? fab.green : fab.green2); tr.position.set(p[0], 3.6, p[1]); tr.castShadow = true; gTower.add(tr);
      box(0.3, 2.6, 0.3, p[0], 1.3, p[1], M(0x6f5137, 0.8), gTower);
    });
  })();

  // ---------- céu de entardecer (vistas externas do edifício)
  var skyU = {top: {value: new T.Color(0x1d2a44)}, mid: {value: new T.Color(0xc98d63)}, bot: {value: new T.Color(0x2b2622)}, k: {value: 0}, cloud: {value: 0}};
  var sky = new T.Mesh(new T.SphereGeometry(600, 32, 16), new T.ShaderMaterial({side: T.BackSide, depthWrite: false, uniforms: skyU,
    vertexShader: 'varying vec3 vp; void main(){ vp = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }',
    fragmentShader: [
      'uniform vec3 top; uniform vec3 mid; uniform vec3 bot; uniform float cloud; varying vec3 vp;',
      'float h(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }',
      'float n(vec2 p){ vec2 i = floor(p), f = fract(p); f = f*f*(3.0-2.0*f); return mix(mix(h(i), h(i+vec2(1.0,0.0)), f.x), mix(h(i+vec2(0.0,1.0)), h(i+vec2(1.0,1.0)), f.x), f.y); }',
      'float fbm(vec2 p){ float v = 0.0, a = 0.5; for (int i = 0; i < 5; i++) { v += a * n(p); p *= 2.03; a *= 0.5; } return v; }',
      'void main(){ float y = vp.y; vec3 c = y > 0.0 ? mix(mid, top, pow(clamp(y*2.2,0.0,1.0),0.7)) : mix(mid, bot, clamp(-y*6.0,0.0,1.0));',
      ' if (cloud > 0.0 && y > 0.02) { vec2 q = vp.xz / (y + 0.12) * 2.6; float d = fbm(q + vec2(3.1, 7.7)) * 0.75 + fbm(q * 3.0) * 0.25; float m = smoothstep(0.5, 0.66, d) * smoothstep(0.02, 0.25, y) * cloud; vec3 cc = mix(vec3(0.82,0.86,0.88), vec3(1.0), smoothstep(0.55, 0.9, d)); c = mix(c, cc, m); }',
      ' gl_FragColor = vec4(c,1.0); }'].join('\n')}));
  sky.visible = false; S.add(sky);
  var fogGold = new T.Fog(0xb98a68, 90, 420), fogDusk = new T.Fog(0x4a4256, 80, 380);
  // ---------- ambiente HDRI (luz e vista pelas janelas)
  var pm = new T.PMREMGenerator(R), envs = {}, bgs = {};
  function loadHDR(name) {
    return new Promise(function (ok) {
      new T.RGBELoader().setDataType(T.UnsignedByteType).load('assets/' + name + '.hdr', function (t) {
        envs[name] = pm.fromEquirectangular(t).texture; t.mapping = T.EquirectangularReflectionMapping; bgs[name] = t; ok();
      });
    });
  }
  var ready = Promise.all([loadHDR('rooftop_day'), loadHDR('shanghai_riverside')].concat(pending)).then(function () { return new Promise(function (ok) { setTimeout(ok, 300); }); });

  // ---------- pós-processamento (profundidade de campo só quando pedida)
  var composer = new T.EffectComposer(R);
  composer.addPass(new T.RenderPass(S, cam));
  var bokeh = new T.BokehPass(S, cam, {focus: 3, aperture: 0.0002, maxblur: 0.006, width: W, height: H});
  composer.addPass(bokeh);

  // ---------- estado
  var ease = function (x) { x = Math.max(0, Math.min(1, x)); return x * x * (3 - 2 * x); };
  var prevEnv = null;
  function setState(s) {
    // planta e volumetria
    planMat.opacity = s.plan === undefined ? 0 : s.plan; gPlan.visible = planMat.opacity > 0.001;
    var rise = s.rise === undefined ? 1 : s.rise;
    [gRaw, gFin].forEach(function (g) { g.scale.y = Math.max(0.002, rise); });
    gRawF.visible = true;
    gGlass.visible = rise > 0.98;
    // acabamentos: varredura (pisos e paredes em tempos diferentes)
    var sw0 = -1.2, sw1 = 11.5, scanAt = null;
    [[cpF, gRawF, gFinF, s.finishFloor || 0], [cpW, gRaw, gFin, s.finishWall || 0]].forEach(function (q) {
      var v = q[3], sv = sw0 + (sw1 - sw0) * v, allRaw = v <= 0, allFin = v >= 1;
      setSweep(q[0], sv); q[1].visible = !allFin; q[2].visible = !allRaw;
      setClip(q[1], allRaw ? null : q[0].raw); setClip(q[2], allFin ? null : q[0].fin);
      if (!allRaw) { if (!allFin) scanAt = sv; }
    });
    scanLine.visible = scanAt !== null; if (scanLine.visible) { scanLine.position.copy(sweepN.clone().multiplyScalar(scanAt)); scanLine.position.y = 0.02; }
    gRawF.scale.y = gRaw.scale.y; gFinF.scale.y = 1;
    // mobiliário
    animSet('basic', s.basic || 0, 11); animSet('decor', s.decor || 0, 25);
    gCeil.visible = !!s.ceiling;
    // estúdio x torre
    gStudio.visible = !s.tower; gTower.visible = !!s.tower; apt.position.y = s.tower ? aptY : 0;
    // luz
    applyLight(s.light || 'studio', s.lampsOn || 0, s.bg || 'dark', s.sunAng);
    R.toneMappingExposure = s.exposure || 1.0;
    // sombras acompanham a área filmada
    if (s.tower) { if (s.shadowFar) shadowBox(-2.6, 7.4, 40); else shadowBox(4.5, 4.2, 8); } else shadowBox(4.5, 4.2, 8);
    sun.shadow.camera.updateProjectionMatrix();
    sun.target.position.y = apt.position.y;
  }
  var perp = new T.Vector3(-sweepN.z, 0, sweepN.x);
  var scanLine = new T.Group(); apt.add(scanLine);
  var goldM = new T.MeshBasicMaterial({color: 0xe2c48a, toneMapped: false});
  var floorLine = new T.Mesh(new T.BoxGeometry(0.05, 0.03, 12), goldM); scanLine.add(floorLine);
  var veil = new T.Mesh(new T.PlaneGeometry(12, Hh * 1.25), new T.MeshBasicMaterial({color: 0xe2c48a, transparent: true, opacity: 0.1, toneMapped: false, side: T.DoubleSide, depthWrite: false}));
  veil.rotation.y = Math.PI / 2; veil.position.y = Hh * 0.62; scanLine.add(veil);
  var topLine = new T.Mesh(new T.BoxGeometry(0.04, 0.03, 12), goldM); topLine.position.y = Hh * 1.25; scanLine.add(topLine);
  scanLine.rotation.y = Math.atan2(perp.x, perp.z);
  function setClip(g, plane) {
    if (g.userData.clip === plane) return; g.userData.clip = plane;
    g.traverse(function (o) { if (o.isMesh) { var ms = Array.isArray(o.material) ? o.material : [o.material]; ms.forEach(function (m) { m.clippingPlanes = plane ? [plane] : null; m.needsUpdate = true; }); } });
  }
  // materiais compartilhados entre os grupos precisam ser exclusivos para o recorte funcionar
  function uniqueMats(g) { g.traverse(function (o) { if (o.isMesh) { if (Array.isArray(o.material)) o.material = o.material.map(function (m) { return m.clone(); }); else o.material = o.material.clone(); } }); }
  uniqueMats(gRaw); uniqueMats(gFin); uniqueMats(gRawF); uniqueMats(gFinF);
  function animSet(set, v, n) {
    items.forEach(function (g) {
      var d = g.userData; if (d.set !== set) return;
      var k = ease((v * (n + 3) - (d.order - 1)) / 3); // entrada escalonada
      g.visible = k > 0.002;
      g.scale.setScalar(0.001 + 0.999 * k); g.position.y = d.base.y + (1 - k) * 0.35;
    });
  }
  var lightCur = '', darkBg = new T.Color(0x0b0b0d).convertSRGBToLinear(), shades = [];
  function applyLight(name, lampsOn, bg, sunAng) {
    var L = {
      studio: {sun: [0xfff6ea, 2.0], dir: [-6, 14, -4], hemi: 0.55, env: 'rooftop_day', envI: 0.55},
      day: {sun: [0xfff1dc, 2.6], dir: [-7, 11, -6], hemi: 0.25, env: 'rooftop_day', envI: 0.7},
      afternoon: {sun: [0xffdcae, 3.0], dir: [12, 7, -9], hemi: 0.18, env: 'rooftop_day', envI: 0.6},
      golden: {sun: [0xffb070, 3.4], dir: [16, 5, -6], hemi: 0.14, env: 'shanghai_riverside', envI: 0.75},
      dusk: {sun: [0xff9a5c, 1.0], dir: [18, 2.5, -4], hemi: 0.12, env: 'shanghai_riverside', envI: 0.55}
    }[name];
    sun.color.setHex(L.sun[0]).convertSRGBToLinear(); sun.intensity = L.sun[1];
    var d = L.dir; sun.position.set(4.5 + d[0], apt.position.y + d[1], 4.2 + d[2]);
    if (sunAng) sun.position.set(4.5 + sunAng[0], apt.position.y + sunAng[1], 4.2 + sunAng[2]);
    hemi.intensity = L.hemi;
    if (prevEnv !== L.env) { S.environment = envs[L.env]; prevEnv = L.env; }
    if (lightCur !== name) {
      lightCur = name;
      S.traverse(function (o) { if (o.isMesh) { var ms = Array.isArray(o.material) ? o.material : [o.material]; ms.forEach(function (m) { if (m.isMeshStandardMaterial) { if (m.userData.baseEnv === undefined) m.userData.baseEnv = m.envMapIntensity; m.envMapIntensity = m.userData.baseEnv * L.envI; } }); } });
    }
    sky.visible = bg === 'sky' || bg === 'skyday'; S.fog = null; skyU.cloud.value = 0;
    towerGlass.forEach(function (m, i) { var day = bg === 'skyday'; m.color.setHex(day ? (i ? 0x24414c : 0x2b4c58) : (i ? 0x5d717d : 0x52646f)).convertSRGBToLinear(); m.metalness = day ? 0.85 : 0.5; m.roughness = day ? 0.04 : 0.08; });
    if (bg === 'skyday') {
      skyU.top.value.setHex(0x1f93a6).convertSRGBToLinear(); skyU.mid.value.setHex(0xbfe4e8).convertSRGBToLinear(); skyU.bot.value.setHex(0x6d7a78).convertSRGBToLinear();
      skyU.cloud.value = 1; S.background = null;
    } else if (bg === 'sky') {
      var dusk = name === 'dusk';
      skyU.top.value.setHex(dusk ? 0x141c33 : 0x2c3d5e); skyU.mid.value.setHex(dusk ? 0x8a5a5a : 0xe0a173); skyU.bot.value.setHex(dusk ? 0x1a1820 : 0x3a332c);
      S.fog = dusk ? fogDusk : fogGold; S.background = null;
    } else S.background = bg === 'hdri' ? bgs[L.env] : darkBg;
    lampMat.emissiveIntensity = lampsOn * 2.2;
    lamps.forEach(function (p) { p.intensity = lampsOn * 2.4; });
    if (!shades.length) S.traverse(function (o) { if (o.userData.shade) shades.push(o); });
    shades.forEach(function (o) { o.material.emissiveIntensity = lampsOn * 0.9; });
    towerGlass.forEach(function (m, i) { m.emissiveIntensity = (name === 'dusk' ? 0.55 : 0) * (i ? 0.6 : 1); });
  }

  // ---------- câmera e quadro
  function frame(c) {
    cam.position.set(c.p[0], c.p[1] + (c.local ? apt.position.y : 0), c.p[2]);
    cam.up.set(0, 1, 0);
    if (c.roll) cam.up.set(Math.sin(c.roll), Math.cos(c.roll), 0);
    cam.lookAt(c.l[0], c.l[1] + (c.local ? apt.position.y : 0), c.l[2]);
    cam.fov = c.fov; cam.aspect = W / H; cam.updateProjectionMatrix();
    if (c.dof) {
      bokeh.enabled = true; bokeh.uniforms.focus.value = c.dof[0]; bokeh.uniforms.aperture.value = c.dof[1]; bokeh.uniforms.maxblur.value = c.dof[2] || 0.008;
      composer.render();
    } else { R.render(S, cam); }
  }
  function project(pts) {
    return pts.map(function (p) {
      var v = new T.Vector3(p[0], p[1] + apt.position.y, p[2]).project(cam);
      return {x: (v.x + 1) / 2 * W, y: (1 - v.y) / 2 * H, vis: v.z < 1 ? (v.z > -1) : false};
    });
  }
  window.FILM = {ready: ready, setState: setState, frame: frame, project: project, W: W, H: H, aptY: aptY, rooms: P.rooms};
})();
