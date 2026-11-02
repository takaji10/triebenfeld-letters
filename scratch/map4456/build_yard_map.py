# The homestead-yard map, v2 — the editor's flow:
#   1. click a farm number (a red mark on the map) -> it becomes the active
#      farm (the panel shows the row's holder and total, NOT the buildings
#      figure — the yard read stays blind)
#   2. draw mode turns on; drag a box around the black "n. / n" figure
#   3. type the area as written (uncertainty in [..?]); Enter links it
# The farm comes only from the clicked mark; the pair is saved with the
# mark's position (the evidence of which red n was clicked).
# v3: a red tag's number can be set right in the page — click the tag, type
# the correct number in the change field, Enter. The fixes live in the
# browser's localStorage keyed by the mark's mosaic position ("x,y" — stable
# across rebuilds, since the marks come from reds_all.json) and ride along
# in the Export JSON as "red_fixes". An empty field + Enter reverts the fix.
# Output: scratch/map4456/yard_map.html
import json
import os
import shutil
import subprocess
import sys

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld"
TILES = "https://takaji10.github.io/triebenfeld-maps/pelzucki1896/info.json"
D = json.load(open(ROOT + r"\scratch\map4456\reds_all.json", encoding="utf-8"))
REF = json.load(open(ROOT + r"\scratch\map4456\reference_numbers.json", encoding="utf-8"))

def canon(t):
    t = t.strip().replace("[", "").replace("?]", "").replace("?", "")
    return t.strip()

refs = []
def add_ref(raw, x, y, ocr):
    c = canon(raw)
    if not c.isdigit():
        return
    # keep the read's own uncertainty: '[33?]' stays '[33?]' on the map
    n = raw.strip() if ("?" in raw or "[" in raw) else int(c)
    refs.append({"n": n, "x": x, "y": y, "ocr": ocr})

for a in D["answered"]:
    x, y = a["x"], a["y"]
    if a.get("fixed"):
        x = a["fixed"]["x"]; y = a["fixed"]["y"]
    # from the spot sheet: a human read the crop and typed this
    add_ref(a["text"], x, y, False)
