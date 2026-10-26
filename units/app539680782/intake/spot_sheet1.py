# -*- coding: utf-8 -*-
"""The spot sheet for APP 53/968/0/-/782: "The contract of 1820 - lines and
the foot of the second page".

The transcription is the editor's own and is not re-read. What is asked here
is the LINE DIVISION - the editor's file carried the text by paragraph, and
the lines were laid out in session against the two images - at the few places
the session could not settle, plus one question of content: the pencil
inscription at the foot of the second page, which the transcription does not
carry. Each row is one region of a photographed page, cut with margins so no
line is lost, with the draft line division beneath it. The editor reads the
strip and either confirms the draft or types what the page says - line by
line, in the "Something else" box. Answers go to
review/app539680782/lines_answers.json.

    python units/app539680782/intake/spot_sheet1.py          # serve
    python units/app539680782/intake/spot_sheet1.py --read   # print answers

The pictures are cut from the unit's raw images by build_strips() into
review/app539680782/spot_img/, so the sheet is self-contained.
"""
import argparse
import http.server
import json
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
import unitlib

UNIT = unitlib.one_unit('app539680782')
REV = unitlib.review_dir(UNIT.slug)
IMGDIR = os.path.join(REV, 'spot_img')
os.makedirs(IMGDIR, exist_ok=True)
STORE = os.path.join(REV, 'lines_answers.json')

SHEETS = {2: '0002', 3: '0003'}

# One row per region whose line division the session could not settle, or
# that carries the question of the pencil inscription. The rect is the region
# of the page in its own pixels (x0, y0, x1, y1), cut with generous margins.
# `lines` is the draft division of the region (as the transcription has it).
ROWS = [
    ('p2_open_end', 2, (0, 850, 2597, 1200),
     ['so verkontraktieren wir uns mit',
      'demselben und stellen ihm selbige Vo-',
      'cation aus.'],
     'The last lines of the opening paragraph. Does the first of them end '
     'at "mit" (as drafted) or already at "mit demselben"?'),
    ('p2_item3', 2, (0, 1770, 2597, 2120),
     ['3. Bekommt er von der Gemeine fünf Viertel',
      'Korn und ein halb Viertel aus Saat,',
      'daß muß er beim Abzuge lasten.'],
     'Term 3, drafted as three lines. Confirm the two breaks, or type the '
     'lines as the page divides them.'),
    ('p2_item9', 2, (0, 2760, 2597, 3100),
     ['9te. Ale hohe Pfest-Tage als Weinachten',
      'Ostern Pfingsten bekommt er von einem',
      'jeden Wirt ein Opfertorium vom Wirthe 6 gl.'],
     'Term 9, drafted as three lines, opening "9te." (ruled 2026-10-25). '
     'Confirm the breaks.'),
    ('p2_item10', 2, (0, 3060, 2597, 3330),
     ['10. Erhält derselbe einen Neujahrsumgang und grünen',
      'Donnerstag Neujahr 6 gr. pohl. gründon 3 gr. pohl'],
     'Term 10, drafted as two lines. Is that where the page breaks?'),
    ('p2_closing', 2, (0, 3280, 2597, 3986),
     ['Auf diesen Contract veroblogiert sich der Schullehrer',
      'Samuel Adolph sein Amt als ein rechtschaffener',
      'Mann fortzusetzen. Die Sontags',
      'Schule so wie'],
     'The closing sentence, drafted as four lines. Confirm the breaks, or '
     'type the lines as the page divides them.'),
    ('p3_unter', 3, (0, 780, 2600, 950),
     ['worauf wir uns Eigen-händig Unter-schrieben.'],
     'The line that ends the board\'s sentence: all of it on one line, '
     'with "Eigen-händig" and "Unter-schrieben" written with their '
     'hyphens as drafted?'),
    ('p3_foot', 3, (0, 3560, 2600, 3996),
     [],
     'The foot of the second page carries writing the transcription does '
     'not have (it reads like an inscription in pencil - the document\'s '
     'title?). What does it say, and should it be transcribed as a heading '
     'line (as the folder inscriptions of 53/968/0/-/783 are) or left out?'),
]

ZOOM = 2.0          # every strip is shown at twice the page's size
SHEET_W = 1500      # the whole-page view is scaled to this width


def raw_path(n):
    return os.path.join(UNIT.raw_dir, f'Image{n:05d}.jpg')


def build_strips():
    """Cut every row's picture from the unit's raw images."""
    cache = {}
    for key, n, (x0, y0, x1, y1), lines, note in ROWS:
        dst = os.path.join(IMGDIR, key + '.jpg')
        if os.path.isfile(dst):
            continue
        if n not in cache:
            src = raw_path(n)
            if not os.path.isfile(src):
                raise SystemExit(f'{UNIT.slug}: raw image not found: {src}')
            cache[n] = Image.open(src)
        im = cache[n]
        w, h = im.size
        box = (max(0, x0), max(0, y0), min(w, x1), min(h, y1))
        crop = im.crop(box)
        crop = crop.resize((int(crop.width * ZOOM), int(crop.height * ZOOM)),
                           Image.LANCZOS)
        crop.save(dst, quality=90)
    # the whole pages, scaled down for quick loading
    for n, tag in SHEETS.items():
        dst = os.path.join(IMGDIR, f'sheet_{tag}.jpg')
        if os.path.isfile(dst):
            continue
        if n not in cache:
            src = raw_path(n)
            if not os.path.isfile(src):
                raise SystemExit(f'{UNIT.slug}: raw image not found: {src}')
            cache[n] = Image.open(src)
        im = cache[n]
        scale = SHEET_W / im.width
        small = im.resize((SHEET_W, int(im.height * scale)), Image.LANCZOS)
        small.save(dst, quality=88)


