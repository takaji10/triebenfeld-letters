# -*- coding: utf-8 -*-
"""A spot check of applied transcription fixes, answered in the browser.

    python pipeline/review/spotcheck.py --unit oe1bu9454              # 20 rows, serve
    python pipeline/review/spotcheck.py --unit oe1bu9454 --n 30 --seed 7
    python pipeline/review/spotcheck.py --unit oe1bu9454 --read       # print the answers

A correction pass is only as good as a sample of it checked against the page. This
draws a random sample from review/<slug>/transcription_fixes.csv, serves it at
http://127.0.0.1:4100/, and saves every answer the moment it is given to
review/<slug>/spotcheck_answers.json - so the editor never has to write the
verdicts out by hand, and a closed tab loses nothing.

Each row links to the letter page on the local Jekyll site (port 4000), where the
scan stands beside the text. Nothing here touches the corpus.
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import unitlib
import io, sys, os, csv, json, random, html, argparse
from http.server import HTTPServer, BaseHTTPRequestHandler

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE = 'http://127.0.0.1:4000'

PAGE = """<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Spot check</title>
<style>
:root{--bg:#fbfaf7;--fg:#222;--mute:#666;--line:#ddd;--ok:#2a6b2a;--bad:#a33;--card:#fff}
@media (prefers-color-scheme:dark){:root{--bg:#1b1a18;--fg:#e8e6e1;--mute:#9a968e;--line:#3a3834;--ok:#7fc27f;--bad:#e08080;--card:#242320}}
body{font:16px/1.5 Georgia,serif;max-width:860px;margin:2em auto;padding:0 16px;background:var(--bg);color:var(--fg)}
.row{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:12px 14px;margin:12px 0}
.row.ok{border-left:5px solid var(--ok)}.row.bad{border-left:5px solid var(--bad)}
.o{color:var(--bad);text-decoration:line-through}.n{color:var(--ok);font-weight:bold}
.line{font-family:ui-monospace,Consolas,monospace;font-size:14px;margin:.4em 0;overflow-wrap:anywhere}
small{color:var(--mute)}button{font:inherit;padding:4px 12px;margin-right:6px;cursor:pointer;border-radius:4px;border:1px solid var(--line);background:var(--bg);color:var(--fg)}
button.on{background:var(--fg);color:var(--bg)}input{font:inherit;width:100%;box-sizing:border-box;margin-top:6px;padding:4px 6px;background:var(--bg);color:var(--fg);border:1px solid var(--line)}
#status{position:sticky;top:0;background:var(--bg);padding:6px 0;color:var(--mute)}a{color:inherit}
</style>
<h1>Spot check: __N__ of __TOTAL__ changes</h1>
<p>Open each letter, find the line on the scan, and say whether the new word is what the page says.
If it isn't, type what the page does say. Answers save as you go.</p>
<div id="status">__DONE__</div>
__ROWS__
<script>
const st=document.getElementById('status');
function count(){const r=document.querySelectorAll('.row'),d=[...r].filter(x=>x.dataset.v).length;st.textContent=d+' of '+r.length+' answered';}
async function save(row){
  const body={key:row.dataset.key,verdict:row.dataset.v||'',reading:row.querySelector('input').value};
  try{const r=await fetch('/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
      if(!r.ok)throw 0;count();}catch(e){st.textContent='Not saved - is spotcheck.py still running?';}
}
document.querySelectorAll('.row').forEach(row=>{
  const [ok,bad]=row.querySelectorAll('button'),inp=row.querySelector('input');
  function set(v){row.dataset.v=v;row.className='row '+v;ok.classList.toggle('on',v==='ok');bad.classList.toggle('on',v==='bad');inp.hidden=v!=='bad';if(v==='bad')inp.focus();}
  if(row.dataset.v)set(row.dataset.v);
  ok.onclick=()=>{set('ok');save(row);};
  bad.onclick=()=>{set('bad');save(row);};
  let t;inp.oninput=()=>{clearTimeout(t);t=setTimeout(()=>save(row),400);};
});
count();
</script></html>"""


def letter_lines(corpus):
    """Corpus line -> the line number the letter page shows beside it.

    The site numbers every non-blank line from the top of the document, markers
    excluded, so page 2 of letter 3 opens at line 31. That is the number the
    editor can find on the page; the corpus line is only ours.
    """
    out, n = {}, 0
    for i, l in enumerate(corpus, 1):
        s = l.strip()
        if s.startswith('[DOC '):
            n = 0
        elif s and not s.startswith('[PAGE '):
            n += 1
            out[i] = n
    return out


def build(rows, answers, total, corpus):
    shown = letter_lines(corpus)
    out = []
    for i, r in enumerate(rows, 1):
        a = answers.get(r['key'], {})
        v, reading = a.get('verdict', ''), a.get('reading', '')
        url = f"{SITE}/documents/{r['pad'].rsplit('-', 1)[0]}/{r['letter']}/#p{r['page']}"
        out.append(
            f"<div class='row {v}' data-key='{r['key']}' data-v='{v}'>"
            f"<div>{i}. <a href='{url}' target='_blank'>Letter {html.escape(r['letter'])}, "
            f"page {r['page']}</a>, <b>line {shown.get(int(r['line']), '?')}</b></div>"
            f"<div><span class=o>{html.escape(r['transcribed'])}</span> &rarr; "
            f"<span class=n>{html.escape(r['proposed'])}</span></div>"
            f"<div class=line>{html.escape(corpus[int(r['line']) - 1])}</div>"
            f"<small>{html.escape(r['why'])}</small><div style='margin-top:8px'>"
            f"<button>Correct</button><button>Not what the page says</button>"
            f"<input placeholder='What the page actually says' value='{html.escape(reading, quote=True)}'"
            f"{'' if v == 'bad' else ' hidden'}></div></div>")
    return (PAGE.replace('__N__', str(len(rows))).replace('__TOTAL__', str(total))
                .replace('__DONE__', '').replace('__ROWS__', '\n'.join(out)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--unit')
    ap.add_argument('--n', type=int, default=20)
    ap.add_argument('--seed', type=int, default=20260927)
    ap.add_argument('--port', type=int, default=4100)
    ap.add_argument('--read', action='store_true', help='print the answers and exit')
    ap.add_argument('--sheet', help='sample from this sheet instead - e.g. several '
                                    'batches pooled, so one check covers them all')
    a = ap.parse_args()
    slug = unitlib.resolve_unit(a.unit)
    unit = unitlib.one_unit(slug)
    rev = unitlib.review_dir(slug)
    sheet = a.sheet or os.path.join(rev, 'transcription_fixes.csv')
    store = os.path.join(rev, 'spotcheck_answers.json')

    rows = list(csv.DictReader(io.open(sheet, encoding='utf-8-sig')))
    answers = json.load(io.open(store, encoding='utf-8')) if os.path.isfile(store) else {}

    if a.read:
        byk = {r['key']: r for r in rows}
        # one answers file serves every batch; report only this sheet's rows
        answers = {k: v for k, v in answers.items() if k in byk}
        ok = sum(1 for x in answers.values() if x.get('verdict') == 'ok')
        bad = [(k, x) for k, x in answers.items() if x.get('verdict') == 'bad']
        print(f'{len(answers)} answered: {ok} correct, {len(bad)} not')
        for k, x in bad:
            r = byk.get(k, {})
            print(f"  L{r.get('letter')} line {r.get('line')}: {r.get('transcribed')} -> "
                  f"{r.get('proposed')}; page says: {x.get('reading') or '(not given)'}")
        return

    random.seed(a.seed)
    pick = sorted(random.sample(rows, min(a.n, len(rows))), key=lambda r: int(r['line']))
    corpus = io.open(os.path.join(unit.dir, unit.get('corpus') or 'corpus.txt'),
                     encoding='utf-8').read().split('\n')

    class H(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def do_GET(self):
            body = build(pick, answers, len(rows), corpus).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(body)

        def do_POST(self):
            d = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
            answers[d['key']] = {'verdict': d.get('verdict', ''),
                                 'reading': d.get('reading', '')}
            with io.open(store, 'w', encoding='utf-8') as f:
                json.dump(answers, f, ensure_ascii=False, indent=1)
            self.send_response(204)
            self.end_headers()

    print(f'spot check at http://127.0.0.1:{a.port}/  -  answers go to {store}')
    HTTPServer(('127.0.0.1', a.port), H).serve_forever()


if __name__ == '__main__':
    main()
