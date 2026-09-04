"""
Second-stage splitter for the processed crops.

crop_scans.py split each scan on the dark scanner gutter between physically
separate documents. That misses the bifolium-photographed-open case: two pages
joined only by a centre fold, kept as one wide crop. This script cuts those wide
crops in two, at the fold line (a low-ink vertical valley very near the centre),
never through text.

Aspect ratio (AR = width / height) picks the candidates:
    AR >= 1.5            -> --auto : split straight away
    1.12 <= AR < 1.5     -> --review : render a proof sheet first, then
                            --apply-review the rows you mark `split`
    AR < 1.12            -> single leaf, left alone

In every genuine bifolium inspected, the middle ~10% of the width is clear of
text (gutter + crease), so the cut column is searched only in [0.44, 0.56] of the
width and can never reach into a text block. The one case that must NOT be
auto-split is two *separate* sheets photographed overlapping past the centre;
that shows up as heavy ink straight through the centre and is diverted to the
review sheet instead.

Naming:  "<stem>_a.jpg"  ->  "<stem>_a1.jpg" (left) + "<stem>_a2.jpg" (right)
The untouched wide original is moved to processed/_spreads_unsplit/.
manifest.json is rewritten with the two half-entries in place of the parent.

Usage:
    python split_spreads.py --auto --dry-run
    python split_spreads.py --auto
    python split_spreads.py --review
    python split_spreads.py --apply-review processed/_spreads_review/INDEX.md
    python split_spreads.py --auto --only 0003
"""

import argparse
import json
import re
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

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
UNSPLIT_DIR = PROCESSED_DIR / "_spreads_unsplit"
REVIEW_DIR = PROCESSED_DIR / "_spreads_review"

# shared with crop_scans.py
ANALYSIS_WIDTH = 560          # downsample width for the ink / crease profiles
BRIGHT_THRESHOLD = 100         # grayscale value; below this a pixel counts as ink
JPEG_QUALITY = 97

AUTO_AR = 1.5                  # >= this -> auto-split
REVIEW_AR = 1.12              # [REVIEW_AR, AUTO_AR) -> review first

FOLD_LO, FOLD_HI = 0.40, 0.60          # fold search window, fraction of width
PAPER_BRIGHT = 150                      # grayscale value at/above which a pixel is bare paper
CREASE_HALF = 5                         # +/- columns for the local-minimum crease test
CREASE_DROP = 8                         # crease column must be this much darker than its local mean
CREASE_MIN = 0.10                       # crease streak strength below which no real fold line is
                                       #   visible -> fall back to centre of the clear channel
GUTTER_MIN = 0.55                       # if the clearest column in the window has less than this
                                       #   fraction of bare-paper rows, the centre is inked across
                                       #   (overlapping sheets) -> do not auto-split

CROP_RE = re.compile(r"^(.*_\d{4})_([a-h])$")


# --------------------------------------------------------------------------- #
# ink profile / fold detection
# --------------------------------------------------------------------------- #
def load_small_grayscale(img: Image.Image):
    w, h = img.size
    scale = ANALYSIS_WIDTH / w
    small = img.convert("L").resize((ANALYSIS_WIDTH, max(1, round(h * scale))))
    return small, scale


def column_ink(small: Image.Image):
    """Per-column count of ink (dark) pixels."""
    px = small.load()
    w, h = small.size
    cols = []
    for x in range(w):
        n = 0
        for y in range(h):
            if px[x, y] < BRIGHT_THRESHOLD:
                n += 1
        cols.append(n)
    return cols


