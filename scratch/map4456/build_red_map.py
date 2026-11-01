# The red-numbers map, v2: the editor's answers as labels (hideable), and a
# draw-mode flow - toggle Draw (button or D), then click-drag a rectangle
# around a red number, type its value, Enter: the label lands at the
# rectangle's centre and the rectangle itself is saved (for calibration).
# Pan mode keeps the ordinary click-to-mark. Exports reds_all.json.
# Output: scratch/map4456/red_map.html
import json

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld"
TILES = "https://takaji10.github.io/triebenfeld-maps/pelzucki1896/info.json"
LAB3 = json.load(open(ROOT + r"\scratch\map4456\region_labels3.json", encoding="utf-8"))
REG = json.load(open(ROOT + r"\scratch\map4456\region_polygon.json", encoding="utf-8"))
POLY = REG["polygon"]

def pip(x, y):
    ins = False
    n = len(POLY)
    for i in range(n):
        x1, y1 = POLY[i]; x2, y2 = POLY[(i + 1) % n]
        if ((y1 > y) != (y2 > y)) and (x < (x2 - x1) * (y - y1) / (y2 - y1) + x1):
            ins = not ins
    return ins

items = []
for lab in LAB3:
    if lab["ink"] != "red":
        continue
    cx, cy = lab["x"] + lab["w"] / 2, lab["y"] + lab["h"] / 2
    if not pip(cx, cy):
        continue
    items.append({"id": "r-%d-%d" % (int(lab["x"]), int(lab["y"])),
                  "x": int(cx), "y": int(cy)})
print("red cards carried:", len(items))

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Pełzucki 1896 — the red numbers on the map (working page)</title>
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
#val { font-size: 1.1rem; padding: .35rem .6rem; width: 8rem;
       border: 1px solid var(--rule); }
#note { font-size: .9rem; padding: .3rem .5rem; width: 12rem;
        border: 1px solid var(--rule); }
.btn { font-family: Verdana, sans-serif; font-size: .78rem; padding: .3rem .8rem;
       border: 1px solid var(--rule); background: #fff; cursor: pointer;
       border-radius: 3px; margin: 0 .3rem .3rem 0; }