for m in D["added"]:
    # from the OCR pass itself: never confirmed by a human
    add_ref(m["text"], m["x"] + (m.get("w", 0)) // 2,
            m["y"] + (m.get("h", 0)) // 2, True)
# the row facts the panel shows (holder, total — not the buildings figure)
rows = {}
for k, r in REF["statement"].items():
    if k.isdigit():
        rows[int(k)] = {"name": r["name"],
                        "td": r["total"]["des"], "ts": r["total"]["saz"]}
print("red reference marks:", len(refs),
      "- OCR-only (purple):", sum(1 for r in refs if r["ocr"]))

# ---- the rulings: run the yard analysis on the latest export, and the ------
# ---- verdicts ride into the page as data (green solid, yellow weak,     ----
# ---- red wrong) with a why-text for the sidebar's Ruling box            ----
dl = r"C:\Users\Tersnaus\Downloads\yards_read.json"
dst = ROOT + r"\scratch\map4456\yards_read.json"
try:
    if os.path.exists(dl) and (not os.path.exists(dst) or
                               os.path.getmtime(dl) > os.path.getmtime(dst)):
        shutil.copyfile(dl, dst)
        print("yards_read.json refreshed from Downloads")
except OSError:
    pass
# the tag fixes relink the yards anchored to the fixed mark (the fix record
# is the evidence of which tag the yard was saved against) — the browser
# relinks live since v7; this catches exports made before a reload
try:
    EX = json.load(open(dst, encoding="utf-8"))
    _moved = 0
    for k, v in (EX.get("red_fixes") or {}).items():
        if not str(v).isdigit():
            continue
        xs, ys = k.split(",")
        x, y = int(xs), int(ys)
        for yy in EX.get("yards", []):
            if yy.get("farm") != v and yy.get("rx") == x and yy.get("ry") == y:
                yy["farm"] = int(v)
                _moved += 1
    if _moved:
        json.dump(EX, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("yards relinked by the tag fixes:", _moved)
except Exception as e:
    print("relink pass skipped:", e)
# the export's tag fixes are baked into the page's tags: the export is the
# record of truth, so the page shows the corrected numbers without waiting
# for the browser's localStorage (which re-applies its own on top — the same
# values). The catalogue read rides along as "orig" for the tooltip.
try:
    _fx = EX.get("red_fixes", {})
    _nbaked = 0
    for r in refs:
        k = str(r["x"]) + "," + str(r["y"])
        if k in _fx:
            v = _fx[k]
            if "orig" not in r:
                r["orig"] = r["n"]
            r["n"] = v if isinstance(v, str) else int(v)
            r["ocr"] = False
            _nbaked += 1
    if _nbaked:
        print("tag fixes baked into the page:", _nbaked)
except Exception as e:
    print("fix baking skipped:", e)
try:
    subprocess.run([sys.executable, ROOT + r"\scratch\map4456\yard_analysis.py"],
                   check=True, capture_output=True, cwd=ROOT + r"\scratch\map4456")
    AN = json.load(open(ROOT + r"\scratch\map4456\yard_analysis.json",
                        encoding="utf-8"))
except Exception as e:
    print("yard analysis unavailable:", e)
    AN = {"groups": []}

ST = REF["statement"]
def bfig(row):
    b = row["buildings"]
    return b["des"] * 2400 + b["saz"]

def ruling(g):
    v = g.get("verdict") or ""
    farm = g["farm"]
    b = bfig(ST[str(farm)]) if isinstance(farm, int) and str(farm) in ST else None
    notes = g.get("notes", [])
    cands = g.get("candidates", [])
    exact = sorted([c for c in cands if c.get("kind") == "exact"],
                   key=lambda c: c["dist"] if c.get("dist") is not None else 10**9)
    nearc = [c for c in cands if c.get("kind") == "near-claim"]
    near = sorted([c for c in cands if c.get("kind") == "near"],
                  key=lambda c: c.get("edits", 9))
    if v == "confirmed":
        t = "<b>Solid.</b> The yard figure is exactly this row's buildings figure (%s saz)." % b
    elif v == "confirmed-sum":
        t = "<b>Solid.</b> The yard's pieces sum exactly to this row's buildings figure (%s saz)." % b
    elif v == "confirmed-weak":
        t = "<b>Weak.</b> The read is uncertain ([..?]) but it agrees with the row's buildings figure (%s saz)." % b
    elif v == "confirmed-sum-weak":
        t = "<b>Weak.</b> The pieces sum to the row's buildings figure (%s saz), but a read in the sum is uncertain." % b
    elif v == "sum-near":
        t = "<b>Near-fit.</b> %s Likely one stroke in one of the reads — trustworthy, verify on sight." % (
            notes[0] if notes else "The pieces come close to the row's figure.")
    elif exact:
        c = exact[0]
        d = (", nearest site %s px away" % c["dist"]) \
            if c.get("dist") is not None else ""
        t = "<b>Wrong claim?</b> The figure is exactly row %d's (%s) buildings figure%s. Forest pieces carry foreign numbers — check the neighbouring parcels before ruling." % (
            c["row"], c["name"], d)
    elif v == "no-match":
        t = "<b>Contradiction.</b> As read, the figure is no row's buildings figure — the read or the claim is wrong."
    elif v == "impossible":
        t = "<b>Impossible.</b> This row records no buildings figure at all, so the read cannot belong to it."
    elif nearc and not near:
        t = "<b>Probable slip.</b> The figure is one digit from this row's own buildings figure (%s saz) — likely the same yard misread." % b
    elif v == "open-gap":
        t = "<b>Open.</b> %s" % (notes[0] if notes else
                                 "An unread [?] piece could carry the rest.")
    elif v in ("open", "open-weak"):
        t = "<b>Untested.</b> The reads are uncertain; nothing closes the test, nothing contradicts the claim."
    elif v == "unreadable":
        t = "<b>Untestable.</b> No readable figure in the yard's pieces."
    elif v == "claim-uncertain":
        t = "<b>Untestable.</b> The farm claim itself is uncertain."
    else:
        t = ""
    for n in notes:
        if v not in ("sum-near", "open-gap"):   # the note is already folded in
            t += " " + n
    if (exact or near) and v not in ("confirmed", "confirmed-sum"):
        bits = []
        for c in (exact + near)[:3]:
            d = (", %s px" % c["dist"]) if c.get("dist") is not None else ""
            bits.append("row %d %s%s" % (c["row"], c["name"], d))
        t += " Other rows in view: " + "; ".join(bits) + "."
    return t

def colour(g):
    v = g.get("verdict") or ""
    cands = g.get("candidates", [])
    if v in ("confirmed", "confirmed-sum"):
        return "ok"
    if v == "sum-near":
        return "ok2"
    if v in ("confirmed-weak", "confirmed-sum-weak"):
        return "warn"
    if any(c.get("kind") == "exact" for c in cands):
        return "bad"
    if v in ("no-match", "impossible"):
        return "bad"
    if any(c.get("kind") == "near-claim" for c in cands) and \
       not any(c.get("kind") == "near" for c in cands):
        return "warn"
    return ""

VERD = {}
for g in AN.get("groups", []):
    w = ruling(g)
    c = colour(g)
    if w or c:
        VERD[str(g["farm"])] = {"c": c, "w": w}
from collections import Counter
cc = Counter(x["c"] or "none" for x in VERD.values())
print("rulings:", dict(cc))

# the uncertain-numbers queue: every red tag whose read carries [?] — with
# the neighbouring confident tags as context (value, distance, site count)
# and a suggested reading from the nearest neighbours
RAD = 1200
UQ = []
for r in refs:
    if not isinstance(r["n"], str):
        continue                      # a confident read — not in the queue
    neigh = {}
    for q in refs:
        if q is r or not isinstance(q["n"], int):
            continue
        d = abs(q["x"] - r["x"]) + abs(q["y"] - r["y"])
        if d > RAD:
            continue
        e = neigh.get(q["n"])
        if e is None:
            neigh[q["n"]] = [d, 1]
        else:
            e[1] += 1
            if d < e[0]:
                e[0] = d
    ns = sorted((v[0], k, v[1]) for k, v in neigh.items())[:6]
    UQ.append({
        "key": str(r["x"]) + "," + str(r["y"]),
        "read": r["n"], "x": r["x"], "y": r["y"], "ocr": bool(r.get("ocr")),
        "neigh": [{"n": k, "d": d, "c": c} for d, k, c in ns],
        "sugg": [k for d, k, c in ns[:3]],
    })
UQ.sort(key=lambda u: (u["y"], u["x"]))
print("uncertain numbers in the queue:", len(UQ))


HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Pełzucki 1896 — the homestead yards (working page)</title>
<style>
:root { --rule: #d8d2c4; --ink: #2a2620; --ink-soft: #6b6459; --accent: #8a3324; }
body { margin: 0; background: #faf8f3; color: var(--ink); font-family: Georgia, serif; }
header { max-width: 120rem; margin: 0 auto; padding: .9rem 2rem .2rem; }
header h1 { font-size: 1.2rem; margin: 0 0 .2rem; }
header p { font-size: .85rem; color: var(--ink-soft); margin: .15rem 0; }
kbd { font-family: Verdana, sans-serif; font-size: .72rem; border: 1px solid var(--rule);
      border-radius: 3px; padding: 0 .35rem; background: #fff; }
.cols { display: grid; grid-template-columns: minmax(19rem, 23rem) minmax(0, 1fr);
        gap: 1.4rem; align-items: start; max-width: 120rem; margin: 0 auto;
        padding: 0 2rem 2rem; }
.side { max-height: 92vh; overflow-y: auto; font-family: Verdana, sans-serif;
        font-size: .82rem; }
.box { border: 1px solid var(--rule); border-radius: .4rem; padding: .7rem .9rem;
       margin: 0 0 .8rem; }
.box h2 { font-size: .9rem; margin: 0 0 .4rem; }
#area, #note, #fixnum { font-size: 1rem; padding: .3rem .5rem;
                        border: 1px solid var(--rule); }
#area { width: 9rem; } #note { width: 11rem; } #fixnum { width: 7rem; }
.activefarm { font-size: .95rem; margin: .3rem 0; line-height: 1.35;
              /* two reserved lines: the buttons and fields below stay put
                 however the farm's line wraps */
              min-height: 2.8rem; }
.activefarm b { font-size: 1.05rem; }
.btn { font-family: Verdana, sans-serif; font-size: .78rem; padding: .3rem .8rem;
       border: 1px solid var(--rule); background: #fff; cursor: pointer;
       border-radius: 3px; margin: 0 .3rem .3rem 0; }
.btn.primary { background: var(--accent); color: #fff; border-color: var(--accent); }
.btn.on { background: #2a6db3; color: #fff; border-color: #2a6db3; }
.alist { list-style: none; margin: .4rem 0 0; padding: 0; max-height: 24rem;
         overflow-y: auto; }
.alist li { display: flex; gap: .5rem; align-items: baseline; padding: .2rem 0;
            border-bottom: 1px solid var(--rule); cursor: pointer; }
.alist li:hover { background: rgba(42,109,179,.06); }
.alist li.selrow { background: rgba(42,109,179,.14); }
.alist .v { font-weight: 700; color: #1d4f7c; min-width: 6.5rem; }
.alist .xy { color: var(--ink-soft); font-size: .72rem; }
.alist button { margin-left: auto; font-size: .7rem; }
.hint { color: var(--ink-soft); font-size: .76rem; }
.viewer { width: 100%; height: min(88vh, 62rem); background: #f4f1ea;
          border: 1px solid var(--rule); touch-action: none; position: relative; }
.stage { position: sticky; top: .8rem; }
.yard-label { box-sizing: border-box; display: flex; align-items: center;
              justify-content: center; min-width: 30px; height: 24px; padding: 0 6px;
              font-family: Verdana, sans-serif; font-weight: 700; font-size: 13px;
              border-radius: 4px; background: rgba(42,109,179,.92); color: #fff;
              border: 2px solid #1d4f7c; white-space: nowrap;
              pointer-events: auto; z-index: 9; cursor: pointer; }
.yard-label.sel { outline: 3px solid #8a3324; outline-offset: 1px; }
.yard-label.ok { background: rgba(46,125,50,.92); border-color: #1b5e20; }
.yard-label.warn { background: rgba(235,185,40,.95); border-color: #8a6d1a;
                   color: #2a2620; }
.yard-label.ok2 { background: rgba(139,195,74,.95); border-color: #5b8a22;
                  color: #1f2a10; }
.yard-label.bad { background: rgba(179,54,44,.94); border-color: #7e211a; }
.ref-label { box-sizing: border-box; min-width: 17px; height: 17px; padding: 0 3px;
             display: flex; align-items: center; justify-content: center;
             font-family: Verdana, sans-serif; font-size: 10px; font-weight: 700;
             color: rgba(140,40,40,.85);
             border: 1px solid transparent; border-radius: 3px;
             background: rgba(255,255,255,.55);
             pointer-events: auto; z-index: 5; cursor: pointer; }
.ref-label.unc { color: #5a4a10; border: 1px dashed #8a6d1a;
                 background: #f0cf3e; }
.ref-label.sel { outline: 3px solid #1d4f7c; outline-offset: 1px; }
.rubber { position: absolute; border: 2px dashed #1d4f7c;
          background: rgba(42,109,179,.10); pointer-events: none; z-index: 7; }
.draw-capture { position: absolute; inset: 0; z-index: 8; cursor: crosshair;
                display: none; touch-action: none; }
@media (max-width: 64rem) { .cols { grid-template-columns: 1fr; }
  .stage { position: static; order: -1; } }
</style>
</head>
<body>
<header>
  <h1>Pełzucki 1896 — the homestead yards <span style="font-family:Verdana,sans-serif;font-size:.72rem;color:#8a6d3b">(v7 · rulings, uncertain numbers' queue)</span>
    <span style="font-family:Verdana,sans-serif;font-size:.68rem;letter-spacing:.05em;text-transform:uppercase;color:#fff;background:#8a6d3b;padding:.1rem .5rem;border-radius:.8rem;vertical-align:middle">working page</span></h1>
  <p class="hint"><kbd>D</kbd> pan/draw &middot; <kbd>L</kbd> labels &middot;
     <kbd>N</kbd> change a number &middot; <kbd>A</kbd> add a number &middot;
     <kbd>Enter</kbd> save / next &middot; <kbd>Esc</kbd> clear</p>
</header>
</header>
<div class="cols">
  <div class="side">
    <div class="box">
      <h2>Layers</h2>
      <p>
        <button class="btn on" id="show-refs">farm numbers</button>
        <button class="btn" id="show-yards">your yards</button>
        <button class="btn on" id="show-all">all (L)</button>
      </p>
    </div>
    <div class="box">
      <h2>Active farm</h2>
      <div class="activefarm" id="activefarm">none — click a red tag on the map</div>
      <p>
        <button class="btn" id="modebtn">Draw mode (D)</button>
      </p>
      <p style="margin:.2rem 0 .4rem">
        <input id="area" placeholder="1. area as written" autocomplete="off"
               spellcheck="false"></p>
      <p style="margin:.2rem 0 .4rem"><input id="note" placeholder="note (optional)"></p>
      <p style="margin:.2rem 0 .4rem">
        <input id="fixnum" placeholder="the right number" autocomplete="off"
               spellcheck="false" inputmode="numeric">
        <button class="btn" id="numbtn">change (N)</button>
        <button class="btn" id="addbtn">add a number (A)</button></p>
      <p class="hint" id="modehint">click a farm number, then drag the box, then
        Enter</p>
    </div>
    <div class="box">
      <h2>Ruling <span class="hint">(from your last export)</span></h2>
      <p class="hint" style="margin:.1rem 0 .3rem">
        <span style="color:#2e7d32;font-weight:700">green</span> solid &middot;
        <span style="color:#7cb342;font-weight:700">light green</span> near-fit &middot;
        <span style="color:#8a6d1a;font-weight:700">yellow</span> weak &middot;
        <span style="color:#b3362c;font-weight:700">red</span> wrong or contradicting</p>
      <div class="hint" id="ruling">click a yard label or a red tag &mdash; the ruling shows here</div>
    </div>
    <div class="box">
      <h2>Uncertain numbers <span id="ucount"></span></h2>
      <ul class="alist" id="ulist" style="max-height:18rem"></ul>
      <p class="hint" id="uhint" style="margin:.3rem 0 0"></p>
      <p style="margin:.3rem 0 0">
        <input id="unote" placeholder="comment (optional)" style="font-size:1rem;
               padding:.3rem .5rem;border:1px solid var(--rule);width:9rem">
        <button class="btn" id="uok">read is right (Enter)</button>
        <button class="btn" id="ubtn">use suggestion</button>
        <button class="btn" id="uunc">uncertain</button>
        <button class="btn" id="uclr">clear marks</button>
      </p>
    </div>
    <div class="box">
      <h2>Your yards <span id="ncount"></span></h2>
      <ul class="alist" id="alist"></ul>
      <p style="margin:.5rem 0 0">
        <button class="btn primary" id="export">Export JSON</button>
        <button class="btn" id="del">Delete selected</button>
      </p>
    </div>
  </div>
  <div class="stage">
    <div id="viewer" class="viewer"></div>
    <p class="hint" style="font-family:Verdana,sans-serif;margin-top:.4rem">
      positions in the mosaic's pixels (21715 &times; 14206)</p>
  </div>
</div>
<script id="ref-data" type="application/json">@@REFS@@</script>
<script id="row-data" type="application/json">@@ROWS@@</script>
<script id="verdict-data" type="application/json">@@VERDICTS@@</script>
<script id="uncertain-data" type="application/json">@@UNCERTAIN@@</script>
<script src="/site/assets/maps/openseadragon.min.js"></script>
<script>
(function () {
  var REFS = JSON.parse(document.getElementById('ref-data').textContent);
  var ROWS = JSON.parse(document.getElementById('row-data').textContent);
  var VERD = JSON.parse(document.getElementById('verdict-data').textContent);
  var UQ = JSON.parse(document.getElementById('uncertain-data').textContent);
  var K_NEW = 'p1896-yards-v1';
  var yards = [];
  try { yards = JSON.parse(localStorage.getItem(K_NEW) || '[]'); } catch (e) {}
  // the corrected red numbers, keyed by the mark's mosaic position ("x,y" —
  // stable across rebuilds): the read of the tag can be set right in the page
  var K_FIX = 'p1896-redfix-v1';
  var fixes = {};
  try { fixes = JSON.parse(localStorage.getItem(K_FIX) || '{}'); } catch (e) {}
  function fixKey(r) { return r.x + ',' + r.y; }
  REFS.forEach(function (r) {
    // a baked fix keeps its catalogue read as orig; otherwise orig is the
    // read as embedded
    if (typeof r.orig === 'undefined') r.orig = r.n;
    // a stored fix marks the mark reviewed — even when the fix agrees with
    // the OCR read (a confirm in the review keeps it out of the purple set)
    if (fixes[fixKey(r)] !== undefined) { r.n = fixes[fixKey(r)]; r.ocr = false; }
  });
  // the numbers added in the page (the catalogue missed them), each stored
  // with its mosaic position; "[?]" until a number is typed for it
  var K_ADD = 'p1896-redadd-v1';
  var added = [];
  try { added = JSON.parse(localStorage.getItem(K_ADD) || '[]'); } catch (e) {}
  function persistAdded() {
    try { localStorage.setItem(K_ADD, JSON.stringify(added)); } catch (e) {}
  }
  added.forEach(function (m) {
    REFS.push({ n: m.n, orig: '[?]', x: m.x, y: m.y, added: true });
  });
  var sel = -1, drawMode = false, activeFarm = null, addMode = false;
  var layers = { refs: true, yards: false };   // the Layers buttons' state

  var viewer = OpenSeadragon({
    id: 'viewer', prefixUrl: '', showNavigationControl: false,
    tileSources: '@@TILES@@', crossOriginPolicy: 'Anonymous',
    maxZoomPixelRatio: 6, visibilityRatio: 0.5, animationTime: 0.5,
    gestureSettingsMouse: { clickToZoom: false, dblClickToZoom: true }
  });
  var world = null;
  viewer.addHandler('open', function () {
    world = viewer.world.getItemAt(0); drawAll();
  });

  var ovs = [];
  function drawAll() {
    ovs.forEach(function (o) { viewer.removeOverlay(o.el); });
    ovs = [];
    if (layers.refs) {
      REFS.forEach(function (r) {
        var d = document.createElement('div');
        // yellow: the read itself carries [?]; otherwise red ink on a
        // semi-transparent white ground — corrections stay applied in the
        // data but no longer colour the tag (the marking session reads the
        // map as the surveyor left it)
        d.className = 'ref-label' +
          (typeof r.n === 'string' ? ' unc' : '') +
          (activeFarm && activeFarm.n === r.n &&
           activeFarm.x === r.x && activeFarm.y === r.y ? ' sel' : '');
        d.textContent = r.n;
        d.title = 'farm ' + r.n +
          (r.added ? ' (added here)'
                   : (r.n !== r.orig ? ' (was ' + r.orig + ')' : '')) +
          (typeof r.n === 'string' ? ' (uncertain read)' : '') +
          ' - click to make it the active farm';
        var p = viewer.viewport.imageToViewportCoordinates(
          new OpenSeadragon.Point(r.x, r.y));
        viewer.addOverlay({ element: d, location: p,
          placement: OpenSeadragon.Placement.CENTER,
          rotationMode: OpenSeadragon.OverlayRotationMode.NO_ROTATION });
        ovs.push({ el: d, rec: { ref: r } });
      });
    }
    if (layers.yards) {
      yards.forEach(function (a, k) {
        var vd = VERD[a.farm];
        var d = document.createElement('div');
        d.className = 'yard-label' +
          (vd && vd.c ? ' ' + vd.c : '') +
          (k === sel ? ' sel' : '');
        d.textContent = 'f' + a.farm + ': ' + a.area;
        d.title = 'farm ' + a.farm + ', yard ' + a.area +
                  ' - click to select; drag anew and Enter to fix';
        var p = viewer.viewport.imageToViewportCoordinates(
          new OpenSeadragon.Point(a.x + (a.w || 0) / 2, a.y + (a.h || 0) / 2));
        viewer.addOverlay({ element: d, location: p,
          placement: OpenSeadragon.Placement.CENTER,
          rotationMode: OpenSeadragon.OverlayRotationMode.NO_ROTATION });
        ovs.push({ el: d, rec: { idx: k } });
      });
    }
    syncList();
    showActive();
    syncLayerBtns();
  }

  // ---- the Layers buttons ---------------------------------------------------
  function syncLayerBtns() {
    document.getElementById('show-refs').classList.toggle('on', layers.refs);
    document.getElementById('show-yards').classList.toggle('on', layers.yards);
    document.getElementById('show-all').classList.toggle('on',
      layers.refs || layers.yards);
  }
  function toggleAllLayers() {
    var show = !(layers.refs || layers.yards);   // all hidden -> all back
    layers.refs = show; layers.yards = show;
    drawAll();
    setHint(show ? 'the labels are back'
                 : 'the labels are hidden &mdash; L brings them back');
  }
  document.getElementById('show-refs').addEventListener('click', function () {
    layers.refs = !layers.refs; drawAll();
  });
  document.getElementById('show-yards').addEventListener('click', function () {
    layers.yards = !layers.yards; drawAll();
  });
  document.getElementById('show-all').addEventListener('click', toggleAllLayers);

  // ---- the active farm ----------------------------------------------------
  var afEl = document.getElementById('activefarm');
  function showActive() {
    if (!activeFarm) {
      afEl.innerHTML = 'none &mdash; click a red tag on the map';
      return;
    }
    var r = ROWS[activeFarm.n];
    afEl.innerHTML = 'Farm <b>' + activeFarm.n + '</b>' +
      (r ? ' &mdash; ' + r.name + ', ' + r.td + ' des ' + r.ts + ' saz in all'
         : (activeFarm.n === '[?]'
            ? (activeFarm.added ? ' (new &mdash; type its number in the change field)'
                                : ' (unreadable on the map)')
            : ' (not a statement row)'));
  }
  function setActive(r) {
    activeFarm = { n: r.n, x: r.x, y: r.y, added: r.added };
    fixnum.value = r.n;              // the read as it stands, ready to correct
    // draw mode stays off this round — the marking session changes numbers,
    // not boxes (D still turns it on by hand for the yard work)
    if (r.ocr && !r.added && r.n === r.orig) {
      // an unreviewed OCR read, picked outside a queue: say what walks them
      setHint('farm ' + r.n + ' selected &mdash; an unreviewed OCR read; the uncertain-numbers list walks the [?] ones');
    } else {
      setHint('farm ' + r.n + ' selected &mdash; the change field holds the read; type the correction, Enter');
    }
    drawAll();
  }

  // ---- the ruling box -------------------------------------------------------
  var rulingEl = document.getElementById('ruling');
  var RUL0 = 'click a yard label or a red tag &mdash; the ruling shows here';
  function showRuling(html) { rulingEl.innerHTML = html; }
  function rulingFor(farm) {
    var vd = VERD[farm];
    if (vd && vd.w) return vd.w;
    return 'no ruling yet &mdash; export the yards and have the page rebuilt';
  }
  function rulingForRef(r) {
    var t = 'tag <b>' + r.n + '</b>';
    if (r.added) return t + ' &mdash; added in the page, not from the catalogue.';
    if (r.n !== r.orig) return t + ' &mdash; corrected from ' + r.orig +
      ' in the page (the catalogue read ' + r.orig + ').';
    if (typeof r.n === 'string') return t + ' &mdash; an uncertain read (yellow);' +
      ' the uncertain-numbers list walks these.';
    return t + ' &mdash; read by hand on the spot sheet.';
  }

  // ---- draw mode: the capture layer (proven) ------------------------------
  var viewerEl = document.getElementById('viewer');
  var cap = document.createElement('div');
  cap.className = 'draw-capture';
  viewerEl.appendChild(cap);
  var modebtn = document.getElementById('modebtn');
  function applyMode() {
    cap.style.display = drawMode ? 'block' : 'none';
    modebtn.classList.toggle('on', drawMode);
    modebtn.textContent = drawMode ? 'Pan mode (D)' : 'Draw mode (D)';
  }
  function toggleModeTo(on) {
    drawMode = on;
    applyMode();
  }
  function toggleMode() { toggleModeTo(!drawMode); }
  modebtn.addEventListener('click', toggleMode);

  var rubber = document.createElement('div');
  rubber.className = 'rubber';
  rubber.style.display = 'none';
  viewerEl.appendChild(rubber);
  var pendRect = null;
  var dragging = false, s0 = null, s1 = null;
  var missDown = null;   // a press that hit no label — a click on the empty map deselects
  function elPos(ev) {
    var r = viewerEl.getBoundingClientRect();
    return { x: ev.clientX - r.left, y: ev.clientY - r.top };
  }
  function imgPos(el) {
    return world.viewerElementToImageCoordinates(new OpenSeadragon.Point(el.x, el.y));
  }
  function showRectEl(a, b) {
    rubber.style.display = 'block';
    rubber.style.left = Math.min(a.x, b.x) + 'px';
    rubber.style.top = Math.min(a.y, b.y) + 'px';
    rubber.style.width = Math.abs(b.x - a.x) + 'px';
    rubber.style.height = Math.abs(b.y - a.y) + 'px';
  }
  function showRectImg(x0, y0, x1, y1) {
    showRectEl(elFromImg(x0, y0), elFromImg(x1, y1));
  }
  function elFromImg(ix, iy) {
    var v = viewer.viewport.imageToViewerElementCoordinates(
      new OpenSeadragon.Point(ix, iy));
    return { x: v.x, y: v.y };
  }
  function hideRect() { rubber.style.display = 'none'; }
  viewer.addHandler('update-viewport', function () {
    if (pendRect) showRectImg(pendRect.x0, pendRect.y0, pendRect.x1, pendRect.y1);
  });
  cap.addEventListener('mousedown', function (ev) {
    if (!drawMode || !world || ev.button !== 0) return;
    dragging = true;
    s0 = elPos(ev); s1 = { x: s0.x, y: s0.y };
    showRectEl(s0, s1);
    ev.preventDefault();
  });
  window.addEventListener('mousemove', function (ev) {
    if (!dragging) return;
    s1 = elPos(ev);
    showRectEl(s0, s1);
  });
  window.addEventListener('mouseup', function (ev) {
    if (dragging) {
      dragging = false;
      s1 = elPos(ev);
      if (Math.abs(s1.x - s0.x) < 9 && Math.abs(s1.y - s0.y) < 9) {
        // a click, not a drag: in add mode it marks the spot for the new
        // number, otherwise it deselects
        pendRect = null; hideRect();
        if (missDown) { missDown = null;
          if (addMode) markSpot(ev); else clearAll(); }
        return;
      }
      var a = imgPos(s0), b = imgPos(s1);
      pendRect = { x0: Math.min(a.x, b.x), y0: Math.min(a.y, b.y),
                   x1: Math.max(a.x, b.x), y1: Math.max(a.y, b.y) };
      showRectImg(pendRect.x0, pendRect.y0, pendRect.x1, pendRect.y1);
      if (addMode) {
        fixnum.value = ''; fixnum.focus();
        setHint('now type the number, Enter &mdash; it lands in the middle of the box');
      } else {
        document.getElementById('area').focus();
      }
      return;
    }
    // pan mode: a press on the empty map that stayed put is a click — deselect
    if (missDown) {
      var moved = Math.hypot(ev.clientX - missDown.x, ev.clientY - missDown.y);
      missDown = null;
      if (moved < 9 && viewerEl.contains(ev.target)) {
        if (addMode) markSpot(ev); else clearAll();
      }
    }
  });
  cap.addEventListener('wheel', function (ev) {
    ev.preventDefault();
    var p = elPos(ev);
    var ip = imgPos(p);
    var sc = ev.deltaY < 0 ? 1.25 : 0.8;
    var ref = viewer.viewport.imageToViewportCoordinates(
      new OpenSeadragon.Point(ip.x, ip.y));
    var before = viewer.viewport.viewportToScreenCoordinates(ref);
    viewer.viewport.zoomBy(sc);
    viewer.viewport.applyConstraints();
    var after = viewer.viewport.viewportToScreenCoordinates(
      viewer.viewport.imageToViewportCoordinates(
        new OpenSeadragon.Point(ip.x, ip.y)));
    var dx = after.x - before.x, dy = after.y - before.y;
    if (dx || dy) viewer.viewport.panBy(
      viewer.viewport.deltaPointsFromPixels(new OpenSeadragon.Point(-dx, -dy)));
    viewer.viewport.applyConstraints();
  });

  // ---- selection: pointer + mousedown interception (proven) --------------
  function hitOverlay(clientX, clientY, filter) {
    var best = null, bestD = 1e9;
    var PAD = 8;
    ovs.forEach(function (o) {
      if (!o.rec || !filter(o.rec)) return;
      var r = o.el.getBoundingClientRect();
      if (r.width === 0) return;
      var cx = r.left + r.width / 2, cy = r.top + r.height / 2;
      var d = Math.hypot(clientX - cx, clientY - cy);
      var inside = clientX >= r.left - PAD && clientX <= r.right + PAD &&
                   clientY >= r.top - PAD && clientY <= r.bottom + PAD;
      if (inside || d < Math.max(r.width, r.height) / 2 + PAD) {
        if (d < bestD) { bestD = d; best = o; }
      }
    });
    return best;
  }
  function setHint(t) {
    document.getElementById('modehint').innerHTML = t;
  }
  function onPress(ev) {
    try {
      if (!world || ev.button !== 0) return;
      if (!viewerEl.contains(ev.target)) return;
      if (ev.target.closest && ev.target.closest('button, input, a, label')) return;
      // a yard label first (they sit above the refs)
      var o = hitOverlay(ev.clientX, ev.clientY, function (r) { return r.idx !== undefined; });
      if (o) {
        ev.preventDefault(); ev.stopPropagation();
        missDown = null;
        sel = (sel === o.rec.idx ? -1 : o.rec.idx);
        if (sel >= 0) {
          var a = yards[sel];
          area.value = a.area; note.value = a.note || '';
          if (a.w) {
            pendRect = { x0: a.x, y0: a.y, x1: a.x + a.w, y1: a.y + a.h };
            showRectImg(pendRect.x0, pendRect.y0, pendRect.x1, pendRect.y1);
          }
          activeFarm = { n: a.farm, x: a.rx || a.x, y: a.ry || a.y };
          setHint('editing the yard of farm ' + a.farm +
                  ': drag a new rectangle (Esc to leave it), then Enter');
          showRuling(rulingFor(a.farm));
        } else {
          area.value = ''; note.value = '';
          pendRect = null; hideRect();
          setHint('click a farm number, then drag the box, then Enter');
          showRuling(RUL0);
        }
        drawAll();
        return;
      }
      // a farm-number tag
      o = hitOverlay(ev.clientX, ev.clientY, function (r) { return r.ref !== undefined; });
      if (o) {
        ev.preventDefault(); ev.stopPropagation();
        missDown = null;
        setActive(o.rec.ref);
        showRuling(rulingForRef(o.rec.ref));
        return;
      }
      // nothing: remember the press — if it ends as a click (no drag) it
      // deselects (the mouseup above)
      missDown = { x: ev.clientX, y: ev.clientY };
    } catch (err) {
      document.getElementById('modehint').textContent =
        'ERROR in the press handler: ' + err.message;
    }
  }
  document.addEventListener('mousedown', onPress, true);
  document.addEventListener('pointerdown', onPress, true);

  // ---- the uncertain numbers' queue -----------------------------------------
  var K_UC = 'p1896-uncnum-v1';
  var umarks = {};   // "x,y" -> {m: 'ok'|'unc', n: comment}
  try { umarks = JSON.parse(localStorage.getItem(K_UC) || '{}'); } catch (e) {}
  function persistU() {
    try { localStorage.setItem(K_UC, JSON.stringify(umarks)); } catch (e) {}
  }
  var REFBY = {};
  REFS.forEach(function (r) { REFBY[r.x + ',' + r.y] = r; });
  var uSel = -1, uList = [];
  function uFixed(u) {
    // the entry's read is certain now (a fix was applied)
    var r = REFBY[u.key];
    return r && typeof r.n !== 'string';
  }
  function uDone(u) {
    return umarks[u.key] || uFixed(u);
  }
  function uNext() {
    for (var i = 1; i <= uList.length; i++) {
      var j = (uSel + i) % uList.length;
      if (!uDone(uList[j])) { gotoU(j); return; }
    }
    syncUlist();
  }
  function syncUlist() {
    // the entries whose read is certain now (a fix was applied) are done —
    // they leave the list; their marks stay in the store
    uList = UQ.filter(function (u) { return !uFixed(u); });
    if (uSel >= uList.length) uSel = -1;
    var ul = document.getElementById('ulist');
    ul.innerHTML = '';
    var left = 0;
    uList.forEach(function (u, k) {
      var mk = umarks[u.key];
      var fx = uFixed(u);
      if (!uDone(u)) left++;
      var li = document.createElement('li');
      li.className = (k === uSel ? 'selrow' : '');
      var r = REFBY[u.key];
      var now = (r && r.n !== u.read) ? String(r.n) : null;
      var dot = fx ? '\u2713' : (mk ? (mk.m === 'ok' ? '\u2713' : '?') : '\u00b7');
      var main = fx ? (u.read + ' \u2192 ' + now) : u.read;
      li.innerHTML = '<span class="v" style="min-width:6.2rem">' + dot +
        ' ' + main.replace(/</g, '&lt;') + '</span>' +
        '<span class="xy">(' + u.x + ', ' + u.y + ')' +
        (mk && mk.n ? ' &mdash; ' + mk.n.replace(/</g, '&lt;') : '') + '</span>';
      li.addEventListener('click', function () { gotoU(k); });
      ul.appendChild(li);
    });
    document.getElementById('ucount').textContent =
      '(' + uList.length + ' left of ' + UQ.length + ')';
    var u = uList[uSel];
    var uh = document.getElementById('uhint');
    if (!u) {
      uh.innerHTML = 'click an entry &mdash; the map goes there, the change' +
        ' field takes the reading; Enter marks it right as shown';
      return;
    }
    var r = REFBY[u.key];
    var bits = u.neigh.map(function (q) {
      return q.n + ' (' + q.d + ' px' + (q.c > 1 ? ', &times;' + q.c : '') + ')';
    });
    uh.innerHTML = '<b>' + String(r && r.n !== undefined ? r.n : u.read)
      .replace(/</g, '&lt;') + '</b> at (' +
      u.x + ', ' + u.y + ')' + (u.ocr ? ' [OCR]' : '') +
      ' &mdash; neighbours: ' + (bits.join(', ') || 'none in ' + 1200 + ' px') +
      (u.sugg.length ? ' &mdash; suggestion: <b>' + u.sugg[0] + '</b>' : '');
  }
  function gotoU(k) {
    uSel = k;
    var u = uList[k];
    if (!u) { uSel = -1; syncUlist(); return; }
    var r = REFBY[u.key];
    viewer.viewport.panTo(viewer.viewport.imageToViewportCoordinates(
      new OpenSeadragon.Point(u.x, u.y)));
    activeFarm = { n: r.n, x: r.x, y: r.y, added: r.added };
    fixnum.value = r.n;
    showRuling(rulingForRef(r));
    syncUlist();
  }
  function markU(m) {
    if (uSel < 0 || !uList[uSel]) return;
    var u = uList[uSel];
    if (m === 'ok') {
      // "the read is right as shown": write the confirm-fix (persists,
      // takes the tag out of the purple set) — then mark and move on
      if (!applyFix()) return;
    }
    var note = document.getElementById('unote').value.trim();
    var mk = { m: m };
    if (note) mk.n = note;
    if (umarks[u.key] && umarks[u.key].m === mk.m &&
        (umarks[u.key].n || '') === note) {
      delete umarks[u.key];           // the same mark again: unmark
    } else {
      umarks[u.key] = mk;
    }
    persistU();
    document.getElementById('unote').value = '';
    uNext();
  }
  function useSugg() {
    if (uSel < 0 || !uList[uSel]) return;
    var u = uList[uSel];
    var s = u.sugg && u.sugg[0];
    if (s === undefined) { setHint('no neighbour to suggest from'); return; }
    fixnum.value = s;
    if (!applyFix()) return;
    umarks[u.key] = { m: 'ok', n: '\u2192 ' + s };
    persistU();
    document.getElementById('unote').value = '';
    uNext();
  }
  document.getElementById('uok').addEventListener('click', function () { markU('ok'); });
  document.getElementById('uunc').addEventListener('click', function () { markU('unc'); });
  document.getElementById('ubtn').addEventListener('click', useSugg);
  document.getElementById('uclr').addEventListener('click', function () {
    umarks = {}; persistU(); syncUlist();
  });
  document.getElementById('unote').addEventListener('keydown', function (ev) {
    if (ev.key === 'Enter') { ev.preventDefault(); markU('unc'); }
    else if (ev.key === 'Escape') { ev.target.blur(); }
  });

  // ---- saving -------------------------------------------------------------
  function persist() {
    try { localStorage.setItem(K_NEW, JSON.stringify(yards)); } catch (e) {}
  }
  // the shared reset (Esc, and a click on the empty map): the selection, the
  // farm, a pending rectangle — all of it goes
  function clearAll() {
    if (sel >= 0) { sel = -1; }
    lastSaved = null;
    addMode = false; syncAddBtn();
    area.value = ''; note.value = ''; fixnum.value = '';
    activeFarm = null; pendRect = null; hideRect();
    toggleModeTo(false);
    setHint('click a farm number, then drag the box, then Enter');
    showRuling(RUL0);
    drawAll();
  }
  function syncList() {
    var ul = document.getElementById('alist');
    ul.innerHTML = '';
    yards.forEach(function (a, k) {
      var li = document.createElement('li');
      li.className = k === sel ? 'selrow' : '';
      li.innerHTML = '<span class="v">f' + a.farm + ': ' + a.area + '</span>' +
        '<span class="xy">(' + a.x + ', ' + a.y + ')' +
        (a.note ? ' - ' + a.note : '') + '</span>';
      li.addEventListener('click', function () {
        sel = (sel === k ? -1 : k);
        if (sel >= 0) {
          var yy = yards[sel];
          area.value = yy.area; note.value = yy.note || '';
          activeFarm = { n: yy.farm, x: yy.rx || yy.x, y: yy.ry || yy.y };
          if (yy.w) {
            pendRect = { x0: yy.x, y0: yy.y, x1: yy.x + yy.w, y1: yy.y + yy.h };
            showRectImg(pendRect.x0, pendRect.y0, pendRect.x1, pendRect.y1);
          }
          showRuling(rulingFor(yy.farm));
        } else {
          area.value = ''; note.value = ''; pendRect = null; hideRect();
          showRuling(RUL0);
        }
        drawAll();
      });
      var b = document.createElement('button');
      b.className = 'btn'; b.textContent = '\\u00d7';
      b.addEventListener('click', function (ev) {
        ev.stopPropagation();
        yards.splice(k, 1); if (sel === k) sel = -1;
        lastSaved = null;
        persist(); drawAll();
      });
      li.appendChild(b);
      ul.appendChild(li);
    });
    document.getElementById('ncount').textContent = '(' + yards.length + ')';
  }
  var area = document.getElementById('area'),
      note = document.getElementById('note'),
      fixnum = document.getElementById('fixnum');

  // ---- changing a red tag's number ----------------------------------------
  function persistFixes() {
    try { localStorage.setItem(K_FIX, JSON.stringify(fixes)); } catch (e) {}
  }
  function activeRef() {
    var found = null;
    REFS.forEach(function (r) {
      if (activeFarm && r.x === activeFarm.x && r.y === activeFarm.y) found = r;
    });
    return found;
  }
  // a tag's correction relinks the yards anchored to that very tag: a yard
  // saved with the tag's old read (and this mark's position) follows the
  // new number — yards anchored to other tags of the same number stay put
  function relinkYards(ref, fromN, toN) {
    var k = 0;
    yards.forEach(function (y) {
      if (y.farm === fromN && y.rx === ref.x && y.ry === ref.y) {
        y.farm = toN; k++;
      }
    });
    if (k) persist();
    return k;
  }

  function applyFix() {
    if (!activeFarm) { setHint('click a farm number first, then change it here'); return false; }
    var ref = activeRef();
    if (!ref) { setHint('the active mark is not on the map any more'); return false; }
    var v = fixnum.value.trim();
    if (ref.added) {
      // an added mark has no catalogue original: empty + Enter removes it,
      // a number sets it (stored with the mark, not among the fixes)
      if (v === '') {
        added = added.filter(function (m) {
          return !(m.x === ref.x && m.y === ref.y); });
        REFS.splice(REFS.indexOf(ref), 1);
        persistAdded();
        activeFarm = null; fixnum.value = '';
        setHint('the added mark at (' + ref.x + ', ' + ref.y + ') is gone');
        drawAll();
        return true;
      }
      if (!/^[\\d\\[\\]?]+$/.test(v) || (!/\\d/.test(v) && v !== '[?]')) {
        setHint('the number takes digits &mdash; uncertainty in [..?], or just [?] for unreadable');
        return false;
      }
      var na = /^\\d+$/.test(v) ? parseInt(v, 10) : v;
      var movedA = relinkYards(ref, ref.n, na);
      added.forEach(function (m) {
        if (m.x === ref.x && m.y === ref.y) m.n = na;
      });
      ref.n = na;
      if (activeFarm) activeFarm.n = na;
      persistAdded();
      fixnum.value = na;
      setHint('the added mark at (' + ref.x + ', ' + ref.y + ') reads <b>' +
              na + '</b> now' +
              (movedA ? ' &mdash; ' + movedA + ' linked yard' +
               (movedA > 1 ? 's' : '') + ' follow' + (movedA > 1 ? '' : 's') : '') +
              ' &mdash; drag the box for its yard, or Esc');
      drawAll();
      return true;
    }
    if (v === '') {
      // empty field + Enter: the correction is withdrawn
      delete fixes[fixKey(ref)];
      var movedR = relinkYards(ref, ref.n, ref.orig);
      ref.n = ref.orig;
      if (activeFarm) activeFarm.n = ref.orig;   // the tag stays selected
      persistFixes();
      fixnum.value = ref.orig;
      setHint('the mark at (' + ref.x + ', ' + ref.y + ') reads ' + ref.orig +
              ' again &mdash; the original is back' +
              (movedR ? ', ' + movedR + ' linked yard' + (movedR > 1 ? 's' : '') +
               ' revert' + (movedR > 1 ? '' : 's') + ' with it' : ''));
      drawAll();
      return true;
    }
    if (!/^[\\d\\[\\]?]+$/.test(v) || (!/\\d/.test(v) && v !== '[?]')) {
      setHint('the number takes digits &mdash; uncertainty in [..?], or just [?] for unreadable');
      return false;
    }
    // pure digits find the statement row; an uncertain read ("3[?]",
    // "[?]") stays text — the panel then shows not-a-statement-row
    var n = /^\\d+$/.test(v) ? parseInt(v, 10) : v;
    // a fix — or a confirm, the read left as it stands — takes the tag out
    // of the purple review set, in the session and (the fix is stored, its
    // mere presence marks the mark reviewed) on every rebuild
    fixes[fixKey(ref)] = n;
    var moved = relinkYards(ref, ref.n, n);
    ref.n = n;
    ref.ocr = false;
    if (activeFarm) activeFarm.n = n;   // the tag stays selected (blue)
    persistFixes();
    fixnum.value = n;
    setHint((n === ref.orig
      ? 'the mark at (' + ref.x + ', ' + ref.y + ') is confirmed as ' + n +
        ' &mdash; it is no longer purple'
      : 'the mark at (' + ref.x + ', ' + ref.y + ') now reads <b>' + n +
        '</b> (was ' + ref.orig + ') &mdash; the panel follows the row') +
      (moved ? '; ' + moved + ' linked yard' + (moved > 1 ? 's' : '') +
       ' relabel' + (moved > 1 ? '' : 's') + ' to f' + n : ''));
    drawAll();
    return true;
  }
  fixnum.addEventListener('keydown', function (ev) {
    if (ev.key === 'Enter') {
      ev.preventDefault();
      if (addMode && pendRect && !activeFarm) { finalizeAdd(); return; }
      var uk = activeFarm ? (activeFarm.x + ',' + activeFarm.y) : null;
      var ok = applyFix();
      // a fix on the queue's current entry marks it and moves on
      if (ok && uSel >= 0 && uList[uSel] && uList[uSel].key === uk &&
          !umarks[uk]) {
        umarks[uk] = { m: 'ok' }; persistU();
        uNext();
      }
    }
    else if (ev.key === 'Escape') { fixnum.blur(); }
  });
  document.getElementById('numbtn').addEventListener('click', function () {
    applyFix();
  });

  // ---- adding a number the catalogue missed --------------------------------
  function syncAddBtn() {
    document.getElementById('addbtn').classList.toggle('on', addMode);
  }
  function toggleAdd() {
    addMode = !addMode; syncAddBtn();
    if (addMode) {
      if (!drawMode) toggleModeTo(true);   // the box needs draw mode
      setHint('add: drag a box around the red number (a click marks the spot), then type the number, Enter');
    } else {
      setHint('click a farm number, then drag the box, then Enter');
    }
  }
  document.getElementById('addbtn').addEventListener('click', toggleAdd);
  // the number typed while a pending add-box is up: the mark is born here,
  // at the middle of the box, already numbered and blue
  function finalizeAdd() {
    var v = fixnum.value.trim();
    if (v === '') { setHint('type the number first &mdash; Enter then puts it on the map'); return; }
    if (!/^[\\d\\[\\]?]+$/.test(v) || (!/\\d/.test(v) && v !== '[?]')) {
      setHint('the number takes digits &mdash; uncertainty in [..?], or just [?] for unreadable');
      return;
    }
    var n = /^\\d+$/.test(v) ? parseInt(v, 10) : v;
    var x = Math.round((pendRect.x0 + pendRect.x1) / 2),
        y = Math.round((pendRect.y0 + pendRect.y1) / 2);
    var ref = { n: n, orig: '[?]', x: x, y: y, added: true };
    added.push({ x: x, y: y, n: n });
    REFS.push(ref);
    persistAdded();
    pendRect = null; hideRect();
    addMode = false; syncAddBtn();
    area.value = ''; note.value = ''; fixnum.value = '';
    toggleModeTo(false);
    setHint('farm <b>' + n + '</b> is on the map (blue) &mdash; click it any time to mark its yard');
    drawAll();
  }
  // a still click in add mode marks the spot (a zero-size pending box)
  function markSpot(ev) {
    var ip = imgPos(elPos(ev));
    pendRect = { x0: ip.x, y0: ip.y, x1: ip.x, y1: ip.y };
    fixnum.value = ''; fixnum.focus();
    setHint('the spot is marked &mdash; type the number, Enter');
  }

  var lastSaved = null;   // the yard just saved — a note typed after it
                          // still belongs to it (see the note field's Enter)

  function save() {
    var a = area.value.trim();
    if (!activeFarm) {
      // the yard went in a moment ago; a note typed now still attaches to it
      var nt = note.value.trim();
      if (sel < 0 && lastSaved !== null && nt && yards[lastSaved]) {
        yards[lastSaved].note = nt;
        note.value = '';
        persist(); drawAll();
        setHint('the note is with the yard of farm ' + yards[lastSaved].farm +
                ' &mdash; Enter again replaces it');
        return;
      }
      setHint('click a farm number first');
      return;
    }
    if (sel >= 0) {
      // edit: geometry if a new rectangle was drawn, area always
      if (a) yards[sel].area = a;
      yards[sel].note = note.value.trim();
      yards[sel].farm = activeFarm.n;
      yards[sel].rx = activeFarm.x; yards[sel].ry = activeFarm.y;
      if (pendRect) {
        yards[sel].x = Math.round(pendRect.x0); yards[sel].y = Math.round(pendRect.y0);
        yards[sel].w = Math.round(pendRect.x1 - pendRect.x0);
        yards[sel].h = Math.round(pendRect.y1 - pendRect.y0);
      }
      lastSaved = sel;
      sel = -1;
    } else {
      if (!pendRect) { setHint('draw the box around the 1. figure first (Draw mode)'); return; }
      yards.push({
        farm: activeFarm.n, rx: activeFarm.x, ry: activeFarm.y,
        area: a, note: note.value.trim(),
        x: Math.round(pendRect.x0), y: Math.round(pendRect.y0),
        w: Math.round(pendRect.x1 - pendRect.x0),
        h: Math.round(pendRect.y1 - pendRect.y0)
      });
      lastSaved = yards.length - 1;
    }
    pendRect = null; hideRect();
    area.value = ''; note.value = '';
    persist(); drawAll();
    // the flow: one farm, one yard — saved, the farm deselects and the
    // mode returns to pan. A note forgotten in the moment still fits:
    // type it and Enter attaches it to this yard.
    activeFarm = null;
    toggleModeTo(false);
    setHint('saved &mdash; a note typed now + Enter goes with farm ' +
            yards[lastSaved].farm + '; or click the next farm number');
  }
  area.addEventListener('keydown', function (ev) {
    if (ev.key === 'Enter') { ev.preventDefault(); save(); }
    else if (ev.key === 'Escape') { pendRect = null; hideRect(); }
  });
  note.addEventListener('keydown', function (ev) {
    if (ev.key === 'Enter') { ev.preventDefault(); save(); }
  });
  document.addEventListener('keydown', function (ev) {
    // the single-key toggles are global: the area field only ever carries
    // digits, '.', '-', '[', '?', ']' — letters mean the shortcut, so the
    // "typing into a field" guard is dropped for D and Esc. Escape inside
    // a field still clears a pending rectangle (nothing else it could mean).
    if (ev.key === 'Delete' && sel >= 0) {
      yards.splice(sel, 1); sel = -1; lastSaved = null; persist(); drawAll();
    }
    if (ev.key === 'Escape') {
      if (ev.target === area || ev.target === note || ev.target === fixnum) {
        pendRect = null; hideRect();
        ev.target.blur();
        return;
      }
      clearAll();
    }
    if (ev.key === 'd' || ev.key === 'D') {
      // the note field carries free text — there a letter is a letter
      if (ev.target === note) return;
      ev.preventDefault(); toggleMode();
    }
    // N: the change-number field, like D for the mode — the area and number
    // fields take digits only, so a letter can only mean the shortcut
    if ((ev.key === 'n' || ev.key === 'N') && ev.target !== note) {
      ev.preventDefault(); fixnum.focus(); fixnum.select();
    }
    // L: every label off/on at once — the same switch the "all (L)" button
    if ((ev.key === 'l' || ev.key === 'L') && ev.target !== note) {
      ev.preventDefault(); toggleAllLayers();
    }
    // A: add a number — the same switch the "add a number" button
    if ((ev.key === 'a' || ev.key === 'A') && ev.target !== note) {
      ev.preventDefault(); toggleAdd();
    }
    // Enter with no field in focus: the uncertain queue's "correct" mark
    if (ev.key === 'Enter' && uSel >= 0 &&
        !/^(INPUT|TEXTAREA|BUTTON|LABEL|A)$/.test(ev.target.tagName)) {
      ev.preventDefault(); markU('ok');
      return;
    }
  });
  document.getElementById('del').addEventListener('click', function () {
    if (sel >= 0) { yards.splice(sel, 1); sel = -1; persist(); drawAll(); }
  });
  document.getElementById('export').addEventListener('click', function () {
    var blob = new Blob([JSON.stringify(
      { yards: yards, red_fixes: fixes, red_added: added,
        uncertain_marks: umarks }, null, 1)],
      { type: 'application/json' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'yards_read.json';
    a.click();
  });
  syncUlist();
  window.__yardmap = { alive: true, count: function () { return ovs.length; } };
})();
</script>
<script>
(function () {
  document.addEventListener('mousedown', function () {
    var h = document.getElementById('modehint');
    if (h && !window.__yardmap) h.textContent = 'MAIN SCRIPT NOT ALIVE — tell Claude';
  }, true);
})();
</script>
</body>
</html>
"""
HTML = HTML.replace("@@REFS@@", json.dumps(refs, ensure_ascii=False))
HTML = HTML.replace("@@ROWS@@", json.dumps(rows, ensure_ascii=False))
HTML = HTML.replace("@@VERDICTS@@", json.dumps(VERD, ensure_ascii=False))
HTML = HTML.replace("@@UNCERTAIN@@", json.dumps(UQ, ensure_ascii=False))
HTML = HTML.replace("@@TILES@@", TILES)
out = ROOT + r"\scratch\map4456\yard_map.html"
with open(out, "w", encoding="utf-8") as f:
    f.write(HTML)
print("wrote", out, round(len(HTML) / 1e3, 1), "KB")
