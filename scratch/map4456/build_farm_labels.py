# -*- coding: utf-8 -*-
"""The working page for the editor's farm labels on the Pełzucki 1896 plan.

    python scratch/map4456/build_farm_labels.py

Builds farm_labels.html beside the other working pages of the map
(scratch/map4456/, served from the repository root at localhost:8779). The
page carries the committed labels of maps/pelzucki1896/farms.yml (one per
farmstead, shown as the settler's name) over the published tiles; a farm is
added by choosing it in the missing list (or typing its number) and
clicking its homestead on the map; a label is dragged to move it, Delete
removes the selected one, Enter re-commits a drag. Export downloads
farm_labels_<date>.json - every label, existing and new, in mosaic pixels -
which pipeline/maps/import_farms.py merges back into farms.yml.

The positions are the pixels of the mosaic (reference/maps.yml), the same
space the site's build reads.
"""
import io
import json
import os
import sys
from datetime import date

import yaml

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
FARMS_YML = os.path.join(ROOT, 'maps', 'pelzucki1896', 'farms.yml')
OUT = os.path.join(HERE, 'farm_labels.html')
TILES = 'https://takaji10.github.io/triebenfeld-maps/pelzucki1896/info.json'
OSD = '/site/assets/maps/openseadragon.min.js'

