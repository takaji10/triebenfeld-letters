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
# Round 1 (S23-S35) answered by the editor and applied. The items
# below = round 2: the footnote-marker audit's residue.
def pg(sheet):
    return 'p. %d' % (int(sheet) - 15)


ITEMS = [
    # ---- round 5 (the footnote-page pass): the open ruling items
    ('S52', 'B', 'p. 23',
     'note 4 total: 24.667 vs the body\'s 15.831 (Δ9)',
     '[^23-4]: "Tj. wykazane w Tod. 89 summa summarum 24.667 dymów, '
     'mniej 8.520 dymów miejskich … mniej 225 dymów … wreszcie mniej 82 '
     'dymy osad wymienionych w przypisie poprzednim.'
     '   → 24.667 − 8.520 − 225 − 82 = 15.840, but the body prints '
     '"15.831 dymów" (Δ9)',
     'keep both figures as the print has them (every figure '
     'pixel-verified: the note total reads 24.667 in both OCR passes '
     'and in the glyph render; the body reads 15.831) — this looks '
     'like the AUTHOR\'s own slip, not an OCR one',
     'Top strip: the body line "Tod. 89 dla tychże osad podaje '
     '15.831 dymów" (scan 0038 y3375-3450). Bottom strip: the note-4 '
     'block (24.667 / mniej 8.520 / mniej 225 / mniej 82). If you '
     'prefer a [sic] after 15.831, or a correcting note, say so — '
     'otherwise the discrepancy stands as the print\'s own.',
     'S52_p23_delta9.png'),
    ('S53', 'A', 'pp. 38–39',
     'note 38-3: the manifest quote CONTINUES on print p. 39',
     '[^38-3] on p. 38 ends "…Grunta za sumę tylko 2.300 talerów '
     'sprzedali, inwentarz zabrali … s. Johann Bóhme”. Na skutek '
     'pozwu olędra sprawa oparła się o sąd ziemski poznański…" — '
     'ALL inside the note def on p. 38',
     'keep the note WHOLE on p. 38 (content complete; the placement '
     'is the print\'s own quirk)',
     'The print fills p. 38\'s note block to the page bottom (top '
     'strip) and then continues the SAME note mid-page on p. 39 in '
     'note-size type (bottom strip: "sprzedali, inwentarz zabrali…" '
     'through "s. Johann Bóhme\"", followed by the note-size "Na '
     'skutek pozwu…" narrative — both at y3024-4104, well above '
     'p. 39\'s own notes). Our def holds the whole text in order. '
     'Options: (a) as transcribed, (b) add a printed-page note like '
     '[continuation on s. 39], (c) split the def with a marker. '
     'A def-tail physical sweep found no other such case in the book.',
     'S53_note38_overflow.png'),
    ('S54', 'A', 'pp. 116–117',
     'note 116-5: the tail CONTINUES on print p. 117',
     '[^116-5] on p. 116 runs "…wielką liczbę niepiśmiennych olędrów '
     'wykazują również najwcześniejsze metryki protestanckie Lwówka '
     '(Archiwum Państwowe w Poznaniu, Metryki 441 C). Nawet w aktach '
     'regulacyjnych … nie umieli się podpisać."',
     'keep the note WHOLE on p. 116 (content complete; the placement '
     'is the print\'s own quirk)',
     'Same class as S53: the note fills p. 116\'s note block to the '
     'bottom (top strip) and its tail prints mid-page on p. 117 in '
     'note-size type (bottom strip: y2835-3105, BEFORE p. 117\'s own '
     'notes). Our def holds the whole text. Options as in S53. No '
     'other case exists (sweep-verified).',
     'S54_note116_overflow.png'),
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
    iid, sec, page, title, raw, propose, logic, crop = it
    uri = datauri(crop) if crop else None
    img = ('<img class="crop" loading="lazy" src="' + uri +
           '" alt="' + E(title) + '">') if uri else ''
    return (
        '<div class="item" id="' + iid + '">'
        '<div class="itemhead"><span class="tag">' + iid + '</span>'
        '<span class="page">' + E(page) + '</span> — <strong>' + E(title) +
        '</strong></div>'
        '<table style="border-collapse:collapse;margin:6px 0">'
        '<tr><td style="padding:2px 12px 2px 0;color:#555;'
        'white-space:nowrap">The transcription reads:</td>'
        '<td><code style="background:#f4f4f4;padding:1px 6px;'
        'white-space:pre-line">' + E(raw) + '</code></td></tr>'
        '<tr><td style="padding:2px 12px 2px 0;color:#555;'
        'white-space:nowrap;font-weight:bold">I propose:</td>'
        '<td style="background:#eef7ee;border-left:4px solid #494">'
        '<code style="background:#eef7ee;padding:1px 6px;'
        'white-space:pre-line">' + E(propose) + '</code></td></tr>'
        '</table>'
        + img +
        '<details style="font-size:85%;color:#666;margin:6px 0">'
        '<summary>Logic</summary><p>' + E(logic) + '</p></details>' +
        '<div class="answer">'
        '<label><input type="radio" name="' + iid +
        '" value="ok"> agree with my proposal</label>'
        '<label><input type="radio" name="' + iid +
        '" value="keep"> keep as transcribed (no change)</label>'
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
