import sys,subprocess,os
from PIL import Image,ImageDraw
src,step,out=sys.argv[1],float(sys.argv[2]),sys.argv[3]
d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',src]))
ts=[];t=0.2
while t<d-0.1: ts.append(t); t+=step
ims=[]
for t in ts:
    p=f'/tmp/claude-0/-home-user-MayconBarbon/acb42350-6b15-5b93-8ea7-60283630e122/scratchpad/strip/_f.jpg'
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',src,'-frames:v','1','-vf','scale=240:-2',p])
    ims.append((t,Image.open(p).copy()))
cols=6; rows=(len(ims)+cols-1)//cols
sh=Image.new('RGB',(240*cols,135*rows),'white'); dr=ImageDraw.Draw(sh)
for k,(t,im) in enumerate(ims):
    x,y=(k%cols)*240,(k//cols)*135; sh.paste(im,(x,y)); dr.rectangle((x,y,x+44,y+14),fill='black'); dr.text((x+2,y+2),f'{t:.1f}',fill='yellow')
sh.save(out,quality=80)
