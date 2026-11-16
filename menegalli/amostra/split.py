import cv2, numpy as np, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
from render import treat
S='/tmp/claude-0/-home-user-MayconBarbon/23adc415-3614-5acc-b755-85d3f8a0a095/scratchpad'; M=S+'/men/'; O=S+'/menv/'
IF='/usr/share/fonts/opentype/inter/'
BLACK=IF+'InterDisplay-Black.otf'; SEMI=IF+'Inter-SemiBold.otf'; BOLD=IF+'Inter-Bold.otf'
W,H,FPS=1080,1920,30; GAP=8
ACC=(110,150,225); MBLUE=(69,88,118); WHITE=(255,255,255)
_c={}
def img(f):
    if f not in _c: _c[f]=treat(M+f)
    return _c[f]
def ease(t): t=min(max(t,0),1); return 1-(1-t)**3
def cover(im,w,h,t,mode):
    ih,iw=im.shape[:2]; s=max(w/iw,h/ih)*(1.06 if mode!='none' else 1.0)
    z={'in':1+0.06*t,'out':1.06-0.06*t}.get(mode,1.0); s*=z
    vw,vh=w/s,h/s
    cx={'lr':t,'rl':1-t}.get(mode,0.5)
    x0=(iw-vw)*cx; y0=(ih-vh)*0.5
    Mx=np.float32([[s,0,-x0*s],[0,s,-y0*s]])
    return cv2.warpAffine(im,Mx,(w,h),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
def bg(f,t,mode):
    if isinstance(f,str): return cover(img(f),W,H,t,mode).astype(np.float32)
    k=len(f); ph=(H-GAP*(k-1))//k; fr=np.full((H,W,3),255,np.float32)
    for j,ff in enumerate(f):
        m=mode if j%2==0 else {'lr':'rl','rl':'lr'}.get(mode,mode)
        fr[j*(ph+GAP):j*(ph+GAP)+ph]=cover(img(ff),W,ph,t,m)
    return fr
def F(p,s): return ImageFont.truetype(p,s)
def spaced(d,xy,txt,fo,fill,sp=6):
    x,y=xy
    for ch in txt: d.text((x,y),ch,font=fo,fill=fill); x+=d.textlength(ch,font=fo)+sp
    return x
def label_layer(w,h,lab):
    im=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(im)
    g=np.zeros((h,w,4),np.uint8); a=np.clip((np.arange(h)-h*0.55)/(h*0.45),0,1)*150; g[...,3]=a[:,None]
    im=Image.alpha_composite(im,Image.fromarray(g)); d=ImageDraw.Draw(im)
    fo=F(SEMI,30); d.rectangle((36,h-86,66,h-81),fill=ACC+(255,)); spaced(d,(36,h-70),lab.upper(),fo,WHITE+(255,),5)
    return np.array(im)
def big_layer(lines,size=118,y=None,align='left',shade=True):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); fo=F(BLACK,size); lh=int(size*1.0)
    y=y if y is not None else int(H*0.5-len(lines)*lh/2)
    if shade:
        g=np.zeros((H,W,4),np.uint8); g[...,3]=95; im=Image.alpha_composite(im,Image.fromarray(g)); d=ImageDraw.Draw(im)
    for l in lines:
        body=l.rstrip('.?,'); punct=l[len(body):]
        tw=d.textlength(l,font=fo); x=70 if align=='left' else (W-tw)/2
        d.text((x,y),body,font=fo,fill=WHITE+(255,)); d.text((x+d.textlength(body,font=fo),y),punct,font=fo,fill=ACC+(255,)); y+=lh
    return np.array(im)
def num_layer(num,lab):
    im=Image.new('RGBA',(W,H),(0,0,0,0))
    g=np.zeros((H,W,4),np.uint8); g[...,3]=110; im=Image.alpha_composite(im,Image.fromarray(g)); d=ImageDraw.Draw(im)
    fo=F(BLACK,200); y=int(H*0.40)
    x=70
    if num.startswith('+'): d.text((x,y),'+',font=fo,fill=ACC+(255,)); x+=d.textlength('+',font=fo); num=num[1:]
    d.text((x,y),num,font=fo,fill=WHITE+(255,))
    fo2=F(SEMI,36); yy=y+230
    for l in lab.split('\n'): spaced(d,(76,yy),l.upper(),fo2,WHITE+(255,),5); yy+=52
    return np.array(im)
