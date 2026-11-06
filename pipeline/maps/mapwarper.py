"""Fetch a map's control points from MapWarper into maps/<key>/georef.yml.

    python pipeline/maps/mapwarper.py <key>

The points are in the pixels of the image uploaded to MapWarper, which is the
map's `original` in reference/maps.yml. A map whose `original` is not the
georeferenced image (the five-sheet mosaic of Pełzucki 1896, georeferenced on
its sheet 4; the composite of Richter 1843, georeferenced on its two trimmed
sheets) names it in `mapwarper_image` and gives the mapping from that image's
pixels into the original's as `mapwarper_fit` - either the uniform
[scale, tx, ty] or, when the georeferenced image's pixel grid is stretched
against the original's (Richter 1843: the trimmed PNGs' y scale differs), the
anisotropic [sx, tx, sy, ty]. The fetched points are transformed before they
are written, and the fit is recorded in the file.
"""
import json
import sys
import urllib.request
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import die, dump_yaml, load_map, map_dir, read_yaml, utf8_stdout

API = "https://mapwarper.net/api/v1/maps/"
HEADER = """\
# Control points of one map: a pixel of the original image tied to a point on
# the ground (docs/MAPS_PLAN.md, section 5). Made by pipeline/maps/mapwarper.py
# from the editor's georeferencing on MapWarper (mapwarper.net); the pixels are
# those of the file uploaded there, which is the map's `original` in
# reference/maps.yml (for pelzucki1896 the sheet named by `mapwarper_image`,
# moved into the mosaic by its `mapwarper_fit`). Rows with `from: mapwarper`
# are replaced on every fetch; any other rows are kept. `fit:` is written by
# pipeline/maps/georef.py.
"""


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "triebenfeld-edition/1.0 (takaji@duck.com)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    utf8_stdout()
    if len(sys.argv) != 2:
        die("usage: mapwarper.py <key>")
    key = sys.argv[1]
    m = load_map(key, check_file=False)
    n = m.get("mapwarper")
    if not n:
        die(f"'{key}' has no `mapwarper` number in maps.yml")
    info = get(f"{API}{n}")["data"]["attributes"]
    # The points are in the pixels of the image uploaded to MapWarper: the
    # map's `original`, or the file named by `mapwarper_image`.
    image = m.get("mapwarper_image") or m.get("original")
    if (info["width"], info["height"]) != (m["mapwarper_width"], m["mapwarper_height"]):
        die(f"MapWarper's image is {info['width']} x {info['height']}, maps.yml says "
            f"{m['mapwarper_width']} x {m['mapwarper_height']}")
    gcps = get(f"{API}{n}/gcps")["data"]
    fit = m.get("mapwarper_fit") or [1.0, 0, 0]
    if len(fit) == 4:            # the anisotropic [sx, tx, sy, ty]
        sx, tx, sy, ty = (float(v) for v in fit)
    else:
        sx = sy = float(fit[0])
        tx, ty = float(fit[1]), float(fit[2])
    if image == m.get("original") and (sx, tx, sy, ty) != (1.0, 0, 1.0, 0):
        die(f"'{key}': a mapwarper_fit without a mapwarper_image makes no sense")
    new = [{"id": "mw" + g["id"],
            "x": round(sx * float(g["attributes"]["x"]) + tx, 2),
            "y": round(sy * float(g["attributes"]["y"]) + ty, 2),
            "lon": float(g["attributes"]["lon"]), "lat": float(g["attributes"]["lat"]),
            "error_mapwarper": round(float(g["attributes"]["error"]), 1),
            "from": "mapwarper"} for g in gcps]

    path = map_dir(key) / "georef.yml"
    old = read_yaml(path) if path.is_file() else {}
    kept = [g for g in (old or {}).get("gcps", []) if g.get("from") != "mapwarper"]
    data = {"map": key, "mapwarper": n, "fetched": date.today().isoformat(),
            "mapwarper_title": info["title"], "source_uri": info.get("source_uri"),
            "bbox": info["bbox"],
            "mapwarper_image": image if image != m.get("original") else None,
            "mapwarper_fit": fit if image != m.get("original") else None,
            "width": m["width"], "height": m["height"],
            "gcps": new + kept}
    if old and old.get("fit"):
        data["fit"] = old["fit"]
    dump_yaml(path, data, HEADER)
    where = ("" if image == m.get("original")
             else f" (from {Path(image).name}, fit {[round(v, 4) for v in fit]})")
    print(f"{len(new)} control points from MapWarper{where} "
          f"({len(kept)} others kept) -> {path}")


main()
