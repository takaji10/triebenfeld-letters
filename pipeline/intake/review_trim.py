# -*- coding: utf-8 -*-
"""
Build a page for trimming the edge off split pages.

    python pipeline/intake/review_trim.py --unit oe1bu14526

Sheets in a volume differ in size, so a page often carries a strip of the leaf
underneath along one edge. This lists every page image with a draggable line;
whichever side of the line is smaller is the strip to remove. Save trims.json,
then:

    python pipeline/intake/apply_trims.py --unit oe1bu14526 \
        --trims processed/_trim_review/trims.json

One edge per pass, which is usually all a page needs. If a page needs both,
run the tool again afterwards: it lists the trimmed image, so the second pass
takes the other side.

Only pages whose line you actually move are written to the JSON. Pages already
trimmed show where their edge now is, so a trim can be checked or taken further.
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

    left = 0.0
    for x in range(band, 2, -1):
        if abs(sm[x] - sm[x - 3]) >= STEP and sm[x - 3] < page - STEP // 2:
            left = x / w
            break
    right = 1.0
    for x in range(w - band, w - 3):
        if abs(sm[x] - sm[x + 3]) >= STEP and sm[x + 3] < page - STEP // 2:
            right = x / w
            break
    return round(left, 4), round(right, 4)


def collect(processed, done_dir):
    from PIL import Image
    items = []
    for fn in sorted(os.listdir(processed)):
        if not fn.lower().endswith('.jpg') or fn == 'manifest.json':
            continue
        path = os.path.join(processed, fn)
        if not os.path.isfile(path):
            continue
        with Image.open(path) as im:
            w, h = im.size
        left, right = edges(path)
        # the suggestion is whichever side has more to lose
        if (1 - right) > left:
            guess, side = right, 'right'
        elif left > 0:
            guess, side = left, 'left'
        else:
            guess, side = 1.0, 'none'
        items.append({'file': fn, 'src': '../' + fn, 'w': w, 'h': h,
                      'guess': guess, 'side': side,
                      'trimmed': os.path.isfile(os.path.join(done_dir, fn))})
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
  #stage { position: relative; margin: 0 auto; width: fit-content; }
  #img { display: block; max-width: 100vw; max-height: calc(100vh - 92px); }
  #cut { position: absolute; top: 0; bottom: 0; background: rgba(255,32,32,.28);
         pointer-events: none; }
  #line { position: absolute; top: 0; bottom: 0; width: 2px; background: #ff2020; }
  #line::after { content: ''; position: absolute; left: -14px; right: -14px;
                 top: 0; bottom: 0; cursor: ew-resize; }
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
  <button id="none">No trim</button>
  <button id="save" class="primary">Save trims.json</button>
  <button id="copy">Copy</button>
  <span class="muted"><kbd>&larr;</kbd><kbd>&rarr;</kbd> page,
    <kbd>,</kbd><kbd>.</kbd> nudge, <kbd>shift</kbd> x10,
    <kbd>x</kbd> no trim; shaded side is removed</span>
</header>

<div id="stage">
  <img id="img" alt="">
  <div id="cut"></div>
  <div id="line"></div>
</div>
<textarea id="out" spellcheck="false"></textarea>

<script>
const ITEMS = %(items)s;
const trims = {};             // only pages you actually set
let i = 0, shown = 1.0;

const img = document.getElementById('img');
const line = document.getElementById('line');
const cut = document.getElementById('cut');
const stage = document.getElementById('stage');
const at = () => ITEMS[i];

function show() {
  const it = at();
  img.src = it.src;
  document.getElementById('name').textContent =
    it.file + (it.trimmed ? ' (already trimmed)' : '');
  document.getElementById('pos').textContent = (i + 1) + ' / ' + ITEMS.length;
  draw(trims[it.file] !== undefined ? trims[it.file] : it.guess, false);
}

function draw(frac, byUser) {
  frac = Math.max(0, Math.min(1, frac));
  shown = frac;
  const w = img.clientWidth || 1;
  line.style.left = (frac * w) + 'px';
  // the smaller side is what goes
  const left = frac < 0.5;
  cut.style.left  = left ? '0px' : (frac * w) + 'px';
  cut.style.width = (left ? frac * w : (1 - frac) * w) + 'px';
  const px = Math.round((left ? frac : 1 - frac) * at().w);
  document.getElementById('cutinfo').textContent =
    (px < 2) ? 'no trim' : ('cut ' + (left ? 'left' : 'right') + ' ' + px + 'px');
  if (byUser) { if (px < 2) delete trims[at().file]; else trims[at().file] = frac; }
  const n = Object.keys(trims).length;
  document.getElementById('chg').textContent = n ? n + ' set' : '';
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
img.addEventListener('load', () => draw(trims[at().file] ?? at().guess, false));
window.addEventListener('resize', () => draw(shown, false));

function step(d) { i = (i + d + ITEMS.length) %% ITEMS.length; show(); }
document.getElementById('next').onclick = () => step(1);
document.getElementById('prev').onclick = () => step(-1);
document.getElementById('none').onclick = () => { delete trims[at().file]; draw(1.0, false); };

document.addEventListener('keydown', e => {
  const px = e.shiftKey ? 10 : 1;
  if (e.key === 'ArrowLeft')  { step(-1); e.preventDefault(); }
  if (e.key === 'ArrowRight') { step(1);  e.preventDefault(); }
  if (e.key === ',' || e.key === '<') { draw((line.offsetLeft - px) / img.clientWidth, true); e.preventDefault(); }
  if (e.key === '.' || e.key === '>') { draw((line.offsetLeft + px) / img.clientWidth, true); e.preventDefault(); }
  if (e.key === 'x') { delete trims[at().file]; draw(1.0, false); }
  if (e.key === 'n') step(1);
  if (e.key === 'p') step(-1);
});

const json = () => JSON.stringify(trims, null, 1);
document.getElementById('save').onclick = () => {
  if (!Object.keys(trims).length) { alert('Nothing set yet.'); return; }
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

    sug = sum(1 for it in items if it['side'] != 'none')
    already = sum(1 for it in items if it['trimmed'])
    print(f'  {len(items)} page(s); an edge was detected on {sug}'
          + (f'; {already} already trimmed' if already else ''))
    print(f'  wrote {out}')
    print()
    print('  The shaded side is what gets removed. Only pages you set are saved.')
    print(f'    python pipeline/intake/apply_trims.py --unit {unit.slug} \\')
    print('        --trims processed/_trim_review/trims.json')


if __name__ == '__main__':
    main()
