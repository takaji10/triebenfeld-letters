# -*- coding: utf-8 -*-
"""The editor's spot sheet for I. HA GR, Rep. 7 C, Nr. 3067 as one
self-contained HTML file (2026-11-19, the editor: "Make a html spot sheet for
me"). Same eight rows as spot_sheet.py (imported from it); no server needed.

    python units/ihagrrep7cnr3067/intake/spot_sheet_html.py
      -> review/ihagrrep7cnr3067/spot_sheet.html

The pictures are embedded (a close crop and a taller view of the lines
around it). Answers stay in the browser (localStorage); "Copy answers" puts
them on the clipboard as the JSON query_answers.json holds, to paste back
into the chat. Answers are applied through build_pages.py (CORRECTIONS).
"""
import base64
import html
import io
import json
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from spot_sheet import ROWS, SRC, REV  # noqa: E402

UNIT = os.path.dirname(HERE)
OUT = os.path.join(REV, 'spot_sheet.html')

# q6's box cut the first letter of "dererjenigen": widened (2026-11-19).
BOX_FIX = {'q6': (0, 1060, 1800, 1290)}

DOC_NAME = {'1': "Goldbeck's promemoria", '2': "the King's note",
            '3': 'the list of the condemned'}


def b64(im, width):
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.convert('RGB').save(buf, 'JPEG', quality=82)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


def context(corpus, line, word):
    """The row's corpus line (1-based, as open_queries.csv gives it), with one
    line either side, the word marked."""
    bare = word.split('[')[0]
    out = []
    for j in (line - 2, line - 1, line):
        if 0 <= j < len(corpus) and not corpus[j].startswith('['):
            t = html.escape(corpus[j])
            for w in (bare, bare[2:]):  # "be-/freyt": the word broken at the line end
                if w and html.escape(w) in t:
                    t = t.replace(html.escape(w), f'<mark>{html.escape(w)}</mark>', 1)
                    break
            out.append(t)
    return '<br>'.join(out)


def main():
    corpus = io.open(os.path.join(UNIT, 'corpus.txt'), encoding='utf-8').read().split('\n')
    cards = []
    for key, doc, line, word, opts, note, (pid, box) in ROWS:
        box = BOX_FIX.get(key, box)
        page = Image.open(SRC % pid)
        close = b64(page.crop(box), 1400)
        cy = (box[1] + box[3]) // 2
        wide = b64(page.crop((0, max(0, cy - 450), page.width,
                              min(page.height, cy + 450))), 1400)
        btns = ''.join(f'<button class="opt" data-v="{html.escape(o)}">{html.escape(o)}</button>'
                       for o in opts.split('|'))
        cards.append(f'''
<section class="row" data-key="{key}">
  <h2><span class="k">{key}</span> {html.escape(DOC_NAME[doc])}, page {pid}</h2>
  <p class="q">{html.escape(note)}</p>
  <img src="{close}" alt="close crop of the word on page {pid}">
  <details><summary>Show the lines around it</summary><img src="{wide}" alt="the lines around the word on page {pid}"></details>
  <p class="ctx">Transcription now:<br>{context(corpus, line, word)}</p>
  <div class="opts">{btns}<button class="opt" data-v="__unsure__">Can't tell</button><button class="opt" data-v="__other__">Something else</button></div>
  <input class="other" placeholder="What the page reads" hidden>
  <input class="note" placeholder="Note (optional)">
  <button class="miss" data-v="__wrongspot__">The picture doesn't show the word</button>
</section>''')

    page = TEMPLATE.replace('__ROWS__', '\n'.join(cards)).replace('__N__', str(len(cards)))
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write(page)
    print(f'{len(cards)} rows -> {OUT} ({os.path.getsize(OUT) // 1024} KB)')


