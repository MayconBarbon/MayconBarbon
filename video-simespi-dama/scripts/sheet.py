import sys,subprocess,os,tempfile
from PIL import Image,ImageDraw
src,step,out=sys.argv[1],float(sys.argv[2]),sys.argv[3]
tw=int(sys.argv[4]) if len(sys.argv)>4 else 192
td=tempfile.mkdtemp()
subprocess.run(['ffmpeg','-v','error','-i',src,'-vf',f'fps=1/{step},scale={tw}:-2',f'{td}/%04d.jpg'])
fs=sorted(os.listdir(td)); ims=[Image.open(f'{td}/{f}') for f in fs]
w,h=ims[0].size; cols=10; rows=(len(ims)+cols-1)//cols
sh=Image.new('RGB',(w*cols,h*rows),'white'); d=ImageDraw.Draw(sh)
for k,im in enumerate(ims):
    x,y=(k%cols)*w,(k//cols)*h; sh.paste(im,(x,y)); t=k*step+step/2
    d.rectangle((x,y,x+34,y+12),fill='black'); d.text((x+1,y+1),f'{t:.0f}',fill='yellow')
sh.save(out,quality=75)
