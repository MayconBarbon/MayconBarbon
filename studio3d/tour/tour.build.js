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

/* Projeto de demonstração 2 · apartamento tipo 2 dormitórios num edifício conceitual (redesenho Vídeo Imóvel).
   Os dados geométricos vêm de plans/apto.json (inseridos pelo build.py em {"nome":"Apartamento tipo 2 dormitórios · edifício de demonstração","T":0.15,"H":2.7,"bounds":[-0.6,0,9.5,8.1],"ground":"slab","ceil":[[-0.6,0,8.1,8.1],[8.1,3.0,9.5,6.7]],"walls":[[0,0,8.1,0],[8.1,0,8.1,6.7],[8.1,6.7,0,6.7],[0,6.7,0,0],[2.7,0,2.7,3.2],[4.9,0,4.9,3.2],[2.7,2.0,4.9,2.0],[0,3.2,2.9,3.2],[4.7,3.2,8.1,3.2],[-0.6,8.1,8.1,8.1],[-0.6,6.7,-0.6,8.1],[8.1,6.7,8.1,8.1],[-0.6,6.7,0,6.7]],"openings":[{"w":0,"a":0.7,"b":2.0,"type":"window","sill":1.0,"h":1.3},{"w":0,"a":3.5,"b":4.1,"type":"window","sill":1.6,"h":0.5},{"w":0,"a":5.6,"b":7.4,"type":"window","sill":1.0,"h":1.3},{"w":1,"a":3.5,"b":5.9,"type":"door","slide":true,"h":2.25},{"w":2,"a":3.9,"b":4.8,"type":"door"},{"w":3,"a":0.9,"b":2.1,"type":"window","sill":1.1,"h":1.0},{"w":4,"a":2.3,"b":3.05,"type":"door"},{"w":5,"a":2.3,"b":3.05,"type":"door","swing":-1},{"w":6,"a":0.7,"b":1.4,"type":"door"}],"rooms":[{"name":"Dormitório","x":0,"y":0,"w":2.7,"d":3.2,"floor":"wood"},{"name":"Banheiro","x":2.7,"y":0,"w":2.2,"d":2.0,"floor":"tile"},{"name":"Circulação","x":2.7,"y":2.0,"w":2.2,"d":1.2,"floor":"wood","nolabel":true},{"name":"Dormitório casal","x":4.9,"y":0,"w":3.2,"d":3.2,"floor":"wood"},{"name":"Cozinha","x":0,"y":3.2,"w":2.7,"d":3.5,"floor":"porc"},{"name":"Jantar","x":2.7,"y":3.2,"w":2.2,"d":3.5,"floor":"wood"},{"name":"Estar","x":4.9,"y":3.2,"w":3.2,"d":3.5,"floor":"wood"},{"name":"Varanda","x":8.1,"y":3.0,"w":1.4,"d":3.7,"floor":"deck","ext":true},{"name":"Hall do andar","x":-0.6,"y":6.7,"w":8.7,"d":1.4,"floor":"stone","ext":true}],"start":{"x":3.75,"z":7.5,"yaw":3.14159},"orbitR":17,"planta":"planta-apto.svg","dims":{"top":[0,2.7,4.9,8.1],"right":[0,3.2,6.7],"varanda":[3.0,6.7]}}). */
window.VI3D_PLANS = window.VI3D_PLANS || {};
(function () {
  var P = {"nome":"Apartamento tipo 2 dormitórios · edifício de demonstração","T":0.15,"H":2.7,"bounds":[-0.6,0,9.5,8.1],"ground":"slab","ceil":[[-0.6,0,8.1,8.1],[8.1,3.0,9.5,6.7]],"walls":[[0,0,8.1,0],[8.1,0,8.1,6.7],[8.1,6.7,0,6.7],[0,6.7,0,0],[2.7,0,2.7,3.2],[4.9,0,4.9,3.2],[2.7,2.0,4.9,2.0],[0,3.2,2.9,3.2],[4.7,3.2,8.1,3.2],[-0.6,8.1,8.1,8.1],[-0.6,6.7,-0.6,8.1],[8.1,6.7,8.1,8.1],[-0.6,6.7,0,6.7]],"openings":[{"w":0,"a":0.7,"b":2.0,"type":"window","sill":1.0,"h":1.3},{"w":0,"a":3.5,"b":4.1,"type":"window","sill":1.6,"h":0.5},{"w":0,"a":5.6,"b":7.4,"type":"window","sill":1.0,"h":1.3},{"w":1,"a":3.5,"b":5.9,"type":"door","slide":true,"h":2.25},{"w":2,"a":3.9,"b":4.8,"type":"door"},{"w":3,"a":0.9,"b":2.1,"type":"window","sill":1.1,"h":1.0},{"w":4,"a":2.3,"b":3.05,"type":"door"},{"w":5,"a":2.3,"b":3.05,"type":"door","swing":-1},{"w":6,"a":0.7,"b":1.4,"type":"door"}],"rooms":[{"name":"Dormitório","x":0,"y":0,"w":2.7,"d":3.2,"floor":"wood"},{"name":"Banheiro","x":2.7,"y":0,"w":2.2,"d":2.0,"floor":"tile"},{"name":"Circulação","x":2.7,"y":2.0,"w":2.2,"d":1.2,"floor":"wood","nolabel":true},{"name":"Dormitório casal","x":4.9,"y":0,"w":3.2,"d":3.2,"floor":"wood"},{"name":"Cozinha","x":0,"y":3.2,"w":2.7,"d":3.5,"floor":"porc"},{"name":"Jantar","x":2.7,"y":3.2,"w":2.2,"d":3.5,"floor":"wood"},{"name":"Estar","x":4.9,"y":3.2,"w":3.2,"d":3.5,"floor":"wood"},{"name":"Varanda","x":8.1,"y":3.0,"w":1.4,"d":3.7,"floor":"deck","ext":true},{"name":"Hall do andar","x":-0.6,"y":6.7,"w":8.7,"d":1.4,"floor":"stone","ext":true}],"start":{"x":3.75,"z":7.5,"yaw":3.14159},"orbitR":17,"planta":"planta-apto.svg","dims":{"top":[0,2.7,4.9,8.1],"right":[0,3.2,6.7],"varanda":[3.0,6.7]}};
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
    var w = root.clientWidth, h = Math.round(w * (root.clientWidth < 700 ? 1.1 : 0.62));
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
