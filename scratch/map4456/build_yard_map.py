# The homestead-yard map, v2 — the editor's flow:
#   1. click a farm number (a red mark on the map) -> it becomes the active
#      farm (the panel shows the row's holder and total, NOT the buildings
#      figure — the yard read stays blind)
#   2. draw mode turns on; drag a box around the black "n. / n" figure
#   3. type the area as written (uncertainty in [..?]); Enter links it
# The farm comes only from the clicked mark; the pair is saved with the
# mark's position (the evidence of which red n was clicked).
# Output: scratch/map4456/yard_map.html
import json

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld"
TILES = "https://takaji10.github.io/triebenfeld-maps/pelzucki1896/info.json"
D = json.load(open(ROOT + r"\scratch\map4456\reds_all.json", encoding="utf-8"))
REF = json.load(open(ROOT + r"\scratch\map4456\reference_numbers.json", encoding="utf-8"))

def canon(t):
    t = t.strip().replace("[", "").replace("?]", "").replace("?", "")
    return t.strip()

refs = []
for a in D["answered"]:
    c = canon(a["text"])
    x, y = a["x"], a["y"]
    if a.get("fixed"):
        x = a["fixed"]["x"]; y = a["fixed"]["y"]
    if c.isdigit():
        refs.append({"n": int(c), "x": x, "y": y})
