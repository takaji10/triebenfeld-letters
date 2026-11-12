# -*- coding: utf-8 -*-
"""The editor's review sheet for AGAD 1/432/0/1/139 (Erdmann's reports of 1882):
the readings left doubtful, the proposals of the supplied-text layer worth a
second look, and the decisions that are the editor's. Written 2026-11-12.

    python units/agad14320139/intake/spot_sheet1.py          # serve (port 4108)
    python units/agad14320139/intake/spot_sheet1.py --read   # print the answers

Each reading row shows a strip cut from the page image (the line or lines
asked about, with the line above and below), the line as the transcription has
it, and buttons; answers are saved as you go to
review/agad14320139/spot_answers.json. Nothing here touches the corpus:
answers are applied afterwards, as rulings.

The line centres on each page were found from the ink profile of the image
(the lines of 0322_a 11 and 22-24 and of 0345_a 12 and 23 are by spacing).
"""
import argparse
import html
import http.server
import json
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
UNIT = os.path.dirname(HERE)
REV = os.path.join(ROOT, 'review', 'agad14320139')
IMG = os.path.join(REV, 'spot_img')
os.makedirs(IMG, exist_ok=True)
STORE = os.path.join(REV, 'spot_answers.json')
SRC = r'C:\Users\Tersnaus\Downloads\AGAD_1_432_0_1_139\processed'

# line -> y centre (pixels of the page image)
Y = {
    '0318_a': dict(zip(range(1, 31), [84, 268, 333, 391, 518, 578, 640, 769, 837, 890, 960, 1027, 1165,
                                       1231, 1279, 1343, 1402, 1462, 1531, 1592, 1653, 1721, 1781, 1846,
                                       1907, 1967, 2034, 2094, 2158, 2215])),
    '0322_a': dict(zip(range(1, 25), [267, 329, 391, 451, 517, 581, 648, 708, 772, 836, 897, 958, 1025,
                                       1089, 1149, 1212, 1279, 1342, 1400, 1464, 1527, 1590, 1706, 1790])),
    '0322_b': dict(zip(range(1, 31), [52, 231, 293, 356, 485, 547, 606, 733, 795, 856, 918, 982, 1120,
                                       1181, 1237, 1308, 1366, 1426, 1491, 1552, 1621, 1678, 1742, 1805,
                                       1869, 1935, 1996, 2060, 2121, 2184])),
    '0345_a': dict(zip(range(1, 24), [259, 326, 384, 448, 514, 578, 644, 703, 768, 837, 896, 957, 1021,
                                       1083, 1150, 1218, 1277, 1342, 1402, 1471, 1543, 1733, 1810])),
}


def tline(page, n):
    with open(os.path.join(UNIT, 'transcriptions', page + '.txt'), encoding='utf-8') as f:
        return f.read().split('\n')[n - 1]


