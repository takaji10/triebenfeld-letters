# Where is 4456-4.jpg in 4456_full.jpg? Wide scale sweep with the corrected
# zero-normalized NCC (score = dot / (sqrt(sum((I-mean)^2)) * tnorm)).
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


def zncc_top(I, patch, topk=3):
    h, w = patch.shape
    H, W = I.shape
    T = patch - patch.mean()
    tn = np.sqrt((T * T).sum())
    N = (H + h - 1, W + w - 1)
    fs = np.fft.fft2(I, s=N)
    fi2 = np.fft.fft2(I * I, s=N)
    fp = np.fft.fft2(T, s=N)
    f1 = np.fft.fft2(np.ones((h, w)), s=N)
    hh, ww = H - h + 1, W - w + 1
    dot = np.fft.ifft2(fs * np.conj(fp))[:hh, :ww].real
    s1 = np.fft.ifft2(fs * np.conj(f1))[:hh, :ww].real
    s2 = np.fft.ifft2(fi2 * np.conj(f1))[:hh, :ww].real
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


# validate
full = grey(FULL, APP)
sheet = grey(SHEET, APP)
print("self-match:", zncc_top(full, full[500:700, 700:900], 1))

P = 200
# a feature-rich patch: the river bend area of sheet 4 (lower middle)
patch = sheet[int(sheet.shape[0] * 0.62):int(sheet.shape[0] * 0.62) + P,
              int(sheet.shape[1] * 0.45):int(sheet.shape[1] * 0.45) + P]
print("patch std", patch.std())
for scale in np.arange(0.85, 1.101, 0.01):
    ps = int(round(P * scale))
    yi = np.linspace(0, patch.shape[0] - 1, ps).round().astype(int)
    xi = np.linspace(0, patch.shape[1] - 1, ps).round().astype(int)
    t = patch[np.ix_(yi, xi)]
    for score, ix, iy in zncc_top(full, t, 1):
        tx = ix * APP - 0.45 * sheet.shape[1] * scale * APP
        ty = iy * APP - 0.62 * sheet.shape[0] * scale * APP
        print("scale %.2f score %.3f at (%d,%d) -> sheet top-left (%.0f, %.0f)"
              % (scale, score, ix * APP, iy * APP, tx, ty))
