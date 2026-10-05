# -*- coding: utf-8 -*-
"""How the numbers in stitch.json were found: for each page photographed in
two overlapping halves, how the bottom photograph lies on the top one, where
the two can be joined without touching a line of writing, and how much
brighter or darker the bottom one is.

    python units/iharep162nr295/intake/find_stitch.py              # report only
    python units/iharep162nr295/intake/find_stitch.py --write      # write stitch.json
    python units/iharep162nr295/intake/find_stitch.py --preview D  # joined pages into folder D,
                                                                   # seam drawn in red

Not part of the pipeline, and the only script here that needs OpenCV and
NumPy (`pip install opencv-python-headless numpy`, best in an environment of
its own). build_pages.py applies what this finds with Pillow alone. Run this
again only to join different photographs or to move a seam; then run
build_pages.py --crop and look at every page.

For each pair:

  1. Points the two photographs share are found (SIFT) and matched; a
     homography is fitted to them (MAGSAC, 3 pixels). The page is not quite
     flat, so about half the matches fit; `check` records how many and how
     closely.
  2. The seam is looked for in the middle 60 per cent of what both
     photographs show, between the left and right edges of the paper. Ink is
     whatever is darker than the paper around it, in either photograph; the
     seam is the path from one side to the other that costs least, where ink
     costs much, every step up or down costs a little, and so does distance
     from the middle of the band. It therefore runs straight along a gap
     between two lines and leaves it only to go round a descender.
  3. The gain is the ratio of the paper's colour in the two photographs beside
     the seam, in 24 columns across the width, smoothed.
"""
import io
import json
import os
import sys

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(UNIT_DIR))
sys.path.insert(0, ROOT)
import unitlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SLUG = 'iharep162nr295'
BAND = (0.20, 0.80)      # the part of the overlap the seam may run in
GAIN_COLUMNS = 24
PAPER = 150              # a pixel this bright in every channel is paper


def imread(path):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)


def homography(top, bottom):
    """Bottom photograph -> top photograph, and how well the matches fit."""
    sift = cv2.SIFT_create(nfeatures=20000)
    kt, dt = sift.detectAndCompute(cv2.cvtColor(top, cv2.COLOR_BGR2GRAY), None)
    kb, db = sift.detectAndCompute(cv2.cvtColor(bottom, cv2.COLOR_BGR2GRAY), None)
    pairs = cv2.BFMatcher(cv2.NORM_L2).knnMatch(db, dt, k=2)
    good = [a for a, b in pairs if a.distance < 0.7 * b.distance]
    pb = np.float32([kb[g.queryIdx].pt for g in good])
    pt = np.float32([kt[g.trainIdx].pt for g in good])
    H, mask = cv2.findHomography(pb, pt, cv2.USAC_MAGSAC, 3.0, maxIters=20000,
                                 confidence=0.9999)
    fit = mask.ravel().astype(bool)
    proj = cv2.perspectiveTransform(pb[fit].reshape(-1, 1, 2), H).reshape(-1, 2)
    return H, np.linalg.norm(proj - pt[fit], axis=1)


def cheapest_path(cost, step_price=0.6):
    """One row per column, from the left edge to the right, moving at most one
    row between neighbouring columns."""
    h, w = cost.shape
    acc = cost.astype(np.float64).copy()
    back = np.zeros((h, w), dtype=np.int8)
    for x in range(1, w):
        prev = acc[:, x - 1]
        best, arg = prev.copy(), np.zeros(h, dtype=np.int8)
        up = np.concatenate(([np.inf], prev[:-1])) + step_price
        down = np.concatenate((prev[1:], [np.inf])) + step_price
        best, arg = np.where(up < best, up, best), np.where(up < best, -1, arg)
        best, arg = np.where(down < best, down, best), np.where(down < best, 1, arg)
        acc[:, x] += best
        back[:, x] = arg
    y = int(np.argmin(acc[:, -1]))
    path = [y]
    for x in range(w - 1, 0, -1):
        y += int(back[y, x])
        path.append(y)
    return path[::-1]


def ink(gray):
    """How much darker each pixel is than the paper around it."""
    smooth = cv2.GaussianBlur(gray, (0, 0), 2)
    paper = cv2.morphologyEx(smooth, cv2.MORPH_CLOSE,
                             cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (61, 61)))
    return np.clip(paper - gray - 14, 0, None)


