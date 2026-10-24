"""Fetch a map's control points from MapWarper into maps/<key>/georef.yml.

    python pipeline/maps/mapwarper.py <key>
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
# reference/maps.yml. Rows with `from: mapwarper` are replaced on every fetch;
# any other rows are kept. `fit:` is written by pipeline/maps/georef.py.
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
    if (info["width"], info["height"]) != (m["width"], m["height"]):
        die(f"MapWarper's image is {info['width']} x {info['height']}, maps.yml says "
            f"{m['width']} x {m['height']}")
    gcps = get(f"{API}{n}/gcps")["data"]
    new = [{"id": "mw" + g["id"], "x": round(float(g["attributes"]["x"]), 2),
            "y": round(float(g["attributes"]["y"]), 2),
            "lon": float(g["attributes"]["lon"]), "lat": float(g["attributes"]["lat"]),
            "error_mapwarper": round(float(g["attributes"]["error"]), 1),
            "from": "mapwarper"} for g in gcps]

    path = map_dir(key) / "georef.yml"
    old = read_yaml(path) if path.is_file() else {}
    kept = [g for g in (old or {}).get("gcps", []) if g.get("from") != "mapwarper"]
    data = {"map": key, "mapwarper": n, "fetched": date.today().isoformat(),
            "mapwarper_title": info["title"], "source_uri": info.get("source_uri"),
            "bbox": info["bbox"], "width": info["width"], "height": info["height"],
            "gcps": new + kept}
    if old and old.get("fit"):
        data["fit"] = old["fit"]
    dump_yaml(path, data, HEADER)
    print(f"{len(new)} control points from MapWarper ({len(kept)} others kept) -> {path}")


main()
