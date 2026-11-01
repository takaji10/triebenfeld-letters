# The mapping of 4456-4.jpg inside 4456_full.jpg: uniform-scale search on
# interior patches (FFT-NCC), then the (sx, sy, tx, ty) that best fits all.
import numpy as np
import pyvips

DIR = r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456"
FULL = DIR + r"\4456_full.jpg"
SHEET = DIR + r"\4456-4.jpg"
SHEET_W, SHEET_H = 7454, 7392
APP = 8


def grey_thumb(path, factor, scale=1.0):
    im = pyvips.Image.new_from_file(path)
    im = im.resize(1.0 / factor * scale)
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


full = grey_thumb(FULL, APP)
fw, fh = full.shape[1], full.shape[0]
# the (row 1, col 1) cell, with margin
cl, ct = fw // 3 - 60, fh // 2 - 60
cw, ch = fw // 3 + 120, fh // 2 + 120
cell = full[ct:ct + ch, cl:cl + cw]

sheet = grey_thumb(SHEET, APP)
sh, sw = sheet.shape

rng = np.random.default_rng(7)
P = 110  # patch size in APP-space
results = []
cands = [(0.25, 0.25), (0.25, 0.75), (0.75, 0.25), (0.75, 0.75), (0.5, 0.5),
         (0.15, 0.5), (0.85, 0.5), (0.5, 0.15), (0.5, 0.85), (0.35, 0.35),
         (0.65, 0.65), (0.4, 0.7)]
SCALES = [0.94, 0.945, 0.95, 0.955, 0.96, 0.965, 0.97, 0.975, 0.98, 0.985, 0.99]
for fy, fx in cands:
    py, px = int(sh * fy), int(sw * fx)
    patch = sheet[py:py + P, px:px + P]
    if patch.std() < 12:
        continue
    best = (-2, None, None)
    for s in SCALES:
        ps = max(6, int(round(P * s)))
        im = pyvips.Image.new_from_array(patch.astype(np.uint8))
        nb = patch.ndim if patch.ndim == 3 else 1
        if nb == 1:
            im = im.resize(ps / patch.shape[1])
            arr = np.frombuffer(im.write_to_memory(), np.uint8)
            n = im.width * im.height
            arr = arr[:n * 1] if arr.size >= n else arr
            t = arr.reshape(im.height, im.width).astype(np.float64)
        else:
            im = im.resize(ps / patch.shape[1])
            arr = np.frombuffer(im.write_to_memory(), np.uint8)
            arr = arr[:im.width * im.height * 3].reshape(im.height, im.width, 3)
            t = arr[:, :, 0].astype(np.float64)
        # the resized patch may be a few pixels off ps: resample in numpy instead, exactly ps x ps
        yi = (np.linspace(0, t.shape[0] - 1, ps)).round().astype(int)
        xi = (np.linspace(0, t.shape[1] - 1, ps)).round().astype(int)
        t = t[np.ix_(np.clip(yi, 0, t.shape[0] - 1), np.clip(xi, 0, t.shape[1] - 1))]
        score, (iy, ix) = ncc_best(cell, t)
        if score > best[0]:
            best = (score, s, (iy, ix))
    if best[1] is None:
        continue
    score, s, (iy, ix) = best
    # full-space coordinates of this patch's top-left
    tx = (cl + ix) * APP - s * px * APP
    ty = (ct + iy) * APP - s * py * APP
    results.append({"patch": (fy, fx), "score": round(score, 3), "s": s,
                    "tx": tx, "ty": ty, "local": ((iy + ct) * APP, (ix + cl) * APP)})
    print(f"patch {fy:.2f},{fx:.2f} score {score:.3f} s {s:.3f} tx {tx:.0f} ty {ty:.0f}")

ss = [r["s"] for r in results]
txs = [r["tx"] for r in results]
tys = [r["ty"] for r in results]
print("scales:", ss)
print("median s", np.median(ss), "median tx", np.median(txs), "median ty", np.median(tys))
