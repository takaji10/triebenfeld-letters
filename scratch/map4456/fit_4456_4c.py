# Where is 4456-4.jpg in 4456_full.jpg? Global search at scale 1.0 first
# (3 sheet widths ~ 21715, 2 heights ~ 14206: the sheets may be butted at
# native size), patches taken across the whole sheet.
import numpy as np
import pyvips

DIR = r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456"
FULL = DIR + r"\4456_full.jpg"
SHEET = DIR + r"\4456-4.jpg"
APP = 16


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
    sd = np.sqrt(np.maximum(var, 0.0))
    sd[sd < 3.0] = np.inf          # featureless windows cannot match
    score = dot / (n * sd * tnorm)
    score[~np.isfinite(score)] = -2.0
    iy, ix = np.unravel_index(np.argmax(score), score.shape)
    return float(score[iy, ix]), (int(iy), int(ix))


full = grey(FULL, APP)
sheet = grey(SHEET, APP)
fh, fw = full.shape
sh, sw = sheet.shape
print("full", full.shape, "sheet", sheet.shape)

P = 140
cands = [(0.3, 0.3), (0.3, 0.7), (0.7, 0.3), (0.7, 0.7), (0.5, 0.5), (0.2, 0.5),
         (0.8, 0.5), (0.5, 0.2), (0.5, 0.8), (0.4, 0.4), (0.6, 0.6)]
for fy, fx in cands:
    py, px = int(sh * fy), int(sw * fx)
    patch = sheet[py:py + P, px:px + P]
    if patch.std() < 10:
        continue
    score, (iy, ix) = ncc_best(full, patch)
    # full-space position of the SHEET'S top-left if this patch matched
    tx = ix * APP - px * APP
    ty = iy * APP - py * APP
    print(f"patch {fy:.2f},{fx:.2f} score {score:.3f} -> sheet top-left at ({tx}, {ty})")
