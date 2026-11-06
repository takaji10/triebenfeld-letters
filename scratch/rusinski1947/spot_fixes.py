# -*- coding: utf-8 -*-
"""spot_fixes: the editor's spot-answer round applied to the draft
layer. Runs AFTER marked_lines, BEFORE compose.

1. marked_lines.json body text fixes (line-addressed, verified against
   the print / the editor's rulings).
2. sliver-line removal (single-letter warp junk that fused onto
   hyphen fragments: 'sporzą-' + 'z' -> 'sporząz').
3. structure4.json note-text fixes (S08 r. 1653; 0058's r. 1643 /
   60 lat; 0113's note block rebuilt to the print's SIX notes).
"""
import json, os, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'

# (scan, top_lo, top_hi, old, new)
BODY_FIXES = [
    # 0044: the ',' after '40%' = the %'s own circles misread -
    # pixel check (x2085-2170, y1409-1498) shows '40%' + the %'s
    # lower-right circle, then 'ogółu'
    ('0044', 1400, 1440, '40%,', '40%'),
    ('0039', 2200, 2320, '13.915', '13.915 [sic]'),
    ('0058', 1900, 2010, 'wynos ła', 'wynosiła'),
    ('0058', 3080, 3180, 'Gebhrrdta', 'Gebhardta'),
    ('0058', 2760, 2870, 'rozb.o-', 'rozbio-'),
    ('0058', 3380, 3480, 'ze łożonych', 'założonych'),
    ('0092', 3250, 3400, '-12121/,', '121½'),
    ('0093', 950, 1060, '4:58', '4,58'),
    ('0062', 1780, 1900, '59/,', '5%'),
    ('0101', 1800, 1900, 'rdzbiorów', 'rozbiorów'),
    ('0101', 2830, 2950, 'pastwiskowe 1 leśne', 'pastwiskowe i leśne'),
    ('0101', 3150, 3260, 'płacono I zł10', 'płacono 1 zł10'),
    ('0113', 1850, 1950, '21 razy', '2½ razy'),
    ('0113', 2080, 2200, '52/5,', '5 2/5,'),
    ('0113', 2130, 2230, '4%/,', '4 3/5,'),
    ('0113', 2360, 2460, '8814', '88½'),
    ('0114', 3450, 3600, 'do 200 z', 'do 200'),
    ('0131', 3400, 3560, 'rzeczy v', 'rzeczy'),
    ('0115', 1580, 1700, '109%/;', '10%'),
    ('0065', 600, 760, 'dzone w określonej formie', 'dzane w określonej formie'),
]

S14_LINES = {
    1150: 'powierzchnia włóki wymierzona prętem 7½-łokciowym wyniesie '
          '16,80 ha; 8 łokci — 19,10 ha; 8½ łokci — 21,60 ha; 9 łokci — '
          '24,20 ha.',
}

# whole junk lines to drop: (scan, top) - warp fragments that poison
# the within-paragraph hyphen joins ('materia-' + 'w pracy' -> 'materiaw')
DROP_LINES = [
    ('0017', 912),
    # Tabela V: the dot-leader and header-fragment junk lines (the
    # table is rebuilt by LINE_TEXT)
    ('0081', 1430), ('0081', 1477), ('0081', 1562), ('0081', 1605),
    ('0081', 1655), ('0081', 1744), ('0081', 1762), ('0081', 1922),
    ('0081', 2039), ('0081', 2075), ('0081', 2162), ('0081', 2560),
    ('0081', 2683),
    # 0103: sliver lines between the body lines - the words the
    # structure reads lost ('po', 'za', three dashes); the content is
    # restored by the LINE_TEXT rewrites below
    ('0103', 1963), ('0103', 2699), ('0103', 2931), ('0103', 3036),
    ('0103', 3143),
    # 0023: the 'nazwy z' fragment folded into the 1938 rewrite
    ('0023', 1968),
]

# whole line RANGES to drop: (scan, lo, hi) - the German petition's
# continuation lines (S19: the quote rewritten from the 3x band reads
# onto the range's first lines)
DROP_RANGES = [
    ('0112', 2064, 2900),
    ('0112', 3013, 4340),
]

