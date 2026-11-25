/* Projeto de demonstração 2 · apartamento tipo 2 dormitórios num edifício conceitual (redesenho Vídeo Imóvel).
   Os dados geométricos vêm de plans/apto.json (inseridos pelo build.py em __APTO__). */
window.VI3D_PLANS = window.VI3D_PLANS || {};
(function () {
  var P = __APTO__;
  var PI = Math.PI;
  P.stops = [
    {x: 3.75, z: 7.5, yaw: PI}, {x: 3.75, z: 6.2, yaw: PI}, {x: 4.4, z: 5.0, yaw: PI * 0.75},
    {x: 4.4, z: 4.0, yaw: -PI / 2}, {x: 7.5, z: 4.0, yaw: PI * 0.62}, {x: 8.8, z: 5.4, yaw: -PI * 0.65},
    {x: 7.5, z: 4.0, yaw: -PI * 0.6}, {x: 3.8, z: 3.6, yaw: PI}, {x: 3.8, z: 2.65, yaw: PI / 2},
    {x: 5.7, z: 2.7, yaw: PI * 0.72}, {x: 3.8, z: 2.65, yaw: PI}, {x: 3.75, z: 1.25, yaw: PI * 1.22},
    {x: 3.8, z: 2.65, yaw: -PI / 2}, {x: 2.1, z: 2.3, yaw: -PI * 0.68}, {x: 3.8, z: 2.65, yaw: 0}, {x: 3.8, z: 4.2, yaw: 0}
  ];
  // torre conceitual: 4 apartamentos por andar, núcleo central, 12 pavimentos-tipo sobre térreo
  var FLOORS = 12, FH = 2.9, BASE = 4.2, FEAT = 7;
  P.tower = {cx: -2.6, cz: 7.4, cy: (BASE + FLOORS * FH) / 2 - 1, r: 112, th: 2.35,
    label: 'Edifício conceitual · apartamento final 1 em destaque no ' + FEAT + 'º andar (exemplo)'};
  P.extras = function (k) {
    var box = k.box, M = k.M, m = k.mats;
    // guarda-corpo de vidro da varanda
    var rail = new k.THREE.MeshStandardMaterial({color: 0xcfe0e6, transparent: true, opacity: 0.3, roughness: 0.05});
    [k.low, k.full].forEach(function (g) {
      box(0.03, 1.05, 3.7, 9.48, 0.55, 4.85, rail, g, true); box(1.4, 1.05, 0.03, 8.8, 0.55, 3.02, rail, g, true); box(1.4, 1.05, 0.03, 8.8, 0.55, 6.68, rail, g, true);
      box(0.05, 0.04, 3.7, 9.48, 1.1, 4.85, m.metal, g, true); box(1.4, 0.04, 0.05, 8.8, 1.1, 3.02, m.metal, g, true); box(1.4, 0.04, 0.05, 8.8, 1.1, 6.68, m.metal, g, true);
    });
    // elevadores no hall do andar
    [0.35, 1.55].forEach(function (x) { box(0.9, 2.1, 0.04, x, 1.05, 8.0, m.metal, k.full, true); box(0.9, 1.5, 0.04, x, 0.75, 8.0, m.metal, k.low, true); });
    // porta de entrada (folha aberta para dentro)
    box(0.05, 2.08, 0.88, 4.2, 1.04, 6.24, m.oak, k.full);
    // torre
    var T = k.tower, white = M(0xf2efe9, 0.8), slabM = M(0xe9e5de, 0.9);
    var glassA = new k.THREE.MeshStandardMaterial({color: 0x5f7584, roughness: 0.15, metalness: 0.2, emissive: 0xffc98a, emissiveIntensity: 0});
    var glassB = new k.THREE.MeshStandardMaterial({color: 0x6d8291, roughness: 0.15, metalness: 0.2, emissive: 0xffc98a, emissiveIntensity: 0});
    var gold = new k.THREE.MeshStandardMaterial({color: 0xe2c48a, emissive: 0xe2c48a, emissiveIntensity: 0.7, roughness: 0.3});
    var x0 = -13.3, x1 = 8.1, z0 = 0, z1 = 14.8, W = x1 - x0, D = z1 - z0, cx = (x0 + x1) / 2, cz = (z0 + z1) / 2;
    box(90, 0.2, 80, cx, -0.1, cz, M(0x9aa58d, 1), T, true);
    box(W + 16, 0.06, D + 14, cx, 0.03, cz, M(0xd9d3c8, 0.9), T, true);
    box(W - 1.2, BASE - 0.3, D - 1.2, cx, (BASE - 0.3) / 2, cz, glassA, T, true);
    box(W + 0.6, 0.35, D + 0.6, cx, BASE - 0.15, cz, white, T, true);
    var bal = [[8.1, 9.5, 3.0, 6.7], [8.1, 9.5, 8.1, 11.8], [-14.7, -13.3, 3.0, 6.7], [-14.7, -13.3, 8.1, 11.8]];
    for (var f = 0; f < FLOORS; f++) {
      var y = BASE + f * FH;
      box(W, 0.22, D, cx, y + FH - 0.11, cz, slabM, T, true);
      box(W - 0.3, FH - 0.22, D - 0.3, cx, y + (FH - 0.22) / 2, cz, (f * 7) % 3 === 0 ? glassB : glassA, T, true);
      bal.forEach(function (b) {
        box(b[1] - b[0], 0.18, b[3] - b[2], (b[0] + b[1]) / 2, y + 0.09, (b[2] + b[3]) / 2, slabM, T, true);
        var ox = b[0] < 0 ? b[0] : b[1];
        box(0.04, 1.05, b[3] - b[2], ox, y + 0.7, (b[2] + b[3]) / 2, rail, T, true);
      });
    }
    // brises verticais nas fachadas longas
    for (var i = 0; i <= 15; i++) {
      var fx = x0 + 0.4 + i * (W - 0.8) / 15;
      box(0.18, FLOORS * FH, 0.5, fx, BASE + FLOORS * FH / 2, z0 - 0.25, white, T, true);
      box(0.18, FLOORS * FH, 0.5, fx, BASE + FLOORS * FH / 2, z1 + 0.25, white, T, true);
    }
    box(W + 0.6, 0.5, D + 0.6, cx, BASE + FLOORS * FH + 0.25, cz, white, T, true);
    box(6, 2.6, 5, -2.6, BASE + FLOORS * FH + 1.8, cz, white, T, true);
    // unidade em destaque
    var yf = BASE + (FEAT - 1) * FH;
    box(8.1, FH - 0.24, 6.7, 4.05, yf + (FH - 0.22) / 2, 3.35, gold, T, true);
    box(1.4, 0.2, 3.7, 8.8, yf + 0.1, 4.85, gold, T, true);
    // paisagismo
    [[-20, -6], [-8, -7], [5, -7], [14, 2], [14, 13], [-24, 10], [-6, 22], [8, 21]].forEach(function (p) {
      var tr = new k.THREE.Mesh(new k.THREE.SphereGeometry(2.2, 14, 10), k.mats.green); tr.position.set(p[0], 3.4, p[1]); T.add(tr);
      box(0.3, 2.4, 0.3, p[0], 1.2, p[1], M(0x6f5137, 0.8), T, true);
    });
    P.tower.onLight = function (night, dusk) { glassA.emissiveIntensity = night * 0.55 + dusk * 0.15; glassB.emissiveIntensity = night * 0.25; };
  };
  P.furnish = function (k) {
    var box = k.box, cyl = k.cyl, lamp = k.lamp, M = k.M, m = k.mats, full = k.full, decor = k.decor;
    var fab = m.fab, fab2 = m.fab2, oak = m.oak, dark = m.dark, white = m.white, rug = m.rug, linen = m.linen, stone = m.stone;
    // dormitório
    box(0.95, 0.32, 1.95, 0.6, 0.16, 1.15, oak); box(0.9, 0.18, 1.9, 0.6, 0.41, 1.17, linen); box(0.9, 0.04, 1.0, 0.6, 0.52, 1.5, fab); box(0.55, 0.12, 0.32, 0.6, 0.56, 0.38, white);
    box(0.45, 0.5, 0.4, 1.35, 0.25, 0.3, oak); lamp(1.35, 0.66, 0.3, 0.09);
    box(0.6, 0.04, 1.1, 2.38, 0.75, 0.9, oak); box(0.04, 0.73, 1.0, 2.1, 0.37, 0.9, oak); box(0.45, 0.45, 0.45, 1.9, 0.23, 1.0, fab2); box(0.03, 0.3, 0.45, 2.6, 1.0, 0.9, dark);
    box(1.8, 2.2, 0.58, 1.05, 1.1, 2.88, white); box(1.2, 0.02, 0.8, 1.5, 0.01, 1.3, rug, decor, true);
    // banheiro
    box(0.9, 0.02, 0.9, 4.4, 0.01, 0.5, M(0xbfc4c4, 0.2), decor, true);
    var gs = new k.THREE.Mesh(new k.THREE.BoxGeometry(0.02, 2.0, 0.9), m.glass); gs.position.set(3.93, 1.0, 0.5); decor.add(gs);
    box(0.4, 0.4, 0.6, 3.1, 0.2, 0.4, white); box(0.4, 0.35, 0.18, 3.1, 0.6, 0.12, white);
    box(0.45, 0.8, 0.9, 2.95, 0.4, 1.4, oak); box(0.47, 0.04, 0.92, 2.95, 0.82, 1.4, stone); box(0.02, 0.8, 0.7, 2.78, 1.5, 1.4, M(0xdfe7ea, 0.05));
    // dormitório casal
    box(2.05, 0.32, 1.7, 7.05, 0.16, 1.6, oak); box(2.0, 0.2, 1.65, 7.02, 0.41, 1.6, linen); box(1.0, 0.04, 1.65, 6.55, 0.52, 1.6, fab2);
    box(0.32, 0.14, 0.6, 7.85, 0.58, 1.2, white); box(0.32, 0.14, 0.6, 7.85, 0.58, 2.0, white); box(0.07, 1.1, 1.9, 8.04, 0.55, 1.6, M(0x7d6a57, 0.9));
    box(0.4, 0.5, 0.45, 7.85, 0.25, 0.45, oak); box(0.4, 0.5, 0.45, 7.85, 0.25, 2.75, oak); lamp(7.85, 0.68, 0.45, 0.09); lamp(7.85, 0.68, 2.75, 0.09);
    box(0.6, 2.2, 1.9, 5.22, 1.1, 1.1, oak); box(1.0, 0.02, 2.0, 5.85, 0.01, 1.6, rug, decor, true);
    // cozinha integrada
    box(0.62, 0.88, 2.4, 0.31, 0.44, 4.6, white); box(0.64, 0.04, 2.42, 0.32, 0.9, 4.6, stone);
    box(0.5, 0.02, 0.6, 0.32, 0.93, 3.9, dark); box(0.45, 0.02, 0.6, 0.32, 0.925, 5.2, m.metal);
    box(0.36, 0.7, 1.0, 0.18, 1.95, 3.95, white, full);
    box(0.68, 1.95, 0.72, 0.36, 0.98, 6.25, M(0xc9cbcd, 0.3));
    box(0.9, 0.9, 1.6, 1.85, 0.45, 4.85, white); box(1.0, 0.04, 1.7, 1.85, 0.92, 4.85, stone);
    [4.4, 5.3].forEach(function (z) { box(0.38, 0.06, 0.38, 2.55, 0.66, z, fab2); box(0.04, 0.64, 0.04, 2.55, 0.32, z, dark); });
    // jantar
    cyl(0.5, 0.5, 0.05, 3.8, 0.76, 4.9, oak); cyl(0.06, 0.06, 0.73, 3.8, 0.37, 4.9, dark);
    [[3.15, 4.9], [4.45, 4.9], [3.8, 4.25], [3.8, 5.55]].forEach(function (p) { box(0.42, 0.06, 0.42, p[0], 0.46, p[1], fab2); box(0.04, 0.44, 0.04, p[0], 0.22, p[1], dark); });
    cyl(0.01, 0.01, 0.6, 3.8, 2.4, 4.9, dark, full); lamp(3.8, 2.05, 4.9, 0.16);
    k.plant(4.65, 6.35, 0.9);
    // estar
    box(2.6, 0.02, 2.0, 6.4, 0.01, 4.9, rug, decor, true);
    box(1.8, 0.45, 0.42, 6.5, 0.23, 3.45, oak); box(1.4, 0.8, 0.05, 6.5, 1.12, 3.3, M(0x111111, 0.25));
    box(2.2, 0.4, 0.9, 6.4, 0.2, 5.75, fab); box(2.2, 0.5, 0.2, 6.4, 0.6, 6.15, fab); box(0.2, 0.6, 0.9, 5.3, 0.3, 5.75, fab); box(0.2, 0.6, 0.9, 7.5, 0.3, 5.75, fab);
    box(0.95, 0.12, 0.75, 5.9, 0.46, 5.7, linen); box(0.95, 0.12, 0.75, 6.9, 0.46, 5.7, linen);
    cyl(0.38, 0.38, 0.06, 6.4, 0.36, 4.55, oak); cyl(0.05, 0.05, 0.33, 6.4, 0.17, 4.55, dark);
    cyl(0.02, 0.02, 1.5, 5.1, 0.75, 6.4, dark); lamp(5.1, 1.55, 6.4, 0.15);
    // varanda
    cyl(0.3, 0.3, 0.04, 8.85, 0.72, 4.2, oak); cyl(0.04, 0.04, 0.7, 8.85, 0.35, 4.2, dark);
    box(0.42, 0.45, 0.42, 8.85, 0.22, 3.6, fab2); box(0.42, 0.45, 0.42, 8.85, 0.22, 4.8, fab2);
    k.plant(9.15, 6.3, 0.9); k.plant(9.15, 3.35, 0.75);
    // hall do andar
    k.plant(7.75, 7.75, 0.8);
  };
  window.VI3D_PLANS.apto = P;
})();
