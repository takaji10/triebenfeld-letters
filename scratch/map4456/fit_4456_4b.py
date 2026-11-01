# The mapping of 4456-4.jpg inside 4456_full.jpg, take 2: wide search window
# (the sheet extends past the cell's edges), finer scale grid, visual check.
import numpy as np
import pyvips

DIR = r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456"
FULL = DIR + r"\4456_full.jpg"
SHEET = DIR + r"\4456-4.jpg"
OUT = r"C:\Users\Tersnaus\AppData\Local\Temp\opencode"
APP = 16          # thumb factor for the search
SHEET_W, SHEET_H = 7454, 7392
FULL_W, FULL_H = 21715, 14206


def grey(path, factor):
    im = pyvips.Image.new_from_file(path)
    im = im.resize(1.0 / factor)
    b = im.extract_band(1)
    a = b.write_to_memory()
    return np.frombuffer(a, np.uint8).reshape(b.height, b.width).astype(np.float64)


def ncc_best(image_region, patch):
    h, w = patch.shape
    H, W = image_region.shape
    T = patch - patch.mean()
    tnorm = np.sqrt((T * T).sum())
    if tnorm == 0:
        return (-2.0, (0, 0))
    I = image_region
    N = (H + h - 1, W + w - 1)
    fs = np.fft.fft2(I, s=N)
    f1 = np.fft.fft2(np.ones((h, w)), s=N)
    fi2 = np.fft.fft2(I * I, s=N)
    fp = np.fft.fft2(T, s=N)
    hh, ww = H - h + 1, W - w + 1
    dot = np.fft.ifft2(fs * np.conj(fp))[:hh, :ww].real
    s1 = np.fft.ifft2(fs * f1)[:hh, :ww].real
    s2 = np.fft.ifft2(fi2 * f1)[:hh, :ww].real
    n = h * w
    var = s2 / n - (s1 / n) ** 2
    var[var < 1e-9] = 1e-9
    score = dot / (n * np.sqrt(var) * tnorm)
    iy, ix = np.unravel_index(np.argmax(score), score.shape)
    return float(score[iy, ix]), (int(iy), int(ix))


full = grey(FULL, APP)          # (fh, fw)
sheet = grey(SHEET, APP)        # (sh, sw)
fh, fw = full.shape
sh, sw = sheet.shape
print("full thumb", full.shape, "sheet thumb", sheet.shape)

# the (row 1, col 1) cell's centre in APP space, with a wide window
cx, cy = fw // 2, 3 * fh // 4
WIN = int(0.9 * sw)             # sheet is ~466 wide at APP 16: window 419
region = full[max(0, cy - WIN):min(fh, cy + WIN), max(0, cx - WIN):min(fw, cx + WIN)]
rx, ry = max(0, cx - WIN), max(0, cy - WIN)
print("region", region.shape, "at", (rx, ry))

P = 120
results = []
cands = [(0.3, 0.3), (0.3, 0.7), (0.7, 0.3), (0.7, 0.7), (0.5, 0.5), (0.2, 0.5), (0.5, 0.2),
         (0.8, 0.5), (0.5, 0.8), (0.35, 0.65), (0.65, 0.35)]
SCALES = np.arange(0.90, 1.021, 0.005)
for fy, fx in cands:
    py, px = int(sh * fy), int(sw * fx)
    patch = sheet[py:py + P, px:px + P]
    if patch.std() < 10:
        continue
    best = (-2, None, None)
    for s in SCALES:
        ps = max(8, int(round(P * s)))
        yi = np.linspace(0, patch.shape[0] - 1, ps).round().astype(int)
        xi = np.linspace(0, patch.shape[1] - 1, ps).round().astype(int)
        t = patch[np.ix_(yi, xi)]
        score, (iy, ix) = ncc_best(region, t)
        if score > best[0]:
            best = (score, s, (iy, ix))
    if best[1] is None:
        continue
    score, s, (iy, ix) = best
    # full-space coords of the sheet's top-left when this patch matches
    tx = (rx + ix) * APP - s * px * APP
    ty = (ry + iy) * APP - s * py * APP
    results.append({"patch": (fy, fx), "score": round(score, 3), "s": float(s),
                    "tx": tx, "ty": ty})
    print(f"patch {fy:.2f},{fx:.2f} score {score:.3f} s {s:.3f} tx {tx:.0f} ty {ty:.0f}")

good = [r for r in results if r["score"] > 0.25]
print("good patches:", len(good))
if good:
    ss = [r["s"] for r in good]
    txs = [r["tx"] for r in good]
    tys = [r["ty"] for r in good]
    print("median s", np.median(ss), "median tx", np.median(txs), "median ty", np.median(tys))
    # visual check: draw the sheet's frame at the median fit on a full thumb
    s = float(np.median(ss))
    tx, ty = float(np.median(txs)), float(np.median(tys))
    vis = pyvips.Image.new_from_file(FULL).resize(900.0 / FULL_W)
    arr = np.frombuffer(vis.write_to_memory(), np.uint8).reshape(vis.height, vis.width, vis.bands).copy()
    sc = 900.0 / FULL_W
    x0, y0 = int(tx * sc), int(ty * sc)
    x1, y1 = int((tx + s * SHEET_W) * sc), int((ty + s * SHEET_H) * sc)
    x0c, y0c, x1c, y1c = np.clip([x0, y0, x1, y1], 0, [arr.shape[1] - 1, arr.shape[0] - 1] * 2)
    arr[y0c:y1c, x0c, 0] = 255; arr[y0c:y1c, x1c, 0] = 255
    arr[y0c, x0c:x1c, 0] = 255; arr[y1c, x0c:x1c, 0] = 255
    pyvips.Image.new_from_array(arr).write_to_file(OUT + r"\fit_check.png")
    print("frame drawn ->", OUT + r"\fit_check.png")
