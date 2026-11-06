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
# S01-S23 resolved in earlier rounds. The items below are the residue
# of the full noise-removal pass (figures + text). Item shape:
# (id, section, page, title, transcription-reads, I-propose, look-at,
#  why-technical, crop)
def pg(sheet):
    return 'p. %d' % (int(sheet) - 15)


ITEMS = [
    ('S23', 'B', pg('0146'), 'a-series RAZEM row',
     'The RAZEM row prints 2.386 dymów | 92 | 12.967. My column '
     'transcription sums to 2387 | 92 | 12.958.',
     'Keep the printed RAZEM row unchanged. The dymy column closes '
     'to within 1 (the print counts the small raised digits); the '
     'ludn column is 9 short of 12.967 and I cannot find the '
     'missing 9 anywhere in the scan.',
     'the RAZEM row at the very bottom of the table; compare its '
     'three numbers with the columns above it.',
     'Every ludn cell was pixel-verified (a_audit.py); the dymy '
     'Delta(-1) follows from the mark-sum law (mark_test.py).',
     'S23_a_totals_0146.png'),
    ('S24', 'B', pg('0157'), 'b-series RAZEM row',
     'The RAZEM row prints 2.071 | 38 | 4.484. My columns sum to '
     '2059 | 38 | ~538.',
     'Keep the printed RAZEM row unchanged. The printed ludn total '
     '4.484 cannot come from this column (almost every ludn cell '
     'is a dash) - it must aggregate something else, or be a print '
     'error. Leave the column as transcribed.',
     'the RAZEM row at the bottom; then scan the Ludn column '
     '(last) upward - you will see it is almost all dashes.',
     'The ludn dash-ness was verified en masse (dash_scan.py: '
     'w~66 h<=7 n~300 ink signature); the dymy Delta(12) may share '
     'the same cause.',
     'S24_b_totals_0157.png'),
    ('S25', 'B', pg('0140'), 'small raised digits after dymy values',
     'Rows 14 and 17 carry a big dymy number followed by a small '
     'raised digit: `165 3` and `11 3` (also `29 3` on p. 131, '
     '`28 1` on p. 136).',
     'Keep them exactly as transcribed (`165 3` etc.). The print\'s '
     'own RAZEM counts these small digits, so they are real '
     'content - but WHAT they mean (a second count? mlyny? an '
     'estimate?) only your copy/knowledge can say.',
     'rows 14 and 17, Dymy column (9th): look closely after the '
     'main number for a small raised digit.',
     'The glyphs matcher-read as digits @>=0.8; sum experiment '
     '(mark_test.py) proves the print\'s total counts them '
     '(2387 vs printed 2386).',
     'S25_marks_0140.png'),
    ('S26', 'B', pg('0139'), 'row 8 (Błonie al. Żdżar): the third glyph',
     'The transcription reads `51` in the Dymy column.',
     'Keep `51`. The scan shows a third small glyph (would read '
     '`511`), but counting it makes the print\'s own total wrong '
     'by +1. I read the third glyph as a stray mark, not a digit.',
     'row 8, Dymy column (9th) - is the value 51 with a smudge, '
     'or 51 with a small 1?',
     'With the third glyph counted as a mark the a-dymy sum '
     'overshoots the printed total by 1; without it, it closes '
     'exactly. The other marked rows (S25) ARE counted - this one '
     'behaves differently.',
     'S26_mark_0139_r8.png'),
    ('S27', 'B', pg('0140'), 'the three "Razem z..." notes',
     'Three notes under the table ("Razem z Borujskimi Starymi...", '
     'etc.) are transcribed as footnotes [^125-1], [^125-2], '
     '[^125-3] with no row references.',
     'Keep the notes as they are. If your print copy shows little '
     'superscript marks on specific rows telling the reader which '
     'note applies where, tell me the rows and I will wire the '
     'references.',
     'the three note lines below the table; the candidate rows are '
     '14-15 (Borujskie) and 28-29 (Dymaczewskie) further up.',
     'The superscripts are smaller than the scan\'s resolution; '
     'repeated high-zoom passes found nothing decisive.',
     'S27_notes_0140.png'),
    ('S28', 'B', pg('0147'), 'row 5 (Bolewickie Olędry): Charakter',
     'The Charakter column reads `szatyn"` - garbage.',
     'No reliable reading. Either empty the cell (`—`), or give me '
     'the word from your print copy (my guess: something like '
     '"na sztynach"? a terrain word?).',
     'row 5, Charakter column (6th).',
     'The strip raw holds nothing usable after the name group.',
     'S28_0147_r5.png'),
    ('S29', 'B', pg('0148'), 'rows 18 and 24: Rok',
     'Row 18 (Daleszynek) Rok reads `r`; row 24 (Filipowo) reads '
     '`o` - both garbage.',
     'Replace both with `—` (no year visible in the scan). If your '
     'print shows a year in either cell, give it to me.',
     'rows 18 and 24, Rok column (5th).',
     'Strip raws show no year for either row (r18\'s strip is the '
     'garble "TE"; r24\'s is the razem-z-Wyszynkami glue).',
     'S29_0148_r18_r24.png'),
    ('S30', 'B', pg('0151'), 'row 68 (Lubowo Zarzeczne): Źródło head',
     'The Źródło column reads `rowo, vol. III` - the citation '
     'starts mid-word.',
     'Reconstruct the head as `AGH. s. ..., maj. Lubo|wo, vol. '
     'III` - but the court/majętność name before "rowo" is lost in '
     'the scan. Needs your print copy to complete.',
     'row 68, Źródło column (7th) - the text visibly starts '
     'mid-word.',
     'The strip shows only the tail; the head sits under the '
     'multi-line glue of the neighbour row.',
     'S30_0151_r68.png'),
    ('S31', 'B', pg('0154'), 'row 105 (Psarskie Małe): Źródło head',
     'The Źródło column reads `ZMITLIZe"- 5a. Z LIU" wy, maj. '
     'Psarskie, Tax Acten, v. II, fol. 88—94`.',
     'Keep the certain tail (`... maj. Psarskie, Tax Acten, v. II, '
     'fol. 88—94`); the garbled head is almost certainly `AGH. s. '
     '<court>, maj. Psarskie...` (cf. row 104\'s clean "AGH. s. '
     'Szamotuły, maj. Myszkowo, Tax Acten"). The court name needs '
     'your print.',
     'row 105, Źródło column; compare with row 104\'s clean '
     'citation two rows up.',
     'Same formula family as 0153 r104 (strip-verified there); '
     'only the court name is unrecoverable here.',
     'S31_0154_r105.png'),
    ('S32', 'B', pg('0154'), 'rows 109-111 (Rańsko/Rożnowo) + row 115',
     'Row 110 nazwa/parafia read `Rosnowskie Olędry | Komorniki`; '
     'row 111 Źródło reads `4VY. Db. FU` (garbage); row 115 '
     'Charakter and Źródło are garbage (`—c= z p"` / `Giszy z a '
     'zu"`).',
     'Row 110 nazwa: change to `Rożnowskie Olędry` (to match row '
     '111\'s Rożnowo) - confirm from your print. Row 111 Źródło and '
     'row 115\'s two cells: need your print copy. The figures '
     '(15/21/13*/11) are verified and unaffected.',
     'rows 109-111 and 115: does the settlement name Rożnowo '
     'appear in both rows 110 and 111? And is row 115\'s Sępolno '
     'row carrying a real źródło?',
     'The rows sit under multi-line glue; figures were settled by '
     'Lp-anchor pixel reads, but the text distribution was not.',
     'S32_0154_r109_r115.png'),
    ('S33', 'B', pg('0157'), 'row 146 (Wyssogotowo al. Czarne Olędry): Rok + Źródło',
     'Rok reads `pozy lil mr £`; Źródło reads `b sz b s I` - both '
     'garbage.',
     'Rok: replace with `—`. Źródło: need your print copy (my '
     'guess: a Rel. Posn. nr ... form like its neighbours). The '
     'dymy value 17 is verified and unaffected.',
     'row 146, Rok (5th) and Źródło (7th) columns.',
     'The row sits under the r146/r147 glue knot; only the figures '
     'and dashes could be anchored.',
     'S33_0157_r146.png'),
    ('S34', 'B', pg('0158'), 'rows 1, 2, 5: Charakter + Źródło garbles',
     'Row 1: Charakter `LL] g`, Źródło garbled. Row 2: Źródło '
     'garbled. Row 5: Charakter `ZZ e ft I`.',
     'No reliable readings - these cells are very tight small '
     'print. Either empty them (`—`) or supply the text from your '
     'copy. The years (1747/1743/1786) and dymy values are '
     'verified and unaffected.',
     'rows 1, 2 and 5, Charakter (6th) and Źródło (7th) columns.',
     'The c-series opening rows render as letter-soup at scan '
     'resolution; strips confirm only years and figures.',
     'S34_0158_r1_r5.png'),
    ('S35', 'B', pg('0159'), 'row 10 (Trzy Domy): Rok',
     'The Rok column reads `I /DO` (garbage). The data column '
     'cleanly reads `15 IV 1755`.',
     'Replace Rok with `—` - unless your print repeats the date\'s '
     'year (1755) in the Rok column, which several other rows do.',
     'row 10: compare the Rok column (5th) with the data column '
     '(4th from the right).',
     'The strip shows the data-year at the far right; whether the '
     'Rok cell carries it too is beyond the scan.',
     'S35_0159_r10.png'),
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
    iid, sec, page, title, now, propose, look, why, crop = it
    uri = datauri(crop)
    img = ('<img class="crop" loading="lazy" src="' + uri +
           '" alt="' + E(title) + '">') if uri else \
          '<p class="miss">[crop missing: ' + E(crop) + ']</p>'
    return (
        '<div class="item" id="' + iid + '">'
        '<div class="itemhead"><span class="tag">' + iid + '</span>'
        '<span class="page">' + E(page) + '</span> — <strong>' + E(title) +
        '</strong></div>'
        '<p><b>The transcription reads:</b> ' + E(now) + '</p>'
        '<p style="background:#eef7ee;border-left:4px solid #494;'
        'padding:6px 10px"><b>I propose:</b> ' + E(propose) + '</p>'
        '<p style="color:#444"><b>Look at:</b> ' + E(look) + '</p>'
        + img +
        '<details style="font-size:85%;color:#666;margin:6px 0">'
        '<summary>why I doubt it (technical)</summary><p>' + E(why) +
        '</p></details>' +
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
