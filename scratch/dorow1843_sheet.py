# -*- coding: utf-8 -*-
"""The spot sheet "Dorow (1843), Triebenfeld's memoir: the doubtful readings".

    python scratch/dorow1843_sheet.py           # serve on port 4132
    python scratch/dorow1843_sheet.py --read    # print the answers

The same page and saving as scratch/werner1904_sheet.py, with its own rows and
its own crops, cut from the SBB digitisation of Dorow's Erlebtes, II. Theil
(C:/Users/Tersnaus/Downloads/"Erlebtes aus den Jahren 1813-1820 (Dorow, 1843).pdf",
the PDF's pages 32-45 = the memoir's title leaf, its motto leaf and printed
pp. 13-24). The readings behind the draft:

  - Tesseract 5.5.3, the script/Fraktur model from tessdata_best fetched into
    %LOCALAPPDATA%\\Tesseract\\tessdata, whole pages at 300 dpi, doubtful lines
    re-read as 900 dpi bands in Fraktur and deu
  - the Materialien (1861), which reprints this memoir (in extract,
    pp. 205-216), read line against line as the human witness

The print is Fraktur; the long s and the tz ligature drive most of the noise.
The rows below are what the passes and the reprint did not settle. Each row's
picture is cut from the page itself; the first button is what the transcription
has now. Answers go to review/dorow1843/query_answers.json.
"""
import io, json, os, argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCAN_DIR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\dorow300'
REV = os.path.join(ROOT, 'review', 'dorow1843')
IMG = os.path.join(REV, 'spot_img')
STORE = os.path.join(REV, 'query_answers.json')
PORT = 4132

# (key, page image, y-range fractions of the page image, draft, options, note)
ROWS = [
    ('procent5', 'm35.png', (0.72, 0.92), '9 Procent',
     '5 Procent|9 Procent',
     '"...waeren die Abgaben vieler Gueter, wo ... klassificirt hatten, '
     'kaum ? Procent gegen den alten Satz betragen haben." (printed p. 14). '
     'The digit is the question: the Fraktur pass reads 9, the deu pass and '
     'the Materialien\'s reprint (1861, p. 206, where the extract sets its own '
     '"(?-)" pointer after the sentence) read 5.'),
    ('gebauset', 'm36.png', (0.20, 0.36), 'gebauset',
     'gebauset|gehauset',
     '"...auf den Plaetzchen aufgefuehrt wurden, wo er und seine Ureltern '
     'ge-?uset hatten." (printed p. 15). The letters under "ge-?uset" are the '
     'question: every OCR pass reads b, the Materialien\'s reprint (p. 207) '
     'prints "gehauset".'),
    ('offizianten', 'm36.png', (0.58, 0.74), 'Offizcianten',
     'Offizcianten|Offizianten|Officianten',
     '"Ein Heer Justizkommissarien ... folgte ihnen, Offiz-?ianten mit hohlen '
     'Augen" (printed p. 15, the word across the line break). The whole word '
     'is the question: the line ends "Offiz" and the next begins what the '
     'passes read "cianten"; printed p. 17 spells the same word whole as '
     '"Offizianten" (both passes), the Materialien\'s reprint prints '
     '"Officianten" (p. 208).'),
    ('wirkungskreis', 'm42.png', (0.08, 0.26), 'Würkungskreis',
     'Würkungskreis|Wirkungskreis',
     '"Hätte Hoym dies Zutrauen des Königs benutzt, so hätte er den größten '
     'W?rungskreis haben..." (printed p. 21). The vowel is the question: both '
     'passes read Wür-, the Materialien\'s reprint (p. 213) prints '
     '"Wirkungskreis"; "Würkung" is an attested older form of Wirkung, so '
     'the print may stand as read.'),
    ('bewuerken', 'm42.png', (0.70, 0.88), 'bewürken',
     'bewürken|bewirken',
     '"Hoym hatte den Pohlen ... ein Kreditsystem zu bew?rken, auf das '
     'heiligste versichert..." (printed p. 21, the line at the top of the '
     'picture). The same Würkung/Wirkung question as the row above.'),
    ('kukken', 'm44.png', (0.64, 0.82), 'kukken',
     'kukken|kuffen',
     '"...weil man sich nicht dürfte von einem Manne, der mit dem '
     'Königlichen Hause so nahe verwandt sey, in die Charte ? lassen." '
     '(printed p. 23, the last line of the picture). The word is the '
     'question: the passes read "fuffen" (Fraktur k reads as f), the '
     'Materialien\'s reprint (p. 215) prints "kukken".'),
    ('michelis', 'm43.png', (0.78, 0.96), 'Michelis',
     'Michelis|Michaelis',
     '"Ein gewisser M?chelis war der Justiziarius der Wittwenkasse." '
     '(printed p. 22, near the foot of the picture). The vowel(s) are the '
     'question: the passes read Michelis, the Materialien\'s reprint (p. 214) '
     'prints "Michaelis".'),
    ('titelwort', 'm32.png', (0.06, 0.44), 'Pohlen',
     'Pohlen|Polen',
     'The memoir\'s title leaf (unnumbered, before printed p. 13): the big '
     'display line(s) above "unter Friedrich II. und Friedrich Wilhelm II." '
     'is the question - the display face defeats the OCR, which reads '
     'fragments ("Po hk eM", "Pohle"). The 1861 reprint\'s heading and the '
     'volume\'s own contents list the piece as "Pohlen unter Friedrich II. '
     'und Friedrich Wilhelm II.", so Pohlen is expected.'),
    ('siehe', 'm32.png', (0.06, 0.44), 'Siehe I. Theil Seite 19.',
     'Siehe I. Theil Seite 19.|Siehe 1. Theil Seite 19.|Siehe Isten Theil Seite 19.',
     'The cross-reference at the foot of the same title leaf, pointing to the '
     'telling of the memoir\'s origin in part I. The form of the numeral is '
     'the question: the passes read "1r Theil" / "Ir Theil".'),
]