# (key, group, page, first line, last line, title, note, options)
# page None = a decision with no picture.
READ = 'A. Readings, against the scans'
SUP = 'B. The supplied-text layer'
DEC = 'C. Decisions and identifications'
ROWS = [
    ('r1_verlangen', READ, '0322_a', 1, 2,
     'Top of page 2: the word before "noch mehr Schulen", and the word before "vorhanden"',
     'Line 1 now reads "für [Verlangen?] noch mehr Schulen"; line 2 "[...] nicht[?] vorhanden". '
     '"nicht" is a negation: the English says "not[?]". What does line 2 say before "vorhanden"?',
     ['nicht', 'diese / dieses (no negation)', 'a different word']),
    ('r2_verlangen_word', READ, '0322_a', 1, 1,
     'The doubtful word in line 1 ("für ... noch mehr Schulen")',
     'Now "[Verlangen?]". Is that what the page says?',
     ['Verlangen', 'Verleihung / another word']),
    ('r3_726', READ, '0318_a', 30, 30,
     'The communicants: "Männliche 72[6?] Weibliche 871 Summa 1597"',
     'The third digit of the first figure lies under an ink blot; the 6 comes from the sum '
     '1597 - 871. Is there a 6?',
     ['726 (a 6 under the blot)', 'only 72, the blot is not a digit', 'another digit']),
    ('r4_before_4rubel', READ, '0322_a', 18, 18,
     'The stroke before "4 Rubel 61 Kopeken"',
     'Now "[...] –[?] 4 Rubel 61". Is it a dash only, or the end of a lost word, or a lost first '
     'digit (14, 24 ...)?',
     ['a dash, nothing lost', 'the end of a word (e.g. "sind")', 'a digit before the 4']),
    ('r5_734', READ, '0322_b', 27, 27,
     'Pyzdry communicants: "Summa 73[4?]"',
     'The 4 is faint at the edge of the stain. 326 + 408 = 734.',
     ['734', 'another figure']),
    ('r6_taufen1', READ, '0318_a', 28, 28,
     '"Die Taufen werden[?] meistens vom Pastor voll[...]"',
     'The second reader saw no bow over the vowel after w, so "werden" (not "wurden"). Which?',
     ['werden', 'wurden']),
    ('r7_taufen2', READ, '0322_b', 22, 22,
     '"Die Taufen werden von den betreffenden Kantor[...]"',
     'The same question, in the Pyzdry report.',
     ['werden', 'wurden']),
    ('r8_religi', READ, '0322_b', 16, 16,
     '"fünf [Religi?][...] Schulen verbunden mit Bethäusern"',
     'The first reader had "Kateg[?]"; the second a capital R and "eligi". Zagórów has '
     '"Religions-Schule" in the same place.',
     ['Religi...', 'Kateg...', 'another word']),
    ('r9_kreuzen', READ, '0318_a', 26, 26,
     '"in gutem Zustande und mit Kreuzen[?] versehen"',
     '"Kreuzen" (crosses), or "Zäunen" (fences)?',
     ['Kreuzen', 'Zäunen', 'another word']),
    ('r10_gegenueber', READ, '0322_b', 28, 28,
     '"Jahre 1881 gegen über mehr 131" - one word or two?',
     'The scribe leaves a clear space in "gegen über".',
     ['two words, as written ("gegen über")', 'one word ("gegenüber")']),
    ('r11_ho', READ, '0318_a', 10, 10,
     'The letters before the burn: "habe ich die Ehre [Ho?][...]" (and the same in line 8)',
     'The twin has "habe ich die Ehre folge[nden]", and the next line begins "den". Is the '
     'doubtful "Ho" really "fo"?',
     ['Ho', 'fo', 'Ew / zu', "can't be read"]),
    ('r12_pastor', READ, '0345_a', 5, 6,
     'The strokes before "stor" at the start of lines 5 and 6',
     'The agent thought they might be a Kurrent capital P (written like "sp"): "Pastor" legible, '
     'not "[...]stor". The text now has "[...]stor".',
     ['"Pastor" is legible', 'only "stor" is legible']),
    ('r13_unbewusst', READ, '0318_a', 29, 29,
     '"Offenbarer Abendmahls-Verächter [unbewußt?]"',
     'Applied from the other report, where it reads "unbewußt". Does it say that here too?',
     ['unbewußt', 'something else']),
    ('r14_haeusliche', READ, '0322_a', 7, 7,
     '"Sittlichkeit so wie das häusliche Zusammenleben" (applied: first reading was "kirchliche")',
     'The second reader read a Kurrent h, and the other report says "häusliche".',
     ['häusliche', 'kirchliche']),
    ('r15_fast', READ, '0322_a', 2, 2,
     '"da fast jede größere Colonie eine" (applied: the first reading was "sich")',
     'Is the word after "da" "fast" or "sich"?',
     ['fast', 'sich']),
    ('r16_dieskau', READ, '0345_a', 3, 4,
     '"bei den Mis-" / "[...]diensten 3 Rubel 40" (applied: the first reading was "bei der Mis-" and "[...]ol die ersten")',
     'The second reader read "den" and "…diensten", as in "Missions-Gottesdiensten" of Zagórów.',
     ['den / diensten', 'der / "die ersten"']),
    ('s1_hochwuerden', SUP, '0318_a', 1, 3,
     'Grade A: the top left address, supply "Hochwürden dem" before "Herrn General-Superin[...]"',
     'The hole at the top left of the leaf. The other report has "Hochwürden dem Herrn General-Superinten-" '
     'on its line 2. Is the supply fair, or should the layer say nothing here?',
     ['keep it', 'drop it (the hole may never have held text)', "can't tell"]),
    ('s2_sandt', SUP, '0322_a', 6, 7,
     'Grade A: "über[...] hat" supplied "sandt" ("übersandt")',
     'The agent called the fit tight. The other report has "übersandt".',
     ['keep it', 'drop it', "can't tell"]),
    ('s3_layer_site', SUP, None, 0, 0,
     'Should the supplied-text panel appear on the published site at all?',
     'It is a first for the edition: a collapsed panel under each page, "Reconstruction of the lost '
     'edges (a proposal)", 43 proposals, grades A and B. Open it on the document pages '
     '/documents/agad14320139/1/ and /2/ once the site is up. Not in the translation, the '
     'summaries or the transcription.',
     ['show it', 'keep it off the site for now', 'show only the A grades']),
    ('d1_filial', DEC, None, 0, 0,
     'Lissewo-Pyzdry as "the filial of Zagórów"',
     'The unit title, the summaries and the holding page say "the filial Lissewo-Pyzdry"; that it '
     'belongs to the Zagórów parish rests on the same pastor and your file context, not on '
     'Erdmann\'s surviving words (the claim check flagged it). May the holding say it is the '
     'parish\'s filial?',
     ['yes, say it is the parish\'s filial', 'no, say only the same pastor']),
    ('d2_manitius', DEC, None, 0, 0,
     'Manitius: one man or two?',
     'The reports name "Superintendent Pastor Manitius at Warsaw" (mission money). The Konstantynów '
     'sample is signed "Sig. Manitius, Pastor". Same man, or only the surname?',
     ['same man', 'two men', 'leave open']),
    ('d3_diocese', DEC, None, 0, 0,
     'Which diocese Zagórów belonged to',
     'Not in Erdmann\'s pages. The Konstantynów sample names the "Ka[li]scher Diöcese". Shall I '
     'check Kneifel and Werner and say it on the holding page?',
     ['yes, check and say it', 'no, say nothing']),
    ('d4_era', DEC, None, 0, 0,
     'The era',
     '`wlodzimierz` was approved; 1882 is after Włodzimierz\'s death (1879). Keep it for these '
     'reports or ask for a later era?',
     ['keep wlodzimierz', 'ask for another era', 'no era']),
    ('d5_more_scans', DEC, None, 0, 0,
     'More scans of file 1/432/0/1/139',
     'Other parishes\' reports of the Kalisz diocese, or Erdmann\'s own reports of other years, '
     'would show his wording and could turn some C stretches into B. Can you bring more?',
     ['yes, I can add more', 'not now']),
    ('d6_next', DEC, None, 0, 0,
     'What next for this holding',
     'Not done: the index of people and places, a timeline event, the era essay, a German reader\'s '
     'review of the German text. Which shall I do?',
     ['the index of people and places', 'a timeline event', 'the era essay', 'all of them']),
]

