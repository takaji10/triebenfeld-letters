# Where is the red ink on the mosaic? Downsample, mask red-dominant pixels,
# cluster by connected boxes on a coarse grid, print the biggest clusters in
# mosaic coordinates.
import numpy as np
import pyvips

FULL = r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456\4456_full.jpg"
APP = 6
im = pyvips.Image.new_from_file(FULL).resize(1.0 / APP)
a = np.frombuffer(im.write_to_memory(), np.uint8).reshape(im.height, im.width, 3).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
red = (R > 110) & (R - G > 45) & (R - B > 45)
print("red px at 1/%d: %d" % (APP, red.sum()))

# coarse clustering: bucket red pixels on a 32-px (thumb) grid, merge adjacent
# buckets, print the biggest merged clusters in mosaic coordinates
H, W = red.shape
CELL = 24
gh, gw = H // CELL, W // CELL
grid = red[:gh * CELL, :gw * CELL].reshape(gh, CELL, gw, CELL).sum(axis=(1, 3))
mask = grid > 8
# merge adjacent mask cells (4-neighbour flood, no scipy: simple BFS)
seen = np.zeros_like(mask, dtype=bool)
out = []
for gy in range(gh):
    for gx in range(gw):
        if mask[gy, gx] and not seen[gy, gx]:
            stack = [(gy, gx)]
            seen[gy, gx] = True
            cells = []
            while stack:
                y, x = stack.pop()
                cells.append((y, x))
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
                    yy, xx = y + dy, x + dx
                    if 0 <= yy < gh and 0 <= xx < gw and mask[yy, xx] and not seen[yy, xx]:
                        seen[yy, xx] = True
                        stack.append((yy, xx))
            out.append(cells)
out.sort(key=len, reverse=True)
for cells in out[:45]:
    ys = [c[0] for c in cells]
    xs = [c[1] for c in cells]
    print("cluster cells %3d  mosaic x %6d-%6d  y %6d-%6d"
          % (len(cells), min(xs) * CELL * APP, (max(xs) + 1) * CELL * APP,
             min(ys) * CELL * APP, (max(ys) + 1) * CELL * APP))