TEMPLATE = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Nr. 3067 spot sheet</title>
<style>
:root{--bg:#f4f1ea;--card:#fff;--fg:#1a1a1a;--mute:#666;--line:#d8d2c4;--acc:#1a5c8a;--accfg:#fff;--mark:#ffd65a;--warn:#a05a00}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#1b1a18;--card:#242320;--fg:#e8e6e1;--mute:#9a968e;--line:#3a3834;--acc:#7fb3d9;--accfg:#111;--mark:#8a6d00;--warn:#e0b060}}
:root[data-theme="dark"]{--bg:#1b1a18;--card:#242320;--fg:#e8e6e1;--mute:#9a968e;--line:#3a3834;--acc:#7fb3d9;--accfg:#111;--mark:#8a6d00;--warn:#e0b060}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 Georgia,serif}
header{position:sticky;top:0;z-index:5;background:var(--acc);color:var(--accfg);padding:10px 16px}
header h1{margin:0;font-size:1.05rem}header p{margin:0;font-size:.85rem;opacity:.9}
main{max-width:1000px;margin:0 auto;padding:8px 16px 90px}
.intro{color:var(--mute);font-size:.92rem}
.row{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px 14px;margin:16px 0}
.row.done{border-left:6px solid var(--acc)}
.row h2{font-size:.95rem;margin:0 0 6px}.k{font-family:ui-monospace,Consolas,monospace;color:var(--mute)}
.q{margin:4px 0 10px}
img{display:block;max-width:100%;height:auto;border:1px solid var(--line);border-radius:4px;background:#fff}
details{margin:6px 0}summary{cursor:pointer;color:var(--acc);font-size:.9rem}details img{margin-top:6px}
.ctx{font-family:ui-monospace,Consolas,monospace;font-size:.85rem;color:var(--mute);overflow-wrap:anywhere}
mark{background:var(--mark);color:inherit;font-weight:bold;padding:0 2px}
.opts{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0}
button{font:inherit;cursor:pointer;border-radius:6px}
.opt{flex:1 1 auto;min-width:110px;padding:10px;border:2px solid var(--acc);background:var(--card);color:var(--acc)}
.opt.on{background:var(--acc);color:var(--accfg)}
input{width:100%;font:inherit;padding:8px;margin:4px 0;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg)}
.miss{width:100%;margin-top:6px;padding:7px;font-size:.85rem;border:1px solid var(--warn);background:transparent;color:var(--warn)}
.miss.on{background:var(--warn);color:var(--card)}
#bar{position:fixed;left:0;right:0;bottom:0;display:flex;gap:10px;align-items:center;padding:10px 16px;background:var(--card);border-top:1px solid var(--line)}
#bar button{padding:10px 16px;border:0;background:var(--acc);color:var(--accfg)}#count{flex:1;color:var(--mute)}
#out{width:100%;height:9em;font:13px ui-monospace,Consolas,monospace;margin-top:8px;background:var(--bg);color:var(--fg);border:1px solid var(--line)}
</style>
</head>
<body>
<header><h1>Spot sheet: I. HA GR, Rep. 7 C, Nr. 3067</h1><p>__N__ readings the scans did not settle</p></header>
<main>
<p class="intro">For each word, look at the picture and pick what the page says.
The first button is what the transcription has now. If it is something else, choose
"Something else" and type it; "Can't tell" is a fine answer too. Answers are kept in
this browser as you go. When you're done, press "Copy answers" and paste the result
into the chat.</p>
__ROWS__
<textarea id="out" readonly hidden></textarea>
</main>
<div id="bar"><span id="count"></span><button id="copy">Copy answers</button></div>
<script>
const KEY='spot-ihagrrep7cnr3067';
let A={};try{A=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){}
function store(){try{localStorage.setItem(KEY,JSON.stringify(A))}catch(e){}count()}
function count(){const rows=document.querySelectorAll('.row');const n=[...rows].filter(r=>(A[r.dataset.key]||{}).reading).length;document.getElementById('count').textContent=n+' of '+rows.length+' answered'}
document.querySelectorAll('.row').forEach(row=>{
  const k=row.dataset.key,opts=[...row.querySelectorAll('.opt')],other=row.querySelector('.other'),note=row.querySelector('.note'),miss=row.querySelector('.miss');
  const a=A[k]||(A[k]={reading:'',other:'',note:'',wrong_spot:false});
  function show(){opts.forEach(b=>b.classList.toggle('on',b.dataset.v===a.reading));other.hidden=a.reading!=='__other__';row.classList.toggle('done',!!a.reading);miss.classList.toggle('on',!!a.wrong_spot)}
  other.value=a.other||'';note.value=a.note||'';show();
  opts.forEach(b=>b.onclick=()=>{a.reading=a.reading===b.dataset.v?'':b.dataset.v;show();store();if(a.reading==='__other__')other.focus()});
  other.oninput=()=>{a.other=other.value;store()};note.oninput=()=>{a.note=note.value;store()};
  miss.onclick=()=>{a.wrong_spot=!a.wrong_spot;show();store()};
});
document.getElementById('copy').onclick=async()=>{
  const out=document.getElementById('out'),txt='Nr. 3067 spot sheet answers:\\n'+JSON.stringify(A,null,1);
  out.value=txt;out.hidden=false;
  try{await navigator.clipboard.writeText(txt);document.getElementById('count').textContent='Copied - paste it into the chat'}
  catch(e){out.select();document.getElementById('count').textContent='Select the box below and copy it'}
};
count();
</script>
</body>
</html>
'''

if __name__ == '__main__':
    main()