def find(top, bottom):
    h, w = top.shape[:2]
    H, errors = homography(top, bottom)
    corners = cv2.perspectiveTransform(
        np.float32([[0, 0], [w, 0], [w, h], [0, h]]).reshape(-1, 1, 2), H).reshape(-1, 2)
    canvas_h = int(min(corners[2][1], corners[3][1]))
    laid = cv2.warpPerspective(bottom, H, (w, canvas_h), flags=cv2.INTER_CUBIC)

    # the band the seam may run in, and the columns the paper fills there
    first, last = int(max(corners[0][1], corners[1][1])), h
    b0 = int(first + BAND[0] * (last - first))
    b1 = int(first + BAND[1] * (last - first))
    gt = cv2.cvtColor(top[b0:b1], cv2.COLOR_BGR2GRAY).astype(np.float32)
    gl = cv2.cvtColor(laid[b0:b1], cv2.COLOR_BGR2GRAY).astype(np.float32)
    cols = np.flatnonzero(((gt > PAPER).mean(axis=0) > 0.6) & ((gl > PAPER).mean(axis=0) > 0.6))
    x0, x1 = int(cols[0]) + 40, int(cols[-1]) - 40

    q = 4                                                    # worked at quarter size
    cost = cv2.GaussianBlur(np.maximum(ink(gt), ink(gl)), (0, 0), 7)
    cost = cv2.resize(cost[:, x0:x1], ((x1 - x0) // q, (b1 - b0) // q),
                      interpolation=cv2.INTER_AREA) ** 2 + 0.02
    cost += 0.01 * np.linspace(-1, 1, cost.shape[0])[:, None] ** 2
    path = cheapest_path(cost)
    near_ink = float(np.mean(cost[path, np.arange(cost.shape[1])] > 1.0))
    pts = [(x0 + q * i, b0 + q * y + q // 2) for i, y in enumerate(path)]
    pts = pts[::24] + [pts[-1]]
    seam = [(0, pts[0][1])] + pts + [(w, pts[-1][1])]
    seam = [[int(x), int(y)] for x, y in seam]

    # the gain, column by column, on the paper beside the seam
    sx, sy = [p[0] for p in seam], [p[1] for p in seam]
    prof = np.full((GAIN_COLUMNS, 3), np.nan)
    for i in range(GAIN_COLUMNS):
        c0, c1 = int(i * w / GAIN_COLUMNS), int((i + 1) * w / GAIN_COLUMNS)
        cy = int(np.interp((c0 + c1) / 2, sx, sy))
        a = top[cy - 140:cy + 140, c0:c1].reshape(-1, 3).astype(np.float32)
        b = laid[cy - 140:cy + 140, c0:c1].reshape(-1, 3).astype(np.float32)
        paper = (a.min(axis=1) > PAPER) & (b.min(axis=1) > PAPER)
        if c0 >= x0 - 40 and c1 <= x1 + 40 and paper.mean() > 0.6:
            prof[i] = (np.median(a[paper], axis=0) / np.median(b[paper], axis=0))[::-1]   # R, G, B
    measured = ~np.isnan(prof[:, 0])
    idx = np.arange(GAIN_COLUMNS)
    for c in range(3):
        v = np.interp(idx, idx[measured], prof[measured, c])      # ends held, gaps bridged
        prof[:, c] = np.convolve(np.pad(v, 1, mode='edge'), [0.25, 0.5, 0.25], mode='valid')

    # Pillow counts a pixel's edges as whole numbers, OpenCV its middle
    shift = np.array([[1, 0, .5], [0, 1, .5], [0, 0, 1.]])
    M = shift @ np.linalg.inv(H) @ np.linalg.inv(shift)
    M /= M[2, 2]
    rec = {
        'canvas': [w, canvas_h],
        'coeffs': [float(f'{v:.12g}') for v in M.ravel()[:8]],
        'seam': seam,
        'gain_r': [round(float(v), 4) for v in prof[:, 0]],
        'gain_g': [round(float(v), 4) for v in prof[:, 1]],
        'gain_b': [round(float(v), 4) for v in prof[:, 2]],
        'check': {'matched_points': int(len(errors)),
                  'median_error_px': round(float(np.median(errors)), 2),
                  'p95_error_px': round(float(np.percentile(errors, 95)), 2),
                  'seam_near_ink': round(near_ink, 4)},
    }
    return rec, laid


def preview(top, laid, rec, path):
    w, h = rec['canvas']
    gain = cv2.resize(np.float32([rec['gain_b'], rec['gain_g'], rec['gain_r']]).T[None].copy(),
                      (w, 1), interpolation=cv2.INTER_LINEAR)
    laid = np.clip(laid.astype(np.float32) * gain, 0, 255)
    below = np.zeros((h, w), np.uint8)
    cv2.fillPoly(below, [np.array(rec['seam'] + [[w, h], [0, h]], np.int32)], 255)
    below = cv2.GaussianBlur(below, (0, 0), 6).astype(np.float32)[:, :, None] / 255
    page = np.zeros((h, w, 3), np.float32)
    page[:top.shape[0]] = top
    page = (page * (1 - below) + laid * below).astype(np.uint8)
    cv2.polylines(page, [np.array(rec['seam'], np.int32)], False, (0, 0, 255), 3)
    cv2.imencode('.jpg', page, [cv2.IMWRITE_JPEG_QUALITY, 85])[1].tofile(path)


def main():
    unit = unitlib.one_unit(SLUG)
    photos = sorted(f for f in os.listdir(unit.raw_dir) if f.startswith('PXL_'))
    if len(photos) != 23:
        sys.exit(f'expected 23 photographs in {unit.raw_dir}, found {len(photos)}')
    out_dir = sys.argv[sys.argv.index('--preview') + 1] if '--preview' in sys.argv else None
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    # the first photograph is the cover; then top, bottom, top, bottom ...
    out = {}
    for n, i in enumerate(range(1, 23, 2), 2):
        pid = f'{n:04d}_a'
        top = imread(os.path.join(unit.raw_dir, photos[i]))
        bottom = imread(os.path.join(unit.raw_dir, photos[i + 1]))
        rec, laid = find(top, bottom)
        out[pid] = {'top': photos[i], 'bottom': photos[i + 1], **rec}
        print(f"  {pid}  {photos[i]} + {photos[i + 1]}  {rec['check']}", flush=True)
        if out_dir:
            preview(top, laid, rec, os.path.join(out_dir, pid + '.jpg'))

    if '--write' in sys.argv:
        lines = ['{']
        for i, (pid, rec) in enumerate(out.items()):
            lines.append(f' "{pid}": {{')
            keys = list(rec)
            for j, k in enumerate(keys):
                lines.append(f'  "{k}": {json.dumps(rec[k])}' + (',' if j < len(keys) - 1 else ''))
            lines.append(' }' + (',' if i < len(out) - 1 else ''))
        lines.append('}')
        with open(os.path.join(HERE, 'stitch.json'), 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(lines) + '\n')
        print('wrote stitch.json')


if __name__ == '__main__':
    main()