# line rewrites: (scan, top, new_text)
LINE_TEXT = {
    # S06: Tabela V rebuilt - the absolute rows confirmed by the
    # editor's reading (44|20|3|21; 20+3+21=44) and the arithmetic of
    # every other row (17+3+58=78, 37+6+79=122; the percents 45,5/6,8/
    # 47,7 = the counts over 44)
    ('0081', 1390): 'Ogólna liczba osad zapisanych w źródłach; liczba '
                    'osad powstałych odpowiednio:',
    ('0081', 1858): 'w absolutnych cyfrach =',
    ('0081', 1987): 'kościański 44 20 3 21',
    ('0081', 2126): 'poznański 78 17 3 58',
    ('0081', 2286): 'Razem 122 37 6 79',
    ('0081', 2436): 'procentowo:',
    ('0081', 2505): 'kościański 45,5 6,8 47,7',
    ('0081', 2648): 'poznański 21,8 3,8 74,4',
    ('0081', 2808): 'Razem — 30,3 4,9 64,8',
    # S19: the 1782 petition of Bracknitzer Holl., re-read at 3x
    ('0112', 2015): '„Nachdem Ihro Majestät aus besonderer Gnadenbezeigung '
                    'gerichtet haben, uns allergnädigst bey unserer alten '
                    'Gerechtigkeit, so wie ehemals unter Königlich '
                    'Pohlnischer Regierung genossen, zu schützen und '
                    'unverändert dabei zu erhalten; wir aber '
                    'demohngeachtet nach der Maassgabe des Conducteurs '
                    'Eichmann, welcher unsere Felder vor zwey Jahren '
                    'gemessen, in unsern Abgaben sehr erhöhet worden, '
                    'indem gedachter Conducteur aus unsern Gründen weit '
                    'mehr gemessen als wir nach altem Königlich '
                    'Pohlnischen Maasse wirklich besitzen. Da doch unsere '
                    'Gründe vor wenig Jahren noch durch die ehemalige '
                    'Pohlnische Obrigkeit aufs allergenauste gemessen '
                    'wurden und zwar jeden Morgen zu 300 Ruthen, jede '
                    'Ruthe zu 8 Ellen, jede Elle zu 24 Zoll, die '
                    'Baustelle wurde aus einem Morgen, darzu Graben, Wege '
                    'und Triften Zinsfrey gelassen.',
    ('0112', 2910): 'Darnachst wurde uns zu Pohlnischen Zeiten gestattet '
                    'freyes Bau-Holz, sowohl zu Reparaturen als auch zu '
                    'gantz neuem Bau von der Königlichen Heide zu holen, '
                    'welches uns auch bisher von Ihro Majestät unserm '
                    'allergnädigsten Könige zwar noch nicht ist gänzlich '
                    'abgeschlagen, dennoch aber bis dato noch keines '
                    'erhalten haben, so höchstnöthig es auch bey vielen '
                    'unserer Einsassen, deren Gebäude alt und baufällig '
                    'ist, zu gebrauchen wären. Wir sind überzeugt, dass '
                    'Ihro Majestät, unser allergnädigster König und Herr, '
                    'uns Landes-Väterlicher Hulde geruhen werden, diese '
                    'unsere Bitte, so wir denenselben in tiefster '
                    'Ehrfurcht und Veneration übergeben, allergnädigst '
                    'von uns auch annehmen werden, und uns in obbemeldten '
                    'Puncten laut unserm Privilegio bey unsern alten '
                    'Rechten und Schützen behalten werden, welche uns, '
                    'seitdem unsere Gründe durch obbemeldten Conducteur '
                    'gemessen worden, dessen Maassgabe wir unmöglich vor '
                    'richtig annehmen und erkennen können, sind gesindert '
                    'und unsere Abgaben erhöhet worden, unangesehen das '
                    'unsere Gründe schlecht und im gantzen hiesigen Amte '
                    'den sandigsten und untragbarsten Boden gaben, wenn '
                    'wir bey Ihro Majestät unserm allergnädigsten Könige '
                    'die hohe Gnade erhalten, werden wir uns verpflichtet '
                    'halten dero Leutseligkeit und Gnadenbezeigung '
                    'lebenslang zu rühmen, und dabei unveränderlich '
                    'zeigen das wir seyn Eur. Königl. Majestät '
                    'allerunterthänigste Knechte. Bracknitzer Holl., '
                    'd. 22-ten May 1782”.',
}