ZOOM = 1.1


def strip_path(key):
    return os.path.join(IMG, key + '.jpg')


def build_strips():
    cache = {}
    for key, grp, page, l0, l1, title, note, opts in ROWS:
        if not page:
            continue
        dst = strip_path(key)
        if os.path.isfile(dst):
            continue
        if page not in cache:
            cache[page] = Image.open(os.path.join(SRC, f'1_432_0_1_139_{page}.jpg'))
        im = cache[page]
        w, h = im.size
        ys = Y[page]
        y0 = max(0, ys[max(1, l0 - 1)] - 55)
        y1 = min(h, ys[min(len(ys), l1 + 1)] + 55)
        crop = im.crop((0, y0, w, y1))
        crop = crop.resize((int(crop.width * ZOOM), int(crop.height * ZOOM)), Image.LANCZOS)
        crop.save(dst, quality=88)
    for page in Y:
        dst = os.path.join(IMG, f'page_{page}.jpg')
        if not os.path.isfile(dst):
            im = Image.open(os.path.join(SRC, f'1_432_0_1_139_{page}.jpg'))
            s = 1100 / im.width
            im.resize((1100, int(im.height * s)), Image.LANCZOS).save(dst, quality=85)


ANSWERS = {}
if os.path.isfile(STORE):
    with open(STORE, encoding='utf-8') as f:
        ANSWERS = json.load(f)

