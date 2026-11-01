# First look at the numbers on Pełzucki 1896: an overview of the mosaic and a
# few mid-scale crops, to see what the black and red figures are.
import pyvips

FULL = r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456\4456_full.jpg"
OUT = r"C:\Users\Tersnaus\AppData\Local\Temp\opencode\p1896"
im = pyvips.Image.new_from_file(FULL, access="random")
print("size", im.width, im.height, "bands", im.bands)
im.resize(3200 / im.width).write_to_file(OUT + "_overview.jpg[Q=88]")

# four quadrants at ~1/3 scale for reading big figures
W, H = im.width, im.height
regions = {
    "nw": (0, 0, W // 2, H // 2),
    "ne": (W // 2, 0, W // 2, H // 2),
    "sw": (0, H // 2, W // 2, H // 2),
    "se": (W // 2, H // 2, W // 2, H // 2),
}
for name, (l, t, w, h) in regions.items():
    im.crop(l, t, w, h).resize(1600 / w).write_to_file(f"{OUT}_{name}.jpg[Q=88]")
