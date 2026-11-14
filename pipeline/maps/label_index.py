"""The labelling to-do list: a table of the maps still to be marked, with
links to their labelling pages, built from reference/maps.yml and the
gazetteer (first made for the bulk batch of 2026-11-06).

    python pipeline/maps/label_index.py

Writes review/maps/index.html (review/ is not in the repository), served at
http://localhost:8780/ (the `map-labelling` configuration in
.claude/launch.json) so the editor can move between the sheets.

A map leaves the list once it is published: when the register on
origin/main (the branch the live site is built from) has `in_project: true`
for it (the editor, 2026-11-14: "When I finish with a map and it gets
published to the site, let's remove it from this to-do list"). Run this
after every publish that carries a map. If git cannot read origin/main,
the working copy's register is used.
"""
import subprocess
import sys
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]

# the editor's list order, with the notes the batch carries
ORDER = [
    ("lukom1766", "To mark again on the archive's JPG as drawn (your word, "
     "2026-11-06): the north-up PNG you georeferenced proved a different "
     "image, so the marks of 2026-10-23 could not carry over. No control "
     "points: your marks georeference it."),
    ("mapadrogi1890", ""),
    ("zagorow1841", "001.jpg as drawn is the map of record (your word, "
     "2026-11-06); the rotated image and the folder's 002 are left out. No "
     "control points: your marks georeference it."),
    ("pelzucki1901", "Image 001 only; 002 left out."),
    ("trojwiorstowki1914", "Only a small section of the sheet bears on the "
     "edition; the sheet comes in whole."),
    ("reymann1834", "The Peisern sheet is the map of record; its file's own "
     "name says ca. 1850 — the year is open (NEEDS_CONFIRMATION). No control "
     "points yet: your marks georeference it."),
    ("richter1843", "<b>To address:</b> the fit's control point "
     "<b>mw759848 sits 844 m off</b> — a possible misidentification; look at "
     "the warp (takaji10.github.io/triebenfeld-maps/warp.html?map=richter1843) "
     "and, if the point is wrong, it comes off the record. The composite "
     "carries both sheets (Kol. I, Sek. II and III); the editor's points from "
     "the two trimmed PNGs were carried in through pixel fits."),
    ("blaeu1665", "Dated ca. 1664 per your reference; the short form keeps "
     "'Blaeu 1665' (the gazetteer's citation). No control points yet."),
    ("vonpfau1770", "The full sheet is the map of record (your _crop.jpg is "
     "not used). No control points yet."),
    ("perthees1798", "Cropped to the gazetteer's area (the full sheet stays "
     "the record; the marks are stored in its pixels). No control points yet."),
    ("trabczyn1790", "The parish sketch. No control points yet."),
    ("messtischblatt1940", "Your four-sheet mosaic is the map of record; no "
     "control points yet — your marks georeference it."),
    ("slupca1957", ""),
    ("bildplan1944", "The source is open (MISSING_SOURCES). No control "
     "points yet. The short form 'Bildplan 1944' is proposed, not yet yours."),
    ("ams1962", "No control points yet: your marks georeference it."),
    ("gilly1802", "Georeferenced without MapWarper at your word (the 83446 "
     "reference was a different version): BII correlated against the warped "
     "tiles of MapWarper 63625 — BII's meridian is tilted ~16°, which is why "
     "the earlier searches found nothing. 43 synthetic points, fit RMS "
     "165 m; your marks sharpen it."),
    ("pambo1803", "Dated 1801 per your reference (drawn 'after Pambo'); the "
     "short form keeps 'Pambo 1803' (the gazetteer's citation)."),
    ("weydner1804", ""),
    ("hollring1804", "Dated 1805 per your reference; the short form keeps "
     "'Hollring 1804'. Your reference names unit 122-27; the scan file on "
     "J: is numbered 388-14."),
    ("krolikow1800", "Dated 1800-1815 per your reference; the short form "
     "keeps 'Królików 1800'. The north-up rotated image is the map of record."),
    ("zagorowo1799", "No control points yet."),
]


