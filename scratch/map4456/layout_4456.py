# The layout of 4456_full.jpg: where each sheet JPG sits in it. Corrected
# zero-normalized NCC (self-match scores ~1.0), patch per sheet, scales swept.
# Output: per sheet, the best (score, scale, tx, ty) - tx/ty the sheet's
# top-left in composite pixels.
import numpy as np
import pyvips

DIR = r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456"
FULL = DIR + r"\4456_full.jpg"
APP = 16
FULL_W, FULL_H = 21715, 14206


def grey(path, factor):
    im = pyvips.Image.new_from_file(path)
    im = im.resize(1.0 / factor)
    b = im.extract_band(1)
    a = b.write_to_memory()
    return np.frombuffer(a, np.uint8).reshape(b.height, b.width).astype(np.float64)


def prep_image(I, patch_shape):
    h, w = patch_shape
    H, W = I.shape
    N = (H + h - 1, W + w - 1)
    return (np.fft.fft2(I, s=N), np.fft.fft2(I * I, s=N), H, W)


def zncc_top(F, fi2, H, W, patch, topk=1):
    h, w = patch.shape
    T = patch - patch.mean()
    tn = np.sqrt((T * T).sum())
    fp = np.fft.fft2(T, s=F.shape)
    f1 = np.fft.fft2(np.ones((h, w)), s=F.shape)
    hh, ww = H - h + 1, W - w + 1
    dot = np.fft.ifft2(F * np.conj(fp)).real[:hh, :ww]
    s1 = np.fft.ifft2(F * np.conj(f1)).real[:hh, :ww]
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


full = grey(FULL, APP)
fh, fw = full.shape
print("composite thumb", full.shape)

SCALES = np.arange(0.90, 1.021, 0.01)
P = 160
for n in range(1, 6):
    sheet = grey(DIR + r"\4456-%d.jpg" % n, APP)
    sh, sw = sheet.shape
    # three patches: centre and two quarters, richest-text areas chosen by std
    cands = []
    for fy, fx in ((0.5, 0.5), (0.3, 0.5), (0.7, 0.5), (0.5, 0.3), (0.5, 0.7)):
        py, px = int(sh * fy) - P // 2, int(sw * fx) - P // 2
        py = max(0, min(sh - P, py)); px = max(0, min(sw - P, px))
        patch = sheet[py:py + P, px:px + P]
        if patch.std() > 12:
            cands.append((fy, fx, patch))
    if not cands:
        print(n, "no usable patch"); continue
    best = None
    for fy, fx, patch in cands:
        for s in SCALES:
            ps = int(round(P * s))
            yi = np.linspace(0, P - 1, ps).round().astype(int)
            xi = np.linspace(0, P - 1, ps).round().astype(int)
            t = patch[np.ix_(yi, xi)]
            F, fi2, H, W = prep_image(full, t.shape)
            for score, ix, iy in zncc_top(F, fi2, H, W, t, 1):
                tx = ix * APP - (px + P / 2) * s * APP + (P / 2) * s * APP
                # top-left of the sheet in composite px:
                tx = ix * APP - (px + P * s / 2) * APP + (P * s / 2) * APP
                ty = iy * APP - (py + P * s / 2) * APP + (P * s / 2) * APP
                tx = ix * APP - (px + P / 2 - P * s / 2) * APP
                ty = iy * APP - (py + P / 2 - P * s / 2) * APP
                cand = (score, float(s), tx, ty, fx, fy)
                if best is None or cand[0] > best[0]:
                    best = cand
    print("sheet %d: score %.3f scale %.2f tx %.0f ty %.0f (patch %.2f,%.2f)"
          % (n, best[0], best[1], best[2], best[3], best[4], best[5]))
