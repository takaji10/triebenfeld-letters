# Where is 4456-4.jpg in 4456_full.jpg? Correct zero-normalized NCC, global
# search, scales 0.90-1.02, rotations 0/90/180/270.
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


def zncc(I, patch):
    h, w = patch.shape
    H, W = I.shape
    T = patch - patch.mean()
    tn = np.sqrt((T * T).sum())
    if tn == 0:
        return -2.0, (0, 0), None
    N = (H + h - 1, W + w - 1)
    fs = np.fft.fft2(I, s=N)
    f1 = np.fft.fft2(np.ones((h, w)), s=N)
    fi2 = np.fft.fft2(I * I, s=N)
    fp = np.fft.fft2(T, s=N)
    hh, ww = H - h + 1, W - w + 1
    dot = np.fft.ifft2(fs * np.conj(fp))[:hh, :ww].real
    s1 = np.fft.ifft2(fs * np.conj(f1))[:hh, :ww].real
    s2 = np.fft.ifft2(fi2 * np.conj(f1))[:hh, :ww].real
    n = h * w
    num = dot - (T.mean() * 0 + patch.mean() * 0)  # placeholder, replaced below
    num = dot - patch.mean() * s1
    var = s2 / n - (s1 / n) ** 2
    sd = np.sqrt(np.maximum(var, 0.0)) * np.sqrt(n)
    sd[sd < 3.0 * np.sqrt(n)] = np.inf
    score = num / (sd * tn)
    score[~np.isfinite(score)] = -2.0
    iy, ix = np.unravel_index(np.argmax(score), score.shape)
    return float(score[iy, ix]), (int(iy), int(ix))


full = grey(FULL, APP)
sheet = grey(SHEET, APP)
fh, fw = full.shape
sh, sw = sheet.shape
print("full", full.shape, "sheet", sheet.shape)

# validate: self-match
s0, (iy0, ix0) = zncc(full, full[500:640, 700:840])
print("self-match score %.3f at (%d,%d) expect (700,500)" % (s0, ix0, iy0))

P = 140
cands = [(0.3, 0.3), (0.3, 0.7), (0.7, 0.3), (0.7, 0.7), (0.5, 0.5)]
for rot in (0, 90, 180, 270):
    s_im = np.rot90(sheet, k=rot // 90)
    rh, rw = s_im.shape
    for scale in (0.95, 1.0):
        if rot % 180 and scale != 1.0:
            pass
        ps = P * scale
        hits = []
        for fy, fx in cands:
            py, px = int(rh * fy), int(rw * fx)
            py = min(py, rh - P - 1); px = min(px, rw - P - 1)
            patch = s_im[py:py + P, px:px + P]
            if patch.std() < 10:
                continue
            score, (iy, ix) = zncc(full, patch)
            hits.append((score, ix * APP, iy * APP, fx, fy))
        hits.sort(reverse=True)
        tops = ", ".join("%.2f@(%d,%d)" % (h[0], h[1], h[2]) for h in hits[:3])
        print("rot %3d scale %.2f: %s" % (rot, scale, tops))
