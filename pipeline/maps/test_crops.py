"""The trace crop must turn the lettering so that it reads left to right, upright.

    python pipeline/maps/test_crops.py

The traced line is the BASELINE of the lettering.  A synthetic image carries a
"text" block (green) standing on the baseline: it rises `h` above it (along
"up", the left-hand perpendicular of the reading direction) and has a small
descender below.  A red marker sits at the start of the block, a blue one at
its end.  The line is drawn at several angles; after the crop the whole block
must lie inside the crop, in its upper part relative to the baseline, with the
start marker on the left.
"""
import math
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
from import_labels import crop_point, crop_trace, load_image, split_lines

W = 1200
H = 40              # the letters' height above the baseline
DESCENT = 10        # the block's descender, within the 0.35 * H the crop allows
L = 300


def frame(angle_deg):
    th = math.radians(angle_deg)
    ux, uy = math.cos(th), math.sin(th)         # reading direction
    upx, upy = uy, -ux                          # up, as in the page: (dy, -dx)
    return ux, uy, upx, upy


def draw_line(d, ux, uy, upx, upy, base, mark_start, mark_end):
    """One line of 'text': base = (x, y) of the line's middle on the baseline."""
    def pt(t, u):   # t along the reading direction, u above the baseline
        return (base[0] + t * ux + u * upx, base[1] + t * uy + u * upy)
    t0, t1 = -L / 2 + 20, L / 2 - 20
    d.polygon([pt(t0, -DESCENT), pt(t1, -DESCENT), pt(t1, H), pt(t0, H)], fill=(0, 160, 0))
    d.line([pt(-L / 2, 0), pt(L / 2, 0)], fill="black", width=4)
    if mark_start:
        x, y = pt(t0 + 12, H / 2)
        d.rectangle([x - 5, y - 5, x + 5, y + 5], fill=(255, 0, 0))
    if mark_end:
        x, y = pt(t1 - 12, H / 2)
        d.rectangle([x - 5, y - 5, x + 5, y + 5], fill=(0, 0, 255))
    return pt(-L / 2, 0), pt(L / 2, 0)


def synthetic(angle_deg, path):
    img = Image.new("RGB", (W, W), "white")
    d = ImageDraw.Draw(img)
    ux, uy, upx, upy = frame(angle_deg)
    p0, p1 = draw_line(d, ux, uy, upx, upy, (W / 2, W / 2), True, True)
    img.save(path)
    return [[int(p0[0]), int(p0[1])], [int(p1[0]), int(p1[1])]], H


def synthetic_two(angle_deg, path):
    """Two lines, the second below the first in the text's frame; red at line 1's
    start, blue at line 2's end."""
    img = Image.new("RGB", (W, W), "white")
    d = ImageDraw.Draw(img)
    ux, uy, upx, upy = frame(angle_deg)
    off = 50
    c = W / 2
    b1 = (c + off * upx, c + off * upy)         # line 1 is higher (further along up)
    b2 = (c - off * upx, c - off * upy)
    l1s, l1e = draw_line(d, ux, uy, upx, upy, b1, True, False)
    l2s, l2e = draw_line(d, ux, uy, upx, upy, b2, False, True)
    img.save(path)
    return [[int(p[0]), int(p[1])] for p in (l1s, l1e, l2s, l2e)], H


def array_of(im):
    return np.ndarray(buffer=im.write_to_memory(), dtype=np.uint8,
                      shape=(im.height, im.width, im.bands))


def masks(a):
    green = (a[..., 1] > 120) & (a[..., 0] < 80) & (a[..., 2] < 80)
    red = (a[..., 0] > 200) & (a[..., 1] < 60) & (a[..., 2] < 60)
    blue = (a[..., 2] > 200) & (a[..., 0] < 60) & (a[..., 1] < 60)
    black = (a.max(axis=2) < 70)
    return green, red, blue, black


