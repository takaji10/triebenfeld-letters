# -*- coding: utf-8 -*-
"""
The page on which the editor places fold lines by hand.

One opening at a time, shown whole, as large as the window allows. The left
and right arrow keys page through the openings; the red line is dragged onto
the fold. This is the page review_folds.py has always written; it lives here
so that the court-book holdings (courtbook.fold_sheet) show the editor the
same page and not another one (the editor, 2026-10-07: "I used to be able to
see the whole page and use arrow keys to cycle through pages").

Two ways of using it:

    render(..., rotate=False)   review_folds.py: only the openings whose line
                                was moved are saved, as {file: fraction of the
                                width}, in folds.json. Unchanged from before.
    render(..., rotate=True)    courtbook.py: the sheet can also be turned
                                with the mouse, so that a fold photographed at
                                a slant stands upright under the line. Every
                                opening is saved, as {file: {"fold": x in
                                pixels of the scan, "angle": degrees}}.

Page edges (crop=True; the editor, 2026-10-15: "You need to give me the
ability to mark vertical lines for where to crop pages"). Two green lines
mark the outer edges of what is kept: the left edge of the left page and the
right edge of the right page, or the two sides of a scan that is one page.
What lies outside them is shaded and is cut away (courtbook.cut). A click
moves the nearest line to it; Tab chooses the line that the comma and full
stop keys move. They are saved with the fold, as "left" and "right" in
pixels of the scan.

Turning. The red line stays vertical, because the cut is vertical; it is the
sheet that turns under it, about its centre. The mouse wheel turns it a tenth
of a degree at a time (half a degree with shift); holding shift, or the right
button, and dragging turns it as a sheet of paper is turned under a finger.
The angle is positive counter-clockwise, the sense of PIL's rotate(), so the
number saved is the rotation that is applied (courtbook.cut).

What the editor has done is kept in the browser as they go (localStorage,
under `key`), so closing the page loses nothing. The page is plain HTML
opened from disk: no server, nothing uploaded.
"""
import json

