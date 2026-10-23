"""The trace crop must turn the lettering so that it reads left to right.

    python pipeline/maps/test_crops.py

A synthetic image carries a red marker at the start of a line and a blue one
at its end; the line is drawn at several angles; after the crop the red marker
must be in the left half and the blue one right of it, on one horizontal line.
"""
import math
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
from import_labels import crop_point, crop_trace, load_image


def synthetic(angle_deg, path):
    W = 1200
    img = Image.new("RGB", (W, W), "white")
    d = ImageDraw.Draw(img)
    c = W / 2
    th = math.radians(angle_deg)
    L, h = 300, 40
    p0 = (c - L / 2 * math.cos(th), c - L / 2 * math.sin(th))
    p1 = (c + L / 2 * math.cos(th), c + L / 2 * math.sin(th))
    d.line([p0, p1], fill="black", width=6)
    d.rectangle([p0[0] - 12, p0[1] - 12, p0[0] + 12, p0[1] + 12], fill=(255, 0, 0))
    d.rectangle([p1[0] - 12, p1[1] - 12, p1[0] + 12, p1[1] + 12], fill=(0, 0, 255))
    img.save(path)
    return [[int(p0[0]), int(p0[1])], [int(p1[0]), int(p1[1])]], h


def centroid(mask):
    ys, xs = np.nonzero(mask)
    assert len(xs) > 20, "marker lost"
    return xs.mean(), ys.mean()


def main():
    tmp = Path(tempfile.mkdtemp())
    for ang in (0, 30, 90, 180, 250):
        p = tmp / f"s{ang}.png"
        trace, h = synthetic(ang, p)
        out = crop_trace(load_image(str(p)), trace, h)
        a = np.ndarray(buffer=out.write_to_memory(), dtype=np.uint8,
                       shape=(out.height, out.width, out.bands))
        red = (a[..., 0] > 200) & (a[..., 1] < 60) & (a[..., 2] < 60)
        blue = (a[..., 2] > 200) & (a[..., 0] < 60) & (a[..., 1] < 60)
        rx, ry = centroid(red)
        bx, by = centroid(blue)
        assert rx < out.width / 2 < bx, f"angle {ang}: start not left of end ({rx:.0f}, {bx:.0f} of {out.width})"
        assert abs(ry - by) < 6, f"angle {ang}: markers not on one horizontal line"
        assert out.width > out.height, f"angle {ang}: crop not wider than tall"
        print(f"angle {ang:3d}: crop {out.width} x {out.height}, start x={rx:.0f}, end x={bx:.0f}  ok")
    c = crop_point(load_image(str(tmp / "s0.png")), [600, 600], 180)
    assert (c.width, c.height) == (400, 400)
    print("point crop ok")
    print("PASSED")


main()
