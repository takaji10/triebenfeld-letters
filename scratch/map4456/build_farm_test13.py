# The farm test for the editor's chosen farm (red 13): the red-13 sites from
# the catalogue, each as a large neighbourhood crop (700 px square at 2x
# display), with the statement's row 13 beside it for the check.
import base64
import io
import json

import numpy as np
import pyvips
import PIL.Image

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld"
FULL = (r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)"
        r"\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456\4456_full.jpg")
OUT = ROOT + r"\scratch\map4456\farm_test_13.html"

D = json.load(open(ROOT + r"\scratch\map4456\reds_all.json", encoding="utf-8"))
REF = json.load(open(ROOT + r"\scratch\map4456\reference_numbers.json", encoding="utf-8"))
stmt = REF["statement"]
ROW = 13
r = stmt[str(ROW)]

def canon(t):
    t = t.strip()
    t = t.replace("[", "").replace("?]", "").replace("?", "")
    return t.strip()

sites = []
for a in D["answered"]:
    if canon(a["text"]) == str(ROW):
        x, y = a["x"], a["y"]
        if a.get("fixed"):
            x = a["fixed"]["x"]; y = a["fixed"]["y"]
        sites.append({"x": x, "y": y, "src": "sheet card"})
for n in D["added"]:
    if canon(n["text"]) == str(ROW):
        sites.append({"x": n["x"] + (n.get("w", 0)) // 2,
                      "y": n["y"] + (n.get("h", 0)) // 2, "src": "map-added"})
print("red-%d sites:" % ROW, len(sites))
for s in sites:
    print("   (%d, %d) from %s" % (s["x"], s["y"], s["src"]))

im = pyvips.Image.new_from_file(FULL, access="random")
W, H = im.width, im.height
cards = []
R = 350
for k, s in enumerate(sites):
    cx, cy = s["x"], s["y"]
    l = max(0, cx - R); t = max(0, cy - R)
    r_ = min(W, cx + R); b_ = min(H, cy + R)
    a = np.frombuffer(im.crop(l, t, r_ - l, b_ - t).write_to_memory(),
                      np.uint8).reshape(b_ - t, r_ - l, 3)
    buf = io.BytesIO()
    PIL.Image.fromarray(a).save(buf, "JPEG", quality=88)
    cards.append({"k": k, "x": cx, "y": cy, "src": s["src"],
                  "img": "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()})
print("cards:", len(cards))

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Pełzucki 1896 — the farm test: red 13 (working page)</title>
<style>
:root { --rule: #d8d2c4; --ink: #2a2620; --ink-soft: #6b6459; --accent: #8a3324; }
body { margin: 0; background: #faf8f3; color: var(--ink); font-family: Georgia, serif; }
header { max-width: 80rem; margin: 0 auto; padding: 1rem 1.5rem .2rem; }
header h1 { font-size: 1.25rem; margin: 0 0 .3rem; }
header p { font-size: .88rem; color: var(--ink-soft); margin: .2rem 0; }
.grid { max-width: 80rem; margin: 0 auto; padding: 0 1.5rem 2rem;
        display: grid; grid-template-columns: 1fr 1fr; gap: 1.4rem; }
.cell { border: 1px solid var(--rule); border-radius: .4rem; padding: .6rem;
        background: #fff; }
.cell h3 { font-size: .9rem; margin: 0 0 .4rem; font-family: Verdana, sans-serif; }
.cell img { width: 100%; display: block; border: 1px solid var(--rule); }
.readout { font-family: Verdana, sans-serif; font-size: .78rem; color: var(--ink-soft);
           margin-top: .3rem; }
.summary { max-width: 80rem; margin: .4rem auto; padding: .7rem 1.5rem;
           border: 1px solid var(--rule); border-radius: .4rem; font-size: .9rem; }
.summary b { font-family: Verdana, sans-serif; }
table.row13 { border-collapse: collapse; font-size: .88rem; margin: .4rem 0 0; }
table.row13 th, table.row13 td { border: 1px solid var(--rule); padding: .2rem .6rem;
                                 text-align: left; }
table.row13 th { font-family: Verdana, sans-serif; font-size: .74rem; font-weight: 400;
                 color: var(--ink-soft); }
table.row13 td.num { font-variant-numeric: tabular-nums; text-align: right; }
</style>
</head>
<body>
<header>
  <h1>The farm test: red 13 — Breyer's row 13 <span style="font-family:Verdana,sans-serif;font-size:.68rem;letter-spacing:.05em;text-transform:uppercase;color:#fff;background:#8a6d3b;padding:.1rem .5rem;border-radius:.8rem;vertical-align:middle">working page</span></h1>
  <p>Read <b>everything</b> around each red-13 mark — the black numbers with their
     decimals (1. 2. 3. …), the areas (D-S like 1-662, or bare like -1862 / 46), the
     red numbers, the angles in circles — and type what you see under each card,
     comma-separated, with its kind: e.g. <em>"3. / 1-662, -1862 at the edge,
     86°, red 47 nearby"</em>. Nothing to save in the page: read the cards, then
     send the readings to Claude in chat (or as a file).</p>
</header>
<div class="summary">
  <b>Row 13 of the statement</b> (the survey of 1896, doc 6): <b>Shteinbord Iulian</b>
  @@ROWTABLE@@
  In all <b>11 des 103 saz</b>. The 1868 table: 17 des 75, dues 17 r. 75 k.
  (the farm lost land in the 1892 servitude transaction, 4 Morgen returned).
  Breyer's 1875 pencil note for row 13: none. The check: the plots you read,
  grouped by the red-13 marks, should be able to make <b>11 des 103 saz</b>.
</div>
<div class="grid">
@@CARDS@@
</div>
</body>
</html>
"""

def row_to_cells(r):
    cols = ("buildings", "arable", "meadow", "pasture", "unusable", "total")
    des = "".join('<td class="num">%d</td>' % r[c]["des"] for c in cols)
    saz = "".join('<td class="num">%d</td>' % r[c]["saz"] for c in cols)
    return '<tr><td>des</td>%s</tr><tr><td>saz</td>%s</tr>' % (des, saz)

cells = []
for c in cards:
    cells.append(
        '<div class="cell"><h3>Site %d — at (%d, %d) · from the %s</h3>'
        '<img src="%s" alt="red-13 site %d">'
        '<div class="readout">the red-13 mark sits at the centre; mosaic position '
        '(%d, %d)</div></div>'
        % (c["k"] + 1, c["x"], c["y"], c["src"], c["img"], c["k"] + 1, c["x"], c["y"]))
HTML = HTML.replace("@@CARDS@@", "\n".join(cells))
HTML = HTML.replace("@@ROWTABLE@@", row_to_cells(r))
# the summary's totals line, from the data
HTML = HTML.replace("In all <b>11 des 103 saz</b>",
                    "In all <b>%d des %d saz</b>" % (r["total"]["des"], r["total"]["saz"]))
HTML = HTML.replace("should be able to make <b>11 des 103 saz</b>",
                    "should be able to make <b>%d des %d saz</b>" % (r["total"]["des"], r["total"]["saz"]))
with open(OUT, "w", encoding="utf-8") as f:
    f.write(HTML)
print("wrote", OUT, round(len(HTML) / 1e3, 1), "KB")