PAGE = """<!doctype html>
<meta charset="utf-8">
<title>Fold review - %(title)s</title>
<style>
  :root { color-scheme: light dark; }
  body { margin: 0; font: 14px/1.45 system-ui, sans-serif; background: #1a1a1a; color: #eee; overflow-x: hidden; }
  header { position: sticky; top: 0; z-index: 5; display: flex; gap: .9rem;
           align-items: center; flex-wrap: wrap;
           padding: .5rem .8rem; background: #111; border-bottom: 1px solid #333; }
  .muted { color: #999; }
  .moved { color: #7ec87e; }
  button { font: inherit; padding: .3rem .7rem; background: #2a2a2a; color: #eee;
           border: 1px solid #444; border-radius: 4px; cursor: pointer; }
  button:hover { background: #333; }
  button.primary { background: #2d5a2d; border-color: #3d7a3d; }
  /* room round the sheet, so that a turned sheet does not run under the bars */
  #stage { position: relative; margin: 26px auto; width: fit-content; touch-action: none; user-select: none; }
  #img { display: block; max-width: calc(100vw - 60px); max-height: calc(100vh - 170px); transform-origin: 50%% 50%%; }
  #line { position: absolute; top: -40px; bottom: -40px; width: 2px; background: #ff2020; }
  #line::after { content: ''; position: absolute; left: -14px; right: -14px;
                 top: 0; bottom: 0; cursor: ew-resize; }
  #band { position: absolute; top: 0; bottom: 0; background: rgba(255, 32, 32, .13); pointer-events: none; }
  #orig { position: absolute; top: 0; bottom: 0; width: 1px; background: #4a90d9; opacity: .8; }
  .cut { position: absolute; top: -40px; bottom: -40px; width: 2px; background: #30d060; }
  .cut::after { content: ''; position: absolute; left: -14px; right: -14px;
                top: 0; bottom: 0; cursor: ew-resize; }
  .shade { position: absolute; top: 0; bottom: 0; background: rgba(0, 0, 0, .55); pointer-events: none; }
  .active { outline: 2px solid #fff; outline-offset: 1px; }
  #grid { position: absolute; inset: -40px 0; pointer-events: none; display: none;
          background: repeating-linear-gradient(90deg, rgba(80, 200, 255, .55) 0 1px, transparent 1px 5%%); }
  #note { position: relative; z-index: 4; padding: .25rem .8rem; background: #151515;
          border-bottom: 1px solid #333; min-height: 1.4em; }
  #out { width: 100%%; height: 9rem; font: 12px/1.4 ui-monospace, monospace;
         background: #111; color: #ddd; border: 1px solid #333; display: none; }
  kbd { background: #333; border-radius: 3px; padding: 0 .3em; }
  .turning #img { cursor: grabbing; }
</style>

<header>
  <button id="prev">&larr;</button>
  <b id="pos"></b>
  <button id="next">&rarr;</button>
  <span id="name" class="muted"></span>
  <span id="cutbox">cut <b id="frac"></b></span>
  <span id="anglebox">turned <b id="angle"></b>&deg;</span>
  <span id="edgebox">page edges <b id="edges"></b></span>
  <span id="was" class="muted"></span>
  <span id="chg" class="moved"></span>
  <span style="flex:1"></span>
  <button id="reset">Reset this</button>
  <button id="save" class="primary">Save %(save)s</button>
  <button id="copy">Copy</button>
  <span class="muted"><kbd>&larr;</kbd><kbd>&rarr;</kbd> page,
    drag or <kbd>,</kbd><kbd>.</kbd> move the line<span id="turnhelp">,
    <b>mouse wheel</b> or <kbd>shift</kbd>+drag (or right-drag) turn the sheet,
    <kbd>[</kbd><kbd>]</kbd> turn a little, <kbd>0</kbd> upright,
    <kbd>g</kbd> guide lines</span>; <kbd>shift</kbd> = bigger steps;
    blue line = current cut<span id="edgehelp">;
    <b>green lines</b> = the edges of what is kept: a click moves the nearest line,
    <kbd>Tab</kbd> chooses the line <kbd>,</kbd><kbd>.</kbd> move</span></span>
</header>
<div id="note" class="muted"></div>

<div id="stage">
  <img id="img" alt="" draggable="false">
  <div id="grid"></div>
  <div id="band"></div>
  <div id="orig"></div>
  <div id="shadeL" class="shade"></div>
  <div id="shadeR" class="shade"></div>
  <div id="lcut" class="cut"></div>
  <div id="rcut" class="cut"></div>
  <div id="line"></div>
</div>
<textarea id="out" spellcheck="false"></textarea>

<script>
const ITEMS = %(items)s;
const CFG = %(cfg)s;
let mine = {};                 // what you changed: {file: {fold: fraction, angle: degrees}}
try { mine = JSON.parse(localStorage.getItem(CFG.key) || '{}'); } catch (e) {}
let i = 0;

const $ = id => document.getElementById(id);
const img = $('img'), line = $('line'), orig = $('orig'), band = $('band'), stage = $('stage');
const cur = () => ITEMS[i];
const fold = it => (mine[it.file] && mine[it.file].fold !== undefined) ? mine[it.file].fold : it.fold;
const angle = it => (mine[it.file] && mine[it.file].angle !== undefined) ? mine[it.file].angle : (it.angle || 0);
// the page edges, as fractions of the width: what lies outside them is cut away
const edge0 = (it, k) => (it[k] === undefined || it[k] === null) ? (k === 'left' ? 0 : 1) : it[k];
const edge = (it, k) => (mine[it.file] && mine[it.file][k] !== undefined) ? mine[it.file][k] : edge0(it, k);
const lcut = $('lcut'), rcut = $('rcut');
let active = 'fold';             // the line that , and . move
const lines = it => (it.fold === null ? [] : ['fold']).concat(CFG.crop ? ['left', 'right'] : []);
const keep = () => { try { localStorage.setItem(CFG.key, JSON.stringify(mine)); } catch (e) {} };
const touched = it => {
  const m = mine[it.file];
  return !!m && ((m.fold !== undefined && Math.abs(m.fold - it.fold) > 1e-6) ||
                 (m.angle !== undefined && Math.abs(m.angle - (it.angle || 0)) > 1e-6) ||
                 (m.left !== undefined && Math.abs(m.left - edge0(it, 'left')) > 1e-6) ||
                 (m.right !== undefined && Math.abs(m.right - edge0(it, 'right')) > 1e-6));
};

if (!CFG.rotate) { $('anglebox').style.display = 'none'; $('turnhelp').style.display = 'none'; }
if (!CFG.crop) { $('edgebox').style.display = 'none'; $('edgehelp').style.display = 'none'; }

function show() {
  const it = cur();
  img.src = it.src;
  $('name').textContent = it.file;
  $('pos').textContent = (i + 1) + ' / ' + ITEMS.length;
  active = lines(it)[0] || 'fold';
  $('note').textContent = it.note || '';
  $('was').textContent = it.fold === null ? 'one page, not cut'
      : (it.conf || '') + ' ' + (CFG.pixels ? Math.round(it.fold * it.w) : it.fold.toFixed(3));
  draw();
}

function draw() {
  const it = cur(), w = img.clientWidth || 1, single = it.fold === null;
  for (const el of [line, orig, band]) el.style.display = single ? 'none' : 'block';
  $('cutbox').style.display = single ? 'none' : '';
  if (!single) {
    const f = fold(it);
    line.style.left = (f * w - 1) + 'px';
    orig.style.left = (it.fold * w) + 'px';
    const o = (CFG.overlap || 0) / it.w * w;
    band.style.left = (f * w - o) + 'px';
    band.style.width = (2 * o) + 'px';
    $('frac').textContent = CFG.pixels ? Math.round(f * it.w) : f.toFixed(4);
  }
  for (const el of [lcut, rcut, $('shadeL'), $('shadeR')]) el.style.display = CFG.crop ? 'block' : 'none';
  if (CFG.crop) {
    const L = edge(it, 'left'), R = edge(it, 'right');
    lcut.style.left = (L * w - 1) + 'px';
    rcut.style.left = (R * w - 1) + 'px';
    $('shadeL').style.left = '0px'; $('shadeL').style.width = (L * w) + 'px';
    $('shadeR').style.left = (R * w) + 'px'; $('shadeR').style.width = ((1 - R) * w) + 'px';
    $('edges').textContent = Math.round(L * it.w) + ' to ' + Math.round(R * it.w);
  }
  line.classList.toggle('active', active === 'fold');
  lcut.classList.toggle('active', active === 'left');
  rcut.classList.toggle('active', active === 'right');
  const a = angle(it);
  img.style.transform = 'rotate(' + (-a) + 'deg)';     // CSS turns clockwise, the angle is counter-clockwise
  $('angle').textContent = (a > 0 ? '+' : '') + a.toFixed(2);
  const d = ITEMS.filter(touched).length;
  $('chg').textContent = d ? d + ' changed' : '';
}

function setFold(f) {
  const it = cur();
  if (it.fold === null) return;
  f = Math.max(0.02, Math.min(0.98, f));
  if (CFG.crop) f = Math.max(edge(it, 'left') + 0.02, Math.min(edge(it, 'right') - 0.02, f));
  (mine[it.file] = mine[it.file] || {}).fold = f;
  keep(); draw();
}
function setEdge(k, f) {
  const it = cur(), gap = 0.02;
  let lo = 0, hi = 1;
  if (k === 'left') hi = (it.fold === null ? edge(it, 'right') : fold(it)) - gap;
  else lo = (it.fold === null ? edge(it, 'left') : fold(it)) + gap;
  (mine[it.file] = mine[it.file] || {})[k] = Math.max(lo, Math.min(hi, f));
  keep(); draw();
}
function setLine(k, f) { if (k === 'fold') setFold(f); else setEdge(k, f); }
function where(k) { const it = cur(); return k === 'fold' ? fold(it) : edge(it, k); }
function setAngle(a) {
  if (!CFG.rotate) return;
  const it = cur();
  a = Math.max(-15, Math.min(15, Math.round(a * 100) / 100));
  (mine[it.file] = mine[it.file] || {}).angle = a;
  keep(); draw();
}

// the unturned box of the picture: its centre does not move when the sheet is turned
function box() {
  const r = stage.getBoundingClientRect();
  return {left: r.left, top: r.top, width: img.clientWidth, height: img.clientHeight,
          cx: r.left + img.clientWidth / 2, cy: r.top + img.clientHeight / 2};
}
const lineAt = e => { const b = box(); setLine(active, (e.clientX - b.left) / b.width); };
function nearest(e) {
  const b = box(), x = (e.clientX - b.left) / b.width;
  let best = active, d = 9;
  for (const k of lines(cur())) { const dd = Math.abs(where(k) - x); if (dd < d) { d = dd; best = k; } }
  return best;
}
const bearing = e => { const b = box(); return Math.atan2(e.clientY - b.cy, e.clientX - b.cx) * 180 / Math.PI; };

let mode = null, a0 = 0, b0 = 0;
stage.addEventListener('pointerdown', e => {
  stage.setPointerCapture(e.pointerId);
  if (CFG.rotate && (e.shiftKey || e.button === 2)) {
    mode = 'turn'; a0 = angle(cur()); b0 = bearing(e); document.body.classList.add('turning');
  } else if (e.button === 0 && lines(cur()).length) { mode = 'line'; active = nearest(e); lineAt(e); }
  e.preventDefault();
});
stage.addEventListener('pointermove', e => {
  if (mode === 'line') lineAt(e);
  if (mode === 'turn') {
    let d = bearing(e) - b0;
    if (d > 180) d -= 360;
    if (d < -180) d += 360;
    setAngle(a0 - d);                  // the bearing grows clockwise on the screen
  }
});
const drop = () => { mode = null; document.body.classList.remove('turning'); };
stage.addEventListener('pointerup', drop);
stage.addEventListener('pointercancel', drop);
stage.addEventListener('contextmenu', e => { if (CFG.rotate) e.preventDefault(); });
stage.addEventListener('wheel', e => {
  if (!CFG.rotate) return;
  e.preventDefault();
  const d = e.deltaY || e.deltaX;      // with shift held the browser reports the wheel sideways
  setAngle(angle(cur()) + (d > 0 ? -1 : 1) * (e.shiftKey ? 0.5 : 0.1));
}, {passive: false});
img.addEventListener('load', draw);
window.addEventListener('resize', draw);

function step(d) { i = (i + d + ITEMS.length) %% ITEMS.length; show(); }
$('next').onclick = () => step(1);
$('prev').onclick = () => step(-1);
$('reset').onclick = () => { delete mine[cur().file]; keep(); draw(); };

document.addEventListener('keydown', e => {
  if (e.target === $('out') || e.ctrlKey || e.metaKey || e.altKey) return;
  const px = e.shiftKey ? 10 : 1, deg = e.shiftKey ? 0.5 : 0.05, w = img.clientWidth || 1;
  // arrows page through the openings; comma and full stop nudge the line; brackets turn the sheet
  if (e.key === 'ArrowLeft')  { step(-1); e.preventDefault(); }
  else if (e.key === 'ArrowRight') { step(1);  e.preventDefault(); }
  else if (e.key === ',' || e.key === '<') { setLine(active, where(active) - px / w); e.preventDefault(); }
  else if (e.key === '.' || e.key === '>') { setLine(active, where(active) + px / w); e.preventDefault(); }
  else if (e.key === 'Tab') {
    const ls = lines(cur());
    if (ls.length) { active = ls[(ls.indexOf(active) + (e.shiftKey ? ls.length - 1 : 1)) %% ls.length]; draw(); }
    e.preventDefault();
  }
  else if (e.key === '[' || e.key === '{') { setAngle(angle(cur()) + deg); e.preventDefault(); }
  else if (e.key === ']' || e.key === '}') { setAngle(angle(cur()) - deg); e.preventDefault(); }
  else if (e.key === '0') setAngle(0);
  else if (e.key === 'g') $('grid').style.display = $('grid').style.display === 'block' ? 'none' : 'block';
  else if (e.key === 'n') step(1);
  else if (e.key === 'p') step(-1);
});

function result() {
  const out = {};
  if (CFG.pixels) {            // every opening, in pixels of the scan, with its angle
    for (const it of ITEMS)
      out[it.file] = Object.assign({fold: it.fold === null ? null : Math.round(fold(it) * it.w), angle: angle(it)},
                                   CFG.crop ? {left: Math.round(edge(it, 'left') * it.w),
                                               right: Math.round(edge(it, 'right') * it.w)} : {});
  } else {                     // only the openings whose line was moved, as a fraction of the width
    for (const it of ITEMS) if (touched(it)) out[it.file] = fold(it);
  }
  return out;
}
const json = () => JSON.stringify(result(), null, 1);

$('save').onclick = () => {
  if (!CFG.pixels && !Object.keys(result()).length) { alert('Nothing moved yet.'); return; }
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([json()], {type: 'application/json'}));
  a.download = CFG.save;
  a.click();
};
$('copy').onclick = async () => {
  const out = $('out');
  out.value = json(); out.style.display = 'block'; out.select();
  try { await navigator.clipboard.writeText(json()); } catch (err) {}
};

show();
</script>
"""


def render(title, items, save='folds.json', key=None, rotate=False, pixels=False, overlap=0, crop=False):
    """The page as a string.

    items: [{'file', 'src', 'w', 'h', 'fold' (fraction of the width, or None
    for a scan that is one page), 'angle' (degrees, optional), 'left' and
    'right' (the page edges as fractions of the width, with crop=True;
    0 and 1 if absent), 'conf' (a word on where the fold comes from), 'note'
    (a line shown under the header)}].
    """
    cfg = {'save': save, 'key': key or ('folds:' + title), 'rotate': bool(rotate), 'pixels': bool(pixels),
           'overlap': overlap, 'crop': bool(crop)}
    return PAGE % {'title': title, 'save': save, 'items': json.dumps(items, ensure_ascii=False),
                   'cfg': json.dumps(cfg, ensure_ascii=False)}
