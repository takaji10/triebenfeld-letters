# The numbers on Pelzucki 1896, the EasyOCR pass: tile the mosaic, read every
# digit group with EasyOCR (colour crop), classify each hit's ink by the
# mean redness inside its box, and save all tokens with mosaic positions.
# Output: scratch/map4456/numbers_easy.json + .csv
import csv
import json
import numpy as np
import pyvips
import easyocr

FULL = r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456\4456_full.jpg"
OUT_JSON = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\numbers_easy.json"
OUT_CSV = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\numbers_easy.csv"

TILE = 2048
OV = 256
STEP = TILE - OV

im = pyvips.Image.new_from_file(FULL, access="random")
W, H = im.width, im.height
print("mosaic", W, H, flush=True)

reader = easyocr.Reader(["en"], gpu=False,
                        model_storage_directory=r"C:\Users\Tersnaus\AppData\Local\Temp\opencode\easymodels",
                        user_network_directory=r"C:\Users\Tersnaus\AppData\Local\Temp\opencode\easynets",
                        verbose=False)

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
        redness = np.clip(R - np.maximum(G, B), 0, 255)
        try:
            res = reader.readtext(a, allowlist="0123456789/.,-",
                                  text_threshold=0.4, low_text=0.25,
                                  link_threshold=0.2)
        except Exception as e:
            print("read fail", ox, oy, e, flush=True)
            continue
        for box, txt, conf in res:
            xs = [p[0] for p in box]; ys = [p[1] for p in box]
            x0, x1 = int(min(xs)), int(max(xs))
            y0, y1 = int(min(ys)), int(max(ys))
            t = txt.strip()
            core = t.replace("/", "").replace(".", "").replace(",", "").replace("-", "").replace(" ", "")
            if not core or not core.isdigit():
                continue
            m = redness[max(0, y0):y1, max(0, x0):x1]
            kind = "red" if m.mean() > 12 else "black"
            found.append({"text": t, "conf": round(float(conf), 3), "kind": kind,
                          "x": ox + x0, "y": oy + y0, "w": x1 - x0, "h": y1 - y0})
    print("row", ty, "of", ny - 1, "tokens", len(found), flush=True)

with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(found, f)
with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
    wr = csv.DictWriter(f, fieldnames=["text", "conf", "kind", "x", "y", "w", "h"])
    wr.writeheader()
    wr.writerows(found)
print("tokens", len(found))