def published_maps():
    """The maps with in_project: true in the register on origin/main."""
    try:
        txt = subprocess.run(
            ["git", "show", "origin/main:reference/maps.yml"], cwd=ROOT,
            capture_output=True, check=True).stdout.decode("utf-8")
        src = "origin/main"
    except (subprocess.CalledProcessError, OSError):
        txt = (ROOT / "reference" / "maps.yml").read_text(encoding="utf-8")
        src = "the working copy (origin/main could not be read)"
    reg = (yaml.safe_load(txt) or {}).get("maps") or {}
    return {k for k, m in reg.items() if (m or {}).get("in_project")}, src


def main():
    maps = (yaml.safe_load((ROOT / "reference" / "maps.yml").read_text(encoding="utf-8"))
            or {})["maps"]
    done, src = published_maps()
    find = {}
    for p in (ROOT / "reference" / "gazetteer").glob("*.yml"):
        g = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        for it in g.get("maps") or []:
            if (it or {}).get("map") and not it.get("absent"):
                find[it["map"]] = find.get(it["map"], 0) + 1
    rows = []
    left_out = []
    for key, note in ORDER:
        if key in done:
            left_out.append(maps[key].get("cited_as") or key)
            continue
        m = maps[key]
        n = find.get(key, 0)
        rms = None
        geo = ROOT / "maps" / key / "georef.yml"
        if geo.is_file():
            g = yaml.safe_load(geo.read_text(encoding="utf-8")) or {}
            f = g.get("fit") or {}
            rms = f.get("rms_m")
        if rms is not None:
            gstat = f"fitted (RMS {rms} m)"
        else:
            gstat = "your marks georeference it"
        note_html = f"<div class='note'>{note}</div>" if note else ""
        if rms is not None:
            warp = "https://takaji10.github.io/triebenfeld-maps/warp.html?map=" + key
            overlay = (f"<a href='{warp}'>OSM</a> · "
                       f"<a href='{warp}&amp;base=satellite'>satellite</a>")
        else:
            overlay = "<span class='dim'>with the georef</span>"
        rows.append(
            f"<tr><td class='m'><b>{m.get('cited_as')}</b>"
            f"<div class='y'>{m.get('year')} · {m.get('kind', '—')}"
            f"{', crop' if m.get('crop') else ''}</div></td>"
            f"<td><a href='{key}/'>open the sheet</a></td>"
            f"<td class='o'>{overlay}</td>"
            f"<td class='n'>{n}</td>"
            f"<td class='g'>{gstat}</td>"
            f"<td class='x'>{note_html}</td></tr>")
    html = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>The bulk batch: label the maps</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{font:14px/1.45 system-ui,Segoe UI,Arial,sans-serif;color:#222;margin:24px auto;max-width:1100px;padding:0 16px}
h1{font-size:20px;margin:0 0 4px}
.sub{color:#666;margin-bottom:14px}
table{border-collapse:collapse;width:100%}
th,td{border:1px solid #ccc;padding:7px 10px;vertical-align:top;text-align:left}
th{background:#f2efe6;font-size:12px;text-transform:uppercase;letter-spacing:.04em}
td.m{width:170px}td.n{width:60px;text-align:center}td.g{width:190px;font-size:13px}
td.o{width:120px;font-size:13px;white-space:nowrap}
.dim{color:#999}
td.x{font-size:13px}
.y{font-size:12px;color:#777}
.note{color:#444}
a{color:#0a5da8;text-decoration:none}a:hover{text-decoration:underline}
.warn{background:#fff3f0;border:1px solid #e0b3a8;border-radius:4px;padding:8px 12px;margin:10px 0;font-size:13px}
</style></head><body>
<h1>The bulk batch: label the maps</h1>
<div class="sub">The maps still to be marked. Work through them in any
order; the work is kept in the browser per sheet. <b>Save</b> each sheet's
file when it is done and tell Claude the file names. <kbd>N</kbd> marks a
name with no symbol; the form field takes the lettering as the map spells it.
A map leaves this list once it is published on the site.</div>
<table>
<tr><th>Map</th><th>Label page</th><th>Overlay</th><th>To find</th><th>Georeference</th><th>Notes</th></tr>
ROWS
</table>
</body></html>
"""
    html = html.replace("ROWS", "\n".join(rows))
    out = ROOT / "review" / "maps" / "index.html"
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print(f"{len(rows)} rows -> {out}")
    print(f"published, left out (from {src}): {', '.join(left_out) or 'none'}")


main()
