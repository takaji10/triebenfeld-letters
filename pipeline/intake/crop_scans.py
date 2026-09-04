"""
Detects the dark gutter/background in each two-up archival scan and crops out
each individual document side, at full native resolution.

No numpy dependency (not installed in this environment) - uses Pillow's
pixel access objects directly, on a small downsampled copy for speed.

Usage:
    python crop_scans.py                  # process all *.jpg in parent dir
    python crop_scans.py --limit 8         # process only the first N scans
    python crop_scans.py --debug 0001      # print detection details for one scan
"""

import argparse
import json
from pathlib import Path
from PIL import Image

import os as _os, sys as _sys
# run directly from two levels down; make the project root importable
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))
import unitlib

# The scans live outside the project. Which unit to work on comes from
# --unit <slug>, and where its images are from that unit's unit.yml.
UNIT = unitlib.one_unit(unitlib.unit_arg())
ROOT = Path(UNIT.raw_dir)
if not ROOT.is_dir():
    raise SystemExit(f'{UNIT.slug}: scans.raw_dir does not exist: {ROOT}')
PROCESSED_DIR = ROOT / "processed"
MANIFEST_PATH = PROCESSED_DIR / "manifest.json"

ANALYSIS_WIDTH = 300          # downsample width for gutter/bbox detection
BRIGHT_THRESHOLD = 100         # grayscale value above which a pixel counts as "paper"
MIN_RUN_FRACTION = 0.06        # a content run must span at least this fraction of width to count as a document
PAD_FRACTION = 0.01            # padding added around each detected bbox, as a fraction of that dimension
JPEG_QUALITY = 97               # crops are kept at full native resolution, no downsizing


def load_small_grayscale(img: Image.Image):
    w, h = img.size
    scale = ANALYSIS_WIDTH / w
    small = img.convert("L").resize((ANALYSIS_WIDTH, max(1, round(h * scale))))
    return small, scale


def column_brightness(small: Image.Image):
    px = small.load()
    w, h = small.size
    cols = []
    for x in range(w):
        total = 0
        for y in range(h):
            total += px[x, y]
        cols.append(total / h)
    return cols


def row_brightness(small: Image.Image, x0: int, x1: int):
    px = small.load()
    h = small.height
    rows = []
    for y in range(h):
        total = 0
        for x in range(x0, x1):
            total += px[x, y]
        rows.append(total / max(1, (x1 - x0)))
    return rows


def find_content_runs(brightness, min_len):
    """Return list of (start, end) index ranges where brightness stays above threshold."""
    runs = []
    start = None
    for i, v in enumerate(brightness + [0]):  # sentinel to close trailing run
        is_bright = v > BRIGHT_THRESHOLD
        if is_bright and start is None:
            start = i
        elif not is_bright and start is not None:
            if i - start >= min_len:
                runs.append((start, i))
            start = None
    return runs


def detect_documents(img: Image.Image):
    """Return list of bounding boxes (in original image coordinates) for each
    document detected in the scan."""
    small, scale = load_small_grayscale(img)
    w, h = small.size

    col_b = column_brightness(small)
    min_run = max(1, round(w * MIN_RUN_FRACTION))
    col_runs = find_content_runs(col_b, min_run)

    if not col_runs:
        # Fallback: treat the whole image as a single document.
        return [(0, 0, img.width, img.height)]

    boxes = []
    for (cx0, cx1) in col_runs:
        row_b = row_brightness(small, cx0, cx1)
        min_run_row = max(1, round(h * MIN_RUN_FRACTION))
        row_runs = find_content_runs(row_b, min_run_row)
        if not row_runs:
            continue
        ry0 = min(r[0] for r in row_runs)
        ry1 = max(r[1] for r in row_runs)

        # map back to original coordinates
        ox0, ox1 = cx0 / scale, cx1 / scale
        oy0, oy1 = ry0 / scale, ry1 / scale

        pad_x = (ox1 - ox0) * PAD_FRACTION
        pad_y = (oy1 - oy0) * PAD_FRACTION
        ox0 = max(0, ox0 - pad_x)
        ox1 = min(img.width, ox1 + pad_x)
        oy0 = max(0, oy0 - pad_y)
        oy1 = min(img.height, oy1 + pad_y)

        boxes.append((round(ox0), round(oy0), round(ox1), round(oy1)))

    return boxes if boxes else [(0, 0, img.width, img.height)]


def process_scan(path: Path, debug=False):
    img = Image.open(path).convert("RGB")
    boxes = detect_documents(img)
    suffix = "abcdefgh"
    crops = []
    for i, box in enumerate(boxes):
        crop = img.crop(box)
        out_name = f"{path.stem}_{suffix[i]}.jpg"
        out_path = PROCESSED_DIR / out_name
        crop.save(out_path, quality=JPEG_QUALITY)
        crops.append({
            "file": out_name,
            "bbox_original": list(box),
            "size": list(crop.size),
        })
        if debug:
            print(f"  {out_name}: bbox={box} -> size={crop.size}")
    return crops


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--unit", required=True, help="unit slug, e.g. oe1bu9454")
    ap.add_argument("--limit", type=int, default=None, help="only process the first N scans")
    ap.add_argument("--debug", type=str, default=None, help="debug a single scan by its 4-digit number, e.g. 0001")
    args = ap.parse_args()

    PROCESSED_DIR.mkdir(exist_ok=True)

    # The filename pattern is the unit's, not this script's.
    scans = sorted(ROOT.glob(UNIT.raw_glob))
    if not scans:
        raise SystemExit(f'no scans matching {UNIT.raw_glob!r} in {ROOT}')
    if args.debug:
        scans = [s for s in scans if args.debug in s.stem]
    elif args.limit:
        scans = scans[: args.limit]

    manifest = {}
    if MANIFEST_PATH.exists():
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    for path in scans:
        print(f"Processing {path.name} ...")
        crops = process_scan(path, debug=bool(args.debug))
        manifest[path.name] = crops

    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote manifest for {len(scans)} scan(s) -> {MANIFEST_PATH}")


if __name__ == "__main__":
    main()
