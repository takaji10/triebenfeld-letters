# What is the paper's colour, and the washes'? Probe known regions, then
# set the fill threshold from the paper's own chroma distribution.
import numpy as np
import pyvips

FULL = (r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)"
        r"\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456\4456_full.jpg")
im = pyvips.Image.new_from_file(FULL, access="random")

def stats(name, x, y, w, h):
    a = np.frombuffer(im.crop(x, y, w, h).write_to_memory(),
                      np.uint8).reshape(h, w, 3).astype(int)
    R = a[:, :, 0]; G = a[:, :, 1]; B = a[:, :, 2]
    lum = (R * 299 + G * 587 + B * 114) // 1000
    chroma = np.maximum(np.maximum(R, G), B) - np.minimum(np.minimum(R, G), B)
    print("%-22s RGB mean %3d/%3d/%3d  lum p10/p50/p90 %3d/%3d/%3d  chroma p50/p90/p99 %2d/%2d/%2d"
          % (name, R.mean(), G.mean(), B.mean(),
             np.percentile(lum, 10), np.percentile(lum, 50), np.percentile(lum, 90),
             np.percentile(chroma, 50), np.percentile(chroma, 90),
             np.percentile(chroma, 99)))
    return chroma

paper = stats("explication block", 5200, 1000, 500, 400)
paper2 = stats("title block area", 1000, 1100, 600, 500)
stats("adjoining-lands list", 500, 4000, 400, 600)
stats("arable parcel", 8000, 4000, 300, 300)
stats("forest", 4000, 9000, 300, 300)
stats("meadow", 11000, 5000, 300, 300)
print("paper chroma pooled p95: %.1f" %
      np.percentile(np.concatenate([paper.ravel(), paper2.ravel()]), 95))
