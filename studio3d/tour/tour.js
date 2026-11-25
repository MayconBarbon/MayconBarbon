/* Vídeo Imóvel Studio 3D · tour 3D de demonstração (planta conceitual).
   Sem dependências além de THREE (r128). Sem "&&" no código: o WordPress converte o caractere. */
(function () {
  var root = document.getElementById('vi3d');
  if (!root) return;
  var cv = root.querySelector('canvas');
  var PLAN = {
    W: 10, D: 7, T: 0.15, H: 2.7,
    walls: [[0,0,10,0],[10,0,10,7],[10,7,0,7],[0,7,0,0],[6,0,6,7],[6,4,10,4]],
    openings: [
      {w:0,a:1.0,b:5.0,type:'window',sill:0.4,h:1.9},
      {w:0,a:7.0,b:9.4,type:'window',sill:0.9,h:1.3},
      {w:1,a:5.0,b:6.0,type:'window',sill:1.5,h:0.6},
      {w:2,a:8.2,b:9.1,type:'door'},
      {w:4,a:2.6,b:3.4,type:'door'},
      {w:4,a:5.2,b:6.0,type:'door'}
    ],
    rooms: [
      {name:'Estar e jantar',x:0,y:0,w:6,d:4.4},
      {name:'Cozinha',x:0,y:4.4,w:6,d:2.6},
      {name:'Suíte',x:6,y:0,w:4,d:4},
      {name:'Banho',x:6,y:4,w:4,d:3}
    ]
  };
  var reduce = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)').matches : false;
  var R = new THREE.WebGLRenderer({canvas: cv, antialias: true});
  R.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.6));
  R.shadowMap.enabled = true; R.shadowMap.type = THREE.PCFSoftShadowMap;
  R.outputEncoding = THREE.sRGBEncoding; R.toneMapping = THREE.ACESFilmicToneMapping; R.toneMappingExposure = 1.0;
  var S = new THREE.Scene();
  var cam = new THREE.PerspectiveCamera(32, 1, 0.05, 200);
  var hemi = new THREE.HemisphereLight(0xffffff, 0xbfb8ac, 0.38); S.add(hemi);
  var sun = new THREE.DirectionalLight(0xfff1dc, 1.9);
  sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048);
  var sc = sun.shadow.camera; sc.left = -9; sc.right = 9; sc.top = 9; sc.bottom = -9; sun.shadow.bias = -0.0005;
  sun.target.position.set(5, 0, 3.5); S.add(sun); S.add(sun.target);

  function M(c, r) { return new THREE.MeshStandardMaterial({color: c, roughness: r === undefined ? 0.85 : r, metalness: 0}); }
  var CLAY = M(0xf1f0ec), CLAY2 = M(0xdcdad4);
  var decor = new THREE.Group(), low = new THREE.Group(), full = new THREE.Group(), floors = new THREE.Group(), glass = new THREE.Group();
  S.add(decor); S.add(low); S.add(full); S.add(floors); S.add(glass);
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
  var stoneK = new THREE.MeshStandardMaterial({roughness: 0.3, map: tex(function (g) {
    g.fillStyle = '#ebe7e0'; g.fillRect(0, 0, 512, 512);
    for (var k = 0; k < 60; k++) { g.strokeStyle = 'rgba(150,140,130,' + (Math.random() * 0.25) + ')'; g.lineWidth = Math.random() * 2; g.beginPath(); g.moveTo(Math.random() * 512, 0); g.bezierCurveTo(Math.random() * 512, 200, Math.random() * 512, 300, Math.random() * 512, 512); g.stroke(); }
  }, 1, 1)});
  // pisos
  PLAN.rooms.forEach(function (r) {
    var mat = r.name === 'Banho' ? tile : (r.name === 'Cozinha' ? stoneK : wood);
    var f = box(r.w, 0.04, r.d, r.x + r.w / 2, -0.02, r.y + r.d / 2, mat, floors, true);
    f.castShadow = false;
  });
  var base = box(PLAN.W + 0.6, 0.3, PLAN.D + 0.6, PLAN.W / 2, -0.19, PLAN.D / 2, M(0x59604f), floors, true);
  // paredes (versão em corte e versão inteira)
  var wallMat = M(0xf5f1e9, 0.9);
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
        if (o.type === 'window') {
          seg(o.a, o.b, 0, Math.min(o.sill, cut));
          if (cut > o.sill + o.h) seg(o.a, o.b, o.sill + o.h, cut - o.sill - o.h);
          if (g === full) {
            var mx = x1 + ux * (o.a + o.b) / 2, mz = y1 + uy * (o.a + o.b) / 2;
            var gl = new THREE.Mesh(new THREE.BoxGeometry(horiz ? o.b - o.a : 0.03, o.h, horiz ? 0.03 : o.b - o.a), new THREE.MeshStandardMaterial({color: 0xcfe2ee, transparent: true, opacity: 0.18, roughness: 0.05}));
            gl.position.set(mx, o.sill + o.h / 2, mz); glass.add(gl);
            box(horiz ? o.b - o.a : 0.06, 0.05, horiz ? 0.06 : o.b - o.a, mx, o.sill, mz, M(0x2b2b2b, 0.5), g, true);
          }
        } else if (cut > 2.1) { seg(o.a, o.b, 2.1, cut - 2.1); }
        cur = o.b;
      });
      seg(cur, L, 0, cut);
    });
  }
  buildWalls(1.5, low); buildWalls(PLAN.H, full);
  var ceil = box(PLAN.W, 0.08, PLAN.D, PLAN.W / 2, PLAN.H + 0.04, PLAN.D / 2, M(0xf8f6f1), full, true);
  // mobiliário
  var fab = M(0x8c9a8a, 0.95), fab2 = M(0xd8c8b2, 0.95), oak = M(0x9b6c44, 0.55), dark = M(0x2a2a2a, 0.5), white = M(0xf3f2ef, 0.45), green = M(0x5d7b4c, 0.9), rug = M(0xd6cab7, 1), brass = M(0xc2a36b, 0.35), linen = M(0xf1ece3, 0.95);
  var lampMat = new THREE.MeshStandardMaterial({color: 0xfff1d6, emissive: 0xffd9a0, emissiveIntensity: 0.0, roughness: 0.6});
  var lamps = [];
  function lamp(x, y, z, r) { var s = new THREE.Mesh(new THREE.SphereGeometry(r, 20, 14), lampMat); s.position.set(x, y, z); decor.add(s); var p = new THREE.PointLight(0xffd3a0, 0, 6, 2); p.position.set(x, y - 0.05, z); decor.add(p); lamps.push(p); }
  // estar
  box(2.8, 0.02, 2.0, 2.4, 0.01, 2.0, rug, decor, true);
  box(2.4, 0.4, 0.95, 2.4, 0.2, 0.8, fab); box(2.4, 0.5, 0.22, 2.4, 0.6, 0.42, fab);
  box(0.22, 0.6, 0.95, 1.1, 0.3, 0.8, fab); box(0.22, 0.6, 0.95, 3.7, 0.3, 0.8, fab);
  box(1.0, 0.12, 0.8, 1.8, 0.46, 0.85, linen); box(1.0, 0.12, 0.8, 3.0, 0.46, 0.85, linen);
  box(0.85, 0.42, 0.85, 0.8, 0.21, 2.4, fab2); box(0.85, 0.4, 0.15, 0.8, 0.6, 2.75, fab2);
  cyl(0.45, 0.45, 0.06, 2.4, 0.36, 2.0, oak); cyl(0.05, 0.05, 0.33, 2.4, 0.17, 2.0, dark);
  box(2.0, 0.45, 0.42, 2.4, 0.23, 3.7, oak); box(1.6, 0.9, 0.05, 2.4, 1.15, 3.88, M(0x111111, 0.25));
  box(1.2, 0.8, 0.03, 2.4, 1.6, 0.09, M(0x46594e, 0.8)); box(1.24, 0.84, 0.02, 2.4, 1.6, 0.08, brass);
  cyl(0.02, 0.02, 1.5, 0.45, 0.75, 1.45, dark); lamp(0.45, 1.55, 1.45, 0.16);
  // jantar
  box(1.8, 0.05, 0.95, 4.5, 0.76, 2.2, oak);
  [[3.75, 1.85], [3.75, 2.55], [5.25, 1.85], [5.25, 2.55]].forEach(function (p) { box(0.07, 0.74, 0.07, p[0], 0.37, p[1], oak); });
  [[4.05, 1.5], [4.95, 1.5], [4.05, 2.9], [4.95, 2.9]].forEach(function (p) { box(0.45, 0.06, 0.45, p[0], 0.46, p[1], fab2); box(0.45, 0.45, 0.06, p[0], 0.7, p[1] + (p[1] < 2 ? -0.2 : 0.2), fab2); });
  cyl(0.01, 0.01, 0.9, 4.2, 2.25, 2.2, dark, full); cyl(0.01, 0.01, 0.9, 4.8, 2.25, 2.2, dark, full);
  lamp(4.2, 1.75, 2.2, 0.17); lamp(4.8, 1.75, 2.2, 0.17);
  // cozinha
  box(4.0, 0.88, 0.62, 3.6, 0.44, 6.62, white); box(4.0, 0.04, 0.64, 3.6, 0.9, 6.62, stoneK);
  box(4.0, 0.7, 0.36, 3.6, 1.95, 6.75, white, full); box(0.8, 2.0, 0.66, 1.0, 1.0, 6.6, M(0xc9cbcd, 0.3));
  box(0.6, 0.02, 0.45, 3.8, 0.93, 6.6, dark, decor, true);
  box(2.0, 0.88, 0.85, 3.8, 0.44, 5.15, oak); box(2.1, 0.05, 0.95, 3.8, 0.9, 5.15, stoneK);
  [[3.2, 4.55], [3.8, 4.55], [4.4, 4.55]].forEach(function (p) { box(0.36, 0.06, 0.36, p[0], 0.72, p[1], fab2); box(0.04, 0.7, 0.04, p[0], 0.35, p[1], dark); });
  lamp(3.3, 1.9, 5.15, 0.12); lamp(4.3, 1.9, 5.15, 0.12);
  // suíte
  box(1.8, 0.35, 2.1, 8.0, 0.18, 2.2, oak); box(1.75, 0.2, 2.0, 8.0, 0.45, 2.22, linen);
  box(1.75, 0.04, 1.1, 8.0, 0.57, 1.85, fab2); box(0.6, 0.15, 0.35, 7.6, 0.62, 3.05, white); box(0.6, 0.15, 0.35, 8.4, 0.62, 3.05, white);
  box(2.0, 1.1, 0.08, 8.0, 0.55, 3.3, M(0x7d6a57, 0.9));
  box(0.45, 0.5, 0.4, 6.75, 0.25, 3.1, oak); box(0.45, 0.5, 0.4, 9.25, 0.25, 3.1, oak);
  lamp(6.75, 0.72, 3.1, 0.1); lamp(9.25, 0.72, 3.1, 0.1);
  box(0.62, 2.3, 2.4, 9.62, 1.15, 1.5, oak);
  box(2.2, 0.02, 1.4, 8.0, 0.01, 1.0, rug, decor, true);
  // banho
  box(1.5, 0.82, 0.52, 6.95, 0.41, 6.68, oak); box(1.5, 0.04, 0.54, 6.95, 0.84, 6.68, stoneK);
  box(1.0, 0.8, 0.02, 6.95, 1.55, 6.9, M(0xdfe7ea, 0.05)); box(0.4, 0.4, 0.6, 8.4, 0.2, 6.62, white);
  box(1.25, 0.02, 1.25, 9.3, 0.01, 4.75, M(0xbfc4c4, 0.2), decor, true);
  var gl2 = new THREE.Mesh(new THREE.BoxGeometry(0.02, 2.0, 1.25), new THREE.MeshStandardMaterial({color: 0xcfe0e6, transparent: true, opacity: 0.25})); gl2.position.set(8.66, 1.0, 4.75); decor.add(gl2);
  // plantas
  [[0.45, 0.4], [5.6, 0.45], [9.55, 3.55], [0.45, 3.7]].forEach(function (p) {
    box(0.34, 0.42, 0.34, p[0], 0.21, p[1], M(0xd8d0c2));
    var a = new THREE.Mesh(new THREE.SphereGeometry(0.36, 18, 12), green); a.position.set(p[0], 0.78, p[1]); a.castShadow = true; decor.add(a);
    var b = new THREE.Mesh(new THREE.SphereGeometry(0.24, 16, 10), green); b.position.set(p[0] + 0.12, 1.05, p[1] - 0.05); b.castShadow = true; decor.add(b);
  });
  // materiais: clay na etapa "estrutura"
  function setClay(on) {
    [decor, low, full, floors].forEach(function (g) { g.traverse(function (o) { if (o.isMesh) { if (!o.userData.real) o.userData.real = o.material; if (!o.material.transparent) o.material = on ? (g === floors ? CLAY2 : CLAY) : o.userData.real; } }); });
  }
  // luz do dia: t 0 = manhã, 0.5 = tarde, 1 = noite
  var light = 0.35;
  function applyLight() {
    var t = light;
    var ang = Math.PI * (0.15 + t * 0.85);
    sun.position.set(5 + Math.cos(ang) * 14, Math.max(1.5, Math.sin(ang) * 14), 3.5 - 9);
    var night = Math.max(0, (t - 0.7) / 0.3), dusk = Math.max(0, 1 - Math.abs(t - 0.75) / 0.2);
    sun.intensity = 2.0 * (1 - night) + 0.1;
    sun.color.setHSL(0.09, 0.55 + dusk * 0.4, 0.82 - dusk * 0.12);
    hemi.intensity = 0.42 - night * 0.3;
    var sky = new THREE.Color(0xeeeae3).lerp(new THREE.Color(0xf2c9a0), dusk * 0.6).lerp(new THREE.Color(0x1b2433), night);
    S.background = sky;
    lampMat.emissiveIntensity = night * 1.4 + dusk * 0.4;
    lamps.forEach(function (p) { p.intensity = (night + dusk * 0.3) * 1.6; });
  }
  // câmera: modos
  var ui = {
    label: root.querySelector('[data-room]'), mini: root.querySelector('canvas.mini'),
    plan: root.querySelector('.vi3d-plan'), walk: root.querySelector('.vi3d-walk'), hint: root.querySelector('[data-hint]')
  };
  var mode = 'decorado', orbit = {th: -0.55, ph: 0.95, r: 17}, walker = {x: 1.35, z: 6.3, yaw: Math.PI * 0.85, pitch: -0.05};
  function size() {
    var w = root.clientWidth, h = Math.round(w * (root.clientWidth < 700 ? 1.1 : 0.62));
    R.setSize(w, h, false); cv.style.width = w + 'px'; cv.style.height = h + 'px'; cam.aspect = w / h; cam.updateProjectionMatrix();
    root.style.setProperty('--vi3d-h', h + 'px');
  }
  function setMode(m) {
    mode = m;
    root.setAttribute('data-mode', m);
    root.querySelectorAll('[data-set]').forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-set') === m ? 'true' : 'false'); });
    var walk = m === 'passeio';
    low.visible = !walk; full.visible = walk; glass.visible = walk; decor.visible = m !== 'estrutura';
    setClay(m === 'estrutura');
    cam.fov = walk ? 62 : 32; cam.updateProjectionMatrix();
    ui.plan.hidden = m !== 'planta'; ui.walk.hidden = !walk;
    if (ui.hint) ui.hint.textContent = walk ? 'Arraste para olhar · botões ou setas para andar' : 'Arraste para girar · role ou pince para aproximar';
  }
  function roomAt(x, z) {
    for (var i = 0; i < PLAN.rooms.length; i++) { var r = PLAN.rooms[i]; if (x >= r.x) { if (x <= r.x + r.w) { if (z >= r.y) { if (z <= r.y + r.d) return r.name; } } } }
    return '';
  }
  // colisão: não atravessar paredes fora dos vãos de porta
  function blocked(x0, z0, x1, z1) {
    if (x1 < 0.25 || x1 > PLAN.W - 0.25 || z1 < 0.25 || z1 > PLAN.D - 0.25) return true;
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
  var stops = [
    {x: 1.35, z: 6.3, yaw: Math.PI * 0.85}, {x: 3.0, z: 3.2, yaw: Math.PI * 1.0}, {x: 4.6, z: 3.6, yaw: Math.PI * 1.25},
    {x: 2.0, z: 5.4, yaw: Math.PI * 0.3}, {x: 5.2, z: 3.0, yaw: Math.PI * 0.5}, {x: 7.4, z: 3.6, yaw: Math.PI * 0.9},
    {x: 8.6, z: 1.2, yaw: Math.PI * 0.05}, {x: 5.2, z: 5.6, yaw: Math.PI * 0.5}, {x: 7.0, z: 5.4, yaw: Math.PI * 0.55}
  ];
  var guided = null;
  function startGuided() {
    setMode('passeio'); guided = {i: 0, t: 0, from: {x: walker.x, z: walker.z, yaw: walker.yaw}};
  }
  function stepGuided(dt) {
    if (!guided) return;
    var to = stops[guided.i]; guided.t += dt / (reduce ? 0.01 : 1.6);
    var k = Math.min(1, guided.t), e = k * k * (3 - 2 * k), f = guided.from;
    var dy = to.yaw - f.yaw; while (dy > Math.PI) dy -= Math.PI * 2; while (dy < -Math.PI) dy += Math.PI * 2;
    walker.x = f.x + (to.x - f.x) * e; walker.z = f.z + (to.z - f.z) * e; walker.yaw = f.yaw + dy * e; walker.pitch = -0.05;
    if (k >= 1) { guided.i++; guided.t = -0.9; guided.from = {x: walker.x, z: walker.z, yaw: walker.yaw}; if (guided.i >= stops.length) guided = null; }
  }
  // entrada
  var drag = null, keys = {}, hold = 0, pinch = null;
  cv.addEventListener('pointerdown', function (e) { drag = {x: e.clientX, y: e.clientY}; guided = null; cv.setPointerCapture(e.pointerId); });
  cv.addEventListener('pointermove', function (e) {
    if (!drag) return; var dx = e.clientX - drag.x, dy = e.clientY - drag.y; drag = {x: e.clientX, y: e.clientY};
    if (mode === 'passeio') { walker.yaw -= dx * 0.005; walker.pitch = Math.max(-0.6, Math.min(0.5, walker.pitch - dy * 0.004)); }
    else { orbit.th -= dx * 0.006; orbit.ph = Math.max(0.35, Math.min(1.35, orbit.ph - dy * 0.005)); }
  });
  cv.addEventListener('pointerup', function () { drag = null; });
  cv.addEventListener('wheel', function (e) { if (mode === 'passeio') return; e.preventDefault(); orbit.r = Math.max(9, Math.min(26, orbit.r + e.deltaY * 0.01)); }, {passive: false});
  cv.addEventListener('touchstart', function (e) { if (e.touches.length === 2) pinch = Math.hypot(e.touches[0].clientX - e.touches[1].clientX, e.touches[0].clientY - e.touches[1].clientY); }, {passive: true});
  cv.addEventListener('touchmove', function (e) { if (e.touches.length === 2) { if (pinch) { var d = Math.hypot(e.touches[0].clientX - e.touches[1].clientX, e.touches[0].clientY - e.touches[1].clientY); orbit.r = Math.max(9, Math.min(26, orbit.r - (d - pinch) * 0.03)); pinch = d; } } }, {passive: true});
  root.addEventListener('keydown', function (e) { keys[e.key] = true; if (mode === 'passeio') { if (e.key.indexOf('Arrow') === 0) e.preventDefault(); } });
  root.addEventListener('keyup', function (e) { keys[e.key] = false; });
  root.querySelectorAll('[data-set]').forEach(function (b) { b.addEventListener('click', function () { guided = null; setMode(b.getAttribute('data-set')); }); });
  root.querySelectorAll('[data-walk]').forEach(function (b) {
    var v = parseFloat(b.getAttribute('data-walk'));
    b.addEventListener('pointerdown', function (e) { e.preventDefault(); hold = v; guided = null; });
    ['pointerup', 'pointerleave', 'pointercancel'].forEach(function (ev) { b.addEventListener(ev, function () { hold = 0; }); });
  });
  root.querySelectorAll('[data-turn]').forEach(function (b) { b.addEventListener('click', function () { walker.yaw += parseFloat(b.getAttribute('data-turn')); guided = null; }); });
  var g = root.querySelector('[data-guided]'); if (g) g.addEventListener('click', startGuided);
  var sl = root.querySelector('input[type=range]'); if (sl) sl.addEventListener('input', function () { light = sl.value / 100; applyLight(); });
  // minimapa
  function drawMini() {
    var c = ui.mini; if (!c) return; var x = c.getContext('2d'), s = c.width / (PLAN.W + 1), o = s * 0.5;
    x.clearRect(0, 0, c.width, c.height); x.fillStyle = 'rgba(13,18,28,.78)'; x.fillRect(0, 0, c.width, c.height);
    x.strokeStyle = '#e2c48a'; x.lineWidth = 2;
    PLAN.walls.forEach(function (w) { x.beginPath(); x.moveTo(o + w[0] * s, o + w[1] * s); x.lineTo(o + w[2] * s, o + w[3] * s); x.stroke(); });
    var px = o + walker.x * s, pz = o + walker.z * s;
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
      var cx = PLAN.W / 2, cz = PLAN.D / 2;
      cam.position.set(cx + orbit.r * Math.sin(orbit.ph) * Math.sin(orbit.th), orbit.r * Math.cos(orbit.ph), cz + orbit.r * Math.sin(orbit.ph) * Math.cos(orbit.th));
      cam.lookAt(cx, 0, cz);
      if (!drag) { if (!reduce) { if (mode !== 'planta') orbit.th += dt * 0.04; } }
    }
    R.render(S, cam);
  }
  window.addEventListener('resize', size);
  size(); applyLight(); setMode('decorado'); requestAnimationFrame(frame);
  window.VI3D_READY = true;
  window.VI3D = {setMode: setMode, startGuided: startGuided, setLight: function (v) { light = v; applyLight(); }};
})();
