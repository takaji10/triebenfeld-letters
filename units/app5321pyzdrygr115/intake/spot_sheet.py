#!/usr/bin/env python3
"""The spot sheet of APP 53/21/0/-/Pyzdry Gr.115, served on the LAN and over a
Cloudflare quick tunnel, so the editor can answer it away from the PC.

    python units/app5321pyzdrygr115/intake/spot_sheet.py   # serve + URL
    ... --read                                             # the answers

Rows (2026-10-26; the editor's other rulings of the day are already applied
in chat: "Parafie", and Marianton):

  gara      what the two figure columns are ("gara zyta", "gara owcza")
  trabczyn  the village row's middle figure: 22 as written, or 42 (the other
            rows double from column to column)
  sitting   whether the page carries a dated sitting heading above the entry,
            which the document could take as its sitting date

Answers save server-side to review/app5321pyzdrygr115/spot_answers.json
(git-ignored, like all review/); --read prints them.
"""
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import threading
import time

from flask import Flask, jsonify, request, send_from_directory

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))  # the repo root
REV = os.path.join(ROOT, 'review', 'app5321pyzdrygr115')
ANSWERS = os.path.join(REV, 'spot_answers.json')
IMG = os.path.join(REV, 'spot_img')
RAW = (r"J:\Documents\Archive\Genealogy\References\Poznań State Archives"
       r"\Relationes [protocollon] 1791-1792 (53.21.0.-.Pyzdry Gr.115)"
       r"\543_trim.jpg")
PORT = 8643

app = Flask(__name__, static_folder=None)

ROWS = [
    {'key': 'gara',
     'title': 'The two sheaf columns',
     'text': 'The table\'s last two column headings read <b>gara zyta</b> and '
             '<b>gara owcza</b> (after "Dymy rolne", the agricultural '
             'hearths). The columns stand as written until you say what they '
             'are - type it under "Something else", or keep as written.',
     'image': 'gara_band.jpg',
     'options': ['Keep as written']},
    {'key': 'trabczyn',
     'title': 'The village row\'s middle figure',
     'text': 'The row of the village of Trąbczyn itself reads <b>21, 22, '
             '84</b>. In every other row the figures double from column to '
             'column (4-8-16, 5-10-20 ...), which would give <b>42</b> here. '
             'Figures are never corrected from arithmetic: pick what the '
             'page says, or leave it for later.',
     'image': 'trabczyn_band.jpg',
     'options': ['22 (as written)', '42']},
    {'key': 'sitting',
     'title': 'A dated heading above the entry?',
     'text': 'Court-book entries can stand under the dated heading of the '
             'court\'s sitting, and the document then takes that date. Does '
             'this page\'s table stand under one? If yes, type the date '
             'under "Something else".',
     'image': 'top_half.jpg',
     'options': ['No dated heading above the entry']},
]

PAGE = """<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial=1">
<title>Pyzdry Gr.115: the spot sheet</title>
<style>
:root{--bg:#fbfaf7;--fg:#222;--mute:#666;--line:#ddd;--ok:#2a6b2a;--hi:#8a5a00;--card:#fff}
@media (prefers-color-scheme:dark){:root{--bg:#1b1a18;--fg:#e8e6e1;--mute:#9a968e;--line:#3a3834;--ok:#7fc27f;--hi:#e0b060;--card:#242320}}
body{font:16px/1.5 Georgia,serif;max-width:900px;margin:2em auto;padding:0 16px;background:var(--bg);color:var(--fg)}
.row{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:12px 14px;margin:12px 0}
.row.done{border-left:5px solid var(--ok)}
h2{font-size:1.05rem;margin:.2em 0}
img{max-width:100%;border:1px solid var(--line);margin:.3em 0}
small{color:var(--mute)}button{font:inherit;padding:5px 14px;margin:0 6px 6px 0;cursor:pointer;border-radius:4px;border:1px solid var(--line);background:var(--bg);color:var(--fg)}
button.on{background:var(--fg);color:var(--bg)}input{font:inherit;width:100%;box-sizing:border-box;margin-top:4px;padding:5px 7px;background:var(--bg);color:var(--fg);border:1px solid var(--line)}
#status{position:sticky;top:0;background:var(--bg);padding:6px 0;color:var(--mute)}
a{color:inherit}
</style>
<h1>APP 53/21/0/-/Pyzdry Gr.115 - the spot sheet</h1>
<p>The table of the parish of Trąbczyn, page 543 of the Relationes
[protocollon] of 1791-1792, is built on your transcription. Three things wait
for your word. Answers save as you go.
<a href="/page" target="_blank">The whole page</a>.</p>
<div id="status"></div>
__ROWS__
<script>
const st=document.getElementById('status');
function count(){const r=document.querySelectorAll('.row'),d=[...r].filter(x=>x.dataset.v).length;st.textContent=d+' of '+r.length+' answered';}
async function save(row){
  const other=row.querySelector('input');
  const body={key:row.dataset.key,reading:row.dataset.v||'',other:other.value};
  try{const r=await fetch('/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
      if(!r.ok)throw 0;count();}catch(e){st.textContent='Not saved - is the sheet still being served?';}
}
document.querySelectorAll('.row').forEach(row=>{
  const bs=[...row.querySelectorAll('button')],other=row.querySelector('input');
  function set(v){row.dataset.v=v;row.classList.toggle('done',!!v);
    bs.forEach(b=>b.classList.toggle('on',b.dataset.v===v));other.hidden=v!=='__other__';if(v==='__other__')other.focus();}
  if(row.dataset.v)set(row.dataset.v);
  bs.forEach(b=>b.onclick=()=>{set(b.dataset.v);save(row);});
  let t;other.oninput=()=>{clearTimeout(t);t=setTimeout(()=>save(row),400);};
});
count();
</script></html>"""


