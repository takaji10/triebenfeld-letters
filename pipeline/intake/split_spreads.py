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
CREASE_MIN = 0.10
# A book photographed open has a fold that is a dark shadow, not a gap. That
# inverts the assumption above: the clearest band of bare paper is then a page
# margin, not the gutter, and cutting there slices a strip off one leaf and can
# run straight through the writing. Where a shadow like this exists it is the
# most reliable signal there is, so it is tried first.
SHADOW_DARK = 150            # at/below this a pixel is not bare paper
SHADOW_RUN = 0.12            # unbroken dark run, as a fraction of image height
SHADOW_STROKE = 0.06         # shorter runs than this are pen strokes, not structure
SPLIT_OVERLAP = 0.008        # each half keeps this much of the other side of the fold                       # crease streak strength below which no real fold line is
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


def shadow_fold(small: Image.Image):
    """The gutter shadow: the column with the longest unbroken dark run.

    Returns (x, run_fraction) or (None, best_fraction_seen). Writing gives
    short scattered runs a few pixels long; a fold shadow runs down a large
    part of the height without a break, so the two do not compete.
    """
    px = small.load()
    w, h = small.size
    lo, hi = int(w * FOLD_LO), int(w * FOLD_HI)
    best_x, best_run = None, 0
    for x in range(lo, hi):
        run = longest = 0
        for y in range(h):
            if px[x, y] <= SHADOW_DARK:
                run += 1
                if run > longest:
                    longest = run
            else:
                run = 0
        if longest > best_run:
            best_x, best_run = x, longest
    if best_run >= h * SHADOW_RUN:
        return best_x, best_run / h
    return None, best_run / h


def text_gap_fold(small: Image.Image):
    """Midpoint of the clear channel between the two blocks of writing.

    A column counts as written when it holds ink in short runs: long runs are
    structure (a fold shadow, a page edge), not a pen. Taking the innermost
    written column on each side of centre and cutting between them puts the cut
    in paper by construction, whatever the lighting did to the gutter.
    """
    px = small.load()
    w, h = small.size
    lo, hi = int(w * FOLD_LO), int(w * FOLD_HI)

    def written(x):
        run = longest = dark = 0
        for y in range(h):
            if px[x, y] <= SHADOW_DARK:
                dark += 1
                run += 1
                if run > longest:
                    longest = run
            else:
                run = 0
        return dark >= 3 and longest < h * SHADOW_STROKE

    mid = w // 2
    left = [x for x in range(lo, mid) if written(x)]
    right = [x for x in range(mid, hi) if written(x)]
    if not left or not right:
        return None, 0.0
    a, b = max(left), min(right)
    if b <= a + 1:
        return None, 0.0
    return (a + b) // 2, (b - a) / w


def detect_fold(img: Image.Image, prior=None):
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
    shadow_x, shadow_run = shadow_fold(small)
    gap_x, gap_w = (None, 0.0) if shadow_x is not None else text_gap_fold(small)
    gutter, crease = column_profiles(small)
    gutter = moving_average(gutter, 5)
    crease = moving_average(crease, 5)

    lo, hi = int(w * FOLD_LO), int(w * FOLD_HI)
    mid = w / 2
    g_max = max(gutter[lo:hi])

    if shadow_x is not None:
        # the fold casts a shadow: that is where the leaves meet
        fold_x = shadow_x
        confidence = "high"
        crease_val = crease[fold_x]
        method = f"shadow {shadow_run:.2f}h"
    elif prior is not None:
        # No shadow on this opening, but the book was photographed the same way
        # throughout, so the folds the shadow did find elsewhere in this unit
        # say where this one is. Measured against 43 folds placed by hand, this
        # lands within about 30px, where the midpoint of the writing gap was
        # 67px out and always to the left of the truth.
        fold_x = max(lo, min(hi - 1, int(round(prior * w))))
        confidence = "high"
        crease_val = crease[fold_x]
        method = f"unit fold {prior:.3f}"
    elif gap_x is not None:
        # no prior yet: fall back on the channel between the two written blocks
        fold_x = gap_x
        confidence = "low"
        crease_val = crease[fold_x]
        method = f"text gap {gap_w:.3f}w"
    elif g_max < GUTTER_MIN:
        confidence = "reject"
        fold_x = min(range(lo, hi), key=lambda x: raw[x])   # best effort
        crease_val = crease[fold_x]
        method = "no channel"
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
        method = "gutter band"
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
        "method": method,
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
def split_one(path, base, suf, manifest, dry_run, proof_rows, fold_override=None, prior=None):
    with Image.open(path) as im:
        img = im.convert("RGB")
        w, h = img.size
        if fold_override is None:
            fold_px, confidence, meta = detect_fold(img, prior=prior)
        else:
            # a fold placed by eye in the review page; trusted over detection
            fold_px = round(fold_override * w)
            confidence = "manual"
            meta = {"fold_frac": round(fold_override, 4), "gutter": 0.0,
                    "crease": 0.0, "content": "set by hand", "method": "by hand"}
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

        # A small overlap either side of the fold. In a bound volume the
        # writing often runs right into the gutter, so a cut exactly on the
        # fold can clip the last stroke of a line. Giving each half a sliver
        # of the other costs nothing and means no ink is lost.
        pad = max(1, int(w * SPLIT_OVERLAP))
        left = img.crop((0, 0, min(w, fold_px + pad), h))
        right = img.crop((max(0, fold_px - pad), 0, w, h))
        left.save(PROCESSED_DIR / f"{base}_{suf}1.jpg", quality=JPEG_QUALITY)
        right.save(PROCESSED_DIR / f"{base}_{suf}2.jpg", quality=JPEG_QUALITY)
        UNSPLIT_DIR.mkdir(exist_ok=True)
        shutil.move(str(path), str(UNSPLIT_DIR / path.name))
        update_manifest_entry(manifest, base, suf, fold_px,
                              left.size, right.size, confidence)
        return "split"


