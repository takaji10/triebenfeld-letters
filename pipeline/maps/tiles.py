"""Cut a map's original into IIIF Image API 3 level-0 static tiles.

    python pipeline/maps/tiles.py <key> [--force]

Output: MAPS_REPO/<key>/ (info.json, tiles, map.json).
"""
import argparse
import json
import shutil
import sys

import pyvips

sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from common import MAPS_REPO, TILE_BASE, die, load_map, utf8_stdout


def main():
    utf8_stdout()
    ap = argparse.ArgumentParser()
    ap.add_argument("key")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    m = load_map(a.key)
    out = MAPS_REPO / a.key
    if out.exists():
        if not a.force:
            die(f"{out} exists; use --force to replace it")
        shutil.rmtree(out)
    MAPS_REPO.mkdir(parents=True, exist_ok=True)

    im = pyvips.Image.new_from_file(m["original"], access="sequential")
    if im.hasalpha():
        im = im.flatten(background=[255, 255, 255])
    if im.interpretation not in ("srgb", "b-w"):
        im = im.colourspace("srgb")
    if im.bands == 1:
        im = im.bandjoin([im, im])
    crop = m.get("crop")
    if crop:
        l, t, w, h = crop
        im = im.crop(l, t, w, h)
    W, H = im.width, im.height

    im.dzsave(str(out), layout="iiif3", tile_size=512, overlap=0, suffix=".jpg[Q=85]",
              id=TILE_BASE + "/" + a.key)

    for stray in (MAPS_REPO / "vips-properties.xml", out / "vips-properties.xml"):
        if stray.exists():
            stray.unlink()
    info_path = out / "info.json"
    if not info_path.is_file():
        die("libvips wrote no info.json")
    info = json.loads(info_path.read_text(encoding="utf-8"))
    want = TILE_BASE + "/" + a.key
    if info.get("id") != want:
        print(f"info.json id was {info.get('id')!r}; set to {want!r}")
        info["id"] = want
    with open(info_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(info, f, indent=2)
        f.write("\n")

    meta = {"map": a.key, "width": m["width"], "height": m["height"],
            "tiled_width": W, "tiled_height": H}
    if crop:
        meta["crop"] = crop
    with open(out / "map.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(meta, f, indent=2)
        f.write("\n")

    stray = out / "vips-properties.xml"
    if stray.exists():
        stray.unlink()
    files = [p for p in out.rglob("*") if p.is_file()]
    mb = sum(p.stat().st_size for p in files) / 1e6
    print(f"{len(files)} files, {mb:.1f} MB; tiled image {W} x {H}; info.json id {info['id']}")


main()
