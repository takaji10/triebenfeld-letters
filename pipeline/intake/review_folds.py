# -*- coding: utf-8 -*-
"""
Build a page for placing fold lines by hand.

    python pipeline/intake/review_folds.py --unit oe1bu14526           # not yet split
    python pipeline/intake/review_folds.py --unit oe1bu14526 --done    # check the splits

Writes processed/_spreads_review/review.html. Open it in a browser, drag the red
line onto each fold, save the JSON it offers, then:

    python pipeline/intake/split_spreads.py --unit oe1bu14526 \
        --apply-folds processed/_spreads_review/folds.json

Default lists openings still waiting. --done lists ones already split, showing
the original with the fold that was used, so an automatic decision can be
checked and moved; folds you placed yourself are left out unless you ask for
them with --include-hand.

Only spreads whose line you actually move are written to the JSON, and moving a
fold on an already-split spread undoes and redoes that split. The page is plain
HTML opened from disk: no server, nothing uploaded.
"""
import argparse
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
import unitlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

REVIEW_AR = 1.12
CROP_RE = re.compile(r'^(.*)_([a-h]\d?)$')


def load_json(path, default):
    if os.path.isfile(path):
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    return default


def detected_folds(index_path):
    """What the detector proposed, from the review index."""
    out = {}
    if not os.path.isfile(index_path):
        return out
    for line in open(index_path, encoding='utf-8'):
        m = re.match(r'\| (\S.*?) \| \d+x\d+ \| [\d.]+ \| ([\d.]+) \| (\w+) \|', line)
        if m:
            out[m.group(1)] = (float(m.group(2)), m.group(3))
    return out


def fold_from_manifest(manifest, base, suf):
    for entries in manifest.values():
        halves = [e for e in entries
                  if e['file'] in (f'{base}_{suf}1.jpg', f'{base}_{suf}2.jpg')]
        if len(halves) == 2:
            halves.sort(key=lambda e: e['bbox_original'][0])
            x0 = halves[0]['bbox_original'][0]
            x1 = halves[1]['bbox_original'][2]
            cut = halves[0]['bbox_original'][2]
            if x1 > x0:
                return (cut - x0) / (x1 - x0)
    return None


def collect(processed, review, done, include_hand):
    from PIL import Image
    proposed = detected_folds(os.path.join(review, 'INDEX.md'))
    hand = load_json(os.path.join(review, 'hand_placed.json'), {})
    manifest = load_json(os.path.join(processed, 'manifest.json'), {})
    unsplit_dir = os.path.join(processed, '_spreads_unsplit')

    items = []
    if done:
        if not os.path.isdir(unsplit_dir):
            return items
        for fn in sorted(os.listdir(unsplit_dir)):
            if not fn.lower().endswith('.jpg'):
                continue
            if fn in hand and not include_hand:
                continue
            m = CROP_RE.match(os.path.splitext(fn)[0])
            if not m:
                continue
            with Image.open(os.path.join(unsplit_dir, fn)) as im:
                w, h = im.size
            fold = fold_from_manifest(manifest, m.group(1), m.group(2))
            det, conf = proposed.get(fn, (None, 'auto'))
            items.append({'file': fn, 'src': '../_spreads_unsplit/' + fn,
                          'w': w, 'h': h,
                          'fold': round(fold if fold is not None else det or 0.5, 4),
                          'conf': ('by hand' if fn in hand else conf),
                          'state': 'split'})
        return items

    for fn in sorted(os.listdir(processed)):
        if not fn.lower().endswith('.jpg'):
            continue
        stem = os.path.splitext(fn)[0]
        m = CROP_RE.match(stem)
        if not m or os.path.isfile(os.path.join(processed, f'{stem}1.jpg')):
            continue
        with Image.open(os.path.join(processed, fn)) as im:
            w, h = im.size
        if w / h < REVIEW_AR:
            continue
        fold, conf = proposed.get(fn, (0.5, 'none'))
        items.append({'file': fn, 'src': '../' + fn, 'w': w, 'h': h,
                      'fold': fold, 'conf': conf, 'state': 'waiting'})
    return items


