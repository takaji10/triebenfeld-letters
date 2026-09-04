# -*- coding: utf-8 -*-
"""
Build a page for placing fold lines by hand.

    python pipeline/intake/review_folds.py --unit oe1bu14526

Writes processed/_spreads_review/review.html. Open it in a browser, drag the
red line onto each fold, save the JSON it offers, then:

    python pipeline/intake/split_spreads.py --unit oe1bu14526 \
        --apply-folds processed/_spreads_review/folds.json

By default it lists the crops still waiting: anything wide enough to be an
opening that has not been split yet. --all includes every unsplit wide crop
even if a verdict was already recorded.

The page is plain HTML opened from disk, so it never uploads anything and
needs no server. It reads the crops straight out of processed/.
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

REVIEW_AR = 1.12          # below this a crop is a single leaf
CROP_RE = re.compile(r'^(.*)_([a-h]\d?)$')


def pending(processed, index_path, include_all):
    """Wide crops that have not been split, with any fold already proposed."""
    from PIL import Image
    proposed = {}
    if os.path.isfile(index_path):
        for line in open(index_path, encoding='utf-8'):
            m = re.match(r'\| (\S.*?) \| \d+x\d+ \| [\d.]+ \| ([\d.]+) \| (\w+) \|.*\| (\w+) \|',
                         line)
            if m:
                proposed[m.group(1)] = (float(m.group(2)), m.group(3), m.group(4))

    out = []
    for fn in sorted(os.listdir(processed)):
        if not fn.lower().endswith('.jpg'):
            continue
        stem = os.path.splitext(fn)[0]
        m = CROP_RE.match(stem)
        if not m:
            continue
        # already split? then <stem>1.jpg and <stem>2.jpg exist
        if os.path.isfile(os.path.join(processed, f'{stem}1.jpg')):
            continue
        with Image.open(os.path.join(processed, fn)) as im:
            w, h = im.size
        if w / h < REVIEW_AR:
            continue
        fold, conf, verdict = proposed.get(fn, (0.5, 'none', 'none'))
        if not include_all and verdict == 'split':
            continue
        out.append({'file': fn, 'w': w, 'h': h,
                    'fold': fold, 'conf': conf, 'verdict': verdict})
    return out


PAGE = """<!doctype html>
<meta charset="utf-8">
<title>Fold review - %(unit)s</title>
<style>
  :root { color-scheme: light dark; }
  body { margin: 0; font: 14px/1.45 system-ui, sans-serif; background: #1a1a1a; color: #eee; }
  header { position: sticky; top: 0; z-index: 5; display: flex; gap: 1rem;
           align-items: center; flex-wrap: wrap;
           padding: .5rem .8rem; background: #111; border-bottom: 1px solid #333; }
  header b { font-weight: 600; }
  .muted { color: #999; }
  button { font: inherit; padding: .3rem .7rem; background: #2a2a2a; color: #eee;
           border: 1px solid #444; border-radius: 4px; cursor: pointer; }
  button:hover { background: #333; }
  button.primary { background: #2d5a2d; border-color: #3d7a3d; }
  #stage { position: relative; margin: 0 auto; width: fit-content; }
  #img { display: block; max-width: 100vw; max-height: calc(100vh - 96px); }
  #line { position: absolute; top: 0; bottom: 0; width: 2px; background: #ff2020;
          cursor: ew-resize; box-shadow: 0 0 0 1px rgba(0,0,0,.4); }
  #line::after { content: ''; position: absolute; left: -12px; right: -12px;
                 top: 0; bottom: 0; cursor: ew-resize; }
  #out { width: 100%%; height: 8rem; font: 12px/1.4 ui-monospace, monospace;
         background: #111; color: #ddd; border: 1px solid #333; display: none; }
  kbd { background: #333; border-radius: 3px; padding: 0 .3em; }
</style>

<header>
  <button id="prev">&larr;</button>
  <b id="pos"></b>
  <button id="next">&rarr;</button>
  <span id="name" class="muted"></span>
  <span>fold <b id="frac"></b></span>
  <span id="was" class="muted"></span>
  <span style="flex:1"></span>
  <button id="save" class="primary">Save folds.json</button>
  <button id="copy">Copy JSON</button>
  <span class="muted"><kbd>&larr;</kbd><kbd>&rarr;</kbd> nudge,
    <kbd>shift</kbd> faster, <kbd>n</kbd>/<kbd>p</kbd> next/prev,
    <kbd>s</kbd> skip</span>
</header>

<div id="stage">
  <img id="img" alt="">
  <div id="line"></div>
</div>
<textarea id="out" spellcheck="false"></textarea>

<script>
const ITEMS = %(items)s;
const folds = {};                       // file -> fraction, only what you set
let i = 0;

const img = document.getElementById('img');
const line = document.getElementById('line');
const stage = document.getElementById('stage');

function cur() { return ITEMS[i]; }

function show() {
  const it = cur();
  img.src = '../' + it.file;
  document.getElementById('name').textContent = it.file;
  document.getElementById('pos').textContent = (i + 1) + ' / ' + ITEMS.length;
  document.getElementById('was').textContent =
    'detected ' + it.fold.toFixed(3) + ' (' + it.conf + ')';
  place(folds[it.file] !== undefined ? folds[it.file] : it.fold);
}

function place(frac) {
  frac = Math.max(0.02, Math.min(0.98, frac));
  folds[cur().file] = frac;
  line.style.left = (frac * img.clientWidth) + 'px';
  document.getElementById('frac').textContent = frac.toFixed(4);
}

function fromEvent(e) {
  const r = img.getBoundingClientRect();
  const x = (e.touches ? e.touches[0].clientX : e.clientX) - r.left;
  place(x / r.width);
}

let dragging = false;
stage.addEventListener('pointerdown', e => { dragging = true; fromEvent(e);
                                             stage.setPointerCapture(e.pointerId); });
stage.addEventListener('pointermove', e => { if (dragging) fromEvent(e); });
stage.addEventListener('pointerup',   e => { dragging = false; });
img.addEventListener('load', () => place(folds[cur().file] ?? cur().fold));
window.addEventListener('resize', () => place(folds[cur().file] ?? cur().fold));

function step(d) { i = (i + d + ITEMS.length) %% ITEMS.length; show(); }
document.getElementById('next').onclick = () => step(1);
document.getElementById('prev').onclick = () => step(-1);

document.addEventListener('keydown', e => {
  const px = e.shiftKey ? 10 : 1;
  if (e.key === 'ArrowLeft')  { place((line.offsetLeft - px) / img.clientWidth); e.preventDefault(); }
  if (e.key === 'ArrowRight') { place((line.offsetLeft + px) / img.clientWidth); e.preventDefault(); }
  if (e.key === 'n') step(1);
  if (e.key === 'p') step(-1);
  if (e.key === 's') { delete folds[cur().file]; step(1); }   // leave this one alone
});

function json() { return JSON.stringify(folds, null, 1); }

document.getElementById('save').onclick = () => {
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([json()], {type: 'application/json'}));
  a.download = 'folds.json';
  a.click();
};
document.getElementById('copy').onclick = async () => {
  const out = document.getElementById('out');
  out.value = json(); out.style.display = 'block'; out.select();
  try { await navigator.clipboard.writeText(json()); } catch (err) { /* select instead */ }
};

show();
</script>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--unit', help='unit slug; required when the project holds more than one')
    ap.add_argument('--all', action='store_true',
                    help='include wide crops already marked split in INDEX.md')
    a = ap.parse_args()

    unit = unitlib.one_unit(a.unit)
    processed = os.path.join(unit.raw_dir, 'processed')
    review = os.path.join(processed, '_spreads_review')
    if not os.path.isdir(processed):
        raise SystemExit(f'{unit.slug}: nothing cropped yet at {processed}')
    os.makedirs(review, exist_ok=True)

    items = pending(processed, os.path.join(review, 'INDEX.md'), a.all)
    if not items:
        print(f'  {unit.slug}: nothing waiting - every opening is split')
        return

    out = os.path.join(review, 'review.html')
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write(PAGE % {'unit': unit.slug,
                        'items': json.dumps(items, ensure_ascii=False)})

    print(f'  {len(items)} opening(s) waiting')
    for it in items:
        print(f"    {it['file']}  detected {it['fold']:.3f} ({it['conf']})")
    print(f'\n  wrote {out}')
    print('  Open it, drag each red line onto the fold, then Save folds.json and run:')
    print(f'    python pipeline/intake/split_spreads.py --unit {unit.slug} \\')
    print('        --apply-folds processed/_spreads_review/folds.json')


if __name__ == '__main__':
    main()
