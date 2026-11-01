# The numbers on Pelzucki 1896, take two: connected components instead of
# whole-tile OCR. For every tile, label the ink blobs (red mask, dark mask),
# keep digit-sized ones, group neighbours into clusters, and OCR each
# cluster's crop alone (psm 7). Output: scratch/map4456/numbers_cc.json.
import csv
import json
import numpy as np
import pyvips
import PIL.Image
import pytesseract
from scipy import ndimage

FULL = r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456\4456_full.jpg"
OUT_JSON = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\numbers_cc.json"
OUT_CSV = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\numbers_cc.csv"
TESS = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = TESS

TILE = 2048
OV = 256
STEP = TILE - OV

im = pyvips.Image.new_from_file(FULL, access="random")
W, H = im.width, im.height
print("mosaic", W, H)

DIGIT_H = (16, 95)     # digit blob height, px
DIGIT_W = (6, 110)
MIN_AREA = 40

def blobs(mask):
    """digit-sized connected components -> list of (x0,y0,x1,y1,area)"""
    lab, n = ndimage.label(mask)
    if n == 0:
        return []
    sl = ndimage.find_objects(lab)
    out = []
    for i, s in enumerate(sl):
        if s is None:
            continue
        y0, y1 = s[0].start, s[0].stop
        x0, x1 = s[1].start, s[1].stop
        h, w = y1 - y0, x1 - x0
        if not (DIGIT_H[0] <= h <= DIGIT_H[1]):
            continue
        if not (DIGIT_W[0] <= w <= DIGIT_W[1]):
            continue
        area = int((lab[s] == i + 1).sum())
        if area < MIN_AREA:
            continue
        out.append((x0, y0, x1, y1, area))
    return out

def group(bs):
    """merge blobs whose boxes sit close: one pass of union by proximity"""
    n = len(bs)
    parent = list(range(n))
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    for i in range(n):
        for j in range(i + 1, n):
            ax0, ay0, ax1, ay1, _ = bs[i]
            bx0, by0, bx1, by1, _ = bs[j]
            # close horizontally, overlapping vertically, similar heights
            gapx = max(bx0 - ax1, ax0 - bx1)
            gapy = max(by0 - ay1, ay0 - by1)
            hi, hj = ay1 - ay0, by1 - by0
            if gapx <= 26 and gapy <= 12 and 0.45 <= hi / hj <= 2.2:
                pi, pj = find(i), find(j)
                if pi != pj:
                    parent[pi] = pj
    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(bs[i])
    out = []
    for g in groups.values():
        x0 = min(b[0] for b in g); y0 = min(b[1] for b in g)
        x1 = max(b[2] for b in g); y1 = max(b[3] for b in g)
        out.append((x0, y0, x1, y1, len(g)))
    return out

def ocr_cluster(mask, x0, y0, x1, y1, pad=6):
    h, w = y1 - y0, x1 - x0
    crop = np.full((h + 2 * pad, w + 2 * pad), 255, np.uint8)
    ys, xs = max(0, y0 - pad), max(0, x0 - pad)
    sub = mask[ys:y1 + pad, xs:x1 + pad]
    crop[:sub.shape[0], :sub.shape[1]] = np.where(sub, 0, 255)
    # upscale x2 for tesseract
    pil = PIL.Image.fromarray(np.stack([crop] * 3, -1)).resize(
        (crop.shape[1] * 2, crop.shape[0] * 2), PIL.Image.LANCZOS)
    best = None
    for cfg in ("--psm 7 -c tessedit_char_whitelist=0123456789/.,-",
                "--psm 8 -c tessedit_char_whitelist=0123456789/.,-"):
        d = pytesseract.image_to_data(
            pil, config=cfg, output_type=pytesseract.Output.DICT)
        for i in range(len(d["text"])):
            t = d["text"][i].strip()
            c = int(d["conf"][i])
            if not t or c < 30:
                continue
            core = t.replace("/", "").replace(".", "").replace(",", "").replace("-", "")
            if not core or not core.isdigit():
                continue
            if best is None or c > best[1]:
                best = (t, c, cfg)
    return best

found = []
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
        red = (R > 110) & (R - G > 45) & (R - B > 45)
        dark = (lum < 135) & (R - G < 30) & (R - B < 30)
        for kind, mask in (("red", red), ("black", dark)):
            bs = blobs(mask)
            if not bs:
                continue
            for x0, y0, x1, y1, nb in group(bs):
                if (x1 - x0) > 340 or (y1 - y0) > 110:
                    continue  # too big for a number
                hit = ocr_cluster(mask, x0, y0, x1, y1)
                if hit:
                    found.append({"kind": kind, "text": hit[0], "conf": hit[1],
                                  "x": ox + x0, "y": oy + y0,
                                  "w": x1 - x0, "h": y1 - y0, "blobs": nb})
    print("row", ty, "of", ny - 1, "tokens", len(found), flush=True)

with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(found, f)
with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
    wr = csv.DictWriter(f, fieldnames=["kind", "text", "conf", "x", "y", "w", "h", "blobs"])
    wr.writeheader()
    wr.writerows(found)
print("tokens", len(found))
