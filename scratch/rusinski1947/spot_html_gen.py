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
    ('S36', 'B', 'various', '22 superscript markers - the NUMBERS',
     'the print has superscript note-markers at 22 places the scan '
     'renders only as a * / % / $ glyph (the digit itself is below '
     'scan resolution). The places, in reading order:\n'
     'p. 5: "Zajączkowo Wielkie i Małe *"\n'
     'p. 18: "10. Szóstaki par. Sieraków %;"\n'
     'p. 29: "Ol. Troszczyńskie %"\n'
     'p. 36: "znaczna część szlachty ... była protestancka *"\n'
     'p. 40: "np. tymczasowa umowa wstępna *"\n'
     'p. 40: "32 w języku niemieckim %"\n'
     'p. 48: "prawo przegonu swej trzody przez grunt olęderski *"\n'
     'p. 51: "cała ława gminna wybierana była dożywotnio %"\n'
     'p. 51: "podawać do dworu imiona i nazwiska wszystkich '
     'osadników $"\n'
     'p. 51: "olędrom Starego i Nowego Ujścia %"\n'
     'p. 54: "od której klucz mieli ławnicy $"\n'
     'p. 54: "pan zastrzegał sobie tylko część dochodów *"\n'
     'p. 74: "w Ol. Ujskich prawo łowiectwa było nieograniczone *"\n'
     'p. 78: "sprzedaż trunków mogła być ... uciążliwym obowiązkiem *"\n'
     'p. 99: "sprawę tę wyczerpująco wyjaśnił już kilka lat przed '
     'tym %"\n'
     'p. 100: "chociaż bywało: i odwrotnie %"\n'
     'p. 101: "aż wszystko zostanie sprzątnięte %"\n'
     'p. 102: "zwiększania powinności olęderskich zdarzały się '
     'rzadko %"\n'
     'p. 112: "Ta sprawa omówiona została już poprzednio *"\n'
     'p. 112: "skłonność do przenoszenia się z jednej osady do '
     'innej *"\n'
     'p. 114: "ofiarowywał na szkołę bezpłatnie jeden z budynków %"\n'
     'p. 118: "i praktyk religijnych %"',
     'I will wire each to its note as soon as you give the numbers '
     '(a simple list: p. 5 = n, p. 18 = n, ...).',
     'the glyphs are unreadable at scan resolution; the marker '
     'numbers follow each page\'s own sequence, which the print '
     'shows directly.',
     None),
    ('S37', 'B', 'various', '6 missing amounts (dropped digits)',
     'the OCR lost these figures; the sentences now read with a '
     'gap:\n'
     'p. 86: "w Ujskich Ol. (r. 1597) wyrosił ___ zł z huby '
     '30-morgowej"\n'
     'p. 86: "...w Skrzydlewie (r. 1785) — ___ talarów w dukatach, '
     'licząc na dukata 3 talary (== 90 zł)" (in note 4)\n'
     'p. 89: "pan pobierał ___ tynfów (14 zł) od każdegoaktu" (my '
     'guess: 2)\n'
     'p. 89: "uiszczali ją olędrzy co ___ lat w wysokości ___ zł z '
     'huby"\n'
     'p. 107: "w dobrach państwowych ___ gr" (between 26—66 gr and '
     '7 talarów 42 gr)\n'
     'p. 30: "Dem Zimer man haben wier gegeben ___ Reichstaler, '
     'drey tohn bier"',
     'fill the gaps from your print copy.',
     'the digits were lost in the scan (likely small/crowded '
     'type); everything else in those sentences is verified.',
     None),
    ('S38', 'B', pg('0077'), 'TABELA III (p. 62): garbled table + its '
     'unlinked notes',
     'the occupational table (Skład zawodowy ludności 36 osad '
     'olęderskich powiatu poznańskiego) is heavily garbled, and its '
     'four table-notes are unlinked: note 1 glued into the Razem '
     'row ("Źródło miesza chałupników z komornikami..."), then '
     '"2 Karczmarze i młynarze.", "3 nauczyciel, 4 lektorów '
     '(Vorleser)." as stray lines.',
     'TABELA III needs its own repair pass (like ANEKS I got). '
     'Confirm from your print: the table\'s row/column structure '
     'and where the four note-markers sit (the scan shows one: '
     '"b. chałupnicy!" = note 1).',
     'the table spans most of p. 62; the notes print below it. The '
     'row data need a pixel-level re-read.',
     None),
    ('S39', 'B', pg('0016'), 'p. 1: notes 4 and 5 look swapped',
     'after the split the notes read: 4 = "Patrz wykaz skrótów.", '
     '5 = "Tamże." - but their markers sit at Maas⁴ and Schulz⁵ '
     '(visible digits in the print).',
     'if your print shows e.g. note 4 = "Tamże." and note 5 = '
     '"Patrz wykaz skrótów." (or different texts), tell me - the '
     'def ORDER should follow the print\'s note block.',
     'the print\'s note block at the page bottom: read notes 4 and '
     '5 verbatim.',
     'S39_p1_full.png'),
    ('S40', 'B', pg('0154'), 'row 115 (Sępolno): Charakter + Źródło '
     '(re-ask)',
     'Charakter `—c= z p"`, Źródło `Giszy z a zu"` (both garbage).',
     'need your print copy\'s row 115 line (p. 139, Sępolno).',
     'the row sits under glue from r116; the figures (11) are '
     'verified.',
     'S32_0154_r109_r115.png'),
    ('S41', 'B', pg('0158'), 'rows 2 and 5 of the c-series (re-ask)',
     'r2 Źródło `MY. AM. o. av..." TE > ">>`; r5 Charakter '
     '`ZZ e ft I` (garbage).',
     'you offered the rows - here they are needed: r2 (Głębockie '
     'Olędry) Źródło and r5 (Krzyżowniki) Charakter.',
     'the crops show both rows in context.',
     'S34_0158_r1_r5.png'),
    ('S42', 'B', pg('0140'), 'the three remaining raised digits: '
     'note refs?',
     '0140 r17 dymy `11 3`; p. 131 r102 dymy `29 3`; p. 136 r67 '
     'dymy `28 1`.',
     'if your print shows a superscript there (note 3 = "Razem z '
     'Ol. Sosnowiec."?), give me the rows and I will convert them '
     'to refs like 51[^1] and 165[^2].',
     'r17\'s Dymy cell in the crop; the other two cells show the '
     'same pattern (a big value + a small raised digit).',
     'S42_0140_r17.png'),
]
def pg(sheet):
    return 'p. %d' % (int(sheet) - 15)


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
