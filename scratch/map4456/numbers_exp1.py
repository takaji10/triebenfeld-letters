# Experiments on one red cluster: how to make the numbers readable for
# tesseract. Patch around x 12960-13680, y 3744-4464 (red cluster).
import numpy as np
import pyvips
import PIL.Image
import pytesseract
from scipy import ndimage

FULL = r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456\4456_full.jpg"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

X0, Y0, X1, Y1 = 12700, 3500, 14100, 4700
im = pyvips.Image.new_from_file(FULL, access="random")
a = np.frombuffer(im.crop(X0, Y0, X1 - X0, Y1 - Y0).write_to_memory(),
                  np.uint8).reshape(Y1 - Y0, X1 - X0, 3)
R = a[:, :, 0].astype(int); G = a[:, :, 1].astype(int); B = a[:, :, 2].astype(int)
lum = (R * 299 + G * 587 + B * 114) // 1000
red = (R > 100) & (R - G > 40) & (R - B > 40)

# remove long strokes: erosion with long 1xk / kx1, then dilate back
def strip_long(mask, k=41):
    hor = ndimage.binary_erosion(mask, structure=np.ones((1, k), bool))
    hor = ndimage.binary_dilation(hor, structure=np.ones((1, k), bool))
    ver = ndimage.binary_erosion(mask, structure=np.ones((k, 1), bool))
    ver = ndimage.binary_dilation(ver, structure=np.ones((k, 1), bool))
    return mask & ~hor & ~ver

red2 = strip_long(red)
print("red px", red.sum(), "->", red2.sum())

lab, n = ndimage.label(red2)
print("components", n)
objs = ndimage.find_objects(lab)
boxes = []
for i, s in enumerate(objs):
    if s is None:
        continue
    h = s[0].stop - s[0].start; w = s[1].stop - s[1].start
    area = int((lab[s] == i + 1).sum())
    if 14 <= h <= 90 and 5 <= w <= 100 and area >= 30:
        boxes.append((s[1].start, s[0].start, s[1].stop, s[0].stop, area))
boxes.sort(key=lambda b: (b[1] // 40, b[0]))
print("digit-like blobs", len(boxes))

# group close blobs into tokens
def group(bs, gapx=24, gapy=10):
    n = len(bs); parent = list(range(n))
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]; i = parent[i]
        return i
    for i in range(n):
        for j in range(i + 1, n):
            ax0, ay0, ax1, ay1, _ = bs[i]; bx0, by0, bx1, by1, _ = bs[j]
            gapx_ = max(bx0 - ax1, ax0 - bx1); gapy_ = max(by0 - ay1, ay0 - by1)
            hi, hj = ay1 - ay0, by1 - by0
            if gapx_ <= gapx and gapy_ <= gapy and 0.45 <= hi / hj <= 2.2:
                pi, pj = find(i), find(j)
                if pi != pj: parent[pi] = pj
    gs = {}
    for i in range(n): gs.setdefault(find(i), []).append(bs[i])
    out = []
    for g in gs.values():
        out.append((min(b[0] for b in g), min(b[1] for b in g),
                    max(b[2] for b in g), max(b[3] for b in g), len(g)))
    return out

toks = group(boxes)
print("tokens", len(toks))
for t in toks:
    x0, y0, x1, y1, nb = t
    w, h = x1 - x0, y1 - y0
    pad = 8
    crop = np.full((h + 2 * pad, w + 2 * pad), 255, np.uint8)
    sub = red2[max(0, y0 - pad):y1 + pad, max(0, x0 - pad):x1 + pad]
    crop[:sub.shape[0], :sub.shape[1]] = np.where(sub, 0, 255)
    pil = PIL.Image.fromarray(np.stack([crop] * 3, -1))
    sc = max(1, int(70 / h))
    if sc > 1:
        pil = pil.resize((pil.width * sc, pil.height * sc), PIL.Image.LANCZOS)
    for psm in (7, 8, 6):
        txt = pytesseract.image_to_string(
            pil, config=f"--psm {psm} -c tessedit_char_whitelist=0123456789/.,-").strip()
        if txt:
            print("  tok", (X0 + x0, Y0 + y0), "size", (w, h), "blobs", nb, "psm", psm, "->", repr(txt))
            break
