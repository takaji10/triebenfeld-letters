# Build the working page: the linked list of the Oleders shown on the
# Pelzucki 1896 map. Reuses the site's viewer (site/assets/maps/) and the
# map layout's DOM conventions; the data (oleders_linked.json +
# farm_locations.json) is embedded. Output: scratch/map4456/oleders_map.html
import json

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld"
LINKED = json.load(open(ROOT + r"\scratch\map4456\oleders_linked.json", encoding="utf-8"))
LOCS = json.load(open(ROOT + r"\scratch\map4456\farm_locations.json", encoding="utf-8"))

SITES = json.load(open(ROOT + r"\scratch\map4456\farm_locations.json", encoding="utf-8"))
TILES = "https://takaji10.github.io/triebenfeld-maps/pelzucki1896/info.json"

# ---- the viewer's labels ----------------------------------------------------
labels = []
sites_by_farm = {}
for s in SITES:
    n = s["n"]
    k = len(sites_by_farm.setdefault(n, []))
    lid = "farm-%d-%d" % (n, k)
    tip = "№ %d · %s" % (n, s["holder"])
    if s["status"] == "supported":
        tip += " — proved by the red figures beside it"
    labels.append({"id": lid, "point": [s["x"], s["y"]],
                   "form": "№ %d" % n, "place_name": s["holder"],
                   "status": s["status"], "conf": s["conf"]})
    sites_by_farm[n].append({"lid": lid, "lon": s["lon"], "lat": s["lat"],
                             "conf": s["conf"], "status": s["status"]})
# the proven stack of farm 84 (the red total read in place)
labels.append({"id": "proof-84", "point": [4751, 5713],
               "form": "№ 84", "place_name":
               "heirs of Shtirtsenbekera — the total 4 des 1684 saz read in place",
               "status": "proof"})
labels.sort(key=lambda l: (l["point"][1], l["point"][0]))

ZELMER = {37, 50, 53, 65, 67}
PROVED = {11: "red 454 = row 11's unusable (0 des 454 saz), unique in the statement",
          78: "red 888 = row 78's meadow (0 des 888 saz); red 936 = row 79's arable",
          84: "the total 4 des 1684 saz read in place (stack 4 over 1684)"}

rows_html = []
n_loc = 0
for e in LINKED:
    n = e["no"]
    ss = sites_by_farm.get(n, [])
    cls = ["frow"]
    if ss:
        cls.append("located")
        n_loc += 1
    else:
        cls.append("unlocated")
    if n in ZELMER:
        cls.append("zelmer")
    if n in PROVED:
        cls.append("proved")
    chips = []
    chip_lid = ss[0]["lid"] if ss else ("proof-%d" % n if n in PROVED else None)
    if chip_lid:
        chips.append('<a class="map-chip" href="#%s" data-label="%s">Locate</a>'
                     % (chip_lid, chip_lid))
    if ss:
        chips.append('<a class="map-chip" href="https://www.openstreetmap.org/?mlat=%s&amp;mlon=%s#map=17/%s/%s" rel="noopener">today</a>'
                     % (ss[0]["lat"], ss[0]["lon"], ss[0]["lat"], ss[0]["lon"]))
    name1868 = e["name_1868"] or "—"
    n1875 = e["holder_1875"]
    chg = e.get("changed", "")
    chg_html = ' <em class="chg" title="the 1868 and 1896 names differ: %s">%s</em>' % (
        chg, chg) if chg not in ("", "same") else ""
    sites_txt = (", ".join("%.5f, %.5f" % (s["lon"], s["lat"]) for s in ss)
                 if ss else "—")
    proof = ('<span class="proof-note">%s</span>' % PROVED[n]) if n in PROVED else ""
    rows_html.append(
        '<li id="row-%d" class="%s">'
        '<span class="fno">№ %d</span> '
        '<span class="f1868">%s%s</span>'
        '<span class="fmeta">1868: %s Morgen %s rods · dues %s · 1894: %s</span>'
        '<span class="fbreyer">1875 (Breyer): %s</span>'
        '<span class="f1896">1896: %s · %s</span>'
        '<span class="fsites">map: %s</span>%s'
        '<span class="map-chips">%s<a class="map-chip" href="/sources/apl399806603/">the holding</a></span>'
        '</li>' % (
            n, " ".join(cls), n, name1868, chg_html,
            e["morgen_1868"] if e["morgen_1868"] is not None else "?",
            e["rods_1868"] if e["rods_1868"] is not None else "?",
            e["dues_1868"] or "?", e["land_serv_1894"] or "—",
            n1875 or "—", e["name_1896"] or "—", e["total_1896"] or "—",
            sites_txt, proof, "".join(chips)))

MAPDATA = json.dumps({"tiles": TILES, "labels": labels}, ensure_ascii=False)

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pełzucki 1896 — the linked list of the Olęders (working page)</title>
<style>
:root { --rule: #d8d2c4; --ink: #2a2620; --ink-soft: #6b6459; --ink-faint: #9a9384;
        --accent: #8a3324; --bg: #faf8f3; }
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--ink);
       font-family: Georgia, 'Times New Roman', serif; line-height: 1.5; }
