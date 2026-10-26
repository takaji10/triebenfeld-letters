# -*- coding: utf-8 -*-
"""The spot sheet "Rostworowski (1918), the Dziennik: the doubtful readings".

    python scratch/rostworowski1918_sheet.py           # serve on port 4110
    python scratch/rostworowski1918_sheet.py --read    # print the answers

The same page and saving as scratch/werner1904_sheet.py, with its own rows
and its own crops, cut from the SBC digitisation of the Dziennik
(C:/Users/Tersnaus/Downloads/89178_Rostworowski_Micha_1864-1940_Materya_y_
do_dziejow__PDF.pdf; PDF page = printed page + 22). The readings behind the
draft:

  - the PDF's own text layer against a lunaroute OCR pass over each kept
    page at 300 dpi - the images could not be read directly in the session,
    so no zoom pass was possible
  - the doubtful spots re-cut here at 600 dpi, each from the text layer's
    own word positions

The three printed pages 321-323 are shown whole below (upscaled), each row
then shows its own place close up. Each row is a word or name the two
witnesses did not settle, and the last row is the structure question of the
stray line between protocols Nr. 2 and Nr. 3. Each row's first button is
what the transcription has now. Answers go to
review/rostworowski1918/query_answers.json.
"""
import io, json, os, argparse
from http.server import HTTPServer, BaseHTTPRequestHandler

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PDF = (r'C:\Users\Tersnaus\Downloads'
       r'\89178_Rostworowski_Micha_1864-1940_Materya_y_do_dziejow__PDF.pdf')
REV = os.path.join(ROOT, 'review', 'rostworowski1918')
IMG = os.path.join(REV, 'spot_img')
STORE = os.path.join(REV, 'query_answers.json')
PORT = 4110

# The printed pages shown whole for context (PDF index, file name), printed
# 321-323: protocol Nr. 3 runs from the "Nr. 3-ci." heading on 321 to just
# before "Nr. 4." on 323.
PAGES_SHOWN = [(342, 'p321.jpg'), (343, 'p322.jpg'), (344, 'p323.jpg')]

