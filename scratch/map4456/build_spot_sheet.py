# The spot sheet of the OCR's doubtful numbers on Pelzucki 1896, v3: the
# overlay box is editable - drag inside to move it, drag a corner to resize
# it - so the editor can frame the figure as drawn (the OCR's own box is
# often too large or off). The adjusted box is saved with the verdict, in
# mosaic pixels, in the export. Same card set as v2 (localStorage key
# p1896-spot-v2 kept, so earlier answers carry over).
import base64
import io
import json

import numpy as np
import pyvips
import PIL.Image

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld"
FULL = (r"J:\Documents\Archive\Genealogy\References\Maps\Congress Poland (1815-1915)"
        r"\Łazińskie Holendry (Muzeum Narodowe Rolnictwa w Szreniawie)\AN-4456\4456_full.jpg")
OUT = ROOT + r"\scratch\map4456\spot_sheet.html"

BLACK = json.load(open(ROOT + r"\scratch\map4456\numbers_black.json", encoding="utf-8"))
RED = json.load(open(ROOT + r"\scratch\map4456\numbers_easy2.json", encoding="utf-8"))

def norm_parts(t):
    t = t.strip().strip(".,-/").strip()
    out = []
    for p in t.replace("/", " ").replace(",", " ").replace(".", " ").replace("-", " ").split():
        if p.isdigit():
            out.append(int(p))
    if t.isdigit() and int(t) not in out:
        out.append(int(t))
    return out

items = []
for t in BLACK:
    if not t.get("drawn") or t["conf"] < 0.45:
        continue
    ps = norm_parts(t["text"])
    if len(ps) != 1:
        continue
    v = ps[0]
    if 1 <= v <= 97:
        if t["conf"] < 0.9:
            items.append({"id": "b-%d-%d" % (t["x"], t["y"]), "grp": "farm number",
                          "my": t["text"], "conf": t["conf"], "x": t["x"], "y": t["y"],
                          "w": t["w"], "h": t["h"]})
    elif t["conf"] >= 0.6:
        items.append({"id": "b-%d-%d" % (t["x"], t["y"]), "grp": "dark figure",
                      "my": t["text"], "conf": t["conf"], "x": t["x"], "y": t["y"],
                      "w": t["w"], "h": t["h"]})
for t in RED:
    if not t.get("drawn") or t["conf"] < 0.3:
        continue
    ps = norm_parts(t["text"])
    if not ps or max(ps) < 100:
        continue
    core = t["text"]
    for ch in "/.,- ":
        core = core.replace(ch, "")
    if len(core) > 4:
        continue
    items.append({"id": "r-%d-%d" % (t["x"], t["y"]), "grp": "red area",
                  "my": t["text"], "conf": t["conf"], "x": t["x"], "y": t["y"],
                  "w": t["w"], "h": t["h"]})

# merge near-duplicates: same value, boxes within 70 px (one figure read twice)
kept = []
for it in sorted(items, key=lambda i: -i["conf"]):
    ps = norm_parts(it["my"])
    v = ps[0] if len(ps) == 1 else max(ps)
    dup = False
    for k in kept:
        ps2 = norm_parts(k["my"])
        v2 = ps2[0] if len(ps2) == 1 else max(ps2)
        if v2 != v:
            continue
        if abs(k["x"] - it["x"]) <= 70 and abs(k["y"] - it["y"]) <= 70:
            dup = True
            break
    if not dup:
        kept.append(it)
items = kept
items.sort(key=lambda i: (0 if i["grp"] == "farm number" else
                          1 if i["grp"] == "red area" else 2, i["conf"]))
print("items:", len(items),
      "farm numbers:", sum(1 for i in items if i["grp"] == "farm number"),
      "red areas:", sum(1 for i in items if i["grp"] == "red area"),
      "dark figures:", sum(1 for i in items if i["grp"] == "dark figure"))

im = pyvips.Image.new_from_file(FULL, access="random")
W, H = im.width, im.height
R = 125   # crop radius: a 250 px square at full resolution, shown enlarged
for k, it in enumerate(items):
    cx, cy = it["x"] + it["w"] // 2, it["y"] + it["h"] // 2
    l = max(0, cx - R); tp = max(0, cy - R)
    r_ = min(W, cx + R); b_ = min(H, cy + R)
    a = np.frombuffer(im.crop(l, tp, r_ - l, b_ - tp).write_to_memory(),
                      np.uint8).reshape(b_ - tp, r_ - l, 3)
    buf = io.BytesIO()
    PIL.Image.fromarray(a).save(buf, "JPEG", quality=82)
    it["img"] = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    it["bx"] = it["x"] - l          # the token's box, crop-local px
    it["by"] = it["y"] - tp
    it["bw"] = it["w"]
    it["bh"] = it["h"]
    it["ox"] = l                    # the crop's origin in the mosaic
    it["oy"] = tp
    it["cw"] = r_ - l
    it["ch"] = b_ - tp
    if k % 60 == 0:
        print("cropped", k, flush=True)