.btn.primary { background: var(--accent); color: #fff; border-color: var(--accent); }
.btn.on { background: #2a6db3; color: #fff; border-color: #2a6db3; }
.alist { list-style: none; margin: .4rem 0 0; padding: 0; max-height: 22rem;
         overflow-y: auto; }
.alist li { display: flex; gap: .5rem; align-items: baseline; padding: .2rem 0;
            border-bottom: 1px solid var(--rule); }
.alist .v { font-weight: 700; min-width: 2.6rem; color: #1d4f7c; }
.alist .vr { color: #b33; }
.alist li.arow { cursor: pointer; }
.alist li.arow:hover { background: rgba(179,51,51,.07); }
.alist li.selrow { background: rgba(42,109,179,.14); }
.alist .xy { color: var(--ink-soft); font-size: .72rem; }
.alist button { margin-left: auto; font-size: .7rem; }
.hint { color: var(--ink-soft); font-size: .76rem; }
.viewer { width: 100%; height: min(88vh, 62rem); background: #f4f1ea;
          border: 1px solid var(--rule); touch-action: none; position: relative; }
.draw-capture { position: absolute; inset: 0; z-index: 8; cursor: crosshair;
                display: none; touch-action: none; }
.stage { position: sticky; top: .8rem; }
.num-label { box-sizing: border-box; display: flex; align-items: center;
              justify-content: center; min-width: 24px; height: 24px; padding: 0 5px;
              font-family: Verdana, sans-serif; font-weight: 700; font-size: 14px;
              border-radius: 4px; background: rgba(179,51,51,.9); color: #fff;
              border: 2px solid #7d2323; cursor: default; white-space: nowrap;
              pointer-events: auto; z-index: 9; }
.num-label.unsure { background: rgba(138,109,59,.92); border-color: #6d5430; }
.num-label.new { background: rgba(42,109,179,.92); border-color: #1d4f7c; }
.num-label.sel { outline: 3px solid #2a6db3; outline-offset: 1px; }
.rubber { position: absolute; border: 2px dashed #2a6db3;
          background: rgba(42,109,179,.12); pointer-events: none; z-index: 7; }
@media (max-width: 64rem) { .cols { grid-template-columns: 1fr; }
  .stage { position: static; order: -1; } }
</style>
</head>
<body>
<header>
  <h1>Pełzucki 1896 — the red numbers on the map <span style="font-family:Verdana,sans-serif;font-size:.72rem;color:#8a6d3b">(v12 · own-box outlines)</span>
    <span style="font-family:Verdana,sans-serif;font-size:.68rem;letter-spacing:.05em;text-transform:uppercase;color:#fff;background:#8a6d3b;padding:.1rem .5rem;border-radius:.8rem;vertical-align:middle">working page</span></h1>
  <p>Your red-sheet answers show as labels at their positions (unsure amber,
     rejections hidden). <b>Select a label</b> (map click, or a row in the answered
     list): its own box shows if it has one, the fields prefill — type the number and
     <kbd>Enter</kbd> commits (moving the label only if you dragged a new rectangle
     first). To give an answered label a position or fix one: <b>Draw mode</b>
     (<kbd>D</kbd>), <b>drag a rectangle</b> around the number, <kbd>Enter</kbd>.
     A plain click no longer spawns a phantom box. New labels are blue; Delete
     removes the selected one; Export when the reds are all caught.</p>
</header>
<div class="cols">
  <div class="side">
    <div class="box">
      <h2>Add a red number</h2>
      <p>
        <button class="btn" id="modebtn">Draw mode (D)</button>
      </p>
      <p style="margin:.2rem 0 .4rem"><input id="val" placeholder="the red number"
         autocomplete="off" spellcheck="false"></p>
      <p style="margin:.2rem 0 .4rem"><input id="note" placeholder="note (optional)"></p>
      <p class="hint" id="modehint">Draw mode (D) draws a box by dragging; a click
        selects a label; Enter commits.</p>
    </div>
    <div class="box">
      <h2>Your answered values <span id="acount2"></span></h2>
      <ul class="alist" id="alist-a"></ul>
      <p class="hint">click a row to select its label on the map (then drag a new
        rectangle and Enter to fix its position) — this works even if the map
        clicks misbehave</p>
    </div>
    <div class="box">
      <h2>Your new labels <span id="ncount"></span></h2>
      <ul class="alist" id="alist"></ul>
      <p style="margin:.5rem 0 0">
        <button class="btn primary" id="export">Export JSON</button>
        <button class="btn" id="del">Delete selected</button>
      </p>
    </div>
    <div class="box">
      <h2>Layers</h2>
      <label><input type="checkbox" id="show-answered" checked>
        your answered values (<span id="a-count"></span>)</label><br>
      <label><input type="checkbox" id="show-unsure" checked>
        the unsure ones in amber</label><br>
      <label><input type="checkbox" id="show-new" checked> your new labels</label>
      <p class="hint" id="stats"></p>
    </div>
  </div>
  <div class="stage">
    <div id="viewer" class="viewer"></div>
    <p class="hint" style="font-family:Verdana,sans-serif;margin-top:.4rem">
      positions in the mosaic's pixels (21715 &times; 14206)</p>
  </div>
</div>
<script id="card-data" type="application/json">@@CARDS@@</script>
<script src="/site/assets/maps/openseadragon.min.js"></script>
<script>
(function () {
  var CARDS = JSON.parse(document.getElementById('card-data').textContent);
  var K_ANS = 'p1896-red-v1';
  var K_NEW = 'p1896-red2-v1';
  var ans = {}, news = [];
  try { ans = JSON.parse(localStorage.getItem(K_ANS) || '{}'); } catch (e) {}
  try { news = JSON.parse(localStorage.getItem(K_NEW) || '[]'); } catch (e) {}
  var sel = -1, selCard = null;   // selCard: the answered label being fixed

  var answered = CARDS.filter(function (c) {
    var a = ans[c.id];
    return a && (a.v === 'read' || a.v === 'unsure') &&
           (a.f1 != null || (a.f2 && a.f2.trim()));
  }).map(function (c) {
    var a = ans[c.id];
    // a fix from this page (nx, ny) outranks the card's original centre
    var x = (a && a.nx != null) ? a.nx : c.x;
    var y = (a && a.ny != null) ? a.ny : c.y;
    return { id: c.id, x: x, y: y, text: (a.f1 != null ? String(a.f1) : '?'),
             note: a.f2 || '', unsure: a.v === 'unsure' };
  });
  var nRejected = CARDS.filter(function (c) {
    return ans[c.id] && ans[c.id].v === 'notanumber'; }).length;
  var nUnread = CARDS.filter(function (c) { return !ans[c.id]; }).length;
  document.getElementById('a-count').textContent = answered.length;
  document.getElementById('stats').textContent =
    'v8 · the red sheet held ' + CARDS.length + ' cards: ' + answered.length +
    ' read (' + answered.filter(function (a) { return a.unsure; }).length +
    ' unsure), ' + nRejected + ' rejected, ' + nUnread + ' still unanswered';

  var viewer = OpenSeadragon({
    id: 'viewer', prefixUrl: '', showNavigationControl: false,
    tileSources: '@@TILES@@', crossOriginPolicy: 'Anonymous',
    maxZoomPixelRatio: 6, visibilityRatio: 0.5, animationTime: 0.5,
    gestureSettingsMouse: { clickToZoom: false, dblClickToZoom: true }
  });
  var world = null;
  viewer.addHandler('open', function () {
    world = viewer.world.getItemAt(0); drawAll(); applyMode();
  });

  // ---- the labels ---------------------------------------------------------
  var ovs = [];
  function drawAll() {
    ovs.forEach(function (o) { viewer.removeOverlay(o.el); });
    ovs = [];
    var showA = document.getElementById('show-answered').checked;
    var showU = document.getElementById('show-unsure').checked;
    var showN = document.getElementById('show-new').checked;
    if (showA) {
      answered.forEach(function (a) {
        if (a.unsure && !showU) return;
        addLabel(a.x, a.y, a.text + (a.note ? ' ' + a.note : ''),
                 a.unsure ? 'unsure' : '', undefined,
                 { card: a });
      });
    }
    if (showN) {
      news.forEach(function (a, k) {
        addLabel(a.x + (a.w || 0) / 2, a.y + (a.h || 0) / 2,
                 a.text + (a.note ? ' ' + a.note : ''),
                 'new' + (k === sel ? ' sel' : ''), k, { idx: k });
      });
    }
    syncList();
  }
  function addLabel(x, y, text, cls, idx, rec) {
    var isCard = rec && rec.card;
    var selected = isCard ? (selCard && selCard.id === rec.card.id)
                          : (idx !== undefined && sel === idx);
    var d = document.createElement('div');
    d.className = 'num-label ' + cls + (selected ? ' sel' : '');
    d.textContent = text;
    d.title = isCard
      ? 'click to select; then drag a new rectangle and Enter to fix its position'
      : 'click to select, Delete to remove';
    var p = viewer.viewport.imageToViewportCoordinates(new OpenSeadragon.Point(x, y));
    viewer.addOverlay({ element: d, location: p,
      placement: OpenSeadragon.Placement.CENTER,
      rotationMode: OpenSeadragon.OverlayRotationMode.NO_ROTATION });
    ovs.push({ el: d, rec: rec });
  }

  // ---- selection by hit-test (both kinds of label) ------------------------
  var HINT_DEFAULT = function () {
    return drawMode
      ? 'draw mode: drag a rectangle around a red number (wheel still zooms), then type and Enter'
      : 'pan mode: click drops a small box; Draw mode (button or D) lets you drag the box around the number';
  };
  function setDefaultHint() {
    document.getElementById('modehint').textContent = HINT_DEFAULT();
  }
  function toggleCard(card, fly) {
    if (selCard && selCard.id === card.id) {
      selCard = null; val.value = ''; note.value = '';
      setDefaultHint();
    } else {
      selCard = card; sel = -1;
      val.value = card.text; note.value = card.note || '';
      // the outline is the label's own box: the one you drew when you fixed
      // it (a.box). An answered label with no fix yet has no box — nothing
      // is drawn until you drag one, or Enter commits the text alone.
      var a = ans[card.id];
      if (a && a.box) {
        pendRect = { x0: a.box[0], y0: a.box[1],
                     x1: a.box[0] + a.box[2], y1: a.box[1] + a.box[3] };
        showRectImg(pendRect.x0, pendRect.y0, pendRect.x1, pendRect.y1);
      } else {
        pendRect = null; hideRect();
      }
      document.getElementById('modehint').textContent = (a && a.box)
        ? 'fixing an answered label (' + card.id + '): its box shows — drag a new rectangle to move it, or Enter to commit'
        : 'selected ' + card.id + ': type the number and Enter to commit; drag a rectangle to give it a position';
      if (fly) {
        // bring the label into view: the map fits a square around it
        var pad = 320;
        viewer.viewport.fitBounds(viewer.viewport.imageToViewportRectangle(
          card.x - pad, card.y - pad, 2 * pad, 2 * pad));
      }
    }
    drawAll();
  }
  function toggleNews(k) {
    sel = (sel === k ? -1 : k);
    if (sel >= 0) {
      selCard = null;
      var a = news[sel];
      val.value = a.text; note.value = a.note || '';
      if (a.w) {
        pendRect = { x0: a.x, y0: a.y, x1: a.x + a.w, y1: a.y + a.h };
        showRectImg(pendRect.x0, pendRect.y0, pendRect.x1, pendRect.y1);
      } else {
        pendRect = null; hideRect();
      }
      document.getElementById('modehint').textContent =
        'editing a label: drag a new rectangle (or Esc to leave it), then Enter';
    } else {
      val.value = ''; note.value = '';
      setDefaultHint();
    }
    drawAll();
  }
  function labelAt(clientX, clientY) {
    // Hit-test against the label elements' OWN rects — the positions the
    // viewer's overlay machinery has set. No coordinate transforms: the
    // previous attempts converted image positions through the viewport and
    // missed however the frames disagreed. A rect is the ground truth.
    var best = null, bestD = 1e9;
    var PAD = 12;
    ovs.forEach(function (o) {
      if (!o.rec) return;
      var r = o.el.getBoundingClientRect();
      if (r.width === 0) return;                 // hidden by a layer toggle
      var cx = r.left + r.width / 2, cy = r.top + r.height / 2;
      var d = Math.hypot(clientX - cx, clientY - cy);
      // inside the box itself, or within PAD of its edge
      var inside = clientX >= r.left - PAD && clientX <= r.right + PAD &&
                   clientY >= r.top - PAD && clientY <= r.bottom + PAD;
      if (inside || d < Math.max(r.width, r.height) / 2 + PAD) {
        if (d < bestD) { bestD = d; best = o.rec; }
      }
    });
    return best;
  }
  function selectByElement(el) {
    // the click landed on the label element itself: find its record
    for (var i = 0; i < ovs.length; i++) {
      if (ovs[i].el === el) {
        var rec = ovs[i].rec;
        if (!rec) return false;
        if (rec.card) toggleCard(rec.card); else toggleNews(rec.idx);
        return true;
      }
    }
    return false;
  }
  function selectHit(hit) {
    if (hit.card) toggleCard(hit.card); else toggleNews(hit.idx);
  }
  // the press handler runs on BOTH mousedown and pointerdown (capture
  // phase): OpenSeadragon's tracker listens to pointer events, so stopping
  // mousedown alone left its click synthesis alive in Firefox - the dashed
  // box that kept appearing through a selected label. A hit stops both.
  function onPress(ev) {
    try {
      if (!world || ev.button !== 0) return;
      if (!viewerEl.contains(ev.target)) return;
      if (ev.target.closest && ev.target.closest('button, input, a, label')) return;
      if (window.__redmap) window.__redmap.handled = false;
      var lab = ev.target.closest && ev.target.closest('.num-label');
      if (lab && selectByElement(lab)) {
        if (window.__redmap) window.__redmap.handled = true;
        ev.preventDefault();
        ev.stopPropagation();
        return;
      }
      var hit = labelAt(ev.clientX, ev.clientY);
      if (hit) {
        if (window.__redmap) window.__redmap.handled = true;
        ev.preventDefault();
        ev.stopPropagation();
        selectHit(hit);
        document.getElementById('modehint').textContent =
          'v11 · selected ' + (hit.card ? hit.card.id : 'new #' + hit.idx) +
          ' — drag a new rectangle, then Enter (Esc to leave it)';
      }
    } catch (err) {
      document.getElementById('modehint').textContent =
        'v11 · ERROR in the press handler: ' + err.message;
    }
  }
  document.addEventListener('mousedown', onPress, true);
  document.addEventListener('pointerdown', onPress, true);

  // ---- draw mode: a capture layer above the canvas, the drag ours -------
  // OpenSeadragon's pan is left untouched: in draw mode a transparent layer
  // takes the pointer events, so no gesture-settings fiddling (which nudged
  // the viewport a few pixels on every toggle) and no swallowed presses.
  var viewerEl = document.getElementById('viewer');
  var drawMode = false;
  var cap = document.createElement('div');
  cap.className = 'draw-capture';
  viewerEl.appendChild(cap);
  var modebtn = document.getElementById('modebtn');
  function applyMode() {
    cap.style.display = drawMode ? 'block' : 'none';
    modebtn.classList.toggle('on', drawMode);
    modebtn.textContent = drawMode ? 'Pan mode (D)' : 'Draw mode (D)';
    document.getElementById('modehint').textContent = drawMode
      ? 'draw mode: drag a rectangle around a red number (wheel still zooms), then type and Enter'
      : 'pan mode: click drops a small box; Draw mode (button or D) lets you drag the box around the number';
  }
  function toggleMode() { drawMode = !drawMode; applyMode(); }
  modebtn.addEventListener('click', toggleMode);

  var rubber = document.createElement('div');
  rubber.className = 'rubber';
  rubber.style.display = 'none';
  viewerEl.appendChild(rubber);
  var pendRect = null;      // {x0,y0,x1,y1} image px
  var dragging = false, s0 = null, s1 = null;   // element px
  function elPos(ev) {
    var r = viewerEl.getBoundingClientRect();
    return { x: ev.clientX - r.left, y: ev.clientY - r.top };
  }
  function imgPos(el) {
    return world.viewerElementToImageCoordinates(
      new OpenSeadragon.Point(el.x, el.y));
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
    if (!dragging) return;
    dragging = false;
    s1 = elPos(ev);
    if (Math.abs(s1.x - s0.x) < 9 && Math.abs(s1.y - s0.y) < 9) {
      // a click, not a drag: no box — the drag is the way to draw one
      pendRect = null; hideRect();
      return;
    }
    var a = imgPos(s0), b = imgPos(s1);
    pendRect = { x0: Math.min(a.x, b.x), y0: Math.min(a.y, b.y),
                 x1: Math.max(a.x, b.x), y1: Math.max(a.y, b.y) };
    showRectImg(pendRect.x0, pendRect.y0, pendRect.x1, pendRect.y1);
    document.getElementById('val').focus();
  });
  cap.addEventListener('wheel', function (ev) {
    ev.preventDefault();
    var p = elPos(ev);                       // the cursor's element position
    var ip = imgPos(p);                      // -> image px
    var sc = ev.deltaY < 0 ? 1.25 : 0.8;
    // zoom about the cursor: the image point under it must stay under it.
    // shift the viewport centre so the anchor holds (screen-points math).
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
      viewer.viewport.deltaPointsFromPixels(
        new OpenSeadragon.Point(-dx, -dy)));
    viewer.viewport.applyConstraints();
  });
  // pan mode: a plain click does nothing — selection goes by the press
  // handler above, and a box only ever comes from a drag in draw mode
  viewer.addHandler('canvas-click', function (e) {
    if (drawMode || !world || !e.quick) return;
    // no-op by design (v12): the phantom default box is gone
  });

  // ---- saving -------------------------------------------------------------
  function persist() {
    try { localStorage.setItem(K_NEW, JSON.stringify(news)); } catch (e) {}
  }
  function syncList() {
    var ul = document.getElementById('alist');
    ul.innerHTML = '';
    news.forEach(function (a, k) {
      var li = document.createElement('li');
      li.innerHTML = '<span class="v">' + a.text + '</span>' +
        '<span class="xy">(' + a.x + ', ' + a.y + ')' +
        (a.w ? ' ' + a.w + '\\u00d7' + a.h : '') +
        (a.note ? ' - ' + a.note : '') + '</span>';
      var b = document.createElement('button');
      b.className = 'btn'; b.textContent = '\\u00d7';
      b.addEventListener('click', function () {
        news.splice(k, 1); if (sel === k) sel = -1; persist(); drawAll();
      });
      li.appendChild(b);
      ul.appendChild(li);
    });
    document.getElementById('ncount').textContent = '(' + news.length + ')';
    // the answered values: a row each, click to select on the map
    var ua = document.getElementById('alist-a');
    ua.innerHTML = '';
    answered.forEach(function (a) {
      var li = document.createElement('li');
      li.className = 'arow' + (selCard && selCard.id === a.id ? ' selrow' : '');
      li.innerHTML = '<span class="v vr">' + a.text +
        (a.unsure ? '?' : '') + '</span>' +
        '<span class="xy">' + a.id.replace('r-', '') +
        (a.note ? ' - ' + a.note : '') + '</span>';
      li.addEventListener('click', function () { toggleCard(a, true); });
      ua.appendChild(li);
    });
    document.getElementById('acount2').textContent = '(' + answered.length + ')';
  }
  var val = document.getElementById('val'), note = document.getElementById('note');
  function save() {
    var v = val.value.trim();
    if (!pendRect || !world) return;
    var r = pendRect;
    var rec = {
      text: v, note: note.value.trim(),
      x: Math.round(r.x0), y: Math.round(r.y0),
      w: Math.round(r.x1 - r.x0), h: Math.round(r.y1 - r.y0)
    };
    if (selCard) {
      // fixing an answered label: write back to the red sheet's storage
      var a = ans[selCard.id];
      if (a) {
        a.f1 = v ? v : a.f1;
        a.f2 = rec.note;
        if (pendRect) {
          a.box = [rec.x, rec.y, rec.w, rec.h];
          a.cx = selCard.x; a.cy = selCard.y;          // the old centre, for the record
          a.nx = Math.round(rec.x + rec.w / 2);        // the fixed centre
          a.ny = Math.round(rec.y + rec.h / 2);
          a.fix = 'moved';
          if (v) selCard.text = v;
          selCard.note = rec.note;
          selCard.x = a.nx; selCard.y = a.ny;
        }
      }      try { localStorage.setItem(K_ANS, JSON.stringify(ans)); } catch (e) {}
      selCard = null;
      val.value = ''; note.value = '';
      pendRect = null; hideRect();
      drawAll();
      return;
    }
    if (sel >= 0) {
      // editing: replace the selected label's geometry (and text if retyped)
      if (v) news[sel].text = v;
      news[sel].note = rec.note;
      if (pendRect) {
        news[sel].x = rec.x; news[sel].y = rec.y;
        news[sel].w = rec.w; news[sel].h = rec.h;
      }
      sel = -1;
    } else {
      if (!v || !pendRect) return;
      news.push(rec);
    }
    pendRect = null; hideRect();
    val.value = ''; note.value = '';
    persist(); drawAll();
  }
  val.addEventListener('keydown', function (ev) {
    if (ev.key !== 'Enter') return;
    ev.preventDefault(); save();
  });
  note.addEventListener('keydown', function (ev) {
    if (ev.key === 'Enter') { ev.preventDefault(); save(); }
  });
  document.addEventListener('keydown', function (ev) {
    var inField = ev.target === val || ev.target === note;
    if (ev.key === 'Delete' && sel >= 0) {
      news.splice(sel, 1); sel = -1; persist(); drawAll();
    }
    if (ev.key === 'Escape') {
      if (sel >= 0) { sel = -1; val.value = ''; note.value = ''; }
      if (selCard) {
        selCard = null; val.value = ''; note.value = '';
        document.getElementById('modehint').textContent = drawMode
          ? 'draw mode: drag a rectangle around a red number (wheel still zooms), then type and Enter'
          : 'pan mode: click drops a small box; Draw mode (button or D) lets you drag the box around the number';
      }
      pendRect = null; hideRect();
    }
    if ((ev.key === 'd' || ev.key === 'D') && !inField) {
      ev.preventDefault(); toggleMode();
    }
  });
  ['show-answered', 'show-unsure', 'show-new'].forEach(function (id) {
    document.getElementById(id).addEventListener('change', drawAll);
  });
  document.getElementById('del').addEventListener('click', function () {
    if (sel >= 0) { news.splice(sel, 1); sel = -1; persist(); drawAll(); }
  });
  document.getElementById('export').addEventListener('click', function () {
    var out = {
      answered: answered.map(function (a) {
        var fix = ans[a.id] && ans[a.id].fix ? {
          x: ans[a.id].nx, y: ans[a.id].ny,
          box: ans[a.id].box, was: [a.x, a.y] } : null;
        return { id: a.id, x: a.x, y: a.y, text: a.text, note: a.note,
                 unsure: a.unsure, fixed: fix };
      }),
      added: news,
      meta: { cards: CARDS.length, rejected: nRejected, unanswered: nUnread }
    };
    var blob = new Blob([JSON.stringify(out, null, 1)], { type: 'application/json' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'reds_all.json';
    a.click();
  });
  // the diagnostic handle: the independent block below reads this. If the
  // main script had died anywhere above, the handle stays absent and the
  // diagnostic says so - that alone narrows the Firefox mystery.
  window.__redmap = {
    alive: true,
    count: function () { return ovs.length; },
    nearest: function (cx, cy) {
      var best = null, bestD = 1e9;
      ovs.forEach(function (o) {
        if (!o.rec) return;
        var r = o.el.getBoundingClientRect();
        if (r.width === 0) return;
        var d = Math.hypot(cx - (r.left + r.width / 2),
                           cy - (r.top + r.height / 2));
        if (d < bestD) {
          bestD = d;
          best = { id: o.rec.card ? o.rec.card.id : 'new#' + o.rec.idx,
                   d: d,
                   rect: [Math.round(r.left), Math.round(r.top),
                          Math.round(r.width), Math.round(r.height)] };
        }
      });
      return best;
    },
    handled: false
  };
})();
</script>
<script>
// The independent diagnostic: a separate script block that the main
// script's errors cannot kill. On every press inside the viewer it reports
// what the browser says is under the cursor, whether the main script is
// alive, and the nearest label's own rect and distance - into the hint
// line and the console (F12).
(function () {
  function chain(el) {
    var out = [];
    while (el && out.length < 4) {
      var c = (typeof el.className === 'string' && el.className)
        ? '.' + el.className.split(' ')[0] : '';
      out.push(el.tagName.toLowerCase() + c);
      el = el.parentElement;
    }
    return out.join(' < ');
  }
  document.addEventListener('mousedown', function (ev) {
    var M = window.__redmap;
    var msg = 'v11 · pressed on ' + chain(ev.target);
    var el = document.elementFromPoint(ev.clientX, ev.clientY);
    msg += ' | under cursor: ' + (el ? chain(el) : 'nothing');
    if (M && M.alive) {
      var near = M.nearest(ev.clientX, ev.clientY);
      if (near) {
        msg += ' | nearest ' + near.id + ' d=' + Math.round(near.d) +
               'px rect=' + near.rect.join(',');
      } else {
        msg += ' | no labels rendered (' + M.count() + ' overlays)';
      }
      if (M.handled) msg += ' | HANDLED';
    } else {
      msg += ' | MAIN SCRIPT NOT ALIVE';
    }
    var h = document.getElementById('modehint');
    if (h) h.textContent = msg;
    if (window.console) console.log(msg);
  }, true);
  var h = document.getElementById('modehint');
  if (h && !/v11/.test(h.textContent)) {
    h.textContent = window.__redmap
      ? 'v11 loaded · diagnostics armed (F12 = console)'
      : 'v11 loaded · MAIN SCRIPT NOT ALIVE — tell Claude';
  }
})();
</script>
</body>
</html>
"""
HTML = HTML.replace("@@CARDS@@", json.dumps(items, ensure_ascii=False))
HTML = HTML.replace("@@TILES@@", TILES)
out = ROOT + r"\scratch\map4456\red_map.html"
with open(out, "w", encoding="utf-8") as f:
    f.write(HTML)
print("wrote", out, round(len(HTML) / 1e3, 1), "KB")