PAGE = """<!doctype html>
<meta charset="utf-8">
<title>Fold review - %(unit)s</title>
<style>
  :root { color-scheme: light dark; }
  body { margin: 0; font: 14px/1.45 system-ui, sans-serif; background: #1a1a1a; color: #eee; }
  header { position: sticky; top: 0; z-index: 5; display: flex; gap: .9rem;
           align-items: center; flex-wrap: wrap;
           padding: .5rem .8rem; background: #111; border-bottom: 1px solid #333; }
  .muted { color: #999; }
  .moved { color: #7ec87e; }
  button { font: inherit; padding: .3rem .7rem; background: #2a2a2a; color: #eee;
           border: 1px solid #444; border-radius: 4px; cursor: pointer; }
  button:hover { background: #333; }
  button.primary { background: #2d5a2d; border-color: #3d7a3d; }
  #stage { position: relative; margin: 0 auto; width: fit-content; }
  #img { display: block; max-width: 100vw; max-height: calc(100vh - 92px); }
  #line { position: absolute; top: 0; bottom: 0; width: 2px; background: #ff2020; }
  #line::after { content: ''; position: absolute; left: -14px; right: -14px;
                 top: 0; bottom: 0; cursor: ew-resize; }
  #orig { position: absolute; top: 0; bottom: 0; width: 1px; background: #4a90d9; opacity: .8; }
  #out { width: 100%%; height: 9rem; font: 12px/1.4 ui-monospace, monospace;
         background: #111; color: #ddd; border: 1px solid #333; display: none; }
  kbd { background: #333; border-radius: 3px; padding: 0 .3em; }
</style>

<header>
  <button id="prev">&larr;</button>
  <b id="pos"></b>
  <button id="next">&rarr;</button>
  <span id="name" class="muted"></span>
  <span>cut <b id="frac"></b></span>
  <span id="was" class="muted"></span>
  <span id="chg" class="moved"></span>
  <span style="flex:1"></span>
  <button id="reset">Reset this</button>
  <button id="save" class="primary">Save folds.json</button>
  <button id="copy">Copy</button>
  <span class="muted"><kbd>&larr;</kbd><kbd>&rarr;</kbd> page,
    <kbd>,</kbd><kbd>.</kbd> nudge the line, <kbd>shift</kbd> x10,
    blue line = current cut</span>
</header>

<div id="stage">
  <img id="img" alt="">
  <div id="orig"></div>
  <div id="line"></div>
</div>
<textarea id="out" spellcheck="false"></textarea>

<script>
const ITEMS = %(items)s;
const moved = {};              // only spreads you actually adjust
let i = 0, shown = 0.5;

const img = document.getElementById('img');
const line = document.getElementById('line');
const orig = document.getElementById('orig');
const stage = document.getElementById('stage');
const cur = () => ITEMS[i];

function show() {
  const it = cur();
  img.src = it.src;
  document.getElementById('name').textContent = it.file;
  document.getElementById('pos').textContent = (i + 1) + ' / ' + ITEMS.length;
  document.getElementById('was').textContent = it.conf + ' ' + it.fold.toFixed(3);
  draw(moved[it.file] !== undefined ? moved[it.file] : it.fold, false);
}

function draw(frac, byUser) {
  frac = Math.max(0.02, Math.min(0.98, frac));
  shown = frac;
  const w = img.clientWidth || 1;
  line.style.left = (frac * w) + 'px';
  orig.style.left = (cur().fold * w) + 'px';
  document.getElementById('frac').textContent = frac.toFixed(4);
  if (byUser) moved[cur().file] = frac;
  const d = Object.keys(moved).length;
  document.getElementById('chg').textContent = d ? d + ' moved' : '';
}

function fromEvent(e) {
  const r = img.getBoundingClientRect();
  draw(((e.touches ? e.touches[0].clientX : e.clientX) - r.left) / r.width, true);
}

let dragging = false;
stage.addEventListener('pointerdown', e => { dragging = true; fromEvent(e);
                                             stage.setPointerCapture(e.pointerId); });
stage.addEventListener('pointermove', e => { if (dragging) fromEvent(e); });
stage.addEventListener('pointerup', () => { dragging = false; });
img.addEventListener('load', () => draw(moved[cur().file] ?? cur().fold, false));
window.addEventListener('resize', () => draw(shown, false));

function step(d) { i = (i + d + ITEMS.length) %% ITEMS.length; show(); }
document.getElementById('next').onclick = () => step(1);
document.getElementById('prev').onclick = () => step(-1);
document.getElementById('reset').onclick = () => { delete moved[cur().file];
                                                   draw(cur().fold, false); };

document.addEventListener('keydown', e => {
  const px = e.shiftKey ? 10 : 1;
  // arrows page through the spreads; comma and full stop nudge the line
  if (e.key === 'ArrowLeft')  { step(-1); e.preventDefault(); }
  if (e.key === 'ArrowRight') { step(1);  e.preventDefault(); }
  if (e.key === ',' || e.key === '<') { draw((line.offsetLeft - px) / img.clientWidth, true); e.preventDefault(); }
  if (e.key === '.' || e.key === '>') { draw((line.offsetLeft + px) / img.clientWidth, true); e.preventDefault(); }
  if (e.key === 'n') step(1);
  if (e.key === 'p') step(-1);
});

const json = () => JSON.stringify(moved, null, 1);

document.getElementById('save').onclick = () => {
  if (!Object.keys(moved).length) { alert('Nothing moved yet.'); return; }
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([json()], {type: 'application/json'}));
  a.download = 'folds.json';
  a.click();
};
document.getElementById('copy').onclick = async () => {
  const out = document.getElementById('out');
  out.value = json(); out.style.display = 'block'; out.select();
  try { await navigator.clipboard.writeText(json()); } catch (err) {}
};

show();
</script>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--unit', help='unit slug; required when the project holds more than one')
    ap.add_argument('--done', action='store_true',
                    help='review spreads already split, rather than ones still waiting')
    ap.add_argument('--include-hand', action='store_true',
                    help='with --done, also list folds you placed yourself')
    a = ap.parse_args()

    unit = unitlib.one_unit(a.unit)
    processed = os.path.join(unit.raw_dir, 'processed')
    review = os.path.join(processed, '_spreads_review')
    if not os.path.isdir(processed):
        raise SystemExit(f'{unit.slug}: nothing cropped yet at {processed}')
    os.makedirs(review, exist_ok=True)

    items = collect(processed, review, a.done, a.include_hand)
    if not items:
        print(f'  {unit.slug}: nothing to show'
              + (' - no splits recorded' if a.done else ' - every opening is split'))
        return

    out = os.path.join(review, 'review.html')
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write(PAGE % {'unit': unit.slug,
                        'items': json.dumps(items, ensure_ascii=False)})

    hand = len([x for x in items if x['conf'] == 'by hand'])
    print(f'  {len(items)} spread(s) to look at'
          + (f' ({hand} of them placed by hand)' if hand else ''))
    print(f'  wrote {out}')
    print()
    print('  Red line is where the cut will go; blue is where it is now.')
    print('  Only spreads you actually move are saved. Then run:')
    print(f'    python pipeline/intake/split_spreads.py --unit {unit.slug} \\')
    print('        --apply-folds processed/_spreads_review/folds.json')


if __name__ == '__main__':
    main()