# 0099 line 892: the structure lost the raised 2 after 'sąsiednich'
# (band read '?. '); the full line with the label in place
LINE_TEXT[('0099', 892)] = ('mieszkańców osad sąsiednich[^84-2]. '
                            'Opieka taka dla olędrów wyrażała się')

# 0103: restore the words/dashes the structure reads dropped into
# sliver lines, and place the okupne-chronology labels
LINE_TEXT[('0103', 1941)] = ('15 szóstaków (== 120 zł)[^88-1] i 100 '
                             'talarów po kursie 5 zł za talar (== 500')
LINE_TEXT[('0103', 2657)] = ('wysokość okupnego ustala się na mniej '
                             'więcej 100 zł z huby. W ostat-')
LINE_TEXT[('0103', 2893)] = ('(r. 1771 — role uprawne z budynkami)'
                             '[^88-10], 24 zł (r. 1773)[^88-11], '
                             '30 czerwonych')
LINE_TEXT[('0103', 3004)] = ('zł (r. 1775)[^88-12], 900 zł (role uprawne '
                             'z budynkami — r. 1776 i 1781)[^88-13],')
LINE_TEXT[('0103', 3108)] = ("10 czerw. zł (r. 1783)[^88-14], 1.800 zł "
                             'i 1.500 zł (role uprawne z budynkami —')
LINE_TEXT[('0103', 2259)] = ('kiem wartości pieniądza podrosi się '
                             'nominalnie suma okupnego, do-')
LINE_TEXT[('0051', 2989)] = ('czystej, względnie w przyrodzonej '
                             'skłonności do wędrówek[^36-5].')
LINE_TEXT[('0129', 696)] = ('regoś. z gospodarzy[^114-1]. Utrzymanie '
                            'nauczyciela umożliwiał pan, przy-')
LINE_TEXT[('0134', 2885)] = ('ciem duchowym gminy. Stąd też Stenger '
                             'wspomina o nich z ironią[^119-3].')
LINE_TEXT[('0135', 677)] = ('błogosławieństwem dla swojej '
                            'okolicy[^120-1]. Zgodnie z zasadami swych.')
LINE_TEXT[('0022', 2344)] = ('na obszarze Prus Królewskich i '
                             'Książęcych[^7-4]. Na oznaczenie osz-')
LINE_TEXT[('0023', 1938)] = ('wstała przez pomieszanie nazwy osadników '
                             'z nazwą karczunków')
LINE_TEXT[('0023', 2041)] = 'leśnych[^8-3].'

SLIVER = re.compile(r'[zvwaoi][.,]?')


