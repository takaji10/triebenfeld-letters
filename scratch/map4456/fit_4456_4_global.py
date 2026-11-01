# Sheet 4: global FFT-ZNCC sweep over the whole mosaic, scale 0.98-1.02,
# patches from the sheet's four quadrants, top-3 peaks each, votes counted.
import numpy as np
import pyvips
from collections import Counter

DIR = r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456"
FULL = DIR + r"\4456_full.jpg"
SHEET = DIR + r"\4456-4.jpg"
APP = 8


def grey(path, factor):
    im = pyvips.Image.new_from_file(path).resize(1.0 / factor)
    b = im.extract_band(1)
    a = b.write_to_memory()
    return np.frombuffer(a, np.uint8).reshape(b.height, b.width).astype(np.float64)


def zncc_top(I, patch, topk=3):
    h, w = patch.shape
    H, W = I.shape
    T = patch - patch.mean()
    tn = np.sqrt((T * T).sum())
    if tn == 0:
        return []
    N = (H + h - 1, W + w - 1)
    fs = np.fft.fft2(I, s=N)
    fp = np.fft.fft2(T, s=N)
    f1 = np.fft.fft2(np.ones((h, w)), s=N)
    fi2 = np.fft.fft2(I * I, s=N)
    hh, ww = H - h + 1, W - w + 1
    dot = np.fft.ifft2(fs * np.conj(fp)).real[:hh, :ww]
    s1 = np.fft.ifft2(fs * np.conj(f1)).real[:hh, :ww]
    s2 = np.fft.ifft2(fi2 * np.conj(f1)).real[:hh, :ww]
    sd = np.sqrt(np.maximum(s2 - s1 * s1 / (h * w), 0.0))
    sd[sd < 3.0 * np.sqrt(h * w)] = np.inf
    score = dot / (sd * tn)
    score[~np.isfinite(score)] = -2.0
    out = []
    sc = score.copy()
    for _ in range(topk):
        iy, ix = np.unravel_index(np.argmax(sc), sc.shape)
        out.append((float(sc[iy, ix]), int(ix), int(iy)))
        y0, y1 = max(0, iy - h // 2), min(sc.shape[0], iy + h // 2 + 1)
        x0, x1 = max(0, ix - w // 2), min(sc.shape[1], ix + w // 2 + 1)
        sc[y0:y1, x0:x1] = -2.0
    return out


full8 = grey(FULL, APP)
sheet8 = grey(SHEET, APP)
sh, sw = sheet8.shape
print("full", full8.shape, "sheet", sheet8.shape)

P = 220
votes = []
for fy, fx in ((0.5, 0.5), (0.3, 0.5), (0.7, 0.5), (0.5, 0.3), (0.5, 0.7)):
    py, px = int(sh * fy) - P // 2, int(sw * fx) - P // 2
    patch = sheet8[py:py + P, px:px + P]
    if patch.std() < 8:
        continue
    for scale in np.arange(0.98, 1.021, 0.005):
        ps = int(round(P * scale))
        yi = np.linspace(0, P - 1, ps).round().astype(int)
        xi = np.linspace(0, P - 1, ps).round().astype(int)
        t = patch[np.ix_(yi, xi)]
        for score, ix, iy in zncc_top(full8, t, 2):
            tx = ix * APP - px * scale * APP
            ty = iy * APP - py * scale * APP
            votes.append((score, scale, tx, ty, fx, fy))
    best = sorted([v for v in votes if v[4] == fx and v[5] == fy], reverse=True)[:3]
    for b in best:
        print("patch %.2f,%.2f scale %.3f score %.3f -> (%.0f, %.0f)" % (b[4], b[5], b[1], b[0], b[2], b[3]))

good = sorted([v for v in votes if v[0] > 0.7], reverse=True)
print("good:", len(good))
for g in good[:12]:
    print("  score %.3f scale %.3f -> sheet top-left (%.0f, %.0f)  patch %.2f,%.2f"
          % (g[0], g[1], g[2], g[3], g[4], g[5]))
