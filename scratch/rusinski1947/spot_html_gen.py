# -*- coding: utf-8 -*-
"""Generate SPOT_SHEET.html: the editor's review sheet as ONE
self-contained file - every crop embedded as a data URI, the decision
tables inline, and a per-item answer form with a 'collect answers'
button that produces a compact summary to paste back into the chat.
Answers persist in localStorage across refreshes.

Assembled by token replacement (@@NAME@@), not f-strings - the embedded
JavaScript's braces collide with f-string syntax."""
import base64, csv, json, os, html

HERE = r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947\literature\rusinski1947'
CROPS = os.path.join(HERE, 'spot_crops')
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'


def datauri(name):
    p = os.path.join(CROPS, name)
    if not os.path.isfile(p):
        return None
    with open(p, 'rb') as fh:
        return 'data:image/png;base64,' + base64.b64encode(fh.read()).decode()


# ---------------- the decision items -------------------------------------
ITEMS = [
    ('S04', 'B', 'p. 26', '514 dymów × 6,05 (crop redone — the numbers are now legible)',
     '"Ostatnia rubryka aneksu I b wykazuje 514 dymów … współczynnik 6.05, otrzymamy 3.122 osoby"',
     '514 × 6,05 = 3.110, not 3.122. Either "516 dymów" or "3.110 osób". The draft still reads 514/3.122 — say which digit the print shows.',
     'Either "516 dymów" or "3.110 osób" (the crop now shows both numbers)', 'S04_p26_514_dymow.png'),
    ('S07', 'B', 'p. 43, note 5', 'r. 1043 (crop redone)',
     'Note 5 of p. 43: "W r. 1043 olędrom Marianowa przedłużono dzierżawę na lat 30 (Q, I, nr 25)."',
     'Impossible year (the note block is the 1597-1677 era). I applied "r. 1643" on internal evidence; the crop now shows the year — confirm or correct.',
     '"r. 1643" (applied; confirm from the crop)', 'S07_p43fn_r1643.png'),
    ('S09', 'B', 'p. 16, note 1', 'Wymysłowo 1889/1890 (crop redone)',
     'The sigla note: "Tp. 89, 90 — Wymysłowo, 1889 — 1 dym, 1890 — 1 dym"',
     'Impossible years; the passage is about Tp. 89/90 = 1789/1790. The crop now shows the line.',
     '"1789 — 1 dym, 1790 — 1 dym"', 'S09_p16_wysylowo.png'),
    ('S14', 'B', 'p. 68', 'The inline table (crop redone)',
     'Was: "wyniesie 16,80 ha ,, „ U ) „„ ) 19, 10 H 1) ”» ” ,) 81/, x ) ,) ,, , 7 » » „ 24 20". Now rebuilt as: "prętem 7½-łokciowym wyniesie 16,80 ha; 8 łokci — 19,10 ha; 8½ łokci — 21,60 ha; 9 łokci — 24,20 ha."',
     'The crop shows the print\'s table. Math: 7½→16,80; 8→19,10; 8½→21,58; 9→24,20. The print reads 21,60 (per the 3x read) — confirm the four pairs and whether the third is 21,58 or 21,60.',
     'confirm the four pairs (the draft has 16,80 / 19,10 / 21,60 / 24,20)', 'S14_p68_wloka_table.png'),
]

# ---------------- the tables ----------------------------------------------
def read_csv(name):
    p = os.path.join(HERE, name)
    if not os.path.isfile(p):
        return []
    with open(p, encoding='utf-8-sig') as fh:
        return list(csv.DictReader(fh))


orphans = read_csv('spot_orphan_defs.csv')
numctx = read_csv('spot_numctx.csv')
annex = read_csv('spot_annex.csv')

s4 = json.load(open(os.path.join(OCR, 'structure4.json'), encoding='utf-8'))
mk = json.load(open(os.path.join(OCR, 'markers.json'), encoding='utf-8'))
shorts = [(str(int(n) - 15), len(mk[n]), len(s4[n]['notes']))
          for n in sorted(mk) if len(mk[n]) < len(s4[n]['notes'])]

# ---------------- render ---------------------------------------------------
E = html.escape


