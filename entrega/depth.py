"""Estimate a disparity map (near = 1, far = 0) for each photo with Depth Anything V2.
usage: python3 depth.py <scratch> <name> [<name> ...]   (name = IMG_xxxx or gen/day_al)"""
import sys, os, numpy as np, cv2, torch
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForDepthEstimation

S = sys.argv[1]
torch.set_num_threads(4)
mid = "depth-anything/Depth-Anything-V2-Base-hf"
proc = AutoImageProcessor.from_pretrained(mid)
model = AutoModelForDepthEstimation.from_pretrained(mid).eval()
os.makedirs(S + "/depth", exist_ok=True)
for name in sys.argv[2:]:
    p = f"{S}/img/{name}.jpg" if name.startswith("IMG") else f"{S}/{name}.jpg"
    im = Image.open(p).convert("RGB")
    w, h = im.size
    small = im.resize((1036, int(1036 * h / w) // 14 * 14))
    with torch.no_grad():
        inp = proc(images=small, return_tensors="pt", do_resize=False)
        out = model(**inp).predicted_depth[0].numpy()
    d = cv2.resize(out, (w, h), interpolation=cv2.INTER_CUBIC)
    lo, hi = np.percentile(d, 1), np.percentile(d, 99.5)
    d = np.clip((d - lo) / (hi - lo + 1e-6), 0, 1)
    # edge-preserving smoothing so walls stay planar
    d = cv2.bilateralFilter(d.astype(np.float32), 9, 0.08, 9)
    np.save(f"{S}/depth/{os.path.basename(name)}.npy", d.astype(np.float16))
    cv2.imwrite(f"{S}/depth/{os.path.basename(name)}.png", (d * 255).astype(np.uint8))
    print(name, d.shape, flush=True)
