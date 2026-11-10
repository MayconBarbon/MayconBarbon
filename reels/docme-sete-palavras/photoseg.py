import sys, os
from PIL import Image, ImageOps
# photoseg.py <img> <name> <nframes> <cx0> <cx1> <cy> <zoom0> <zoom1>   (centres as fractions of image)
S="/tmp/claude-0/-home-user-MayconBarbon/14558cd3-e9d2-53c0-bc97-8331b175cad2/scratchpad"
src, name, n = sys.argv[1], sys.argv[2], int(sys.argv[3]); cx0, cx1, cy, z0, z1 = map(float, sys.argv[4:9])
im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
d = f"{S}/work/seg/{name}"; os.makedirs(d, exist_ok=True)
for f in os.listdir(d): os.remove(os.path.join(d, f))
ch_full = min(im.height, im.width * 16 / 9); cw_full = ch_full * 9 / 16
for i in range(n):
    p = i / max(1, n - 1); p = p * p * (3 - 2 * p)
    z = z0 + (z1 - z0) * p; cw, ch = cw_full / z, ch_full / z
    cx = (cx0 + (cx1 - cx0) * p) * im.width; cyy = cy * im.height
    cx = min(max(cx, cw / 2), im.width - cw / 2); cyy = min(max(cyy, ch / 2), im.height - ch / 2)
    im.transform((1080, 1920), Image.EXTENT, (cx - cw / 2, cyy - ch / 2, cx + cw / 2, cyy + ch / 2), Image.BICUBIC).save(f"{d}/{i+1:04d}.jpg", quality=92)
print(name, n, im.size)