CSS = """
:root{--bg:#fbfaf7;--fg:#222;--mute:#666;--line:#ddd;--ok:#2a6b2a;--hi:#8a5a00;--card:#fff}
@media (prefers-color-scheme:dark){:root{--bg:#1b1a18;--fg:#e8e6e1;--mute:#9a968e;--line:#3a3834;--ok:#7fc27f;--hi:#e0b060;--card:#242320}}
body{font:16px/1.5 Georgia,serif;max-width:900px;margin:2em auto;padding:0 16px;background:var(--bg);color:var(--fg)}
h1{font-size:22px} h2{font-size:18px;margin-top:2em;border-top:2px solid var(--line);padding-top:.8em}
.row{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:12px 14px;margin:14px 0}
.row.done{border-left:5px solid var(--ok)}
.line{font-family:ui-monospace,Consolas,monospace;font-size:14px;margin:.4em 0;overflow-wrap:anywhere;color:var(--hi)}
img.strip{max-width:100%;border:1px solid var(--line);margin:.4em 0;display:block}
small{color:var(--mute)} .k{font:12px monospace;color:var(--mute)}
button{font:inherit;padding:4px 12px;margin:0 6px 6px 0;cursor:pointer;border-radius:4px;border:1px solid var(--line);background:var(--bg);color:var(--fg)}
button.on{background:var(--fg);color:var(--bg)}
input{font:inherit;width:100%;box-sizing:border-box;margin-top:4px;padding:4px 6px;background:var(--bg);color:var(--fg);border:1px solid var(--line)}
#status{position:sticky;top:0;background:var(--bg);padding:6px 0;color:var(--mute);border-bottom:1px solid var(--line)}
a{color:inherit}
"""

JS = """
const st=document.getElementById('status');
function count(){const r=document.querySelectorAll('.row'),d=[...r].filter(x=>x.dataset.v).length;st.textContent=d+' of '+r.length+' answered';}
async function save(row){
  const [other,note]=row.querySelectorAll('input');
  const body={key:row.dataset.key,reading:row.dataset.v||'',other:other.value,note:note.value};
  try{const r=await fetch('/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
      if(!r.ok)throw 0;count();}catch(e){st.textContent='Not saved - is the sheet server still running?';}
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
"""