def item_html(it):
    iid, sec, page, title, draft, why, guess, crop = it
    uri = datauri(crop)
    img = ('<img class="crop" loading="lazy" src="' + uri +
           '" alt="' + E(title) + '">') if uri else \
          '<p class="miss">[crop missing: ' + E(crop) + ']</p>'
    return (
        '<div class="item" id="' + iid + '">'
        '<div class="itemhead"><span class="tag">' + iid + '</span>'
        '<span class="page">' + E(page) + '</span> — <strong>' + E(title) +
        '</strong></div>'
        '<p><b>Draft:</b> ' + E(draft) + '</p>'
        '<p><b>Why doubtful:</b> ' + E(why) + '</p>'
        '<p><b>My reading:</b> ' + E(guess) + '</p>'
        + img +
        '<div class="answer">'
        '<label><input type="radio" name="' + iid +
        '" value="ok"> agree with my reading</label>'
        '<label><input type="radio" name="' + iid +
        '" value="keep"> keep as in draft</label>'
        '<label><input type="radio" name="' + iid +
        '" value="other"> other:</label>'
        '<input type="text" class="othertext" id="' + iid + '_txt" '
        'placeholder="the correct reading…">'
        '</div></div>')


def table(rows, headers):
    out = ['<table><thead><tr>']
    out += ['<th>' + E(h) + '</th>' for h in headers]
    out.append('</tr></thead><tbody>')
    for r in rows:
        out.append('<tr>' + ''.join('<td>' + E(str(v)) + '</td>'
                                    for v in r) + '</tr>')
    out.append('</tbody></table>')
    return '\n'.join(out)


secA = '\n'.join(item_html(it) for it in ITEMS if it[1] == 'A')
secB = '\n'.join(item_html(it) for it in ITEMS if it[1] == 'B')
secE = '\n'.join(item_html(it) for it in ITEMS if it[1] == 'E')
secF = '\n'.join(item_html(it) for it in ITEMS if it[1] == 'F')
nav = ' '.join('<a href="#' + it[0] + '">' + it[0] + '</a>'
               for it in ITEMS)
orphan_rows = [(o['page_note'], o['text'][:120]) for o in orphans]
numctx_rows = [(o['page'], o['label'], o['digit_token']) for o in numctx]
annex_rows = [(o['sheet'], o['issue'], o['detail']) for o in annex]
short_rows = shorts

TEMPLATE = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'spot_html_template.html'),
                encoding='utf-8').read()
page = (TEMPLATE
        .replace('@@NAV@@', nav)
        .replace('@@SECA@@', secA)
        .replace('@@SECB@@', secB)
        .replace('@@SECE@@', secE)
        .replace('@@SECF@@', secF)
        .replace('@@NUMCTX_COUNT@@', str(len(numctx_rows)))
        .replace('@@NUMCTX@@', table(numctx_rows,
                                     ['page', 'label', 'digit token']))
        .replace('@@ORPHAN_COUNT@@', str(len(orphan_rows)))
        .replace('@@ORPHANS@@', table(orphan_rows,
                                       ['page-note', 'text']))
        .replace('@@SHORTS@@', table(short_rows,
                                     ['page', 'markers found',
                                      'notes in print']))
        .replace('@@ANNEX@@', table(annex_rows,
                                    ['sheet', 'issue', 'detail']))
        .replace('@@S20@@', datauri('S20_annex_0142_dupes.png'))
        .replace('@@S21@@', datauri('S21_annex_0144_dupes.png'))
        .replace('@@S22@@', datauri('S22_annex_0146_totals.png'))
        .replace('@@IDS@@', json.dumps([it[0] for it in ITEMS]))
        .replace('@@META@@', json.dumps([[it[0], it[2]] for it in ITEMS])))

with open(os.path.join(HERE, 'SPOT_SHEET.html'), 'w', encoding='utf-8') as fh:
    fh.write(page)
print('SPOT_SHEET.html written:',
      os.path.getsize(os.path.join(HERE, 'SPOT_SHEET.html')) // 1024, 'kB;',
      'items:', len(ITEMS), '; orphans:', len(orphan_rows),
      '; numctx:', len(numctx_rows), '; annex:', len(annex_rows))
