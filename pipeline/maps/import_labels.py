"""Take the labelling page's saved file into the edition.

    python pipeline/maps/import_labels.py <key> <saved.json>

Validates the file, writes maps/<key>/labels.yml, cuts the crops into
site/assets/maps/crops/<key>/<id>.jpg and fills the gazetteer's `maps:` items
with `label:`.  The saved file is the editor's and wins.
"""
import json
import math
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pyvips

sys.path.insert(0, str(Path(__file__).parent))
from common import (GAZETTEER_DIR, ROOT, Flow, die, dump_yaml, header_of, load_gazetteer,
                    load_map, map_dir, read_yaml, utf8_stdout)

SHOWS = {"village", "oleder-settlement", "folwark", "tavern", "water-mill", "windmill", "forest",
         "field", "water", "road", "church", "other", "unsure"}
FIELDS = ["id", "place", "new_place", "form", "point", "trace", "height", "shows", "note"]
MAX_W, MAX_H = 600, 200
WHITE = [255, 255, 255]


def validate(m, data, gaz):
    errs = []
    key = m["key"]
    if data.get("map") != key:
        errs.append(f"the file is for map {data.get('map')!r}, not {key!r}")
    if (data.get("width"), data.get("height")) != (m["width"], m["height"]):
        errs.append(f"the file's size {data.get('width')} x {data.get('height')} differs from "
                    f"maps.yml's {m['width']} x {m['height']}")
    seen = set()
    for i, lb in enumerate(data.get("labels") or []):
        lid = lb.get("id")
        where = f"label {i + 1} ({lid})"
        if not lid:
            errs.append(f"label {i + 1} has no id")
        elif lid in seen:
            errs.append(f"{where}: duplicate id")
        seen.add(lid)
        if lb.get("place"):
            if lb["place"] not in gaz:
                errs.append(f"{where}: place {lb['place']!r} is not in the gazetteer")
        elif not lb.get("new_place"):
            errs.append(f"{where}: neither a place nor a new_place")
        if lb.get("shows") not in SHOWS:
            errs.append(f"{where}: shows {lb.get('shows')!r} is not one of {sorted(SHOWS)}")
        for name in ("point", "trace"):
            v = lb.get(name)
            if v is None:
                continue
            pts = [v] if name == "point" else v
            for p in pts:
                if (not isinstance(p, (list, tuple)) or len(p) != 2
                        or not all(isinstance(c, (int, float)) for c in p)):
                    errs.append(f"{where}: bad {name} {p!r}")
                    break
                if not (0 <= p[0] <= m["width"] and 0 <= p[1] <= m["height"]):
                    errs.append(f"{where}: {name} point {p!r} lies outside the image")
                    break
        if lb.get("trace") is not None and len(lb["trace"]) < 2:
            errs.append(f"{where}: a trace needs at least 2 points")
        if lb.get("trace") and not isinstance(lb.get("height"), (int, float)):
            errs.append(f"{where}: a trace needs a band height")
    return errs


def load_image(path):
    im = pyvips.Image.new_from_file(path, access="random")
    if im.hasalpha():
        im = im.flatten(background=WHITE)
    if im.bands == 1:
        im = im.bandjoin([im, im])
    return im


def rotate_xy(p, theta):
    """Rotate vector p so that a vector at angle theta (image coords, y down) points +x."""
    c, s = math.cos(theta), math.sin(theta)
    return (c * p[0] + s * p[1], -s * p[0] + c * p[1])


def split_lines(trace, breaks=None):
    """Split a trace into the lines of a name written on several lines.

    A new line starts at trace[i] for each i in `breaks` (the labelling page's
    key L).  With no breaks given, segment k (trace[k] -> trace[k+1]) is a jump
    to the next line when it runs against the first segment:
    dot(seg_k, seg_0) < 0.  Curved lettering never bends 90 degrees between two
    clicks; a return to the start of the next line always does.  The page's
    JavaScript (splitLines in label_page.py) mirrors this exactly.
    """
    n = len(trace)
    if n == 0:
        return []
    if breaks:
        starts = sorted({int(i) for i in breaks if 0 < int(i) < n})
    else:
        starts = []
        if n > 2:
            sx, sy = trace[1][0] - trace[0][0], trace[1][1] - trace[0][1]
            for k in range(1, n - 1):
                dx, dy = trace[k + 1][0] - trace[k][0], trace[k + 1][1] - trace[k][1]
                if dx * sx + dy * sy < 0:
                    starts.append(k + 1)
    lines, prev = [], 0
    for s in starts + [n]:
        lines.append([list(p) for p in trace[prev:s]])
        prev = s
    return lines


