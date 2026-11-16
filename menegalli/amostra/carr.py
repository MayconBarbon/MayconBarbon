import render as R, cv2, numpy as np
from PIL import Image
R.W,R.H=1080,1350
sl=[('AP0933/02.jpg','AP0933 · ESTAÇÃO PAULISTA','R$ 560 mil · 84 m² · 3 quartos · 2 vagas cobertas'),
('AP0933/01.jpg',None,'Varanda gourmet planejada'),('AP0933/04.jpg',None,'Sala para dois ambientes'),
('AP0933/07.jpg',None,'Cozinha planejada com fogão'),('AP0933/19.jpg',None,'Suíte com armários'),
('AP0933/14.jpg',None,'3 dormitórios com armários'),('AP0933/26.jpg',None,'Lazer com piscina adulto e infantil')]
import os; os.makedirs('AP0933_carrossel',exist_ok=True)
for i,(f,k,t) in enumerate(sl,1):
    img=R.treat(R.M+f); fr=next(R.frames_for(img,0.04,'none')); ov=R.overlay(k,t)
    a=ov[...,3:4]/255; rgb=cv2.cvtColor(ov[...,:3],cv2.COLOR_RGB2BGR)
    cv2.imwrite(f'AP0933_carrossel/{i:02d}.jpg',(fr*(1-a)+rgb*a).astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,92])
c=R.card([('R$ 560.000',R.F8,96,R.WHITE,10),('84 m² · 3 dorm. · 1 suíte · 2 vagas cobertas',R.F7,40,R.WHITE,6),('Condomínio R$ 600',R.F7,38,R.MUT,60),
 ('Chame no WhatsApp e agende sua visita',R.F8,56,R.ACCT,60),('AP0933 · Imobiliária Menegalli · CRECI 021362J',R.F7,32,R.MUT,0)])
cv2.imwrite('AP0933_carrossel/08.jpg',c,[cv2.IMWRITE_JPEG_QUALITY,92])
