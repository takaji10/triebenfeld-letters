# -*- coding: utf-8 -*-
"""
Build a page for straightening pages, from the slope of their own writing.

    python pipeline/intake/review_skew.py --unit oe1bu14525

A leaf photographed a degree or two off square has writing that runs downhill,
and every later stage inherits it: the trim edge is no longer vertical, so a
straight cut either clips the text or leaves a wedge. Straighten first, trim
second.

The angle is read off the writing, not off the paper edge - the edge is the one
thing on these scans that is often genuinely crooked, torn or absent, while the
lines of text were written level. Shearing the ink by a trial angle and scoring
how sharply it stacks into rows (the classic projection profile: rows are
sharpest when the lines are horizontal) finds that angle without needing to
detect a single line.

Grab the sheet anywhere and turn it, as you would a sheet of paper under a
finger; the marked corners are the longest lever and so the finest control.

Every page is written to the JSON: at the angle you set, or at the detected
angle if you leave it alone. Leaving a page untouched means you agree with the
proposed rotation - so page through all of them. Press `x` to record a page as
one to leave alone.

    python pipeline/intake/apply_skew.py --unit oe1bu14525 \
        --angles processed/_skew_review/skew.json

Positive is counter-clockwise, the same sense as PIL's rotate(), so the number
in the JSON is the rotation that gets applied.
"""
import argparse
import io
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
import unitlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

W = 500                # analysis width; enough for a baseline to be a line
MARGIN_X = 0.10        # ignore this much of each side: page edges, not writing
MARGIN_Y = 0.08        # and of the head and tail, which are ragged
INK_DROP = 35          # a pixel this much darker than the page counts as ink
MAX_POINTS = 12000     # ink points kept; more than this buys no accuracy
COARSE = 5.0           # search +/- this many degrees
COARSE_STEP = 0.5
FINE_STEP = 0.05
FLAT = 0.05            # below this, call it straight and leave it alone


