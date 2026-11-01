# Find the drawn plan's frame on the mosaic: long straight dark lines at 1/8,
# their row/column profiles, and the biggest rectangle they bound.
import numpy as np
import pyvips
from scipy import ndimage

FULL = (r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)"
        r"\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456\4456_full.jpg")
DS = 8
im = pyvips.Image.new_from_file(FULL, access="random")
small = im.resize(1.0 / DS)
a = np.frombuffer(small.write_to_memory(), np.uint8).reshape(
    small.height, small.width, 3).astype(int)
R = a[:, :, 0]; G = a[:, :, 1]; B = a[:, :, 2]
lum = (R * 299 + G * 587 + B * 114) // 1000
dark = lum < 130
print("down", a.shape[1], a.shape[0])

K = 22   # a line >= 22 cells = 176 mosaic px long
hor = ndimage.binary_erosion(dark, structure=np.ones((1, K), bool))
hor = ndimage.binary_dilation(hor, structure=np.ones((1, K), bool))
ver = ndimage.binary_erosion(dark, structure=np.ones((K, 1), bool))
ver = ndimage.binary_dilation(ver, structure=np.ones((K, 1), bool))
print("hor px", int(hor.sum()), "ver px", int(ver.sum()))

# the rows/columns with the most line pixels
hsum = hor.sum(axis=1)
vsum = ver.sum(axis=0)
print("\nhorizontal lines with count>80:")
prev = -9
for y in np.argsort(hsum)[::-1]:
    if hsum[y] <= 80:
        break
    if y - prev <= 2 and prev > 0:
        prev = y
        continue
    print("   y %4d (%6d mosaic)  %d" % (y, y * DS, hsum[y]))
    prev = y
print("\nvertical lines with count>80:")
prev = -9
for x in np.argsort(vsum)[::-1]:
    if vsum[x] <= 80:
        break
    if x - prev <= 2 and prev > 0:
        prev = x
        continue
    print("   x %4d (%6d mosaic)  %d" % (x, x * DS, vsum[x]))
    prev = x

# horizontal extent of each strong line: where do the runs sit?
print("\nextent of selected lines (first/last col with line px):")
for y in (1751, 723, 1610, 681):
    xs = np.where(hor[y])[0]
    if len(xs):
        print("   h-line y=%4d (%6d): x %4d..%4d  (mosaic %6d..%6d), cells %d"
              % (y, y * DS, xs.min(), xs.max(), xs.min() * DS, xs.max() * DS, len(xs)))
for x in (1814, 897, 888):
    ys = np.where(ver[:, x])[0]
    if len(ys):
        print("   v-line x=%4d (%6d): y %4d..%4d  (mosaic %6d..%6d), cells %d"
              % (x, x * DS, ys.min(), ys.max(), ys.min() * DS, ys.max() * DS, len(ys)))
