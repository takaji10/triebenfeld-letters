# The free annotation page: the mosaic in the site's viewer, a click drops a
# mark, the editor types the number read there and its ink (red/black),
# the annotations persist in localStorage and export as JSON (mosaic pixels).
# Output: scratch/map4456/annotate_numbers.html
import json

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld"
TILES = "https://takaji10.github.io/triebenfeld-maps/pelzucki1896/info.json"
SITES = json.load(open(ROOT + r"\scratch\map4456\farm_locations.json", encoding="utf-8"))
LINKED = json.load(open(ROOT + r"\scratch\map4456\oleders_linked.json", encoding="utf-8"))
holder = {e["no"]: e["name_1868"] for e in LINKED}

# the OCR'd black farm sites as faint reference marks (toggleable)
ref = [{"x": s["x"], "y": s["y"], "n": s["n"], "h": holder.get(s["n"], "?"),
        "st": s["status"]} for s in SITES]

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Pełzucki 1896 — annotate the numbers (working page)</title>
<style>
:root { --rule: #d8d2c4; --ink: #2a2620; --ink-soft: #6b6459; --accent: #8a3324; }
body { margin: 0; background: #faf8f3; color: var(--ink); font-family: Georgia, serif; }
header { max-width: 120rem; margin: 0 auto; padding: .9rem 2rem .2rem; }
header h1 { font-size: 1.2rem; margin: 0 0 .2rem; }
header p { font-size: .85rem; color: var(--ink-soft); margin: .15rem 0; }
.cols { display: grid; grid-template-columns: minmax(20rem, 26rem) minmax(0, 1fr);
        gap: 1.4rem; align-items: start; max-width: 120rem; margin: 0 auto; padding: 0 2rem 2rem; }
.side { max-height: 92vh; overflow-y: auto; padding-right: .4rem;
        font-family: Verdana, sans-serif; font-size: .82rem; }
.box { border: 1px solid var(--rule); border-radius: .4rem; padding: .7rem .9rem; margin: 0 0 .8rem; }
.box h2 { font-size: .9rem; margin: 0 0 .4rem; }
.inks { display: flex; gap: 1rem; margin: .3rem 0 .6rem; }
.inks label { cursor: pointer; }
.swatch { display: inline-block; width: .8em; height: .8em; border-radius: 2px; vertical-align: -1px; }
.sw-red { background: #b33; } .sw-black { background: #333; }
#val { font-size: 1.1rem; padding: .35rem .6rem; width: 8rem; border: 1px solid var(--rule); }
.btn { font-family: Verdana, sans-serif; font-size: .78rem; padding: .3rem .8rem;
       border: 1px solid var(--rule); background: #fff; cursor: pointer; border-radius: 3px; }
.btn.primary { background: var(--accent); color: #fff; border-color: var(--accent); }
.alist { list-style: none; margin: .4rem 0 0; padding: 0; max-height: 24rem; overflow-y: auto; }
.alist li { display: flex; gap: .5rem; align-items: baseline; padding: .22rem 0;
            border-bottom: 1px solid var(--rule); }
.alist .v { font-weight: 700; min-width: 3.4rem; }
.alist .dot { width: .7em; height: .7em; border-radius: 2px; display: inline-block; }
.alist .xy { color: var(--ink-soft); font-size: .72rem; }
.alist button { margin-left: auto; }
.togl { margin: .3rem 0; }
.viewer { width: 100%; height: min(88vh, 62rem); background: #f4f1ea;
          border: 1px solid var(--rule); touch-action: none; }
.stage { position: sticky; top: .8rem; }
.note { font-size: .74rem; color: var(--ink-soft); margin-top: .4rem; }
/* the marks */
.num-mark { box-sizing: border-box; min-width: 22px; height: 22px; padding: 0 4px;
            display: flex; align-items: center; justify-content: center;
            font-family: Verdana, sans-serif; font-weight: 700; font-size: 13px;
            border-radius: 3px; cursor: pointer; user-select: none; }
.num-red { background: rgba(179,51,51,.92); color: #fff; border: 2px solid #7d2323; }
.num-black { background: rgba(40,38,34,.92); color: #fff; border: 2px solid #191713; }
.num-mark.sel { outline: 3px solid #2a6db3; }
.ref-mark { box-sizing: border-box; width: 14px; height: 14px; border-radius: 50%;
            border: 2px dashed rgba(60,90,140,.55); background: rgba(255,255,255,.25);
            pointer-events: none; }
@media (max-width: 64rem) { .cols { grid-template-columns: 1fr; } .stage { position: static; order: -1; } }
</style>
</head>
<body>
<header>
  <h1>Pełzucki 1896 — annotate the numbers <span style="font-family:Verdana,sans-serif;font-size:.68rem;letter-spacing:.05em;text-transform:uppercase;color:#fff;background:#8a6d3b;padding:.1rem .5rem;border-radius:.8rem;vertical-align:middle">working page</span></h1>
  <p>Zoom in, click on a number you can read on the mosaic, type its value in the side panel
     (choose the ink colour first), press <b>Enter</b>. Click a saved mark to select it
     (then re-type to correct, or Delete). Everything persists in the browser; <b>Export</b>
     downloads the JSON that joins the OCR data. The dashed circles are the farm sites the
     first pass found (toggle below) — the farms with no circle are where a reading helps most.</p>
</header>
<div class="cols">
  <div class="side">
    <div class="box">
      <h2>New annotation</h2>
      <div class="inks">
        <label><input type="radio" name="ink" value="black" checked> <span class="swatch sw-black"></span> black (farm number)</label>
        <label><input type="radio" name="ink" value="red"> <span class="swatch sw-red"></span> red (area)</label>
      </div>
      <input id="val" placeholder="the number as written" autocomplete="off" spellcheck="false">
      <span class="note">then Enter; the map stays where it is</span>
    </div>
    <div class="box">
      <h2>Your annotations <span id="acount"></span></h2>
      <ul class="alist" id="alist"></ul>
      <p style="margin:.5rem 0 0">
        <button class="btn primary" id="export">Export JSON</button>
        <button class="btn" id="undo">Delete selected</button>
      </p>
    </div>
    <div class="box">
      <h2>Reference</h2>
      <label class="togl"><input type="checkbox" id="showref"> show the first pass's farm sites
        (<span id="refcount"></span> dashed circles; green-filled = proved)</label>
      <p class="note">Farms still with no site on the map:
        <span id="missing"></span></p>
    </div>
  </div>
  <div class="stage">
    <div id="viewer" class="viewer"></div>
    <p class="note">positions are recorded in the mosaic's pixels (21715 &times; 14206)</p>
  </div>
</div>
<script id="ref-data" type="application/json">@@REF@@</script>
<script src="/site/assets/maps/openseadragon.min.js"></script>
<script>
(function () {
  var REF = JSON.parse(document.getElementById('ref-data').textContent);
  var KEY = 'p1896-annot-v1';
  var ann = [];
  try { ann = JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (e) {}
  var sel = -1;
  var viewer = OpenSeadragon({
    id: 'viewer', prefixUrl: '', showNavigationControl: false,
    tileSources: '@@TILES@@', crossOriginPolicy: 'Anonymous',
    maxZoomPixelRatio: 6, visibilityRatio: 0.5, animationTime: 0.5,
    gestureSettingsMouse: { clickToZoom: false, dblClickToZoom: true }
  });
  var world = null;
  viewer.addHandler('open', function () { world = viewer.world.getItemAt(0); drawRef(); drawAll(); focus(); });
  viewer.addHandler('canvas-click', function (e) {
    if (!e.quick || !world) return;
    var p = world.viewerElementToImageCoordinates(e.position);
    pending = { x: Math.round(p.x), y: Math.round(p.y) };
    document.getElementById('val').focus();
  });
  var pending = null;
  var overlays = [];
  function clear(list) { list.forEach(function (o) { viewer.removeOverlay(o.el); }); }
  function drawRef() {
    if (!document.getElementById('showref').checked) return;
    REF.forEach(function (r) {
      var d = document.createElement('div');
      d.className = 'ref-mark';
      if (r.st !== 'candidate') d.style.borderStyle = 'solid';
      if (r.st !== 'candidate') d.style.borderColor = 'rgba(61,122,61,.8)';
      var p = viewer.viewport.imageToViewportCoordinates(new OpenSeadragon.Point(r.x, r.y));
      viewer.addOverlay({ element: d, location: p,
        placement: OpenSeadragon.Placement.CENTER,
        rotationMode: OpenSeadragon.OverlayRotationMode.NO_ROTATION });
      refOv.push(d);
    });
  }
  var refOv = [];
  document.getElementById('showref').addEventListener('change', function () {
    clear(refOv); refOv = []; drawRef();
  });
  function drawAll() {
    clear(overlays); overlays = [];
    ann.forEach(function (a, k) {
      var d = document.createElement('div');
      d.className = 'num-mark num-' + a.ink + (k === sel ? ' sel' : '');
      d.textContent = a.text;
      d.title = 'at (' + a.x + ', ' + a.y + ') - click to select';
      d.addEventListener('click', function () { sel = k; drawAll(); syncList(); });
      var p = viewer.viewport.imageToViewportCoordinates(new OpenSeadragon.Point(a.x, a.y));
      viewer.addOverlay({ element: d, location: p,
        placement: OpenSeadragon.Placement.CENTER,
        rotationMode: OpenSeadragon.OverlayRotationMode.NO_ROTATION });
      overlays.push(d);
    });
  }
  function persist() {
    try { localStorage.setItem(KEY, JSON.stringify(ann)); } catch (e) {}
  }
  function syncList() {
    var ul = document.getElementById('alist');
    ul.innerHTML = '';
    ann.forEach(function (a, k) {
      var li = document.createElement('li');
      li.innerHTML = '<span class="dot ' + (a.ink === 'red' ? 'sw-red' : 'sw-black') +
        '"></span><span class="v">' + a.text + '</span>' +
        '<span class="xy">(' + a.x + ', ' + a.y + ')' +
        (a.ll ? ' ' + a.ll : '') + '</span>';
      var b = document.createElement('button');
      b.className = 'btn'; b.textContent = '&times;';
      b.textContent = '\\u00d7';
      b.addEventListener('click', function () { ann.splice(k, 1); if (sel === k) sel = -1; persist(); drawAll(); syncList(); });
      li.appendChild(b);
      ul.appendChild(li);
    });
    document.getElementById('acount').textContent = '(' + ann.length + ')';
  }
  function focus() { document.getElementById('val').focus(); }
  document.getElementById('val').addEventListener('keydown', function (ev) {
    if (ev.key !== 'Enter') return;
    ev.preventDefault();
    var v = this.value.trim();
    if (!v) return;
    if (sel >= 0 && !pending) {
      ann[sel].text = v;
      ann[sel].ink = inkOf();
      sel = -1;
    } else {
      if (!pending) return;
      var a = { text: v, ink: inkOf(), x: pending.x, y: pending.y, ts: Date.now() };
      ann.push(a);
      pending = null;
    }
    this.value = '';
    persist(); drawAll(); syncList();
  });
  function inkOf() {
    return document.querySelector('input[name="ink"]:checked').value;
  }
  document.getElementById('undo').addEventListener('click', function () {
    if (sel >= 0) { ann.splice(sel, 1); sel = -1; persist(); drawAll(); syncList(); }
  });
  document.getElementById('export').addEventListener('click', function () {
    var blob = new Blob([JSON.stringify(ann, null, 1)], { type: 'application/json' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'numbers_annot.json';
    a.click();
  });
  // the farms with no site
  var have = {};
  REF.forEach(function (r) { have[r.n] = true; });
  var missing = [];
  for (var n = 1; n <= 97; n++) if (!have[n]) missing.push(n);
  document.getElementById('missing').textContent = missing.join(', ');
  document.getElementById('refcount').textContent = REF.length;
  syncList();
})();
</script>
</body>
</html>
"""
HTML = HTML.replace("@@REF@@", json.dumps(ref, ensure_ascii=False))
HTML = HTML.replace("@@TILES@@", TILES)
out = ROOT + r"\scratch\map4456\annotate_numbers.html"
with open(out, "w", encoding="utf-8") as f:
    f.write(HTML)
print("wrote", out, round(len(HTML) / 1e3, 1), "KB;", len(ref), "reference sites")