def centroid(mask):
    ys, xs = np.nonzero(mask)
    assert len(xs) > 20, "marker lost"
    return xs.mean(), ys.mean()


def check_block(label, src_path, out, expect_two=False):
    a = array_of(out)
    green, red, blue, black = masks(a)
    sgreen = masks(np.array(Image.open(src_path).convert("RGB")))[0]
    n_src, n_out = int(sgreen.sum()), int(green.sum())
    assert 0.95 * n_src <= n_out <= 1.05 * n_src, \
        f"{label}: the block is cut by the crop ({n_out} of {n_src} marker pixels)"
    ys, xs = np.nonzero(green)
    assert xs.min() >= 2 and ys.min() >= 2 and xs.max() <= out.width - 3 and ys.max() <= out.height - 3, \
        f"{label}: the block touches the crop's edge"
    rx, ry = centroid(red)
    bx, by = centroid(blue)
    assert rx < out.width / 2 < bx, f"{label}: start not left of end ({rx:.0f}, {bx:.0f} of {out.width})"
    bys = np.nonzero(black)[0]
    assert len(bys) > 50, f"{label}: baseline lost"
    top_base, bot_base = bys.min(), bys.max()
    # the letters stand above the baseline: the block's top is about H above it
    assert top_base - ys.min() > 0.8 * H, f"{label}: block not above the baseline ({top_base - ys.min()})"
    if expect_two:
        assert by - ry > 70, f"{label}: lines not separated ({ry:.0f}, {by:.0f})"
        assert ry < out.height / 2 < by, f"{label}: red not upper, blue not lower"
        # the crop's top is above the first block and its bottom below the last descender
        assert ys.max() > bot_base, f"{label}: no descender below the last baseline"
    else:
        assert abs(ry - by) < 6, f"{label}: markers not on one horizontal line"
        assert ys.max() > bot_base, f"{label}: no descender below the baseline"
        # the block (centroid) lies in the upper part of the crop, above the baseline
        gy = ys.mean()
        assert gy < top_base, f"{label}: block's centre not above the baseline"
        assert top_base < out.height * 0.75, f"{label}: baseline not in the lower part of the crop"
        assert out.width > out.height, f"{label}: crop not wider than tall"
    return rx, bx, ry, by


def main():
    tmp = Path(tempfile.mkdtemp())
    for ang in (0, 30, 180, 250):
        p = tmp / f"s{ang}.png"
        trace, h = synthetic(ang, p)
        out = crop_trace(load_image(str(p)), trace, h)
        rx, bx, _, _ = check_block(f"angle {ang}", p, out)
        print(f"angle {ang:3d}: crop {out.width} x {out.height}, start x={rx:.0f}, end x={bx:.0f}  ok")
    real = [[9457, 3110], [8809, 2962], [9233, 2880], [8696, 2754]]
    ls = split_lines(real)
    assert [len(x) for x in ls] == [2, 2], f"real example split into {[len(x) for x in ls]}"
    assert len(split_lines([[0, 0], [100, 10], [190, 50]])) == 1, "curved trace was split"
    assert [len(x) for x in split_lines(real, [3])] == [3, 1], "explicit breaks ignored"
    print("split_lines ok")
    for ang in (0, 30, 180, 250):
        p = tmp / f"t{ang}.png"
        trace, h = synthetic_two(ang, p)
        out = crop_trace(load_image(str(p)), trace, h)
        rx, bx, ry, by = check_block(f"two lines, angle {ang}", p, out, expect_two=True)
        assert abs(by - ry - 100) < 40, f"two lines, angle {ang}: crop tilted ({by - ry:.0f})"
        print(f"two lines, angle {ang:3d}: crop {out.width} x {out.height}, red ({rx:.0f},{ry:.0f}), blue ({bx:.0f},{by:.0f})  ok")
    c = crop_point(load_image(str(tmp / "s0.png")), [600, 600], 180)
    assert (c.width, c.height) == (400, 400)
    print("point crop ok")
    print("PASSED")


main()
