import sys, split
from split import render
G=(110,110,110); A=(70,110,190)
def end(code,info,cta): return ('end',3.5,code,[(info,40,G),(cta,46,A),('Imobiliária Menegalli · CRECI 021362J',30,G)])
split.RENDERS.update({f'CA1097/{i:02d}.jpg' for i in range(1,19)})
SH={
'CH0149':[
 ('full',1.6,['CH0149/01.jpg','CH0149/27.jpg'],'lr',['UMA CHÁCARA','CERCADA DE','NATUREZA.'],104),
 ('num',1.8,['CH0149/32.jpg','CH0149/37.jpg'],'lr','7.750 m²','de área total\nvertentes das águas · são pedro'),
 ('split',2.4,[('CH0149/08.jpg','lr','Piscina'),('CH0149/07.jpg','rl','Espaço gourmet'),('CH0149/24.jpg','lr','Varanda em três lados')]),
 ('full',1.6,['CH0149/13.jpg','CH0149/12.jpg'],'lr',['SALA COM','LAREIRA.']),
 ('num',1.8,['CH0149/17.jpg','CH0149/18.jpg'],'lr','3','dormitórios\n2 suítes'),
 ('split',2.4,[('CH0149/34.jpg','lr','Lago'),('CH0149/29.jpg','rl','Capela'),('CH0149/33.jpg','lr','Campo de futebol')]),
 ('split',2.2,[('CH0149/35.jpg','rl','Pomar'),('CH0149/36.jpg','lr','Natureza ao redor'),('CH0149/10.jpg','rl','Área da piscina')]),
 ('full',1.6,['CH0149/38.jpg','CH0149/28.jpg'],'lr',['PARA','DESCANSAR','E RECEBER.']),
 ('num',2.0,['CH0149/01.jpg','CH0149/08.jpg'],'lr','R$ 1,8 mi','chácara · são pedro-sp'),
 end('CH0149','Chácara · São Pedro','Agende sua visita pelo WhatsApp')],
'CA1097':[
 ('full',1.6,['CA1097/03.jpg','CA1097/04.jpg'],'lr',['CASA','MODERNA EM','CONDOMÍNIO.'],110),
 ('num',1.8,['CA1097/19.jpg','CA1097/20.jpg'],'lr','166 m²','construídos\nterreno de 231,41 m²'),
 ('split',2.4,[('CA1097/05.jpg','lr','Sala com pé-direito alto'),('CA1097/07.jpg','rl','Cozinha'),('CA1097/16.jpg','lr','Gourmet com churrasqueira')]),
 ('num',1.8,['CA1097/14.jpg','CA1097/09.jpg'],'lr','3','dormitórios\n2 suítes'),
 ('split',2.0,[('CA1097/13.jpg','lr','Banheiro'),('CA1097/17.jpg','rl','Circulação')]),
 ('full',1.6,['CA1097/21.jpg','CA1097/22.jpg'],'lr',['VILLA','D’ITÁLIA II.']),
 ('split',2.4,[('CA1097/19.jpg','lr','Portaria'),('CA1097/25.jpg','rl','Quadra'),('CA1097/27.jpg','lr','Espaço de lazer')]),
 ('num',2.0,['CA1097/20.jpg','CA1097/30.jpg'],'lr','R$ 1,35 mi','2 vagas cobertas\naceita financiamento'),
 end('CA1097','Casa · Villa D’Itália II','Agende sua visita pelo WhatsApp')],
'CH0134':[
 ('full',1.6,['CH0134/01.jpg','CH0134/04.jpg'],'lr',['UM CLUBE','PARTICULAR','EM CASA.']),
 ('num',1.8,['CH0134/15.jpg','CH0134/17.jpg'],'lr','850 m²','construídos\nterreno de 1.142 m²'),
 ('split',2.4,[('CH0134/08.jpg','lr','Living'),('CH0134/12.jpg','rl','Sala de jantar'),('CH0134/14.jpg','lr','Cozinha')]),
 ('split',2.4,[('CH0134/23.jpg','rl','Gourmet para 50 pessoas'),('CH0134/36.jpg','lr','Academia'),('CH0134/32.jpg','rl','Sala de jogos')]),
 ('num',1.8,['CH0134/43.jpg','CH0134/39.jpg'],'lr','6','suítes\n10 banheiros'),
 ('split',2.4,[('CH0134/16.jpg','lr','Piscina'),('CH0134/07.jpg','rl','Parquinho'),('CH0134/05.jpg','lr','Jardim')]),
 ('full',1.6,['CH0134/57.jpg','CH0134/58.jpg'],'lr',['COLINAS DO','PIRACICABA.'],104),
 ('num',2.0,['CH0134/01.jpg','CH0134/24.jpg'],'lr','R$ 2,5 mi','totalmente mobiliada\n6 suítes · área gourmet'),
 end('CH0134','Chácara · Colinas do Piracicaba','Agende sua visita pelo WhatsApp')],
}
for k in sys.argv[1:]: render(k,SH[k])
