# The region label sheet: every black label cluster inside the editor's
# polygon as a card - the crop, and three fields: the lead number (1..12),
# the D-S pair (as "D-S"), or "not a label". The user's readings feed the
# parcel groups and the sum test. Output: scratch/map4456/label_sheet.html
import base64
import io
import json

import numpy as np
import pyvips
import PIL.Image

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld"
FULL = (r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)"
        r"\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456\4456_full.jpg")
OUT = ROOT + r"\scratch\map4456\label_sheet.html"

LAB = json.load(open(ROOT + r"\scratch\map4456\region_labels.json", encoding="utf-8"))
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

im = pyvips.Image.new_from_file(FULL, access="random")
W, H = im.width, im.height

# every black label cluster (the parcel labels are black); keep the cluster's
# own box, crop generously (the stack's two lines plus the area line)
items = []
for k, lab in enumerate(LAB):
    if lab["ink"] != "black":
        continue
    cx, cy = lab["x"] + lab["w"] / 2, lab["y"] + lab["h"] / 2
    if not pip(cx, cy):
        continue
    items.append({"id": "l-%d-%d" % (int(lab["x"]), int(lab["y"])),
                  "x": lab["x"], "y": lab["y"], "w": lab["w"], "h": lab["h"],
                  "lines": lab["lines"][:4], "conf": lab.get("conf")})
print("black label clusters in region:", len(items))

R = 150
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

payload = json.dumps(items, ensure_ascii=False)
print("payload MB:", round(len(payload) / 1e6, 1))

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Pełzucki 1896 — the parcel labels' sheet (working page)</title>
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
         width: max-content; }
