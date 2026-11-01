# Which cell of 4456_full.jpg is each 4456-N.jpg? A 3x2 grid is suspected.
import numpy as np
import pyvips

FULL = r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456\4456_full.jpg"
DIR = r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456"
THUMB_W = 2160  # divisible by 6 nice enough


def to_thumb(path, target=None, crop=None):
    im = pyvips.Image.new_from_file(path)
    if crop:
        im = im.extract_area(crop[0], crop[1], crop[2], crop[3])
    scale = target / im.width
    im = im.resize(scale)
    a = im.write_to_memory()
    return np.frombuffer(a, np.uint8).reshape(im.height, im.width, 3)


def norm(a):
    a = a.astype(np.float64)
    a = a.mean(axis=2)
    a -= a.mean()
    s = a.std()
    return a / s if s else a


full = to_thumb(FULL, THUMB_W)
fh, fw, _ = full.shape
print("full thumb", full.shape)

for name in ["4456-1.jpg", "4456-2.jpg", "4456-3.jpg", "4456-4.jpg", "4456-5.jpg"]:
    thumb = to_thumb(DIR + "\\" + name, 700)
    sheet = norm(thumb)
    best = (-2, None)
    for row in (0, 1):
        for col in (0, 1, 2):
            cell = full[row * fh // 2:(row + 1) * fh // 2, col * fw // 3:(col + 1) * fw // 3]
            ch, cw, _ = cell.shape
            sh, sw = sheet.shape
            # nearest-neighbour resample with numpy
            yi = (np.arange(ch) * sh // ch).clip(0, sh - 1)
            xi = (np.arange(cw) * sw // cw).clip(0, sw - 1)
            s2 = sheet[yi][:, xi]
            a = norm(cell)
            b = s2 - s2.mean()
            corr = float((a * b).mean())
            if corr > best[0]:
                best = (corr, (row, col))
    print(name, "best cell (row,col)=", best[1], "corr=", round(best[0], 3))
