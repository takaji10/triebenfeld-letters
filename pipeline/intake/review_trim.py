# -*- coding: utf-8 -*-
"""
Build a page for trimming the left and right edges off pages.

    python pipeline/intake/review_trim.py --unit oe1bu14526

Sheets in a volume differ in size, so a page often carries a strip of the leaf
underneath along an edge - and on a page narrower than both its neighbours, along
both edges at once. This lists every page image with two draggable lines, one per
side; the shaded bands outside them are what gets removed. Save trims.json, then:

    python pipeline/intake/apply_trims.py --unit oe1bu14526 \
        --trims processed/_trim_review/trims.json

The JSON is {page: [left, right]} as fractions of the width: everything left of
`left` and right of `right` goes, so [0, 1] means leave the page alone.

Every page is written to the JSON: at the lines you moved, or at the detected
edges if you left them alone. Leaving a page untouched means you agree with the
proposed cut, not that the page is skipped - so page through all of them. To
keep a page whole, press `x` (or "No trim"), which records it explicitly as not
to be cut.

Pages already trimmed show where their edges now are, so a trim can be checked
or taken further.
"""
import argparse
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
import unitlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

W = 240
BAND = 0.28
STEP = 12
SMOOTH = 2


def edges(path):
    """(left, right) as fractions: where the top leaf starts and ends.

    The boundary is a step in median column brightness, tiny across the page
    and tens of levels at a paper edge. Median down the column ignores the
    writing; the top and bottom eighths are skipped because the head and tail
    of the book are ragged.
    """
    from PIL import Image
    with Image.open(path) as im:
        g = im.convert('L')
        w0, h0 = g.size
        s = g.resize((W, max(1, round(h0 * W / w0))))
        px = s.load()
        w, h = s.size
        y0, y1 = h // 8, h - h // 8
        med = []
        for x in range(w):
            vals = sorted(px[x, y] for y in range(y0, y1))
            med.append(vals[len(vals) // 2])
    sm = []
    for x in range(w):
        lo, hi = max(0, x - SMOOTH), min(w, x + SMOOTH + 1)
        sm.append(sum(med[lo:hi]) // (hi - lo))

    band = int(w * BAND)
    body = sorted(sm[band:w - band])
    page = body[len(body) // 2] if body else 200

    # Walk in from the outside and stop at the first step, not out from the
    # inside and stop at the last. The paper edge is the outermost step there
    # is; a step further in is the writing block or a shadow. Read the other way
    # round, the right-hand edge on this holding proposed a median of 3.3% and a
    # worst case of 25%; read from outside in, 1.7% and 5%. The failure this way
    # is a dark line at the very edge stopping the scan early, which under-trims
    # - obvious on sight, and another pass fixes it.
    left = 0.0
    for x in range(3, band):
        if abs(sm[x] - sm[x - 3]) >= STEP and sm[x - 3] < page - STEP // 2:
            left = x / w
            break
    right = 1.0
    for x in range(w - 4, w - band, -1):
        if abs(sm[x] - sm[x + 3]) >= STEP and sm[x + 3] < page - STEP // 2:
            right = x / w
            break
    return round(left, 4), round(right, 4)


def collect(processed, done_dir):
    from PIL import Image
    items = []
    names = sorted(f for f in os.listdir(processed) if f.lower().endswith('.jpg'))
    for n, fn in enumerate(names, 1):
        path = os.path.join(processed, fn)
        if not os.path.isfile(path):
            continue
        with Image.open(path) as im:
            w, h = im.size
        left, right = edges(path)
        items.append({'file': fn, 'src': '../' + fn, 'w': w, 'h': h,
                      'left': left, 'right': right,
                      'trimmed': os.path.isfile(os.path.join(done_dir, fn))})
        print(f'  [{n}/{len(names)}] {fn}  left {round(left * w):4d}px  '
              f'right {round((1 - right) * w):4d}px')
    return items


PAGE = """<!doctype html>
<meta charset="utf-8">
<title>Trim review - %(unit)s</title>
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
  button.on { background: #444; border-color: #777; }
  #stage { position: relative; margin: 0 auto; width: fit-content;
           cursor: ew-resize; touch-action: none; }
  #img { display: block; max-width: 100vw; max-height: calc(100vh - 96px); }
  .cut { position: absolute; top: 0; bottom: 0; background: rgba(255,32,32,.28);
         pointer-events: none; }
  .line { position: absolute; top: 0; bottom: 0; width: 2px; background: #ff2020;
          pointer-events: none; }
  /* the line being steered is the brighter one */
  .line.idle { background: rgba(255,32,32,.45); }
  #out { width: 100%%; height: 9rem; font: 12px/1.4 ui-monospace, monospace;
         background: #111; color: #ddd; border: 1px solid #333; display: none; }
  kbd { background: #333; border-radius: 3px; padding: 0 .3em; }
</style>

<header>
  <button id="prev">&larr;</button>
  <b id="pos"></b>
  <button id="next">&rarr;</button>
  <span id="name" class="muted"></span>
  <span id="cutinfo"></span>
  <span id="chg" class="moved"></span>
  <span style="flex:1"></span>
  <button id="pick-l">Left</button>
  <button id="pick-r">Right</button>
  <button id="none">No trim</button>
  <button id="reset">Reset</button>
  <button id="save" class="primary">Save trims.json</button>
  <button id="copy">Copy</button>
  <span class="muted"><kbd>&larr;</kbd><kbd>&rarr;</kbd> page,
    <kbd>l</kbd><kbd>r</kbd> side, <kbd>,</kbd><kbd>.</kbd> nudge,
    <kbd>shift</kbd> x10, <kbd>x</kbd> no trim; shaded bands are removed</span>
</header>

<div id="stage">
  <img id="img" alt="">
  <div class="cut" id="cut-l"></div>
  <div class="cut" id="cut-r"></div>
  <div class="line" id="line-l"></div>
  <div class="line" id="line-r"></div>
</div>
<textarea id="out" spellcheck="false"></textarea>

<script>
const ITEMS = %(items)s;
const set = {};                // your overrides; everything else saves at its guess
const MIN_GAP = 0.05;          // the two lines may not cross or pinch the page shut
// NB: not `left`/`right` as bare globals would be fine, but `top`, `name` and
// friends are not - a `let top` at script scope is a SyntaxError that stops the
// whole file. Keeping to these two names sidesteps the whole family.
let i = 0, lcut = 0, rcut = 1, active = 'l';

const img = document.getElementById('img');
const stage = document.getElementById('stage');
const at = () => ITEMS[i];

function show() {
  const it = at();
  img.src = it.src;
  document.getElementById('name').textContent =
    it.file + (it.trimmed ? ' (already trimmed)' : '');
  document.getElementById('pos').textContent = (i + 1) + ' / ' + ITEMS.length;
  const s = set[it.file];
  lcut = s ? s[0] : it.left;
  rcut = s ? s[1] : it.right;
  draw(false);
}

function draw(byUser) {
  const w = img.clientWidth || 1;
  document.getElementById('cut-l').style.left = '0px';
  document.getElementById('cut-l').style.width = (lcut * w) + 'px';
  document.getElementById('cut-r').style.right = '0px';
  document.getElementById('cut-r').style.width = ((1 - rcut) * w) + 'px';
  document.getElementById('line-l').style.left = (lcut * w) + 'px';
  document.getElementById('line-r').style.left = (rcut * w) + 'px';
  document.getElementById('line-l').className = 'line' + (active === 'l' ? '' : ' idle');
  document.getElementById('line-r').className = 'line' + (active === 'r' ? '' : ' idle');

  const it = at();
  const lp = Math.round(lcut * it.w), rp = Math.round((1 - rcut) * it.w);
  document.getElementById('cutinfo').textContent =
    (lp < 2 && rp < 2) ? 'no trim' : ('left ' + lp + 'px, right ' + rp + 'px');
  document.getElementById('pick-l').className = active === 'l' ? 'on' : '';
  document.getElementById('pick-r').className = active === 'r' ? 'on' : '';
  if (byUser) set[it.file] = [round4(lcut), round4(rcut)];
  const n = Object.keys(set).length;
  document.getElementById('chg').textContent =
    n + ' adjusted; all ' + ITEMS.length + ' will be saved';
}

const round4 = v => Math.round(v * 10000) / 10000;

function place(frac, which) {
  frac = Math.max(0, Math.min(1, frac));
  if (which === 'l') lcut = Math.min(frac, rcut - MIN_GAP);
  else rcut = Math.max(frac, lcut + MIN_GAP);
  active = which;
  draw(true);
}

// the line you grab is whichever is nearer where you pressed
function fromEvent(e, which) {
  const r = img.getBoundingClientRect();
  const frac = (e.clientX - r.left) / r.width;
  place(frac, which || (Math.abs(frac - lcut) <= Math.abs(frac - rcut) ? 'l' : 'r'));
}

let dragging = null;
stage.addEventListener('pointerdown', e => {
  const r = img.getBoundingClientRect();
  const frac = (e.clientX - r.left) / r.width;
  dragging = Math.abs(frac - lcut) <= Math.abs(frac - rcut) ? 'l' : 'r';
  fromEvent(e, dragging);
  stage.setPointerCapture(e.pointerId);
  e.preventDefault();
});
stage.addEventListener('pointermove', e => { if (dragging) fromEvent(e, dragging); });
stage.addEventListener('pointerup', () => { dragging = null; });
img.addEventListener('load', () => draw(false));
window.addEventListener('resize', () => draw(false));

function step(d) { i = (i + d + ITEMS.length) %% ITEMS.length; show(); }
document.getElementById('next').onclick = () => step(1);
document.getElementById('prev').onclick = () => step(-1);
document.getElementById('pick-l').onclick = () => { active = 'l'; draw(false); };
document.getElementById('pick-r').onclick = () => { active = 'r'; draw(false); };
document.getElementById('none').onclick = () => { lcut = 0; rcut = 1; draw(true); };
document.getElementById('reset').onclick = () => { delete set[at().file];
                                                   lcut = at().left; rcut = at().right;
                                                   draw(false); };

document.addEventListener('keydown', e => {
  const w = img.clientWidth || 1;
  const d = (e.shiftKey ? 10 : 1) / w;
  if (e.key === 'ArrowLeft')  { step(-1); e.preventDefault(); }
  if (e.key === 'ArrowRight') { step(1);  e.preventDefault(); }
  if (e.key === 'l') { active = 'l'; draw(false); }
  if (e.key === 'r') { active = 'r'; draw(false); }
  if (e.key === ',' || e.key === '<') { place((active === 'l' ? lcut : rcut) - d, active);
                                        e.preventDefault(); }
  if (e.key === '.' || e.key === '>') { place((active === 'l' ? lcut : rcut) + d, active);
                                        e.preventDefault(); }
  if (e.key === 'x') { lcut = 0; rcut = 1; draw(true); }
  if (e.key === 'n') step(1);
  if (e.key === 'p') step(-1);
});

const json = () => JSON.stringify(Object.fromEntries(ITEMS.map(it =>
  [it.file, set[it.file] !== undefined ? set[it.file] : [it.left, it.right]])), null, 1);

document.getElementById('save').onclick = () => {
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([json()], {type: 'application/json'}));
  a.download = 'trims.json';
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
    a = ap.parse_args()

    unit = unitlib.one_unit(a.unit)
    processed = os.path.join(unit.raw_dir, 'processed')
    review = os.path.join(processed, '_trim_review')
    untrimmed = os.path.join(processed, '_untrimmed')
    if not os.path.isdir(processed):
        raise SystemExit(f'{unit.slug}: nothing cropped yet at {processed}')
    os.makedirs(review, exist_ok=True)

    items = collect(processed, untrimmed)
    if not items:
        print(f'  {unit.slug}: no page images found')
        return

    out = os.path.join(review, 'review.html')
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write(PAGE % {'unit': unit.slug,
                        'items': json.dumps(items, ensure_ascii=False)})

    lefts = sum(1 for it in items if it['left'] > 0)
    rights = sum(1 for it in items if it['right'] < 1)
    both = sum(1 for it in items if it['left'] > 0 and it['right'] < 1)
    already = sum(1 for it in items if it['trimmed'])
    print()
    print(f'  {len(items)} page(s); a left edge on {lefts}, a right edge on {rights}, '
          f'both on {both}' + (f'; {already} already trimmed' if already else ''))
    print(f'  wrote {out}')
    print()
    print('  Both sides are set on the one page: grab the nearer line, or pick with')
    print('  l and r. Every page is saved: at the lines you move, or at the detected')
    print('  edges if you leave them. Press x to keep a page whole.')
    print(f'    python pipeline/intake/apply_trims.py --unit {unit.slug} \\')
    print('        --trims processed/_trim_review/trims.json')


if __name__ == '__main__':
    main()