a { color: var(--accent); }
header.workhead { max-width: 120rem; margin: 0 auto; padding: 1.2rem 2rem .4rem; }
header.workhead h1 { font-size: 1.35rem; margin: 0 0 .2rem; }
header.workhead p { margin: .15rem 0; font-size: .88rem; color: var(--ink-soft); }
.tag { font-family: Verdana, sans-serif; font-size: .68rem; letter-spacing: .05em;
       text-transform: uppercase; color: #fff; background: #8a6d3b;
       padding: .1rem .5rem; border-radius: .8rem; vertical-align: middle; }
.map-columns { display: grid; grid-template-columns: minmax(24rem, 30rem) minmax(0, 1fr);
               gap: 1.6rem; align-items: start; max-width: 120rem; margin: 0 auto;
               padding: 0 2rem 2rem; }
.map-side { max-height: 92vh; overflow-y: auto; padding-right: .4rem; }
.map-stage { position: sticky; top: .8rem; }
.map-viewer { width: 100%; height: min(86vh, 60rem); background: #f4f1ea;
              border: 1px solid var(--rule); touch-action: none; position: relative; }
.map-status { font-family: Verdana, sans-serif; font-size: .85rem; color: #b33; }
.map-tools { display: flex; gap: .8rem; align-items: center; margin-top: .4rem;
             font-family: Verdana, sans-serif; font-size: .82rem; }
.filters { font-family: Verdana, sans-serif; font-size: .8rem; color: var(--ink-soft);
           display: flex; gap: 1rem; align-items: center; margin: .6rem 0 .2rem; }
.keybox { font-family: Verdana, sans-serif; font-size: .78rem; color: var(--ink-soft);
          border: 1px solid var(--rule); border-radius: .4rem; padding: .6rem .8rem;
          margin: .6rem 0 1rem; }
.keybox b { font-weight: 600; }
.proofblock { border: 1px solid #4d7c4d; border-radius: .4rem; padding: .6rem .8rem;
              margin: 0 0 1rem; font-size: .86rem; }
.proofblock h2 { font-size: .95rem; margin: 0 0 .3rem; color: #2f5e2f; }
.proofblock ul { margin: .2rem 0 0; padding-left: 1.1rem; }
.marklist { list-style: none; margin: 0; padding: 0; font-size: .88rem; }
.frow { padding: .5rem .5rem .5rem .6rem; border-bottom: 1px solid var(--rule);
        border-left: 3px solid transparent; }
.frow.unlocated { color: var(--ink-faint); }
.frow.unlocated .f1868, .frow.unlocated .f1896 { color: var(--ink-faint); }
.frow.zelmer { background: rgba(138, 109, 59, .10); }
.frow.proved { border-left-color: #3d7a3d; }
.frow.is-on { background: rgba(180, 60, 50, .10); border-left-color: var(--accent); }
body.hide-unlocated .frow.unlocated { display: none; }
.fno { font-family: Verdana, sans-serif; font-weight: 700; font-size: .95rem;
       display: inline-block; min-width: 2.6rem; }
.f1868 { font-weight: 600; }
.fmeta, .fbreyer, .f1896, .fsites, .proof-note { display: block;
       font-family: Verdana, sans-serif; font-size: .74rem; color: var(--ink-soft); }
.f1896 { color: var(--ink); }
.chg { font-family: Verdana, sans-serif; font-size: .7rem; color: #b33;
       font-style: normal; }
.map-chips { display: inline-flex; flex-wrap: wrap; gap: .3rem; margin-top: .25rem; }
.map-chip { font-family: Verdana, sans-serif; font-size: .68rem; padding: 0 .5rem;
            border: 1px solid var(--rule); border-radius: 1rem; color: var(--ink-soft);
            text-decoration: none; white-space: nowrap; }
.map-chip:hover { border-color: var(--accent); color: var(--accent); }
/* the marks on the map (the site's own classes, this page's additions) */
.map-mark { box-sizing: border-box; width: 15px; height: 15px; margin: 0;
            border: 2px solid #b33; border-radius: 50%;
            background: rgba(255,255,255,.55); cursor: pointer; }
.map-mark.is-on, .map-mark:hover { background: #b33; }
.map-mark-proof { border-radius: 0; border-color: #3d7a3d;
                  background: rgba(214, 240, 214, .8); }
.map-mark-proof.is-on, .map-mark-proof:hover { background: #3d7a3d; }
.map-tip { position: fixed; transform: translateX(-50%);
           background: rgba(40,36,30,.92); color: #fff; font-family: Verdana, sans-serif;
           font-size: .78rem; padding: .25rem .55rem; border-radius: 3px;
           white-space: nowrap; pointer-events: none; z-index: 60; }
.map-boundary-canvas { position: absolute; inset: 0; pointer-events: none; z-index: 5; }
@media (max-width: 64rem) { .map-columns { grid-template-columns: 1fr; }
  .map-stage { position: static; order: -1; } .map-side { max-height: none; } }
</style>
</head>
<body>
<header class="workhead">
  <h1>Pełzucki 1896 — the linked list of the Olęders <span class="tag">working page</span></h1>
  <p>Claude's working material of 2026-11-01 (scratch/map4456/), not a page of the edition.
     The farm numbers are the rows of the liquidation table; the marks are the black
     numbers read on the mosaic by OCR — candidates, two of them proved by the red
     figures beside them. Read a mark's number, and the row gives the holder across
     the tables: the 1868 table, the 1869 copy, Breyer's 1875 pencil notes, the 1894
     inscription's Morgen, the 1896 survey.</p>
  <p>Documents: <a href="/sources/apl399806603/">APŁ 39/98/0/-/6603 — the liquidation table of Łazińsk and its copies</a>
     · <a href="/sources/app539680716/">APP 53/968/0/-/716 — Breyer's Łazińsk notebook</a>
     · the map's page: <a href="/maps/pelzucki1896/">Pełzucki 1896</a>.</p>
</header>

<div class="map-columns">
  <div class="map-side">
    <div class="filters">
      <label><input type="checkbox" id="f-located"> only the rows with map sites</label>
      <span id="f-count"></span>
    </div>
    <div class="keybox">
      <b>The map's system:</b> black number = the farm's row in the tables;
      red = that parcel's area in desiatinas/sazhens (written stacked, des over saz).
      A number recurs because every parcel of the farm carries it.
      <b>Green marks</b> are proved by the red figures; blue-black circles are candidates.
      Rows tinted brown are the <b>Zelmer farms</b>; a red left edge marks a proved farm.
    </div>
    <div class="proofblock">
      <h2>The proved parcels</h2>
      <ul>
        <li><b>№ 78 · Želchak Foma</b> — 17.87796 E, 52.10876 N; red 888 (his meadow,
            unique in the statement) and red 936 (row 79's arable) beside the mark.</li>
        <li><b>№ 11 · Grunvald Kristof</b> — 17.95456 E, 52.09687 N; red 454
            (his unusable, unique) 30 px from the mark.</li>
        <li><b>№ 84 · heirs of Shtirtsenbekera</b> — 17.88197 E, 52.11131 N;
            the total 4/1684 read as a stack in place.</li>
      </ul>
    </div>
    <ol class="marklist">
@@ROWS@@
    </ol>
  </div>

  <div class="map-stage">
    <div id="map-viewer" class="map-viewer" style="aspect-ratio: 21715 / 14206;"></div>
    <div class="map-tools">
      <span>the marks sit where the black numbers were read on the mosaic
        (21715 × 14206 px)</span>
    </div>
    <p class="map-status" id="map-status" hidden></p>
  </div>
</div>

<script id="map-data" type="application/json">@@MAPDATA@@</script>
<script src="/site/assets/maps/openseadragon.min.js"></script>
<script src="/site/assets/maps/map-viewer.js"></script>
<script>
(function () {
  var M = JSON.parse(document.getElementById('map-data').textContent);
  var statusOf = {};
  M.labels.forEach(function (l) { statusOf[l.id] = l.status; });
  // restyle the proved marks once the overlays exist
  var viewer = OpenSeadragon.getViewer(document.getElementById('map-viewer'));
  viewer.addHandler('open', function () {
    document.querySelectorAll('.map-mark').forEach(function (d) {
      var lid = d.getAttribute('data-label');
      if (statusOf[lid] === 'supported' || statusOf[lid] === 'proof') {
        d.classList.add('map-mark-proof');
      }
    });
  });
  // a mark click highlights and scrolls to the farm's row
  // (the stock viewer's own row-lookup targets the edition's DOM, absent here)
  document.addEventListener('click', function (ev) {
    var m = ev.target.closest ? ev.target.closest('.map-mark') : null;
    if (!m) return;
    var lid = m.getAttribute('data-label') || '';
    var n = parseInt(lid.split('-')[1], 10);
    var row = document.getElementById('row-' + n);
    if (!row) return;
    document.querySelectorAll('.frow.is-on').forEach(function (r) {
      r.classList.remove('is-on'); });
    row.classList.add('is-on');
    row.scrollIntoView({ block: 'center', behavior: 'smooth' });
  });
  // the filter
  var cb = document.getElementById('f-located');
  var cnt = document.getElementById('f-count');
  var rows = document.querySelectorAll('.frow');
  var nLoc = document.querySelectorAll('.frow.located').length;
  cnt.textContent = nLoc + ' of ' + rows.length + ' rows located';
  cb.addEventListener('change', function () {
    document.body.classList.toggle('hide-unlocated', cb.checked);
  });
})();
</script>
</body>
</html>
"""

HTML = HTML.replace("@@ROWS@@", "\n".join(rows_html))
HTML = HTML.replace("@@MAPDATA@@", MAPDATA)
out = ROOT + r"\scratch\map4456\oleders_map.html"
with open(out, "w", encoding="utf-8") as f:
    f.write(HTML)
print("wrote", out, len(HTML), "bytes;", len(labels), "labels,", len(rows_html), "rows,", n_loc, "located")