.frame img { display: block; user-select: none; -webkit-user-drag: none; }
.obox { position: absolute; border: 2px solid rgba(42,38,34,.9); box-sizing: border-box;
        pointer-events: none; }
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
.done { color: #3d7a3d; } .skip { color: #b33; }
.unsure { color: #8a6d3b; }
.mach { color: var(--ink-faint); font-size: .72rem; }
</style>
</head>
<body>
<header>
  <h1>Pełzucki 1896 — the parcel labels' sheet <span style="font-family:Verdana,sans-serif;font-size:.68rem;letter-spacing:.05em;text-transform:uppercase;color:#fff;background:#8a6d3b;padding:.1rem .5rem;border-radius:.8rem;vertical-align:middle">working page</span></h1>
  <p>Each card is a black ink cluster inside your region — the machine's guess of where
     a parcel label stands (its own reading underneath, faint). Read the label and fill
     what you see: the <b>lead</b> number (the small n above the area), the <b>area</b>
     as written (D-S, e.g. 1-662; leave blank if the label shows only one of them), and
     say what the mark is. <kbd>Enter</kbd> saves and moves on; <b>Unsure</b>
     (<kbd>Ctrl</kbd>+<kbd>Enter</kbd>) keeps what you typed, empty or not, and flags
     the card (amber in the log); empty fields mean "not shown on this label". Export
     any time; partial work is kept in the browser.</p>
  <p class="progress"><span id="cnt"></span><span class="bar"><span id="fill"></span></span>
     <button class="btn" id="export">Export JSON</button></p>
</header>
<div class="card">
  <div class="framewrap">
    <div class="frame"><img id="img" alt="crop"><div class="obox" id="obox"></div></div>
    <div class="hint">The box marks the machine's cluster. Use <b>Hide box</b> (H) to see
      the crop bare.</div>
  </div>
  <div class="fields">
    <label>lead <input id="f-lead" autocomplete="off"> <span class="note">the small number (1..12)</span></label>
    <label>area <input id="f-area" autocomplete="off" placeholder="D-S e.g. 1-662">
      <span class="note">as written; or just S if no desiatinas</span></label>
    <div>
      <button class="btn primary" id="ok">Save (Enter)</button>
      <button class="btn" id="unsure">Unsure (?)</button>
      <button class="btn warn" id="nonum">Not a label</button>
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
  var KEY = 'p1896-labels-v1';
  var ans = {};
  try { ans = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) {}
  var i = 0;
  function firstOpen() {
    for (var k = 0; k < ITEMS.length; k++) if (!ans[ITEMS[k].id]) return k;
    return 0;
  }
  i = firstOpen();
  var img = document.getElementById('img'), obox = document.getElementById('obox'),
      lead = document.getElementById('f-lead'), area = document.getElementById('f-area'),
      cnt = document.getElementById('cnt'), fill = document.getElementById('fill'),
      verb = document.getElementById('verb');
  function show() {
    var it = ITEMS[i];
    img.src = it.img;
    obox.style.left = (it.x - it.ox) + 'px'; obox.style.top = (it.y - it.oy) + 'px';
    obox.style.width = it.w + 'px'; obox.style.height = it.h + 'px';
    var a = ans[it.id];
    lead.value = a && a.lead != null ? a.lead : '';
    area.value = a && a.area ? a.area : '';
    var d = 0;
    ITEMS.forEach(function (t) { if (ans[t.id]) d++; });
    cnt.textContent = d + ' of ' + ITEMS.length + ' answered';
    fill.style.width = (100 * d / ITEMS.length) + '%';
    var lines = [];
    ITEMS.forEach(function (t) {
      var aa = ans[t.id];
      if (aa && (aa.lead != null || aa.area || aa.v === 'notalabel')) {
        var cls = aa.v === 'notalabel' ? 'skip' :
                  aa.v === 'unsure' ? 'unsure' : 'done';
        var tag = aa.v === 'unsure' ? ' (unsure)' : '';
        lines.push('<div class="' + cls + '">' + (aa.v === 'notalabel'
          ? 'not a label'
          : (aa.lead != null ? 'n=' + aa.lead + ' ' : '') +
            (aa.area ? aa.area : '') + tag) +
          ' at (' + t.x + ',' + t.y + ')</div>');
      }
    });
    verb.innerHTML = lines.slice(-14).join('');
    verb.scrollTop = verb.scrollHeight;
    lead.focus();
  }
  function save(v) {
    var it = ITEMS[i];
    if (v === 'notalabel') {
      ans[it.id] = { v: v, lead: null, area: '' };
    } else if (v === 'unsure') {
      // keep whatever is typed; works empty too - a label seen but not pinned
      var lv = lead.value.trim();
      var av = area.value.trim().replace(' ', '');
      ans[it.id] = { v: 'unsure',
                     lead: lv ? parseInt(lv, 10) : null,
                     area: av };
    } else {
      var lv = lead.value.trim();
      var av = area.value.trim().replace(' ', '');
      if (!lv && !av) return;
      ans[it.id] = { v: 'read',
                     lead: lv ? parseInt(lv, 10) : null,
                     area: av };
    }
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
  var boxHidden = false;
  function setBoxHidden(h) {
    boxHidden = h;
    obox.style.display = h ? 'none' : 'block';
    document.getElementById('hidebox').textContent = h ? 'Show box (H)' : 'Hide box (H)';
  }
  document.getElementById('hidebox').addEventListener('click', function () {
    setBoxHidden(!boxHidden); lead.focus();
  });
  [lead, area].forEach(function (el) {
    el.addEventListener('keydown', function (ev) {
      if (ev.key === 'Enter' && ev.ctrlKey) { ev.preventDefault(); save('unsure'); }
      else if (ev.key === 'Enter' && !ev.ctrlKey) { ev.preventDefault(); save('read'); }
      else if (ev.key === 'Escape') { ev.preventDefault(); nextOpen(1); }
      else if ((ev.key === 'h' || ev.key === 'H') && el === lead && !lead.value) {
        ev.preventDefault(); setBoxHidden(!boxHidden);
      }
    });
  });
  document.getElementById('ok').addEventListener('click', function () { save('read'); });
  document.getElementById('unsure').addEventListener('click', function () { save('unsure'); });
  document.getElementById('nonum').addEventListener('click', function () { save('notalabel'); });
  document.getElementById('skip').addEventListener('click', function () { nextOpen(1); });
  document.getElementById('prev').addEventListener('click', function () { i = (i - 1 + ITEMS.length) % ITEMS.length; show(); });
  document.getElementById('next').addEventListener('click', function () { nextOpen(1); });
  document.getElementById('export').addEventListener('click', function () {
    var out = ITEMS.map(function (it) {
      var a = ans[it.id];
      return { id: it.id, x: it.x, y: it.y, w: it.w, h: it.h,
               verdict: a ? a.v : 'open',
               lead: a ? a.lead : null, area: a ? a.area : null,
               machine_lines: it.lines };
    });
    var blob = new Blob([JSON.stringify(out, null, 1)], { type: 'application/json' });
    var aEl = document.createElement('a');
    aEl.href = URL.createObjectURL(blob);
    aEl.download = 'labels_read.json';
    aEl.click();
  });
  show();
})();
</script>
</body>
</html>
"""
HTML = HTML.replace("@@DATA@@", payload)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(HTML)
print("wrote", OUT, round(len(HTML) / 1e6, 1), "MB")
