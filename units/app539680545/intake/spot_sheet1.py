# -*- coding: utf-8 -*-
"""The reading sheet for APP 53/968/0/-/545: "Readings in Breyer's sheets 1".

Each row is one region of one photographed sheet, shown as a picture cut from
the original image with generous margins (the first cuts took the band
boundaries of the reading pass and sliced through lines; the editor,
2026-10-25), with the draft reading of that region beneath it and the
doubtful words marked [?]. The editor reads the strip and either confirms the
draft or types what the page says. Every row also links the whole sheet.
Answers go to review/app539680545/readings1_answers.json.

    python units/app539680545/intake/spot_sheet1.py          # serve
    python units/app539680545/intake/spot_sheet1.py --read   # print answers

The pictures are cut from the unit's raw images by build_strips() into
review/app539680545/spot_img/, so the sheet is self-contained.
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

UNIT = unitlib.one_unit('app539680545')
REV = unitlib.review_dir(UNIT.slug)
IMGDIR = os.path.join(REV, 'spot_img')
os.makedirs(IMGDIR, exist_ok=True)
STORE = os.path.join(REV, 'readings1_answers.json')

# One row per region that carries a doubtful reading. The rect is the region
# of the sheet in its own pixels (x0, y0, x1, y1), cut with the margins it
# has here - generous, so no line is sliced. `lines` is the draft reading of
# the region (as the transcription has it).
SHEETS = {25: '0025', 26: '0026', 27: '0027', 28: '0028', 29: '0029', 30: '0030'}

ROWS = [
    ('p25b0', 25, (0, 0, 2861, 430), ['P. Winkler Polonisiert Namen.'],
     'The heading. Is it "Polonisiert Namen" or "Polonischer Namen"?'),
    ('p25b1', 25, (0, 130, 2861, 670), ['7. 1855 Bobbe[?] - Rybicki.'],
     'The first pair and the "7. 1855" before it.'),
    ('p25b2', 25, (0, 370, 2861, 910), ['Gem. Lagiewniki[?]',
                                        'Grünberg - Zieliński.',
                                        'Schröcke[?] - Frisierski[?]'],
     'Three lines. The "Gem." line, then Grünberg, then Schröcke.'),
    ('p25b3', 25, (0, 610, 2861, 1150), ['Breitkreutz - Breitkrejc.',
                                         'Schmeckel[?] - Kmiqielski[?]'],
     'The second line: the reads disagree (Schmeckel/Schneetel; '
     'Kmiqielski/Smiqielski/Kniqielski).'),
    ('p25b4', 25, (0, 850, 2861, 1390), ['Betke - Bedeka[?]',
                                         'Gerke - Gierka.'],
     'Is the Polonised form "Bedeka", "Biertka" or something else? '
     'And "Gierka" or "Giertka"?'),
    ('p25b5', 25, (0, 1090, 2861, 1630), ['Harge[?] - Ktarga[?]',
                                          'Subke[?] - Gurz[?]'],
     'Both pairs. The first name was read Harge/Starse.'),
    ('p25b6', 25, (0, 1330, 2861, 1870), ['Waldowski[?]',
                                          '1843. Fruberski[?]'],
     'The tail of the page. "Waldowsch. Frubersh." as one or two lines?'),
    ('p25b7', 25, (0, 1570, 2861, 1929), [],
     'The last line of the page, read once as "1873. Universal.", '
     'once as "1893. Gruberstr.". What does it say?'),
    ('p26b0', 26, (0, 0, 1849, 620), ['Polonizator[?]', 'Sint.[?] Blann.[?]',
                                      '1. Mittmann - Nowak'],
     'The heading lines above the list.'),
    ('p26b1', 26, (0, 340, 1849, 1060), ['2. Berwald - Jagodziński',
                                         '3. Rode - Czerwiński[?]',
                                         '4. Naeghyall[?] - Storowski[?]',
                                         '5. Fuhrmann - Fuhrmannski[?]'],
     'Lines 3 to 5: the Polonised forms were read variously '
     '(Czerwiński/Czrzewinski/Ozrzewinski; Storowski/Horovinski; '
     'Fuhrmannski/Fukrmannski).'),
    ('p26b2', 26, (0, 790, 1849, 1510), ['6. Rotloff - Surowiecki[?]',
                                         '7. Krebs - Rakowski[?]',
                                         '8. Will - Dzikowski',
                                         '9. Pidda - Peda'],
     'Lines 6 and 7: Surowiecki/Surowrecki, Rakowski/Dakowski.'),
    ('p26b3', 26, (0, 1240, 1849, 1960), ['10. Pidda - Studziński[?]',
                                          '11. Sekinike[?] - Stodulski[?]'],
     'Line 11: the German name was read Sekinike/Soliinke/Tokienke.'),
    ('p26b4', 26, (0, 1690, 1849, 2410), ['14. Neuwert - Nowaczyński[?]',
                                          '15. Martin - Marcinkowski',
                                          '16. Nahr[?] - Koguciński'],
     'Line 14: the Polonised form was read Nowaczyński/Nowaerypki. '
     'Line 16: Mahn or Nahr?'),
    ('p26b5', 26, (0, 2140, 1849, 2695), ['18. Kybs - Kübsch',
                                          '19. Brodel - Brudel'],
     'Line 18: Kybs or Tybs? Kübsch or Hübsch?'),
    ('p27b0', 27, (0, 0, 1857, 630), ['A. Arminski,',
                                      'B. Bartmanski, Brojerski, '
                                      'Bartnowski, Bauerowicz[?],'],
     'The B line: is the last name "Bauerowicz" or "Bauerschwiez"? '
     'And "Brojerski" or "Brojeski"?'),
    ('p27b1', 27, (0, 340, 1857, 1070), ['D. Donarski,',
                                         'F. Funkiewicz, Festerkiewicz[?], '
                                         'Frydrychowski[?], Feterowski[?],',
                                         'G. Gutwiński,',
                                         'H. Holendajski, '
                                         'Hendzelewski[?], Hirszowski,'],
     'The F line and the H line. F: Festerkiewicz? Frydrychowski? '
     'Feterowski? H: Hendzelewski/Nedzelewski/Hendrelewski? '
     'Hirszowski or Hirszewski?'),
    ('p27b2', 27, (0, 790, 1857, 1520), ['J. Jursowski[?]',
                                         'K. Kuntski, Kurzmanowski[?], '
                                         'Knapski, Kirschkowski,',
                                         'L. Licznerowski, Lernaciński, '
                                         'Lencewicz, Langowski,',
                                         'M. Murnerowski, Mieklewski, '
                                         'Mundkowski, Mystelkowski,',
                                         'N. Najderski,'],
     'The J line (Jursowski or Jurzowski); K (Kurzmanowski?); '
     'L (Lencewicz? Langowski?); M (Murnerowski? Mystelkowski?).'),
    ('p27b3', 27, (0, 1250, 1857, 1970), ['O. Oberski,', 'P. Palmowski,',
                                          'R. Ringwelski, Rosenkiewicz, '
                                          'Retelewski, Reinowski,',
                                          'S. Schmiedcki[?], Sendowrz[?], '
                                          'Sulborski,'],
     'The S line: the three names were read variously '
     '(Schmidcki/Schmiedzeki/Schmielecki; Semidowrz/Sendowrz/Smidowrz; '
     'Sulborski). Also Rosenkiewicz (Ranzenkiewicz?).'),
    ('p27b4', 27, (0, 1700, 1857, 2430), ['W. Weynerowski, Wilmański,'],
     'The W line (Weynerowski or Heynerowski?). Are T, U, V, Z really '
     'empty on the page?'),
    ('p28b0', 28, (0, 0, 1856, 630),
     ['Polnische[?] deutsche Briefe von George Schlag,'],
     'The first line of the excerpt heading.'),
    ('p28b1', 28, (0, 340, 1856, 1070),
     ['Morgenprediger zu St. Hieronymi u. der polnischen',
      'Schule verordneter Moderator.',
      'Breslau, den 18. September 1741.',
      'Wojciech Wilkotek - Albrecht Bärwolf[?]'],
     'The rest of the heading and the first pair. "Breslau" or '
     '"Bruselau"? And the second name: Bärwolf? Bärwinkel?'),
    ('p28b2', 28, (0, 790, 1856, 1520),
     ['Jakub Maślanka - Jacob Buttermilch',
      'Tomasz Kapusta - Thomas Erzont[?]',
      'Tomas[?] Klotomecki[?] - Thomas Goldmann',
      'Jan Tarnowski[?] - John Tannon[?]'],
     'Four pairs. The Polonised names read variously: Kapusta; '
     'Klotomecki/Kłotomeksi; Tarnowski/Ternowski. The German: Erzont? '
     'Tannon?'),
    ('p28b3', 28, (0, 1240, 1856, 1970),
     ['Michał Kierznicki[?] - Michael Strauch',
      'Jerzy Samotyia[?] - George Selbstfell[?]',
      'Jakub Wierzbrecki[?] - Jacob Weidner[?]'],
     'Three pairs: Kierznicki? Samotyia? Selbstfell? Wierzbrecki? '
     'Weidner?'),
    ('p29top', 29, (0, 0, 1850, 640),
     ['Polonisazja[?] techniczna[?]',
      '[Rocle?] - Rola[?]', 'Sack[?] - Lak[?]',
      'Riebschel[?] - Rysel[?]', 'Pall[?] - Pal[?]'],
     'The heading of the sheet and the pairs under it, top right. '
     'The reads disagree on almost every name.'),
    ('p29c0a', 29, (0, 0, 800, 1520),
     ['1. Bartmanski', '2. Schmielecki',
      '3. Funkiewicz', '4. Sulborski',
      '5. Riewe[?] - Riwa[?]'],
     'The first column, numbers 1 to 5. Is number 5 a pair '
     '"Riewe - Riwa", and what are the two names?'),
    ('p29c0b', 29, (0, 1280, 800, 2696),
     ['6. Ringwelski', '7. Festerkiewicz',
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
    ('p29c1b', 29, (450, 1280, 1400, 2696),
     ['26. Hendzelewski[?]', '27. Folkierski',
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
    ('p29c3', 29, (1060, 0, 1850, 1420),
     ['Gross[?] - Grosz[?]', 'Rosin[?] - Rosyp[?]',
      'Hahnirt[?] - Hanus[?]', 'Brick[?] - Brych[?]',
      'Bordel[?] - Bordo[?]',
      'Avon[?] - Mianowski[?]'],
     'The pairs column. Each pair: what does the page say on either '
     'side of the dash? The reads disagree on nearly all.'),
    ('p29c3b', 29, (1060, 1280, 1850, 2696),
     ['Gaensler[?] - Gasiorowski[?]',
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
    ('p30c0', 30, (0, 0, 800, 1520),
     ['49. Oberski', '50. Langowski',
      '51. Sabss[?]', '52. Maldelin[?]',
      '53. Melerowicz[?]'],
     'The end of the numbered list. Doubtful: 51, 52, 53. '
     'The whole-page read had "51. Salto Karlowski", "52. Madalinski - '
     'Miele", "53. Melerovolz".'),
    ('p30c1', 30, (450, 0, 1400, 1520), [],
     'Four short lines below the list (read once as "Bwhre / Them. / '
     'Bomfurtun. / evangelesy."). What do they say?'),
    ('p30c2', 30, (1060, 0, 1846, 1520), [],
     'More short lines on the same page (read once as "sirdorfki", '
     '"motzungen"). What do they say?'),
]

ZOOM = 2.0          # every strip is shown at twice the sheet's size
SHEET_W = 1500      # the whole-sheet view is scaled to this width


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
    # the whole sheets, scaled down for quick loading
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
        ls = '<br>'.join(
            l.replace('[?]', '<span class=q>[?]</span>') for l in lines) or \
            '<i>(nothing read)</i>'
        rows.append(
            f"<div class=row data-key='{key}'>"
            f"<div><b>{i}.</b> <span class=k>{key}</span> "
            f"<a href='/spot_img/sheet_{tag}.jpg' target='_blank'>"
            f"whole sheet {tag}</a></div>"
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
<p>Each row is one region of a photographed sheet, cut with margins so no
line is lost; the draft reading is under the picture, doubtful words marked
<span class=q>[?]</span>. Read the region and either take the draft as it
stands or type what the page says &mdash; line by line, in the "Something
else" box, is welcome. "Whole sheet" above every picture opens the page in
full, smaller.</p>
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
</script></body></html>"""


def read_html():
    rows = []
    for i, (key, n, rect, lines, note) in enumerate(ROWS, 1):
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