def column_profiles(small: Image.Image):
    """Per-column, over the full height:
        gutter[x] - fraction of rows that are bare paper (>= PAPER_BRIGHT)
        crease[x] - fraction of rows where x is a thin local brightness minimum
                    (a fold crease casts a faint dark vertical streak)
    """
    px = small.load()
    w, h = small.size
    gutter = [0.0] * w
    crease = [0.0] * w
    for x in range(w):
        x0, x1 = max(0, x - CREASE_HALF), min(w, x + CREASE_HALF + 1)
        g = c = 0
        for y in range(h):
            b = px[x, y]
            if b >= PAPER_BRIGHT:
                g += 1
            loc = [px[xx, y] for xx in range(x0, x1)]
            if b <= min(loc) and b < (sum(loc) / len(loc)) - CREASE_DROP:
                c += 1
        gutter[x] = g / h
        crease[x] = c / h
    return gutter, crease


def moving_average(values, win):
    if win <= 1:
        return list(values)
    half = win // 2
    n = len(values)
    return [sum(values[max(0, i - half):min(n, i + half + 1)])
            / (min(n, i + half + 1) - max(0, i - half)) for i in range(n)]


def median(values):
    s = sorted(values)
    n = len(s)
    if n == 0:
        return 0.0
    return float(s[n // 2]) if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2.0


def detect_fold(img: Image.Image):
    """Locate the physical fold and return (fold_px_fullres, confidence, meta).

    The fold is NOT assumed to be at the image centre. Within the search window
    it is taken as the darkest crease streak among the columns that are clearest
    of ink (most bare-paper rows) - i.e. the fold line inside the gutter channel
    between the two written blocks, wherever that channel actually falls.

    confidence: "high"  - a distinct crease streak was found in a clear channel
                "low"   - channel is clear but the crease is faint (blank leaf /
                          flat gutter); the cut still lands in bare paper
                "reject"- no clear vertical channel in the window (the centre is
                          written across - overlapping sheets, not a bifolium)
    """
    small, scale = load_small_grayscale(img)
    w = small.size[0]

    raw = column_ink(small)
    gutter, crease = column_profiles(small)
    gutter = moving_average(gutter, 5)
    crease = moving_average(crease, 5)

    lo, hi = int(w * FOLD_LO), int(w * FOLD_HI)
    mid = w / 2
    g_max = max(gutter[lo:hi])

    if g_max < GUTTER_MIN:
        confidence = "reject"
        fold_x = min(range(lo, hi), key=lambda x: raw[x])   # best effort
        crease_val = crease[fold_x]
    else:
        # bare-paper columns; the true gutter is the WIDEST contiguous band of
        # them (an isolated clear column is a ruled line, not the fold)
        clear = [x for x in range(lo, hi) if gutter[x] >= 0.92 * g_max]
        runs, start = [], clear[0]
        for a, b in zip(clear, clear[1:] + [None]):
            if b is None or b != a + 1:
                runs.append((start, a))
                start = b
        band = max(runs, key=lambda r: (r[1] - r[0], -abs((r[0] + r[1]) / 2 - mid)))
        cols = range(band[0], band[1] + 1)
        crease_val = max(crease[x] for x in cols)
        if crease_val >= CREASE_MIN:
            # a real fold line inside the gutter band - honour where it falls
            fold_x = max(cols, key=lambda x: (crease[x], -abs(x - mid)))
            confidence = "high"
        else:
            # faint crease (blank leaf / flat gutter): cut at the band centre
            fold_x = (band[0] + band[1]) // 2
            confidence = "low"
        crease_val = crease[fold_x]

    left_ink = sum(raw[:fold_x])
    right_ink = sum(raw[fold_x:])
    weak = min(left_ink, right_ink)
    strong = max(left_ink, right_ink) or 1
    if weak <= 0.02 * (left_ink + right_ink or 1):
        content = "one side blank"
    elif weak <= 0.20 * strong:
        content = "one side sparse"
    else:
        content = "text both sides"

    meta = {
        "fold_frac": round(fold_x / w, 4),
        "gutter": round(gutter[fold_x], 2),
        "crease": round(crease_val, 2),
        "content": content,
    }
    return round(fold_x / scale), confidence, meta


def verdict_for(confidence, meta):
    if confidence in ("high", "low"):
        return "split"
    return "manual"     # reject


# --------------------------------------------------------------------------- #
# candidate discovery
# --------------------------------------------------------------------------- #
def crop_files():
    for p in sorted(PROCESSED_DIR.glob("*.jpg")):
        m = CROP_RE.match(p.stem)
        if m:
            yield p, m.group(1), m.group(2)   # path, scan-base, suffix


def already_done(base, suf):
    return ((PROCESSED_DIR / f"{base}_{suf}1.jpg").exists()
            or (UNSPLIT_DIR / f"{base}_{suf}.jpg").exists())


def candidates(mode, only=None):
    """mode: 'auto' or 'review'. Yields (path, base, suf, W, H, ar)."""
    for path, base, suf in crop_files():
        if only and only not in path.stem:
            continue
        with Image.open(path) as im:
            w, h = im.size
        ar = w / h
        if mode == "auto" and ar >= AUTO_AR:
            yield path, base, suf, w, h, ar
        elif mode == "review" and REVIEW_AR <= ar < AUTO_AR:
            yield path, base, suf, w, h, ar


# --------------------------------------------------------------------------- #
# manifest
# --------------------------------------------------------------------------- #
def load_manifest():
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return {}


def save_manifest(manifest):
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def update_manifest_entry(manifest, base, suf, fold_px, left_size, right_size, confidence):
    key = f"{base}.jpg"
    entries = manifest.get(key)
    parent_name = f"{base}_{suf}.jpg"

    parent_bbox, idx = None, None
    if entries:
        for i, e in enumerate(entries):
            if e.get("file") == parent_name:
                parent_bbox, idx = e.get("bbox_original"), i
                break

    if parent_bbox and len(parent_bbox) == 4:
        px0, py0, px1, py1 = parent_bbox
    else:
        px0, py0, px1, py1 = 0, 0, left_size[0] + right_size[0], left_size[1]

    l_entry = {
        "file": f"{base}_{suf}1.jpg",
        "bbox_original": [px0, py0, px0 + fold_px, py1],
        "size": list(left_size),
        "split_from": parent_name,
        "fold_confidence": confidence,
    }
    r_entry = {
        "file": f"{base}_{suf}2.jpg",
        "bbox_original": [px0 + fold_px, py0, px1, py1],
        "size": list(right_size),
        "split_from": parent_name,
        "fold_confidence": confidence,
    }

    if entries is None:
        manifest[key] = [l_entry, r_entry]
    elif idx is None:
        entries.extend([l_entry, r_entry])
    else:
        entries[idx:idx + 1] = [l_entry, r_entry]


# --------------------------------------------------------------------------- #
# proof rendering
# --------------------------------------------------------------------------- #
def _font():
    try:
        return ImageFont.load_default()
    except Exception:
        return None


def render_proof(img, fold_px, caption):
    REVIEW_DIR.mkdir(exist_ok=True)
    w, h = img.size
    scale = 1000 / w
    thumb = img.resize((1000, max(1, round(h * scale))))
    tw, th = thumb.size
    strip = 22
    canvas = Image.new("RGB", (tw, th + strip), (255, 255, 255))
    canvas.paste(thumb, (0, strip))
    draw = ImageDraw.Draw(canvas)
    fx = round(fold_px * scale)
    draw.line([(fx, strip), (fx, th + strip)], fill=(230, 0, 0), width=3)
    draw.text((4, 4), caption, fill=(0, 0, 0), font=_font())
    return canvas


# --------------------------------------------------------------------------- #
# splitting
# --------------------------------------------------------------------------- #
def split_one(path, base, suf, manifest, dry_run, proof_rows):
    with Image.open(path) as im:
        img = im.convert("RGB")
        w, h = img.size
        fold_px, confidence, meta = detect_fold(img)
        fold_px = max(1, min(w - 1, fold_px))

        tag = "DIVERTED" if confidence == "reject" else "split"
        print(f"  {path.name:<34} {w}x{h} AR={w/h:.2f} "
              f"fold={meta['fold_frac']:.3f} gut={meta['gutter']:.2f} "
              f"crs={meta['crease']:.2f} {confidence:<6} {meta['content']:<15} -> {tag}")

        if confidence == "reject":
            proof_rows.append((path.name, f"{w}x{h}", f"{w/h:.2f}",
                               f"{meta['fold_frac']:.3f}", confidence,
                               meta["content"], "auto", "manual"))
            if not dry_run:
                render_proof(img, fold_px,
                             f"{path.name}  gutter={meta['gutter']:.2f}  "
                             f"{meta['content']}  DIVERTED - not auto-split"
                             ).save(REVIEW_DIR / f"{base}_{suf}.jpg", quality=90)
            return "diverted"

        if confidence == "low":
            proof_rows.append((path.name, f"{w}x{h}", f"{w/h:.2f}",
                               f"{meta['fold_frac']:.3f}", confidence,
                               meta["content"], "auto", "split (done)"))
            if not dry_run:
                render_proof(img, fold_px,
                             f"{path.name}  crease={meta['crease']:.2f}  "
                             f"{meta['content']}  auto-split - verify cut"
                             ).save(REVIEW_DIR / f"{base}_{suf}.jpg", quality=90)

        if dry_run:
            return "would-split"

        left = img.crop((0, 0, fold_px, h))
        right = img.crop((fold_px, 0, w, h))
        left.save(PROCESSED_DIR / f"{base}_{suf}1.jpg", quality=JPEG_QUALITY)
        right.save(PROCESSED_DIR / f"{base}_{suf}2.jpg", quality=JPEG_QUALITY)
        UNSPLIT_DIR.mkdir(exist_ok=True)
        shutil.move(str(path), str(UNSPLIT_DIR / path.name))
        update_manifest_entry(manifest, base, suf, fold_px,
                              left.size, right.size, confidence)
        return "split"


def run_split(triples, dry_run, write_index=True):
    manifest = load_manifest()
    proof_rows, done, diverted = [], 0, 0
    for path, base, suf in triples:
        if already_done(base, suf):
            print(f"  {path.name}: already split, skipping")
            continue
        r = split_one(path, base, suf, manifest, dry_run, proof_rows)
        if r == "split":
            done += 1
        elif r == "diverted":
            diverted += 1
    if not dry_run and done:
        save_manifest(manifest)
    if proof_rows and write_index and not dry_run:
        write_review_index(proof_rows, append=True)
    print(f"\n{'(dry run) ' if dry_run else ''}split {done} crop(s); "
          f"{diverted} diverted to {REVIEW_DIR.name}/ for review")


# --------------------------------------------------------------------------- #
# review sheet
# --------------------------------------------------------------------------- #
INDEX_HEADER = [
    "# Spread review",
    "",
    "Proof images are in this folder; the red line is the proposed cut.",
    "Edit the `verdict` column, then run:",
    "",
    "    python scripts/split_spreads.py --apply-review processed/_spreads_review/INDEX.md",
    "",
    "Only rows with verdict `split` are acted on. `skip` / `manual` / `split (done)` are ignored.",
    "",
    "| crop | WxH | AR | fold_frac | confidence | content | origin | verdict |",
    "|---|---|---|---|---|---|---|---|",
]


def _existing_index_rows():
    fp = REVIEW_DIR / "INDEX.md"
    if not fp.exists():
        return {}
    rows = {}
    for line in fp.read_text(encoding="utf-8").splitlines():
        if line.startswith("|"):
            c = [x.strip() for x in line.strip("|").split("|")]
            if len(c) == 8 and c[0] not in ("crop", "---"):
                rows[c[0]] = tuple(c)
    return rows


def write_review_index(rows, append=False):
    REVIEW_DIR.mkdir(exist_ok=True)
    merged = _existing_index_rows() if append else {}
    for r in rows:
        merged[r[0]] = r
    lines = list(INDEX_HEADER)
    for r in sorted(merged.values()):
        lines.append("| " + " | ".join(r) + " |")
    (REVIEW_DIR / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_review():
    rows = []
    for path, base, suf, w, h, ar in candidates("review"):
        with Image.open(path) as im:
            img = im.convert("RGB")
            fold_px, confidence, meta = detect_fold(img)
        v = verdict_for(confidence, meta)
        render_proof(img, fold_px,
                     f"{path.name}  AR={ar:.2f}  fold={meta['fold_frac']:.3f}  "
                     f"gut={meta['gutter']:.2f} crs={meta['crease']:.2f}  "
                     f"{confidence}  {meta['content']}  => {v}"
                     ).save(REVIEW_DIR / f"{base}_{suf}.jpg", quality=90)
        rows.append((path.name, f"{w}x{h}", f"{ar:.2f}", f"{meta['fold_frac']:.3f}",
                     confidence, meta["content"], "review", v))
        print(f"  {path.name:<34} AR={ar:.2f} fold={meta['fold_frac']:.3f} "
              f"gut={meta['gutter']:.2f} crs={meta['crease']:.2f} "
              f"{confidence:<6} {meta['content']:<15} => {v}")
    write_review_index(rows, append=True)
    n = lambda k: sum(1 for r in rows if r[7] == k)
    print(f"\nwrote {len(rows)} proof(s) -> {REVIEW_DIR}")
    print(f"suggested: {n('split')} split, {n('skip')} skip, {n('manual')} manual")
    print(f"review/edit {REVIEW_DIR / 'INDEX.md'} then --apply-review it")


def parse_apply_list(fp: Path):
    """INDEX.md table rows with verdict == 'split', or a plain list of crop
    filenames (one per line, '#' comments allowed)."""
    wanted = []
    for line in fp.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("|"):
            c = [x.strip() for x in line.strip("|").split("|")]
            if len(c) == 8 and c[0] not in ("crop", "---") and c[7].lower() == "split":
                wanted.append(c[0])
        else:
            wanted.append(line.split()[0])
    return wanted


def run_apply_review(fp: Path, dry_run):
    names = parse_apply_list(fp)
    if not names:
        print(f"no 'split' rows found in {fp}")
        return
    triples = []
    for name in names:
        stem = Path(name).stem
        m = CROP_RE.match(stem)
        p = PROCESSED_DIR / (stem + ".jpg")
        if not m:
            print(f"  {name}: not a <scan>_<suffix> crop name, skipping")
        elif not p.exists():
            print(f"  {name}: not found in processed/, skipping")
        else:
            triples.append((p, m.group(1), m.group(2)))
    print(f"applying {len(triples)} approved split(s) from {fp.name}")
    run_split(triples, dry_run, write_index=False)


# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--unit", required=True, help="unit slug, e.g. oe1bu9454")
    ap.add_argument("--auto", action="store_true", help="split crops with AR >= 1.5")
    ap.add_argument("--review", action="store_true",
                    help="render the proof sheet for 1.12 <= AR < 1.5")
    ap.add_argument("--apply-review", metavar="PATH",
                    help="split the crops marked 'split' in a review INDEX.md / list file")
    ap.add_argument("--only", metavar="NNNN", help="restrict to crops whose name contains this")
    ap.add_argument("--limit", type=int, default=None, help="process at most N crops")
    ap.add_argument("--dry-run", action="store_true", help="report only; write nothing")
    args = ap.parse_args()

    if sum(bool(x) for x in (args.auto, args.review, args.apply_review)) != 1:
        ap.error("pick exactly one of --auto / --review / --apply-review")

    if args.review:
        build_review()
    elif args.apply_review:
        run_apply_review(Path(args.apply_review), args.dry_run)
    else:
        cand = list(candidates("auto", only=args.only))
        if args.limit:
            cand = cand[: args.limit]
        print(f"--auto: {len(cand)} candidate crop(s) with AR >= {AUTO_AR}")
        run_split([(p, b, s) for (p, b, s, *_r) in cand], args.dry_run)


if __name__ == "__main__":
    main()
