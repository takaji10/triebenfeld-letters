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
# of the full noise-removal pass (figures + text): 5 sum/mark items
# and 8 cluster items covering the 15 deep-garble text cells.
def pg(sheet):
    return 'p. %d' % (int(sheet) - 15)


ITEMS = [
    ('S23', 'B', pg('0146'), 'a-series RAZEM vs the column sums',
     'RAZEM prints 2.386 dymów / 92 / 12.967; the pixel column reads '
     '2387 (incl. raised marks) / 92 exact / 12958.',
     'The dymy Delta(-1) is the mark-sum law (marks counted). The '
     'ludn column is 9 short of the printed 12.967 after every cell '
     'was pixel-verified; either one settlement hides a 2-digit '
     'value the scan will not yield, or the print\'s own total is '
     'loose.',
     'keep the printed 12.967 as the truth; the transcription stays '
     'as pixel-read.',
     'S23_a_totals_0146.png'),
    ('S24', 'B', pg('0157'), 'b-series RAZEM vs the column sums',
     'RAZEM prints 2.071 / 38 / 4.484; the pixel column reads '
     '2059 (incl. marks) / 38 exact / ~538.',
     'The ludn RAZEM (4.484) exceeds what the b-column can hold '
     '(most b-cells read dash, verified en masse). The print\'s '
     'total must aggregate something beyond the column - possibly '
     'the ludn of settlements counted elsewhere.',
     'keep the printed 4.484; flag the column as incomplete by '
     'print design.',
     'S24_b_totals_0157.png'),
    ('S25', 'B', pg('0140'), 'the raised small digits after dymy values',
     'transcribed as plain digits: `165 3`, `11 3`, `29 3` (and '
     '`28 1` on 0151 r67).',
     'The small raised glyphs read as true digits (@>=0.8) and the '
     'sum experiment proves the print\'s RAZEM COUNTS them (2387 vs '
     '2386). What they MEAN is unknown (mlyny? karczmy? a second '
     'estimate?) - the transcription shows them inline, separated '
     'by a space.',
     'inline digits are correct; the semantic label is the '
     'editor\'s call.',
     'S25_marks_0140.png'),
    ('S26', 'B', pg('0139'), '0139 r8 (Błonie al. Żdżar): the third glyph',
     'dymy `51` (ludn 229).',
     'The pixel blob reads `511`, but the print\'s total arithmetic '
     'fits `51` (a `51 1` mark would push the sum to 2388, one PAST '
     'the printed 2386). The third glyph is either a stray mark or '
     'the raised-digit law differs here.',
     'keep `51`; the third glyph documented as a mark.',
     'S26_mark_0139_r8.png'),
    ('S27', 'B', pg('0140'), 'the three "Razem z..." notes under 0140',
     'added as notes [^125-1..3]; the superscript REF markers in the '
     'print could not be resolved from the scan.',
     'The notes print verbatim; which rows carry the superscript '
     'refs (Borujskie Nowe? Dymaczewskie?) is unresolvable at scan '
     'resolution.',
     'notes as added; refs = editor\'s ruling.',
     'S27_notes_0140.png'),
    ('S28', 'B', pg('0147'), '0147 r5 (Bolewickie Olędry): charakter',
     'charakter `szatyn"` (garble).',
     'The strip raw holds nothing after the name group; `szatyn"` '
     'is likely OCR of a hyphenated print word (szlachecka?) glued '
     'from the neighbour row.',
     'unknown - needs the editor\'s print copy.',
     'S28_0147_r5.png'),
    ('S29', 'B', pg('0148'), '0148 r18 (Daleszynek) and r24 (Filipowo): rok',
     'r18 rok `r` (junk), r24 rok `o` (junk).',
     'The strip raws show no year for either row (r18: "TE" garble; '
     'r24: the razem-z-Wyszynkami glue). The print may carry a year '
     'in tight italic the scan cannot split.',
     'likely `—` in both; editor\'s copy decides.',
     'S29_0148_r18_r24.png'),
    ('S30', 'B', pg('0151'), '0151 r68 (Lubowo Zarzeczne): źródło prefix',
     'źródło `rowo, vol. III` (head lost).',
     'The strip shows only the tail; the head is presumably '
     '"AGH. s. ..., maj. Lubo-" wrapping into `rowo`. The majętność '
     'name is cut at the scan.',
     'reconstruct as "AGH. s. <maj.>, maj. Lubowo, vol. III"? - '
     'editor\'s copy decides.',
     'S30_0151_r68.png'),
    ('S31', 'B', pg('0154'), '0154 r105 (Psarskie Małe): źródło prefix',
     'źródło `ZMITLIZe"- 5a. Z LIU" wy, maj. Psarskie, Tax Acten, '
     'v. II, fol. 88—94` (head garbled).',
     'The tail is clean and formula-typical (cf. 0153 r104 '
     '"AGH. s. Szamotuły, maj. Myszkowo, Tax Acten"); the head '
     '(the sąd/majętność group) is beyond the scan.',
     'likely "AGH. s. <sąd>, maj. Psarskie, Tax Acten, v. II, '
     'fol. 88—94" - editor\'s copy decides the sąd.',
     'S31_0154_r105.png'),
    ('S32', 'B', pg('0154'),
     '0154 r109-r111 (the Rańsko/Rożnowo knot) + r115 (Sępolno)',
     'r110 nazwa `Rosnowskie Olędry` + parafia `Komorniki` (both '
     'suspect); r111 zródło `4VY. Db. FU` (garble); r115 charakter '
     '`—c= z p"` and źródło `Giszy z a zu"` (garble).',
     'The figures are pixel-confirmed (35/15/21/13*), but the '
     'nazwa/parafia distribution across r109-r111 and the r111/r115 '
     'source cells sit under multi-line glue the scan cannot split.',
     'r110 nazwa likely `Rożnowskie Olędry` matching r111; the '
     'rest = editor\'s copy.',
     'S32_0154_r109_r115.png'),
    ('S33', 'B', pg('0157'), '0157 r146 (Wyssogotowo al. Czarne Olędry): rok + źródło',
     'rok `pozy lil mr £`, źródło `b sz b s I` (both junk).',
     'The row sits under the r146/r147 glue knot; the strip shows '
     'only r147\'s data/figures. dymy 17 and the dashes are '
     'pixel-verified.',
     'likely rok `—`; the źródło (Rel. Posn. nr ...?) = editor\'s '
     'copy.',
     'S33_0157_r146.png'),
    ('S34', 'B', pg('0158'), '0158 r1/r2/r5: charakter and źródło garbles',
     'r1 charakter `LL] g`, źródło `A«xYY. D. id s...`; r2 źródło '
     '`MY. AM. o. av...`; r5 charakter `ZZ e ft I`.',
     'The c-series sheet\'s first rows carry tight, small italic '
     'the scan renders as letter-soup; the strip confirms only the '
     'years (1747/1743/1786) and the dymy values.',
     'r1/r2 źródło likely AW./Kl. forms; r5 charakter unknown - '
     'editor\'s copy.',
     'S34_0158_r1_r5.png'),
    ('S35', 'B', pg('0159'), '0159 r10 (Trzy Domy): rok',
     'rok `I /DO` (junk); zrodlo `AW. CG. I, fol. 13` and data '
     '`15 IV 1755` are clean.',
     'The strip shows the data-year 1755 at the far right; whether '
     'the rok column carries 1755 or a dash is unresolvable.',
     'likely `—` (the data column holds 1755); editor\'s copy.',
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
