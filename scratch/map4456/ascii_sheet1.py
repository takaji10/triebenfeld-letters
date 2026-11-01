# ASCII rendering of sheet 1's region (and a coarse whole-mosaic view):
# per-cell dark-ink density and red-ink density, to see where the
# information blocks sit and where the drawn map runs.
import numpy as np
import pyvips

FULL = (r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)"
        r"\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456\4456_full.jpg")
DS = 8
CELL = 8   # -> 64 mosaic px per char
im = pyvips.Image.new_from_file(FULL, access="random")
small = im.resize(1.0 / DS)
a = np.frombuffer(small.write_to_memory(), np.uint8).reshape(
    small.height, small.width, 3).astype(int)
R = a[:, :, 0]; G = a[:, :, 1]; B = a[:, :, 2]
lum = (R * 299 + G * 587 + B * 114) // 1000
dark = lum < 125
red = (R > 100) & (R - G > 40) & (R - B > 40)

gh, gw = a.shape[0] // CELL, a.shape[1] // CELL
D = dark[:gh * CELL, :gw * CELL].reshape(gh, CELL, gw, CELL).mean(axis=(1, 3))
Rr = red[:gh * CELL, :gw * CELL].reshape(gh, CELL, gw, CELL).mean(axis=(1, 3))

def art(x0, x1, y0, y1, step=1, title=""):
    print("\n== %s  (mosaic x %d..%d, y %d..%d; char = %d px) ==" %
          (title, x0, x1, y0, y1, CELL * DS * step))
    ncols = (x1 - x0) // (CELL * DS * step)
    print("     " + "".join(str((x0 + x * CELL * DS * step) // 1000 % 10)
                            for x in range(ncols)))
    gy0, gy1 = y0 // (CELL * DS), y1 // (CELL * DS)
    gx0, gx1 = x0 // (CELL * DS), x1 // (CELL * DS)
    for gy in range(gy0, gy1, step):
        line = []
        for gx in range(gx0, gx1, step):
            d = D[gy:gy + step, gx:gx + step].mean()
            r = Rr[gy:gy + step, gx:gx + step].mean()
            if r > 0.04:
                c = "R"
            elif d > 0.30:
                c = "#"
            elif d > 0.15:
                c = "+"
            elif d > 0.06:
                c = ":"
            elif d > 0.02:
                c = "."
            else:
                c = " "
            line.append(c)
        print("%5d %s" % (gy * CELL * DS, "".join(line)))

# sheet 1, fine
art(0, 7300, 0, 7100, step=1, title="sheet 1 (top-left)")
