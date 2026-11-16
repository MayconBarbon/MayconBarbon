import cv2, numpy as np, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
S='/tmp/claude-0/-home-user-MayconBarbon/23adc415-3614-5acc-b755-85d3f8a0a095/scratchpad'
M=S+'/men/'; O=S+'/menv/'
F8=S+'/ig/fonts/Manrope-800.ttf'; F7=S+'/ig/fonts/Manrope-700.ttf'
W,H,FPS=1080,1920,30; NAVY=(13,26,46); ACC=(19,168,158)
def font(p,s): return ImageFont.truetype(p,s)
def treat(path):
    im=cv2.imread(path).astype(np.float32)/255
    # equilíbrio de branco suave (gray world 40%)
    m=im.reshape(-1,3).mean(0); g=m.mean(); im=im*(1+0.4*(g/m-1))
    # levanta sombras e dá contraste leve
    im=np.clip(im,0,1)**0.9
    im=np.clip((im-0.5)*1.08+0.5+0.01,0,1)
    hsv=cv2.cvtColor((im*255).astype(np.uint8),cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[...,1]=np.clip(hsv[...,1]*1.12,0,255)
    out=cv2.cvtColor(hsv.astype(np.uint8),cv2.COLOR_HSV2BGR)
    return cv2.detailEnhance(out,sigma_s=6,sigma_r=0.08) if False else out
def wrap(d,t,fo,mw):
    out=[];cur=''
    for w in t.split():
        x=(cur+' '+w).strip()
        if d.textlength(x,font=fo)<=mw: cur=x
        else: out.append(cur); cur=w
    return out+[cur]
def overlay(kicker,title):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    # degradê inferior
    grad=np.zeros((H,W,4),np.uint8); y0=int(H*0.55)
    a=np.clip((np.arange(H)-y0)/(H-y0),0,1)**1.3*200
    grad[...,3]=a[:,None].astype(np.uint8); grad[...,:3]=NAVY
    im=Image.alpha_composite(im,Image.fromarray(grad)); d=ImageDraw.Draw(im)
    ft=font(F8,74); lines=wrap(d,title,ft,W-140)
    y=H-260-len(lines)*88
    if kicker:
        fk=font(F7,34); tw=d.textlength(kicker,font=fk)
        d.rounded_rectangle((70,y-70,70+tw+40,y-18),26,fill=ACC+(255,)); d.text((90,y-64),kicker,font=fk,fill=(255,255,255,255))
    for l in lines: d.text((70,y),l,font=ft,fill=(255,255,255,255)); y+=88
    return np.array(im)
def card(lines):
    im=Image.new('RGB',(W,H),NAVY); d=ImageDraw.Draw(im); y=600
    for txt,fp,sz,col,gap in lines:
        fo=font(fp,sz)
        for l in wrap(d,txt,fo,W-160):
            d.text(((W-d.textlength(l,font=fo))/2,y),l,font=fo,fill=col); y+=int(sz*1.25)
        y+=gap
    fo=font(F7,30); t='Vídeo: Vídeo Imóvel'; d.text(((W-d.textlength(t,font=fo))/2,H-150),t,font=fo,fill=(167,176,192))
    return cv2.cvtColor(np.array(im),cv2.COLOR_RGB2BGR)
def frames_for(img,dur,motion):
    h,w=img.shape[:2]; n=int(dur*FPS)
    s=max(W/w,H/h)
    for i in range(n):
        t=i/max(n-1,1); t=t*t*(3-2*t)
        if motion=='in': z=1.0+0.10*t; cx=0.5; cy=0.5
        elif motion=='out': z=1.10-0.10*t; cx=0.5; cy=0.5
        elif motion=='lr': z=1.02; cx=t; cy=0.5
        elif motion=='rl': z=1.02; cx=1-t; cy=0.5
        else: z=1.0; cx=cy=0.5
        sc=s*z; vw,vh=W/sc,H/sc
        x0=(w-vw)*cx; y0=(h-vh)*cy
        Mx=np.float32([[sc,0,-x0*sc],[0,sc,-y0*sc]])
        yield cv2.warpAffine(img,Mx,(W,H),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT)
def render(name,scenes,final,fin_dur=4.0,xf=0.4):
    p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
        '-f','lavfi','-i','anullsrc=r=48000:cl=stereo','-shortest','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-movflags','+faststart',O+name+'.mp4'],stdin=subprocess.PIPE)
    prev_tail=None
    clips=[]
    for (f,dur,mot,kick,title) in scenes:
        img=treat(M+f); ov=overlay(kick,title); a=ov[...,3:4].astype(np.float32)/255; rgb=cv2.cvtColor(ov[...,:3],cv2.COLOR_RGB2BGR).astype(np.float32)
        fr=[]
        for k,frm in enumerate(frames_for(img,dur+xf,mot)):
            ta=min(1,max(0,(k/FPS-0.25)/0.35))
            fr.append((frm*(1-a*ta)+rgb*a*ta).astype(np.uint8))
        clips.append(fr)
    c=card(final); clips.append([c]*int((fin_dur+xf)*FPS))
    nx=int(xf*FPS); first=True; out=0
    for ci,fr in enumerate(clips):
        if ci>0:
            # crossfade com o final do anterior
            for k in range(nx):
                al=(k+1)/(nx+1); p.stdin.write(cv2.addWeighted(tail[k],1-al,fr[k],al,0).tobytes()); out+=1
            body=fr[nx:]
        else: body=fr
        last=ci==len(clips)-1
        keep=body if last else body[:-nx]
        for frm in keep: p.stdin.write(frm.tobytes()); out+=1
        tail=body[-nx:] if not last else None
    p.stdin.close(); p.wait(); print(name, out/FPS,'s')
    return clips
