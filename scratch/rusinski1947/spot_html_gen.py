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
    ('S01', 'A', 'p. 50', 'RESOLVED — the quotation after "W nielicznych wypadkach" is a spanning footnote',
     'Before: p. 50\'s body carried the old-Polish quotation "z pierwszego małżeństwa dzieci równo należeć maią…" after "…W nielicznych wypadkach". Now: p. 49\'s note 4 („Bardzo szczegółowe…: „Ponieważ znaczna się krzywda dzieje…") runs to the page bottom mid-sentence ("…a miała wprzód") and completes at the top of p. 50\'s note block; the continuation was moved into [^49-4] and p. 50\'s body ends "…W nielicznych wypadkach" as in the print.',
     'Your hypothesis, confirmed against the print (bands 0064 3900-4750 / 0065 3400-4200). Four sibling cases found and repaired the same way (pp. 32→33, 38→39, 103→104, 116→117). A related class also surfaced: five pages whose whole first note was absorbed into the body (pp. 16, 20, 49, 99, 118) - repaired. See also the new items S23a-f.',
     'No action needed; flag only if you disagree.', 'S01_0065_quote_note.png'),
    ('S02', 'A', 'p. 14', 'Is the long commentary ONE note or several?',
     'Note 1 = "Podaną cyfrę trudno skontrolować…" runs ~9 printed lines of settlement commentary (Dąbrowo, Grabowiec, Łoskońskie… Goraj) set solid, no readable marker digits.',
     'The block could be one long note or several (2., 3. …) with unread markers.',
     'One note; if the print splits it, the split points are in the crop.',
     'S02_0029_note1_extent.png'),
    ('S03', 'B', 'p. 24', '13.915 dymów',
     '"Rzeczywista liczba dymów wiejskich … wynosi 13.915 dymów … W Tod. 89 brak zatem 552 dymów"',
     'Arithmetic: 13.353 + 552 = 13.905, not 13.915; and 552 × 6,41 = 3.538 fits the given person-count, so the TOTAL is the misread digit.',
     '13.905', 'S03_p24_13915.png'),
    ('S04', 'B', 'p. 26', '514 dymów × 6,05',
     '"Ostatnia rubryka aneksu I b wykazuje 514 dymów … współczynnik 6.05, otrzymamy 3.122 osoby"',
     '514 × 6,05 = 3.110, not 3.122.',
     'Either "516 dymów" or "3.110 osób"', 'S04_p26_514_dymow.png'),
    ('S05', 'B', 'p. 68', '608 morgów',
     '"Tutaj także role liczono na ślady, te jednakże równały się 2 włókom czyli 60 morgom. Tak samo w pobliskiej majętności wieleńskiej na włókę liczono 50 lub nawet 608 morgów normalnej wielkości."',
     '608 morgów per włóka is impossible (a włóka = 60 morgów); the trailing 8 looks like the footnote marker fused to "60".',
     '"60 morgów" (the 8 = the footnote marker)', 'S05_p68_608_morgow.png'),
    ('S06', 'B', 'p. 66 (Tabela V)', 'kościański row',
     '"kościański ......... = 45,5 | 6,8 | 41,7"',
     'The percent row must sum to 100 (45,5+6,8+41,7=94,0), and 41.7% of 44 settlements is not 21.',
     'third value "47,7" (21/44 = 47.7%)', 'S06_p66_tabelaV_row.png'),
    ('S07', 'B', 'p. 43, note 2', 'r. 1043',
     '"W r. 1043 olędrom Marianowa przedłużono dzierżawę na lat 30"',
     'Impossible year; the note\'s context is the 1677+ privilege era.',
     '"r. 1643"', 'S07_p43fn_r1043.png'),
    ('S08', 'B', 'p. 30, note 4', 'r. 1053',
     '"Inwentarz z r. 1053 odróżnia wsie polskie, niemieckie…"',
     'Impossible year; the parallel note (30-3) cites the same inventory as r. 1653.',
     '"r. 1653"', 'S08_p30fn_r1053.png'),
    ('S09', 'B', 'p. 16', 'Wymysłowo 1889/1890',
     '"Tp. 89, 90 — Wymysłowo, 1889 — 1 dym, 1890 — 1 dym"',
     'Impossible years; the whole passage is about Tp. 89/90 = 1789/1790.',
     '"1789 — 1 dym, 1790 — 1 dym"', 'S09_p16_wysylowo.png'),
    ('S10a', 'B', 'p. 98', '21 razy większa',
     '"Jest jednak od niego 21 razy większa. Czynsz wynosił 2627 zł."',
     'The context figure is 6588 zł: 6588/2627 ≈ 2.5, not 21.',
     '"2½ razy większa"', 'S10a_p98_21_razy.png'),
    ('S10b', 'B', 'p. 98', '8814 zł z włóki',
     '"na włókę przypadnie: w Nowych Dworach 8814 zł"',
     'Larger than the 3187 zł total for the whole osada.',
     '"88 zł 14 gr" (fits the "44 ½ zł" half-włóka figure below it)', 'S10b_p98_8814.png'),
    ('S11', 'B', 'p. 86', 'od 301 do 70? tynfów',
     '"przeciętnie 50 tynfów, wahając się w poszczególnych wypadkach od 301 do 70? tynfów"',
     'The range must bracket the 50 average.',
     '"od 30 do 70 tynfów"', 'S11_p86_301_70.png'),
    ('S12', 'B', 'p. 77', 'beczki i garnce',
     '"wyszynk roczny wynosił 229 beczek 56 garncy piwa, oraz 12 beczek -12121/ garnca wódki"',
     'Digit mush. Sanity: 8300 garnców piwa / 1152 osób ≈ 8 garnców per head suggests the beer figure; wódka 12 beczek i 12½ garnca fits the 1:16 ratio.',
     'verify both numbers from the crop', 'S12_p77_beczki.png'),
    ('S13', 'B', 'p. 78', '4:58 litra',
     '"garnca berlińskiego, który zawierał 4:58 litra"',
     'The colon is not this book\'s decimal separator.',
     '"3,58" or "4,58 litra"', 'S13_p78_litra.png'),
    ('S14', 'B', 'p. 68', 'The inline table: włóka area per pręt length',
     'Draft: "wyniesie 16,80 ha ,, „ U ) „„ ) 19, 10 H 1) ”» ” ,) 81/, x ) ,) ,, , 7 » » „ 24 20"',
     'The print tabulates włóka area (ha) for pręt lengths 7½, 8, 8½, 9 łokci. Math: 7½→16,80; 8→19,10; 8½→21,58; 9→24,20.',
     'confirm the four pairs', 'S14_p68_wloka_table.png'),
    ('S15', 'B', 'p. 98', 'przyorali 52/5 / 4%/, włóki',
     '"przyorali sobie 52/5, a w Folsztynie 4%/, włóki"',
     'Fraction glyphs; the Folsztyn figure fits ~4¾ (2627 zł over ~32 włóki).',
     'read both fractions from the crop', 'S15_p98_fractions.png'),
    ('S16', 'B', 'p. 47', '59/., sumy sprzedażnej',
     '"12-ty grosz 3, wyjątkowo 59/., sumy sprzedażnej"',
     '"5%" or "5/9 of the sale sum" - different meanings.',
     'carried from the earlier sitting; the glyph decides', 'S16_p47_59_sumy.png'),
    ('S17', 'B', 'p. 100', '109%/; kwoty',
     '"i opłat nie przekroczy 109%/; kwoty czynszowej"',
     '109% of the rent is odd; possibly 1/9 or 10%.',
     'read the glyph', 'S17_p100_109kwoty.png'),
    ('S18', 'B', 'p. 43', '"44 lata 3,"',
     '"W Ol. Ujskich dzierżawa wynosiła 44 lata 3, w Ol. Nowe Dwory 60 lat"',
     'The stray "3," right after "lata" - is it marker 3 riding the number, or part of the figure?',
     'confirm "44 lata" and the "3"', 'S18_p43_44_lata.png'),
    ('S19', 'E', 'p. 97', 'The German petition',
     'The 1743 petition of the Ujskie Olędry is quoted in German at length; the OCR is heavily corrupted ("Allcrgnidigst", "gintzlich", "Kónigł").',
     'If the quote matters for the edition it needs a careful re-read; otherwise mark it as an unchecked quotation (sic).',
     'editor\'s call: re-read or sic', 'S19_p97_german.png'),
    ('S23a', 'F', 'p. 49 (scan 0064, y≈2240-2430)', 'Degraded lines: after "Testamenty musiały być niekiedy sporzą-"',
     'The body ends "…Testamenty musiały być niekiedy sporzą-" and the note block follows; 1-2 lines are lost (the word completion and possibly more).',
     'The zone defeats OCR at 8x with thresholding/autocontrast/median (tried). The print itself is degraded there.',
     'leave the break, or supply the reading from your copy', 'S23a_0064_testamenty.png'),
    ('S23b', 'F', 'p. 99 (scan 0114, y≈3560-3780)', 'Degraded lines: after "podniosła się do 200"',
     'The body ends "…cena gospodarstwa … podniosła się do 200" and the note block follows; the amount\'s completion (1 line) is lost.',
     'Same degradation class; 8x + thresholding fails.',
     'leave the break, or supply the reading', 'S23b_0114_do200.png'),
    ('S23c', 'F', 'p. 101 (scan 0116, y≈4060-4280)', 'Degraded lines: after "znacznie podwyż-"',
     'The body ends "…Radca pruski v. Zacha wbrew przywilejowi znacznie podwyż-" mid-word; ~2 lines lost before the note block.',
     'Same degradation class; 8x + thresholding fails.',
     'leave the break, or supply the reading', 'S23c_0116_podwyz.png'),
    ('S23d', 'F', 'p. 108 (scan 0123, y≈3260-3470)', 'Degraded lines: after "…z lat 1764 i 1775 przywileje"',
     'The body ends "…W związku z reformami skarbowymi z lat 1764 i 1775 przywileje"; ~2 lines lost before the note block.',
     'Same degradation class; 8x + thresholding fails.',
     'leave the break, or supply the reading', 'S23d_0123_przywileje.png'),
    ('S23e', 'F', 'p. 109 (scan 0124, y≈4160-4400)', 'Degraded lines: after "Potwierdza to rów-"',
     'The body ends "…Potwierdza to rów-" mid-word; ~2-3 lines lost before the note block.',
     'Same degradation class; 8x + thresholding fails.',
     'leave the break, or supply the reading', 'S23e_0124_row.png'),
    ('S23f', 'F', 'p. 117 (scan 0132, y≈2600-2860)', 'Degraded lines: after "…kazań przez nauczyciela względnie"',
     'The body ends "…Tu należał zakaz wygłaszania kazań przez nauczyciela względnie"; 2 lines lost before the note runover.',
     'Same degradation class (the known case from the first sitting).',
     'leave the break, or supply the reading', 'S23f_0132_wzglednie.png'),
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
