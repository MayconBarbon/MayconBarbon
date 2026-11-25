/* Projeto de demonstração 1 · casa térrea 2 dormitórios (redesenho Vídeo Imóvel). */
window.VI3D_PLANS = window.VI3D_PLANS || {};
(function () {
  var P = {"nome": "Casa térrea 2 dormitórios · demonstração", "W": 10.5, "D": 7.5, "T": 0.15, "H": 2.8, "walls": [[0, 0, 8, 0], [8, 0, 8, 6], [8, 6, 0, 6], [0, 6, 0, 0], [3, 0, 3, 3], [0, 3, 4, 3], [4, 3, 4, 6], [4.5, 0, 4.5, 2], [3, 2, 4.5, 2]], "openings": [{"w": 3, "a": 3.8, "b": 5.0, "type": "window", "sill": 1.0, "h": 1.2}, {"w": 3, "a": 0.9, "b": 2.1, "type": "window", "sill": 1.0, "h": 1.2}, {"w": 2, "a": 5.4, "b": 6.6, "type": "window", "sill": 1.0, "h": 1.2}, {"w": 2, "a": 1.6, "b": 3.0, "type": "window", "sill": 0.5, "h": 1.7}, {"w": 0, "a": 3.5, "b": 4.0, "type": "window", "sill": 1.6, "h": 0.5}, {"w": 0, "a": 5.8, "b": 7.2, "type": "window", "sill": 1.1, "h": 1.0}, {"w": 1, "a": 4.1, "b": 5.1, "type": "door"}, {"w": 2, "a": 0.3, "b": 1.2, "type": "door"}, {"w": 4, "a": 2.1, "b": 2.9, "type": "door"}, {"w": 6, "a": 0.2, "b": 1.0, "type": "door"}, {"w": 8, "a": 0.4, "b": 1.1, "type": "door"}], "rooms": [{"name": "Dormitório", "x": 0, "y": 0, "w": 3, "d": 3, "floor": "wood"}, {"name": "Banheiro", "x": 3, "y": 0, "w": 1.5, "d": 2, "floor": "tile"}, {"name": "Circulação", "x": 3, "y": 2, "w": 1.5, "d": 1, "floor": "wood", "nolabel": true}, {"name": "Cozinha", "x": 4.5, "y": 0, "w": 3.5, "d": 3, "floor": "stone"}, {"name": "Dormitório casal", "x": 0, "y": 3, "w": 4, "d": 3, "floor": "wood"}, {"name": "Sala", "x": 4, "y": 3, "w": 4, "d": 3, "floor": "wood"}, {"name": "Área", "x": 8, "y": 2.5, "w": 2.5, "d": 5, "floor": "deck", "ext": true}, {"name": "Área", "x": 4, "y": 6, "w": 4, "d": 1.5, "floor": "deck", "ext": true, "nolabel": true}], "ceil": [[0, 0, 8, 6]], "bounds": [0, 0, 10.5, 7.5], "ground": "grass", "start": {"x": 7.25, "z": 7.0, "yaw": 3.14159}, "orbitR": 18, "planta": "planta.svg"};
  P.stops = [
      {x: 7.25, z: 7.0, yaw: Math.PI}, {x: 7.25, z: 5.3, yaw: Math.PI}, {x: 7.3, z: 3.7, yaw: -Math.PI * 0.6},
      {x: 6.2, z: 2.7, yaw: Math.PI}, {x: 4.6, z: 2.5, yaw: -Math.PI / 2}, {x: 3.75, z: 2.5, yaw: -Math.PI / 2},
      {x: 2.3, z: 2.4, yaw: Math.PI * 1.2}, {x: 3.75, z: 2.5, yaw: Math.PI}, {x: 3.75, z: 1.4, yaw: Math.PI},
      {x: 3.75, z: 2.5, yaw: Math.PI * 0.4}, {x: 4.3, z: 2.75, yaw: 0}, {x: 4.4, z: 3.6, yaw: -Math.PI / 2}, {x: 3.5, z: 3.6, yaw: -Math.PI / 2}, {x: 2.4, z: 4.4, yaw: -Math.PI * 0.6},
      {x: 3.5, z: 3.6, yaw: Math.PI / 2}, {x: 4.6, z: 3.6, yaw: Math.PI * 0.6}, {x: 7.3, z: 3.7, yaw: 0}, {x: 7.3, z: 4.6, yaw: Math.PI / 2},
      {x: 8.6, z: 4.6, yaw: Math.PI * 0.75}, {x: 9.3, z: 5.4, yaw: -Math.PI * 0.85}
    ];
  P.extras = function (k) {
  var box = k.box, cyl = k.cyl, lamp = k.lamp, M = k.M, THREE = k.THREE, decor = k.decor, full = k.full, low = k.low;
  var m = k.mats, fab = m.fab, fab2 = m.fab2, oak = m.oak, dark = m.dark, white = m.white, green = m.green, rug = m.rug, linen = m.linen, stoneK = m.stone;

  // beiral sobre a área (pergolado)
  for (var pg = 0; pg < 9; pg++) { box(0.08, 0.14, 5.0, 8.15 + pg * 0.29, P.H - 0.1, 5.0, M(0x6f5137, 0.7), full); }
  [[10.4, 2.6], [10.4, 7.4], [4.1, 7.4]].forEach(function (p) { box(0.12, P.H, 0.12, p[0], P.H / 2, p[1], M(0x6f5137, 0.7), full); box(0.12, 1.5, 0.12, p[0], 0.75, p[1], M(0x6f5137, 0.7), low); });
  };
  P.furnish = function (k) {
  var box = k.box, cyl = k.cyl, lamp = k.lamp, M = k.M, THREE = k.THREE, decor = k.decor, full = k.full, low = k.low;
  var m = k.mats, fab = m.fab, fab2 = m.fab2, oak = m.oak, dark = m.dark, white = m.white, green = m.green, rug = m.rug, linen = m.linen, stoneK = m.stone;

  // dormitório
  box(0.95, 0.32, 1.95, 0.65, 0.16, 1.2, oak); box(0.9, 0.18, 1.9, 0.65, 0.41, 1.22, linen); box(0.9, 0.04, 1.0, 0.65, 0.52, 1.55, fab); box(0.55, 0.12, 0.32, 0.65, 0.56, 0.42, white);
  box(0.5, 0.5, 0.4, 1.45, 0.25, 0.3, oak); lamp(1.45, 0.66, 0.3, 0.09);
  box(0.6, 0.04, 1.1, 2.6, 0.75, 0.85, oak); box(0.04, 0.73, 1.0, 2.33, 0.37, 0.85, oak); box(0.45, 0.45, 0.45, 2.25, 0.23, 1.0, fab2); box(0.4, 0.3, 0.03, 2.75, 1.0, 0.9, dark);
  box(1.7, 2.2, 0.55, 1.05, 1.1, 2.68, white); box(1.2, 0.02, 0.8, 1.6, 0.01, 1.25, rug, decor, true);
  // banheiro
  box(0.8, 0.02, 0.8, 3.5, 0.01, 0.5, M(0xbfc4c4, 0.2), decor, true);
  var gl2 = new THREE.Mesh(new THREE.BoxGeometry(0.8, 2.0, 0.02), new THREE.MeshStandardMaterial({color: 0xcfe0e6, transparent: true, opacity: 0.25})); gl2.position.set(3.5, 1.0, 0.92); decor.add(gl2);
  box(0.4, 0.4, 0.6, 4.2, 0.2, 0.45, white); box(0.5, 0.8, 0.45, 4.22, 0.4, 1.45, oak); box(0.52, 0.04, 0.47, 4.22, 0.82, 1.45, stoneK); box(0.02, 0.7, 0.5, 4.43, 1.45, 1.45, M(0xdfe7ea, 0.05));
  // cozinha
  box(3.3, 0.88, 0.62, 6.15, 0.44, 0.33, white); box(3.3, 0.04, 0.64, 6.15, 0.9, 0.33, stoneK); box(2.6, 0.7, 0.36, 5.8, 1.95, 0.2, white, full);
  box(0.75, 1.95, 0.68, 7.55, 0.98, 0.38, M(0xc9cbcd, 0.3)); box(0.6, 0.02, 0.45, 5.2, 0.93, 0.33, dark, decor, true);
  cyl(0.55, 0.55, 0.05, 6.1, 0.76, 1.85, oak); cyl(0.06, 0.06, 0.73, 6.1, 0.37, 1.85, dark);
  [[5.35, 1.85], [6.85, 1.85], [6.1, 1.1], [6.1, 2.6]].forEach(function (p) { box(0.42, 0.06, 0.42, p[0], 0.46, p[1], fab2); box(0.04, 0.44, 0.04, p[0], 0.22, p[1], dark); });
  cyl(0.01, 0.01, 0.6, 6.1, 2.5, 1.85, dark, full); lamp(6.1, 2.15, 1.85, 0.16);
  // dormitório casal
  box(1.7, 0.32, 2.05, 1.8, 0.16, 4.15, oak); box(1.65, 0.2, 2.0, 1.8, 0.41, 4.18, linen); box(1.65, 0.04, 1.0, 1.8, 0.52, 4.6, fab2);
  box(0.6, 0.14, 0.32, 1.4, 0.58, 3.35, white); box(0.6, 0.14, 0.32, 2.2, 0.58, 3.35, white); box(1.9, 1.1, 0.07, 1.8, 0.55, 3.1, M(0x7d6a57, 0.9));
  box(0.45, 0.5, 0.4, 0.65, 0.25, 3.3, oak); box(0.45, 0.5, 0.4, 2.95, 0.25, 3.3, oak); lamp(0.65, 0.68, 3.3, 0.09); lamp(2.95, 0.68, 3.3, 0.09);
  box(0.58, 2.2, 1.6, 3.68, 1.1, 5.1, oak); box(2.2, 0.02, 1.5, 1.8, 0.01, 4.4, rug, decor, true);
  // sala (TV na parede da circulação íntima, sofá de costas para a área)
  box(2.4, 0.02, 2.2, 5.45, 0.01, 4.95, rug, decor, true);
  box(0.9, 0.4, 2.1, 6.45, 0.2, 4.95, fab); box(0.2, 0.5, 2.1, 6.82, 0.6, 4.95, fab); box(0.9, 0.6, 0.2, 6.45, 0.3, 3.95, fab); box(0.9, 0.6, 0.2, 6.45, 0.3, 5.95, fab);
  box(0.75, 0.12, 0.95, 6.4, 0.46, 4.45, linen); box(0.75, 0.12, 0.95, 6.4, 0.46, 5.45, linen);
  cyl(0.42, 0.42, 0.06, 5.25, 0.36, 4.95, oak); cyl(0.05, 0.05, 0.33, 5.25, 0.17, 4.95, dark);
  box(0.4, 0.45, 1.7, 4.3, 0.23, 5.05, oak); box(0.05, 0.8, 1.4, 4.13, 1.12, 5.05, M(0x111111, 0.25));
  cyl(0.02, 0.02, 1.5, 7.55, 0.75, 5.7, dark); lamp(7.55, 1.55, 5.7, 0.15);
  // área externa
  [[9.0, 3.4], [9.9, 3.4]].forEach(function (p) { box(0.65, 0.35, 0.65, p[0], 0.18, p[1], fab2); box(0.65, 0.45, 0.12, p[0], 0.55, p[1] - 0.28, fab2); });
  cyl(0.3, 0.3, 0.04, 9.45, 0.45, 4.1, oak); cyl(0.04, 0.04, 0.42, 9.45, 0.21, 4.1, dark);
  box(1.4, 0.05, 0.8, 9.3, 0.76, 6.4, oak); [[8.85, 6.4], [9.75, 6.4]].forEach(function (p) { box(0.08, 0.74, 0.7, p[0], 0.37, p[1], oak); });
  [[8.9, 5.7], [9.7, 5.7], [8.9, 7.1], [9.7, 7.1]].forEach(function (p) { box(0.42, 0.45, 0.42, p[0], 0.22, p[1], fab2); });
  box(1.6, 0.42, 0.45, 5.5, 0.21, 7.15, oak);
  // plantas
  [[2.75, 2.7], [7.65, 5.65], [10.2, 2.85], [4.4, 7.15], [7.6, 7.15]].forEach(function (p) {
    box(0.34, 0.42, 0.34, p[0], 0.21, p[1], M(0xd8d0c2));
    var a = new THREE.Mesh(new THREE.SphereGeometry(0.36, 18, 12), green); a.position.set(p[0], 0.78, p[1]); a.castShadow = true; decor.add(a);
    var b = new THREE.Mesh(new THREE.SphereGeometry(0.24, 16, 10), green); b.position.set(p[0] + 0.12, 1.05, p[1] - 0.05); b.castShadow = true; decor.add(b);
  });
  };
  window.VI3D_PLANS.casa = P;
})();
