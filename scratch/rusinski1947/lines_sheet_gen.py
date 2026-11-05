# -*- coding: utf-8 -*-
"""Build LINES_SHEET.html: the editor draws horizontal row-separator
lines over the table-page scans; the Collect button outputs the line
y-coordinates (in original scan pixels) as JSON to paste back."""
import base64, io, json, os, sys
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
HERE = (r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba'
        r'\rusinski1947\literature\rusinski1947')

PAGES = [('0081', 'p. 66 — Tabela V')] + \
    [(f'{i:04d}', 'ANEKS I — sheet %s (p. %d)' % (f'{i:04d}', i - 15))
     for i in range(139, 160)]

pages = []
for n, label in PAGES:
    with open(os.path.join(SRC, f'tom5_{n}.tif'), 'rb') as fh:
        im = Image.open(io.BytesIO(fh.read()))
    im.load()
    W, H = im.size
    scale = 1500 / W
    im2 = im.convert('RGB').resize((1500, int(H * scale)), Image.LANCZOS)
    buf = io.BytesIO()
    im2.save(buf, 'JPEG', quality=82)
    uri = 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()
    pages.append({'scan': n, 'label': label, 'w': 1500,
                  'h': int(H * scale), 'ow': W, 'oh': H, 'uri': uri})
    print(n, im2.size)

tpl = '''<!DOCTYPE html>
<html lang="pl"><head><meta charset="utf-8">
<title>Row separators — Rusiński 1947</title>
<style>
 body { font: 15px/1.5 Georgia, serif; max-width: 64em; margin: 1.5em auto;
        padding: 0 1em; background: #faf8f4; color: #222; }
 h1 { font-size: 1.4em; border-bottom: 2px solid #8b6f47; }
 .page { background: #fff; border: 1px solid #d8c9b4; border-radius: 6px;
         margin: 1.5em 0; padding: .8em; }
 .page h2 { font-size: 1em; font-family: sans-serif; margin: .2em 0 .6em; }
 .wrap { position: relative; }
 .wrap img { display: block; width: 100%; }
 canvas { position: absolute; inset: 0; cursor: crosshair; }
 .collect { position: sticky; bottom: 0; background: #5a4632; color: #fff;
            padding: .7em 1em; border-radius: 6px 6px 0 0; }
 #out { width: 100%; height: 7em; margin-top: .5em; font-family: monospace;
        font-size: .78em; }
 button { font-size: 1em; padding: .35em .9em; cursor: pointer; }
 .hint { font-family: sans-serif; font-size: .85em; color: #665; }
</style></head><body>
<h1>Row separators — draw the horizontal lines</h1>
<p class="hint">For each sheet: drag across a row separator (between two
rows) to draw a red line; drag again anywhere on the line to remove it.
The lines snap to where you draw - exactness is not needed, ±10 px is
fine. When done, press <b>Collect lines</b> and paste the output back
into the chat. The y-values are original-scan pixels.</p>
@@PAGES@@
<div class="collect"><button onclick="collect()">Collect lines</button>
<textarea id="out" placeholder="…the JSON appears here"></textarea></div>
<script>
const PAGES = @@DATA@@;
const saved = JSON.parse(localStorage.getItem('row_lines') || '{}');
for (const p of PAGES) {
  const wrap = document.getElementById('w_' + p.scan);
  const img = wrap.querySelector('img');
  const cv = wrap.querySelector('canvas');
  cv.width = p.w; cv.height = p.h;
  let lines = saved[p.scan] || [];
  function draw() {
    const g = cv.getContext('2d');
    g.clearRect(0, 0, cv.width, cv.height);
    g.strokeStyle = 'red'; g.lineWidth = 2;
    for (const y of lines) {
      g.beginPath(); g.moveTo(0, y); g.lineTo(cv.width, y); g.stroke();
    }
  }
  let down = null;
  cv.addEventListener('mousedown', e => {
    const r = cv.getBoundingClientRect();
    down = Math.round((e.clientY - r.top) * cv.height / r.height);
  });
  cv.addEventListener('mouseup', e => {
    if (down === null) return;
    const r = cv.getBoundingClientRect();
    const y = Math.round((e.clientY - r.top) * cv.height / r.height);
    if (Math.abs(y - down) < 8) {
      const i = lines.findIndex(v => Math.abs(v - y) < 12);
      if (i >= 0) lines.splice(i, 1); else lines.push(y);
    } else {
      lines.push(Math.round((y + down) / 2));
    }
    down = null; saved[p.scan] = lines; draw();
    localStorage.setItem('row_lines', JSON.stringify(saved));
  });
  draw();
}
function collect() {
  const out = {};
  for (const p of PAGES) {
    const lines = saved[p.scan] || [];
    if (lines.length)
      out[p.scan] = lines.map(y =>
        Math.round(y * p.oh / p.h)).sort((a, b) => a - b);
  }
  document.getElementById('out').value = JSON.stringify(out);
  document.getElementById('out').select();
}
</script></body></html>'''

body = []
for p in pages:
    body.append(
        '<div class="page"><h2>%s (scan %s)</h2>'
        '<div class="wrap" id="w_%s"><img src="%s">'
        '<canvas></canvas></div></div>'
        % (p['label'], p['scan'], p['scan'], p['uri']))
html = tpl.replace('@@PAGES@@', '\n'.join(body)) \
          .replace('@@DATA@@', json.dumps(
              [{k: v for k, v in p.items() if k != 'uri'} for p in pages]))
with open(os.path.join(HERE, 'LINES_SHEET.html'), 'w',
          encoding='utf-8', newline='\n') as fh:
    fh.write(html)
print('LINES_SHEET.html:', os.path.getsize(
    os.path.join(HERE, 'LINES_SHEET.html')) // 1024, 'kB,',
    len(pages), 'pages')