def page_html():
    out, group, n = [], None, 0
    for key, grp, page, l0, l1, title, note, opts in ROWS:
        n += 1
        if grp != group:
            group = grp
            out.append(f'<h2>{html.escape(grp)}</h2>')
        a = ANSWERS.get(key, {})
        v = a.get('reading', '')
        lines = ''
        if page:
            lines = '<div class=line>' + '<br>'.join(
                html.escape(f'{page} line {k}: ' + tline(page, k)) for k in range(l0, l1 + 1)) + '</div>'
            lines += (f"<a href='/img/strip/{key}.jpg' target='_blank'><img class=strip "
                      f"src='/img/strip/{key}.jpg'></a>"
                      f"<small><a href='/img/page/{page}.jpg' target='_blank'>whole page {page}</a></small>")
        btns = ''.join(f"<button data-v='{html.escape(o, quote=True)}'>{html.escape(o)}</button>" for o in opts)
        btns += ("<button data-v='__other__'>Something else</button>"
                 "<button data-v='__unsure__'>Can't tell</button>")
        out.append(
            f"<div class='row' data-key='{key}' data-v='{html.escape(v, quote=True)}'>"
            f"<div><b>{n}.</b> {html.escape(title)} <span class=k>{key}</span></div>"
            f"{lines}<small>{html.escape(note)}</small>"
            f"<div style='margin-top:8px'>{btns}"
            f"<input placeholder='What the page says' value='{html.escape(a.get('other', ''), quote=True)}'"
            f"{'' if v == '__other__' else ' hidden'}>"
            f"<input placeholder='Note (optional)' value='{html.escape(a.get('note', ''), quote=True)}'></div></div>")
    return (f"<!doctype html><html lang=en><meta charset=utf-8>"
            f"<meta name=viewport content='width=device-width,initial-scale=1'>"
            f"<title>AGAD 1/432/0/1/139: Erdmann's reports of 1882 - for review</title><style>{CSS}</style>"
            f"<h1>Pastor Erdmann's reports of 1882 (AGAD 1/432/0/1/139): for your review</h1>"
            f"<p>{len(ROWS)} items: the readings left doubtful, the proposals of the supplied-text layer "
            f"worth a second look, and the decisions that are yours. Each reading shows a strip of the "
            f"page (click it to open full size) and the line as the transcription has it. \"Can't tell\" "
            f"is a fine answer. Answers save as you go. Nothing here changes the text until I apply "
            f"your answers.</p><div id=status></div>{''.join(out)}<script>{JS}</script></html>")


def read_text():
    lines = []
    for i, r in enumerate(ROWS, 1):
        a = ANSWERS.get(r[0], {})
        lines.append(f"{i}. {r[0]}: {a.get('reading', '(no answer)')}"
                     + (f" | {a['other']}" if a.get('other') else '')
                     + (f" | note: {a['note']}" if a.get('note') else ''))
    return '\n'.join(lines)


class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def _send(self, body, ctype, code=200):
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        p = self.path.split('?')[0]
        if p == '/':
            self._send(page_html().encode('utf-8'), 'text/html; charset=utf-8')
        elif p == '/answers':
            self._send(read_text().encode('utf-8'), 'text/plain; charset=utf-8')
        elif p.startswith('/img/strip/') or p.startswith('/img/page/'):
            name = os.path.basename(p)
            path = (os.path.join(IMG, name) if p.startswith('/img/strip/')
                    else os.path.join(IMG, 'page_' + name))
            if os.path.isfile(path):
                with open(path, 'rb') as f:
                    self._send(f.read(), 'image/jpeg')
            else:
                self._send(b'not found', 'text/plain', 404)
        else:
            self._send(b'not found', 'text/plain', 404)

    def do_POST(self):
        d = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        ANSWERS[d['key']] = {'reading': d.get('reading', ''), 'other': d.get('other', ''),
                             'note': d.get('note', '')}
        with open(STORE, 'w', encoding='utf-8') as f:
            json.dump(ANSWERS, f, ensure_ascii=False, indent=1)
        self.send_response(204)
        self.end_headers()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--read', action='store_true')
    ap.add_argument('--port', type=int, default=4108)
    a = ap.parse_args()
    if a.read:
        print(read_text())
        return
    build_strips()
    print(f'serving the sheet at http://127.0.0.1:{a.port}/  (answers: {STORE})', flush=True)
    http.server.ThreadingHTTPServer(('127.0.0.1', a.port), H).serve_forever()


if __name__ == '__main__':
    main()
