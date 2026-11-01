# The reading sheets for the editor's region, built from one template:
#   label_sheet.html  - the black ink clusters (parcel labels: lead n, area D-S)
#   red_sheet.html    - the red ink clusters (the red system: upper/lower line)
# Both share the spot sheet's proven interaction: adjustable box (drag inside
# to move, an edge to move that edge, a corner for both; no grab marks, the
# cursor shows the mode), Hide box (H) from anywhere, verdicts
# read / unsure (Ctrl+Enter, empty allowed) / not-a-label / skip.
# Box adjustments are saved in mosaic pixels in the exports.
import base64
import io
import json

import numpy as np
import pyvips
import PIL.Image

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld"
FULL = (r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)"
        r"\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456\4456_full.jpg")

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

LAB3 = json.load(open(ROOT + r"\scratch\map4456\region_labels3.json", encoding="utf-8"))
im = pyvips.Image.new_from_file(FULL, access="random")
W, H = im.width, im.height

def build_items(ink):
    items = []
    for lab in LAB3:
        if lab["ink"] != ink:
            continue
        cx, cy = lab["x"] + lab["w"] / 2, lab["y"] + lab["h"] / 2
        if not pip(cx, cy):
            continue
        items.append({"id": "%s-%d-%d" % (ink[0], int(lab["x"]), int(lab["y"])),
                      "x": lab["x"], "y": lab["y"], "w": lab["w"], "h": lab["h"],
                      "lines": [l["text"] for l in lab["lines"]][:4]})
    return items

def crop_items(items, R=125):
    for k, it in enumerate(items):
        cx, cy = int(it["x"] + it["w"] / 2), int(it["y"] + it["h"] / 2)
        l = max(0, cx - R); tp = max(0, cy - R)
        r_ = min(W, cx + R); b_ = min(H, cy + R)
        a = np.frombuffer(im.crop(l, tp, r_ - l, b_ - tp).write_to_memory(),
                          np.uint8).reshape(b_ - tp, r_ - l, 3)
        buf = io.BytesIO()
        PIL.Image.fromarray(a).save(buf, "JPEG", quality=85)
        it["img"] = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
        it["ox"], it["oy"] = l, tp
        it["cw"], it["ch"] = r_ - l, b_ - tp
        if k % 80 == 0:
            print("cropped", k, flush=True)
    return items

