# -*- coding: utf-8 -*-
"""The reading sheet for APP 53/968/0/-/545: "Readings in Breyer's sheets 1".

Each row is one strip of one photographed sheet, shown as a picture, with the
draft reading of that strip beneath it and the doubtful words marked [?]. The
editor reads the strip and either confirms the draft or types what the page
says. Answers go to review/app539680545/readings1_answers.json.

    python units/app539680545/intake/spot_sheet1.py          # serve
    python units/app539680545/intake/spot_sheet1.py --read   # print answers

The strip pictures are cut from the archive images by the band crops of the
reading pass (temp folder polonisierta); this script copies the ones it needs
into review/app539680545/spot_img/ so the sheet is self-contained.
"""
import argparse
import http.server
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
import unitlib

UNIT = unitlib.one_unit('app539680545')
REV = unitlib.review_dir(UNIT.slug)
IMGDIR = os.path.join(REV, 'spot_img')
os.makedirs(IMGDIR, exist_ok=True)
STORE = os.path.join(REV, 'readings1_answers.json')

# Where the band crops lie on this machine (the reading pass of 2026-10-25).
BANDS = [r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\polonisierta\cols',
         r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\polonisierta\bands2']


def find(name):
    for d in BANDS:
        p = os.path.join(d, name + '.jpg')
        if os.path.isfile(p):
            return p
    raise SystemExit(f'missing band image {name}')


# One row per strip that carries a doubtful reading. `lines` is the draft
# reading of the strip (as the transcription has it); the editor's eye
# settles the [?] words.
ROWS = [
    ('p25b0', 'p25f_b0', ['P. Winkler Polonisiert Namen.'],
     'The heading. Is it "Polonisiert Namen" or "Polonischer Namen"?'),
    ('p25b1', 'p25f_b1', ['7. 1855 Bobbe[?] - Rybicki.'],
     'The first pair and the "7. 1855" before it.'),
    ('p25b2', 'p25f_b2', ['Gem. Lagiewniki[?]', 'Grünberg - Zieliński.',
                          'Schröcke[?] - Frisierski[?]'],
     'Three lines. The "Gem." line, then Grünberg, then Schröcke.'),
    ('p25b3', 'p25f_b3', ['Breitkreutz - Breitkrejc.',
                          'Schmeckel[?] - Kmiqielski[?]'],
     'The second line: the reads disagree (Schmeckel/Schneetel; '
     'Kmiqielski/Smiqielski/Kniqielski).'),
    ('p25b4', 'p25f_b4', ['Betke - Bedeka[?]', 'Gerke - Gierka.'],
     'Is the Polonised form "Bedeka", "Biertka" or something else? '
     'And "Gierka" or "Giertka"?'),
    ('p25b5', 'p25f_b5', ['Harge[?] - Ktarga[?]', 'Subke[?] - Gurz[?]'],
     'Both pairs. The first name was read Harge/Starse.'),
    ('p25b6', 'p25f_b6', ['Waldowski[?]', '1843. Fruberski[?]'],
     'The tail of the page. "Waldowsch. Frubersh." as one or two lines?'),
    ('p25b7', 'p25f_b7', [],
     'The last line of the page, read once as "1873. Universal.", '
     'once as "1893. Gruberstr.". What does it say?'),
    ('p26b0', 'p26_b0', ['Polonizator[?]', 'Sint.[?] Blann.[?]',
                         '1. Mittmann - Nowak'],
     'The heading lines above the list.'),
    ('p26b1', 'p26_b1', ['2. Berwald - Jagodziński',
                         '3. Rode - Czerwiński[?]',
                         '4. Naeghyall[?] - Storowski[?]',
                         '5. Fuhrmann - Fuhrmannski[?]'],
     'Lines 3 to 5: the Polonised forms were read variously '
     '(Czerwiński/Czrzewinski/Ozrzewinski; Storowski/Horovinski; '
     'Fuhrmannski/Fukrmannski).'),
    ('p26b2', 'p26_b2', ['6. Rotloff - Surowiecki[?]', '7. Krebs - Rakowski[?]',
                         '8. Will - Dzikowski', '9. Pidda - Peda'],
     'Lines 6 and 7: Surowiecki/Surowrecki, Rakowski/Dakowski.'),
    ('p26b3', 'p26_b3', ['10. Pidda - Studziński[?]',
                         '11. Sekinike[?] - Stodulski[?]'],
     'Line 11: the German name was read Sekinike/Soliinke/Tokienke.'),
    ('p26b4', 'p26_b4', ['14. Neuwert - Nowaczyński[?]',
                         '15. Martin - Marcinkowski',
                         '16. Nahr[?] - Koguciński'],
     'Line 14: the Polonised form was read Nowaczyński/Nowaerypki. '
     'Line 16: Mahn or Nahr?'),
    ('p26b5', 'p26_b5', ['18. Kybs - Kübsch', '19. Brodel - Brudel'],
     'Line 18: Kybs or Tybs? Kübsch or Hübsch?'),
    ('p27b0', 'p27_b0', ['A. Arminski,',
                         'B. Bartmanski, Brojerski, Bartnowski, '
                         'Bauerowicz[?],'],
     'The B line: is the last name "Bauerowicz" or "Bauerschwiez"? '
     'And "Brojerski" or "Brojeski"?'),
    ('p27b1', 'p27_b1', ['D. Donarski,',
                         'F. Funkiewicz, Festerkiewicz[?], '
                         'Frydrychowski[?], Feterowski[?],',
                         'G. Gutwiński,',
                         'H. Holendajski, Hendzelewski[?], Hirszowski,'],
     'The F line and the H line. F: Festerkiewicz? Frydrychowski? '
     'Feterowski? H: Hendzelewski/Nedzelewski/Hendrelewski? '
     'Hirszowski or Hirszewski?'),
    ('p27b2', 'p27_b2', ['J. Jursowski[?]',
                         'K. Kuntski, Kurzmanowski[?], Knapski, '
                         'Kirschkowski,',
                         'L. Licznerowski, Lernaciński, Lencewicz, '
                         'Langowski,',
                         'M. Murnerowski, Mieklewski, Mundkowski, '
                         'Mystelkowski,',
                         'N. Najderski,'],
     'The J line (Jursowski or Jurzowski); K (Kurzmanowski?); '
     'L (Lencewicz? Langowski?); M (Murnerowski? Mystelkowski?).'),
    ('p27b3', 'p27_b3', ['O. Oberski,', 'P. Palmowski,',
                         'R. Ringwelski, Rosenkiewicz, Retelewski, '
                         'Reinowski,',
                         'S. Schmiedcki[?], Sendowrz[?], Sulborski,'],
     'The S line: the three names were read variously '
     '(Schmidcki/Schmiedzeki/Schmielecki; Semidowrz/Sendowrz/Smidowrz; '
     'Sulborski). Also Rosenkiewicz (Ranzenkiewicz?).'),
    ('p27b4', 'p27_b4', ['W. Weynerowski, Wilmański,'],
     'The W line (Weynerowski or Heynerowski?). Are T, U, V, Z really '
     'empty on the page?'),
    ('p28b0', 'p28_b0', ['Polnische[?] deutsche Briefe von George Schlag,'],
     'The first line of the excerpt heading.'),
    ('p28b1', 'p28_b1', ['Morgenprediger zu St. Hieronymi u. der polnischen',
                         'Schule verordneter Moderator.',
                         'Breslau, den 18. September 1741.',
                         'Wojciech Wilkotek - Albrecht Bärwolf[?]'],
     'The rest of the heading and the first pair. "Breslau" or '
     '"Bruselau"? And the second name: Bärwolf? Bärwinkel?'),
    ('p28b2', 'p28_b2', ['Jakub Maślanka - Jacob Buttermilch',
                         'Tomasz Kapusta - Thomas Erzont[?]',
                         'Tomas[?] Klotomecki[?] - Thomas Goldmann',
                         'Jan Tarnowski[?] - John Tannon[?]'],
     'Four pairs. The Polonised names read variously: Kapusta; '
     'Klotomecki/Kłotomeksi; Tarnowski/Ternowski. The German: Erzont? '
     'Tannon?'),
    ('p28b3', 'p28_b3', ['Michał Kierznicki[?] - Michael Strauch',
                         'Jerzy Samotyia[?] - George Selbstfell[?]',
                         'Jakub Wierzbrecki[?] - Jacob Weidner[?]'],
     'Three pairs: Kierznicki? Samotyia? Selbstfell? Wierzbrecki? '
     'Weidner?'),
    ('p29top', 'p29_top', ['Polonisazja[?] techniczna[?]',
                           '[Rocle?] - Rola[?]', 'Sack[?] - Lak[?]',
                           'Riebschel[?] - Rysel[?]', 'Pall[?] - Pal[?]'],
     'The heading of the sheet and the pairs under it, top right. '
     'The reads disagree on almost every name.'),
    ('p29c0a', 'p29_c0_a', ['1. Bartmanski', '2. Schmielecki',
                            '3. Funkiewicz', '4. Sulborski',
                            '5. Riewe[?] - Riwa[?]'],
     'The first column, numbers 1 to 5. Is number 5 a pair '
     '"Riewe - Riwa", and what are the two names?'),
    ('p29c0b', 'p29_c0_b', ['6. Ringwelski', '7. Festerkiewicz',
                            '8. Hassewicz[?]', '9. Brojerski',
                            '10. Murnerowski', '11. Rosenkiewicz',
                            '12. Kuntski', '13. Micklewski',
                            '14. Purgowski', '15. Mundkowski',
                            '16. Licznerowski', '17. Bartnowski',
                            '18. Holendajski', '19. Lernaciński',
                            '20. Mystelkowski[?]',
                            '21. Mlyptkowski[?]', '22. Bauerowicz',
                            '23. Lencewicz', '24. Frydrychowski',
                            '25. Sekerowski[?]'],
     'The first column, numbers 6 to 20, and the second column, '
     '21 to 25. Doubtful: 8 (Hassewicz?), 13 (Micklewski?), '
     '20 (Mystelkowski?), 21 (Mlyptkowski?), 25 (Sekerowski? '
     'Kuzmarowski?).'),
    ('p29c1b', 'p29_c1_b', ['26. Hendzelewski[?]', '27. Folkierski',
                            '28. Hirzowski[?]', '29. Hirszowski',
                            '30. Weynerowski', '31. Herschlewski[?]',
                            '32. Knapski', '33. Kirschkowski',
                            '34. Wilmański', '35. Retelewski',
                            '36. Palmowski', '37. Mellerowicz',
                            '38. Donarski', '39. Najderski',
                            '40. Gutwiński', '41. Kornowski[?]',
                            '42. Heymowski[?]'],
     'The second column. Doubtful: 26, 28 (Hirzowski or Hirszowski?), '
     '31 (Herschlewski? Henschlewski?), 41 (Kornowski?), '
     '42 (Heymowski?).'),
    ('p29c3', 'p29_c3pairs', ['Gross[?] - Grosz[?]', 'Rosin[?] - Rosyp[?]',
                              'Hahnirt[?] - Hanus[?]', 'Brick[?] - Brych[?]',
                              'Bordel[?] - Bordo[?]',
                              'Avon[?] - Mianowski[?]'],
     'The pairs column. Each pair: what does the page say on either '
     'side of the dash? The reads disagree on nearly all.'),
    ('p29c3b', 'p29_c2_b', ['Gaensler[?] - Gasiorowski[?]',
                            'Blum[?] - Koziatkowska[?]',
                            'Erdmann[?] - Zieminski[?]',
                            'Hoppe - Chmielewski',
                            'Lemke[?] - Lemrock[?]', 'Born[?] - Borna[?]',
                            '43. Arminski', '44. Kindelski',
                            '45. Reinowski', '46. Kuncewicz[?]',
                            '47. Hardkowski', '48. Weglerski[?]'],
     'The pairs column, lower half, then the end of the numbered list. '
     'Is there one line "Borckl - Boryl" or two (also "Brill - Boryl")? '
     'Doubtful: Gąsiorowski, Koziatkowska, Zieminski, Lemke, Borna, '
     '46 (Kuncewicz?), 48 (Weglerski?).'),
    ('p30c0', 'p30_c0_a', ['49. Oberski', '50. Langowski',
                           '51. Sabss[?]', '52. Maldelin[?]',
                           '53. Melerowicz[?]'],
     'The end of the numbered list. Doubtful: 51, 52, 53. '
     'The whole-page read had "51. Salto Karlowski", "52. Madalinski - '
     'Miele", "53. Melerovolz".'),
    ('p30c1', 'p30_c1_a', [],
     'Four short lines below the list (read once as "Bwhre / Them. / '
     'Bomfurtun. / evangelesy."). What do they say?'),
    ('p30c2', 'p30_c2_a', [],
     'More short lines on the same page (read once as "sirdorfki", '
     '"motzungen"). What do they say?'),
]

ANSWER_KEYS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def page_html():
    rows = []
    for i, (key, img, lines, note) in enumerate(ROWS, 1):
        ls = '<br>'.join(
            l.replace('[?]', '<span class=q>[?]</span>') for l in lines) or \
            '<i>(nothing read)</i>'
        rows.append(
            f"<div class=row data-key='{key}'>"
            f"<div><b>{i}.</b> <span class=k>{key}</span></div>"
            f"<a href='/spot_img/{img}.jpg' target='_blank'>"
            f"<img src='/spot_img/{img}.jpg'></a>"
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
<title>Readings in Breyer's sheets 1 - APP 53/968/0/-/545</title>
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
<h1>Readings in Breyer's sheets 1 &mdash; APP 53/968/0/-/545</h1>
<p>Each row is one strip of a photographed sheet. The draft reading is under
the picture, doubtful words marked <span class=q>[?]</span>. Read the strip
and either take the draft as it stands or type what the page says &mdash;
line by line, in the "Something else" box, is welcome. The strips overlap a
little where a line sat across two of them.</p>
<div id=rows>{''.join(rows)}</div>
<p>When you have worked down the page, the answers are saved as you go.</p>
<script>
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
var ANSWERS = {json.dumps(ANSWERS, ensure_ascii=False)};
</script></body></html>"""


def read_html():
    rows = []
    for i, (key, img, lines, note) in enumerate(ROWS, 1):
        a = ANSWERS.get(key, {})
        rows.append(f"<p><b>{i}. {key}</b> &mdash; {a.get('reading', '(no answer)')}"
                    f"{(' &mdash; ' + a['other']) if a.get('other') else ''}"
                    f"{(' &mdash; note: ' + a['note']) if a.get('note') else ''}</p>")
    return ('<html><meta charset=utf-8><body><h1>Answers, readings1</h1>'
            + '\n'.join(rows) + '</body></html>')


ANSWERS = {}
if os.path.isfile(STORE):
    with open(STORE, encoding='utf-8') as f:
        ANSWERS = json.load(f)

for key, img, lines, note in ROWS:
    src = find(img)
    dst = os.path.join(IMGDIR, img + '.jpg')
    if not os.path.isfile(dst):
        shutil.copyfile(src, dst)


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
    ap.add_argument('--port', type=int, default=4103)
    a = ap.parse_args()
    if a.read:
        if not ANSWERS:
            print('no answers yet')
        for key, a_ in ANSWERS.items():
            print(key, '|', a_.get('reading', ''), '|', a_.get('other', ''),
                  '|', a_.get('note', ''))
        return
    print(f'readings1 at http://127.0.0.1:{a.port}/  -  answers go to {STORE}')
    http.server.HTTPServer(('127.0.0.1', a.port), H).serve_forever()


if __name__ == '__main__':
    main()
