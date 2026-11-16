import sys
from split import render
G=(110,110,110); B=(69,88,118); A=(70,110,190)
def end(code,info,cta): return ('end',3.5,code,[(info,40,G),(cta,46,A),('Imobiliária Menegalli · CRECI 021362J',30,G)])
SH={
'AP0933':[
 ('full',1.6,'AP0933/02.jpg','in',['PROCURANDO','O PRIMEIRO','APARTAMENTO?']),
 ('full',1.4,'AP0933/04.jpg','in',['COM ESPAÇO','PARA A','FAMÍLIA.']),
 ('num',1.8,'AP0933/06.jpg','out','84 m²','de área útil'),
 ('split',2.4,[('AP0933/01.jpg','in','Varanda gourmet'),('AP0933/07.jpg','out','Cozinha planejada'),('AP0933/03.jpg','in','Sala 2 ambientes')]),
 ('num',1.6,'AP0933/18.jpg','in','3','dormitórios com armários\n1 suíte'),
 ('split',2.0,[('AP0933/19.jpg','in','Suíte'),('AP0933/14.jpg','out','Dormitório')]),
 ('num',1.6,'AP0933/13.jpg','in','2','vagas cobertas'),
 ('split',2.4,[('AP0933/26.jpg','lr','Piscina'),('AP0933/31.jpg','rl','Quadra'),('AP0933/32.jpg','lr','Salão de jogos')]),
 ('split',2.2,[('AP0933/34.jpg','rl','Brinquedoteca'),('AP0933/33.jpg','lr','Bicicletário'),('AP0933/28.jpg','rl','Portaria 24h')]),
 ('full',1.6,['AP0933/27.jpg','AP0933/29.jpg'],'lr',['ESTAÇÃO','PAULISTA.'],120),
 ('num',2.0,'AP0933/06.jpg','in','R$ 560 mil','condomínio R$ 600'),
 end('AP0933','Apartamento · Piracicaba','Agende sua visita pelo WhatsApp')],
'SO0342':[
 ('full',1.6,['SO0342/01.jpg','SO0342/02.jpg'],'lr',['UMA CASA','ONDE CADA','UM TEM','SEU LUGAR.']),
 ('num',1.8,['SO0342/17.jpg','SO0342/02.jpg'],'rl','15 m','de raia na piscina'),
 ('split',2.4,[('SO0342/08.jpg','lr','Sala para 3 ambientes'),('SO0342/14.jpg','rl','Cozinha integrada'),('SO0342/15.jpg','lr','Gourmet com churrasqueira e forno')]),
 ('full',1.6,['SO0342/09.jpg','SO0342/06.jpg'],'lr',['TUDO','VOLTADO','PARA O','QUINTAL.']),
 ('num',1.8,['SO0342/29.jpg','SO0342/30.jpg'],'lr','5','suítes\n4 com sacada'),
 ('split',2.4,[('SO0342/41.jpg','lr','Suíte'),('SO0342/47.jpg','rl','Hidromassagem'),('SO0342/53.jpg','lr','Sacada')]),
 ('split',2.0,[('SO0342/18.jpg','lr','Jardim'),('SO0342/17.jpg','rl','Área da piscina')]),
 ('num',1.8,['SO0342/57.jpg','SO0342/18.jpg','SO0342/19.jpg'],'lr','1.000 m²','de terreno\n504,86 m² construídos'),
 ('split',2.2,[('SO0342/55.jpg','lr','Park Campestre'),('SO0342/56.jpg','rl','Condomínio fechado'),('SO0342/58.jpg','lr','Piracicaba')]),
 ('num',2.0,['SO0342/01.jpg','SO0342/08.jpg','SO0342/15.jpg'],'lr','R$ 3,38 mi','aceita financiamento\nestuda permuta'),
 end('SO0342','Sobrado · Park Campestre','Agende sua visita pelo WhatsApp')],
'CA0438':[
 ('full',1.6,['CA0438/01.jpg','CA0438/02.jpg'],'lr',['NO CENTRO DE','PIRACICABA,'],96),
 ('full',1.6,['CA0438/03.jpg','CA0438/04.jpg'],'rl',['PERTO DO','TEATRO','MUNICIPAL.']),
 ('num',1.8,['CA0438/05.jpg','CA0438/06.jpg','CA0438/07.jpg'],'lr','1.558 m²','de terreno\ncerca de 27 x 56 m'),
 ('split',2.6,[('CA0438/03.jpg','lr','420 m² construídos'),('CA0438/04.jpg','rl','Área livre'),('CA0438/05.jpg','lr','Estacionamento')]),
 ('split',2.2,[('CA0438/06.jpg','lr','Av. Independência'),('CA0438/07.jpg','rl','Casa comercial')]),
 ('num',2.0,['CA0438/01.jpg','CA0438/03.jpg'],'lr','R$ 4,1 mi','casa comercial\nav. independência'),
 end('CA0438','Casa comercial · Centro','Fale com a Menegalli pelo WhatsApp')],
}
for k in sys.argv[1:]: render(k,SH[k])
