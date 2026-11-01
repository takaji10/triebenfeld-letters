# Sheet 4 in the mosaic, refined: scale fixed 1.000 (the other sheets lock
# there and the mosaic is uniform), patches from across the sheet, search
# local round the coarse position (5725, 5638).
import numpy as np
import pyvips

DIR = r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456"
FULL = DIR + r"\4456_full.jpg"
SHEET = DIR + r"\4456-4.jpg"
APP = 8
TX0, TY0 = 5725, 5638


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


full8 = grey(FULL, APP)
sheet8 = grey(SHEET, APP)
sh, sw = sheet8.shape
P = 300
results = []
for fy, fx in ((0.5, 0.5), (0.3, 0.5), (0.7, 0.5), (0.5, 0.3), (0.5, 0.7),
               (0.35, 0.35), (0.65, 0.65), (0.35, 0.65), (0.65, 0.35)):
    py, px = int(sh * fy) - P // 2, int(sw * fx) - P // 2
    py = max(0, min(sh - P, py)); px = max(0, min(sw - P, px))
    patch = sheet8[py:py + P, px:px + P]
    if patch.std() < 8:
        continue
    # the patch's expected centre in thumb px
    cx, cy = int((TX0 + fx * sw * APP) / APP), int((TY0 + fy * sh * APP) / APP)
    R = 100
    y0, x0 = max(0, cy - R), max(0, cx - R)
    reg = full8[y0:cy + R, x0:cx + R]
    score, (iy, ix) = zncc(reg, patch)
    tx = (x0 + ix) * APP - (px + P / 2) * APP
    ty = (y0 + iy) * APP - (py + P / 2) * APP
    results.append((score, tx, ty, fx, fy))
    print("patch %.2f,%.2f score %.3f -> tx %.0f ty %.0f" % (fx, fy, score, tx, ty))

good = [r for r in results if r[0] > 0.5]
print("good:", len(good), "of", len(results))
if good:
    txs = sorted(r[1] for r in good); tys = sorted(r[2] for r in good)
    med = lambda v: v[len(v) // 2]
    print("median tx", med(txs), "median ty", med(tys), "spread", txs[0], "-", txs[-1], "/", tys[0], "-", tys[-1])