BLACK_ITEMS = crop_items(build_items("black"))
RED_ITEMS = crop_items(build_items("red"))
print("black cards:", len(BLACK_ITEMS), " red cards:", len(RED_ITEMS))

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>@@TITLE@@</title>
<style>
:root { --rule: #d8d2c4; --ink: #2a2620; --ink-soft: #6b6459; --accent: #8a3324; }
body { margin: 0; background: #faf8f3; color: var(--ink); font-family: Georgia, serif; }
header { max-width: 62rem; margin: 0 auto; padding: 1rem 1.5rem .2rem; }
header h1 { font-size: 1.25rem; margin: 0 0 .3rem; }
header p { font-size: .88rem; color: var(--ink-soft); margin: .2rem 0; }
kbd { font-family: Verdana, sans-serif; font-size: .72rem; border: 1px solid var(--rule);
      border-radius: 3px; padding: 0 .35rem; background: #fff; }
.card { max-width: 62rem; margin: .8rem auto; padding: 0 1.5rem 2rem; }
.framewrap { display: flex; gap: 1.2rem; align-items: flex-start; }
.frame { position: relative; border: 1px solid var(--rule); background: #fff;
         width: max-content; touch-action: none; }
.frame img { display: block; user-select: none; -webkit-user-drag: none; }
.obox { position: absolute; border: 2px solid rgba(42,109,179,.95);
        box-sizing: border-box; }
.obox.adjusted { border-color: #2a6db3; box-shadow: 0 0 0 1px rgba(42,109,179,.4); }
.hint { font-family: Verdana, sans-serif; font-size: .74rem; color: var(--ink-soft);
        max-width: 14rem; }
.fields { font-family: Verdana, sans-serif; font-size: .8rem; margin: .6rem 0;
          display: flex; flex-direction: column; gap: .45rem; }
.fields label { display: flex; gap: .5rem; align-items: center; }
.fields input { font-size: 1rem; padding: .25rem .5rem; width: 7rem;
                border: 1px solid var(--rule); }
.fields .note { color: var(--ink-soft); font-size: .72rem; }
.btn { font-family: Verdana, sans-serif; font-size: .8rem; padding: .3rem .8rem;
       border: 1px solid var(--rule); background: #fff; cursor: pointer;
       border-radius: 3px; }
.btn.primary { background: var(--accent); color: #fff; border-color: var(--accent); }
.btn.warn { border-color: #b33; color: #b33; }
.progress { font-family: Verdana, sans-serif; font-size: .8rem; color: var(--ink-soft);
            display: flex; gap: 1.2rem; align-items: center; margin: .5rem 0; }
.bar { flex: 1; height: 8px; background: #e8e2d4; border-radius: 4px; overflow: hidden; }
.bar span { display: block; height: 100%; background: var(--accent); width: 0; }
.verdicts { font-family: Verdana, sans-serif; font-size: .74rem; color: var(--ink-soft);
            margin-top: .3rem; max-height: 6rem; overflow-y: auto; }
.done { color: #3d7a3d; } .skip { color: #b33; } .unsure { color: #8a6d3b; }
.mach { color: #a49c8c; font-size: .7rem; }
</style>
</head>
<body>
<header>
  <h1>@@HEAD@@ <span style="font-family:Verdana,sans-serif;font-size:.68rem;letter-spacing:.05em;text-transform:uppercase;color:#fff;background:#8a6d3b;padding:.1rem .5rem;border-radius:.8rem;vertical-align:middle">working page</span></h1>
  <p>@@INTRO@@</p>
  <p class="progress"><span id="cnt"></span><span class="bar"><span id="fill"></span></span>
     <button class="btn" id="export">Export JSON</button></p>
</header>
<div class="card">
  <div class="framewrap">
    <div class="frame"><img id="img" alt="crop"><div class="obox" id="obox"></div></div>
    <div class="hint">The blue box marks the machine's cluster - <b>drag inside it to
      move it, an edge to move that edge, a corner for both</b> (the cursor shows
      which). <b>Hide box</b> (<kbd>H</kbd>) shows the crop bare, from anywhere; the
      setting stays. A darker blue box means you adjusted it.</div>
  </div>
  <div class="fields">
    @@FIELDS@@
    <div>
      <button class="btn primary" id="ok">Save (Enter)</button>
      <button class="btn" id="unsure">Unsure (Ctrl+Enter)</button>
      <button class="btn warn" id="nonum">@@NOTA@@</button>
      <button class="btn" id="hidebox">Hide box (H)</button>
      <button class="btn" id="skip">Skip (Esc)</button>
    </div>
  </div>
  <div class="verdicts" id="verb"></div>
  <div class="progress">
    <button class="btn" id="prev">&#8592; Prev</button>
    <button class="btn" id="next">Next &#8594;</button>
  </div>
</div>
<script id="sheet-data" type="application/json">@@DATA@@</script>
<script>
(function () {
  var ITEMS = JSON.parse(document.getElementById('sheet-data').textContent);
  var KEY = '@@KEY@@';
  var ans = {};
  try { ans = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) {}
  var i = 0;
  function firstOpen() {
    for (var k = 0; k < ITEMS.length; k++) if (!ans[ITEMS[k].id]) return k;
    return 0;
  }
  i = firstOpen();
  var img = document.getElementById('img'), obox = document.getElementById('obox'),
      frame = document.getElementById('frame'),
      f1 = document.getElementById('f1'), f2 = document.getElementById('f2'),
      cnt = document.getElementById('cnt'), fill = document.getElementById('fill'),
      verb = document.getElementById('verb');
  var Z = 1.3;
  var B = { bx: 0, by: 0, bw: 10, bh: 10 };
  function defaultBox(it) { return { bx: it.x - it.ox, by: it.y - it.oy,
                                     bw: it.w, bh: it.h }; }
  function boxIsDefault(it) {
    return B.bx === it.x - it.ox && B.by === it.y - it.oy &&
           B.bw === it.w && B.bh === it.h;
  }
  function drawBox() {
    obox.style.left = B.bx * Z + 'px'; obox.style.top = B.by * Z + 'px';
    obox.style.width = B.bw * Z + 'px'; obox.style.height = B.bh * Z + 'px';
    obox.classList.toggle('adjusted', !boxIsDefault(ITEMS[i]));
  }
  function show() {
    var it = ITEMS[i];
    img.src = it.img;
    img.style.width = Math.round(it.cw * Z) + 'px';
    B = (ans[it.id] && ans[it.id].box_local)
      ? { bx: ans[it.id].box_local[0], by: ans[it.id].box_local[1],
          bw: ans[it.id].box_local[2], bh: ans[it.id].box_local[3] }
      : defaultBox(it);
    B.bw = Math.min(B.bw, it.cw); B.bh = Math.min(B.bh, it.ch);
    B.bx = Math.min(Math.max(0, B.bx), Math.max(0, it.cw - B.bw));
    B.by = Math.min(Math.max(0, B.by), Math.max(0, it.ch - B.bh));
    drawBox();
    var a = ans[it.id];
    f1.value = a && a.f1 != null ? a.f1 : '';
    f2.value = a && a.f2 ? a.f2 : '';
    var d = 0;
    ITEMS.forEach(function (t) { if (ans[t.id]) d++; });
    cnt.textContent = d + ' of ' + ITEMS.length + ' answered';
    fill.style.width = (100 * d / ITEMS.length) + '%';
    var lines = [];
    ITEMS.forEach(function (t) {
      var aa = ans[t.id];
      if (aa && (aa.v !== 'open')) {
        var cls = aa.v === 'notalabel' || aa.v === 'notanumber' ? 'skip' :
                  aa.v === 'unsure' ? 'unsure' : 'done';
        var txt = aa.v === 'notalabel' || aa.v === 'notanumber' ? aa.v :
                  ((aa.f1 != null && aa.f1 !== '' ? aa.f1 + ' / ' : '') +
                   (aa.f2 || '')) + (aa.v === 'unsure' ? ' (unsure)' : '');
        lines.push('<div class="' + cls + '">' + txt +
          ' at (' + t.x + ',' + t.y + ')' +
          (aa.adj ? ' &middot; box adjusted' : '') + '</div>');
      }
    });
    verb.innerHTML = lines.slice(-14).join('');
    verb.scrollTop = verb.scrollHeight;
    f1.focus(); f1.select();
  }
  function save(v) {
    var it = ITEMS[i];
    if (v === 'notalabel' || v === 'notanumber') {
      ans[it.id] = { v: v, f1: null, f2: '' };
    } else {
      var v1 = f1.value.trim();
      var v2 = f2.value.trim().replace(' ', '');
      ans[it.id] = { v: v, f1: v1 ? v1 : null, f2: v2 };
    }
    var a = ans[it.id];
    a.box = [it.ox + B.bx, it.oy + B.by, B.bw, B.bh];
    a.adj = !boxIsDefault(it);
    if (a.adj) a.box_local = [B.bx, B.by, B.bw, B.bh];
    try { localStorage.setItem(KEY, JSON.stringify(ans)); } catch (e) {}
    nextOpen(1);
  }
  function nextOpen(dir) {
    var j = i;
    for (var k = 0; k < ITEMS.length; k++) {
      j = (j + dir + ITEMS.length) % ITEMS.length;
      if (!ans[ITEMS[j].id]) break;
    }
    i = j; show();
  }
  // ---- the box: move / edge / corner by where the pointer lands ----------
  var drag = null;
  var EDGE = 11;
  function modeAt(lx, ly, r) {
    var w = lx <= r.x + EDGE, e = lx >= r.x + r.w - EDGE;
    var n = ly <= r.y + EDGE, s = ly >= r.y + r.h - EDGE;
    if (w && n) return 'nw'; if (e && n) return 'ne';
    if (w && s) return 'sw'; if (e && s) return 'se';
    if (w) return 'w'; if (e) return 'e'; if (n) return 'n'; if (s) return 's';
    return 'move';
  }
  var CURS = { move: 'move', n: 'ns-resize', s: 'ns-resize',
               e: 'ew-resize', w: 'ew-resize',
               nw: 'nwse-resize', se: 'nwse-resize',
               ne: 'nesw-resize', sw: 'nesw-resize' };
  function evPos(ev) {
    var r = img.getBoundingClientRect();
    return { x: ev.clientX - r.left, y: ev.clientY - r.top };
  }
  obox.addEventListener('pointermove', function (ev) {
    if (drag) return;
    var r = { x: B.bx * Z, y: B.by * Z, w: B.bw * Z, h: B.bh * Z };
    var p = evPos(ev);
    obox.style.cursor = CURS[modeAt(p.x, p.y, r)];
  });
  obox.addEventListener('pointerleave', function () {
    if (!drag) obox.style.cursor = '';
  });
  obox.addEventListener('pointerdown', function (ev) {
    var r = { x: B.bx * Z, y: B.by * Z, w: B.bw * Z, h: B.bh * Z };
    var p0 = evPos(ev);
    var mode = modeAt(p0.x, p0.y, r);
    drag = { mode: mode, p0: { x: p0.x / Z, y: p0.y / Z },
             B0: { bx: B.bx, by: B.by, bw: B.bw, bh: B.bh } };
    obox.setPointerCapture(ev.pointerId);
    ev.preventDefault();
  });
  obox.addEventListener('pointermove', function (ev) {
    if (!drag) return;
    var it = ITEMS[i];
    var p = evPos(ev);
    var dx = p.x / Z - drag.p0.x, dy = p.y / Z - drag.p0.y;
    var b = drag.B0, m = drag.mode;
    if (m === 'move') {
      B.bx = Math.min(Math.max(0, b.bx + dx), it.cw - B.bw);
      B.by = Math.min(Math.max(0, b.by + dy), it.ch - B.bh);
    } else {
      var x1 = b.bx + b.bw, y1 = b.by + b.bh, x0 = b.bx, y0 = b.by;
      if (m.indexOf('w') >= 0) x0 = Math.min(Math.max(0, b.bx + dx), x1 - 8);
      if (m.indexOf('n') >= 0) y0 = Math.min(Math.max(0, b.by + dy), y1 - 8);
      if (m.indexOf('e') >= 0) x1 = Math.max(Math.min(it.cw, b.bx + b.bw + dx), x0 + 8);
      if (m.indexOf('s') >= 0) y1 = Math.max(Math.min(it.ch, b.by + b.bh + dy), y0 + 8);
      B.bx = x0; B.by = y0; B.bw = x1 - x0; B.bh = y1 - y0;
    }
    drawBox();
  });
  obox.addEventListener('pointerup', function () { drag = null; f1.focus(); f1.select(); });
  // ---- hide box: from anywhere -------------------------------------------
  var boxHidden = false;
  function setBoxHidden(h) {
    boxHidden = h;
    obox.style.display = h ? 'none' : 'block';
    document.getElementById('hidebox').textContent = h ? 'Show box (H)' : 'Hide box (H)';
  }
  document.getElementById('hidebox').addEventListener('click', function () {
    setBoxHidden(!boxHidden); f1.focus();
  });
  document.addEventListener('keydown', function (ev) {
    var inField = ev.target === f1 || ev.target === f2;
    if ((ev.key === 'h' || ev.key === 'H') && (!inField || !ev.target.value)) {
      ev.preventDefault(); setBoxHidden(!boxHidden);
    }
  });
  [f1, f2].forEach(function (el) {
    el.addEventListener('keydown', function (ev) {
      if (ev.key === 'Enter' && ev.ctrlKey) { ev.preventDefault(); save('unsure'); }
      else if (ev.key === 'Enter') { ev.preventDefault(); save('read'); }
      else if (ev.key === 'Escape') { ev.preventDefault(); nextOpen(1); }
    });
  });
  document.getElementById('ok').addEventListener('click', function () { save('read'); });
  document.getElementById('unsure').addEventListener('click', function () { save('unsure'); });
  document.getElementById('nonum').addEventListener('click', function () { save('@@NOTAV@@'); });
  document.getElementById('skip').addEventListener('click', function () { nextOpen(1); });
  document.getElementById('prev').addEventListener('click', function () { i = (i - 1 + ITEMS.length) % ITEMS.length; show(); });
  document.getElementById('next').addEventListener('click', function () { nextOpen(1); });
  document.getElementById('export').addEventListener('click', function () {
    var out = ITEMS.map(function (it) {
      var a = ans[it.id];
      return { id: it.id, x: it.x, y: it.y, w: it.w, h: it.h,
               verdict: a ? a.v : 'open',
               f1: a ? a.f1 : null, f2: a ? a.f2 : null,
               box: a && a.box ? a.box : null,
               box_adjusted: a ? !!a.adj : false,
               machine_lines: it.lines };
    });
    var blob = new Blob([JSON.stringify(out, null, 1)], { type: 'application/json' });
    var aEl = document.createElement('a');
    aEl.href = URL.createObjectURL(blob);
    aEl.download = '@@EXPORT@@';
    aEl.click();
  });
  show();
})();
</script>
</body>
</html>
"""

def render(path, title, head, intro, fields_html, nota_label, nota_value,
           key, export_name, items):
    h = TEMPLATE
    h = h.replace("@@TITLE@@", title)
    h = h.replace("@@HEAD@@", head)
    h = h.replace("@@INTRO@@", intro)
    h = h.replace("@@FIELDS@@", fields_html)
    h = h.replace("@@NOTA@@", nota_label)
    h = h.replace("@@NOTAV@@", nota_value)
    h = h.replace("@@KEY@@", key)
    h = h.replace("@@EXPORT@@", export_name)
    h = h.replace("@@DATA@@", json.dumps(items, ensure_ascii=False))
    with open(path, "w", encoding="utf-8") as f:
        f.write(h)
    print("wrote", path, round(len(h) / 1e6, 1), "MB;", len(items), "cards")

FIELDS_BLACK = (
    '<label>lead <input id="f1" autocomplete="off"> '
    '<span class="note">the small number above the area (1..12)</span></label>\n'
    '    <label>area <input id="f2" autocomplete="off" placeholder="D-S e.g. 1-662">'
    '<span class="note">as written; or just S if no desiatinas</span></label>')
FIELDS_RED = (
    '<label>value <input id="f1" autocomplete="off"> '
    '<span class="note">the red number as written (they are single, low, no hyphen)</span></label>\n'
    '    <label>note <input id="f2" autocomplete="off"> '
    '<span class="note">optional: what it sits by (parcel corner, edge, stream, building...)</span></label>')

render(ROOT + r"\scratch\map4456\label_sheet.html",
       "Pełzucki 1896 — the parcel labels' sheet (working page)",
       "Pełzucki 1896 — the parcel labels' sheet",
       "Each card is a black ink cluster inside your region - the machine's guess of "
       "where a parcel label stands. Read the label: the <b>lead</b> number (the small "
       "n above the area) and the <b>area</b> as written (D-S, e.g. 1-662; or just S). "
       "Enter saves and moves on; <b>Unsure</b> (Ctrl+Enter) keeps what you typed, "
       "empty or not, and flags the card. Export any time.",
       FIELDS_BLACK, "Not a label", "notalabel", "p1896-labels-v1", "labels_read.json",
       BLACK_ITEMS)
render(ROOT + r"\scratch\map4456\red_sheet.html",
       "Pełzucki 1896 — the red numbers' sheet (working page)",
       "Pełzucki 1896 — the red numbers' sheet",
       "Each card is a <b>red</b> ink cluster inside your region. The red numbers are "
       "<b>single, low figures without a hyphen</b> (the editor's observation; the "
       "areas stand in black, so these are not area pairs) - read the <b>value</b> as "
       "written, and note what it sits beside if you can. Enter saves; <b>Unsure</b> "
       "(Ctrl+Enter) flags a doubtful card, empty or not. Export any time.",
       FIELDS_RED, "Not a number", "notanumber", "p1896-red-v1", "reds_read.json",
       RED_ITEMS)
