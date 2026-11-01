# The numbers on Pelzucki 1896, take three: cheap candidate detection by
# connected components over the whole mosaic (red and dark ink, long map
# strokes stripped), then EasyOCR recognition on each candidate's colour
# crop only. Output: scratch/map4456/numbers_easy2.json + .csv
import csv
import json
import numpy as np
import pyvips
import easyocr
from scipy import ndimage

FULL = r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456\4456_full.jpg"
OUT_JSON = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\numbers_easy2.json"
OUT_CSV = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\numbers_easy2.csv"

TILE = 2048
OV = 384
STEP = TILE - OV
DIGIT_H = (14, 100)
DIGIT_W = (5, 110)
MIN_AREA = 30

im = pyvips.Image.new_from_file(FULL, access="random")
W, H = im.width, im.height
print("mosaic", W, H, flush=True)

def strip_long(mask, k=41):
    hor = ndimage.binary_erosion(mask, structure=np.ones((1, k), bool))
    hor = ndimage.binary_dilation(hor, structure=np.ones((1, k), bool))
    ver = ndimage.binary_erosion(mask, structure=np.ones((k, 1), bool))
    ver = ndimage.binary_dilation(ver, structure=np.ones((k, 1), bool))
    return mask & ~hor & ~ver

def digit_boxes(mask):
    lab, n = ndimage.label(mask)
    if n == 0:
        return []
    objs = ndimage.find_objects(lab)
    out = []
    for i, s in enumerate(objs):
        if s is None:
            continue
        h = s[0].stop - s[0].start
        w = s[1].stop - s[1].start
        if not (DIGIT_H[0] <= h <= DIGIT_H[1] and DIGIT_W[0] <= w <= DIGIT_W[1]):
            continue
        if int((lab[s] == i + 1).sum()) < MIN_AREA:
            continue
        out.append((s[1].start, s[0].start, s[1].stop, s[0].stop))
    return out

def group(boxes, gapx=26, gapy=12):
    n = len(boxes)
    parent = list(range(n))
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    for i in range(n):
        ax0, ay0, ax1, ay1 = boxes[i]
        for j in range(i + 1, n):
            bx0, by0, bx1, by1 = boxes[j]
            gx = max(bx0 - ax1, ax0 - bx1)
            gy = max(by0 - ay1, ay0 - by1)
            hi, hj = ay1 - ay0, by1 - by0
            if gx <= gapx and gy <= gapy and 0.4 <= hi / hj <= 2.5:
                pi, pj = find(i), find(j)
                if pi != pj:
                    parent[pi] = pj
    gs = {}
    for i in range(n):
        gs.setdefault(find(i), []).append(boxes[i])
    return [(min(b[0] for b in g), min(b[1] for b in g),
             max(b[2] for b in g), max(b[3] for b in g)) for g in gs.values()]

# ---- pass 1: candidates ---------------------------------------------------
cands = []  # (kind, x0, y0, x1, y1)
ny = (H - OV) // STEP + 1
nx = (W - OV) // STEP + 1
for ty in range(ny):
    for tx in range(nx):
        ox, oy = tx * STEP, ty * STEP
        tw, th = min(TILE, W - ox), min(TILE, H - oy)
        a = np.frombuffer(im.crop(ox, oy, tw, th).write_to_memory(),
                          np.uint8).reshape(th, tw, 3)
        R = a[:, :, 0].astype(int); G = a[:, :, 1].astype(int); B = a[:, :, 2].astype(int)
        lum = (R * 299 + G * 587 + B * 114) // 1000
        red = (R > 100) & (R - G > 40) & (R - B > 40)
        dark = (lum < 135) & (R - G < 30) & (R - B < 30)
        for kind, mask in (("red", red), ("black", dark)):
            m2 = strip_long(mask)
            bs = digit_boxes(m2)
            if not bs:
                continue
            for x0, y0, x1, y1 in group(bs):
                w, h = x1 - x0, y1 - y0
                if w > 360 or h > 120 or (w * h) < 200:
                    continue
                cands.append((kind, ox + x0, oy + y0, ox + x1, oy + y1))
    print("detect row", ty, "of", ny - 1, "cands", len(cands), flush=True)

# dedupe overlapping candidates (tile overlaps, same cluster seen twice)
cands.sort(key=lambda c: (c[3] - c[1]) * (c[4] - c[2]), reverse=True)
kept = []
for c in cands:
    k, x0, y0, x1, y1 = c
    dup = False
    for k2, a0, b0, a1, b1 in kept:
        if k2 != k:
            continue
        ix = max(0, min(x1, a1) - max(x0, a0))
        iy = max(0, min(y1, b1) - max(y0, b0))
        inter = ix * iy
        area = (x1 - x0) * (y1 - y0)
        a2 = (a1 - a0) * (b1 - b0)
        if inter > 0.45 * min(area, a2):
            dup = True
            break
    if not dup:
        kept.append(c)
print("candidates after dedupe:", len(kept), flush=True)

# ---- pass 2: recognition ---------------------------------------------------
reader = easyocr.Reader(["en"], gpu=False,
                        model_storage_directory=r"C:\Users\Tersnaus\AppData\Local\Temp\opencode\easymodels",
                        user_network_directory=r"C:\Users\Tersnaus\AppData\Local\Temp\opencode\easynets",
                        verbose=False)
PAD = 10
found = []
for i, (kind, x0, y0, x1, y1) in enumerate(kept):
    l = max(0, x0 - PAD); t = max(0, y0 - PAD)
    r = min(W, x1 + PAD); b = min(H, y1 + PAD)
    crop = np.frombuffer(im.crop(l, t, r - l, b - t).write_to_memory(),
                         np.uint8).reshape(b - t, r - l, 3)
    try:
        res = reader.readtext(crop, allowlist="0123456789/.,-",
                              text_threshold=0.4, low_text=0.3, link_threshold=0.2)
    except Exception as e:
        continue
    R = crop[:, :, 0].astype(int); G = crop[:, :, 1].astype(int); B = crop[:, :, 2].astype(int)
    redness = np.clip(R - np.maximum(G, B), 0, 255)
    for box, txt, conf in res:
        xs = [p[0] for p in box]; ys = [p[1] for p in box]
        bx0, bx1 = int(min(xs)), int(max(xs))
        by0, by1 = int(min(ys)), int(max(ys))
        core = txt.strip()
        for ch in "/.,- ":
            core = core.replace(ch, "")
        if not core or not core.isdigit():
            continue
        m = redness[max(0, by0):by1, max(0, bx0):bx1]
        ink = "red" if (m.size and m.mean() > 12) else kind
        found.append({"text": txt.strip(), "conf": round(float(conf), 3), "kind": ink,
                      "x": l + bx0, "y": t + by0, "w": bx1 - bx0, "h": by1 - by0})
    if i % 500 == 0:
        print("recognise", i, "of", len(kept), "tokens", len(found), flush=True)

with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(found, f)
with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
    wr = csv.DictWriter(f, fieldnames=["text", "conf", "kind", "x", "y", "w", "h"])
    wr.writeheader()
    wr.writerows(found)
print("tokens", len(found))