def blend(base,layer,alpha=1.0,dy=0):
    if dy: layer=np.roll(layer,int(dy),axis=0)
    a=layer[...,3:4].astype(np.float32)/255*alpha; rgb=layer[...,2::-1].astype(np.float32)
    return (base*(1-a)+rgb*a)
def end_card(code,lines):
    im=Image.new('RGB',(W,H),(245,245,245)); d=ImageDraw.Draw(im)
    lg=Image.open(M+'logo_men.jpeg').convert('RGB'); lg=lg.resize((860,int(860*lg.height/lg.width)),Image.LANCZOS)
    im.paste(lg,((W-860)//2,640)); y=900
    fo=F(BLACK,64); t=code; d.text(((W-d.textlength(t,font=fo))/2,y),t,font=fo,fill=MBLUE); y+=110
    for txt,sz,col in lines:
        fo=F(BOLD,sz); d.text(((W-d.textlength(txt,font=fo))/2,y),txt,font=fo,fill=col); y+=int(sz*1.5)
    fo=F(SEMI,28); t='Vídeo: Vídeo Imóvel'; d.text(((W-d.textlength(t,font=fo))/2,H-140),t,font=fo,fill=(150,150,150))
    return cv2.cvtColor(np.array(im),cv2.COLOR_RGB2BGR).astype(np.float32)
def shot_frames(sh):
    kind=sh[0]; dur=sh[1]; n=int(round(dur*FPS)); out=[]
    if kind=='full':
        _,_,f,mode,lines=sh[:5]; size=sh[5] if len(sh)>5 else 110
        lay=big_layer(lines,size) if lines else None
        for i in range(n):
            t=i/max(n-1,1); fr=bg(f,t,mode)
            if lay is not None: fr=blend(fr,lay,ease(i/(0.3*FPS)),dy=40*(1-ease(i/(0.3*FPS))))
            out.append(fr)
    elif kind=='num':
        _,_,f,mode,num,lab=sh; lay=num_layer(num,lab)
        for i in range(n):
            t=i/max(n-1,1); fr=bg(f,t,mode)
            out.append(blend(fr,lay,ease(i/(0.25*FPS)),dy=60*(1-ease(i/(0.3*FPS)))))
    elif kind=='split':
        _,_,panels=sh; k=len(panels); ph=(H-GAP*(k-1))//k
        labs=[label_layer(W,ph,p[2]) if p[2] else None for p in panels]
        for i in range(n):
            t=i/max(n-1,1); fr=np.full((H,W,3),255,np.float32)
            for j,(f,mode,lab) in enumerate(panels):
                pt=cover(img(f),W,ph,t,mode).astype(np.float32)
                if labs[j] is not None: pt=blend(pt,labs[j],ease((i-4-3*j)/(0.25*FPS)))
                # entrada: painel desliza alternando lados
                e=ease((i-3*j)/(0.35*FPS)); off=int((1-e)*W*(1 if j%2==0 else -1))
                y0=j*(ph+GAP); row=np.full((ph,W,3),255,np.float32)
                if off>=0: row[:,off:]=pt[:,:W-off]
                else: row[:,:W+off]=pt[:,-off:]
                fr[y0:y0+ph]=row
            out.append(fr)
    elif kind=='end':
        _,_,code,lines=sh; c=end_card(code,lines)
        for i in range(n): out.append(c)
    return out
def whip(a,b,n=6):
    res=[]
    for k in range(n):
        p=(k+1)/(n+1); off=int(ease(p)*W)
        fr=np.zeros_like(a); fr[:,:W-off]=a[:,off:]; fr[:,W-off:]=b[:,:off]
        kb=int(90*np.sin(np.pi*p))+1
        res.append(cv2.blur(fr,(kb,1)))
    return res
def render(name,shots):
    p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
        '-f','lavfi','-i','anullsrc=r=48000:cl=stereo','-shortest','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-movflags','+faststart',O+name+'_split.mp4'],stdin=subprocess.PIPE)
    prev=None; tot=0
    for sh in shots:
        fr=shot_frames(sh)
        if prev is not None and sh[0]!='split' and shots.index(sh)>0:
            for w_ in whip(prev,fr[0]): p.stdin.write(np.clip(w_,0,255).astype(np.uint8).tobytes()); tot+=1
        for f in fr: p.stdin.write(np.clip(f,0,255).astype(np.uint8).tobytes()); tot+=1
        prev=fr[-1]
    p.stdin.close(); p.wait(); print(name,round(tot/FPS,1),'s')
