# The farm-polygon tool — draw the outline of each owner's farm on the
# Pełzucki 1896 mosaic.
#
# The flow (the editor's plan, 2026-11-02: an updated vector map of the farms,
# to be overlaid with present-day roads and farms later):
#   1. D toggles draw mode; a click lays a vertex, U undoes one, Enter closes
#      the polygon (Esc cancels it)
#   2. the polygon takes the farm number from the assign field; empty, it
#      takes the nearest confident red tag inside the polygon
#   3. a click inside a drawn polygon selects it; type a number + Enter to
#      reassign, Delete removes it
# The sidebar lists rows 1-97 with the evidence per row: the confident and
# uncertain red tags, how many sit inside the row's polygons, the polygons'
# estimated area against the row's statement total (the calibration is
# approximate — see PX2_PER_SAZ below), and a status colour. The rows with
# no confident tag at all are listed separately: the map cannot name them.
#
# Input: reds_all.json + yards_read.json's red_fixes (the tags),
# farm_locations.json (the black farm-number sites), reference_numbers.json.
# Output: scratch/map4456/farm_polygons.html — served from the repository
# root at localhost:8779 like the other working pages.
import json

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld"
TILES = "https://takaji10.github.io/triebenfeld-maps/pelzucki1896/info.json"

D = json.load(open(ROOT + r"\scratch\map4456\reds_all.json", encoding="utf-8"))
EX = json.load(open(ROOT + r"\scratch\map4456\yards_read.json", encoding="utf-8"))
FL = json.load(open(ROOT + r"\scratch\map4456\farm_locations.json", encoding="utf-8"))
REF = json.load(open(ROOT + r"\scratch\map4456\reference_numbers.json", encoding="utf-8"))
ST = {k: v for k, v in REF["statement"].items() if k.isdigit()}

def canon(t):
    return t.strip().replace("[", "").replace("?]", "").replace("?", "").strip()

fixes = EX.get("red_fixes", {})
refs = []
for a in D["answered"]:
    x, y = a["x"], a["y"]
    if a.get("fixed"):
        x = a["fixed"]["x"]; y = a["fixed"]["y"]
    k = str(x) + "," + str(y)
    raw = str(fixes[k]) if k in fixes else a["text"].strip()
    c = canon(raw)
    n = raw if ("?" in raw or "[" in raw) else (int(c) if c.isdigit() else raw)
    refs.append({"n": n, "x": x, "y": y, "ocr": False})
for m in D["added"]:
    cx = m["x"] + m.get("w", 0) // 2
    cy = m["y"] + m.get("h", 0) // 2
    k = str(cx) + "," + str(cy)
    raw = str(fixes[k]) if k in fixes else m["text"].strip()
    c = canon(raw)
    n = raw if ("?" in raw or "[" in raw) else (int(c) if c.isdigit() else raw)
    refs.append({"n": n, "x": cx, "y": cy, "ocr": True})

blacks = [{"n": b["n"], "x": b["x"], "y": b["y"]} for b in FL]

rows = []
for k in sorted(ST, key=lambda s: int(s)):
    r = ST[k]
    rows.append({
        "n": int(k), "name": r["name"],
        "total": [r["total"]["des"], r["total"]["saz"]],
        "buildings": [r["buildings"]["des"], r["buildings"]["saz"]],
    })