for n in D["added"]:
    c = canon(n["text"])
    if c.isdigit():
        refs.append({"n": int(c), "x": n["x"] + (n.get("w", 0)) // 2,
                     "y": n["y"] + (n.get("h", 0)) // 2})
# the row facts the panel shows (holder, total — not the buildings figure)
rows = {}
for k, r in REF["statement"].items():
    if k.isdigit():
        rows[int(k)] = {"name": r["name"],
                        "td": r["total"]["des"], "ts": r["total"]["saz"]}
print("red reference marks:", len(refs))

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
#area, #note { font-size: 1rem; padding: .3rem .5rem; border: 1px solid var(--rule); }
#area { width: 9rem; } #note { width: 11rem; }
.activefarm { font-size: .95rem; margin: .3rem 0; }
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
.ref-label { box-sizing: border-box; min-width: 17px; height: 17px; padding: 0 3px;
             display: flex; align-items: center; justify-content: center;
             font-family: Verdana, sans-serif; font-size: 10px; font-weight: 700;
             color: rgba(140,40,40,.65); border: 1px dashed rgba(140,40,40,.45);
             border-radius: 3px; background: rgba(255,255,255,.4);
             pointer-events: auto; z-index: 5; cursor: pointer; }
.ref-label.sel { outline: 3px solid #1d4f7c; outline-offset: 1px;
                 color: #fff; background: rgba(42,109,179,.92);
                 border-style: solid; }
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
  <h1>Pełzucki 1896 — the homestead yards <span style="font-family:Verdana,sans-serif;font-size:.72rem;color:#8a6d3b">(v2 · click farm, draw, Enter)</span>
    <span style="font-family:Verdana,sans-serif;font-size:.68rem;letter-spacing:.05em;text-transform:uppercase;color:#fff;background:#8a6d3b;padding:.1rem .5rem;border-radius:.8rem;vertical-align:middle">working page</span></h1>
  <p>The flow: <b>click a farm number</b> on the map (a red dashed tag — it turns
     solid blue; draw mode comes on by itself), <b>drag a box</b> around the black
     <b>n. / n</b> figure, type the <b>area as written</b> — uncertainty in
     [..?] — and press <kbd>Enter</kbd>: the figure is linked to that farm, and the
     farm deselects for the next one. <b>D</b> toggles pan/draw from anywhere — it
     never types a letter (the area field takes digits, dots and dashes only).
     <kbd>Esc</kbd> clears the farm (or a pending rectangle, in the fields). The
     panel shows the farm's holder and total, but <b>not</b> its buildings figure —
     the yard read stays blind, so the check means something. Click a yard label to
     edit it; Export when done.</p>
</header>
<div class="cols">
  <div class="side">
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
      <p class="hint" id="modehint">click a farm number, then drag the box, then
        Enter</p>
    </div>
    <div class="box">
      <h2>Your yards <span id="ncount"></span></h2>
      <ul class="alist" id="alist"></ul>
      <p style="margin:.5rem 0 0">
        <button class="btn primary" id="export">Export JSON</button>
        <button class="btn" id="del">Delete selected</button>
      </p>
    </div>
    <div class="box">
      <h2>Layers</h2>
      <label><input type="checkbox" id="show-refs" checked>
        the red catalogue's farm numbers</label><br>
      <label><input type="checkbox" id="show-yards" checked> your yards</label>
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
<script src="/site/assets/maps/openseadragon.min.js"></script>
<script>
(function () {
  var REFS = JSON.parse(document.getElementById('ref-data').textContent);
  var ROWS = JSON.parse(document.getElementById('row-data').textContent);
  var K_NEW = 'p1896-yards-v1';
  var yards = [];
  try { yards = JSON.parse(localStorage.getItem(K_NEW) || '[]'); } catch (e) {}
  var sel = -1, drawMode = false, activeFarm = null;

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
    if (document.getElementById('show-refs').checked) {
      REFS.forEach(function (r) {
        var d = document.createElement('div');
        d.className = 'ref-label' +
          (activeFarm && activeFarm.n === r.n &&
           activeFarm.x === r.x && activeFarm.y === r.y ? ' sel' : '');
        d.textContent = r.n;
        d.title = 'farm ' + r.n + ' - click to make it the active farm';
        var p = viewer.viewport.imageToViewportCoordinates(
          new OpenSeadragon.Point(r.x, r.y));
        viewer.addOverlay({ element: d, location: p,
          placement: OpenSeadragon.Placement.CENTER,
          rotationMode: OpenSeadragon.OverlayRotationMode.NO_ROTATION });
        ovs.push({ el: d, rec: { ref: r } });
      });
    }
    if (document.getElementById('show-yards').checked) {
      yards.forEach(function (a, k) {
        var d = document.createElement('div');
        d.className = 'yard-label' + (k === sel ? ' sel' : '');
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
  }

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
         : ' (not a statement row)');
  }
  function setActive(r) {
    activeFarm = { n: r.n, x: r.x, y: r.y };
    if (!drawMode) toggleMode();     // the flow: farm picked, now draw
    setHint('farm ' + r.n + ' selected &mdash; drag the box around its 1. figure, type the area, Enter');
    drawAll();
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
    if (!dragging) return;
    dragging = false;
    s1 = elPos(ev);
    if (Math.abs(s1.x - s0.x) < 9 && Math.abs(s1.y - s0.y) < 9) {
      pendRect = null; hideRect();
      return;
    }
    var a = imgPos(s0), b = imgPos(s1);
    pendRect = { x0: Math.min(a.x, b.x), y0: Math.min(a.y, b.y),
                 x1: Math.max(a.x, b.x), y1: Math.max(a.y, b.y) };
    showRectImg(pendRect.x0, pendRect.y0, pendRect.x1, pendRect.y1);
    document.getElementById('area').focus();
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
        } else {
          area.value = ''; note.value = '';
          pendRect = null; hideRect();
          setHint('click a farm number, then drag the box, then Enter');
        }
        drawAll();
        return;
      }
      // a farm-number tag
      o = hitOverlay(ev.clientX, ev.clientY, function (r) { return r.ref !== undefined; });
      if (o) {
        ev.preventDefault(); ev.stopPropagation();
        setActive(o.rec.ref);
        return;
      }
      // nothing: a miss clears nothing (the drag or pan handles it)
    } catch (err) {
      document.getElementById('modehint').textContent =
        'ERROR in the press handler: ' + err.message;
    }
  }
  document.addEventListener('mousedown', onPress, true);
  document.addEventListener('pointerdown', onPress, true);

  // ---- saving -------------------------------------------------------------
  function persist() {
    try { localStorage.setItem(K_NEW, JSON.stringify(yards)); } catch (e) {}
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
        } else {
          area.value = ''; note.value = ''; pendRect = null; hideRect();
        }
        drawAll();
      });
      var b = document.createElement('button');
      b.className = 'btn'; b.textContent = '\\u00d7';
      b.addEventListener('click', function (ev) {
        ev.stopPropagation();
        yards.splice(k, 1); if (sel === k) sel = -1; persist(); drawAll();
      });
      li.appendChild(b);
      ul.appendChild(li);
    });
    document.getElementById('ncount').textContent = '(' + yards.length + ')';
  }
  var area = document.getElementById('area'),
      note = document.getElementById('note');
  function save() {
    var a = area.value.trim();
    if (!activeFarm) { setHint('click a farm number first'); return; }
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
    }
    pendRect = null; hideRect();
    area.value = ''; note.value = '';
    persist(); drawAll();
    // the flow: one farm, one yard — saved, the farm deselects and the
    // mode returns to pan, ready for the next farm's click
    activeFarm = null;
    toggleModeTo(false);
    setHint('saved &mdash; click the next farm number to mark its yard');
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
      yards.splice(sel, 1); sel = -1; persist(); drawAll();
    }
    if (ev.key === 'Escape') {
      if (ev.target === area || ev.target === note) {
        pendRect = null; hideRect();
        ev.target.blur();
        return;
      }
      if (sel >= 0) { sel = -1; area.value = ''; note.value = ''; }
      activeFarm = null; pendRect = null; hideRect();
      toggleModeTo(false);
      setHint('click a farm number, then drag the box, then Enter');
      drawAll();
    }
    if (ev.key === 'd' || ev.key === 'D') {
      ev.preventDefault(); toggleMode();
    }
  });
  ['show-refs', 'show-yards'].forEach(function (id) {
    document.getElementById(id).addEventListener('change', drawAll);
  });
  document.getElementById('del').addEventListener('click', function () {
    if (sel >= 0) { yards.splice(sel, 1); sel = -1; persist(); drawAll(); }
  });
  document.getElementById('export').addEventListener('click', function () {
    var blob = new Blob([JSON.stringify({ yards: yards }, null, 1)],
                        { type: 'application/json' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'yards_read.json';
    a.click();
  });
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
HTML = HTML.replace("@@TILES@@", TILES)
out = ROOT + r"\scratch\map4456\yard_map.html"
with open(out, "w", encoding="utf-8") as f:
    f.write(HTML)
print("wrote", out, round(len(HTML) / 1e3, 1), "KB")