def ink_points(path):
    """Ink pixels of the writing block, as (x, y) on the analysis-size image.

    Returns (points, width, height). The page brightness is the median of the
    sampled pixels, so a grey scan and a white one are thresholded alike.
    """
    from PIL import Image
    with Image.open(path) as im:
        g = im.convert('L')
        w0, h0 = g.size
        s = g.resize((W, max(1, round(h0 * W / w0))))
    px = s.load()
    w, h = s.size
    x0, x1 = int(w * MARGIN_X), int(w * (1 - MARGIN_X))
    y0, y1 = int(h * MARGIN_Y), int(h * (1 - MARGIN_Y))
    if x1 - x0 < 8 or y1 - y0 < 8:
        return [], w, h

    vals = [px[x, y] for y in range(y0, y1, 3) for x in range(x0, x1, 3)]
    vals.sort()
    page = vals[len(vals) // 2] if vals else 200
    cut = page - INK_DROP

    pts = [(x, y) for y in range(y0, y1) for x in range(x0, x1) if px[x, y] < cut]
    if len(pts) > MAX_POINTS:
        step = len(pts) // MAX_POINTS + 1
        pts = pts[::step]
    return pts, w, h


def score(pts, xc, tan):
    """How sharply the ink stacks into rows once sheared by this angle.

    Sum of the squared row counts - large when the ink is concentrated in a few
    rows (lines of writing lying flat) and small when it is spread evenly.
    """
    rows = {}
    for x, y in pts:
        r = int(y - (x - xc) * tan)
        rows[r] = rows.get(r, 0) + 1
    return sum(n * n for n in rows.values())


def detect(path):
    """(angle in degrees, confidence 0-1). Positive angle = counter-clockwise."""
    pts, w, h = ink_points(path)
    if len(pts) < 200:
        return 0.0, 0.0
    xc = w / 2

    def best(lo, hi, step):
        a, s = lo, -1
        n = int(round((hi - lo) / step))
        for i in range(n + 1):
            t = lo + i * step
            v = score(pts, xc, math.tan(math.radians(t)))
            if v > s:
                a, s = t, v
        return a, s

    coarse, _ = best(-COARSE, COARSE, COARSE_STEP)
    angle, peak = best(coarse - COARSE_STEP, coarse + COARSE_STEP, FINE_STEP)

    # Confidence: how much better the best angle stacks than the flat one. A
    # page of solid writing peaks hard; a near-blank page or a diagram barely
    # peaks at all, and its angle is not worth trusting.
    flat = score(pts, xc, 0.0)
    conf = 0.0 if peak <= 0 else max(0.0, min(1.0, (peak - flat) / peak * 8))
    if abs(angle) < FLAT:
        angle = 0.0
    return round(angle, 2), round(conf, 3)


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
        angle, conf = detect(path)
        items.append({'file': fn, 'src': '../' + fn, 'w': w, 'h': h,
                      'guess': angle, 'conf': conf,
                      'done': os.path.isfile(os.path.join(done_dir, fn))})
        print(f'  [{n}/{len(names)}] {fn}  {angle:+.2f} deg  conf {conf:.2f}')
    return items


PAGE = """<!doctype html>
<meta charset="utf-8">
<title>Skew review - %(unit)s</title>
<style>
  :root { color-scheme: light dark; }
  body { margin: 0; font: 14px/1.45 system-ui, sans-serif; background: #1a1a1a; color: #eee; }
  header { position: sticky; top: 0; z-index: 5; display: flex; gap: .9rem;
           align-items: center; flex-wrap: wrap;
           padding: .5rem .8rem; background: #111; border-bottom: 1px solid #333; }
  .muted { color: #999; }
  .moved { color: #7ec87e; }
  .weak { color: #e0a030; }
  button { font: inherit; padding: .3rem .7rem; background: #2a2a2a; color: #eee;
           border: 1px solid #444; border-radius: 4px; cursor: pointer; }
  button:hover { background: #333; }
  button.primary { background: #2d5a2d; border-color: #3d7a3d; }
  #stage { position: relative; margin: 0 auto; width: fit-content;
           overflow: hidden; touch-action: none; }
  #img { display: block; max-width: 100vw; max-height: calc(100vh - 96px);
         transform-origin: 50%% 50%%; cursor: grab; }
  #stage.turning #img { cursor: grabbing; }
  /* Grab anywhere to turn the sheet; the corners are marked because that is
     where the lever is longest and the turn finest. */
  .handle { position: absolute; width: 15px; height: 15px; margin: -8px;
            border: 2px solid rgba(255,32,32,.9); border-radius: 50%%;
            background: rgba(0,0,0,.35); cursor: grab; }
  #stage.turning .handle { cursor: grabbing; }
  .h-tl { left: 0; top: 0; } .h-tr { right: 0; top: 0; margin-right: -7px; }
  .h-bl { left: 0; bottom: 0; margin-bottom: -7px; }
  .h-br { right: 0; bottom: 0; margin-right: -7px; margin-bottom: -7px; }
  /* Horizontal rules to read the writing against: the line is straight when a
     run of text sits parallel to them. */
  #rules { position: absolute; inset: 0; pointer-events: none;
           background-image: repeating-linear-gradient(
             to bottom, rgba(255,32,32,.55) 0 1px, transparent 1px 48px); }
  #out { width: 100%%; height: 9rem; font: 12px/1.4 ui-monospace, monospace;
         background: #111; color: #ddd; border: 1px solid #333; display: none; }
  kbd { background: #333; border-radius: 3px; padding: 0 .3em; }
</style>

<header>
  <button id="prev">&larr;</button>
  <b id="pos"></b>
  <button id="next">&rarr;</button>
  <span id="name" class="muted"></span>
  <span>angle <b id="ang"></b></span>
  <span id="was" class="muted"></span>
  <span id="chg" class="moved"></span>
  <span style="flex:1"></span>
  <button id="rules-off">Hide rules</button>
  <button id="none">No rotation</button>
  <button id="reset">Reset</button>
  <button id="save" class="primary">Save skew.json</button>
  <button id="copy">Copy</button>
  <span class="muted"><kbd>&larr;</kbd><kbd>&rarr;</kbd> page,
    <kbd>,</kbd><kbd>.</kbd> turn 0.05&deg;, <kbd>shift</kbd> x10,
    <kbd>x</kbd> leave alone, <kbd>r</kbd> rules;
    grab a corner and turn</span>
</header>

<div id="stage">
  <img id="img" alt="">
  <div id="rules"></div>
  <div class="handle h-tl"></div><div class="handle h-tr"></div>
  <div class="handle h-bl"></div><div class="handle h-br"></div>
</div>
<textarea id="out" spellcheck="false"></textarea>

<script>
const ITEMS = %(items)s;
const set = {};                // your overrides; everything else saves at its guess
const MIN_R = 45;              // nearer the centre than this there is no leverage
let i = 0, shown = 0;

const img = document.getElementById('img');
const stage = document.getElementById('stage');
const rules = document.getElementById('rules');
const at = () => ITEMS[i];

function show() {
  const it = at();
  img.src = it.src;
  document.getElementById('name').textContent = it.file + (it.done ? ' (rotated)' : '');
  document.getElementById('pos').textContent = (i + 1) + ' / ' + ITEMS.length;
  const was = document.getElementById('was');
  was.textContent = 'detected ' + it.guess.toFixed(2) + '\\u00b0 conf ' + it.conf.toFixed(2);
  was.className = it.conf < 0.25 ? 'weak' : 'muted';
  draw(set[it.file] !== undefined ? set[it.file] : it.guess, false);
}

function draw(deg, byUser) {
  deg = Math.max(-15, Math.min(15, deg));
  shown = Math.round(deg * 100) / 100;
  // the JSON is a counter-clockwise rotation; CSS turns the other way
  img.style.transform = 'rotate(' + (-shown) + 'deg)';
  document.getElementById('ang').textContent = shown.toFixed(2) + '\\u00b0';
  if (byUser) set[at().file] = shown;
  const n = Object.keys(set).length;
  document.getElementById('chg').textContent =
    n + ' adjusted; all ' + ITEMS.length + ' will be saved';
}

// The sheet turns with the pointer: where you grabbed it stays under the
// pointer, the way a sheet of paper turns under a finger. Grabbing at a corner
// gives the longest lever, so a pixel of travel there is under a tenth of a
// degree.
let dragging = false, bear0 = 0, a0 = 0;

function grip(e) {
  const r = img.getBoundingClientRect();       // axis-aligned, but concentric
  const dx = e.clientX - (r.left + r.width / 2);
  const dy = e.clientY - (r.top + r.height / 2);
  return {deg: Math.atan2(dy, dx) * 180 / Math.PI, r: Math.hypot(dx, dy)};
}

stage.addEventListener('pointerdown', e => {
  const g = grip(e);
  if (g.r < MIN_R) return;                     // a twitch at the pivot is not a turn
  dragging = true; bear0 = g.deg; a0 = shown;
  stage.setPointerCapture(e.pointerId);
  stage.classList.add('turning');
  e.preventDefault();
});
stage.addEventListener('pointermove', e => {
  if (!dragging) return;
  let d = grip(e).deg - bear0;
  while (d > 180) d -= 360;
  while (d < -180) d += 360;
  draw(a0 - d, true);                          // screen y runs down, so this flips
});
stage.addEventListener('pointerup', () => {
  dragging = false; stage.classList.remove('turning');
});
img.addEventListener('load', () => draw(set[at().file] ?? at().guess, false));

function step(d) { i = (i + d + ITEMS.length) %% ITEMS.length; show(); }
document.getElementById('next').onclick = () => step(1);
document.getElementById('prev').onclick = () => step(-1);
document.getElementById('reset').onclick = () => { delete set[at().file];
                                                   draw(at().guess, false); };
document.getElementById('none').onclick = () => draw(0, true);
document.getElementById('rules-off').onclick = () => {
  const off = rules.style.display === 'none';
  rules.style.display = off ? 'block' : 'none';
  document.getElementById('rules-off').textContent = off ? 'Hide rules' : 'Show rules';
};

document.addEventListener('keydown', e => {
  const d = (e.shiftKey ? 0.5 : 0.05);
  if (e.key === 'ArrowLeft')  { step(-1); e.preventDefault(); }
  if (e.key === 'ArrowRight') { step(1);  e.preventDefault(); }
  if (e.key === ',' || e.key === '<') { draw(shown - d, true); e.preventDefault(); }
  if (e.key === '.' || e.key === '>') { draw(shown + d, true); e.preventDefault(); }
  if (e.key === 'x') draw(0, true);
  if (e.key === 'r') document.getElementById('rules-off').click();
  if (e.key === 'n') step(1);
  if (e.key === 'p') step(-1);
});

const json = () => JSON.stringify(Object.fromEntries(
  ITEMS.map(it => [it.file, set[it.file] !== undefined ? set[it.file] : it.guess])),
  null, 1);

document.getElementById('save').onclick = () => {
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([json()], {type: 'application/json'}));
  a.download = 'skew.json';
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
    review = os.path.join(processed, '_skew_review')
    straight = os.path.join(processed, '_unrotated')
    if not os.path.isdir(processed):
        raise SystemExit(f'{unit.slug}: nothing cropped yet at {processed}')
    os.makedirs(review, exist_ok=True)

    items = collect(processed, straight)
    if not items:
        print(f'  {unit.slug}: no page images found')
        return

    out = os.path.join(review, 'review.html')
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write(PAGE % {'unit': unit.slug,
                        'items': json.dumps(items, ensure_ascii=False)})

    turned = [it for it in items if it['guess']]
    weak = [it for it in items if it['conf'] < 0.25]
    print()
    print(f'  {len(items)} page(s); {len(turned)} want turning'
          + (f', {len(weak)} read weakly - check those by eye' if weak else ''))
    print(f'  wrote {out}')
    print()
    print('  Drag to turn; the red rules are there to lay the writing against.')
    print('  Every page is saved: at the angle you set, or at the detected one if')
    print('  you leave it. Press x to leave a page as it is.')
    print(f'    python pipeline/intake/apply_skew.py --unit {unit.slug} \\')
    print('        --angles processed/_skew_review/skew.json')


if __name__ == '__main__':
    main()