WHITE=(244,245,248); MUT=(167,176,192); ACCT=ACC
JOBS={
'AP0933':([('AP0933/02.jpg',3.0,'in','AP0933 · ESTAÇÃO PAULISTA','R$ 560 mil · 3 quartos · 2 vagas cobertas'),
  ('AP0933/04.jpg',2.6,'in',None,'Sala para dois ambientes'),
  ('AP0933/01.jpg',2.8,'out',None,'Varanda gourmet planejada'),
  ('AP0933/07.jpg',2.8,'in',None,'Cozinha planejada'),
  ('AP0933/18.jpg',2.6,'in',None,'3 dormitórios com armários, 1 suíte'),
  ('AP0933/26.jpg',3.2,'lr',None,'Piscina adulto e infantil'),
  ('AP0933/31.jpg',2.8,'rl',None,'Quadra, salão de jogos e academia')],
  [('R$ 560.000',F8,96,WHITE,10),('84 m² · 3 dorm. · 1 suíte · 2 vagas',F7,42,WHITE,6),('Condomínio R$ 600',F7,38,MUT,60),
   ('Chame no WhatsApp e agende sua visita',F8,56,ACCT,60),('AP0933 · Imobiliária Menegalli · CRECI 021362J',F7,32,MUT,0)]),
'SO0342':([('SO0342/01.jpg',4.0,'lr','SO0342 · PARK CAMPESTRE','Piscina com raia de 15 m'),
  ('SO0342/15.jpg',3.6,'in',None,'Cozinha integrada ao gourmet, com churrasqueira e forno'),
  ('SO0342/08.jpg',3.6,'lr',None,'Sala para três ambientes'),
  ('SO0342/29.jpg',3.4,'in',None,'5 suítes, 4 com sacada'),
  ('SO0342/53.jpg',3.4,'out',None,'Vista da sacada'),
  ('SO0342/17.jpg',3.8,'rl',None,'1.000 m² de terreno · 504,86 m² construídos')],
  [('R$ 3.380.000',F8,96,WHITE,10),('Sobrado · 5 suítes · estúdio musical',F7,42,WHITE,6),('Aceita financiamento e estuda permuta',F7,38,MUT,60),
   ('Agende sua visita pelo WhatsApp',F8,56,ACCT,60),('SO0342 · Imobiliária Menegalli · CRECI 021362J',F7,32,MUT,0)]),
'CA0438':([('CA0438/01.jpg',3.6,'lr','CA0438 · CENTRO','1.558,50 m² na Avenida Independência'),
  ('CA0438/02.jpg',3.2,'rl',None,'Perto do Teatro Municipal'),
  ('CA0438/03.jpg',3.2,'lr',None,'420 m² construídos'),
  ('CA0438/05.jpg',3.2,'rl',None,'Ampla área livre para estacionamento'),
  ('CA0438/06.jpg',3.2,'lr',None,'Terreno de cerca de 27 x 56 m')],
  [('R$ 4.100.000',F8,96,WHITE,10),('Casa comercial · Centro de Piracicaba',F7,42,WHITE,60),
   ('Fale com a Menegalli pelo WhatsApp',F8,56,ACCT,60),('CA0438 · Imobiliária Menegalli · CRECI 021362J',F7,32,MUT,0)]),
}
if __name__=='__main__':
    for k in sys.argv[1:]: render(k,*JOBS[k])