# (key, PDF page index, search needle or None, draft, options, note).
# The needle is located by the PDF's own text layer; the crop is the word
# plus a margin, rendered at 600 dpi. key 'stray' builds its box from two
# needles (the signature of Nr. 2 to the heading of Nr. 3).
ROWS = [
    ('sum', 343, 'SOO/m', '500/m', '500/m|300/m|SOO/m as the layer has it',
     'The sum to forward to the army: "ażeby tu dla wojska wyliczyć i zaraz '
     'przesłać do wojska ?/m, a tam assygnować tymże kupcom" (the pay '
     'negotiation with Küssel, Senior of the Merchants\' Confraternity). The '
     'layer reads SOO/m - its S for 5, the usual misread - the OCR 300/m; '
     'the transcript took 500/m. A figure: the editor\'s eye.'),
    ('anzeatyczny', 343, 'anzeatyeznym', 'anzeatyeznym',
     'anzeatyeznym|anzeatycznym',
     '"powiadają, że myślą zrobić to miasto a——, wolnym" (the Dresden '
     'leavers\' plan). No Polish word traced; the sentence\'s sense is "make '
     'that city …, free". The layer letters anzeatyeznym, the OCR '
     'anzeatycznym; the transcript kept the layer\'s letters, and the '
     'English carries "anzeatyczna".'),
    ('xze', 343, 'zapewnił', 'X-żę', 'X-żę|X-że|X-ążę',
     '"? Dyrektor zapewnił, iż się w wojsku żadnego lękać nie potrzeba '
     'poruszenia" - the Prince Director of War, the print\'s abbreviation of '
     'Książę. The layer X-żę, the OCR X-że; the sense wants the nominative '
     'X-ążę. What the print abbreviates is the question.'),
    ('riviera', 343, 'Riviera', 'Riviera Załuski', 'Riviera Załuski|Riviera, Załuski',
     '"ma jechać Riviera Załuski, Wołoski, Nakwaski" (the Dresden list, '
     'after "Wyjechał Horodyński, Gliszczyński, Czarnecki"). Whether '
     'Riviera is a man beside Załuski, Wołoski and Nakwaski, or one name '
     'with Załuski, is the question.'),
    ('sciagnianym', 343, 'ciągn', 'ściągniąnym',
     'ściągniąnym|ściągnionym|ścięgniąnym',
     '"że pod Augustowem na to jedynie jest ścią——, żeby było rozbrojone" '
     '(the army drawn together under Augustów, fearing disarmament). The '
     'layer\'s form ściągniąnym kept, the OCR ścięgniąnym; what the print '
     'writes of what sense would give as ściągnionym is the question.'),
    ('kaiena', 344, 'Kaiena', 'Kaiena', 'Kaiena|Kajena',
     'The Kościan bailiffs in the nominations Łubieński sent with protocol '
     'Nr. 3: "Sąd Kościański (Komornicy): Józef Dąmbrowski, ?" - a name not '
     'traced; both witnesses agree on the letters.'),
    ('stray', 342, None, "Nr. 2's matter (left out)",
     "Nr. 2's matter (left out)|Inside Nr. 3 (add it)",
     'The line "Nominowani zostali do konsystorza Luterskiego w Płocku." '
     'stands between protocol Nr. 2\'s "Łubieński." signature and the '
     '"Nr. 3-ci." heading (the picture shows all three). The transcript '
     'took it for Nr. 2\'s closing item, as Nr. 3 closes with its own '
     'postscript after the signature, and left it out; if the print meant '
     'it inside Nr. 3, the excerpt misses one sentence of it.'),
]

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
<p>The three printed pages 321-323 of the Dziennik are shown whole below
(upscaled), each row then shows its own place close up. Every row is a word
or name the two readings did not settle - the digitisation's own text layer
against an OCR pass over the 300 dpi pages - and the last row is the
structure question of the stray line between protocols Nr. 2 and Nr. 3.
The first button is what the transcription has now. Pick what the page
shows, type it under "Something else", or say you cannot tell. Answers
save as you go.</p>
<div id="status"></div>
<img src='/img/p321.jpg'>
<img src='/img/p322.jpg'>
<img src='/img/p323.jpg'>
__ROWS__
<script>
const st=document.getElementById('status');
function count(){const r=document.querySelectorAll('.row'),d=[...r].filter(x=>x.dataset.v).length;st.textContent=d+' of '+r.length+' answered';}
async function save(row){
  const [other,note]=row.querySelectorAll('input');
  const body={key:row.dataset.key,reading:row.dataset.v||'',other:other.value,note:note.value};
  try{const r=await fetch('/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
      if(!r.ok)throw 0;count();}catch(e){st.textContent='Not saved - is rostworowski1918_sheet.py still running?';}
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
    import fitz
    from PIL import Image
    os.makedirs(IMG, exist_ok=True)
    doc = fitz.open(PDF)
    for idx, name in PAGES_SHOWN:
        pix = doc[idx].get_pixmap(dpi=300)
        im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
        big = im.resize((int(im.width * 1.4), int(im.height * 1.4)), Image.LANCZOS)
        big.save(os.path.join(IMG, name), quality=80)
    for key, pidx, needle, _draft, _opts, _note in ROWS:
        page = doc[pidx]
        if needle:
            hits = page.search_for(needle)
            if not hits:
                raise SystemExit('needle %r not found on PDF page %d'
                                 % (needle, pidx + 1))
            r = hits[0]
            box = (r.x0 - 120, r.y0 - 8, r.x1 + 120, r.y1 + 8)
        else:                      # the stray line: signature to heading
            a = page.search_for('Łubieński.')[0]
            b = page.search_for('Nr. 3-ci')[0]
            box = (a.x0 - 20, a.y0 - 12, page.rect.width - 60, b.y1 + 12)
        pix = page.get_pixmap(dpi=600, clip=fitz.Rect(*box))
        pix.save(os.path.join(IMG, key + '_0.png'))
    doc.close()


def rows_html():
    out = []
    for key, _pidx, _needle, draft, opts, note in ROWS:
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
        page = (PAGE.replace('__TITLE__', 'Rostworowski (1918), the Dziennik: '
                             'the doubtful readings')
                    .replace('__N__', str(len(ROWS)))
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