PAGES = ['m32.png', 'm33.png', 'm34.png', 'm35.png', 'm36.png', 'm37.png',
         'm38.png', 'm39.png', 'm40.png', 'm41.png', 'm42.png', 'm43.png',
         'm44.png', 'm45.png']

PAGE = """<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<style>
:root{--bg:#fbfaf7;--fg:#222;--mute:#666;--line:#ddd;--ok:#2a6b2a;--hi:#8a5a00;--card:#fff}
@media (prefers-color-scheme:dark){:root{--bg:#1b1a18;--fg:#e8e6e1;--mute:#9a968e;--line:#3a3834;--ok:#7fc27f;--hi:#e0b060;--card:#242320}}
body{font:16px/1.5 Georgia,serif;max-width:960px;margin:2em auto;padding:0 16px;background:var(--bg);color:var(--fg)}
.row{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:12px 14px;margin:12px 0}
.row.done{border-left:5px solid var(--ok)}
.w{color:var(--hi);font-weight:bold}
small{color:var(--mute)}button{font:inherit;padding:4px 12px;margin:0 6px 6px 0;cursor:pointer;border-radius:4px;border:1px solid var(--line);background:var(--bg);color:var(--fg)}
button.on{background:var(--fg);color:var(--bg)}input{font:inherit;width:100%;box-sizing:border-box;margin-top:4px;padding:4px 6px;background:var(--bg);color:var(--fg);border:1px solid var(--line)}
#status{position:sticky;top:0;background:var(--bg);padding:6px 0;color:var(--mute)}a{color:inherit}
img{max-width:100%;border:1px solid var(--line);margin:.3em 0}
</style>
<h1>__TITLE__: __N__ items</h1>
<p>The memoir's fourteen pages are shown whole below, each row then shows its
own place close up. Every row is a word the OCR readings and the Materialien's
reprint did not settle. The first button is what the transcription draft has
now. Pick what the page shows, type it under "Something else", or say you
cannot tell. Answers save as you go.</p>
<div id="status"></div>
__PAGES__
__ROWS__
<script>
const st=document.getElementById('status');
function count(){const r=document.querySelectorAll('.row'),d=[...r].filter(x=>x.dataset.v).length;st.textContent=d+' of '+r.length+' answered';}
async function save(row){
  const [other,note]=row.querySelectorAll('input');
  const body={key:row.dataset.key,reading:row.dataset.v||'',other:other.value,note:note.value};
  try{const r=await fetch('/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
      if(!r.ok)throw 0;count();}catch(e){st.textContent='Not saved - is dorow1843_sheet.py still running?';}
}
document.querySelectorAll('.row').forEach(row=>{
  const bs=[...row.querySelectorAll('button')],[other,note]=row.querySelectorAll('input');
  function set(v){row.dataset.v=v;row.classList.toggle('done',!!v);
    bs.forEach(b=>b.classList.toggle('on',b.textContent===v));save(row);}
  bs.forEach(b=>b.onclick=()=>set(b.textContent));
  other.oninput=()=>{if(other.value){row.dataset.v=other.value;row.classList.add('done');
    bs.forEach(b=>b.classList.remove('on'));save(row);}};
});
count();
</script>
"""


