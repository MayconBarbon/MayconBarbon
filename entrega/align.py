"""Align AI-relit keyframes (golden/night) to the original day photo, pixel-exact.
usage: python3 align.py <day.jpg> <in.jpg> <out.jpg>"""
import sys, cv2, numpy as np

day = cv2.imread(sys.argv[1])
src = cv2.imread(sys.argv[2])
h, w = day.shape[:2]
src = cv2.resize(src, (w, h), interpolation=cv2.INTER_LANCZOS4)


def edges(im):
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32)
    g = cv2.GaussianBlur(g, (0, 0), 2)
    gx = cv2.Sobel(g, cv2.CV_32F, 1, 0); gy = cv2.Sobel(g, cv2.CV_32F, 0, 1)
    m = np.sqrt(gx * gx + gy * gy)
    return m / (m.max() + 1e-6)

# work on downscaled gradient images (lighting-invariant)
sc = 0.25
a = cv2.resize(edges(day), None, fx=sc, fy=sc)
b = cv2.resize(edges(src), None, fx=sc, fy=sc)
warp = np.eye(2, 3, dtype=np.float32)
try:
    cc, warp = cv2.findTransformECC(a, b, warp, cv2.MOTION_AFFINE,
                                    (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 300, 1e-6), None, 5)
except cv2.error as e:
    cc = -1
warp[:, 2] /= sc
print('ecc', cc, warp.tolist())
out = cv2.warpAffine(src, warp, (w, h), flags=cv2.INTER_LANCZOS4 + cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REFLECT)
cv2.imwrite(sys.argv[3], out, [cv2.IMWRITE_JPEG_QUALITY, 95])