def unit_prior(triples):
    """Median fold across the openings that do show a shadow.

    One book photographed in one sitting puts its fold in nearly the same place
    every time, so the openings that give a clear answer are the best evidence
    for the ones that do not.
    """
    seen = []
    for path, _, _ in triples:
        try:
            with Image.open(path) as im:
                small, _ = load_small_grayscale(im.convert("L"))
                x, run = shadow_fold(small)
                if x is not None:
                    seen.append(x / small.size[0])
        except OSError:
            continue
    if len(seen) < 5:
        return None
    seen.sort()
    return seen[len(seen) // 2]


def run_split(triples, dry_run, write_index=True, folds=None):
    manifest = load_manifest()
    prior = None
    if triples and not folds:
        prior = unit_prior(triples)
        if prior is not None:
            print(f"  fold prior for this unit: {prior:.3f} of the width")
    proof_rows, done, diverted = [], 0, 0
    for path, base, suf in triples:
        if already_done(base, suf):
            print(f"  {path.name}: already split, skipping")
            continue
        r = split_one(path, base, suf, manifest, dry_run, proof_rows,
                      fold_override=(folds or {}).get(path.name), prior=prior)
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


def current_fold(manifest, base, suf):
    """The fold a split was made at, as a fraction of the crop, from the manifest."""
    for entries in manifest.values():
        halves = [e for e in entries
                  if e["file"] in (f"{base}_{suf}1.jpg", f"{base}_{suf}2.jpg")]
        if len(halves) == 2:
            halves.sort(key=lambda e: e["bbox_original"][0])
            x0 = halves[0]["bbox_original"][0]
            x1 = halves[1]["bbox_original"][2]
            cut = halves[0]["bbox_original"][2]
            if x1 > x0:
                return (cut - x0) / (x1 - x0)
    return None


def unsplit(base, suf, manifest):
    """Undo a split: put the original back and drop the halves."""
    original = UNSPLIT_DIR / f"{base}_{suf}.jpg"
    if not original.exists():
        return False
    shutil.move(str(original), str(PROCESSED_DIR / f"{base}_{suf}.jpg"))
    for half in (f"{base}_{suf}1.jpg", f"{base}_{suf}2.jpg"):
        fp = PROCESSED_DIR / half
        if fp.exists():
            fp.unlink()
    for entries in manifest.values():
        halves = [e for e in entries
                  if e["file"] in (f"{base}_{suf}1.jpg", f"{base}_{suf}2.jpg")]
        if len(halves) != 2:
            continue
        # Put the parent crop back, or a re-split has no bbox to work from and
        # falls back to summing the two half widths - which include the overlap,
        # so the fold would land short of where it was asked for.
        halves.sort(key=lambda e: e["bbox_original"][0])
        a = halves[0]["bbox_original"]
        # The restored file is the authority on the crop's size. Deriving it
        # from the halves instead would carry the overlap into the width and
        # shift every later fold by that much.
        with Image.open(PROCESSED_DIR / f"{base}_{suf}.jpg") as im:
            cw, ch = im.size
        parent = {"file": f"{base}_{suf}.jpg",
                  "bbox_original": [a[0], a[1], a[0] + cw, a[1] + ch],
                  "size": [cw, ch]}
        keep = [e for e in entries if e not in halves]
        idx = min(entries.index(h) for h in halves)
        keep.insert(min(idx, len(keep)), parent)
        entries[:] = keep
    return True


def run_apply_folds(fp: Path, dry_run):
    """Split at folds placed by hand in the review page.

    The file is {crop filename: fold as a fraction of width}, which is what
    review.html saves. A spread that is already split is redone only when the
    fold has actually moved, so re-applying the same file changes nothing.
    """
    with open(fp, encoding='utf-8') as f:
        folds = {k: float(v) for k, v in json.load(f).items()}
    manifest = load_manifest()
    triples, redone, unchanged = [], 0, 0
    for name in sorted(folds):
        stem = Path(name).stem
        m = CROP_RE.match(stem)
        frac = folds[name]
        if not m:
            print(f"  {name}: not a <scan>_<suffix> crop name, skipping")
            continue
        if not (0.05 < frac < 0.95):
            print(f"  {name}: fold {frac} is outside the sheet, skipping")
            continue
        base, suf = m.group(1), m.group(2)
        path = PROCESSED_DIR / (stem + ".jpg")
        if not path.exists():
            was = current_fold(manifest, base, suf)
            if was is not None and abs(was - frac) < 0.0005:
                unchanged += 1
                continue
            if not dry_run and not unsplit(base, suf, manifest):
                print(f"  {name}: already split and no original kept, skipping")
                continue
            if dry_run:
                print(f"  {name}: would move the fold {was:.4f} -> {frac:.4f}"
                      if was is not None else f"  {name}: would re-split at {frac:.4f}")
                continue
            redone += 1
        triples.append((path, base, suf))
    if not dry_run:
        save_manifest(manifest)
    print(f"applying {len(triples)} hand-placed fold(s) from {fp.name}"
          + (f"; {redone} moved, {unchanged} unchanged" if redone or unchanged else ""))
    if triples:
        run_split(triples, dry_run, write_index=False, folds=folds)
    # remember which were placed by hand so a later review can leave them be
    if not dry_run and folds:
        marker = REVIEW_DIR / "hand_placed.json"
        seen = {}
        if marker.exists():
            with open(marker, encoding='utf-8') as f:
                seen = json.load(f)
        seen.update({k: round(v, 4) for k, v in folds.items()})
        REVIEW_DIR.mkdir(exist_ok=True)
        with open(marker, 'w', encoding='utf-8') as f:
            json.dump(seen, f, ensure_ascii=False, indent=1)


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
    ap.add_argument("--apply-folds", metavar="PATH",
                    help="JSON of hand-placed folds saved by review.html")
    ap.add_argument("--apply-review", metavar="PATH",
                    help="split the crops marked 'split' in a review INDEX.md / list file")
    ap.add_argument("--only", metavar="NNNN", help="restrict to crops whose name contains this")
    ap.add_argument("--limit", type=int, default=None, help="process at most N crops")
    ap.add_argument("--dry-run", action="store_true", help="report only; write nothing")
    args = ap.parse_args()

    if sum(bool(x) for x in (args.auto, args.review, args.apply_review, args.apply_folds)) != 1:
        ap.error("pick exactly one of --auto / --review / --apply-review")

    if args.review:
        build_review()
    elif args.apply_folds:
        _f = Path(args.apply_folds)
        if not _f.is_absolute():
            _f = ROOT / args.apply_folds
        run_apply_folds(_f, args.dry_run)
    elif args.apply_review:
        _p = Path(args.apply_review)
        if not _p.is_absolute():
            _p = ROOT / args.apply_review     # relative to the unit, not the shell
        run_apply_review(_p, args.dry_run)
    else:
        cand = list(candidates("auto", only=args.only))
        if args.limit:
            cand = cand[: args.limit]
        print(f"--auto: {len(cand)} candidate crop(s) with AR >= {AUTO_AR}")
        run_split([(p, b, s) for (p, b, s, *_r) in cand], args.dry_run)


if __name__ == "__main__":
    main()
