# Sheet 4 in the mosaic: final fine fit. Centre known ~(7030, 6930) thumb px
# at APP 8, scale ~1.005. Fine scale steps, patches across the sheet, then a
# least-squares corner from all the patch votes.
import numpy as np
import pyvips

DIR = r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456"
FULL = DIR + r"\4456_full.jpg"
SHEET = DIR + r"\4456-4.jpg"
APP = 8
CX0, CY0 = 7030, 6930   # sheet top-left, coarse


def grey(path, factor):
    im = pyvips.Image.new_from_file(path).resize(1.0 / factor)
    b = im.extract_band(1)
    a = b.write_to_memory()
    return np.frombuffer(a, np.uint8).reshape(b.height, b.width).astype(np.float64)


def zncc_top(I, patch, topk=1):
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

# local search window round the coarse corner: region of the mosaic covering
# the whole sheet +- margin
M = 60
y0 = max(0, int(CY0 / APP) - M); x0 = max(0, int(CX0 / APP) - M)
SW, SH = 7454, 7392
y1 = min(full8.shape[0], int((CY0 + SH * 1.02) / APP) + M)
x1 = min(full8.shape[1], int((CX0 + SW * 1.02) / APP) + M)
reg = full8[y0:y1, x0:x1]
print("region", reg.shape, "at thumb", (x0, y0))

P = 240
votes = []
for fy, fx in ((0.5, 0.5), (0.3, 0.5), (0.7, 0.5), (0.5, 0.3), (0.5, 0.7),
               (0.35, 0.35), (0.65, 0.65), (0.35, 0.65), (0.65, 0.35)):
    py, px = int(sh * fy) - P // 2, int(sw * fx) - P // 2
    py = max(0, min(sh - P, py)); px = max(0, min(sw - P, px))
    patch = sheet8[py:py + P, px:px + P]
    if patch.std() < 8:
        continue
    best = None
    for scale in np.arange(0.9975, 1.0076, 0.0025):
        ps = int(round(P * scale))
        yi = np.linspace(0, P - 1, ps).round().astype(int)
        xi = np.linspace(0, P - 1, ps).round().astype(int)
        t = patch[np.ix_(yi, xi)]
        for score, ix, iy in zncc_top(reg, t, 1):
            if best is None or score > best[0]:
                best = (score, float(scale), ix, iy)
    score, scale, ix, iy = best
    # patch centre in sheet px; its match in composite px
    cxs, cys = (px + P / 2), (py + P / 2)
    cxc = (x0 + ix) * APP
    cyc = (y0 + iy) * APP
    tx = cxc - scale * cxs
    ty = cyc - scale * cys
    votes.append((score, scale, tx, ty, fx, fy))
    print("patch %.2f,%.2f score %.3f scale %.4f -> corner (%.0f, %.0f)" % (fx, fy, score, scale, tx, ty))

good = [v for v in votes if v[0] > 0.7]
print("good:", len(good))
if good:
    w = np.array([v[0] for v in good])
    tx = float(np.average([v[2] for v in good], weights=w))
    ty = float(np.average([v[3] for v in good], weights=w))
    sc = float(np.median([v[1] for v in good]))
    print("WEIGHTED corner: scale %.4f tx %.0f ty %.0f" % (sc, tx, ty))
    # residual spread
    print("tx spread", min(v[2] for v in good), "-", max(v[2] for v in good),
          "| ty spread", min(v[3] for v in good), "-", max(v[3] for v in good))
