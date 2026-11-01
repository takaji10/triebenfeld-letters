# Draw the OCR'd numbers on a downscaled mosaic: red ink red, black ink
# dark; matched-to-table tokens boxed in green, unmatched boxed grey.
# Output: C:\Users\Tersnaus\AppData\Local\Temp\opencode\p1896_overlay.jpg
import json
import numpy as np
import pyvips
import PIL.Image
import PIL.ImageDraw

FULL = r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456\4456_full.jpg"
OUT = r"C:\Users\Tersnaus\AppData\Local\Temp\opencode\p1896_overlay.jpg"
OUT_BIG = r"C:\Users\Tersnaus\AppData\Local\Temp\opencode\p1896_overlay_full.jpg"

TOK = json.load(open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\numbers_easy2.json", encoding="utf-8"))
try:
    MAT = json.load(open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\numbers_hits.json", encoding="utf-8"))
    matched_keys = {(m["kind"], m["x"], m["y"]) for m in MAT}
except FileNotFoundError:
    matched_keys = set()

im = pyvips.Image.new_from_file(FULL, access="random")
SC = 3000 / im.width
small = im.resize(SC)
base = PIL.Image.fromarray(
    np.frombuffer(small.write_to_memory(), np.uint8).reshape(
        small.height, small.width, 3))
dr = PIL.ImageDraw.Draw(base)
n_match = n_un = 0
for t in TOK:
    x0, y0 = t["x"] * SC, t["y"] * SC
    x1, y1 = (t["x"] + t["w"]) * SC, (t["y"] + t["h"]) * SC
    ink = (255, 60, 60) if t["kind"] == "red" else (30, 30, 30)
    hit = (t["kind"], t["x"], t["y"]) in matched_keys
    box = (60, 200, 90) if hit else (150, 150, 150)
    if hit:
        n_match += 1
    else:
        n_un += 1
    dr.rectangle([x0 - 2, y0 - 2, x1 + 2, y1 + 2], outline=box, width=2)
base.save(OUT, quality=90)
print("overlay saved; matched", n_match, "unmatched", n_un, "of", len(TOK))
