# Geometry check of take 2's coarse results at scale 1.000, plus frames drawn.
import numpy as np
import pyvips

DIR = r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456"
FULL = DIR + r"\4456_full.jpg"
OUT = r"C:\Users\Tersnaus\AppData\Local\Temp\opencode"
FULL_W, FULL_H = 21715, 14206
SHEETS = {1: (7449, 7487), 2: (7554, 7372), 3: (7651, 7333), 4: (7454, 7392), 5: (7754, 7053)}
# take 2 (scale fixed 1.000 where it locked; sheet 3's 1.015 and sheet 4's 1.005 suspect)
T = {1: (1.000, -1344, -1376), 2: (1.000, 5688, -1264),
     3: (1.015, 12751, 5463), 4: (1.005, 5725, 5638), 5: (1.000, -1632, 5680)}

print("sheet  tx      ty     x1      y1")
for n, (s, tx, ty) in T.items():
    W, H = SHEETS[n]
    print("%d  %7.0f %7.0f %7.0f %7.0f" % (n, tx, ty, tx + s * W, ty + s * H))

# overlaps: sheet 1 right edge vs sheet 2 left edge, etc.
def ov(a, b):
    ax0, ay0 = T[a][1], T[a][2]
    ax1, ay1 = ax0 + T[a][0] * SHEETS[a][0], ay0 + T[a][0] * SHEETS[a][1]
    bx0, by0 = T[b][1], T[b][2]
    bx1, by1 = bx0 + T[b][0] * SHEETS[b][0], by0 + T[b][0] * SHEETS[b][1]
    ox = min(ax1, bx1) - max(ax0, bx0)
    oy = min(ay1, by1) - max(ay0, by0)
    return ox, oy

for a, b in ((1, 2), (4, 3), (5, 4), (2, 3), (5, 1)):
    print("overlap %d-%d:" % (a, b), ov(a, b))

vis = pyvips.Image.new_from_file(FULL).resize(1200.0 / FULL_W)
arr = np.frombuffer(vis.write_to_memory(), np.uint8).reshape(vis.height, vis.width, vis.bands).copy()
sc = 1200.0 / FULL_W
for n, (s, tx, ty) in T.items():
    W, H = SHEETS[n]
    x0, y0, x1, y1 = [int(v * sc) for v in (tx, ty, tx + s * W, ty + s * H)]
    x0c, y0c, x1c, y1c = np.clip([x0, y0, x1, y1], 0, [arr.shape[1] - 1, arr.shape[0] - 1] * 2)
    col = [255, 0, 0] if n == 4 else [0, 160, 0]
    arr[y0c:y1c, x0c] = col; arr[y0c:y1c, x1c - 1] = col
    arr[y0c, x0c:x1c] = col; arr[y1c - 1, x0c:x1c] = col
pyvips.Image.new_from_array(arr).write_to_file(OUT + r"\layout_check2.png")
print("frames ->", OUT + r"\layout_check2.png")