def crops():
    os.makedirs(IMG, exist_ok=True)
    for page in PAGES:
        im = Image.open(os.path.join(SCAN_DIR, page))
        im.save(os.path.join(IMG, page), quality=92)
    for key, page, (y0, y1), _draft, _opts, _note in ROWS:
        im = Image.open(os.path.join(SCAN_DIR, page))
        w, h = im.size
        c = im.crop((int(w * 0.05), int(h * y0), int(w * 0.98), int(h * y1)))
        c = c.resize((c.width * 3, c.height * 3), Image.LANCZOS)
        c.save(os.path.join(IMG, key + '_0.png'))


def pages_html():
    return '\n'.join('<img src="/img/%s">' % p for p in PAGES)


def rows_html():
    out = []
    for key, page, _yr, draft, opts, note in ROWS:
        btns = ''.join('<button>%s</button>' % o for o in opts.split('|'))
        out.append('<div class="row" data-key="%s"><p><span class="w">%s</span> '
                   '&mdash; %s</p><img src="/img/%s_0.png"><p>%s</p><div>%s</div>'
                   '<input placeholder="Something else">'
                   '<input placeholder="Note (optional)"></div>'
                   % (key, draft, note, key, draft, btns))
    return '\n'.join(out)


class S(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _img(self, name):
        p = os.path.join(IMG, name)
        if not os.path.isfile(p):
            self.send_error(404)
            return
        ctype = 'image/png' if name.endswith('png') else 'image/jpeg'
        with open(p, 'rb') as f:
            self.send_response(200)
            self.send_header('Content-Type', ctype)
            self.end_headers()
            self.wfile.write(f.read())

    def do_GET(self):
        if self.path.startswith('/img/'):
            self._img(self.path[5:])
            return
        page = (PAGE.replace('__TITLE__', 'Dorow (1843), Triebenfeld\'s '
                             'memoir: the doubtful readings')
                    .replace('__N__', str(len(ROWS)))
                    .replace('__PAGES__', pages_html())
                    .replace('__ROWS__', rows_html()))
        body = page.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        n = int(self.headers.get('Content-Length', 0))
        data = json.loads(self.rfile.read(n).decode('utf-8'))
        store = {}
        if os.path.isfile(STORE):
            with io.open(STORE, encoding='utf-8') as f:
                store = json.load(f)
        store[data['key']] = data
        with io.open(STORE, 'w', encoding='utf-8') as f:
            json.dump(store, f, ensure_ascii=False, indent=1, sort_keys=True)
        self.send_response(200)
        self.end_headers()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--read', action='store_true')
    a = ap.parse_args()
    if a.read:
        with io.open(STORE, encoding='utf-8') as f:
            store = json.load(f)
        for k, v in sorted(store.items()):
            print(k, '->', v['reading'] or '(none)',
                  (' | other: ' + v['other']) if v.get('other') else '',
                  (' | note: ' + v['note']) if v.get('note') else '')
        return
    crops()
    print('serving on http://127.0.0.1:%d  (Ctrl-C to stop)' % PORT)
    HTTPServer(('127.0.0.1', PORT), S).serve_forever()


if __name__ == '__main__':
    main()
