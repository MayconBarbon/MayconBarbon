// Planta conceitual de demonstração (metros). Mesma geometria para planta 2D, estrutura 3D e visualização final.
window.PLAN = {
  W: 10, D: 7, T: 0.15, H: 2.7,
  // paredes: [x1,y1,x2,y2]
  walls: [
    [0,0,10,0],[10,0,10,7],[10,7,0,7],[0,7,0,0],   // perímetro
    [6,0,6,7],                                       // divisa sala / íntimos
    [6,4,10,4]                                       // suíte / banheiro
  ],
  // vãos: parede índice, de, até (ao longo da parede, em metros a partir do 1º ponto), tipo, peitoril, altura
  openings: [
    {w:0, a:1.0, b:5.0, type:'window', sill:0.4, h:1.9},   // janela sala (frente)
    {w:0, a:7.0, b:9.4, type:'window', sill:0.9, h:1.3},   // janela suíte
    {w:1, a:5.0, b:6.0, type:'window', sill:1.5, h:0.6},   // basculante banheiro
    {w:2, a:8.2, b:9.1, type:'door'},                       // porta de entrada (x 0.9..1.8)
    {w:4, a:2.6, b:3.4, type:'door'},                       // sala -> suíte
    {w:4, a:5.2, b:6.0, type:'door'}                        // sala -> banheiro
  ],
  rooms: [
    {name:'Estar / jantar / cozinha', x:0, y:0, w:6, d:7},
    {name:'Suíte', x:6, y:0, w:4, d:4},
    {name:'Banho', x:6, y:4, w:4, d:3}
  ]
};
