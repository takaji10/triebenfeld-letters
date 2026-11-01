# Re-classify every token's ink by its INK pixels, not the box mean: the
# box-mean test classified black labels on red-ochre washes as "red". For
# each token box, ink pixels are the dark/red extremes; the ink is whichever
# dominates. Updates numbers_easy2.json (kind), numbers_black.json (drops
# tokens whose true ink is red), region_tokens.json; then region_reread can
# be re-run on the corrected inks.
import json
import numpy as np
import pyvips

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld"
FULL = (r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)"
        r"\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456\4456_full.jpg")
im = pyvips.Image.new_from_file(FULL, access="random")
W, H = im.width, im.height

def ink_of(x, y, w, h):
    x0 = max(0, x); y0 = max(0, y)
    x1 = min(W, x + w); y1 = min(H, y + h)
    if x1 <= x0 or y1 <= y0:
        return "?"
    a = np.frombuffer(im.crop(x0, y0, x1 - x0, y1 - y0).write_to_memory(),
                      np.uint8).reshape(y1 - y0, x1 - x0, 3).astype(int)
    R = a[:, :, 0]; G = a[:, :, 1]; B = a[:, :, 2]
    lum = (R * 299 + G * 587 + B * 114) // 1000
    redpx = ((R > 95) & (R - G > 35) & (R - B > 35)).sum()
    darkpx = ((lum < 115) & (R - G < 35) & (R - B < 35)).sum()
    if redpx == 0 and darkpx == 0:
        return "?"
    return "red" if redpx >= darkpx else "black"

RED = json.load(open(ROOT + r"\scratch\map4456\numbers_easy2.json", encoding="utf-8"))
BLACK = json.load(open(ROOT + r"\scratch\map4456\numbers_black.json", encoding="utf-8"))

n_flip_r = n_flip_b = 0
for t in RED:
    true = ink_of(t["x"], t["y"], t["w"], t["h"])
    if true != t["kind"] and true != "?":
        n_flip_r += 1
    t["kind_true"] = true
for t in BLACK:
    true = ink_of(t["x"], t["y"], t["w"], t["h"])
    if true != "black" and true != "?":
        n_flip_b += 1
    t["kind_true"] = true
print("red tokens reclassified:", n_flip_r, "of", len(RED))
print("black tokens reclassified:", n_flip_b, "of", len(BLACK))

# rebuild the two lists: kind_true decides where a token lives
red_out, black_out = [], []
for t in RED:
    t["kind"] = t["kind_true"]
    (red_out if t["kind"] == "red" else black_out).append(t)
for t in BLACK:
    if t["kind_true"] == "black":
        black_out.append(t)
    elif t["kind_true"] == "red":
        red_out.append(t)
print("after correction: red", len(red_out), " black", len(black_out))

json.dump(red_out, open(ROOT + r"\scratch\map4456\numbers_easy2.json", "w", encoding="utf-8"),
          ensure_ascii=False)
json.dump(black_out, open(ROOT + r"\scratch\map4456\numbers_black.json", "w", encoding="utf-8"),
          ensure_ascii=False)

# region tokens, corrected
REG = json.load(open(ROOT + r"\scratch\map4456\region_polygon.json", encoding="utf-8"))
POLY = REG["polygon"]
def pip(x, y):
    ins = False
    n = len(POLY)
    for i in range(n):
        x1, y1 = POLY[i]; x2, y2 = POLY[(i + 1) % n]
        if ((y1 > y) != (y2 > y)) and (x < (x2 - x1) * (y - y1) / (y2 - y1) + x1):
            ins = not ins
    return ins
rin = [t for t in red_out if pip(t["x"] + t["w"] // 2, t["y"] + t["h"] // 2)]
bin_ = [t for t in black_out if pip(t["x"] + t["w"] // 2, t["y"] + t["h"] // 2)]
json.dump({"red": rin, "black": bin_},
          open(ROOT + r"\scratch\map4456\region_tokens.json", "w", encoding="utf-8"))
print("region tokens corrected: red %d, black %d" % (len(rin), len(bin_)))
