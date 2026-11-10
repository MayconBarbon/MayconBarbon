import sys,subprocess,tempfile,os
from PIL import Image,ImageDraw
# args: out  then list of src:t0:t1
out=sys.argv[1]; rows=[]
for spec in sys.argv[2:]:
    src,t0,t1=spec.split(':'); t0=float(t0); t1=float(t1)
    n=6; ts=[t0+(t1-t0)*i/(n-1) for i in range(n)]
    ims=[]
    for t in ts:
        p=tempfile.mktemp(suffix='.jpg')
        subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',src,'-frames:v','1','-vf','scale=320:-2',p])
        ims.append((t,Image.open(p)))
    rows.append((src,ims))
W=320; H=max(im.height for _,ims in rows for _,im in ims)
sh=Image.new('RGB',(W*6,H*len(rows)),'white'); d=ImageDraw.Draw(sh)
for r,(src,ims) in enumerate(rows):
    for c,(t,im) in enumerate(ims):
        sh.paste(im,(c*W,r*H)); d.rectangle((c*W,r*H,c*W+120,r*H+12),fill='black'); d.text((c*W+2,r*H+1),f'{os.path.basename(src)[:10]} {t:.1f}',fill='yellow')
sh.save(out,quality=80)
