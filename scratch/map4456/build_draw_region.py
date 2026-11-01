# The region-drawing page: the full mosaic in the site's viewer; a polyline
# drawn by clicking lays down the area where numbers should be looked at;
# close it and every OCR token on the map is shown inside (solid) or
# outside (faded) the region, with counts. Export the polygon as JSON.
# Output: scratch/map4456/draw_region.html
import json

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld"
TILES = "https://takaji10.github.io/triebenfeld-maps/pelzucki1896/info.json"
RED = json.load(open(ROOT + r"\scratch\map4456\numbers_easy2.json", encoding="utf-8"))
BLACK = json.load(open(ROOT + r"\scratch\map4456\numbers_black.json", encoding="utf-8"))

toks = []
for t in RED:
    toks.append({"x": t["x"] + t["w"] // 2, "y": t["y"] + t["h"] // 2,
                 "ink": "red", "text": t["text"], "conf": t["conf"]})
for t in BLACK:
    toks.append({"x": t["x"] + t["w"] // 2, "y": t["y"] + t["h"] // 2,
                 "ink": "black", "text": t["text"], "conf": t["conf"]})
print("tokens carried:", len(toks))

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Pełzucki 1896 — draw the region of interest (working page)</title>
<style>
:root { --rule: #d8d2c4; --ink: #2a2620; --ink-soft: #6b6459; --accent: #8a3324; }
body { margin: 0; background: #faf8f3; color: var(--ink); font-family: Georgia, serif; }
header { max-width: 120rem; margin: 0 auto; padding: .9rem 2rem .2rem; }
header h1 { font-size: 1.2rem; margin: 0 0 .2rem; }
header p { font-size: .85rem; color: var(--ink-soft); margin: .15rem 0; }
.cols { display: grid; grid-template-columns: minmax(19rem, 24rem) minmax(0, 1fr);
        gap: 1.4rem; align-items: start; max-width: 120rem; margin: 0 auto;
        padding: 0 2rem 2rem; }
.side { max-height: 92vh; overflow-y: auto; font-family: Verdana, sans-serif;
        font-size: .82rem; }
.box { border: 1px solid var(--rule); border-radius: .4rem; padding: .7rem .9rem;
       margin: 0 0 .8rem; }
.box h2 { font-size: .9rem; margin: 0 0 .4rem; }
.btn { font-family: Verdana, sans-serif; font-size: .78rem; padding: .3rem .8rem;
       border: 1px solid var(--rule); background: #fff; cursor: pointer;
       border-radius: 3px; margin: 0 .3rem .3rem 0; }
.btn.primary { background: var(--accent); color: #fff; border-color: var(--accent); }
.btn:disabled { opacity: .4; cursor: default; }
.counts { margin: .4rem 0 0; }
.counts b { font-variant-numeric: tabular-nums; }
.kbd { border: 1px solid var(--rule); border-radius: 3px; padding: 0 .3rem;
       background: #fff; font-size: .72rem; }
.viewer { width: 100%; height: min(88vh, 62rem); background: #f4f1ea;
          border: 1px solid var(--rule); touch-action: none; position: relative; }
.stage { position: sticky; top: .8rem; }
.poly-canvas { position: absolute; inset: 0; pointer-events: none; z-index: 6; }
.tok-dot { box-sizing: border-box; position: absolute; border-radius: 50%;
           pointer-events: none; }
.tok-red { background: rgba(179,51,51,.85); }
.tok-black { background: rgba(40,38,34,.85); }
.tok-out { opacity: .18; }
.hint { color: var(--ink-soft); font-size: .76rem; }
@media (max-width: 64rem) { .cols { grid-template-columns: 1fr; }
  .stage { position: static; order: -1; } }
</style>
</head>
<body>
<header>
  <h1>Pełzucki 1896 — draw the region of interest
    <span style="font-family:Verdana,sans-serif;font-size:.68rem;letter-spacing:.05em;text-transform:uppercase;color:#fff;background:#8a6d3b;padding:.1rem .5rem;border-radius:.8rem;vertical-align:middle">working page</span></h1>
  <p>Zoom to the drawn plan (you can follow the sheet edges roughly), then <b>click
     along its boundary</b> to lay vertices of a polyline around the area where
     numbers should be read. Close the polygon with the button (or
     <span class="kbd">Enter</span>); every OCR'd number on the map then shows
     <b>solid inside</b> your region and <b>faded outside</b> it, with counts —
     what the machine over-caught becomes visible. Export the polygon when it
     looks right; the next pass reads only inside it.</p>
</header>
<div class="cols">
  <div class="side">
    <div class="box">
      <h2>Drawing</h2>
      <p class="hint" id="pstate">no vertices yet — click on the map to start</p>
      <p>
        <button class="btn" id="undo">Undo vertex</button>
        <button class="btn primary" id="close">Close polygon (Enter)</button>
        <button class="btn" id="clear">Clear</button>
      </p>
      <p class="counts" id="counts"></p>
    </div>
    <div class="box">
      <h2>Export</h2>
      <button class="btn primary" id="export">Export polygon JSON</button>
      <p class="hint" id="expstate"></p>
    </div>
    <div class="box">
      <h2>Layers</h2>
      <label><input type="checkbox" id="showtok" checked> the OCR'd numbers
        (red dots / dark dots)</label><br>
      <label><input type="checkbox" id="showpoly" checked> the polygon</label>
    </div>
  </div>
  <div class="stage">
    <div id="viewer" class="viewer"></div>
    <p class="hint" style="font-family:Verdana,sans-serif;margin-top:.4rem">
      vertices and tokens are recorded in the mosaic's pixels (21715 &times; 14206)</p>
  </div>
</div>
<script id="tok-data" type="application/json">@@TOKS@@</script>
<script src="/site/assets/maps/openseadragon.min.js"></script>
<script>
(function () {
  var TOKS = JSON.parse(document.getElementById('tok-data').textContent);
  var viewer = OpenSeadragon({
    id: 'viewer', prefixUrl: '', showNavigationControl: false,
    tileSources: '@@TILES@@', crossOriginPolicy: 'Anonymous',
    maxZoomPixelRatio: 6, visibilityRatio: 0.5, animationTime: 0.5,
    gestureSettingsMouse: { clickToZoom: false, dblClickToZoom: true }
  });
  var world = null, opened = false;
  viewer.addHandler('open', function () {
    world = viewer.world.getItemAt(0); opened = true; drawTokens(); drawPoly();
  });

  // ---- the token dots ----------------------------------------------------
  var tokEls = [];
  function drawTokens() {
    tokEls.forEach(function (el) { viewer.removeOverlay(el); });
    tokEls = [];
    if (!document.getElementById('showtok').checked) return;
    TOKS.forEach(function (t) {
      var d = document.createElement('div');
      d.className = 'tok-dot tok-' + t.ink;
      var r = t.conf >= 0.6 ? 9 : 7;
      d.style.width = r + 'px'; d.style.height = r + 'px';
      var p = viewer.viewport.imageToViewportCoordinates(
        new OpenSeadragon.Point(t.x, t.y));
      viewer.addOverlay({ element: d, location: p,
        placement: OpenSeadragon.Placement.CENTER,
        rotationMode: OpenSeadragon.OverlayRotationMode.NO_ROTATION });
      tokEls.push(d);
    });
    applyInOut();
  }
  function applyInOut() {
    if (!poly.length || !closed) return;
    var nin = 0;
    TOKS.forEach(function (t, k) {
      var inside = pip(t.x, t.y);
      tokEls[k] && tokEls[k].classList.toggle('tok-out', !inside);
      if (inside) nin++;
    });
    var nr = 0, nb = 0;
    TOKS.forEach(function (t, k) {
      if (pip(t.x, t.y)) (t.ink === 'red' ? nr++ : nb++);
    });
    document.getElementById('counts').innerHTML =
      'region set: <b>' + nin + '</b> of ' + TOKS.length +
      ' tokens inside &mdash; red ' + nr + ', black ' + nb +
      ' (the faded ones are what would be dropped)';
  }

  // ---- the polyline ------------------------------------------------------
  var poly = [], closed = false;
  var cv = document.createElement('canvas');
  cv.className = 'poly-canvas';
  document.getElementById('viewer').appendChild(cv);
  var ctx = cv.getContext('2d');
  function sizeCv() {
    var r = document.getElementById('viewer').getBoundingClientRect();
    var dpr = window.devicePixelRatio || 1;
    cv.style.width = r.width + 'px'; cv.style.height = r.height + 'px';
    cv.width = Math.round(r.width * dpr); cv.height = Math.round(r.height * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  function drawPoly() {
    sizeCv();
    ctx.clearRect(0, 0, cv.width, cv.height);
    if (!document.getElementById('showpoly').checked || !poly.length) {
      updateState(); return;
    }
    var pts = poly.map(function (p) {
      var q = viewer.viewport.imageToViewerElementCoordinates(
        new OpenSeadragon.Point(p[0], p[1]));
      return [q.x, q.y];
    });
    if (closed && pts.length > 2) {
      ctx.beginPath();
      pts.forEach(function (p, i) { i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]); });
      ctx.closePath();
      ctx.fillStyle = 'rgba(138,51,36,.06)';
      ctx.fill();
    }
    ctx.beginPath();
    pts.forEach(function (p, i) { i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]); });
    if (closed) ctx.closePath();
    ctx.strokeStyle = 'rgba(138,51,36,.9)';
    ctx.lineWidth = 2;
    ctx.setLineDash(closed ? [] : [8, 6]);
    ctx.stroke();
    ctx.setLineDash([]);
    pts.forEach(function (p) {
      ctx.beginPath();
      ctx.arc(p[0], p[1], 4, 0, 6.29);
      ctx.fillStyle = '#8a3324';
      ctx.fill();
    });
    updateState();
  }
  function updateState() {
    var el = document.getElementById('pstate');
    if (!poly.length) el.textContent = 'no vertices yet - click on the map to start';
    else el.textContent = poly.length + ' vertices' + (closed ? ' - closed' : ' - still open');
    document.getElementById('close').disabled = closed || poly.length < 3;
    document.getElementById('undo').disabled = !poly.length;
    document.getElementById('export').disabled = !(closed && poly.length > 2);
  }
  function pip(x, y) {
    var inside = false;
    for (var i = 0, j = poly.length - 1; i < poly.length; j = i++) {
      var xi = poly[i][0], yi = poly[i][1], xj = poly[j][0], yj = poly[j][1];
      if (((yi > y) !== (yj > y)) &&
          (x < (xj - xi) * (y - yi) / (yj - yi) + xi)) inside = !inside;
    }
    return inside;
  }
  viewer.addHandler('canvas-click', function (e) {
    if (!opened || !e.quick || closed) return;
    var p = world.viewerElementToImageCoordinates(e.position);
    poly.push([Math.round(p.x), Math.round(p.y)]);
    drawPoly();
  });
  viewer.addHandler('canvas-double-click', function (e) {
    e.preventDefault();
  });
  ['animation', 'update-viewport', 'resize', 'rotate', 'open'].forEach(function (ev) {
    viewer.addHandler(ev, drawPoly);
  });
  window.addEventListener('resize', drawPoly);
  document.getElementById('undo').addEventListener('click', function () {
    if (closed) return;
    poly.pop(); drawPoly();
  });
  document.getElementById('close').addEventListener('click', closePoly);
  function closePoly() {
    if (poly.length < 3) return;
    closed = true;
    drawPoly(); applyInOut();
  }
  document.getElementById('clear').addEventListener('click', function () {
    poly = []; closed = false; drawPoly();
    document.getElementById('counts').textContent = '';
    document.getElementById('expstate').textContent = '';
  });
  document.getElementById('showtok').addEventListener('change', drawTokens);
  document.getElementById('showpoly').addEventListener('change', drawPoly);
  document.getElementById('export').addEventListener('click', function () {
    var blob = new Blob([JSON.stringify({ closed: closed, polygon: poly }, null, 1)],
                        { type: 'application/json' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'region_polygon.json';
    a.click();
    document.getElementById('expstate').textContent = 'exported: ' + poly.length +
      ' vertices - drop the file anywhere in scratch/map4456/ and say so';
  });
  document.addEventListener('keydown', function (ev) {
    if (ev.key === 'Enter' && !closed) { closePoly(); }
  });
})();
</script>
</body>
</html>
"""
HTML = HTML.replace("@@TOKS@@", json.dumps(toks, ensure_ascii=False))
HTML = HTML.replace("@@TILES@@", TILES)
out = ROOT + r"\scratch\map4456\draw_region.html"
with open(out, "w", encoding="utf-8") as f:
    f.write(HTML)
print("wrote", out, round(len(HTML) / 1e3, 1), "KB")