def crops():
    """Cut the sheet's pictures from the editor's trim."""
    from PIL import Image
    os.makedirs(IMG, exist_ok=True)
    im = Image.open(RAW).convert('RGB')
    W, H = im.size

    def band(name, fx0, fy0, fx1, fy1, scale=1.5):
        p = os.path.join(IMG, name)
        c = im.crop((int(W * fx0), int(H * fy0), int(W * fx1), int(H * fy1)))
        c = c.resize((int(c.width / scale), int(c.height / scale)), Image.LANCZOS)
        c.save(p, quality=86)
    # the heading row of the table, with the columns' names: a wide band of
    # the page's top; the exact line is the editor's to find on it
    band('gara_band.jpg', 0.02, 0.02, 0.98, 0.28, 1.4)
    # the first data row, generous: the table's upper body
    band('trabczyn_band.jpg', 0.02, 0.10, 0.98, 0.34, 1.4)
    # the whole top half, for the sitting-heading row
    band('top_half.jpg', 0.0, 0.0, 1.0, 0.5, 2.2)
    # and the whole page, scaled for the phone
    full = im.resize((1100, int(H * 1100 / W)), Image.LANCZOS)
    full.save(os.path.join(IMG, 'full_page.jpg'), quality=85)


def build(answers):
    out = []
    for i, r in enumerate(ROWS, 1):
        a = answers.get(r['key'], {})
        v = a.get('reading', '')
        buttons = ''.join(
            f"<button data-v=\"{o}\">{o}</button>" for o in r['options'])
        buttons += ("<button data-v='__other__'>Something else</button>"
                    "<button data-v='__unsure__'>Can't tell</button>")
        out.append(
            f"<div class='row' data-key='{r['key']}' data-v='{v}'>"
            f"<h2>{i}. {r['title']}</h2><p>{r['text']}</p>"
            f"<a href='/img/{r['image']}' target='_blank'>"
            f"<img src='/img/{r['image']}'></a>"
            f"<div style='margin-top:8px'>{buttons}"
            f"<input placeholder='What the page says' value=\"{a.get('other', '')}\""
            f"{' hidden' if v != '__other__' else ''}></div></div>")
    return (PAGE.replace('__ROWS__', '\n'.join(out))
            .replace('initial=1', 'initial-scale=1'))


def tunnel_url():
    exe = os.path.join(HERE, 'cloudflared.exe')
    if not os.path.isfile(exe):
        exe = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\cloudflared.exe"
    if not os.path.isfile(exe) and not shutil.which('cloudflared'):
        return None
    exe = exe if os.path.isfile(exe) else shutil.which('cloudflared')
    proc = subprocess.Popen(
        [exe, 'tunnel', '--url', f'http://127.0.0.1:{PORT}'],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
        creationflags=subprocess.CREATE_NO_WINDOW)
    deadline = time.time() + 60
    for line in proc.stdout:
        m = re.search(r'https://[a-z0-9-]+\.trycloudflare\.com', line)
        if m:
            return m.group(0)
        if time.time() > deadline:
            break
    return None


def main():
    if '--read' in sys.argv:
        answers = json.load(open(ANSWERS, encoding='utf-8')) if \
            os.path.isfile(ANSWERS) else {}
        done = [k for k in answers if answers[k].get('reading')]
        print(f'{len(done)} of {len(ROWS)} answered')
        for k, a in answers.items():
            got = {'__other__': f"other: {a.get('other') or '(not given)'}",
                   '__unsure__': "can't tell"}.get(a.get('reading'),
                                                   a.get('reading'))
            print(f'  {k}: {got}')
        return
    crops()
    os.makedirs(REV, exist_ok=True)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    s.close()
    print(f'LAN URL:  http://{ip}:{PORT}/', flush=True)

    def bg():
        url = tunnel_url()
        print(f'WEB URL:  {url or "unavailable (tunnel failed)"}', flush=True)
    threading.Thread(target=bg, daemon=True).start()

    @app.get('/')
    def page():
        answers = json.load(open(ANSWERS, encoding='utf-8')) if \
            os.path.isfile(ANSWERS) else {}
        return build(answers)

    @app.get('/img/<name>')
    def img(name):
        return send_from_directory(IMG, name)

    @app.get('/page')
    def page_full():
        return send_from_directory(IMG, 'full_page.jpg')

    @app.post('/save')
    def save():
        d = request.get_json(force=True)
        existing = json.load(open(ANSWERS, encoding='utf-8')) if \
            os.path.isfile(ANSWERS) else {}
        existing[d['key']] = {'reading': d.get('reading', ''),
                              'other': d.get('other', '')}
        with open(ANSWERS, 'w', encoding='utf-8') as f:
            json.dump(existing, f, ensure_ascii=False, indent=1)
        return jsonify({'ok': True, 'count': len(existing)})

    app.run(host='0.0.0.0', port=PORT, debug=False)


if __name__ == '__main__':
    main()
