# Sheet 4 in the mosaic: direct (non-FFT) NCC around the coarse position,
# no offset algebra beyond the one definition:
#   match of patch whose sheet-position top-left is (px, py) at thumb (X, Y)
#   => sheet top-left = (X*APP - px*APP, Y*APP - py*APP)   [scale 1]
# Each patch votes for a sheet top-left; the mode is the answer.
import numpy as np
import pyvips
from collections import Counter

DIR = r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456"
FULL = DIR + r"\4456_full.jpg"
SHEET = DIR + r"\4456-4.jpg"
APP = 8
TX0, TY0 = 5725, 5638


def grey(path, factor):
    im = pyvips.Image.new_from_file(path).resize(1.0 / factor)
    b = im.extract_band(1)
    a = b.write_to_memory()
    return np.frombuffer(a, np.uint8).reshape(b.height, b.width).astype(np.float64)


def direct_ncc(reg, patch):
    h, w = patch.shape
    H, W = reg.shape
    T = patch - patch.mean()
    tn = np.sqrt((T * T).sum())
    best = (-2, 0, 0)
    for iy in range(H - h + 1):
        for ix in range(0, W - w + 1, 2):
            win = reg[iy:iy + h, ix:ix + w]
            Wm = win - win.mean()
            dw = np.sqrt((Wm * Wm).sum())
            if dw == 0:
                continue
            s = float((Wm * T).sum() / (dw * tn))
            if s > best[0]:
                best = (s, iy, ix)
    return best


full8 = grey(FULL, APP)
sheet8 = grey(SHEET, APP)
sh, sw = sheet8.shape
P = 160
votes = []
for fy, fx in ((0.5, 0.5), (0.3, 0.5), (0.7, 0.5), (0.5, 0.3), (0.5, 0.7)):
    py, px = int(sh * fy) - P // 2, int(sw * fx) - P // 2
    patch = sheet8[py:py + P, px:px + P]
    if patch.std() < 8:
        continue
    # expected patch top-left in thumb px
    ex, ey = int((TX0 + fx * sw * APP) / APP), int((TY0 + fy * sh * APP) / APP)
    R = 24
    reg = full8[max(0, ey - R):ey + P + R, max(0, ex - R):ex + P + R]
    score, iy, ix = direct_ncc(reg, patch)
    X, Y = max(0, ex - R) + ix, max(0, ey - R) + iy
    tx = X * APP - px * APP
    ty = Y * APP - py * APP
    votes.append((score, tx, ty, fx, fy))
    print("patch %.2f,%.2f score %.3f -> sheet top-left (%.0f, %.0f)" % (fx, fy, score, tx, ty))

good = [v for v in votes if v[0] > 0.7]
print("good:", len(good))
for g in good:
    print("  vote", g[3], g[4], "->", g[1], g[2], "score", round(g[0], 3))
if good:
    tx = Counter(round(v[1]) for v in good).most_common(1)[0]
    ty = Counter(round(v[2]) for v in good).most_common(1)[0]
    print("mode tx", tx, "mode ty", ty)