def crop_trace(im, trace, height, breaks=None):
    """The lettering along `trace`, straightened so that it reads left to right.

    The reading direction is that of the first line (first point to its last);
    the crop covers all lines.  `trace` is the baseline of the lettering: the
    letters stand `height` above it, descenders reach 0.35 * height below."""
    pts = np.array(trace, float)
    pad = height * 1.5 + 10
    l = max(0, int(math.floor(pts[:, 0].min() - pad)))
    t = max(0, int(math.floor(pts[:, 1].min() - pad)))
    r = min(im.width, int(math.ceil(pts[:, 0].max() + pad)))
    b = min(im.height, int(math.ceil(pts[:, 1].max() + pad)))
    piece = im.crop(l, t, r - l, b - t)
    local = pts - [l, t]
    first = split_lines(trace, breaks)[0]
    if len(first) >= 2:
        d = np.array(first[-1], float) - np.array(first[0], float)
    elif len(pts) >= 2:
        d = pts[1] - pts[0]
    else:
        d = np.zeros(2)
    theta = math.atan2(d[1], d[0])
    rot = np.array([rotate_xy(p, theta) for p in local])
    x0, x1 = rot[:, 0].min() - height * 0.4, rot[:, 0].max() + height * 0.4
    # in the rotated image "up" is -y: the letters above the baseline, descenders below
    y0 = rot[:, 1].min() - height - 0.15 * height
    y1 = rot[:, 1].max() + 0.35 * height + 0.1 * height
    w, h = max(1, int(round(x1 - x0))), max(1, int(round(y1 - y0)))
    c, s = math.cos(theta), math.sin(theta)
    # output = R * input - (x0, y0), with R = [[c, s], [-s, c]]; the rotation and
    # the second crop are one affine step, so the sign is set here, not by a rotate call
    return piece.affine([c, s, -s, c], odx=-x0, ody=-y0, oarea=[0, 0, w, h],
                        interpolate=pyvips.Interpolate.new("bicubic"), background=WHITE)


def crop_point(im, point, view_rotation, size=400):
    half = size // 2
    l = int(min(max(0, round(point[0]) - half), max(0, im.width - size)))
    t = int(min(max(0, round(point[1]) - half), max(0, im.height - size)))
    piece = im.crop(l, t, min(size, im.width - l), min(size, im.height - t))
    rot = (view_rotation or 0) % 360
    angle = {0: "d0", 90: "d90", 180: "d180", 270: "d270"}.get(rot)
    if angle is None:
        die(f"view_rotation {view_rotation} is not a multiple of 90")
    return piece.rot(angle)


def shrink(im):
    scale = min(1.0, MAX_W / im.width, MAX_H / im.height)
    return im.resize(scale, kernel="lanczos3") if scale < 1 else im


def main():
    utf8_stdout()
    if len(sys.argv) != 3:
        die("usage: import_labels.py <key> <saved.json>")
    key, saved = sys.argv[1], Path(sys.argv[2])
    m = load_map(key)
    gaz = load_gazetteer()
    data = json.loads(saved.read_text(encoding="utf-8"))
    errs = validate(m, data, gaz)
    if errs:
        die("the saved file has problems:\n  - " + "\n  - ".join(errs))
    labels = []
    for src in data["labels"]:
        lb = {f: src.get(f) for f in FIELDS}
        if src.get("breaks"):
            lb["breaks"] = Flow(int(i) for i in src["breaks"])
        labels.append(lb)
    for lb in labels:
        if lb["point"] is not None:
            lb["point"] = Flow(int(round(c)) for c in lb["point"])
        if lb["trace"] is not None:
            lb["trace"] = [Flow(int(round(c)) for c in p) for p in lb["trace"]]
        if lb["height"] is not None:
            lb["height"] = int(round(lb["height"]))

    header = (f"# The editor's marks on the map {key}, from the labelling page, imported from\n"
              f"# {saved.name} on {date.today().isoformat()} by pipeline/maps/import_labels.py.\n"
              f"# The saved file is the editor's and wins; marks are in the pixels of the\n"
              f"# original image (reference/maps.yml). Docs: docs/MAPS_PLAN.md, sections 3-4.\n")
    dump_yaml(map_dir(key) / "labels.yml",
              {"map": key, "width": m["width"], "height": m["height"],
               "saved": data.get("saved"), "labels": labels}, header)

    im = load_image(m["original"])
    cdir = ROOT / "site" / "assets" / "maps" / "crops" / key
    cdir.mkdir(parents=True, exist_ok=True)
    made = 0
    for lb in labels:
        if lb["trace"]:
            c = crop_trace(im, lb["trace"], lb["height"], lb.get("breaks"))
        elif lb["point"]:
            c = crop_point(im, lb["point"], m.get("view_rotation"))
        else:
            continue
        c = shrink(c)
        out = cdir / f"{lb['id']}.jpg"
        c.write_to_file(str(out), Q=85)
        made += 1
        print(f"  crop {lb['id']}: {c.width} x {c.height}, {out.stat().st_size} bytes")
    print(f"{len(labels)} labels, {made} crops -> {cdir}")

    diffs, news = [], []
    for lb in labels:
        if lb["new_place"] and not lb["place"]:
            news.append(f"{lb['id']}: new place {lb['new_place']!r} (form {lb['form']!r})")
        if not lb["place"]:
            continue
        path = GAZETTEER_DIR / f"{lb['place']}.yml"
        if not path.is_file():
            die(f"no gazetteer file {path}")
        g = read_yaml(path)
        items = g.setdefault("maps", [])
        item = next((i for i in items if i.get("map") == key and not i.get("label") and not i.get("absent")), None)
        if item is None:
            item = {"map": key, "form": lb["form"], "note": None}
            items.append(item)
            diffs.append(f"{lb['id']}: {lb['place']} had no item for {key}; one added with form {lb['form']!r}")
        elif item.get("form") != lb["form"]:
            diffs.append(f"{lb['id']}: {lb['place']}: gazetteer form {item.get('form')!r}, typed {lb['form']!r}")
        item["label"] = lb["id"]
        dump_yaml(path, g, header_of(path))
    print(f"gazetteer updated for {sum(1 for l in labels if l['place'])} labels")
    for line in diffs + news:
        print("  REPORT " + line)


if __name__ == "__main__":
    main()