payload = json.dumps(items, ensure_ascii=False)
print("payload MB:", round(len(payload) / 1e6, 1))

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Pełzucki 1896 — the numbers' spot sheet (working page)</title>
<style>
:root { --rule: #d8d2c4; --ink: #2a2620; --ink-soft: #6b6459; --accent: #8a3324; }
body { margin: 0; background: #faf8f3; color: var(--ink); font-family: Georgia, serif; }
header { max-width: 60rem; margin: 0 auto; padding: 1rem 1.5rem .2rem; }
header h1 { font-size: 1.25rem; margin: 0 0 .3rem; }
header p { font-size: .88rem; color: var(--ink-soft); margin: .2rem 0; }
kbd { font-family: Verdana, sans-serif; font-size: .72rem; border: 1px solid var(--rule);
      border-radius: 3px; padding: 0 .35rem; background: #fff; }
.card { max-width: 60rem; margin: .8rem auto; padding: 0 1.5rem 2rem; }
.framewrap { display: flex; gap: 1.2rem; align-items: flex-start; }
.frame { position: relative; border: 1px solid var(--rule); background: #fff;
         width: max-content; touch-action: none; }
.frame img { display: block; user-select: none; -webkit-user-drag: none; }
.obox { position: absolute; border: 2px solid rgba(138,51,36,.9);
        box-sizing: border-box; }
.obox.adjusted { border-color: #2a6db3; }
.hint { font-family: Verdana, sans-serif; font-size: .74rem; color: var(--ink-soft);
        max-width: 13rem; }
.meta { font-family: Verdana, sans-serif; font-size: .78rem; color: var(--ink-soft); margin: .4rem 0; }
.answer { display: flex; gap: .6rem; align-items: center; margin: .6rem 0; flex-wrap: wrap; }
.answer input { font-family: Verdana, sans-serif; font-size: 1.05rem; padding: .3rem .5rem;
                width: 9rem; border: 1px solid var(--rule); }
.btn { font-family: Verdana, sans-serif; font-size: .8rem; padding: .3rem .8rem;
       border: 1px solid var(--rule); background: #fff; cursor: pointer; border-radius: 3px; }
.btn.primary { background: var(--accent); color: #fff; border-color: var(--accent); }
.btn.warn { border-color: #b33; color: #b33; }
.progress { font-family: Verdana, sans-serif; font-size: .8rem; color: var(--ink-soft);
            display: flex; gap: 1.2rem; align-items: center; margin: .5rem 0; }
.bar { flex: 1; height: 8px; background: #e8e2d4; border-radius: 4px; overflow: hidden; }
.bar span { display: block; height: 100%; background: var(--accent); width: 0; }
.grp { font-family: Verdana, sans-serif; font-size: .7rem; letter-spacing: .05em;
       text-transform: uppercase; color: #8a6d3b; }
.done { color: #3d7a3d; } .unread { color: #b33; } .nonum { color: #8a6d3b; }
.verdicts { font-family: Verdana, sans-serif; font-size: .74rem; color: var(--ink-soft);
            margin-top: .3rem; max-height: 5.5rem; overflow-y: auto; }
</style>
</head>
<body>
<header>
  <h1>Pełzucki 1896 — the numbers' spot sheet <span class="grp">working page</span></h1>
  <p>Each card is a place where the OCR read a number <b>in the drawn portion of the
     map</b>, with the machine's reading in the red box. <b>The box is yours to
     adjust</b>: drag inside it to move it, drag any edge to move that edge
  alone, a corner for both at once, so it
     frames exactly what is drawn (the machine's box is often too large or shifted —
     the adjusted box is saved with your answer and sharpens the site's position).
     Then correct or confirm the reading, <kbd>Enter</kbd>. <kbd>Ctrl</kbd>+<kbd>Enter</kbd>
     = cannot read; <kbd>Ctrl</kbd>+<kbd>N</kbd> = not a number; <kbd>Esc</kbd> skips.
     Answers persist in the browser; <b>Export</b> downloads the JSON at any point.</p>
  <p class="progress"><span id="cnt"></span><span class="bar"><span id="fill"></span></span>
     <button class="btn" id="export">Export JSON</button></p>
</header>
<div class="card">
  <div class="framewrap">
    <div class="frame" id="frame"><img id="img" alt="crop">
      <div class="obox" id="obox"></div>
    </div>
    <div class="hint">Drag inside the box to move it; drag any <b>edge</b> to move
      that edge alone, a <b>corner</b> for both at once — the cursor shows which.
      <b>Hide box</b> (<kbd>H</kbd>) shows the crop bare, no marks; the setting
      stays until you toggle it back. A blue box means you have adjusted it;
      <b>Reset box</b> puts it back where the machine had it.</div>
  </div>
  <div class="meta" id="meta"></div>
  <div class="answer">
    <input id="ans" autocomplete="off" spellcheck="false">
    <button class="btn primary" id="ok">Confirm (Enter)</button>
    <button class="btn" id="resbox">Reset box</button>
    <button class="btn" id="hidebox">Hide box (H)</button>
    <button class="btn warn" id="nonum">Not a number (Ctrl+N)</button>
    <button class="btn" id="cant">Cannot read (Ctrl+Enter)</button>
    <button class="btn" id="skip">Skip (Esc)</button>
  </div>
  <div class="verdicts" id="verb"></div>
  <div class="answer" style="margin-top:.8rem">
    <button class="btn" id="prev">&#8592; Previous</button>
    <button class="btn" id="next">Next &#8594;</button>
  </div>
</div>
<script id="sheet-data" type="application/json">@@DATA@@</script>
<script>
(function () {
  var ITEMS = JSON.parse(document.getElementById('sheet-data').textContent);
  var KEY = 'p1896-spot-v2';
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
      meta = document.getElementById('meta'), input = document.getElementById('ans'),
      cnt = document.getElementById('cnt'), fill = document.getElementById('fill'),
      verb = document.getElementById('verb');
  // the live box, crop-local px (native resolution)
  var B = { bx: 0, by: 0, bw: 10, bh: 10 };
  var Z = 1.3;   // the crop is shown enlarged by this factor
  function defaultBox(it) { return { bx: it.bx, by: it.by, bw: it.bw, bh: it.bh }; }
  function boxIsDefault(it) {
    return B.bx === it.bx && B.by === it.by && B.bw === it.bw && B.bh === it.bh;
  }
  function drawBox() {
    obox.style.left = B.bx * Z + 'px'; obox.style.top = B.by * Z + 'px';
    obox.style.width = B.bw * Z + 'px'; obox.style.height = B.bh * Z + 'px';
    obox.classList.toggle('adjusted', !boxIsDefault(ITEMS[i]));
  }
  function doneCount() {
    var d = 0, c = 0, u = 0, n = 0, adj = 0;
    ITEMS.forEach(function (it) {
      var a = ans[it.id];
      if (a) { d++;
        if (a.v === 'unreadable') u++;
        else if (a.v === 'notanumber') n++;
        else if (a.v === 'corrected') c++;
        if (a.adj) adj++; }
    });
    return { d: d, c: c, u: u, n: n, adj: adj };
  }
  function show() {
    var it = ITEMS[i];
    img.src = it.img;
    img.style.width = Math.round(it.cw * Z) + 'px';
    frame.style.width = 'max-content';
    B = (ans[it.id] && ans[it.id].box_local)
      ? { bx: ans[it.id].box_local[0], by: ans[it.id].box_local[1],
          bw: ans[it.id].box_local[2], bh: ans[it.id].box_local[3] }
      : defaultBox(it);
    // a token wider than the crop sticks out: clamp it into the frame
    B.bw = Math.min(B.bw, it.cw);
    B.bh = Math.min(B.bh, it.ch);
    B.bx = Math.min(Math.max(0, B.bx), Math.max(0, it.cw - B.bw));
    B.by = Math.min(Math.max(0, B.by), Math.max(0, it.ch - B.bh));
    drawBox();
    meta.innerHTML = 'card ' + (i + 1) + ' of ' + ITEMS.length +
      ' &middot; <span class="grp">' + it.grp + '</span> &middot; machine read ' +
      '<b>' + it.my + '</b> (conf ' + it.conf.toFixed(2) + ') &middot; at (' +
      it.x + ', ' + it.y + ')';
    var a = ans[it.id];
    input.value = a ? (a.v === 'unreadable' || a.v === 'notanumber' ? '' : a.read) : it.my;
    var d = doneCount();
    cnt.textContent = d.d + ' of ' + ITEMS.length + ' answered (' + d.c +
      ' corrected, ' + d.n + ' not a number, ' + d.u + ' unreadable, ' + d.adj +
      ' boxes adjusted)';
    fill.style.width = (100 * d.d / ITEMS.length) + '%';
    var lines = [];
    ITEMS.forEach(function (t) {
      var aa = ans[t.id];
      if (aa) {
        var cls = aa.v === 'unreadable' ? 'unread' :
                  aa.v === 'notanumber' ? 'nonum' : 'done';
        var txt = aa.v === 'unreadable' ? 'cannot read' :
                  aa.v === 'notanumber' ? 'not a number' : aa.read;
        lines.push('<div>' + t.grp + ' ' + t.my + ' at (' + t.x + ',' + t.y +
          ') &rarr; <span class="' + cls + '">' + txt +
          (aa.v === 'corrected' ? ' (corrected)' : '') +
          (aa.adj ? ' &middot; box adjusted' : '') + '</span></div>');
      }
    });
    verb.innerHTML = lines.slice(-12).join('');
    verb.scrollTop = verb.scrollHeight;
    input.focus(); input.select();
  }
  function save(v) {
    var it = ITEMS[i];
    if (v === 'unreadable' || v === 'notanumber') {
      ans[it.id] = { v: v, read: '' };
    } else {
      var read = input.value.trim();
      if (!read) return;
      ans[it.id] = { v: read === it.my ? 'confirmed' : 'corrected', read: read };
    }
    // the box as it stands, in mosaic px, and whether it was adjusted
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
  // ---- the box: drag inside to move, drag an edge or corner to resize ----
  // No grab marks: the mode follows where on the box the pointer goes down.
  var drag = null;
  var EDGE = 11;   // hit distance from an edge, display px
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
    // all drag math in native crop px
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
  obox.addEventListener('pointerup', function (ev) {
    drag = null;
    input.focus(); input.select();
  });
  document.getElementById('resbox').addEventListener('click', function () {
    B = defaultBox(ITEMS[i]); drawBox(); input.focus();
  });
  // hide the box to see the crop bare; H or the button toggles it back
  var boxHidden = false;
  function setBoxHidden(h) {
    boxHidden = h;
    obox.style.display = h ? 'none' : 'block';
    document.getElementById('hidebox').textContent = h ? 'Show box (H)' : 'Hide box (H)';
  }
  document.getElementById('hidebox').addEventListener('click', function () {
    setBoxHidden(!boxHidden); input.focus();
  });
  input.addEventListener('keydown', function (ev) {
    if (ev.key === 'h' || ev.key === 'H') { ev.preventDefault(); setBoxHidden(!boxHidden); }
    else if (ev.key === 'Enter' && ev.ctrlKey) { ev.preventDefault(); save('unreadable'); }
    else if (ev.key === 'n' && ev.ctrlKey) { ev.preventDefault(); save('notanumber'); }
    else if (ev.key === 'Enter') { ev.preventDefault(); save('read'); }
    else if (ev.key === 'Escape') { ev.preventDefault(); nextOpen(1); }
  });
  document.getElementById('ok').addEventListener('click', function () { save('read'); });
  document.getElementById('nonum').addEventListener('click', function () { save('notanumber'); });
  document.getElementById('cant').addEventListener('click', function () { save('unreadable'); });
  document.getElementById('skip').addEventListener('click', function () { nextOpen(1); });
  document.getElementById('prev').addEventListener('click', function () { i = (i - 1 + ITEMS.length) % ITEMS.length; show(); });
  document.getElementById('next').addEventListener('click', function () { nextOpen(1); });
  document.getElementById('export').addEventListener('click', function () {
    var out = ITEMS.map(function (it) {
      var a = ans[it.id];
      return { id: it.id, grp: it.grp, my: it.my, conf: it.conf,
               x: it.x, y: it.y, w: it.w, h: it.h,
               verdict: a ? a.v : 'open', read: a ? a.read : null,
               box: a && a.box ? a.box : null,
               box_adjusted: a ? !!a.adj : false };
    });
    var blob = new Blob([JSON.stringify(out, null, 1)], { type: 'application/json' });
    var aEl = document.createElement('a');
    aEl.href = URL.createObjectURL(blob);
    aEl.download = 'numbers_spot.json';
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
