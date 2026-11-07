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
    ('S43', 'B', 'p. 129', 'the asterisk note above the table',
     '* Dymy niekt\u00f3rych osad podane s\u0105 w Tp. 89 zbiorowo '
     'dla ca\u0142ej osady; wysoko\u015b\u0107 ich na '
     'poszczeg\u00f3lne zagrody przeliczona zosta\u0142a '
     'wed\u0142ug Tp. 90.',
     'confirm or correct the wording (the scan is marginal)',
     'the band = the print page\'s top strip (rotated in the scan); '
     'the note sits under the column header.',
     'S43_p129_band.png'),
    ('S44', 'B', 'p. 131', 'the two notes on p. 131 - do they match '
     'the transcription?',
     'transcribed: 131-1 = "Sroczewskie Ol\u0119dry powsta\u0142y z '
     'dawnej wsi Sroczewa..." (long); 131-2 = "Razem z Ol. '
     'G\u00f3ry."',
     'confirm the band\'s two note lines are these two notes (and '
     'their order)',
     'the band shows the notes small; the transcription came from '
     'the strip OCR.',
     'S44_p131_band.png'),
    ('S45', 'B', 'p. 124', 'TABELA VI + the a-table\'s title',
     'TABELA VI / Osady ol\u0119derskie w by\u0142ym powiecie '
     'ko\u015bcia\u0144skim w okresie rozbior\u00f3w',
     'confirm the exact wording of the title line',
     'the band\'s second and third lines.',
     'S45_p124_band.png'),
    ('S46', 'B', 'p. 132', 'TABELA VII + the b-table\'s title',
     'TABELA VII / Osady ol\u0119derskie w by\u0142ym powiecie '
     'pozna\u0144skim w okresie rozbior\u00f3w',
     'confirm the exact wording (does it mention ziemia wschowska '
     'too?)',
     'the band\'s second and third lines.',
     'S46_p132_band.png'),
    ('S47', 'B', 'p. 143', 'the c-table\'s title',
     'Osady ol\u0119derskie w ziemi wschowskiej w okresie '
     'rozbior\u00f3w (no TABELA number seen)',
     'confirm the exact wording and whether a TABELA number '
     'precedes it',
     'the band\'s second line.',
     'S47_p143_band.png'),
    ('S48', 'B', 'p. 130', 'the p. 130 band: is there a continuation '
     'marker?',
     '(nothing transcribed)',
     'does the print carry a "(ci\u0105g dalszy)" or similar '
     'marker on p. 130 (and the other continuation pages)?',
     'the band between the running head and the column header.',
     'S48_p130_band.png'),
    ('S49', 'B', 'p. 62', 'TABELA III - the repair pass',
     'the table is garbled; the notes are unlinked',
     'your marker info is logged (b. cha\u0142upnicy[^1]; the '
     'Rolnictwo line: 60[^2] and 13[^2]; the O\u015bw. line: '
     '5[^3]). I will do a dedicated pixel-level repair pass of the '
     'table and then wire the four notes - no answer needed now, '
     'unless you want to prioritize it.',
     'the table spans most of p. 62.',
     None),
    ('S50', 'B', '?', 'the Ujskie czynsz amount - which print page?',
     'our p. 86 reads: "W najwcze\u015bniejszych osadach by\u0142 '
     'on bardzo niski: w Ujskich Ol. (r. 1597) wyrosi\u0142 ___ '
     'z\u0142 z huby 30-morgowej, w Ol. Nowe Dwory (r. 1601) 25 '
     'z\u0142 z huby..."',
     'you marked this "not on page 86" - which print page holds '
     'this sentence? (our page labels may drift from the print\'s '
     'folios in the body; the sentence\'s true page would '
     'recalibrate them)',
     'the sentence opens the czynsz-gruntowy discussion.',
     None),
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