def main():
    ml_path = os.path.join(OCR, 'marked_lines.json')
    ml = json.load(open(ml_path, encoding='utf-8'))
    nfix = 0
    nsliver = 0
    for n in sorted(ml):
        lines = ml[n]['lines']
        out = []
        for l in lines:
            txt = l['text'].strip()
            if SLIVER.fullmatch(txt) or (n, l['top']) in DROP_LINES \
                    or any(scan == n and lo <= l['top'] < hi
                           for (scan, lo, hi) in DROP_RANGES):
                nsliver += 1
                continue
            if (n, l['top']) in LINE_TEXT:
                l['text'] = LINE_TEXT[(n, l['top'])]
            for (scan, lo, hi, old, new) in BODY_FIXES:
                if scan == n and lo <= l['top'] < hi and old in l['text']:
                    l['text'] = l['text'].replace(old, new, 1)
                    nfix += 1
            if n == '0083' and l['top'] in S14_LINES:
                l['text'] = S14_LINES[l['top']]
            elif n == '0083' and 1180 <= l['top'] < 1470:
                l['text'] = ''
            out.append(l)
        ml[n]['lines'] = out
    json.dump(ml, open(ml_path, 'w', encoding='utf-8', newline='\n'),
              ensure_ascii=False)
    print('body fixes applied:', nfix, '| sliver lines dropped:', nsliver)

    s_path = os.path.join(OCR, 'structure4.json')
    s = json.load(open(s_path, encoding='utf-8'))

    def note_fix(scan, num, old, new):
        for x in s[scan]['notes']:
            if x['num'] == num and old in x['text']:
                x['text'] = x['text'].replace(old, new, 1)
                return True
        return False

    ok = []
    ok.append(('0045 #4 r. 1053->1653',
               note_fix('0045', 4, 'r. 1053', 'r. 1653')))
    ok.append(('0058 #5 r. 1043->1643',
               note_fix('0058', 5, 'r. 1043', 'r. 1643')))
    ok.append(('0058 #6 na 00 lat->60 lat',
               note_fix('0058', 6, 'na 00 lat', 'na 60 lat')))
    # S09 (editor): the 1889/1890 datings are the book's own error -
    # marked [sic]
    for x in s['0031']['notes']:
        if '1889 — 1 dym, 1890 — 1 dym' in x['text']:
            x['text'] = x['text'].replace(
                '1889 — 1 dym, 1890 — 1 dym',
                '1889 [sic] — 1 dym, 1890 [sic] — 1 dym', 1)
            ok.append(('0031 #1 1889/1890 [sic]', True))
            break
    else:
        ok.append(('0031 #1 1889/1890 [sic]', False))
    ok.append(('0113 #1 377 1 nast.->377 i nast.',
               note_fix('0113', 1, '377 1 nast.', '377 i nast.')))
    ok.append(('0113 #2 KI./tol.->Kl./fol.',
               note_fix('0113', 2, 'KI. XII 7 tol.', 'Kl. XII 7 fol.')))
    # 0113's note block: the print has SIX notes; the strip merged
    # 3-6 into stored note 3 (band-read 4150-5450 verified). Idempotent:
    # skipped when already rebuilt.
    if len(s['0113']['notes']) == 3:
        old3 = [x for x in s['0113']['notes'] if x['num'] == 3][0]
    if len(s['0113']['notes']) == 3:
        t3 = old3['text']
        i4 = t3.find('4 Wskutek')
        i5 = t3.find('5 W r. 1773')
        i6 = t3.find('6 Gumowski')
        assert i4 > 0 and i5 > i4 and i6 > i5, '0113 split points missing'
        n4 = t3[i4 + 1:i5].strip()
        n5 = t3[i5 + 1:i6].strip()
        n6 = t3[i6 + 1:].strip()
        n4 = (n4.replace('30%/;', '30%').replace('271/4', '27¼')
              .replace('313/,', '31¾'))
        n5 = n5.replace('w r. 1077', 'w r. 1677')
        s['0113']['notes'] = [
            {'num': 1, 'top': 4213, 'text': 'Geschichte, s. 377 i nast.',
             'src': 'repair-noteblock'},
            {'num': 2, 'top': 4303,
             'text': 'Kl. XII 7 fol. 170—191, Folsztyn, fol. 229 i nast., '
                     'Nowe Dwory.', 'src': 'repair-noteblock'},
            {'num': 3, 'top': 4392, 'text': 'J. w., fol. 191.',
             'src': 'repair-noteblock'},
            {'num': 4, 'top': 4460, 'text': n4, 'src': 'repair-noteblock'},
            {'num': 5, 'top': 4560, 'text': n5, 'src': 'repair-noteblock'},
            {'num': 6, 'top': 5060, 'text': n6, 'src': 'repair-noteblock'},
        ]
        ok.append(('0113 notes 3->6', True))
    else:
        ok.append(('0113 notes 3->6 (already rebuilt)', True))
    # 0095's note block: the print has SEVEN notes; the strip merged
    # note 7 (AW. Borkowskie, the owiec note) into note 6 after
    # "...po kurze”." (zoom-read 4919-5130 verified the leading '7').
    # Also note 2's OCR slips: 'Nowc'->'Nowe', 'fol. 560'->'fol. 660'
    # (TSV word box '660).'). Idempotent via the note count.
    ok.append(('0095 #2 Nowc->Nowe',
               note_fix('0095', 2, 'OIL. Nowc Dwory', 'Ol. Nowe Dwory')))
    ok.append(('0095 #2 fol. 560->660',
               note_fix('0095', 2, 'fol. 560', 'fol. 660')))
    # 0098: note 6 carries the next note's '7' glued by the strip;
    # note 8 caught the page footer ('(3%').
    ok.append(('0098 #6 stray 7',
               note_fix('0098', 6, 'Kawczyn Ol. 7', 'Kawczyn Ol.')))
    ok.append(('0098 #8 footer junk',
               note_fix('0098', 8, ' (3%', '')))
    # 0105: the print has TWELVE notes; the strip merged note 7
    # ('7 AW. Paproć, C. 2, fol. 255 (Lipiec Małe OI.); Rel. Cost.
    # nr 223, r. 1787, fol. 182.') into note 6 after 'A. I.' (the '7"?'
    # = note 7's number glyph; linemap 4204 = the '7' line). Split and
    # renumber 8-12. Idempotent: skipped when a Paproć note exists.
    n6 = [x for x in s['0105']['notes'] if x['num'] == 6]
    if n6 and 'Paproć' in n6[0]['text'] and not any(
            x['text'].strip().startswith('AW. Paproć')
            for x in s['0105']['notes']):
        t6 = n6[0]['text']
        i7 = t6.find('Paproć')
        assert i7 > 0, '0105 split point missing'
        n6new = re.sub(r'\s*7”? AW\.?\s*$', '', t6[:i7]).strip()
        n7txt = t6[i7:].strip()
        if not n7txt.startswith('AW.'):
            n7txt = 'AW. ' + n7txt
        n6[0]['text'] = n6new
        rest = [x for x in s['0105']['notes'] if x['num'] > 6]
        for x in rest:
            x['num'] += 1
        s['0105']['notes'].append({'num': 7, 'top': 4204,
                                   'text': n7txt,
                                   'src': 'repair-noteblock'})
        s['0105']['notes'].sort(key=lambda x: x['num'])
        ok.append(('0105 notes 6->7 split', True))
    else:
        ok.append(('0105 notes 6->7 split (already rebuilt)', True))
    if len(s['0095']['notes']) == 6:
        old6 = [x for x in s['0095']['notes'] if x['num'] == 6][0]
        t6 = old6['text']
        i7 = t6.find('7 AW. Borkowskie')
        assert i7 > 0, '0095 split point missing'
        n6 = t6[:i7].strip()
        n7 = t6[i7 + 1:].strip()
        old6['text'] = n6
        s['0095']['notes'].append({'num': 7, 'top': 4919, 'text': n7,
                                   'src': 'repair-noteblock'})
        ok.append(('0095 notes 6->7', True))
    else:
        ok.append(('0095 notes 6->7 (already rebuilt)', True))
    # 0107: the print has SIX notes - the strip merged note 4 ('Kl.
    # XII 6 V, fol. 36, Króteckie Ol.; AW. Rożnowskie OI., B. 770;
    # Rel. Posn. nr 641, r. 1792, fol. 127, Rudka OI.; tamże, fol. 163,
    # Zamorze OI.') into note 3 after 'Charłub OI.' (its '4' misread
    # as '''; linemap 4386 = the '4' line). Split and renumber 4-6.
    n3 = [x for x in s['0107']['notes'] if x['num'] == 3]
    _kxii = re.compile(r'[Kk][Iil]\.\s*XII\s*6\s*V,\s*fol\.\s*36')
    if n3 and _kxii.search(n3[0]['text']) and not any(
            _kxii.match(x['text'].strip()) for x in s['0107']['notes']):
        t3 = n3[0]['text']
        m4 = _kxii.search(t3)
        assert m4, '0107 split point missing'
        n3new = t3[:m4.start()].strip()
        n4txt = t3[m4.start():].strip()
        rest = [x for x in s['0107']['notes'] if x['num'] > 3]
        for x in rest:
            x['num'] += 1
        s['0107']['notes'].append({'num': 4, 'top': 4386,
                                   'text': n4txt,
                                   'src': 'repair-noteblock'})
        s['0107']['notes'].sort(key=lambda x: x['num'])
        ok.append(('0107 notes 3->4 split', True))
    else:
        ok.append(('0107 notes 3->4 split (already rebuilt)', True))
    # 0134: the print has THREE notes - the strip split note 2's
    # German quote (pastor Piotrowa's complaint) into a phantom note 3
    # ('Jahre als Prediger hier...' = the quote's continuation line),
    # and the real note 3 ('Von den Haulindern, s. 254.') sits as
    # note 4. Merge the phantom back and renumber 4 -> 3; also fix
    # 'Hauliindern' and the stray ' ,' tail.
    n2 = [x for x in s['0134']['notes'] if x['num'] == 2]
    n3 = [x for x in s['0134']['notes'] if x['num'] == 3]
    if n3 and n3[0]['text'].strip().startswith('Jahre als Prediger'):
        n2[0]['text'] = (n2[0]['text'].rstrip() + ' '
                         + n3[0]['text'].strip())
        s['0134']['notes'].remove(n3[0])
        for x in s['0134']['notes']:
            if x['num'] > 3:
                x['num'] -= 1
        s['0134']['notes'].sort(key=lambda x: x['num'])
        ok.append(('0134 notes merge 3->2, renum 4->3', True))
    else:
        ok.append(('0134 notes merge (already rebuilt)', True))
    ok.append(('0134 #3 Hauliindern+tail',
               note_fix('0134', 3, 'Hauliindern, s. 254. 7',
                        'Haulindern, s. 254.')))
    # 0044: the strip's 'note 1' ('Wszystkie wspomniane osady lokowane
    # są na podmokłej nizinie nadnoteckiej...') is actually LIST ITEM 1
    # of the 'szereg pewnych, niezbitych danych zrodlowych'
    # enumeration - its lines (3457/3553/3668) are already body lines
    # and 0045 carries items 2. and 3. Remove the pseudo-note and
    # renumber the real notes 2,3,4 -> 1,2,3. Idempotent via the
    # 'Wszystkie' guard.
    if any(x['text'].lstrip().startswith('Wszystkie wspomniane')
           for x in s['0044']['notes']):
        s['0044']['notes'] = [x for x in s['0044']['notes']
                              if not x['text'].lstrip()
                              .startswith('Wszystkie wspomniane')]
        for x in s['0044']['notes']:
            x['num'] -= 1
        ok.append(('0044 pseudo-note removed, renumbered', True))
    else:
        ok.append(('0044 pseudo-note (already rebuilt)', True))
    # 0041: the print has THREE notes - the strip merged note 3
    # ('Współczynnik ten, obliczony na podstawie danych z r. 1789...')
    # into note 2 after 'lub KI. i G.' (linemap 4849 = the '3'
    # line). Split and renumber. Idempotent via the note count.
    if len(s['0041']['notes']) == 2:
        n2 = [x for x in s['0041']['notes'] if x['num'] == 2][0]
        t2 = n2['text']
        i3 = t2.find('3 Współczynnik')
        assert i3 > 0, '0041 split point missing'
        n2['text'] = t2[:i3].strip()
        s['0041']['notes'].append({'num': 3, 'top': 4849,
                                   'text': t2[i3 + 1:].strip(),
                                   'src': 'repair-noteblock'})
        ok.append(('0041 notes 2->3', True))
    else:
        ok.append(('0041 notes 2->3 (already rebuilt)', True))
    json.dump(s, open(s_path, 'w', encoding='utf-8', newline='\n'),
              ensure_ascii=False)
    for name, done in ok:
        print('%s %s' % ('PASS' if done else 'FAIL', name))


if __name__ == '__main__':
    main()
