"""Shared helpers for the map scripts (docs/MAPS_PLAN.md)."""
import io
import os
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
MAPS_REPO = Path(os.environ.get("TRIEBENFELD_MAPS", ROOT.parent / "triebenfeld-maps"))
TILE_BASE = "https://takaji10.github.io/triebenfeld-maps"
MAPS_YML = ROOT / "reference" / "maps.yml"
GAZETTEER_DIR = ROOT / "reference" / "gazetteer"


def utf8_stdout():
    if not isinstance(sys.stdout, io.TextIOWrapper) or sys.stdout.encoding.lower() != "utf-8":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def die(msg):
    print("STOP: " + msg)
    sys.exit(1)


class Flow(list):
    """A list dumped in flow style: [1, 2] on one line (points, traces)."""


yaml.SafeDumper.add_representer(
    Flow, lambda d, v: d.represent_sequence("tag:yaml.org,2002:seq", list(v), flow_style=True))


def read_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def header_of(path):
    """The leading comment lines of a file (with their newlines), or ''."""
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or (not line.strip() and out):
                out.append(line)
            else:
                break
    return "".join(out)


def dump_yaml(path, data, header=""):
    """Write data as YAML under a comment header, UTF-8, LF."""
    if header and not header.endswith("\n"):
        header += "\n"
    body = yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=1000,
                          default_flow_style=False)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(header + body)


def image_size(path):
    import pyvips
    im = pyvips.Image.new_from_file(str(path))  # header only until pixels are read
    return im.width, im.height


def load_map(key, check_file=True):
    maps = read_yaml(MAPS_YML)["maps"]
    if key not in maps:
        die(f"map '{key}' is not in reference/maps.yml (known: {', '.join(maps)})")
    m = dict(maps[key])
    m["key"] = key
    if check_file:
        orig = m.get("original")
        if not orig:
            die(f"map '{key}' has no `original` in reference/maps.yml")
        if not Path(orig).is_file():
            die(f"the original of '{key}' is not there: {orig}")
        w, h = image_size(orig)
        if (w, h) != (m.get("width"), m.get("height")):
            die(f"'{key}': the file is {w} x {h} but maps.yml says "
                f"{m.get('width')} x {m.get('height')}")
    return m


def load_gazetteer():
    out = {}
    for p in sorted(GAZETTEER_DIR.glob("*.yml")):
        # A gazetteer file that does not parse stops the run: skipping it would
        # silently drop a place from the page and from the import.
        try:
            d = read_yaml(p)
        except yaml.YAMLError as e:
            sys.exit(f"{p.name} does not parse: {str(e).splitlines()[-1]}")
        if isinstance(d, dict) and d.get("slug"):
            out[d["slug"]] = d
    return out


def map_dir(key):
    d = ROOT / "maps" / key
    d.mkdir(parents=True, exist_ok=True)
    return d
