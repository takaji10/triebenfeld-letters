# The numbers on Pelzucki 1896: tile the mosaic, isolate red and black ink,
# OCR digits with tesseract, and collect every numeric token with its mosaic
# position. Output: scratch/map4456/numbers_ocr.json + .csv
import csv
import json
import numpy as np
import pyvips
import PIL.Image
import io
import pytesseract

FULL = r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456\4456_full.jpg"
OUT_JSON = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\numbers_ocr.json"
OUT_CSV = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\numbers_ocr.csv"
TESS = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = TESS

TILE = 2048
OV = 256
STEP = TILE - OV

im = pyvips.Image.new_from_file(FULL, access="random")
W, H = im.width, im.height
print("mosaic", W, H)

CFG = "--psm 11 -c tessedit_char_whitelist=0123456789/.,-"

def ocr_tile(a, ox, oy):
    """a: HxWx3 uint8 tile. Returns list of tokens (mosaic coords)."""
    R = a[:, :, 0].astype(int)
    G = a[:, :, 1].astype(int)
    B = a[:, :, 2].astype(int)
    lum = (R * 299 + G * 587 + B * 114) // 1000
    red = (R > 110) & (R - G > 45) & (R - B > 45)
    dark = (lum < 135) & (R - G < 30) & (R - B < 30)
    toks = []
    for kind, mask in (("red", red), ("black", dark)):
        if mask.sum() < 30:
            continue
        img = np.where(mask, 0, 255).astype(np.uint8)
        img = np.stack([img] * 3, axis=-1)
        pil = PIL.Image.fromarray(img)
        try:
            data = pytesseract.image_to_data(
                pil, config=CFG, output_type=pytesseract.Output.DICT)
        except Exception as e:
            print("ocr fail", ox, oy, kind, e)
            continue
        for i in range(len(data["text"])):
            t = data["text"][i].strip()
            c = int(data["conf"][i])
            if not t or c < 40:
                continue
            # keep only tokens that are mostly digits with separators
            core = t.replace("/", "").replace(".", "").replace(",", "").replace("-", "")
            if not core or not core.isdigit():
                continue
            nd = sum(ch.isdigit() for ch in t)
            if nd < 1:
                continue
            x = ox + data["left"][i]
            y = oy + data["top"][i]
            w = data["width"][i]
            h = data["height"][i]
            toks.append({"kind": kind, "text": t, "conf": c,
                         "x": int(x), "y": int(y), "w": int(w), "h": int(h)})
    return toks

found = []
ny = (H - OV) // STEP + 1
nx = (W - OV) // STEP + 1
for ty in range(ny):
    for tx in range(nx):
        ox, oy = tx * STEP, ty * STEP
        tw, th = min(TILE, W - ox), min(TILE, H - oy)
        tile = np.frombuffer(
            im.crop(ox, oy, tw, th).write_to_memory(), np.uint8
        ).reshape(th, tw, 3)
        found.extend(ocr_tile(tile, ox, oy))
    print("row", ty, "of", ny - 1, "tokens so far", len(found))

with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(found, f)
with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
    wr = csv.DictWriter(f, fieldnames=["kind", "text", "conf", "x", "y", "w", "h"])
    wr.writeheader()
    wr.writerows(found)
print("tokens", len(found))
