/* Vídeo Imóvel Studio 3D · tour 3D de demonstração (projetos de demonstração redesenhados).
   Motor multi-planta: os projetos ficam em window.VI3D_PLANS (plans/*.js).
   Sem dependências além de THREE (r128). Sem o operador "e lógico" duplo no código: o WordPress converte o caractere. */
(function () {
  var root = document.getElementById('vi3d');
  if (!root) return;
  var PLANS = window.VI3D_PLANS || {};
  var cv = root.querySelector('canvas');
  var reduce = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)').matches : false;
  var R = new THREE.WebGLRenderer({canvas: cv, antialias: true});
  R.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.6));
  R.shadowMap.enabled = true; R.shadowMap.type = THREE.PCFSoftShadowMap;
  R.outputEncoding = THREE.sRGBEncoding; R.toneMapping = THREE.ACESFilmicToneMapping; R.toneMappingExposure = 1.0;
  var S = new THREE.Scene();
  var cam = new THREE.PerspectiveCamera(32, 1, 0.05, 400);
  var hemi = new THREE.HemisphereLight(0xfffaf2, 0xcfc4b2, 0.38); S.add(hemi);
  var sun = new THREE.DirectionalLight(0xfff1dc, 1.9);
  sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048);
  var sc = sun.shadow.camera; sc.left = -10; sc.right = 10; sc.top = 10; sc.bottom = -10; sun.shadow.bias = -0.0005;
  S.add(sun); S.add(sun.target);

  function M(c, r) { return new THREE.MeshStandardMaterial({color: c, roughness: r === undefined ? 0.85 : r, metalness: 0}); }
  var CLAY = M(0xf1f0ec), CLAY2 = M(0xdcdad4);
  var decor = new THREE.Group(), low = new THREE.Group(), full = new THREE.Group(), floors = new THREE.Group(), glass = new THREE.Group(), tower = new THREE.Group();
  [decor, low, full, floors, glass, tower].forEach(function (g) { S.add(g); });
  function box(w, h, d, x, y, z, mat, g, noShadow) {
    var m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat);
    m.position.set(x, y, z); m.castShadow = !noShadow; m.receiveShadow = true;
    m.userData.real = mat; (g || decor).add(m); return m;
  }
  function cyl(r1, r2, h, x, y, z, mat, g) {
    var m = new THREE.Mesh(new THREE.CylinderGeometry(r1, r2, h, 24), mat);
    m.position.set(x, y, z); m.castShadow = true; m.receiveShadow = true; m.userData.real = mat; (g || decor).add(m); return m;
  }
  function tex(draw, rx, ry) {
    var c = document.createElement('canvas'); c.width = 512; c.height = 512; draw(c.getContext('2d'));
    var t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(rx, ry); t.encoding = THREE.sRGBEncoding; return t;
  }
  var wood = new THREE.MeshStandardMaterial({roughness: 0.55, map: tex(function (g) {
    for (var i = 0; i < 16; i++) {
      var v = 150 + Math.random() * 28; g.fillStyle = 'rgb(' + (v + 38) + ',' + (v + 4) + ',' + (v - 38) + ')'; g.fillRect(0, i * 32, 512, 32);
      g.strokeStyle = 'rgba(60,35,15,.28)'; g.beginPath(); g.moveTo(0, i * 32); g.lineTo(512, i * 32); g.stroke();
      var o = Math.random() * 512; g.beginPath(); g.moveTo(o, i * 32); g.lineTo(o, i * 32 + 32); g.stroke();
      for (var k = 0; k < 26; k++) { g.strokeStyle = 'rgba(90,55,25,' + (Math.random() * 0.12) + ')'; var yy = i * 32 + Math.random() * 32; g.beginPath(); g.moveTo(0, yy); g.lineTo(512, yy + Math.random() * 4 - 2); g.stroke(); }
    }
  }, 2, 2)});
  var tile = new THREE.MeshStandardMaterial({roughness: 0.35, map: tex(function (g) {
    g.fillStyle = '#dcd8d1'; g.fillRect(0, 0, 512, 512); g.strokeStyle = '#bdb8af'; g.lineWidth = 3;
    for (var i = 0; i <= 512; i += 128) { g.beginPath(); g.moveTo(i, 0); g.lineTo(i, 512); g.stroke(); g.beginPath(); g.moveTo(0, i); g.lineTo(512, i); g.stroke(); }
  }, 2, 2)});
  var deck = new THREE.MeshStandardMaterial({roughness: 0.7, map: tex(function (g) {
    for (var i = 0; i < 24; i++) { var v = 120 + Math.random() * 25; g.fillStyle = 'rgb(' + (v + 35) + ',' + (v + 8) + ',' + (v - 25) + ')'; g.fillRect(i * 21.33, 0, 21.33, 512); g.fillStyle = 'rgba(40,25,10,.35)'; g.fillRect(i * 21.33, 0, 1.5, 512); }
  }, 2, 2)});
  var stoneK = new THREE.MeshStandardMaterial({roughness: 0.3, map: tex(function (g) {
    g.fillStyle = '#ebe7e0'; g.fillRect(0, 0, 512, 512);
    for (var k = 0; k < 60; k++) { g.strokeStyle = 'rgba(150,140,130,' + (Math.random() * 0.25) + ')'; g.lineWidth = Math.random() * 2; g.beginPath(); g.moveTo(Math.random() * 512, 0); g.bezierCurveTo(Math.random() * 512, 200, Math.random() * 512, 300, Math.random() * 512, 512); g.stroke(); }
  }, 1, 1)});
  var porc = new THREE.MeshStandardMaterial({roughness: 0.25, map: tex(function (g) {
    g.fillStyle = '#d9d4cc'; g.fillRect(0, 0, 512, 512); g.strokeStyle = '#c4beb4'; g.lineWidth = 2;
    for (var i = 0; i <= 512; i += 256) { g.beginPath(); g.moveTo(i, 0); g.lineTo(i, 512); g.stroke(); g.beginPath(); g.moveTo(0, i); g.lineTo(512, i); g.stroke(); }
  }, 2, 2)});
  var floorMats = {wood: wood, tile: tile, deck: deck, stone: stoneK, porc: porc};
  var wallMat = M(0xf5f1e9, 0.9);
  var mats = {
    fab: M(0x8c9a8a, 0.95), fab2: M(0xd8c8b2, 0.95), oak: M(0x9b6c44, 0.55), dark: M(0x2a2a2a, 0.5), white: M(0xf3f2ef, 0.45),
    green: M(0x5d7b4c, 0.9), rug: M(0xd6cab7, 1), linen: M(0xf1ece3, 0.95), stone: stoneK, metal: M(0x9fa3a6, 0.3),
    glass: new THREE.MeshStandardMaterial({color: 0xcfe0e6, transparent: true, opacity: 0.25, roughness: 0.05})
  };
  var lampMat = new THREE.MeshStandardMaterial({color: 0xfff1d6, emissive: 0xffd9a0, emissiveIntensity: 0.0, roughness: 0.6});
  var lamps = [];
  function lamp(x, y, z, r) { var s = new THREE.Mesh(new THREE.SphereGeometry(r, 20, 14), lampMat); s.position.set(x, y, z); decor.add(s); var p = new THREE.PointLight(0xffd3a0, 0, 6, 2); p.position.set(x, y - 0.05, z); decor.add(p); lamps.push(p); }
  function plant(x, z, s) {
    s = s || 1;
    box(0.34 * s, 0.42 * s, 0.34 * s, x, 0.21 * s, z, M(0xd8d0c2));
    var a = new THREE.Mesh(new THREE.SphereGeometry(0.36 * s, 18, 12), mats.green); a.position.set(x, 0.78 * s, z); a.castShadow = true; decor.add(a);
    var b = new THREE.Mesh(new THREE.SphereGeometry(0.24 * s, 16, 10), mats.green); b.position.set(x + 0.12 * s, 1.05 * s, z - 0.05 * s); b.castShadow = true; decor.add(b);
  }
  var kit = {box: box, cyl: cyl, lamp: lamp, plant: plant, M: M, mats: mats, decor: decor, low: low, full: full, glass: glass, tower: tower, floors: floors, THREE: THREE};

  var PLAN = null;
  function clear() {
    lamps = [];
    [decor, low, full, floors, glass, tower].forEach(function (g) {
      for (var i = g.children.length - 1; i >= 0; i--) { var o = g.children[i]; if (o.geometry) o.geometry.dispose(); g.remove(o); }
    });
  }
  function buildWalls(cut, g) {
    PLAN.walls.forEach(function (w, i) {
      var x1 = w[0], y1 = w[1], x2 = w[2], y2 = w[3], L = Math.hypot(x2 - x1, y2 - y1), ux = (x2 - x1) / L, uy = (y2 - y1) / L;
      var horiz = Math.abs(ux) > 0.5;
      function seg(a, b, y0, h) {
        if (b - a < 0.01) return; if (h <= 0) return;
        var mx = x1 + ux * (a + b) / 2, mz = y1 + uy * (a + b) / 2;
        box(horiz ? (b - a) : PLAN.T, h, horiz ? PLAN.T : (b - a), mx, y0 + h / 2, mz, wallMat, g);
      }
      var ops = PLAN.openings.filter(function (o) { return o.w === i; }).sort(function (a, b) { return a.a - b.a; });
      var cur = 0;
      ops.forEach(function (o) {
        seg(cur, o.a, 0, cut);
        var mx = x1 + ux * (o.a + o.b) / 2, mz = y1 + uy * (o.a + o.b) / 2;
        if (o.type === 'window') {
          seg(o.a, o.b, 0, Math.min(o.sill, cut));
          if (cut > o.sill + o.h) seg(o.a, o.b, o.sill + o.h, cut - o.sill - o.h);
          if (g === full) {
            var gl = new THREE.Mesh(new THREE.BoxGeometry(horiz ? o.b - o.a : 0.03, o.h, horiz ? 0.03 : o.b - o.a), new THREE.MeshStandardMaterial({color: 0xcfe2ee, transparent: true, opacity: 0.18, roughness: 0.05}));
            gl.position.set(mx, o.sill + o.h / 2, mz); glass.add(gl);
            box(horiz ? o.b - o.a : 0.06, 0.05, horiz ? 0.06 : o.b - o.a, mx, o.sill, mz, M(0x2b2b2b, 0.5), g, true);
          }
        } else {
          var top = o.h || 2.1;
          if (cut > top) seg(o.a, o.b, top, cut - top);
          if (o.slide) { if (g === full) {
            var half = (o.b - o.a) / 2, sx = x1 + ux * (o.a + half / 2), sz = y1 + uy * (o.a + half / 2);
            var sg = new THREE.Mesh(new THREE.BoxGeometry(horiz ? half : 0.03, top, horiz ? 0.03 : half), new THREE.MeshStandardMaterial({color: 0xcfe2ee, transparent: true, opacity: 0.2, roughness: 0.05}));
            sg.position.set(sx, top / 2, sz); glass.add(sg);
            box(horiz ? o.b - o.a : 0.07, 0.05, horiz ? 0.07 : o.b - o.a, mx, top, mz, M(0x2b2b2b, 0.5), g, true);
          } }
        }
        cur = o.b;
      });
      seg(cur, L, 0, cut);
    });
  }
  function build(id) {
    var P = PLANS[id]; if (!P) return;
    clear(); PLAN = P; root.setAttribute('data-plan', id);
    root.querySelectorAll('[data-plan-set]').forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-plan-set') === id ? 'true' : 'false'); });
    root.querySelectorAll('[data-only]').forEach(function (b) { b.hidden = b.getAttribute('data-only') !== id; });
    var B = P.bounds;
    PLAN.cx = (B[0] + B[2]) / 2; PLAN.cz = (B[1] + B[3]) / 2;
    sun.target.position.set(PLAN.cx, 0, PLAN.cz);
    P.rooms.forEach(function (r) {
      var f = box(r.w, 0.04, r.d, r.x + r.w / 2, -0.02, r.y + r.d / 2, floorMats[r.floor] || wood, floors, true);
      f.castShadow = false;
    });
    if (P.ground === 'slab') box(B[2] - B[0] + 1.2, 0.3, B[3] - B[1] + 1.2, PLAN.cx, -0.19, PLAN.cz, M(0xb9b5ad, 1), floors, true);
    else box(B[2] - B[0] + 6, 0.3, B[3] - B[1] + 6, PLAN.cx, -0.2, PLAN.cz, M(0x7f9568, 1), floors, true);
    buildWalls(1.5, low); buildWalls(P.H, full);
    (P.ceil || []).forEach(function (c) { box(c[2] - c[0], 0.08, c[3] - c[1], (c[0] + c[2]) / 2, P.H + 0.04, (c[1] + c[3]) / 2, M(0xf8f6f1), full, true); });
    if (P.extras) P.extras(kit);
    if (P.furnish) P.furnish(kit);
    walker = {x: P.start.x, z: P.start.z, yaw: P.start.yaw, pitch: -0.05};
    orbit.r = P.orbitR || 18; guided = null;
    if (ui.planImg) { if (P.planta) ui.planImg.src = P.planta; ui.planImg.alt = 'Planta 2D · ' + P.nome; }
    if (ui.title) ui.title.textContent = P.nome;
    setMode(mode === 'edificio' ? (P.tower ? 'edificio' : 'decorado') : mode);
  }
  // materiais: clay na etapa "estrutura"
  function setClay(on) {
    [decor, low, full, floors].forEach(function (g) { g.traverse(function (o) { if (o.isMesh) { if (!o.userData.real) o.userData.real = o.material; if (!o.material.transparent) o.material = on ? (g === floors ? CLAY2 : CLAY) : o.userData.real; } }); });
  }
  // luz do dia: t 0 = manhã, 0.5 = tarde, 1 = noite
  var light = 0.35;
  function applyLight() {
    var t = light, cx = PLAN ? PLAN.cx : 5, cz = PLAN ? PLAN.cz : 3.5;
    var ang = Math.PI * (0.15 + t * 0.85), far = mode === 'edificio' ? 3 : 1;
    sun.position.set(cx + Math.cos(ang) * 14 * far, Math.max(1.5, Math.sin(ang) * 14) * far, cz - 9 * far);
    var night = Math.max(0, (t - 0.7) / 0.3), dusk = Math.max(0, 1 - Math.abs(t - 0.75) / 0.2);
    sun.intensity = 2.0 * (1 - night) + 0.1;
    sun.color.setHSL(0.09, 0.55 + dusk * 0.4, 0.82 - dusk * 0.12);
    hemi.intensity = (0.42 - night * 0.3) * (mode === 'passeio' ? 1.7 : 1);
    var sky = new THREE.Color(0xeeeae3).lerp(new THREE.Color(0xf2c9a0), dusk * 0.6).lerp(new THREE.Color(0x1b2433), night);
    S.background = sky;
    lampMat.emissiveIntensity = night * 1.4 + dusk * 0.4;
    lamps.forEach(function (p) { p.intensity = (night + dusk * 0.3) * 1.6; });
    if (PLAN) { if (PLAN.tower) { if (PLAN.tower.onLight) PLAN.tower.onLight(night, dusk); } }
  }
  // câmera: modos
  var ui = {
    label: root.querySelector('[data-room]'), mini: root.querySelector('canvas.mini'), title: root.querySelector('[data-title]'),
    plan: root.querySelector('.vi3d-plan'), planImg: root.querySelector('.vi3d-plan img'), walk: root.querySelector('.vi3d-walk'), hint: root.querySelector('[data-hint]')
  };
  var mode = 'decorado', orbit = {th: 0.5, ph: 0.92, r: 18}, walker = {x: 0, z: 0, yaw: 0, pitch: -0.05};
  function size() {
    var w = root.clientWidth, h = Math.round(w * (w < 700 ? 1.4 : 0.62));
    R.setSize(w, h, false); cv.style.width = w + 'px'; cv.style.height = h + 'px'; cam.aspect = w / h; cam.updateProjectionMatrix();
    root.style.setProperty('--vi3d-h', h + 'px');
  }
  function setMode(m) {
    if (m === 'edificio') { if (!PLAN.tower) m = 'decorado'; }
    mode = m;
    root.setAttribute('data-mode', m);
    root.querySelectorAll('[data-set]').forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-set') === m ? 'true' : 'false'); });
    var walk = m === 'passeio', bld = m === 'edificio';
    low.visible = !walk; full.visible = walk; glass.visible = walk; decor.visible = m !== 'estrutura';
    if (bld) { low.visible = false; decor.visible = false; floors.visible = false; } else { floors.visible = true; }
    tower.visible = bld; sun.castShadow = !bld;
    setClay(m === 'estrutura');
    cam.fov = walk ? 62 : 32; cam.updateProjectionMatrix();
    ui.plan.hidden = m !== 'planta'; ui.walk.hidden = !walk;
    applyLight();
    if (ui.label) { if (!walk) ui.label.textContent = bld ? (PLAN.tower.label || '') : ''; }
    if (ui.hint) ui.hint.textContent = walk ? 'Arraste para olhar · botões ou setas para andar' : 'Arraste para girar · role ou pince para aproximar';
  }
  function roomAt(x, z) {
    for (var i = 0; i < PLAN.rooms.length; i++) { var r = PLAN.rooms[i]; if (x >= r.x + 0.2) { if (x <= r.x + r.w - 0.2) { if (z >= r.y + 0.2) { if (z <= r.y + r.d - 0.2) return r.name; } } } }
    for (var j = 0; j < PLAN.rooms.length; j++) { var q = PLAN.rooms[j]; if (x >= q.x) { if (x <= q.x + q.w) { if (z >= q.y) { if (z <= q.y + q.d) return q.name; } } } }
    return '';
  }
  // colisão: não atravessar paredes fora dos vãos de porta
  function blocked(x0, z0, x1, z1) {
    if (!roomAt(x1, z1)) return true;
    for (var i = 0; i < PLAN.walls.length; i++) {
      var w = PLAN.walls[i], horiz = w[1] === w[3];
      if (horiz) {
        var zw = w[1]; if ((z0 - zw) * (z1 - zw) <= 0) { if (x1 >= Math.min(w[0], w[2])) { if (x1 <= Math.max(w[0], w[2])) {
          var along = Math.abs(x1 - w[0]); if (!inDoor(i, along)) return true; } } }
      } else {
        var xw = w[0]; if ((x0 - xw) * (x1 - xw) <= 0) { if (z1 >= Math.min(w[1], w[3])) { if (z1 <= Math.max(w[1], w[3])) {
          var al = Math.abs(z1 - w[1]); if (!inDoor(i, al)) return true; } } }
      }
    }
    return false;
  }
  function inDoor(i, a) { for (var k = 0; k < PLAN.openings.length; k++) { var o = PLAN.openings[k]; if (o.w === i) { if (o.type === 'door') { if (a > o.a + 0.08) { if (a < o.b - 0.08) return true; } } } } return false; }
  function move(d) {
    var nx = walker.x + Math.sin(walker.yaw) * d, nz = walker.z + Math.cos(walker.yaw) * d;
    if (!blocked(walker.x, walker.z, nx, nz)) { walker.x = nx; walker.z = nz; }
  }
  // tour guiado
  var guided = null;
  function startGuided() {
    setMode('passeio'); var s0 = PLAN.stops[0];
    walker.x = s0.x; walker.z = s0.z; walker.yaw = s0.yaw;
    guided = {i: 1, t: 0, from: {x: walker.x, z: walker.z, yaw: walker.yaw}};
  }
  function stepGuided(dt) {
    if (!guided) return;
    var to = PLAN.stops[guided.i]; guided.t += dt / (reduce ? 0.01 : 1.6);
    var k = Math.min(1, Math.max(0, guided.t)), e = k * k * (3 - 2 * k), f = guided.from;
    var dy = to.yaw - f.yaw; while (dy > Math.PI) dy -= Math.PI * 2; while (dy < -Math.PI) dy += Math.PI * 2;
    walker.x = f.x + (to.x - f.x) * e; walker.z = f.z + (to.z - f.z) * e; walker.yaw = f.yaw + dy * e; walker.pitch = -0.05;
    if (k >= 1) { guided.i++; guided.t = -0.9; guided.from = {x: walker.x, z: walker.z, yaw: walker.yaw}; if (guided.i >= PLAN.stops.length) guided = null; }
  }
  // entrada
  var drag = null, keys = {}, hold = 0, pinch = null, lastR = 0;
  function rMin() { return mode === 'edificio' ? 30 : 9; }
  function rMax() { return mode === 'edificio' ? 160 : 30; }
  function goMode(m) {
    guided = null;
    if (m === 'edificio') { if (mode !== 'edificio') lastR = orbit.r; orbit.r = PLAN.tower ? (PLAN.tower.r || 70) : orbit.r; orbit.ph = 1.22; orbit.th = PLAN.tower ? (PLAN.tower.th || orbit.th) : orbit.th; }
    else if (mode === 'edificio') { orbit.r = lastR || PLAN.orbitR || 18; orbit.ph = 0.92; }
    setMode(m);
  }
  cv.addEventListener('pointerdown', function (e) { drag = {x: e.clientX, y: e.clientY}; guided = null; cv.setPointerCapture(e.pointerId); });
  cv.addEventListener('pointermove', function (e) {
    if (!drag) return; var dx = e.clientX - drag.x, dy = e.clientY - drag.y; drag = {x: e.clientX, y: e.clientY};
    if (mode === 'passeio') { walker.yaw -= dx * 0.005; walker.pitch = Math.max(-0.6, Math.min(0.5, walker.pitch - dy * 0.004)); }
    else { orbit.th -= dx * 0.006; orbit.ph = Math.max(0.35, Math.min(1.4, orbit.ph - dy * 0.005)); }
  });
  cv.addEventListener('pointerup', function () { drag = null; });
  cv.addEventListener('wheel', function (e) { if (mode === 'passeio') return; e.preventDefault(); orbit.r = Math.max(rMin(), Math.min(rMax(), orbit.r + e.deltaY * 0.01 * (mode === 'edificio' ? 4 : 1))); }, {passive: false});
  cv.addEventListener('touchstart', function (e) { if (e.touches.length === 2) pinch = Math.hypot(e.touches[0].clientX - e.touches[1].clientX, e.touches[0].clientY - e.touches[1].clientY); }, {passive: true});
  cv.addEventListener('touchmove', function (e) { if (e.touches.length === 2) { if (pinch) { var d = Math.hypot(e.touches[0].clientX - e.touches[1].clientX, e.touches[0].clientY - e.touches[1].clientY); orbit.r = Math.max(rMin(), Math.min(rMax(), orbit.r - (d - pinch) * 0.03)); pinch = d; } } }, {passive: true});
  root.addEventListener('keydown', function (e) { keys[e.key] = true; if (mode === 'passeio') { if (e.key.indexOf('Arrow') === 0) e.preventDefault(); } });
  root.addEventListener('keyup', function (e) { keys[e.key] = false; });
  root.querySelectorAll('[data-set]').forEach(function (b) { b.addEventListener('click', function () { goMode(b.getAttribute('data-set')); }); });
  root.querySelectorAll('[data-plan-set]').forEach(function (b) { b.addEventListener('click', function () {
    if (mode === 'edificio') { orbit.r = lastR || 18; orbit.ph = 0.92; mode = 'decorado'; }
    build(b.getAttribute('data-plan-set'));
  }); });
  root.querySelectorAll('[data-walk]').forEach(function (b) {
    var v = parseFloat(b.getAttribute('data-walk'));
    b.addEventListener('pointerdown', function (e) { e.preventDefault(); hold = v; guided = null; });
    ['pointerup', 'pointerleave', 'pointercancel'].forEach(function (ev) { b.addEventListener(ev, function () { hold = 0; }); });
  });
  root.querySelectorAll('[data-turn]').forEach(function (b) { b.addEventListener('click', function () { walker.yaw += parseFloat(b.getAttribute('data-turn')); guided = null; }); });
  root.querySelectorAll('[data-guided]').forEach(function (g) { g.addEventListener('click', startGuided); });
  var sl = root.querySelector('input[type=range]'); if (sl) sl.addEventListener('input', function () { light = sl.value / 100; applyLight(); });
  // minimapa
  function drawMini() {
    var c = ui.mini; if (!c) return; var B = PLAN.bounds, x = c.getContext('2d');
    var s = Math.min(c.width / (B[2] - B[0] + 1), c.height / (B[3] - B[1] + 1)), ox = s * 0.5 - B[0] * s, oz = s * 0.5 - B[1] * s;
    x.clearRect(0, 0, c.width, c.height); x.fillStyle = 'rgba(13,18,28,.78)'; x.fillRect(0, 0, c.width, c.height);
    x.fillStyle = 'rgba(226,196,138,.14)'; PLAN.rooms.forEach(function (r) { if (r.ext) x.fillRect(ox + r.x * s, oz + r.y * s, r.w * s, r.d * s); });
    x.strokeStyle = '#e2c48a'; x.lineWidth = 2;
    PLAN.walls.forEach(function (w) { x.beginPath(); x.moveTo(ox + w[0] * s, oz + w[1] * s); x.lineTo(ox + w[2] * s, oz + w[3] * s); x.stroke(); });
    var px = ox + walker.x * s, pz = oz + walker.z * s;
    x.fillStyle = 'rgba(226,196,138,.28)'; x.beginPath(); x.moveTo(px, pz);
    x.arc(px, pz, s * 1.6, -walker.yaw + Math.PI / 2 - 0.5, -walker.yaw + Math.PI / 2 + 0.5); x.closePath(); x.fill();
    x.fillStyle = '#fff'; x.beginPath(); x.arc(px, pz, 4, 0, Math.PI * 2); x.fill();
  }
  var last = performance.now(), visible = true;
  if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }).observe(root);
  function frame(now) {
    requestAnimationFrame(frame);
    var dt = Math.min(0.05, (now - last) / 1000); last = now; if (!visible) return;
    if (mode === 'passeio') {
      var sp = 1.6 * dt;
      if (keys.ArrowUp || keys.w) move(sp); if (keys.ArrowDown || keys.s) move(-sp);
      if (keys.ArrowLeft || keys.a) walker.yaw += 1.6 * dt; if (keys.ArrowRight || keys.d) walker.yaw -= 1.6 * dt;
      if (hold) move(hold * sp);
      stepGuided(dt);
      cam.position.set(walker.x, 1.6, walker.z);
      cam.lookAt(walker.x + Math.sin(walker.yaw) * Math.cos(walker.pitch), 1.6 + Math.sin(walker.pitch), walker.z + Math.cos(walker.yaw) * Math.cos(walker.pitch));
      var rn = roomAt(walker.x, walker.z); if (ui.label) { if (ui.label.textContent !== rn) ui.label.textContent = rn; }
      drawMini();
    } else {
      var T = mode === 'edificio' ? PLAN.tower : null;
      var cx = T ? T.cx : PLAN.cx, cy = T ? T.cy : 0, cz = T ? T.cz : PLAN.cz;
      cam.position.set(cx + orbit.r * Math.sin(orbit.ph) * Math.sin(orbit.th), cy + orbit.r * Math.cos(orbit.ph), cz + orbit.r * Math.sin(orbit.ph) * Math.cos(orbit.th));
      cam.lookAt(cx, cy, cz);
      if (!drag) { if (!reduce) { if (mode !== 'planta') orbit.th += dt * 0.04; } }
    }
    R.render(S, cam);
  }
  window.addEventListener('resize', size);
  var first = root.getAttribute('data-plan') || Object.keys(PLANS)[0];
  size(); build(first); requestAnimationFrame(frame);
  window.VI3D_READY = true;
  window.VI3D = {goto: function (i) { setMode('passeio'); guided = null; var t = PLAN.stops[i]; walker.x = t.x; walker.z = t.z; walker.yaw = t.yaw; }, setMode: goMode, setPlan: build, startGuided: startGuided, setLight: function (v) { light = v; applyLight(); }, orbit: orbit};
})();
