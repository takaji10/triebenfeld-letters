# -*- coding: utf-8 -*-
"""Open questions about the transcription, answered in the browser.

    python pipeline/review/queries.py --unit oe1bu9454          # serve
    python pipeline/review/queries.py --unit oe1bu9454 --read   # print the answers

The spot check asks whether an applied change is right. This asks the other kind
of question: a word left as written because the right reading could not be pinned
down without the page. Each row of review/<slug>/open_queries.csv names the word
(its corpus line), the candidate readings, and why it is in doubt. The editor
picks a reading, or types another, and every answer is saved at once to
review/<slug>/query_answers.json. Nothing here touches the corpus: answers are
applied afterwards, through apply_transcription_fixes.py, like any other ruling.
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))))

import unitlib
import io, sys, os, re, csv, json, html, argparse
from http.server import HTTPServer, BaseHTTPRequestHandler

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spotcheck import letter_lines, SITE   # also sets stdout to UTF-8

PAGE = """<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<style>
:root{--bg:#fbfaf7;--fg:#222;--mute:#666;--line:#ddd;--ok:#2a6b2a;--hi:#8a5a00;--card:#fff}
@media (prefers-color-scheme:dark){:root{--bg:#1b1a18;--fg:#e8e6e1;--mute:#9a968e;--line:#3a3834;--ok:#7fc27f;--hi:#e0b060;--card:#242320}}
body{font:16px/1.5 Georgia,serif;max-width:860px;margin:2em auto;padding:0 16px;background:var(--bg);color:var(--fg)}
.row{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:12px 14px;margin:12px 0}
.row.done{border-left:5px solid var(--ok)}
.w{color:var(--hi);font-weight:bold}
.line{font-family:ui-monospace,Consolas,monospace;font-size:14px;margin:.4em 0;overflow-wrap:anywhere}
small{color:var(--mute)}button{font:inherit;padding:4px 12px;margin:0 6px 6px 0;cursor:pointer;border-radius:4px;border:1px solid var(--line);background:var(--bg);color:var(--fg)}
button.on{background:var(--fg);color:var(--bg)}input{font:inherit;width:100%;box-sizing:border-box;margin-top:4px;padding:4px 6px;background:var(--bg);color:var(--fg);border:1px solid var(--line)}
#status{position:sticky;top:0;background:var(--bg);padding:6px 0;color:var(--mute)}a{color:inherit}
</style>
<h1>__TITLE__: __N__ items</h1>
<p>__INTRO__ Open the letter,
find the line on the scan, and pick what the page says, or type it under "Something else".
"Can't tell" is a fine answer. Answers save as you go.</p>
<div id="status"></div>
__ROWS__
<script>
const st=document.getElementById('status');
function count(){const r=document.querySelectorAll('.row'),d=[...r].filter(x=>x.dataset.v).length;st.textContent=d+' of '+r.length+' answered';}
async function save(row){
  const [other,note]=row.querySelectorAll('input');
  const body={key:row.dataset.key,reading:row.dataset.v||'',other:other.value,note:note.value};
  try{const r=await fetch('/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
      if(!r.ok)throw 0;count();}catch(e){st.textContent='Not saved - is queries.py still running?';}
}
document.querySelectorAll('.row').forEach(row=>{
  const bs=[...row.querySelectorAll('button')],[other,note]=row.querySelectorAll('input');
  function set(v){row.dataset.v=v;row.classList.toggle('done',!!v);
    bs.forEach(b=>b.classList.toggle('on',b.dataset.v===v));other.hidden=v!=='__other__';if(v==='__other__')other.focus();}
  if(row.dataset.v)set(row.dataset.v);
  bs.forEach(b=>b.onclick=()=>{set(b.dataset.v);save(row);});
  let t;[other,note].forEach(i=>i.oninput=()=>{clearTimeout(t);t=setTimeout(()=>save(row),400);});
});
count();
</script></html>"""


def pages(corpus):
    """Corpus line -> the page number within its document (1 for the first)."""
    out, n = {}, 0
    for i, l in enumerate(corpus, 1):
        s = l.strip()
        if s.startswith('[DOC '):
            n = 0
        elif s.startswith('[PAGE '):
            n += 1
        out[i] = n
    return out


def build(rows, answers, corpus, slug, stem='open_queries'):
    shown, pg = letter_lines(corpus), pages(corpus)
    out = []
    for i, r in enumerate(rows, 1):
        n = int(r['line'])
        a = answers.get(r['key'], {})
        v = a.get('reading', '')
        text = html.escape(corpus[n - 1])
        w = html.escape(r['word'])
        text = text.replace(w, f'<span class=w>{w}</span>', 1)
        if r.get('summary'):
            # a summary to judge, not a word: show the paragraph itself
            text = f"<p style='font:16px/1.5 Georgia,serif'>{html.escape(r['summary'])}</p>"
        opts = [o for o in r['options'].split('|') if o]
        buttons = ''.join(
            f"<button data-v='{html.escape(o, quote=True)}'>"
            f"{html.escape(o)}{' (as written)' if o == r['word'] else ''}</button>"
            for o in opts)
        buttons += ("<button data-v='__other__'>Something else</button>"
                    "<button data-v='__unsure__'>Can't tell</button>")
        url = f"{SITE}/documents/{slug}/{r['letter']}/#p{pg.get(n, 1)}"
        out.append(
            f"<div class='row' data-key='{r['key']}' data-v='{html.escape(v, quote=True)}'>"
            f"<div>{i}. <a href='{url}' target='_blank'>Letter {html.escape(r['letter'])}, "
            f"page {pg.get(n, 1)}</a>, <b>line {shown.get(n, '?')}</b></div>"
            f"<div class=line>{text}</div>"
            f"<small>{html.escape(r['note'])}</small><div style='margin-top:8px'>{buttons}"
            f"<input placeholder='What the page says' "
            f"value='{html.escape(a.get('other', ''), quote=True)}'"
            f"{'' if v == '__other__' else ' hidden'}>"
            f"<input placeholder='Note (optional)' "
            f"value='{html.escape(a.get('note', ''), quote=True)}'></div></div>")
    title, intro = {
        'doubt_queries': ('Doubt marks', 'Each word carries your [?]. The context suggests a '
                          'reading; keeping it as written keeps the [?].'),
        'abbr_queries': ('Abbreviations', 'Each abbreviation was left unexpanded because '
                         'the text does not decide it. Pick the expansion the page supports.'),
        'trial_251': ('Trial reading, letter 251', 'Each row is a word where the trial '
                      'reading from the original scan differs from the current text. Pick '
                      'what the page says.'),
        'trial_144': ('Trial reading, letter 144', 'Each row is a word where the trial '
                      'reading from the original scan differs from the current text. Pick '
                      'what the page says.'),
        'garbled_sample': ('Garbled letters, sample of fixes', 'Twenty fixes drawn at random from the 220 made in the garbled letters. '
                           'The highlighted word is the new reading; the second button is what stood before.'),
        'break_queries': ('Line-break marks', 'Each row is a word at a line end marked ¬ where the next line does not complete it. Keep the break as written, mark it as two separate words, take the suggested reading, or type what the page says (for example a lost ending).'),
        'break_queries_left': ('Line-break marks, the rest', 'The line ends I could not settle from the scan or the sentence. Keep as written, mark two separate words, take the suggestion, or type what the page says.'),
        'johann_queries': ('Johann or Johanni', 'The three places where Johann was left as written. Pick what the page says.'),
        'open_questions_2': ('Open questions', 'Readings I would change but need you to confirm on the page.'),
        'brzechsta_queries': ('Brzechsta', 'His own signatures. Pick what the page shows and the spelling the edition should standardise to.'),
        'brzechffa_initial': ('Brzechffa, the initial', 'His initial in the signature of letter 72e.'),
        'watch_queries': ('Watch-list: the doubtful ones', 'Stray French words and similar that the sentence does not settle.'),
        'letter205': ('Letter 205', 'One interlinear word.'),
        'niedz_queries': ('Niedziewiecki', 'His own signatures, and the spelling to standardise to.'),
        'initial_queries': ('Initials I was not sure of', 'Single-letter name abbreviations I did not expand. Pick an expansion or keep as written.'),
        'pohl_queries': ('Pohlen: the unclear ones', 'Forms of Pohlen and lookalikes the sentence did not settle.'),
        'trial_245': ('Trial reading, letter 245', 'Each row is a word where my reading of the original scan differs from the current text. Pick what the page says.'),
        'rescan_choice': ('Pages to request from the archive', 'One row per page on the shortlist, worst first. Open the letter, look at the scan, and choose Request or Skip.'),
        'date_queries': ('Dates: yours against the page', 'Where the new transcription reads a date differently from the date you supplied. Pick the date the letter should carry.'),
        'pilot_summaries': ('Pilot: ten letters read', 'English renderings of the German summaries for ten letters. Their accuracy has been checked against the letters claim by claim, so you are not asked to judge that. Say only whether each picks out what you want: the right focus, something missing, too much detail, or the wrong emphasis.'),
        'unknown_names': ('Unidentified names', 'None of these could be identified from the '
                          'letters. Where the context suggests a reading it is offered; '
                          'otherwise say what the page reads, or who or where it is.'),
    }.get(stem, ('Open questions', 'Each word was left as written because the right '
                 'reading needs the page.'))
    return (PAGE.replace('__TITLE__', title).replace('__INTRO__', intro)
                .replace('__N__', str(len(rows))).replace('__ROWS__', '\n'.join(out)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--unit')
    ap.add_argument('--port', type=int, default=4101)
    ap.add_argument('--read', action='store_true', help='print the answers and exit')
    ap.add_argument('--sheet', default='open_queries.csv',
                    help='a question sheet in review/<slug>/; its answers go to '
                         '<sheet>_answers.json (open_queries.csv keeps query_answers.json)')
    a = ap.parse_args()
    slug = unitlib.resolve_unit(a.unit)
    unit = unitlib.one_unit(slug)
    rev = unitlib.review_dir(slug)
    sheet = os.path.join(rev, a.sheet)
    stem = os.path.splitext(a.sheet)[0]
    store = os.path.join(rev, 'query_answers.json' if stem == 'open_queries'
                         else stem + '_answers.json')

    rows = list(csv.DictReader(io.open(sheet, encoding='utf-8-sig')))
    answers = json.load(io.open(store, encoding='utf-8')) if os.path.isfile(store) else {}

    if a.read:
        done = [r for r in rows if answers.get(r['key'], {}).get('reading')]
        print(f'{len(done)} of {len(rows)} answered')
        for r in done:
            x = answers[r['key']]
            got = {'__other__': f"other: {x.get('other') or '(not given)'}",
                   '__unsure__': "can't tell"}.get(x['reading'], x['reading'])
            note = f"  [{x['note']}]" if x.get('note') else ''
            print(f"  {r['key']} L{r['letter']} line {r['line']}: {r['word']} -> {got}{note}")
        return

    corpus = io.open(os.path.join(unit.dir, unit.get('corpus') or 'corpus.txt'),
                     encoding='utf-8').read().split('\n')

    class H(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def do_GET(self):
            body = build(rows, answers, corpus, slug, stem).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(body)

        def do_POST(self):
            d = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
            answers[d['key']] = {'reading': d.get('reading', ''),
                                 'other': d.get('other', ''), 'note': d.get('note', '')}
            with io.open(store, 'w', encoding='utf-8') as f:
                json.dump(answers, f, ensure_ascii=False, indent=1)
            self.send_response(204)
            self.end_headers()

    print(f'open questions at http://127.0.0.1:{a.port}/  -  answers go to {store}')
    HTTPServer(('127.0.0.1', a.port), H).serve_forever()


if __name__ == '__main__':
    main()
