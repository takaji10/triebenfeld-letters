# The layout of 4456_full.jpg, take 3: the coarse positions of take 2 are
# confirmed at APP 8 and refined at APP 4 locally round each sheet's known
# corner, then each sheet's frame is drawn on a composite thumb for a look.
# Also: verify sheet 4's mapping against the MapWarper GCPs' neighbourhoods.
import numpy as np
import pyvips

DIR = r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456"
FULL = DIR + r"\4456_full.jpg"
OUT = r"C:\Users\Tersnaus\AppData\Local\Temp\opencode"
FULL_W, FULL_H = 21715, 14206
SHEETS = {1: (7449, 7487), 2: (7554, 7372), 3: (7651, 7333), 4: (7454, 7392), 5: (7754, 7053)}
# take 2's coarse results, composite pixels
COARSE = {1: (1.000, -1344, -1376), 2: (1.000, 5688, -1264),
          3: (1.015, 12751, 5463), 4: (1.005, 5725, 5638), 5: (1.000, -1632, 5680)}


def grey(path, factor, crop=None):
    im = pyvips.Image.new_from_file(path)
    if crop:
        im = im.extract_area(*crop)
    im = im.resize(1.0 / factor)
    b = im.extract_band(1)
    a = b.write_to_memory()
    return np.frombuffer(a, np.uint8).reshape(b.height, b.width).astype(np.float64)


def zncc(I, patch):
    h, w = patch.shape
    H, W = I.shape
    T = patch - patch.mean()
    tn = np.sqrt((T * T).sum())
    if tn == 0:
        return -2.0, (0, 0)
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
    iy, ix = np.unravel_index(np.argmax(score), score.shape)
    return float(score[iy, ix]), (int(iy), int(ix))


full8 = grey(FULL, 8)
print("APP8", full8.shape)

# refine each sheet locally at APP 8 round the coarse corner
fine = {}
for n, (s0, tx0, ty0) in COARSE.items():
    W, H = SHEETS[n]
    sheet = grey(DIR + r"\4456-%d.jpg" % n, 8)
    sh, sw = sheet.shape
    P = 300
    # patch at the sheet's centre
    py, px = sh // 2 - P // 2, sw // 2 - P // 2
    patch = sheet[py:py + P, px:px + P]
    # search the composite round the expected patch position, +/- 120 thumb px
    ex, ey = tx0 + s0 * (px + P / 2), ty0 + s0 * (py + P / 2)   # in composite px
    cx, cy = int(ex / 8), int(ey / 8)
    R = 120
    reg = full8[max(0, cy - R):cy + R, max(0, cx - R):cx + R]
    best = None
    for s in np.arange(0.99, 1.011, 0.0025):
        ps = int(round(P * s))
        yi = np.linspace(0, P - 1, ps).round().astype(int)
        xi = np.linspace(0, P - 1, ps).round().astype(int)
        t = patch[np.ix_(yi, xi)]
        score, (iy, ix) = zncc(reg, t)
        if best is None or score > best[0]:
            best = (score, float(s), ix, iy)
    score, s, ix, iy = best
    # reg's top-left in composite thumb px:
    rx, ry = max(0, cx - R), max(0, cy - R)
    # patch centre in sheet px: (px + P/2, py + P/2); its match at thumb (rx+ix, ry+iy)
    tx = (rx + ix) * 8 - s * (px + P / 2)
    ty = (ry + iy) * 8 - s * (py + P / 2)
    fine[n] = (s, tx, ty)
    print("sheet %d: score %.3f scale %.4f tx %.0f ty %.0f" % (n, score, s, tx, ty))

# draw all five frames on one thumb
vis = pyvips.Image.new_from_file(FULL).resize(1200.0 / FULL_W)
arr = np.frombuffer(vis.write_to_memory(), np.uint8).reshape(vis.height, vis.width, vis.bands).copy()
sc = 1200.0 / FULL_W
for n, (s, tx, ty) in fine.items():
    W, H = SHEETS[n]
    x0, y0, x1, y1 = [int(v * sc) for v in (tx, ty, tx + s * W, ty + s * H)]
    x0c, y0c, x1c, y1c = np.clip([x0, y0, x1, y1], 0, [arr.shape[1] - 1, arr.shape[0] - 1] * 2)
    col = [255, 0, 0] if n == 4 else [0, 160, 0]
    arr[y0c:y1c, x0c] = col; arr[y0c:y1c, x1c - 1] = col
    arr[y0c, x0c:x1c] = col; arr[y1c - 1, x0c:x1c] = col
pyvips.Image.new_from_array(arr).write_to_file(OUT + r"\layout_check.png")
print("frames ->", OUT + r"\layout_check.png")
