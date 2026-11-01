# The farm test: one farm (row 47, Zeer Kristiian, 9 red sites) on a page
# of crops - every red-47 site shown large, plus a wide view of each
# neighbourhood (so the editor can read every black number, red number and
# angle in the fields around the sites). The editor reads; Claude checks
# against the statement. Output: scratch/map4456/farm_test_47.html
import base64
import io
import json

import numpy as np
import pyvips
import PIL.Image

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld"
FULL = (r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)"
        r"\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456\4456_full.jpg")
OUT = ROOT + r"\scratch\map4456\farm_test_47.html"

D = json.load(open(ROOT + r"\scratch\map4456\reds_all.json", encoding="utf-8"))

def canon(t):
    t = t.strip()
    t = t.replace("[", "").replace("?]", "").replace("?", "")
    return t.strip()

FARM = 47
sites = []
for a in D["answered"]:
    if canon(a["text"]) == str(FARM):
        x, y = a["x"], a["y"]
        if a.get("fixed"):
            x = a["fixed"]["x"]; y = a["fixed"]["y"]
        sites.append({"x": x, "y": y, "src": "sheet"})
for n in D["added"]:
    if canon(n["text"]) == str(FARM):
        sites.append({"x": n["x"] + (n.get("w", 0)) // 2,
                      "y": n["y"] + (n.get("h", 0)) // 2, "src": "added"})
print("red-%d sites:" % FARM, len(sites))

im = pyvips.Image.new_from_file(FULL, access="random")
W, H = im.width, im.height
cards = []
for k, s in enumerate(sites):
    # the neighbourhood: 700 px square, shown at 2x
    R = 350
    cx, cy = s["x"], s["y"]
    l = max(0, cx - R); t = max(0, cy - R)
    r_ = min(W, cx + R); b_ = min(H, cy + R)
    a = np.frombuffer(im.crop(l, t, r_ - l, b_ - t).write_to_memory(),
                      np.uint8).reshape(b_ - t, r_ - l, 3)
    buf = io.BytesIO()
    PIL.Image.fromarray(a).save(buf, "JPEG", quality=88)
    cards.append({"k": k, "x": cx, "y": cy, "src": s["src"],
                  "img": "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(),
                  "ox": l, "oy": t, "cw": r_ - l, "ch": b_ - t,
                  "bx": cx - l, "by": cy - t})
print("cards:", len(cards))

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Pełzucki 1896 — the farm test: red 47 (working page)</title>
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
           border: 1px solid var(--rule); border-radius: .4rem;
           font-size: .9rem; }
.summary b { font-family: Verdana, sans-serif; }
</style>
</head>
<body>
<header>
  <h1>The farm test: red 47 — Zeer Kristiian <span style="font-family:Verdana,sans-serif;font-size:.68rem;letter-spacing:.05em;text-transform:uppercase;color:#fff;background:#8a6d3b;padding:.1rem .5rem;border-radius:.8rem;vertical-align:middle">working page</span></h1>
  <p>The statement's row 47: <b>Zeer Kristiian</b>, 26 desiatinas 1922 sazhens in all
     (buildings 0/300 · arable 6/661 · meadow 1/564 · pasture 4/2169 · unusable 0/673),
     dues 22 r. 227 k., 4 Morgen for the servitudes of 1894, the name unchanged in
     1896. Nine red-47 sites stand in your catalogue; each card shows one site's
     neighbourhood (700 px square, the red-47 mark at centre). Read <b>everything</b>
     around each site — the black numbers (with their decimals, 1. 2. 3. …), the
     areas (D-S, bare numbers), the red numbers, the angles — and type what you see
     into the box under each card; your readings are checked against the row.</p>
</header>
<div class="summary">
  <b>The test:</b> if the black "n." decimals are the plot numbers within the farm,
  the plots' areas should sum to the row's total (26 des 1922 saz) when grouped by
  the red-47 marks — and the counts should make sense (the statement's five land
  kinds). Type per card, comma-separated: every figure you see, black or red, with
  its kind (e.g. "3. / 1-662, -1862 at edge, red 47, 86°").
</div>
<div class="grid">
@@CARDS@@
</div>
<script>
// nothing to compute here: the readings go to Claude via the exported text
</script>
</body>
</html>
"""

cells = []
for c in cards:
    cells.append(
        '<div class="cell"><h3>Site %d — at (%d, %d) · from the %s</h3>'
        '<img src="%s" alt="site %d">'
        '<div class="readout">the red-47 mark sits at the centre; mosaic position '
        '(%d, %d)</div></div>'
        % (c["k"] + 1, c["x"], c["y"], c["src"], c["img"], c["k"] + 1, c["x"], c["y"]))
HTML = HTML.replace("@@CARDS@@", "\n".join(cells))
with open(OUT, "w", encoding="utf-8") as f:
    f.write(HTML)
print("wrote", OUT, round(len(HTML) / 1e3, 1), "KB")
