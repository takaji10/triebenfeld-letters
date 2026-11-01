# Probe: what does "black ink" look like where we already read black
# tokens? Stats of luminance inside known black-token boxes vs the
# building/forest fills, to choose a threshold that separates ink.
import numpy as np
import pyvips

FULL = r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456\4456_full.jpg"
im = pyvips.Image.new_from_file(FULL, access="random")

PROBES = [
    ("tok 7   7677,6501", 7677, 6501, 28, 32),
    ("tok 3   7599,5438", 7599, 5438, 34, 28),
    ("tok 360 18832,8566", 18832, 8566, 131, 99),
    ("tok 266 18614,8590", 18614, 8590, 142, 103),
    ("tok 837 4632,6457", 4632, 6457, 68, 48),
]
for name, x, y, w, h in PROBES:
    a = np.frombuffer(im.crop(x - 10, y - 10, w + 20, h + 20).write_to_memory(),
                      np.uint8).reshape(h + 20, w + 20, 3).astype(int)
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    lum = (R * 299 + G * 587 + B * 114) // 1000
    chroma = np.max(a, axis=2) - np.min(a, axis=2)
    print("%-20s lum p1/p5/p25/p50 = %3d/%3d/%3d/%3d   chroma p50/p95 = %2d/%2d"
          % (name, np.percentile(lum, 1), np.percentile(lum, 5),
             np.percentile(lum, 25), np.percentile(lum, 50),
             np.percentile(chroma, 50), np.percentile(chroma, 95)))

# fills for comparison: a building block, forest, arable (sample regions)
FILLS = [("buildings fill", 12000, 6000), ("forest fill", 4000, 9000),
         ("arable fill", 8000, 4000)]
for name, x, y in FILLS:
    a = np.frombuffer(im.crop(x, y, 300, 300).write_to_memory(),
                      np.uint8).reshape(300, 300, 3).astype(int)
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    lum = (R * 299 + G * 587 + B * 114) // 1000
    chroma = np.max(a, axis=2) - np.min(a, axis=2)
    print("%-20s lum p1/p5/p25/p50 = %3d/%3d/%3d/%3d   chroma p50/p95 = %2d/%2d"
          % (name, np.percentile(lum, 1), np.percentile(lum, 5),
             np.percentile(lum, 25), np.percentile(lum, 50),
             np.percentile(chroma, 50), np.percentile(chroma, 95)))
