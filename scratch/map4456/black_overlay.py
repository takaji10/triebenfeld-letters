# Overlay of the black farm-number sites on a downscaled mosaic, with the
# supported sites boxed in green and the rest in blue.
import json
import numpy as np
import pyvips
import PIL.Image
import PIL.ImageDraw

FULL = r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456\4456_full.jpg"
OUT = r"C:\Users\Tersnaus\AppData\Local\Temp\opencode\p1896_black_overlay.jpg"

LOC = json.load(open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\farm_locations.json", encoding="utf-8"))
im = pyvips.Image.new_from_file(FULL, access="random")
SC = 3000 / im.width
small = im.resize(SC)
base = PIL.Image.fromarray(
    np.frombuffer(small.write_to_memory(), np.uint8).reshape(small.height, small.width, 3))
dr = PIL.ImageDraw.Draw(base)
n_sup = 0
for o in LOC:
    x0, y0 = o["x"] * SC, o["y"] * SC
    x1, y1 = (o["x"] + 60) * SC, (o["y"] + 40) * SC
    col = (30, 180, 60) if o["status"] == "supported" else (40, 80, 220)
    if o["status"] == "supported":
        n_sup += 1
    dr.rectangle([x0 - 2, y0 - 2, x1 + 2, y1 + 2], outline=col, width=2)
base.save(OUT, quality=90)
print("overlay saved:", len(LOC), "sites,", n_sup, "supported ->", OUT)