# the calibration: the mosaic is ~0.4 m/px on the ground (the fit's corner
# error +-35 px = +-14 m, maps/pelzucki1896/notes.md), 1 sq sazhen = 4.548 m2
# -> 1 sazhen ~ 28.4 px2. APPROXIMATE — the polygon areas read as estimates,
# good to perhaps +-10%; the exact calibration can come from the warper.
PX2_PER_SAZ = 28.4

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Pełzucki 1896 — the farms' polygons (working page)</title>
<style>
:root { --rule: #d8d2c4; --ink: #2a2620; --ink-soft: #6b6459; --accent: #8a3324; }
body { margin: 0; background: #faf8f3; color: var(--ink); font-family: Georgia, serif; }
header { max-width: 120rem; margin: 0 auto; padding: .9rem 2rem .2rem; }
header h1 { font-size: 1.2rem; margin: 0 0 .2rem; }
header p { font-size: .85rem; color: var(--ink-soft); margin: .15rem 0; }
kbd { font-family: Verdana, sans-serif; font-size: .72rem; border: 1px solid var(--rule);
      border-radius: 3px; padding: 0 .35rem; background: #fff; }
.cols { display: grid; grid-template-columns: minmax(20rem, 25rem) minmax(0, 1fr);
        gap: 1.4rem; align-items: start; max-width: 120rem; margin: 0 auto;
        padding: 0 2rem 2rem; }
.side { max-height: 92vh; overflow-y: auto; font-family: Verdana, sans-serif;
         font-size: .82rem; }
.box { border: 1px solid var(--rule); border-radius: .4rem; padding: .7rem .9rem;
       margin: 0 0 .8rem; }
.box h2 { font-size: .9rem; margin: 0 0 .4rem; }
#fnum, #pnote { font-size: 1rem; padding: .3rem .5rem; border: 1px solid var(--rule); }
#fnum { width: 7rem; } #pnote { width: 10rem; }
.btn { font-family: Verdana, sans-serif; font-size: .78rem; padding: .3rem .8rem;
       border: 1px solid var(--rule); background: #fff; cursor: pointer;
       border-radius: 3px; margin: 0 .3rem .3rem 0; }
.btn.primary { background: var(--accent); color: #fff; border-color: var(--accent); }
.btn.on { background: #2a6db3; color: #fff; border-color: #2a6db3; }
.alist { list-style: none; margin: .4rem 0 0; padding: 0; max-height: 26rem;
         overflow-y: auto; }
.alist li { display: flex; gap: .5rem; align-items: baseline; padding: .2rem 0;
            border-bottom: 1px solid var(--rule); cursor: pointer; }
.alist li:hover { background: rgba(42,109,179,.06); }
.alist li.selrow { background: rgba(42,109,179,.14); }
.alist .v { font-weight: 700; color: #1d4f7c; min-width: 5.5rem; }
.alist .xy { color: var(--ink-soft); font-size: .72rem; }
.hint { color: var(--ink-soft); font-size: .76rem; }
.viewer { width: 100%; height: min(88vh, 62rem); background: #f4f1ea;
          border: 1px solid var(--rule); touch-action: none; position: relative; }
.stage { position: sticky; top: .8rem; }
.ref-label { box-sizing: border-box; min-width: 17px; height: 17px; padding: 0 3px;
             display: flex; align-items: center; justify-content: center;
             font-family: Verdana, sans-serif; font-size: 10px; font-weight: 700;
             color: rgba(140,40,40,.85);
             border: 1px solid transparent; border-radius: 3px;
             background: rgba(255,255,255,.55);
             pointer-events: auto; z-index: 8; }
.ref-label.unc { color: #5a4a10; border: 1px dashed #8a6d1a;
                 background: #f0cf3e; }
.ref-label.picked { outline: 3px solid #2a6db3; outline-offset: 1px; }
.black-dot { width: 10px; height: 10px; border-radius: 50%;
             background: rgba(20,20,20,.75); border: 1px solid #fff;
             pointer-events: none; z-index: 4; }
.pgn-fill { fill: rgba(42,109,179,.16); stroke: #1d4f7c; stroke-width: 2;
            pointer-events: auto; cursor: pointer; }
.pgn-fill.sel { fill: rgba(138,51,36,.22); stroke: #8a3324; }
.pgn-fill.pend { fill: rgba(42,109,179,.08); stroke-dasharray: 6 4; }
.pgn-vtx { fill: #1d4f7c; stroke: #fff; stroke-width: 1.5; }
.pgn-hit { fill: none; stroke: transparent; stroke-width: 14;
           stroke-linejoin: round; }
.pgn-vtx:hover { stroke: #8a3324; }
.pgn-vtx.vselected { fill: #8a3324; stroke: #2a2620; r: 6; }
@media (max-width: 64rem) { .cols { grid-template-columns: 1fr; }
  .stage { position: static; order: -1; } }
</style>
</head>
<body>
<header>
  <h1>Pełzucki 1896 — the farms' polygons <span style="font-family:Verdana,sans-serif;font-size:.72rem;color:#8a6d3b">(v1 · click vertices, Enter closes, assign a farm)</span>
    <span style="font-family:Verdana,sans-serif;font-size:.68rem;letter-spacing:.05em;text-transform:uppercase;color:#fff;background:#8a6d3b;padding:.1rem .5rem;border-radius:.8rem;vertical-align:middle">working page</span></h1>
  <p class="hint"><kbd>D</kbd> draw/pan &middot; click = vertex &middot; <kbd>U</kbd> undo vertex &middot;
     <kbd>Enter</kbd> close &amp; assign &middot; <kbd>Esc</kbd> cancel / deselect &middot;
     <kbd>Del</kbd> delete selected &middot; click inside a polygon to select</p>
</header>
<div class="cols">
  <div class="side">
    <div class="box">
      <h2>Layers</h2>
      <p>
        <button class="btn on" id="ly-refs">red farm numbers</button>
        <button class="btn" id="ly-blacks">black farm sites</button>
        <button class="btn on" id="ly-pgns">polygons</button>
      </p>
    </div>
    <div class="box">
      <h2>Drawing</h2>
      <p>
        <button class="btn" id="modebtn">Draw mode (D)</button>
        <button class="btn" id="undobtn">undo vertex (U)</button>
        <button class="btn" id="cancelbtn">cancel (Esc)</button>
      </p>
      <p style="margin:.2rem 0 .4rem">
        <input id="fnum" placeholder="farm no." autocomplete="off" spellcheck="false"
               inputmode="numeric">
        <button class="btn primary" id="closebtn">close &amp; assign (Enter)</button></p>
      <p style="margin:.2rem 0 .4rem">
        <input id="pnote" placeholder="note (optional)"></p>
      <p style="margin:.2rem 0 .4rem">
        <input id="fixnum" placeholder="the tag's right number" autocomplete="off"
               spellcheck="false" inputmode="text">
        <button class="btn" id="numbtn">change the tag (N)</button></p>
      <p class="hint" id="modehint">press D, click the vertices round a farm's parcels,
        type the farm no. (or leave empty to take the nearest confident tag inside),
        Enter. A tag picked on the map can be renumbered: N, type, Enter.</p>
    </div>
    <div class="box">
      <h2>Missing from the map <span id="mcount"></span></h2>
      <div class="hint" id="missing"></div>
    </div>
    <div class="box">
      <h2>The farms <span id="fcount"></span></h2>
      <ul class="alist" id="flist"></ul>
      <p style="margin:.5rem 0 0">
        <button class="btn primary" id="export">Export JSON</button>
        <button class="btn" id="del">Delete selected</button>
      </p>
    </div>
  </div>
  <div class="stage">
    <div id="viewer" class="viewer"></div>
    <p class="hint" style="font-family:Verdana,sans-serif;margin-top:.4rem">
      positions in the mosaic's pixels (21715 &times; 14206) &middot; the areas are
      estimates (~0.4 m/px)</p>
  </div>
</div>
<script id="ref-data" type="application/json">@@REFS@@</script>
<script id="black-data" type="application/json">@@BLACKS@@</script>
<script id="row-data" type="application/json">@@ROWS@@</script>
<script src="/site/assets/maps/openseadragon.min.js"
        onerror="this.remove();var s=document.createElement('script');
        s.src='https://cdn.jsdelivr.net/npm/openseadragon@4.1.0/build/openseadragon/openseadragon.min.js';
        document.head.appendChild(s);"></script>
<script>
// the load check: if OpenSeadragon never arrived (the page opened from disk,
// not through the server), say so in the viewer instead of failing silently
window.addEventListener('DOMContentLoaded', function () {
  setTimeout(function () {
    if (!window.OpenSeadragon) {
      var v = document.getElementById('viewer');
      if (v) v.innerHTML = '<div style="padding:2rem;font-family:Verdana,' +
        'sans-serif;color:#b3362c"><b>OpenSeadragon did not load.</b><br>' +
        'Open this page through the repository server:' +
        '<br><code>http://localhost:8779/scratch/map4456/farm_polygons.html</code>' +
        '<br>(the page loads /site/assets/maps/openseadragon.min.js, which only' +
        ' resolves from the repository root)</div>';
    }
  }, 1500);
});
</script>
<script>
(function () {
  var REFS = JSON.parse(document.getElementById('ref-data').textContent);
  var BLACKS = JSON.parse(document.getElementById('black-data').textContent);
  var ROWS = JSON.parse(document.getElementById('row-data').textContent);
  var PX2_PER_SAZ = @@PXSAZ@@;
  var K = 'p1896-farms-v1';
  var pgns = [];
  try { pgns = JSON.parse(localStorage.getItem(K) || '[]'); } catch (e) {}

  var layers = { refs: true, blacks: false, pgns: true };
  var drawMode = false, pend = [], sel = -1, dragP = null;
  var pickFarm = null;   // the tag clicked on the map — the polygon's farm

  var viewer = OpenSeadragon({
    id: 'viewer', prefixUrl: '', showNavigationControl: false,
    tileSources: '@@TILES@@', crossOriginPolicy: 'Anonymous',
    maxZoomPixelRatio: 6, visibilityRatio: 0.5, animationTime: 0.5,
    gestureSettingsMouse: { clickToZoom: false, dblClickToZoom: true }
  });
  var world = null, W = 0, H = 0;
  viewer.addHandler('open', function () {
    world = viewer.world.getItemAt(0);
    W = world.source.width; H = world.source.height;
    drawTags(); drawAll();
  });

  // ---- the tag overlays -----------------------------------------------------
  var ovs = [];
  function drawTags() {
    ovs.forEach(function (o) { viewer.removeOverlay(o.el); });
    ovs = [];
    if (layers.refs) {
      REFS.forEach(function (r) {
        var d = document.createElement('div');
        d.className = 'ref-label' + (typeof r.n === 'string' ? ' unc' : '') +
          (pickFarm && pickFarm.x === r.x && pickFarm.y === r.y ? ' picked' : '');
        d.textContent = r.n;
        d.title = 'farm ' + r.n + ' - click to choose it for the polygon' +
          ' (its row lights in the list)';
        d.style.pointerEvents = 'auto';
        d.style.cursor = 'pointer';
        // pointerdown AND mousedown: Firefox's ordering of the two on
        // transformed overlays is not Chrome's — listening to both (with
        // the pointerdown setting a guard the mousedown checks) makes the
        // pick land exactly once, in every browser
        var picked = 0;
        function onDown(ev) {
          if (drawMode) return;   // in draw mode the click lays a vertex
          ev.preventDefault(); ev.stopPropagation();
          var now = Date.now();
          if (now - picked < 500) return;   // the pair's second event
          picked = now;
          pickTag(r);
        }
        d.addEventListener('pointerdown', onDown);
        d.addEventListener('mousedown', onDown);
        var p = viewer.viewport.imageToViewportCoordinates(
          new OpenSeadragon.Point(r.x, r.y));
        viewer.addOverlay({ element: d, location: p,
          placement: OpenSeadragon.Placement.CENTER,
          rotationMode: OpenSeadragon.OverlayRotationMode.NO_ROTATION });
        ovs.push({ el: d });
      });
    }
    if (layers.blacks) {
      BLACKS.forEach(function (b) {
        var d = document.createElement('div');
        d.className = 'black-dot';
        d.title = 'black site: farm ' + b.n;
        var p = viewer.viewport.imageToViewportCoordinates(
          new OpenSeadragon.Point(b.x, b.y));
        viewer.addOverlay({ element: d, location: p,
          placement: OpenSeadragon.Placement.CENTER,
          rotationMode: OpenSeadragon.OverlayRotationMode.NO_ROTATION });
        ovs.push({ el: d });
      });
    }
  }

  // ---- the svg polygon layer ------------------------------------------------
  var viewerEl = document.getElementById('viewer');
  var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;' +
    'pointer-events:none;z-index:6;transform:none;';
  viewerEl.appendChild(svg);

  // the wheel, once, at the container in the capture phase: everything the
  // event can land on that is NOT OpenSeadragon's own canvas (the polygons,
  // the outline's grab band, the tag overlays) is FORWARDED to the canvas as
  // a synthetic wheel event — OpenSeadragon then zooms with its own handler,
  // identical to hovering the bare map, in every browser (the manual zoom
  // math disagreed with Firefox's wheel handling)
  viewerEl.addEventListener('wheel', function (ev) {
    if (!world || !viewer.canvas) return;
    if (viewer.canvas.contains(ev.target)) return;   // OSD handles it natively
    ev.preventDefault(); ev.stopPropagation();
    var fwd = new WheelEvent('wheel', {
      deltaY: ev.deltaY, deltaX: ev.deltaX, deltaMode: ev.deltaMode,
      clientX: ev.clientX, clientY: ev.clientY, screenX: ev.screenX,
      screenY: ev.screenY, button: 0, bubbles: true, cancelable: true,
      view: window
    });
    viewer.canvas.dispatchEvent(fwd);
  }, { capture: true, passive: false });

  function toEl(p) {
    var v = viewer.viewport.imageToViewerElementCoordinates(
      new OpenSeadragon.Point(p[0], p[1]));
    return [v.x, v.y];
  }
  function inside(pt, pts) {
    var x = pt[0], y = pt[1], c = false;
    for (var i = 0, j = pts.length - 1; i < pts.length; j = i++) {
      var xi = pts[i][0], yi = pts[i][1], xj = pts[j][0], yj = pts[j][1];
      if (((yi > y) !== (yj > y)) &&
          (x < (xj - xi) * (y - yi) / (yj - yi) + xi)) c = !c;
    }
    return c;
  }
  function areaPx(pts) {
    var a = 0;
    for (var i = 0, j = pts.length - 1; i < pts.length; j = i++) {
      a += (pts[j][0] + pts[i][0]) * (pts[j][1] - pts[i][1]);
    }
    return Math.abs(a / 2);
  }
  function centroid(pts) {
    var x = 0, y = 0;
    pts.forEach(function (p) { x += p[0]; y += p[1]; });
    return [x / pts.length, y / pts.length];
  }

  function drawAll() {
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    if (!layers.pgns) return;
    pgns.forEach(function (g, k) {
      if (g.pts.length < 3) return;
      var el = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
      el.setAttribute('points', g.pts.map(toEl).map(function (p) {
        return p[0] + ',' + p[1]; }).join(' '));
      el.setAttribute('class', 'pgn-fill' + (k === sel ? ' sel' : ''));
      el.addEventListener('mousedown', function (ev) {
        if (!drawMode) { ev.preventDefault(); ev.stopPropagation(); selectP(k); }
      });
      svg.appendChild(el);
      // the selected polygon gets its vertices (draggable); any point of
      // the outline itself is a handle: mousedown on the edge inserts a
      // vertex there and the drag moves it — no midpoints to aim for
      if (k === sel) {
        // the outline's grab band first, the vertex dots after: the paint
        // order is the hit order in SVG, so the dots sit above the band
        // and a mousedown on a vertex moves it instead of inserting
        var hit = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
        hit.setAttribute('points', el.getAttribute('points'));
        hit.setAttribute('class', 'pgn-hit');
        hit.style.pointerEvents = 'auto';
        attachEdgeDrag(hit, g);
        svg.appendChild(hit);
        g.pts.forEach(function (p, i) {
          var e = toEl(p);
          var c = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
          c.setAttribute('cx', e[0]); c.setAttribute('cy', e[1]);
          c.setAttribute('r', 5);
          c.setAttribute('class', 'pgn-vtx' +
            (vSel && vSel.g === g && vSel.idx === i ? ' vselected' : ''));
          c.style.pointerEvents = 'auto'; c.style.cursor = 'move';
          attachVtxDrag(c, g, i, false);
          svg.appendChild(c);
        });
      }
    });
    if (pend.length) {
      if (pend.length > 1) {
        var pl = document.createElementNS('http://www.w3.org/2000/svg', 'polyline');
        pl.setAttribute('points', pend.map(toEl).map(function (p) {
          return p[0] + ',' + p[1]; }).join(' '));
        pl.setAttribute('class', 'pgn-fill pend');
        pl.setAttribute('fill', 'rgba(42,109,179,.08)');
        svg.appendChild(pl);
      }
      pend.forEach(function (p) {
        var e = toEl(p);
        var c = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        c.setAttribute('cx', e[0]); c.setAttribute('cy', e[1]);
        c.setAttribute('r', 4);
        c.setAttribute('class', 'pgn-vtx');
        svg.appendChild(c);
      });
    }
    syncList();
  }
  viewer.addHandler('update-viewport', drawAll);

  function selectP(k) {
    sel = (sel === k ? -1 : k);
    vSel = null;
    var hint = document.getElementById('modehint');
    if (sel >= 0) {
      var g = pgns[sel];
      document.getElementById('fnum').value = g.farm;
      document.getElementById('pnote').value = g.note || '';
      hint.innerHTML = 'polygon of farm <b>' + g.farm + '</b> (' +
        (Math.round(areaPx(g.pts) / PX2_PER_SAZ)).toLocaleString() +
        ' saz est.) &mdash; drag a vertex to reshape, drag anywhere on the' +
        ' edge to add a point; Ctrl+Z undoes; Enter reassigns, Delete removes';
    } else {
      hint.textContent = 'press D, click the vertices round the parcels of a farm';
    }
    drawAll();
  }

  // ---- the undo stack ---------------------------------------------------------
  // every mutating action pushes the previous state; Ctrl+Z pops one back
  var undoStack = [];
  var MAX_UNDO = 50;
  function snapshot(label) {
    undoStack.push({ label: label,
      state: JSON.stringify(pgns), sel: sel });
    if (undoStack.length > MAX_UNDO) undoStack.shift();
  }
  function undo() {
    var s = undoStack.pop();
    if (!s) { setHint('nothing to undo'); return; }
    pgns = JSON.parse(s.state);
    sel = Math.min(s.sel, pgns.length - 1);
    if (sel < -1) sel = -1;
    persist(); drawAll();
    setHint('undone: ' + s.label + (undoStack.length
      ? ' &mdash; ' + undoStack.length + ' step' + (undoStack.length > 1 ? 's' : '') + ' back'
      : ' &mdash; the stack is empty'));
  }

  // ---- vertex and edge dragging ---------------------------------------------
  var vDrag = null;   // { g, idx, live }
  var vSel = null;    // { g, idx } — the vertex picked for Delete
  function attachVtxDrag(node, g, idx, isMid) {
    node.addEventListener('mousedown', function (ev) {
      if (drawMode || ev.button !== 0) return;
      ev.preventDefault(); ev.stopPropagation();
      vDrag = { g: g, idx: idx, live: true };
      vSel = { g: g, idx: idx };
      window.addEventListener('mousemove', onVtxMove, true);
      window.addEventListener('mouseup', onVtxUp, true);
      drawAll();
      setHint('vertex picked &mdash; drag to move, Delete removes it' +
        (g.pts.length <= 3 ? ' (a polygon keeps at least 3)' : ''));
    });
  }
  // mousedown anywhere on the outline: find the nearest edge, insert a
  // vertex at the pointer, and hand the drag to that new vertex
  function attachEdgeDrag(node, g) {
    node.addEventListener('mousedown', function (ev) {
      if (drawMode || ev.button !== 0) return;
      ev.preventDefault(); ev.stopPropagation();
      var r = viewerEl.getBoundingClientRect();
      var elPt = [ev.clientX - r.left, ev.clientY - r.top];
      var p = world.viewerElementToImageCoordinates(
        new OpenSeadragon.Point(elPt[0], elPt[1]));
      // the nearest edge is judged in ELEMENT space (both the pointer and
      // the segments) — mixing image and element coords sent the insert to
      // the wrong edge (farm 8's shape jumping to the beginning)
      var best = -1, bestD = 1e18;
      for (var i = 0; i < g.pts.length; i++) {
        var a = toEl(g.pts[i]), b = toEl(g.pts[(i + 1) % g.pts.length]);
        var d = distToSeg(elPt, a, b);
        if (d < bestD) { bestD = d; best = i; }
      }
      if (best < 0) return;
      snapshot('point into the outline');
      // insert after edge `best`'s first vertex, at the pointer's position
      var ins = [Math.round(p.x), Math.round(p.y)];
      g.pts.splice(best + 1, 0, ins);
      persist();
      // and the drag moves the new vertex from now on
      vDrag = { g: g, idx: best + 1, live: true };
      window.addEventListener('mousemove', onVtxMove, true);
      window.addEventListener('mouseup', onVtxUp, true);
      drawAll();
      setHint('a point went into the outline &mdash; drag it where the edge belongs, release to fix');
    });
  }
  function distToSeg(p, a, b) {
    var dx = b[0] - a[0], dy = b[1] - a[1];
    var l2 = dx * dx + dy * dy;
    var t = l2 ? ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / l2 : 0;
    t = Math.max(0, Math.min(1, t));
    var x = a[0] + t * dx, y = a[1] + t * dy;
    return Math.hypot(p[0] - x, p[1] - y);
  }
  function onVtxMove(ev) {
    if (!vDrag) return;
    if (!vDrag.snap) { snapshot('vertex reshape'); vDrag.snap = true; }
    var r = viewerEl.getBoundingClientRect();
    var p = world.viewerElementToImageCoordinates(
      new OpenSeadragon.Point(ev.clientX - r.left, ev.clientY - r.top));
    vDrag.g.pts[vDrag.idx] = [Math.round(p.x), Math.round(p.y)];
    persist();
    drawAll();
  }
  function onVtxUp(ev) {
    if (!vDrag) return;
    window.removeEventListener('mousemove', onVtxMove, true);
    window.removeEventListener('mouseup', onVtxUp, true);
    vDrag = null;
    persist();
    drawAll();
  }

  // clicking a tag chooses the farm for the next polygon: the assign field
  // fills (when the read is confident), the row lights in the list, and the
  // list jumps to the row — the drawing then starts wherever the parcels are
  function pickTag(r) {
    pickFarm = { n: r.n, x: r.x, y: r.y };
    // the field always takes the read: a confident number fills it ready to
    // close, an uncertain read fills it so you can correct before assigning
    document.getElementById('fnum').value = r.n;
    document.getElementById('fixnum').value = r.n;
    var hint = document.getElementById('modehint');
    var n = typeof r.n === 'number' ? r.n : String(r.n);
    var row = ROWS.filter(function (q) { return q.n === n; })[0];
    hint.innerHTML = 'farm <b>' + n + '</b>' +
      (row ? ' (' + row.name + ')' : '') +
      ' chosen &mdash; press D and click the vertices round its parcels;' +
      ' Enter assigns the field. The tag renumbers in the change field' +
      ' (N): type the right number, Enter.' + (typeof r.n === 'string' ?
      ' The read is uncertain &mdash; correct it there or in the farm field.' : '');
    uLightRow(n);
  }

  // ---- changing a tag's number ----------------------------------------------
  // the fixes ride in the page (localStorage by mosaic position) and in the
  // export's red_fixes — the same record the yard map's build bakes in
  var K_FIX = 'p1896-redfix-v1';
  var fixes = {};
  try { fixes = JSON.parse(localStorage.getItem(K_FIX) || '{}'); } catch (e) {}
  function persistFixes() {
    try { localStorage.setItem(K_FIX, JSON.stringify(fixes)); } catch (e) {}
  }
  function applyFix() {
    if (!pickFarm) { setHint('click a tag on the map first'); return false; }
    var v = document.getElementById('fixnum').value.trim();
    if (!v) { setHint('the change field is empty'); return false; }
    var ok = /^[0-9\\[\\]\\/?]+$/.test(v) &&
      (/[0-9]/.test(v) || v === '[?]');
    if (!ok) {
      setHint('the number takes digits &mdash; uncertainty in [..?], or [?]');
      return false;
    }
    var k = pickFarm.x + ',' + pickFarm.y;
    var oldN = pickFarm.n;
    fixes[k] = v;
    persistFixes();
    // the tag itself follows at once
    var r = REFS.filter(function (q) {
      return q.x === pickFarm.x && q.y === pickFarm.y; })[0];
    if (r) {
      r.n = v;
      drawTags();
    }
    // the polygons drawn for this farm follow: the assignment was made on
    // the strength of the tag, so the renumber carries (uncertain values
    // like "[33?]" do not reassign — a polygon wants a real row number)
    var moved = 0;
    if (/^[0-9]+$/.test(v)) {
      pgns.forEach(function (g) {
        if (g.farm === oldN) { g.farm = parseInt(v, 10); moved++; }
      });
      if (moved) {
        snapshot('polygons ' + oldN + ' -> ' + v);
        persist();
      }
    }
    // the pick and the farm field follow too
    pickFarm.n = v;
    document.getElementById('fnum').value = v;
    setHint('the tag at (' + pickFarm.x + ', ' + pickFarm.y + ') reads <b>' +
      v + '</b> now' +
      (moved ? ' &mdash; ' + moved + ' polygon' + (moved > 1 ? 's' : '') +
        ' reassign' + (moved > 1 ? '' : 's') + ' to farm ' + v
              : ' &mdash; it rides in the export as red_fixes'));
    return true;
  }
  document.getElementById('numbtn').addEventListener('click', applyFix);
  document.getElementById('fixnum').addEventListener('keydown', function (ev) {
    if (ev.key === 'Enter') {
      ev.preventDefault();
      applyFix();
    } else if (ev.key === 'Escape') {
      ev.target.blur();
    }
  });
  function uLightRow(n) {
    var ul = document.getElementById('flist');
    var lis = ul.children;
    for (var i = 0; i < lis.length; i++) {
      lis[i].classList.toggle('selrow',
        lis[i].getAttribute('data-row') == String(n));
    }
    var el = ul.querySelector('[data-row="' + n + '"]');
    if (el) el.scrollIntoView({ block: 'nearest' });
  }
  // ---- drawing --------------------------------------------------------------
  var modebtn = document.getElementById('modebtn');
  function applyMode() {
    modebtn.classList.toggle('on', drawMode);
    modebtn.textContent = drawMode ? 'Pan mode (D)' : 'Draw mode (D)';
  }
  function toggleMode() {
    drawMode = !drawMode; applyMode();
    if (drawMode) { pend = []; sel = -1; drawAll(); }
  }
  modebtn.addEventListener('click', toggleMode);

  function elPos(ev) {
    var r = viewerEl.getBoundingClientRect();
    return { x: ev.clientX - r.left, y: ev.clientY - r.top };
  }
  function imgPos(el) {
    var p = world.viewerElementToImageCoordinates(
      new OpenSeadragon.Point(el.x, el.y));
    return [p.x, p.y];
  }
  viewerEl.addEventListener('click', function (ev) {
    if (!drawMode || !world || ev.button !== 0) return;
    if (ev.target.closest && ev.target.closest('button, input')) return;
    var p = imgPos(elPos(ev));
    if (p[0] < 0 || p[1] < 0 || p[0] > W || p[1] > H) return;
    pend.push([Math.round(p[0]), Math.round(p[1])]);
    drawAll();
    document.getElementById('modehint').textContent =
      pend.length + ' vertices — click more, U undoes, Enter closes';
  });

  function closePolygon() {
    if (pend.length < 3) {
      setHint('a polygon wants at least 3 vertices');
      return;
    }    var fv = document.getElementById('fnum').value.trim();
    var farm = null;
    if (fv !== '' && /^\\d+$/.test(fv)) {
      farm = parseInt(fv, 10);
    } else if (pickFarm && typeof pickFarm.n === 'number') {
      farm = pickFarm.n;               // the tag clicked on the map
    } else {
      // the nearest confident tag inside the polygon
      var best = null;
      REFS.forEach(function (r) {
        if (typeof r.n !== 'string' && inside([r.x, r.y], pend)) {
          var c = centroid(pend);
          var d = Math.abs(r.x - c[0]) + Math.abs(r.y - c[1]);
          if (!best || d < best.d) best = { n: r.n, d: d };
        }
      });
      if (!best) {
        setHint('no confident tag inside — type the farm no. first');
        return;
      }
      farm = best.n;
    }
    snapshot('polygon drawn');
    pgns.push({ farm: farm, pts: pend.slice(),
                note: document.getElementById('pnote').value.trim() });
    pend = [];
    pickFarm = null;
    document.getElementById('fnum').value = '';
    document.getElementById('pnote').value = '';
    persist(); drawAll();
    setHint('farm ' + farm + ' drawn (' + pgns.length + ' polygons) — keep going, or click inside one to edit');
  }
  function setHint(t) {
    document.getElementById('modehint').innerHTML = t;
  }
  function persist() {
    try { localStorage.setItem(K, JSON.stringify(pgns)); } catch (e) {}
  }

  // ---- the farms list -------------------------------------------------------
  function sitesByRow() {
    var m = {};
    ROWS.forEach(function (r) { m[r.n] = { c: 0, u: 0, inC: 0, inU: 0, first: null }; });
    REFS.forEach(function (r) {
      var n = typeof r.n === 'string' ? null : r.n;
      var key = null;
      if (n !== null && m[n]) key = n;
      else {
        // an uncertain read: count toward every row it might name? No — its
        // canonical digits, when they parse
        var s = String(r.n).replace(/[^0-9]/g, '');
        if (s && m[parseInt(s, 10)] && s.length <= 2) key = parseInt(s, 10);
      }
      if (key === null) return;
      var rec = m[key];
      var isU = typeof r.n === 'string';
      var isIn = pgns.some(function (g, k) {
        return g.farm === key && inside([r.x, r.y], g.pts); });
      if (isU) { rec.u++; if (isIn) rec.inU++; }
      else { rec.c++; if (isIn) rec.inC++; }
      if (!rec.first) rec.first = [r.x, r.y];
    });
    return m;
  }
  function syncList() {
    var m = sitesByRow();
    var ul = document.getElementById('flist');
    ul.innerHTML = '';
    var drawn = 0;
    ROWS.forEach(function (r) {
      var rec = m[r.n];
      var gp = pgns.filter(function (g) { return g.farm === r.n; });
      if (gp.length) drawn++;
      var est = gp.reduce(function (s, g) { return s + areaPx(g.pts); }, 0) / PX2_PER_SAZ;
      var tot = r.total[0] * 2400 + r.total[1];
      var li = document.createElement('li');
      var status = gp.length
        ? (est ? ' ~' + Math.round(100 * est / tot) + '%' : '')
        : (rec.c ? ' tags ' + rec.c : (rec.u ? ' only [?]' : ' none'));
      var dot = gp.length ? '\u25a0' : (rec.c ? '\u25a1' : '\u00b7');
      li.setAttribute('data-row', r.n);
      // the completion shading: the polygon estimate against the row's
      // statement total — under 100% the tint deepens toward green, over
      // 100% it slides to red (a few points of slack are fine)
      if (gp.length && est && tot) {
        var pct = est / tot;
        var sh;
        if (pct >= 1) {
          // over 100%: the red keeps deepening through 2x — 110% a light
          // red, 150% a strong red, 167%+ a dark maroon (the over-share
          // matters: it says whose land the polygon swallowed)
          var o = Math.min(1, Math.log(pct) / Math.log(2.0));
          sh = 'background:rgba(' + Math.round(179 + 76 * o) + ',' +
            Math.round(220 - 176 * o) + ',' + Math.round(120 - 96 * o) + ',' +
            (0.25 + 0.60 * o).toFixed(2) + ')';
        } else {
          var u = Math.min(1, 1 - pct);                // 1 at 0%, 0 at 100%
          sh = 'background:rgba(' + Math.round(46 + 180 * u) + ',' +
            Math.round(125 + 94 * u) + ',' + Math.round(50 + 150 * u) + ',' +
            (0.62 - 0.42 * u).toFixed(2) + ')';
        }
        li.setAttribute('style', sh);
      } else if (gp.length && !est) {
        li.setAttribute('style', 'background:rgba(107,100,89,.15)');
      }
      li.innerHTML = '<span class="v">' + dot + ' ' + r.n + '</span>' +
        '<span class="xy">' + r.name + ', ' + r.total[0] + 'd' + r.total[1] +
        ' &middot; ' + (gp.length ? gp.length + ' pgn' + (gp.length > 1 ? 's' : '') +
        (est ? ' ~' + Math.round(est).toLocaleString() + ' saz' : '') : 'no polygon') +
        status + '</span>';
      li.addEventListener('click', function () {
        var tgt = gp.length ? centroid(gp[0].pts) : rec.first;
        if (tgt) viewer.viewport.panTo(viewer.viewport.imageToViewportCoordinates(
          new OpenSeadragon.Point(tgt[0], tgt[1])));
        sel = -1; drawAll();
      });
      ul.appendChild(li);
    });
    document.getElementById('fcount').textContent =
      '(' + drawn + ' of ' + ROWS.length + ' drawn)';
  }
  // the missing rows: no confident tag anywhere
  (function () {
    var m = sitesByRow();
    var miss = ROWS.filter(function (r) { return m[r.n].c === 0; });
    document.getElementById('mcount').textContent = '(' + miss.length + ')';
    document.getElementById('missing').innerHTML = miss.map(function (r) {
      return '<b>' + r.n + '</b> ' + r.name + ' (' + r.total[0] + 'd' +
        r.total[1] + ')' + (m[r.n].u ? ' — only [?] tags' : '');
    }).join('<br>') || 'none — every row has a confident tag';
  })();

  // ---- keys and buttons -----------------------------------------------------
  document.addEventListener('keydown', function (ev) {
    if (ev.target.tagName === 'INPUT') {
      if (ev.key === 'Enter' && ev.target.id === 'fnum') {
        ev.preventDefault();
        if (pend.length) closePolygon();
        else if (sel >= 0) reassign();
      }
      return;
    }
    if (ev.key === 'd' || ev.key === 'D') { ev.preventDefault(); toggleMode(); }
    // N: focus the change field for the picked tag
    if (ev.key === 'n' || ev.key === 'N') {
      var f = document.getElementById('fixnum');
      f.focus(); f.select();
    }
    if ((ev.key === 'u' || ev.key === 'U') && pend.length) {
      ev.preventDefault(); pend.pop(); drawAll();
    }
    if (ev.key === 'Enter' && pend.length) { ev.preventDefault(); closePolygon(); }
    if (ev.key === 'Escape') {
      if (pend.length) { pend = []; drawAll(); setHint('the pending polygon is gone'); }
      else { sel = -1; vSel = null; drawAll(); }
    }
    if ((ev.key === 'Delete') && sel >= 0 && !vSel) {
      snapshot('polygon deleted');
      pgns.splice(sel, 1); sel = -1; persist(); drawAll();
    }
    // Delete with a picked vertex: the vertex goes (a polygon keeps 3)
    if ((ev.key === 'Delete') && vSel) {
      ev.preventDefault();
      var g = vSel.g, i = vSel.idx;
      vSel = null;
      if (g.pts.length <= 3) {
        setHint('a polygon keeps at least 3 vertices &mdash; Delete the whole polygon instead');
      } else {
        snapshot('vertex deleted');
        g.pts.splice(i, 1);
        persist();
        drawAll();
        setHint('the vertex is gone &mdash; Ctrl+Z brings it back');
      }
      return;
    }
    // Ctrl+Z: undo the last polygon action
    if ((ev.ctrlKey || ev.metaKey) && (ev.key === 'z' || ev.key === 'Z')) {
      ev.preventDefault(); undo();
    }
  });
  function reassign() {
    var fv = document.getElementById('fnum').value.trim();
    if (!/^\\d+$/.test(fv) || sel < 0) return;
    snapshot('reassign to ' + fv);
    pgns[sel].farm = parseInt(fv, 10);
    pgns[sel].note = document.getElementById('pnote').value.trim();
    persist(); drawAll();
    setHint('the polygon reads farm ' + fv + ' now');
  }
  document.getElementById('closebtn').addEventListener('click', function () {
    if (pend.length) closePolygon(); else if (sel >= 0) reassign();
  });
  document.getElementById('undobtn').addEventListener('click', function () {
    if (pend.length) { pend.pop(); drawAll(); }
  });
  document.getElementById('cancelbtn').addEventListener('click', function () {
    if (pend.length) { pend = []; drawAll(); } else { sel = -1; drawAll(); }
  });
  document.getElementById('del').addEventListener('click', function () {
    if (sel >= 0) { pgns.splice(sel, 1); sel = -1; persist(); drawAll(); }
  });
  document.getElementById('export').addEventListener('click', function () {
    var blob = new Blob([JSON.stringify({ polygons: pgns,
      red_fixes: fixes,
      calibration: { px2_per_saz: PX2_PER_SAZ, note: 'approximate (~0.4 m/px)' } },
      null, 1)], { type: 'application/json' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'farm_polygons.json';
    a.click();
  });
  [['ly-refs', 'refs'], ['ly-blacks', 'blacks'], ['ly-pgns', 'pgns']]
  .forEach(function (p) {
    document.getElementById(p[0]).addEventListener('click', function () {
      layers[p[1]] = !layers[p[1]];
      this.classList.toggle('on', layers[p[1]]);
      drawTags(); drawAll();
    });
  });

  applyMode();
  window.__farms = { alive: true };
})();
</script>
</body>
</html>
"""
HTML = HTML.replace("@@REFS@@", json.dumps(refs, ensure_ascii=False))
HTML = HTML.replace("@@BLACKS@@", json.dumps(blacks, ensure_ascii=False))
HTML = HTML.replace("@@ROWS@@", json.dumps(rows, ensure_ascii=False))
HTML = HTML.replace("@@PXSAZ@@", repr(PX2_PER_SAZ))
HTML = HTML.replace("@@TILES@@", TILES)
out = ROOT + r"\scratch\map4456\farm_polygons.html"
with open(out, "w", encoding="utf-8") as f:
    f.write(HTML)
print("red tags:", len(refs), "| black sites:", len(blacks),
      "| rows:", len(rows))
print("wrote", out, round(len(HTML) / 1e3, 1), "KB")