def main():
    with open(FARMS_YML, encoding='utf-8') as f:
        d = yaml.safe_load(f)
    settlers = {s['n']: s for s in (d.get('settlers') or [])}
    marks = [{'n': m['n'], 'x': m['x'], 'y': m['y'],
              'name': (settlers.get(m['n']) or {}).get('name')}
             for m in (d.get('marks') or [])]
    rows = [{'n': s['n'], 'name': s.get('name'), 'total': s.get('total')}
            for s in (d.get('settlers') or [])]
    # the red numbers, the statement's row numbers on each parcel
    # (maps/pelzucki1896/reds.yml): shown as a second layer, toggleable
    reds = []
    reds_p = os.path.join(ROOT, 'maps', 'pelzucki1896', 'reds.yml')
    if os.path.isfile(reds_p):
        with open(reds_p, encoding='utf-8') as f:
            reds = yaml.safe_load(f).get('marks') or []
    data = json.dumps({'tiles': TILES, 'marks': marks, 'rows': rows,
                       'reds': reds,
                       'width': 21715, 'height': 14206},
                      ensure_ascii=False).replace('<', '\\u003c')
    page = TEMPLATE.replace('__DATA__', data).replace('__OSD__', OSD).replace(
        '__TODAY__', date.today().isoformat())
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write(page)
    print(f'farm_labels.html: {len(marks)} labels of {len(rows)} farms '
          f'({len(rows) - len(marks)} to add) -> {OUT}')

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Farm labels — Pełzucki 1896</title>
<style>
body { margin: 0; font: 14px/1.45 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #171614; color: #e8e3da; /* the working page must never scroll: a focus click on the canvas used to scroll the window's 49px of overflow to the bottom, jumping the map under the pointer mid-placement */ height: 100vh; display: flex; flex-direction: column; overflow: hidden; }
header { padding: .6rem 1rem; border-bottom: 1px solid #38342e; flex: 0 0 auto; }
h1 { font-size: 1rem; margin: 0; font-weight: 600; }
.hint { color: #8b847a; font-size: .8rem; margin-top: .25rem; }
#wrap { display: grid; grid-template-columns: 20rem 1fr; flex: 1 1 auto; min-height: 0; }
#panel { border-right: 1px solid #38342e; overflow-y: auto; padding: .6rem; }
#panel h2 { font-size: .78rem; text-transform: uppercase; letter-spacing: .06em; color: #8b847a; margin: .6rem 0 .3rem; }
.farmrow { display: flex; gap: .45rem; align-items: baseline; padding: .18rem .3rem; border-radius: 4px; cursor: pointer; }
.farmrow .multi { color: #b3aca1; font-size: .72rem; white-space: nowrap; }
.farmrow .del { margin-left: auto; flex: 0 0 auto; background: none; border: none; color: #8b847a; font-size: .8rem; line-height: 1; cursor: pointer; padding: .1rem .25rem; border-radius: 3px; }
.farmrow .del:hover { color: #ffb09e; background: rgba(168, 66, 47, .25); }
/* the hovered row's own label on the map: the one the ✕ would remove */
.tag.hovered { background: #c46a3a; box-shadow: 0 0 0 3px rgba(255, 233, 168, .85), 0 0 10px 2px rgba(255, 233, 168, .6); z-index: 7; }
.farmrow:hover { background: #24211d; }
.farmrow.pending { background: #7a3b2e; color: #fff; }
.farmrow .no { font-variant-numeric: tabular-nums; color: #8b847a; min-width: 1.6rem; text-align: right; }
.farmrow.pending .no { color: #f2d8ce; }
.farmrow.done .no { color: #7fae7a; }
#map { position: relative; min-width: 0; }
#viewer { position: absolute; inset: 0; }
#viewer.armed { cursor: crosshair; }
/* the farm pills sit above the red pills: a drag or a click on an overlap
   reaches the farm first, and a red number under a farm pill is edited
   after hiding the names layer (Farm names off) */
.tag { z-index: 6; font-size: 11px; line-height: 1.25; padding: 2px 8px; background: rgba(122, 59, 46, .92); color: #fff; border-radius: 10px; white-space: nowrap; cursor: pointer; box-shadow: 0 1px 3px rgba(0, 0, 0, .4); user-select: none; touch-action: none; position: relative; }
.tag::after { content: ''; position: absolute; left: 50%; top: 50%; width: 7px; height: 7px; margin: -3.5px 0 0 -3.5px; background: #ffe9a8; border: 1px solid #241f1c; border-radius: 50%; pointer-events: none; }
/* The viewer's own drawHTML sets style.display="block" on every redraw
   (each zoom or pan frame), so hiding an overlay by inline style does not
   hold - the label comes back as the map moves. A class with !important
   beats the library's inline style and holds through every redraw. */
.tag.gone, .red-tag.gone { display: none !important; }
/* the red number's editor: a small form under the clicked pill */
#red-editor { position: absolute; z-index: 30; background: #24211d; border: 1px solid #8b847a; border-radius: 4px; padding: .45rem .55rem; display: flex; flex-wrap: wrap; gap: .35rem; align-items: center; box-shadow: 0 2px 8px rgba(0,0,0,.5); font-size: .8rem; }
#red-editor label { display: flex; gap: .35rem; align-items: center; }
#red-editor input { font: inherit; background: #171614; color: #e8e3da; border: 1px solid #38342e; border-radius: 3px; padding: .25rem .4rem; }
#red-editor button { padding: .3rem .55rem; font-size: .78rem; }
#saved.savefail { color: #ffb09e; font-weight: bold; }
/* the save-state banner: a failed or refused save must be impossible to
   miss - small text in a corner has already cost the editor an afternoon */
#savebanner { position: absolute; left: 50%; top: .6rem; transform: translateX(-50%); z-index: 40; display: none; max-width: 44rem; padding: .5rem .55rem .5rem .8rem; border-radius: 4px; font-size: .85rem; line-height: 1.35; box-shadow: 0 2px 10px rgba(0,0,0,.5); align-items: flex-start; gap: .55rem; }
#savebanner.on { display: flex; }
#savebanner button { flex: 0 0 auto; background: none; border: none; color: inherit; font-size: 1rem; line-height: 1; cursor: pointer; padding: 0 .15rem; opacity: .8; }
#savebanner button:hover { opacity: 1; }
#savebanner.fail { background: #7a1f14; color: #ffd9cf; border: 1px solid #a8422f; }
#savebanner.warn { background: #6b5320; color: #ffedc2; border: 1px solid #a88a3a; }
.red-tag.new { box-shadow: 0 0 0 3px rgba(46, 111, 216, .6); }
.red-tag.new .red-num { background: #2e6fd8; }
/* the selected red pill: the one Delete will remove */
.red-tag.sel { box-shadow: 0 0 0 3px #ffe9a8, 0 0 10px rgba(255, 233, 168, .7); }
#red-hint { flex-basis: 100%; color: #8b847a; font-size: .72rem; }
.tag.sel { background: #d99274; color: #241f1c; }
.tag.new { background: #2f6a4f; }
/* the red numbers: grey, all of them - the editor's ruling (2026-11-05):
   they are the plan's finding aids, not highlights. The unsure readings
   are marked by their own [?] and the editor's tooltip, not by colour */
.red-tag { font-size: 10px; line-height: 1.2; padding: 1px 5px; background: rgba(96, 96, 100, .88); color: #fff; border-radius: 8px; white-space: nowrap; box-shadow: 0 1px 2px rgba(0, 0, 0, .25); cursor: move; user-select: none; touch-action: none; }
.red-tag .red-num.unsure { background: rgba(96, 96, 100, .88); border-radius: 8px; padding: 1px 5px; margin: -1px -5px; }
/* the hunt: the pending farm's occurrences, called out loudly */
.red-tag .red-num.hunt { background: #2e6fd8; box-shadow: 0 0 0 3px rgba(46, 111, 216, .6), 0 0 12px 3px rgba(46, 111, 216, .5); }
#saved { font-size: .78rem; color: #8fca8a; align-self: center; }
button.toggle[aria-pressed="true"] { border-color: #d99274; color: #d99274; }
#tools { position: absolute; left: .6rem; top: .6rem; z-index: 10; display: flex; gap: .4rem; }
button { font: inherit; font-size: .82rem; padding: .4rem .8rem; border: 1px solid #38342e; border-radius: 4px; background: #24211d; color: #e8e3da; cursor: pointer; }
button:hover { border-color: #8b847a; }
button.primary { background: #7a3b2e; border-color: #7a3b2e; }
#status { position: absolute; left: .6rem; bottom: .6rem; z-index: 10; font-size: .8rem; color: #b3aca1; background: rgba(23, 22, 20, .85); padding: .3rem .6rem; border-radius: 4px; }
@media (max-width: 50rem) { #wrap { grid-template-columns: 1fr; grid-template-rows: auto 1fr; } #panel { max-height: 30vh; } }
</style>
</head>
<body>
<header>
  <h1>Farm labels — Pełzucki 1896 (working page)</h1>
  <div class="hint">Pick a farm in either list (or type its number and press Enter), then click its homestead - the farm disarms after one placement, so a stray click never becomes a label. A farmer can hold several farmsteads: to place several in one run, hold Shift while clicking, or just click the farm's row again for the next one. Drag a farm label to move it; select a label by clicking its pill, Delete removes that one only. A red number DRAGS to wherever its parcel really lies, and a CLICK corrects its reading (Enter saves - a [?] doubt stays bracketed); the change relinks at once and hides with its farm when Hide linked is on. Every change saves to the project the moment you make it; the server keeps dated snapshots under scratch/map4456/history/. Export JSON downloads the whole state - farms and red readings; Import JSON reads such a file back (the way back from a lost session).</div>
</header>
<div id="wrap">
  <div id="panel">
    <h2>To add (<span id="n-missing"></span>)</h2>
    <div id="missing"></div>
    <h2>Marked (<span id="n-marked"></span>)</h2>
    <div id="marked"></div>
  </div>
  <div id="map">
    <div id="tools">
      <button id="reds-toggle" class="toggle" aria-pressed="true">Red numbers</button>
      <button id="names-toggle" class="toggle" aria-pressed="true">Farm names</button>
      <button id="hide-linked" class="toggle" aria-pressed="false">Hide linked</button>
      <button id="export" class="primary">Export JSON</button>
      <button id="importbtn">Import JSON</button>
      <input type="file" id="importfile" accept=".json,application/json" style="display: none">
      <button id="red-add">+ red number</button>
      <button id="cancel">Esc — cancel</button>
      <span id="saved"></span>
    </div>
    <div id="viewer"></div>
    <div id="savebanner"></div>
    <div id="status"></div>
  </div>
</div>
<script src="__OSD__"></script>
<script>
const D = __DATA__;
const viewer = OpenSeadragon({
  id: 'viewer', prefixUrl: '', showNavigationControl: false,
  tileSources: D.tiles, crossOriginPolicy: 'Anonymous',
  maxZoomPixelRatio: 4, visibilityRatio: 0.5,
  gestureSettingsMouse: { clickToZoom: false, dblClickToZoom: true }
});
const statusEl = document.getElementById('status');
function say(msg) { statusEl.textContent = msg || ''; }

const marksList = [];          // every label: {id, n, x, y, el, ov} - a
                               // farm number may own SEVERAL of these (a
                               // farmer can hold more than one farmstead
                               // within his plot); the (n, x, y) triple is
                               // a label's identity
let nextLabelId = 1;
let pending = null;          // the farm number waiting for its click
let selected = null;         // the selected label's id

function marksFor(n) {
  return marksList.filter(m => m.n === Number(n));
}
// the first label of a farm (or null) - a convenience for the tests
function markPos(n) {
  const m = marksFor(n)[0];
  return m ? { x: m.x, y: m.y } : null;
}
let numBuf = '', numTimer = null;
const savedEl = document.getElementById('saved');

// the whole label set, to the project: the server writes it whole, so the
// disk always carries the state the page shows. Called on every change -
// the end of a drag, a placement, a deletion. A failed save (the server
// down, say) retries itself every few seconds and says so loudly: a move
// must never be lost to a dead server, and the editor must know a save
// did not land.
let saveRetry = null;
// a save that has not landed yet: set when one goes out or fails, cleared
// on success. Only an unsaved state is beacons on tab close - a reload of
// an already-saved page must not rewrite the file under the import.
let farmDirty = false, redsDirty = false;
// the version this tab last saw of each file: sent with every save so the
// server can refuse a stale window (a second tab of this page open, or an
// import that landed after this tab loaded) instead of letting it
// silently overwrite the newer state
let farmV = null, redsV = null;

// the browser's own backup, written before every save attempt - even a
// failed one: a refresh with the server down loses nothing, because the
// next load compares this record's time against the project file's and
// takes the newer
const LS_KEY = 'vonTriebenfeld.map4456.labels';

// an exact duplicate (same farm, same pixel) collapses to one label
// wherever the state is serialised - a double-click must never be able to
// wedge the save file, let alone brick every save after it
function dedupeLabels(list) {
  const seen = new Set();
  return list.filter(m => {
    const k = m.n + ',' + m.x + ',' + m.y;
    if (seen.has(k)) return false;
    seen.add(k);
    return true;
  });
}

function stashLocal() {
  try {
    localStorage.setItem(LS_KEY, JSON.stringify({
      t: new Date().toISOString(),
      farms: dedupeLabels(
        marksList.map(m => ({ n: m.n, x: m.x, y: m.y }))
          .sort((a, b) => a.n - b.n || a.x - b.x || a.y - b.y)),
      reds: {
        marks: redTags.map(t => {
          if (!t.raw) return null;
          const e = { n: t.raw, x: t.x, y: t.y };
          if (t.id < 0) e.id = t.id;
          else if (t.ox != null) { e.ox = t.ox; e.oy = t.oy; }
          return e;
        }).filter(Boolean)
          .sort((a, b) => String(a.n).padStart(4, '0')
            .localeCompare(String(b.n).padStart(4, '0'))),
        deleted: D.redsDeleted || []
      }
    }));
  } catch (e) { /* private mode, quota - the server path still works */ }
}

function banner(msg, kind) {
  const b = document.getElementById('savebanner');
  if (!msg) { b.classList.remove('on'); b.innerHTML = ''; return; }
  // a close button: a banner that cannot be dismissed is its own nuisance
  b.innerHTML = '<span>' + msg + '</span>' +
    '<button id="banner-close" title="dismiss" aria-label="dismiss">' +
    '\u00d7</button>';
  b.className = 'on ' + (kind || 'fail');
  b.querySelector('#banner-close').addEventListener('click', () => {
    b.classList.remove('on');
    b.innerHTML = '';
  });
}

function saveNow() {
  farmDirty = true;
  stashLocal();
  const out = dedupeLabels(
    marksList.map(m => ({ n: m.n, x: m.x, y: m.y }))
      .sort((a, b) => a.n - b.n || a.x - b.x || a.y - b.y));
  const body = JSON.stringify(out);
  fetch('/__save/farm_labels', { method: 'POST',
    headers: { 'Content-Type': 'application/json',
               'X-State-Version': farmV == null ? '' : String(farmV) },
    body: body })
    .then(r => r.json().then(d => ({ ok: r.ok, status: r.status, d })))
    .then(({ ok, status, d }) => {
      if (ok) {
        farmDirty = false;
        farmV = d.v;
        savedEl.classList.remove('savefail');
        savedEl.textContent = 'saved \u00b7 ' + d.saved + ' \u00b7 ' +
          new Date().toLocaleTimeString();
        if (!redsDirty) banner(null);
        return;
      }
      if (status === 409) {
        // another window saved since this tab last did: this tab's state
        // is behind - never overwrite blindly
        banner('The map was changed in another window (or by an import) ' +
               'since this one loaded. Your last change is NOT saved - ' +
               'reload this window to pick up the newer state; Export JSON ' +
               'still holds a copy of what you see.', 'warn');
        savedEl.classList.add('savefail');
        savedEl.textContent = 'not saved \u2014 changed in another window';
        return;
      }
      throw new Error('save failed: ' + status);
    })
    .catch(e => {
      if (e && e.message && e.message.indexOf('409') >= 0) return;
      savedEl.classList.add('savefail');
      savedEl.textContent = 'SAVE FAILED \u2014 server down? Retrying; ' +
        'use Export JSON for a copy now.';
      banner('The server did not take the save. Your work is kept in this ' +
             'browser and pushes again automatically - but export a copy ' +
             'if you are about to close the window.', 'fail');
      clearTimeout(saveRetry);
      saveRetry = setTimeout(saveNow, 3000);
    });
}

// There is deliberately NO save-on-tab-close: a closing window is exactly
// the window whose state may be stale (the work is saved at every change,
// before anything can be lost), and a last-moment write is the one that
// cannot be refused or reasoned about. Unsaved work lives in the browser
// backup stashed at every save attempt; the next load takes it when it is
// newer than the project file and pushes it.

const missingEl = document.getElementById('missing');
const markedEl = document.getElementById('marked');

function rows() { return D.rows; }
function nameOf(n) { const r = rows().find(x => x.n === Number(n)); return r ? r.name : ('№ ' + n); }
function totalOf(n) { const r = rows().find(x => x.n === Number(n)); return r ? (r.total || '') : ''; }

function renderPanel() {
  const done = new Set(marksList.map(m => m.n));
  const miss = rows().filter(r => !done.has(r.n));
  document.getElementById('n-missing').textContent = miss.length;
  document.getElementById('n-marked').textContent = done.size;
  missingEl.innerHTML = '';
  miss.forEach(r => {
    const d = document.createElement('div');
    d.className = 'farmrow' + (pending === r.n ? ' pending' : '');
    d.innerHTML = '<span class="no">' + r.n + '</span><span>' + r.name + '</span>';
    d.addEventListener('click', () => { setPending(pending === r.n ? null : r.n); });
    missingEl.appendChild(d);
  });
  markedEl.innerHTML = '';
  // one row per LABEL: a farmer may hold several farmsteads, each with its
  // own label to move or delete; the count shows when a farm has more
  // than one (2nd of 3, say). Clicking a marked row arms the farm for
  // ANOTHER placement - the way the to-add rows work - so a secondary
  // farmstead is one click away; a specific label is selected by clicking
  // its pill on the map.
  const counts = {};
  marksList.forEach(m => { counts[m.n] = (counts[m.n] || 0) + 1; });
  const seen = {};
  marksList.slice().sort((a, b) => a.n - b.n || a.x - b.x || a.y - b.y)
    .forEach(rec => {
      seen[rec.n] = (seen[rec.n] || 0) + 1;
      const k = counts[rec.n] > 1
        ? ' <span class="multi">' + seen[rec.n] + '/' + counts[rec.n] + '</span>'
        : '';
      const d = document.createElement('div');
      d.className = 'farmrow done' + (pending === rec.n ? ' pending' : '');
      d.title = 'at ' + rec.x + ', ' + rec.y +
        ' - hover finds the label on the map';
      d.innerHTML = '<span class="no">' + rec.n + '</span><span>' +
        nameOf(rec.n) + k + '</span>' +
        '<button class="del" title="remove this label" ' +
        'aria-label="remove this label">\u2715</button>';
      d.addEventListener('click', () => {
        setPending(pending === rec.n ? null : rec.n);
      });
      // hovering the row finds its label on the map: with several labels
      // of one farm, the rows all read alike, but each carries its place
      // (the native tooltip shows the coordinates; no status line here -
      // the row list rebuilds under the cursor on every arm or removal,
      // and the re-entered row would overwrite the arm/remove message)
      d.addEventListener('mouseenter', () => {
        rec.el.classList.add('hovered');
      });
      d.addEventListener('mouseleave', () => {
        rec.el.classList.remove('hovered');
      });
      // the row arms the farm for another placement; the ✕ removes THIS
      // label and no other - the way out of a pile of stray labels
      d.querySelector('.del').addEventListener('click', ev => {
        ev.stopPropagation();
        removeLabel(rec);
      });
      markedEl.appendChild(d);
    });
}

// one label's removal, from the list's ✕ or the Delete key: the label is
// named by its place in the farm's own sequence, so a pile of strays can
// be cleared one at a time
function removeLabel(rec) {
  const i = marksList.indexOf(rec);
  if (i < 0) return;
  viewer.removeOverlay(rec.el);
  marksList.splice(i, 1);
  if (selected === rec.id) select(null);
  const left = marksFor(rec.n).length;
  say('A label of farm ' + rec.n + ' removed \u2014 ' +
      (left ? left + ' of its labels remain.' : 'the farm has none left.'));
  renderPanel();
  applyLayers();
  saveNow();
}

function setPending(n) {
  pending = n;
  // a visible crosshair: while a farm is armed, a plain map click places
  // a label - the cursor must say so
  document.getElementById('viewer').classList.toggle('armed', !!n);
  const found = huntReds(n);
  if (!n) { renderPanel(); return; }
  const k = marksFor(n).length;
  const lead = k
    ? 'Farm ' + n + ' (' + nameOf(n) + ') already has ' +
      (k === 1 ? 'a label' : k + ' labels') +
      ' \u2014 click where its next farmstead stands (hold Shift to arm ' +
      'it for several in a row).'
    : 'Placing farm ' + n + ' (' + nameOf(n) +
      ') \u2014 click the homestead on the map.';
  say(lead + (found ? ' Its ' + found +
       ' red number(s) on the map are outlined blue.'
       : ' No red number of it was found on the map \u2014 place it freely.'));
  renderPanel();
}

// the hunt: while a farm waits for its spot, every red number that reads
// it is outlined blue on the map - the places where that farm's parcels
// lie, so the editor can see where the label belongs. The highlight lives
// on the pill's child span (mutations of the overlay element itself are
// reverted by the viewer's redraw). An unsure reading that carries the
// number (4[5?] reads 45) counts: a doubtful occurrence is still where
// the farm's parcels are.
function huntReds(n) {
  let found = 0;
  redTags.forEach(t => {
    const on = n != null && t.num === n;
    t.span.classList.toggle('hunt', on);
    if (on) found++;
  });
  if (found && !redOn) {
    // the hunt is pointless with the layer off: turn it on and say so
    redOn = true;
    say('Red numbers turned on to show farm ' + n + "'s parcels.");
  }
  if (n != null) applyLayers();
  return found;
}

function select(id) {
  selected = id;
  if (id != null) clearRedSel();   // one selection at a time
  marksList.forEach(m => m.el.classList.toggle('sel', m.id === id));
  renderPanel();
  if (id != null) {
    const m = marksList.find(x => x.id === id);
    if (m) {
      const k = marksFor(m.n).length;
      say('Farm ' + m.n + ' selected' + (k > 1 ? ' (label ' +
          (marksFor(m.n).indexOf(m) + 1) + ' of ' + k + ')' : '') +
          ' — drag to move, Delete removes this one label.');
    }
  }
}

function makeTag(m, isNew) {
  // an exact duplicate - same farm, same pixel - is a double-click, not a
  // second farmstead: two farmsteads are two buildings, never one point.
  // Seven stacked labels of one farm once taught this the hard way.
  const dup = marksList.find(x => x.n === m.n && x.x === m.x && x.y === m.y);
  if (dup) {
    say('A label of farm ' + m.n + ' already stands at ' + m.x + ', ' +
        m.y + ' \u2014 nothing added.');
    return null;
  }
  const d = document.createElement('div');
  d.className = 'tag' + (isNew ? ' new' : '');
  const nm = nameOf(m.n);
  d.textContent = '\u2116 ' + m.n +
    (nm && nm !== ('\u2116 ' + m.n) ? ' \u00b7 ' + nm : '');
  d.setAttribute('data-farm', m.n);
  const p = viewer.viewport.imageToViewportCoordinates(new OpenSeadragon.Point(m.x, m.y));
  viewer.addOverlay({ element: d, location: p,
    placement: OpenSeadragon.Placement.CENTER,
    rotationMode: OpenSeadragon.OverlayRotationMode.NO_ROTATION });
  d.addEventListener('click', ev => {
    ev.stopPropagation();
    if (justMoved === rec.id) { justMoved = null; return; }  // the drag's own click
    if (pending != null) {
      // a placement click landed on an existing label: say so, keep the
      // pending farm armed (the label may belong to the very farm being
      // placed - its next farmstead is just elsewhere)
      say('Farm ' + pending + ' is waiting for its next spot, but this is ' +
          '\u2116 ' + m.n + ' (' + nameOf(m.n) + ')' +
          "'s label - click clear ground nearby for the next one.");
      return;
    }
    select(rec.id);
  });
  const rec = { id: nextLabelId++, n: m.n, x: m.x, y: m.y,
                el: d, ov: overlayFor(d) };
  marksList.push(rec);
  makeDraggable(rec);
  return rec;
}

// the overlay of an element, from the viewer's own list (the public
// getOverlayById has failed in the field once; this reads the same list it
// maintains and cannot disagree with it)
function overlayFor(el) {
  const list = viewer.currentOverlays || [];
  for (let i = 0; i < list.length; i++) {
    if (list[i].element === el) return list[i];
  }
  return null;
}

function makeDraggable(rec) {
  const el = rec.el;
  el.style.cursor = 'move';
  let moved = false;
  function onMove(ev) {
    const rect = document.getElementById('viewer').getBoundingClientRect();
    const vp2 = viewer.viewport.pointFromPixel(
      new OpenSeadragon.Point(ev.clientX - rect.left, ev.clientY - rect.top));
    // the viewer's own updateOverlay, not the overlay's raw update: it sets
    // the redraw flag, without which the pill's drawing lagged its position
    viewer.updateOverlay(el, vp2);
    moved = true;
    const img = viewer.viewport.viewportToImageCoordinates(vp2);
    rec.x = Math.round(img.x);
    rec.y = Math.round(img.y);
  }
  function off() {
    document.removeEventListener('pointermove', onMove, true);
    document.removeEventListener('pointerup', onUp, true);
    document.removeEventListener('pointercancel', off, true);
  }
  function onUp() {
    off();
    if (moved) {
      justMoved = rec.id;
      say('Farm ' + rec.n + ' moved to ' + rec.x + ', ' + rec.y + '.');
      saveNow();
    }
  }
  el.addEventListener('pointerdown', ev => {
    if (ev.button !== 0) return;
    // the map must not pan under the drag: the pointerdown never reaches
    // the viewer's handlers. The move itself is followed on the document,
    // in the capture phase, so the drag keeps working wherever the pointer
    // goes - pointer capture proved unreliable inside the viewer.
    ev.stopPropagation();
    ev.preventDefault();
    rec.ov = overlayFor(el) || rec.ov;
    if (!rec.ov) { say('This label is not on the map - click to place it first.'); return; }
    moved = false;
    document.addEventListener('pointermove', onMove, true);
    document.addEventListener('pointerup', onUp, true);
    document.addEventListener('pointercancel', off, true);
  });
  el.addEventListener('dblclick', ev => ev.stopPropagation());
}

// the red numbers drag the same way the farm labels do: the pointerdown
// never reaches the viewer (the map must not pan under the drag), the
// move is followed on the document in the capture phase, and a drop
// saves at once. A click without movement still opens the reading's
// editor - the drag's own click is swallowed by justDraggedRed.
let justDraggedRed = null;
// the clicked red pill: Delete removes it (a hand-added one outright, a
// baked one by the deletion ledger). One selection at a time - picking a
// farm label or another pill clears it.
let selectedRed = null;

function clearRedSel() {
  selectedRed = null;
  redTags.forEach(t => t.el.classList.remove('sel'));
}

function selectRed(rec) {
  selectedRed = rec;
  redTags.forEach(t => t.el.classList.toggle('sel', t === rec));
  select(null);          // one selection at a time
  editRed(rec);
  say('Red number ' + (rec.raw || '(new)') + ' selected \u2014 Delete ' +
      'removes it; the editor edits the reading.');
}

function makeRedDraggable(rec) {
  const el = rec.el;
  let moved = false;
  function onMove(ev) {
    const rect = document.getElementById('viewer').getBoundingClientRect();
    const vp2 = viewer.viewport.pointFromPixel(
      new OpenSeadragon.Point(ev.clientX - rect.left, ev.clientY - rect.top));
    viewer.updateOverlay(el, vp2);
    moved = true;
    const img = viewer.viewport.viewportToImageCoordinates(vp2);
    rec.x = Math.round(img.x);
    rec.y = Math.round(img.y);
  }
  function off() {
    document.removeEventListener('pointermove', onMove, true);
    document.removeEventListener('pointerup', onUp, true);
    document.removeEventListener('pointercancel', off, true);
  }
  function onUp() {
    off();
    if (moved) {
      justDraggedRed = rec;
      say('Red number ' + rec.raw + ' moved to ' + rec.x + ', ' + rec.y +
          '.'); 
      saveReds();
    }
  }
  el.addEventListener('pointerdown', ev => {
    if (ev.button !== 0) return;
    // the pointerdown must never reach the viewer's handlers: OSD
    // captures the pointer to its canvas and both the drag and the
    // click are lost (the farm pills' guard, twice proven)
    ev.stopPropagation();
    ev.preventDefault();
    rec.ov = overlayFor(el) || rec.ov;
    if (!rec.ov) return;
    moved = false;
    document.addEventListener('pointermove', onMove, true);
    document.addEventListener('pointerup', onUp, true);
    document.addEventListener('pointercancel', off, true);
  });
  el.addEventListener('dblclick', ev => ev.stopPropagation());
}

const redTags = [];          // {el, num} - num the farm's row number, null when unsure
let redOn = true, namesOn = true, hideLinked = false;
let justMoved = null;        // the farm whose drag's own click is to be swallowed

// The layer states in one place: a red number shows when its layer is on
// and, with Hide linked pressed, its farm has no name label yet; a name
// label shows when its layer is on and Hide linked is off (a linked farm's
// name goes with its red numbers). An UNSURE reading (3[7?]) is never
// hidden, whatever number it carries: a doubtful reading is not hidden on
// a say-so - only a firm reading whose farm is linked goes.
function isLinked(num) {
  return num != null && marksList.some(m => m.n === Number(num));
}

function applyLayers() {
  document.getElementById('reds-toggle').setAttribute('aria-pressed', String(redOn));
  document.getElementById('names-toggle').setAttribute('aria-pressed', String(namesOn));
  document.getElementById('hide-linked').setAttribute('aria-pressed', String(hideLinked));
  let shown = 0;
  redTags.forEach(t => {
    const linked = hideLinked && !t.unsure && isLinked(t.num);
    const vis = redOn && !linked;
    t.el.classList.toggle('gone', !vis);
    if (vis) shown++;
  });
  marksList.forEach(m => {
    m.el.classList.toggle('gone', !(namesOn && !hideLinked));
  });
  return shown;
}

// the pill's visible reading: the span's text is what the editor changed,
// the record's raw/num/unsure is what the relink and the import read
function redText(t) { return t.span.textContent; }

function redLayerOn(on) {
  const b = document.getElementById('reds-toggle');
  b.setAttribute('aria-pressed', String(on));
}

// ---- editing a red number -------------------------------------------------
// A click on a red pill opens a small editor at it: type the number as the
// editor reads it (a [?] doubt stays bracketed), Enter saves, Esc cancels.
// The save relinks the number at once - a corrected 3[7?] to 37 links it to
// farm 37, and with Hide linked on, the corrected pill hides with the farm.
const REDS_SAVE = '/__save/red_labels';

// A NEW red number (one the editor adds by hand, with no baked mark behind
// it) carries the negative id that will become its row in reds.yml. The
// id is minted here, kept through every save and reload, and the import
// turns it into the next free mark.
let nextNewRed = -1;

function editRed(rec) {
  if (document.getElementById('red-editor')) return;
  const r = rec.el.getBoundingClientRect();
  const host = document.getElementById('map');
  const box = document.createElement('div');
  box.id = 'red-editor';
  box.style.left = Math.max(8, r.left) - 4 + 'px';
  box.style.top = (r.bottom + 6) + 'px';
  box.innerHTML =
    '<label>\u2116 on the plan <input id="red-num" value="' +
    String(rec.raw).replace(/"/g, '&quot;') + '" size="8" autocomplete="off"></label>' +
    '<button id="red-ok">Save (Enter)</button>' +
    '<button id="red-cancel">Esc</button>' +
    (rec.id >= 0
      ? '<button id="red-del" title="this mark is not on the plan - ' +
        'remove it">Delete</button>'
      : '<button id="red-del" title="withdraw this new number">' +
        'Withdraw</button>') +
    '<div id="red-hint">a bracketed [?] stays a doubt; empty not allowed</div>';
  host.appendChild(box);
  const inp = box.querySelector('#red-num');
  inp.focus();
  inp.select();
  const close = () => box.remove();
  const commit = () => {
    const v = inp.value.trim();
    if (!v) { say('The number cannot be empty.'); return; }
    rec.raw = v;
    rec.unsure = v.includes('[');
    const m = v.match(/\d+/);
    rec.num = m ? Number(m[0]) : null;
    // the text and the unsure colour live on the pill's child span (the
    // viewer's redraw reverts mutations of the overlay element itself)
    rec.span.textContent = v;
    rec.span.classList.toggle('unsure', rec.unsure);
    close();
    applyLayers();
    saveReds();
    say('Red number saved: ' + v +
        (rec.num != null ? ' (farm ' + rec.num + ')' : ' (no farm behind it)') +
        (hideLinked && isLinked(rec.num)
          ? ' - linked, hidden with its farm.'
          : '.'));
  };
  box.querySelector('#red-ok').addEventListener('click', commit);
  box.querySelector('#red-cancel').addEventListener('click', close);
  const delBtn = box.querySelector('#red-del');
  if (delBtn) {
    delBtn.addEventListener('click', () => {
      close();
      removeRed(rec);
    });
  }
  inp.addEventListener('keydown', ev => {
    if (ev.key === 'Enter') {
      ev.preventDefault();
      ev.stopPropagation();   // the editor's keys are the editor's alone
      commit();
    } else if (ev.key === 'Escape') {
      ev.preventDefault();
      ev.stopPropagation();   // the editor's Esc closes only the editor
      close();
      if (rec.fresh && !rec.raw) removeRed(rec);
    }
  });
  box.addEventListener('click', ev => ev.stopPropagation());
  box.addEventListener('pointerdown', ev => ev.stopPropagation());
}

// ---- adding and removing red numbers ---------------------------------------
// The red numbers are the statement's row numbers as the OCR read them off
// the plan; where the OCR missed one, the editor adds it by hand, and
// where it read a smudge as a number, the editor deletes it. A deletion is
// remembered as {del: id} in the saved state, so the import can take the
// mark out of reds.yml; an addition carries its (negative) id until the
// import turns it into a real mark.
function removeRed(rec) {
  const i = redTags.indexOf(rec);
  if (i < 0) return;
  viewer.removeOverlay(rec.el);
  redTags.splice(i, 1);
  if (selectedRed === rec) clearRedSel();
  if (rec.id >= 0) {
    // a baked mark: its deletion is remembered by the position it was
    // baked at - the same identity the import matches by
    if (!D.redsDeleted) D.redsDeleted = [];
    D.redsDeleted.push({ x: rec.ox, y: rec.oy });
    say('Red number ' + rec.raw + ' deleted.');
  } else {
    // a hand-added one: removing it from the state is the whole story -
    // the save no longer carries it, so the import never adds it
    say('The new red number ' + (rec.raw || '') + ' was withdrawn.');
  }
  applyLayers();
  saveReds();
}

// the button's placement: the new pill appears at the centre of the
// current view, already armed for dragging, and the reading editor opens
// at once - drag it into place, type the number, Enter
function addRed() {
  const c = viewer.viewport.getCenter();
  const img = viewer.viewport.viewportToImageCoordinates(c);
  const x = Math.round(img.x), y = Math.round(img.y);
  const d = document.createElement('div');
  d.className = 'red-tag new';
  const span = document.createElement('span');
  span.className = 'red-num';
  span.textContent = '\u00b7 \u00b7 \u00b7';
  d.appendChild(span);
  const p = viewer.viewport.imageToViewportCoordinates(
    new OpenSeadragon.Point(x, y));
  viewer.addOverlay({ element: d, location: p,
    placement: OpenSeadragon.Placement.CENTER,
    rotationMode: OpenSeadragon.OverlayRotationMode.NO_ROTATION });
  const rec = { el: d, span, num: null, raw: '', unsure: false,
                x, y, ox: null, oy: null,
                id: nextNewRed--, ov: overlayFor(d), fresh: true };
  makeRedDraggable(rec);
  d.addEventListener('click', ev => {
    ev.stopPropagation();
    if (justDraggedRed === rec) { justDraggedRed = null; return; }
    selectRed(rec);
  });
  redTags.push(rec);
  applyLayers();
  saveReds();
  editRed(rec);
  say('New red number at ' + x + ', ' + y +
      ' - drag it into place, type the number, Enter.');
  return rec;
}

function saveReds() {
  redsDirty = true;
  stashLocal();
  // a moved red carries the position it was baked at (ox,oy) beside its
  // new one (x,y): the position is a red mark's identity in the import,
  // so the origin must travel with the move. New reds carry their (negative)
  // id; deletions are remembered as the baked positions they removed.
  const out = {
    marks: redTags.map(t => {
      if (!t.raw) return null;   // an untouched new pill: not yet a mark
      const e = { n: t.raw, x: t.x, y: t.y };
      if (t.id < 0) e.id = t.id;
      else if (t.ox != null) { e.ox = t.ox; e.oy = t.oy; }
      return e;
    }).filter(Boolean)
      .sort((a, b) => String(a.n).padStart(4, '0')
        .localeCompare(String(b.n).padStart(4, '0'))),
    deleted: (D.redsDeleted || []).slice()
  };
  fetch(REDS_SAVE, { method: 'POST',
    headers: { 'Content-Type': 'application/json',
               'X-State-Version': redsV == null ? '' : String(redsV) },
    body: JSON.stringify(out) })
    .then(r => r.json().then(d => ({ ok: r.ok, status: r.status, d })))
    .then(({ ok, status, d }) => {
      if (ok) {
        redsDirty = false;
        redsV = d.v;
        savedEl.classList.remove('savefail');
        savedEl.textContent = 'saved \u00b7 reds \u00b7 ' + d.saved;
        if (!farmDirty) banner(null);
        return;
      }
      if (status === 409) {
        banner('The map was changed in another window (or by an import) ' +
               'since this one loaded. Your correction is NOT saved - ' +
               'reload this window to pick up the newer state; Export JSON ' +
               'still holds a copy of what you see.', 'warn');
        savedEl.classList.add('savefail');
        savedEl.textContent = 'not saved \u2014 changed in another window';
        return;
      }
      throw new Error('save failed: ' + status);
    })
    .catch(e => {
      if (e && e.message && e.message.indexOf('409') >= 0) return;
      savedEl.classList.add('savefail');
      savedEl.textContent = 'RED SAVE FAILED \u2014 server down? Retrying; ' +
        'use Export JSON for a copy now.';
      banner('The server did not take the save. Your work is kept in this ' +
             'browser and pushes again automatically - but export a copy ' +
             'if you are about to close the window.', 'fail');
      clearTimeout(saveRetry);
      saveRetry = setTimeout(saveReds, 3000);
    });
}

function init() {
  D.marks.forEach(m => { makeTag(m, false); });
  renderPanel();
  // the red numbers, the statement's row numbers on each parcel: a layer
  // of its own, clickable (a click opens the number for editing - the
  // editor's corrections of uncertain readings). The pill's content is a
  // child span: the viewer's own redraw path has been seen to restore the
  // element's older text and class (an overlay element's mutation after
  // addOverlay was reverted on the next animation frame), so the editing
  // writes the span, which the viewer leaves alone.
  (D.reds || []).forEach((r, i) => {
    if (r.x == null || r.y == null) return;
    const d = document.createElement('div');
    d.className = 'red-tag';
    const span = document.createElement('span');
    span.className = 'red-num' + (r.unsure ? ' unsure' : '');
    span.textContent = r.n;
    d.appendChild(span);
    const p = viewer.viewport.imageToViewportCoordinates(new OpenSeadragon.Point(r.x, r.y));
    viewer.addOverlay({ element: d, location: p,
      placement: OpenSeadragon.Placement.CENTER,
      rotationMode: OpenSeadragon.OverlayRotationMode.NO_ROTATION });
    // the link number comes from the reading itself, however it is
    // written: the baked data carries the readings as strings ('1',
    // '4[5?]'), and a typeof check alone left every unedited pill
    // unlinked - none of the baked red numbers hid with their farm
    const mn = String(r.n).match(/\d+/);
  const rec = { el: d, span, num: mn ? Number(mn[0]) : null,
                raw: r.n, unsure: !!r.unsure, x: r.x, y: r.y,
                // the baked position is the mark's identity: a moved
                // red keeps it beside its new place for the import. A
                // hand-added red keeps its (negative) id instead.
                ox: (r.ox != null ? r.ox : r.x),
                oy: (r.oy != null ? r.oy : r.y),
                id: (typeof r.id === 'number' ? r.id : i),
                ov: overlayFor(d) };
    makeRedDraggable(rec);
    d.addEventListener('click', ev => {
      ev.stopPropagation();
      if (justDraggedRed === rec) { justDraggedRed = null; return; }
      selectRed(rec);
    });
    redTags.push(rec);
  });
  const shown = applyLayers();
  // the next hand-added red continues below the lowest id seen (the ids
  // survive saves and reloads); deletions start as an empty ledger
  redTags.forEach(t => { if (t.id < 0 && t.id < nextNewRed) nextNewRed = t.id; });
  if (!D.redsDeleted) D.redsDeleted = [];
  say((D.restored ? 'Restored ' : 'Loaded ') + D.marks.length +
      ' labels' + (D.redsFixed ? ' and ' + D.redsFixed + ' corrected red numbers' : '') +
      ', ' + shown + ' red numbers showing.' +
      (D.fromLocal ? ' (from this browser\u2019s backup - it was newer than the project file.)' : ''));
  // no POST here: the state was just read from the disk, and an initial
  // save would only mark the tab as a writer of possibly-stale state -
  // two windows of this page used exactly that to erase each other's work.
  // The indicator still reads saved from the start, truthfully: the file
  // holds exactly what this window shows.
  savedEl.textContent = 'saved \u00b7 ' + D.marks.length +
    ' \u00b7 from the project file';
  if (D.fromLocal) {
    // the browser backup was newer than the project file (the server was
    // down at the time): push it now, so the project carries it again
    saveNow();
    saveReds();
  }
}

// the working state of the last save wins over the build's baked data, so a
// reload continues where the last drag left off. The farm labels and the
// reds' corrections each restore from their own file, and BOTH fetches must
// have settled before the tags are built - whichever resolved alone used to
// decide, and a red correction could land after the pills were drawn.
// Against a stale or missing project file stands the browser's own backup
// (written before every save attempt): whichever is newer wins, so even a
// refresh with the server down loses nothing.
// the reds' working state applied to the baked marks, from either source
// (the server file or the browser's backup): a saved entry matches its
// mark by the position the mark had when the entry was written - ox,oy,
// the baked position, falling back to x,y for files written before reds
// could be moved. A moved red carries its new place in x,y; a corrected
// reading carries it in n. The doubt follows the reading, as the import
// does: a correction can clear a doubt as well as set one.
function applyRedsState(saved) {
  // the working state, from either source: a bare list (the old format) or
  // {marks, deleted}. A saved entry matches its mark by the position the
  // mark had when the entry was written - ox,oy, the baked position,
  // falling back to x,y for files written before reds could be moved; new
  // reds (negative id, no ox) carry their own id and are added whole. A
  // deleted entry removes the baked mark baked at that position. The
  // doubt follows the reading, as the import does.
  if (Array.isArray(saved)) saved = { marks: saved, deleted: [] };
  if (!saved || !Array.isArray(saved.marks)) return;
  const dels = new Set((saved.deleted || [])
    .map(x => x.x + ',' + x.y));
  // the deletion ledger MERGES: this state may be the server file or the
  // browser's backup, applied after the other - a ledger that replaced
  // instead of merging once emptied itself on a reload
  if (!D.redsDeleted) D.redsDeleted = [];
  (saved.deleted || []).forEach(x => {
    const k = x.x + ',' + x.y;
    if (!D.redsDeleted.some(d => d.x + ',' + d.y === k)) {
      D.redsDeleted.push({ x: Number(x.x), y: Number(x.y) });
    }
  });
  if (dels.size) D.restored = true;
  D.reds = D.reds.filter(r => {
    if (r.ox == null) { r.ox = r.x; r.oy = r.y; }
    return !dels.has(r.ox + ',' + r.oy);
  });
  const at = new Map(saved.marks.map(x => [
    (x.ox != null ? x.ox : x.x) + ',' + (x.oy != null ? x.oy : x.y), x]));
  let fixed = 0;
  D.reds.forEach(r => {
    const s = at.get(r.ox + ',' + r.oy);
    if (!s) return;
    let ch = false;
    if (s.n != null && String(s.n) !== String(r.n)) {
      r.n = s.n;
      r.unsure = String(s.n).includes('[');
      ch = true;
    }
    if (s.x != null && (Number(s.x) !== r.x || Number(s.y) !== r.y)) {
      r.x = Number(s.x);
      r.y = Number(s.y);
      ch = true;
    }
    if (ch) fixed++;
  });
  // the hand-added marks: no baked origin, they ARE their saved entry -
  // by id, so applying two sources (server file, browser backup) cannot
  // duplicate one
  const added = saved.marks.filter(x => typeof x.id === 'number'
                                        && x.id < 0 && x.n);
  added.forEach(x => {
    if (D.reds.some(r => typeof r.id === 'number' && r.id === x.id)) return;
    D.reds.push({ n: x.n, x: Number(x.x), y: Number(x.y),
                  unsure: String(x.n).includes('['),
                  ox: null, oy: null, id: x.id });
    fixed++;
  });
  if (fixed) { D.redsFixed = fixed; D.restored = true; }
}

let opened = false, farmsIn = false, redsIn = false, inited = false;
function maybeInit() {
  if (opened && farmsIn && redsIn && !inited) {
    // the browser backup wins when it is newer than both files: the case
    // of a change saved to the browser while the server was down
    if (LS && LS.t && new Date(LS.t).getTime() > serverT &&
        Array.isArray(LS.farms) && LS.farms.length) {
      D.marks = LS.farms;
      D.restored = true;
      D.fromLocal = true;
      if (Array.isArray(LS.reds) && LS.reds.length) {
        applyRedsState(LS.reds);
      }
    }
    inited = true; init();
  }
}
viewer.addHandler('open', () => { opened = true; maybeInit(); });
// the browser backup, read first: {t, farms, reds}
let LS = null;
try { LS = JSON.parse(localStorage.getItem(LS_KEY) || 'null'); } catch (e) {}
let serverT = 0;   // the project file's own recency, from Last-Modified
// the versions this window will save against (a save the server refuses
// teaches the banner; without them the first save is blind), and the
// working state comes from THIS server - a test instance serves its own
// sandbox, so the page restores whatever server it was loaded from
fetch('/__save/state?name=farm_labels_latest')
  .then(r => {
    const lm = r.headers.get('Last-Modified');
    if (lm) { const t = new Date(lm).getTime(); if (t > serverT) serverT = t; }
    return r.ok ? r.json() : null;
  })
  .then(saved => {
    if (Array.isArray(saved) && saved.length) { D.marks = saved; D.restored = true; }
  })
  .catch(() => {})
  .then(() => { farmsIn = true; maybeInit(); });
// the reds' own working state (the editor's corrections) restores the same
// way: matched to the baked marks by position, since the positions are the
// marks' identity
fetch('/__save/state?name=red_labels_latest')
  .then(r => {
    const lm = r.headers.get('Last-Modified');
    if (lm) { const t = new Date(lm).getTime(); if (t > serverT) serverT = t; }
    return r.ok ? r.json() : null;
  })
  .then(saved => {
    applyRedsState(saved);
  })
  .catch(() => {})
  .then(() => { redsIn = true; maybeInit(); });
// the versions this window will save against (a save the server refuses
// teaches the banner; without them the first save is blind)
fetch('/__save/version?name=farm_labels_latest').then(r => r.json())
  .then(d => { farmV = d.v; }).catch(() => {});
fetch('/__save/version?name=red_labels_latest').then(r => r.json())
  .then(d => { redsV = d.v; }).catch(() => {});

document.getElementById('reds-toggle').addEventListener('click', () => {
  redOn = !redOn; applyLayers();
});
document.getElementById('names-toggle').addEventListener('click', () => {
  namesOn = !namesOn; applyLayers();
});
document.getElementById('hide-linked').addEventListener('click', () => {
  hideLinked = !hideLinked;
  const shown = applyLayers();
  say(hideLinked ? 'Linked farms and their red numbers hidden - ' + shown +
      ' red numbers left showing (the farms still to do).'
                 : 'All farms and red numbers shown.');
});

// a click on the map places the pending farm - once: the farm DISARMS
// after the placement, because a plain click on the map must never
// quietly become another label (six accidental labels taught this). To
// place SEVERAL farmsteads of the same number in one run, hold Shift
// while clicking: the farm stays armed for the next click.
document.getElementById('viewer').addEventListener('click', ev => {
  if (pending == null) return;
  const rect = document.getElementById('viewer').getBoundingClientRect();
  const vp = viewer.viewport.pointFromPixel(
    new OpenSeadragon.Point(ev.clientX - rect.left, ev.clientY - rect.top));
  const img = viewer.viewport.viewportToImageCoordinates(vp);
  const m = { n: pending, x: Math.round(img.x), y: Math.round(img.y) };
  const keep = ev.shiftKey;
  const k = marksFor(m.n).length;
  const nrec = makeTag(m, true);
  if (!nrec) return;        // an exact duplicate: said so, nothing added
  select(nrec.id);
  huntReds(null);          // the match is made: the blue outlines go
  applyLayers();
  if (keep) {
    say('Farm ' + m.n + ' placed at ' + m.x + ', ' + m.y + ' - label ' +
        (k + 1) + ' of the farm. Shift was held: still armed for the ' +
        'next homestead (plain click or Esc to finish).');
  } else {
    setPending(null);
    say('Farm ' + m.n + ' placed at ' + m.x + ', ' + m.y + '.' +
        (k ? ' That is label ' + (k + 1) + ' of the farm.' : '') +
        (hideLinked ? ' Its name and red numbers are hidden with it.' : '') +
        ' The farm has disarmed - for another farmstead of it, click its ' +
        'row again, or hold Shift while clicking next time.');
  }
  saveNow();
});

window.addEventListener('keydown', ev => {
  if (ev.key === 'Escape') {
    setPending(null); clearRedSel(); select(null); banner(null);
    say('Cancelled.');
  } else if (ev.key === 'Enter' && selected != null) {
    say('Position of farm ' + selected + ' kept.'); select(null);
  } else if ((ev.key === 'Delete' || ev.key === 'Backspace')
             && selectedRed != null
             && document.activeElement === document.body) {
    const rec = selectedRed;
    clearRedSel();
    removeRed(rec);
  } else if ((ev.key === 'Delete' || ev.key === 'Backspace') && selected != null) {
    const rec = marksList.find(m => m.id === selected);
    if (!rec) { select(null); return; }
    removeLabel(rec);
  } else if (/^[0-9]$/.test(ev.key) && document.activeElement === document.body) {
    // digits arm a farm: two keys in quick succession make a two-digit
    // number (7 then 8 -> 78), a pause starts again. A farm that already
    // carries labels arms just the same - that is how another of its
    // farmsteads gets its label.
    numBuf += ev.key;
    clearTimeout(numTimer);
    numTimer = setTimeout(() => { numBuf = ''; }, 900);
    const n = Number(numBuf);
    if (rows().some(r => r.n === n)) {
      setPending(n);
    }
  }
});

document.getElementById('cancel').addEventListener('click', () => { setPending(null); select(null); });
document.getElementById('export').addEventListener('click', () => {
  // the whole working state, farms and red readings both: the file the
  // import takes when the labelling is done
  const out = {
    farms: dedupeLabels(
      marksList.map(m => ({ n: m.n, x: m.x, y: m.y }))
        .sort((a, b) => a.n - b.n || a.x - b.x || a.y - b.y)),
    reds: {
      marks: redTags.map(t => {
        if (!t.raw) return null;
        const e = { n: t.raw, x: t.x, y: t.y };
        if (t.id < 0) e.id = t.id;
        else if (t.ox != null) { e.ox = t.ox; e.oy = t.oy; }
        return e;
      }).filter(Boolean)
        .sort((a, b) => String(a.n).padStart(4, '0')
          .localeCompare(String(b.n).padStart(4, '0'))),
      deleted: D.redsDeleted || []
    }
  };
  const blob = new Blob([JSON.stringify(out, null, 1)],
    { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'map_labels___TODAY__.json';
  a.click();
  URL.revokeObjectURL(a.href);
  say('Exported ' + out.farms.length + ' labels and ' +
      out.reds.marks.length + ' red readings.');
});

document.getElementById('red-add').addEventListener('click', () => {
  addRed();
});

// ---- importing a labels file ----------------------------------------------
// The way back from a lost session: the Export JSON file (or any file in
// its shape) re-sets the whole working state - farm labels wholesale, the
// red readings matched by position. Also takes a bare [{n, x, y}] list of
// farm labels.
document.getElementById('importbtn').addEventListener('click', () => {
  document.getElementById('importfile').click();
});
document.getElementById('importfile').addEventListener('change', ev => {
  const f = ev.target.files[0];
  if (!f) return;
  const rd = new FileReader();
  rd.onload = () => {
    try {
      applyImport(JSON.parse(rd.result), f.name);
    } catch (e) {
      say('That file is not valid JSON — ' + e.message);
    }
  };
  rd.readAsText(f);
  ev.target.value = '';   // the same file can be picked again
});

function applyImport(data, fname) {
  if (!inited) { say('The map is still loading — try again in a moment.'); return; }
  let farms = null, reds = null;
  if (Array.isArray(data)) {
    farms = data;
  } else if (data && Array.isArray(data.farms)) {
    farms = data.farms;
    reds = Array.isArray(data.reds) ? data.reds : null;
  } else {
    say('That file has neither a label list nor {farms, reds} — nothing imported.');
    return;
  }
  if (farms && farms.length) {
    // validate before touching anything: a half-applied import is the
    // one thing worse than a refused one. A farm number may appear
    // several times (several farmsteads) - only the exact same position
    // twice is a mistake.
    const seen = new Set();
    for (const x of farms) {
      if (!Number.isInteger(x.n) || !Number.isFinite(Number(x.x)) ||
          !Number.isFinite(Number(x.y))) {
        say('Farm ' + (x.n != null ? x.n : '?') +
            ' has no usable position — nothing imported.'); return;
      }
      const key = x.n + ',' + Number(x.x) + ',' + Number(x.y);
      if (seen.has(key)) {
        say('Farm ' + x.n + ' appears twice at ' + x.x + ',' + x.y +
            ' — nothing imported.');
        return;
      }
      seen.add(key);
    }
    select(null); setPending(null);
    // the tags are rebuilt whole, as the import into farms.yml does: the
    // file carries the whole set
    marksList.forEach(m => viewer.removeOverlay(m.el));
    marksList.length = 0;
    farms.forEach(m => makeTag({ n: m.n, x: Number(m.x), y: Number(m.y) },
                               false));
  }
  let changed = 0;
  if (reds && (reds.length || reds.deleted && reds.deleted.length)) {
    if (!Array.isArray(reds)) reds = { marks: reds.marks || [],
                                       deleted: reds.deleted || [] };
    const marksL = Array.isArray(reds) ? reds : reds.marks;
    const dels = new Set((reds.deleted || []).map(x => x.x + ',' + x.y));
    // deletions first: the baked pills whose origin is deleted go, and the
    // deletion is remembered for the save
    dels.forEach(k => {
      if (!D.redsDeleted.some(x => x.x + ',' + x.y === k)) {
        D.redsDeleted.push({ x: Number(k.split(',')[0]),
                             y: Number(k.split(',')[1]) });
      }
    });
    for (let i = redTags.length - 1; i >= 0; i--) {
      const t = redTags[i];
      if (t.id >= 0 && dels.has(t.ox + ',' + t.oy)) {
        viewer.removeOverlay(t.el);
        redTags.splice(i, 1);
        changed++;
      }
    }
    const at = new Map(marksL.map(x => [
      (x.ox != null ? x.ox : x.x) + ',' + (x.oy != null ? x.oy : x.y), x]));
    redTags.forEach(t => {
      const v = at.get(t.ox + ',' + t.oy);
      if (v == null) return;
      if (v.n != null && String(v.n) !== t.raw) {
        t.raw = String(v.n);
        t.unsure = t.raw.includes('[');
        const m = t.raw.match(/\d+/);
        t.num = m ? Number(m[0]) : null;
        t.span.textContent = t.raw;
        t.span.classList.toggle('unsure', t.unsure);
        changed++;
      }
      if (v.x != null && (Number(v.x) !== t.x || Number(v.y) !== t.y)) {
        t.x = Number(v.x); t.y = Number(v.y);
        const p = viewer.viewport.imageToViewportCoordinates(
          new OpenSeadragon.Point(t.x, t.y));
        viewer.updateOverlay(t.el, p);
        changed++;
      }
    });
    // hand-added reds in the file: pills built whole
    marksL.filter(x => typeof x.id === 'number' && x.id < 0 && x.n)
      .forEach(x => {
        if (redTags.some(t => t.id === x.id)) return;
        const d = document.createElement('div');
        d.className = 'red-tag';
        const span = document.createElement('span');
        span.className = 'red-num';
        span.textContent = x.n;
        d.appendChild(span);
        const p = viewer.viewport.imageToViewportCoordinates(
          new OpenSeadragon.Point(Number(x.x), Number(x.y)));
        viewer.addOverlay({ element: d, location: p,
          placement: OpenSeadragon.Placement.CENTER,
          rotationMode: OpenSeadragon.OverlayRotationMode.NO_ROTATION });
        const rec = { el: d, span, num: null, raw: x.n,
                      unsure: String(x.n).includes('['),
                      x: Number(x.x), y: Number(x.y), ox: null, oy: null,
                      id: x.id, ov: overlayFor(d) };
        makeRedDraggable(rec);
        d.addEventListener('click', ev => {
          ev.stopPropagation();
          if (justDraggedRed === rec) { justDraggedRed = null; return; }
          selectRed(rec);
        });
        redTags.push(rec);
        changed++;
      });
    if (typeof nextNewRed === 'number') {
      redTags.forEach(t => {
        if (t.id < 0 && t.id < nextNewRed) nextNewRed = t.id;
      });
    }
  }
  applyLayers(); renderPanel();
  if (farms && farms.length) saveNow();
  if (changed) saveReds();
  say('Imported ' + fname + ': ' + (farms ? farms.length : 0) +
      ' farm label(s)' + (changed ? ', ' + changed + ' red reading(s) changed'
                                  : '') + '.');
}
</script>
</body>
</html>
"""

if __name__ == '__main__':
    main()
