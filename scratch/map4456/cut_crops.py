# Cut verification crops of the matched numbers (for the editor's eyes):
# a square patch around each given mosaic position, named by token and ink.
# Usage: python cut_crops.py <matched.json> [max]
import sys
import json
import os
import pyvips

FULL = r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456\4456_full.jpg"
OUTD = r"C:\Users\Tersnaus\AppData\Local\Temp\opencode\p1896_crops"
os.makedirs(OUTD, exist_ok=True)

src = sys.argv[1] if len(sys.argv) > 1 else \
    r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\numbers_matched.json"
maxn = int(sys.argv[2]) if len(sys.argv) > 2 else 30

items = json.load(open(src, encoding="utf-8"))
im = pyvips.Image.new_from_file(FULL, access="random")
W, H = im.width, im.height

def cut(i, it):
    cx, cy = it["x"] + it["w"] // 2, it["y"] + it["h"] // 2
    r = 220
    l = max(0, cx - r); t = max(0, cy - r)
    w = min(2 * r, W - l); h = min(2 * r, H - t)
    name = "%s_%s_%s_c%02d_%d_%d.jpg" % (it["kind"], it["text"].replace("/", "_").replace(".", ""),
                                         str(it["conf"]).replace(".", ""), i, cx, cy)
    im.crop(l, t, w, h).resize(440 / w).write_to_file(os.path.join(OUTD, name) + "[Q=90]")

for i, it in enumerate(items[:maxn]):
    cut(i, it)
print("crops of", min(maxn, len(items)), "of", len(items), "in", OUTD)
