# -*- coding: utf-8 -*-
"""
Build a page for trimming the head and the tail off pages.

    python pipeline/intake/review_headtail.py --unit oe1bu14525

review_trim.py takes one vertical edge per pass, because a page usually carries
its neighbour's strip down one side and that is all. The head and the tail are
different: a leaf shorter than the one beneath it shows a band at BOTH ends, and
they are independent of each other, so this page carries two lines at once and
writes both.

The edge is found the same way review_trim.py finds a side: a step in the median
brightness of a row, which is tiny across the page and tens of levels where the
paper ends. The median across the row ignores the writing, and the outer eighth
of each side is skipped because a rotation wedge sits in the corners.

    python pipeline/intake/apply_headtail.py --unit oe1bu14525 \
        --cuts processed/_headtail_review/headtail.json

The JSON is {page: [top, bottom]} as fractions of the height: everything above
top and below bottom is removed, so [0, 1] means leave the page alone. Every
page is written, at the lines you set or at the detected ones you left - so page
through all of them, and press `x` on any page that should keep its full height.
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

H = 320                # analysis height
BAND = 0.28            # an edge is looked for within this much of each end
SIDE = 0.125           # ignore this much of each side: rotation wedges live there
STEP = 12              # brightness change that counts as a paper edge
SMOOTH = 2


def edges(path):
    """(top, bottom) as fractions of the height: where the top leaf begins and ends."""
    from PIL import Image
    with Image.open(path) as im:
        g = im.convert('L')
        w0, h0 = g.size
        s = g.resize((max(1, round(w0 * H / h0)), H))
        px = s.load()
        w, h = s.size
        x0, x1 = int(w * SIDE), max(int(w * SIDE) + 1, int(w * (1 - SIDE)))
        med = []
        for y in range(h):
            vals = sorted(px[x, y] for x in range(x0, x1))
            med.append(vals[len(vals) // 2])
    sm = []
    for y in range(h):
        lo, hi = max(0, y - SMOOTH), min(h, y + SMOOTH + 1)
        sm.append(sum(med[lo:hi]) // (hi - lo))

    band = int(h * BAND)
    body = sorted(sm[band:h - band])
    page = body[len(body) // 2] if body else 200

    # Walk in from the outside and stop at the first step, rather than out from
    # the inside and stop at the last. The paper edge is the outermost step there
    # is; steps further in are the writing block or a shadow, and taking those
    # put a quarter of the page in the cut band on twenty-odd pages here. Read
    # from outside in, the same scans propose a median of about 1%. The failure
    # this way round is a thin dark line at the very edge stopping the scan
    # early, which under-trims - visible at a glance, and a second pass fixes it.
    top = 0.0
    for y in range(3, band):
        if abs(sm[y] - sm[y - 3]) >= STEP and sm[y - 3] < page - STEP // 2:
            top = y / h
            break
    bottom = 1.0
    for y in range(h - 4, h - band, -1):
        if abs(sm[y] - sm[y + 3]) >= STEP and sm[y + 3] < page - STEP // 2:
            bottom = y / h
            break
    return round(top, 4), round(bottom, 4)


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
        top, bottom = edges(path)
        items.append({'file': fn, 'src': '../' + fn, 'w': w, 'h': h,
                      'top': top, 'bottom': bottom,
                      'done': os.path.isfile(os.path.join(done_dir, fn))})
        print(f'  [{n}/{len(names)}] {fn}  head {round(top * h):4d}px  '
              f'tail {round((1 - bottom) * h):4d}px')
    return items


PAGE = """<!doctype html>
<meta charset="utf-8">
<title>Head/tail review - %(unit)s</title>
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
           cursor: ns-resize; touch-action: none; }
  #img { display: block; max-width: 100vw; max-height: calc(100vh - 96px); }
  .cut { position: absolute; left: 0; right: 0; background: rgba(255,32,32,.28);
         pointer-events: none; }
  .line { position: absolute; left: 0; right: 0; height: 2px; background: #ff2020;
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
  <button id="pick-top">Head</button>
  <button id="pick-bot">Tail</button>
  <button id="none">No trim</button>
  <button id="reset">Reset</button>
  <button id="save" class="primary">Save headtail.json</button>
  <button id="copy">Copy</button>
  <span class="muted"><kbd>&larr;</kbd><kbd>&rarr;</kbd> page,
    <kbd>t</kbd><kbd>b</kbd> head/tail, <kbd>,</kbd><kbd>.</kbd> nudge,
    <kbd>shift</kbd> x10, <kbd>x</kbd> no trim; shaded bands are removed</span>
</header>

<div id="stage">
  <img id="img" alt="">
  <div class="cut" id="cut-top"></div>
  <div class="cut" id="cut-bot"></div>
  <div class="line" id="line-top"></div>
  <div class="line" id="line-bot"></div>
</div>
<textarea id="out" spellcheck="false"></textarea>

<script>
const ITEMS = %(items)s;
const set = {};                // your overrides; everything else saves at its guess
const MIN_GAP = 0.05;          // the two lines may not cross or pinch the page shut
// NB: not `top` - window.top is non-configurable, and `let top` at script
// scope is a SyntaxError that stops the whole file from running.
let i = 0, head = 0, tail = 1, active = 'top';

const img = document.getElementById('img');
const stage = document.getElementById('stage');
const at = () => ITEMS[i];

function show() {
  const it = at();
  img.src = it.src;
  document.getElementById('name').textContent = it.file + (it.done ? ' (trimmed)' : '');
  document.getElementById('pos').textContent = (i + 1) + ' / ' + ITEMS.length;
  const s = set[it.file];
  head = s ? s[0] : it.top;
  tail = s ? s[1] : it.bottom;
  draw(false);
}

function draw(byUser) {
  const h = img.clientHeight || 1;
  document.getElementById('cut-top').style.height = (head * h) + 'px';
  document.getElementById('cut-top').style.top = '0px';
  document.getElementById('cut-bot').style.height = ((1 - tail) * h) + 'px';
  document.getElementById('cut-bot').style.bottom = '0px';
  document.getElementById('line-top').style.top = (head * h) + 'px';
  document.getElementById('line-bot').style.top = (tail * h) + 'px';
  document.getElementById('line-top').className = 'line' + (active === 'top' ? '' : ' idle');
  document.getElementById('line-bot').className = 'line' + (active === 'bot' ? '' : ' idle');

  const it = at();
  const tp = Math.round(head * it.h), bp = Math.round((1 - tail) * it.h);
  document.getElementById('cutinfo').textContent =
    (tp < 2 && bp < 2) ? 'no trim' : ('head ' + tp + 'px, tail ' + bp + 'px');
  document.getElementById('pick-top').className = active === 'top' ? 'on' : '';
  document.getElementById('pick-bot').className = active === 'bot' ? 'on' : '';
  if (byUser) set[it.file] = [round4(head), round4(tail)];
  const n = Object.keys(set).length;
  document.getElementById('chg').textContent =
    n + ' adjusted; all ' + ITEMS.length + ' will be saved';
}

const round4 = v => Math.round(v * 10000) / 10000;

function place(frac, which) {
  frac = Math.max(0, Math.min(1, frac));
  if (which === 'top') head = Math.min(frac, tail - MIN_GAP);
  else tail = Math.max(frac, head + MIN_GAP);
  active = which;
  draw(true);
}

// the line you grab is whichever is nearer where you pressed
function fromEvent(e, which) {
  const r = img.getBoundingClientRect();
  const frac = (e.clientY - r.top) / r.height;
  place(frac, which || (Math.abs(frac - head) <= Math.abs(frac - tail) ? 'top' : 'bot'));
}

let dragging = null;
stage.addEventListener('pointerdown', e => {
  const r = img.getBoundingClientRect();
  const frac = (e.clientY - r.top) / r.height;
  dragging = Math.abs(frac - head) <= Math.abs(frac - tail) ? 'top' : 'bot';
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
document.getElementById('pick-top').onclick = () => { active = 'top'; draw(false); };
document.getElementById('pick-bot').onclick = () => { active = 'bot'; draw(false); };
document.getElementById('none').onclick = () => { head = 0; tail = 1; draw(true); };
document.getElementById('reset').onclick = () => { delete set[at().file];
                                                   head = at().top; tail = at().bottom;
                                                   draw(false); };

document.addEventListener('keydown', e => {
  const h = img.clientHeight || 1;
  const d = (e.shiftKey ? 10 : 1) / h;
  if (e.key === 'ArrowLeft')  { step(-1); e.preventDefault(); }
  if (e.key === 'ArrowRight') { step(1);  e.preventDefault(); }
  if (e.key === 't') { active = 'top'; draw(false); }
  if (e.key === 'b') { active = 'bot'; draw(false); }
  if (e.key === ',' || e.key === '<') { place((active === 'top' ? head : tail) - d, active);
                                        e.preventDefault(); }
  if (e.key === '.' || e.key === '>') { place((active === 'top' ? head : tail) + d, active);
                                        e.preventDefault(); }
  if (e.key === 'x') { head = 0; tail = 1; draw(true); }
  if (e.key === 'n') step(1);
  if (e.key === 'p') step(-1);
});

const json = () => JSON.stringify(Object.fromEntries(ITEMS.map(it =>
  [it.file, set[it.file] !== undefined ? set[it.file] : [it.top, it.bottom]])), null, 1);

document.getElementById('save').onclick = () => {
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([json()], {type: 'application/json'}));
  a.download = 'headtail.json';
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
    review = os.path.join(processed, '_headtail_review')
    done = os.path.join(processed, '_pre_headtail')
    if not os.path.isdir(processed):
        raise SystemExit(f'{unit.slug}: nothing cropped yet at {processed}')
    os.makedirs(review, exist_ok=True)

    items = collect(processed, done)
    if not items:
        print(f'  {unit.slug}: no page images found')
        return

    out = os.path.join(review, 'review.html')
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write(PAGE % {'unit': unit.slug,
                        'items': json.dumps(items, ensure_ascii=False)})

    heads = sum(1 for it in items if it['top'] > 0)
    tails = sum(1 for it in items if it['bottom'] < 1)
    both = sum(1 for it in items if it['top'] > 0 and it['bottom'] < 1)
    print()
    print(f'  {len(items)} page(s); a head edge on {heads}, a tail edge on {tails}, '
          f'both on {both}')
    print(f'  wrote {out}')
    print()
    print('  Both bands are set on the one page: grab the nearer line, or pick with')
    print('  t and b. Every page is saved, at your lines or the detected ones.')
    print('  Press x to keep a page at full height.')
    print(f'    python pipeline/intake/apply_headtail.py --unit {unit.slug} \\')
    print('        --cuts processed/_headtail_review/headtail.json')


if __name__ == '__main__':
    main()