def page_html():
    rows = []
    for i, (key, n, rect, lines, note) in enumerate(ROWS, 1):
        tag = SHEETS[n]
        ls = '<br>'.join(lines) or '<i>(nothing read)</i>'
        rows.append(
            f"<div class=row data-key='{key}'>"
            f"<div><b>{i}.</b> <span class=k>{key}</span> "
            f"<a href='/spot_img/sheet_{tag}.jpg' target='_blank'>"
            f"whole page {tag}</a></div>"
            f"<a href='/spot_img/{key}.jpg' target='_blank'>"
            f"<img src='/spot_img/{key}.jpg'></a>"
            f"<div class=lines>{ls}</div>"
            f"<small>{note}</small>"
            f"<div class=btns>"
            f"<button data-v='as_drafted'>As drafted</button>"
            f"<button data-v='__other__'>Something else</button>"
            f"<button data-v='__unsure__'>Can't tell</button>"
            f"<input class=other placeholder='What the page says' hidden>"
            f"<input class=note placeholder='Note (optional)'>"
            f"</div></div>")
    return f"""<!DOCTYPE html><html><head><meta charset=utf-8>
<title>The contract of 1820 - lines and the foot of the second page - APP 53/968/0/-/782</title>
<style>
body{{font:15px/1.45 Georgia,serif;max-width:880px;margin:24px auto;padding:0 12px}}
h1{{font-size:20px}} .row{{border:1px solid #bbb;border-radius:6px;padding:10px 14px;margin:14px 0}}
.row img{{max-width:100%;border:1px solid #ccc;margin:6px 0}}
.q{{background:#ffe9a8;font-weight:bold}}
.lines{{font:15px/1.5 Georgia,serif;margin:6px 0}}
.k{{color:#888;font:12px monospace}}
button{{font:14px Georgia,serif;padding:3px 10px;margin-right:6px;cursor:pointer}}
.row.active{{border-color:#c60}}
input{{font:14px Georgia,serif;padding:3px 6px;margin-right:6px;width:40%}}
small{{color:#555}}
</style></head><body>
<h1>The contract of 1820 &mdash; lines and the foot of the second page &mdash; APP 53/968/0/-/782</h1>
<p>Your transcription is not being re-read. What is asked is where the
manuscript's lines break, at the few places the session could not settle,
and what to do with the pencil writing at the foot of the second page.
Each row shows the region with the draft line division beneath it; read the
strip and either take the draft or type what the page says &mdash; line by
line, in the "Something else" box. "Whole page" above every picture opens
the page in full, smaller.</p>
<div id=rows>{''.join(rows)}</div>
<p>When you have worked down the page, the answers are saved as you go.</p>
<script>
var ANSWERS = {json.dumps(ANSWERS, ensure_ascii=False)};
document.querySelectorAll('.row').forEach(function(r) {{
  var key = r.dataset.key;
  var saved = ANSWERS[key] || {{}};
  var btns = r.querySelectorAll('button');
  var other = r.querySelector('.other'), note = r.querySelector('.note');
  function set(v) {{
    r.dataset.v = v;
    btns.forEach(function(b) {{ b.style.background =
      (b.dataset.v === v ? '#ffd' : ''); }});
    other.hidden = (v !== '__other__');
  }}
  btns.forEach(function(b) {{ b.onclick = function() {{ set(b.dataset.v);
    send(); }}; }});
  other.oninput = note.oninput = function() {{ send(); }};
  if (saved.reading) set(saved.reading);
  if (saved.other) {{ other.value = saved.other; other.hidden = false;
    r.dataset.v = '__other__';
    btns.forEach(function(b) {{ b.style.background =
      (b.dataset.v === '__other__' ? '#ffd' : ''); }}); }}
  if (saved.note) note.value = saved.note;
  function send() {{
    fetch('/', {{ method: 'POST', headers: {{'Content-Type': 'application/json'}},
      body: JSON.stringify({{ key: key, reading: r.dataset.v,
        other: other.value, note: note.value }}) }});
  }}
}});
</script></body></html"""


def read_html():
    rows = []
    for i, (key, n, rect, lines, note) in enumerate(ROWS, 1):
        a = ANSWERS.get(key, {})
        rows.append(f"<p><b>{i}. {key}</b> &mdash; {a.get('reading', '(no answer)')}"
                    f"{(' &mdash; ' + a['other']) if a.get('other') else ''}"
                    f"{(' &mdash; note: ' + a['note']) if a.get('note') else ''}</p>")
    return ('<html><meta charset=utf-8><body><h1>Answers, lines</h1>'
            + '\n'.join(rows) + '</body></html>')


ANSWERS = {}
if os.path.isfile(STORE):
    with open(STORE, encoding='utf-8') as f:
        ANSWERS = json.load(f)

build_strips()


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=REV, **kw)

    def log_message(self, *_):
        pass

    def do_GET(self):
        if self.path == '/':
            body = page_html().encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif self.path == '/answers':
            body = read_html().encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            super().do_GET()

    def do_POST(self):
        d = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        ANSWERS[d['key']] = {'reading': d.get('reading', ''),
                             'other': d.get('other', ''),
                             'note': d.get('note', '')}
        with open(STORE, 'w', encoding='utf-8') as f:
            json.dump(ANSWERS, f, ensure_ascii=False, indent=1)
        self.send_response(204)
        self.end_headers()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--read', action='store_true')
    ap.add_argument('--port', type=int, default=4107)
    a = ap.parse_args()
    if a.read:
        print(read_html())
    else:
        http.server.ThreadingHTTPServer(('127.0.0.1', a.port), H).serve_forever()


if __name__ == '__main__':
    main()
