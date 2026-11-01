# Can ink texture separate the information blocks from the drawn map?
# Labeled points: known info-block numbers (explication, title block, the
# sheet-1 text zones) vs known drawn-map numbers (the proved farm parcels).
# Measure the dark-fraction in windows of several sizes around each.
import numpy as np
import pyvips

FULL = (r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)"
        r"\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456\4456_full.jpg")
im = pyvips.Image.new_from_file(FULL, access="random")
DS = 4
small = im.resize(1.0 / DS)
a = np.frombuffer(small.write_to_memory(), np.uint8).reshape(
    small.height, small.width, 3).astype(int)
R = a[:, :, 0]; G = a[:, :, 1]; B = a[:, :, 2]
lum = (R * 299 + G * 587 + B * 114) // 1000
dark = lum < 125
print("dark px overall: %.2f%%" % (100 * dark.mean()))

INFO = [
    ("explication 1454", 5338, 1286), ("explication 1883", 5335, 1483),
    ("explication 335", 5379, 1559), ("explication 219", 5373, 1071),
    ("title 1896 a", 952, 1352), ("title 1896 b", 3064, 1750),
    ("sheet1 11 a", 1570, 1476), ("sheet1 11 b", 2592, 1766),
    ("sheet1 47", 1260, 1880), ("sheet1 14", 4683, 1505),
]
MAP_ = [
    ("farm78", 3847, 6371), ("farm49", 5423, 8654), ("farm84 stack", 4751, 5713),
    ("farm11 east", 17769, 11984), ("farm50 a", 5974, 10546),
    ("farm92", 9504, 9896), ("farm86", 6970, 5153), ("farm88", 19978, 12188),
    ("farm64", 18798, 12315), ("farm54", 19612, 10949),
]
for win_mosaic in (240, 360, 500):
    w = win_mosaic // DS // 2
    print("\nwindow %d px (mosaic):" % win_mosaic)
    for tag, xs in (("INFO", INFO), ("MAP ", MAP_)):
        vals = []
        for name, x, y in xs:
            cx, cy = x // DS, y // DS
            box = dark[max(0, cy - w):cy + w, max(0, cx - w):cx + w]
            vals.append(100 * box.mean())
        print("  %s: %s" % (tag, "  ".join("%s %.1f" % (n.split()[0], v)
                                           for (n, _, _), v in zip(xs, vals))))
        print("    min %.1f max %.1f" % (min(vals), max(vals)))
