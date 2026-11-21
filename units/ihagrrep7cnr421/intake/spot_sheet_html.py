# -*- coding: utf-8 -*-
"""The editor's spot sheet for I. HA GR, Rep. 7 C, Nr. 421 as one
self-contained HTML file (the page template of
units/ihagrrep7cnr3067/intake/spot_sheet_html.py). Written 2026-11-21.

    python units/ihagrrep7cnr421/intake/spot_sheet_html.py [--contact <png>]
      -> review/ihagrrep7cnr421/spot_sheet.html

Readings the four readers and Claude could not settle from the scans, the
readings Claude changed that the editor should see, then four decisions (two
person entries, the connection, the date of the suit). The first option of each
reading is what the transcription has now. Answers come back as JSON pasted into
the chat and are applied through intake/holding.py (CORRECTIONS), never here.
"""
import html
import io
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(UNIT))
sys.path.insert(0, os.path.join(ROOT, 'units', 'ihagrrep7cnr3067', 'intake'))
import spot_sheet_html as base  # noqa: E402

REV = os.path.join(ROOT, 'review', 'ihagrrep7cnr421')
OUT = os.path.join(REV, 'spot_sheet.html')
SRC = r'C:/Users/Tersnaus/Downloads/74344_Lacko/I_HA_Rep_7_C_Nr_421/processed/I_HA_Rep_7_C_Nr_421_%s.jpg'

# key, where, transcription now, options, question, (page, box)
ROWS = [
    ('q1', 'the cover, top left', 'd. 21 Octobr 1799',
     'd. 21 Octobr 1799|d. 24 Octobr 1799',
     'Your transcription had "24"; a reader is sure it is "21", the date of the King\'s answer (document 3). Claude changed it. Is that what the cover has?',
     ('0001_a', (0, 180, 1000, 400))),
    ('q2', 'document 1 (Chełmski\'s petition), the official\'s note in the left margin, second line',
     'beide in dieser Storstell[s?] rohl[?] unterstrichen',
     'beide in dieser Storstell[s?] rohl[?] unterstrichen|beide in dieser Vorstellung roth unterstrichen',
     'Two readers see "Vorstellung roth unterstrichen" (underlined in red in this petition); the petition does have a date underlined in red crayon on its third side. The rest of the note stays unread.',
     ('0002_a2', (40, 860, 1250, 1090))),
    ('q3', 'document 1, the decision in the left margin, seventh line', 'Anspruche anzugeben habe,',
     'Anspruche anzugeben habe,|Anspruche anzugeben hat,',
     'One reader sees "hat" (as the clean draft of the answer, document 3, has it); the other did not question your "habe".',
     ('0002_a2', (40, 2180, 1200, 2340))),
    ('q4', 'document 1, the decision in the left margin, eighth line', 'sich von selbst bescheiden werden.',
     'sich von selbst bescheiden werden.|sich von selbst bescheiden wird,|sich von selbst bescheiden werde',
     'One reader sees "wird," (the clean draft has "wird"), the other "werde".',
     ('0002_a2', (40, 2290, 1200, 2450))),
    ('q5', 'document 1, fourth side, line 4', 'dero Aufläger der',
     'dero Aufläger der|dero Hoflager den',
     '"an Allerhöchst dero ... Rekurs zu ergreifen" (to take recourse to Your Majesty\'s ...). A reader sees "Hoflager den" (Your Majesty\'s court); "Aufläger" is no word. The English already says "court".',
     ('0004_a1', (1150, 580, 2497, 820))),
    ('q6', 'document 1, sixth side, line 13', 'derung dieser Schä',
     'derung dieser Schä|Deckung dieser Schä',
     '"... zur derung dieser Schäden nicht hinreichend" (not sufficient to ... these damages). A reader suggests "Deckung" (to cover), which the English already says.',
     ('0005_a1', (1150, 1470, 2499, 1710))),
    ('q7', 'document 2 (the second decree), line 4', 'umsomehr, da er sollnst die¬',
     'umsomehr, da er sollnst die¬|umsomehr, da er selbst die¬|umsomehr, da er sonst die¬',
     '"... da er ... diese Forderung als eine persönliche behandelt" (since he ... treats this claim as a personal one). A reader sees "sonst" (otherwise); Claude sees "selbst" (himself), which gives the better sense.',
     ('0007_a1', (300, 620, 2528, 800))),
    ('q8', 'document 5 (the copy of Mondro\'s petition), the cabinet order\'s date', 'vom 10t dess. M.',
     'vom 10t dess. M.|vom 16t dess. M.',
     'The original petition (document 4) plainly has "vom 16ten deß. M." (16 September 1796). Does the copy have 10 or 16?',
     ('0011_a2', (80, 2560, 2467, 2740))),
    ('q9', 'document 6 (the suit), the date', 'Posen den 19ten Maert 1799.',
     'Posen den 19ten Maert 1799.|Posen den 19ten Maert 1796.',
     'The suit\'s own words fit 1796, not 1799: it names the Fiscus\'s eviction suit of 7 December 1795, a hearing on "27. Februar c." (of the current year), and payment due "zu Johanni v. J." (last year), where the bond had it due at St John\'s Day 1795. Is the last digit a 9 or a 6? (If 1799, the copyist may have miswritten it; Claude will flag it either way.)',
     ('0012_a2', (60, 380, 1800, 560))),
    ('q10', 'document 6, first line of the text', 'Unterm 16 Juny 1794. umste ich',
     'Unterm 16 Juny 1794. umste ich|Unterm 16 Juny 1794. muste ich|Unterm 16 Juny 1794. liehe ich',
     '"... umste ich dem Starosten ... 12000 # ... vorschücken" (I ... advanced the Starost 12,000 ducats). A reader suggests "muste ich" (I had to advance); not sure.',
     ('0012_a2', (300, 1640, 2587, 1810))),
    ('q11', 'document 6, lines 16 and 17', 'die Räth / palung[?]',
     'die Räth / palung[?]|die Rük / zalung',
     '"... daß, wofern die ... dieser 12000 # nicht in Termino ... erfolgen sollte" (that if the ... of these 12,000 ducats did not follow on the date). A reader suggests "Rükzalung" (repayment), broken over the two lines.',
     ('0012_a2', (300, 3320, 2587, 3550))),
    ('q12', 'document 6, second side, lines 6 and 7', 'Termine, re[?]ha[l?]¬ / lich zu Johanni',
     'Termine, re[?]ha[l?]¬ / lich zu Johanni|Termine, nem¬ / lich zu Johanni',
     '"Die Zalung ist auch in dem eingestandenen Termine, ... lich zu Johanni v. J. wirklich nicht erfolgt" (payment did not follow on the agreed date, ... at St John\'s Day last year). A reader suggests "nemlich" (namely).',
     ('0013_a1', (100, 730, 2579, 1070))),
    ('q13', 'document 6, third side, line 10', 'abregern, alsdann aber',
     'abregern, alsdann aber|abtragen, alsdann aber|abrechnen, alsdann aber',
     '"... von der Einnahme zuvorderst die Verzugs zinsen mit 7. pro[cent] ..." (first ... the interest at 7 per cent from the income). "abregern" is no word; a reader suggests "abtragen" or "abrechnen". The English says "deduct".',
     ('0013_a2', (350, 1250, 2571, 1400))),
    ('q14', 'document 6, third side, lines 12 and 13', '[?]a[i?]e[?] anforderen / gen[?]',
     '[?]a[i?]e[?] anforderen / gen[?]|meine Anforderun¬ / gen',
     '"dabei aber ... noch gerichtlich wahrnehmen soll" (while still pursuing ... at law). A reader suggests "meine Anforderungen" (my claims).',
     ('0013_a2', (350, 1390, 2571, 1680))),
    ('q15', 'document 6, fourth side, lines 5 and 6', 'die u[?]hab¬ / [h?]ören',
     'die u[?]hab¬ / [h?]ören|dieselben ab¬ / hören',
     '"... beziehe ich mich auch auf obige vorgeschlagenen Zeugen u. ... hören zu laßen" (I refer to the witnesses proposed above and ask that ... be heard). A reader suggests "dieselben abhören" (that they be heard); doubtful.',
     ('0014_a1', (150, 760, 2573, 990))),
    ('q16', 'document 6, the Polish bond, line 5', 'na wigilię Swiętego',
     'na wigilię Swiętego|na wigilię Swiętey',
     'A reader sees the word end in "-ey" ("Swiętey"), not "-ego". Correct Polish is "Świętego Jana"; the copyist may have written otherwise.',
     ('0014_a2', (1300, 730, 2570, 880))),
    ('q17', 'document 6, the Polish bond, line 7', 'z dobrey woli i na wgystnie iż',
     'z dobrey woli i na wgystnie iż|z dobrey woli i na wy[?]lnie iż',
     'A reader sees the word begin "wy", not "wg", with a long stroke below the third letter, and cannot read it. Can you?',
     ('0014_a2', (1300, 920, 2570, 1070))),
    ('q18', 'document 6, the Polish bond, line 15', 'nie exceptuiąc procz Zabryki',
     'nie exceptuiąc procz Zabryki|nie exceptuiąc procz Fabryki',
     '"... procz Zabryki Zelazney Magazynu y zborów Drzewa" (except the ... iron ..., the magazine and the timber stores). "Fabryki Żelazney" would be the ironworks. Is the first letter Z or F?',
     ('0014_a2', (1300, 1580, 2570, 1730))),
    ('q19', 'document 4, the office\'s slip, line 2', 'Es ist dem Capit[?]. cop.',
     'Es ist dem Capit[?]. cop.|Es ist dem Crim. R. cop.',
     'The addressee of the copy, Mondro. Both readers see an abbreviation beginning with C, probably "Crim." (Criminalrath); not "Capit".',
     ('0016_a2', (0, 950, 1350, 1110))),
    ('q20', 'document 4, the office\'s slip, line 3', 'principal geworden resol.',
     'principal geworden resol.|principal gewordenen resol.|principal ertheilten resol.',
     '"der seinem principal ... resol." (the resolution ... to his principal). One reader sees "gewordenen", the other "ertheilten".',
     ('0016_a2', (0, 1080, 1350, 1220))),
    ('q21', 'document 4, the office\'s slip, the last lines', 'de conclusi eodem / [Willen?]',
     'de conclusi eodem / [Willen?]|ita conclus. eod. / [Willen?]',
     'One reader sees "ita conclus. eod.", the formula under the decision in the margin of document 1 ("ita conclusum eodem"), signed with the same name.',
     ('0016_a2', (0, 1440, 1350, 1740))),
]

DECISIONS = [
    ('d1', 'A person entry for Stanisław Chełmski of Łukom',
     'The edition has one entry for the Chełmski family, which says the documents name several men not yet told apart. '
     'This file is about one of them, Stanisław von Chełmski of Łukom, skarbnik (the bond calls him so), who lent Prusimski '
     '12,000 ducats in 1794. A person entry would give him his own page; whether he is the Stanisław of the boundary decree of 1775 '
     'and of Boniecki would be noted as open. Built now: the family entry only.',
     'Keep the family entry only|Make a person entry'),
    ('d2', 'Mondro: the same man as the entry from Nr. 3705',
     'His name here is settled as Mondro, as he signs it (you asked me to fix the readings). The edition already has an entry "Mondro": '
     'the criminal councillor who was the Prince\'s attorney in the Olesnica suits of 1805 (I. HA GR, Rep. 7 C, Nr. 3705). '
     'Chełmski\'s lawyer here is a criminal councillor at Kalisz of the same name, so very probably the same man, working against '
     'the Prince in 1799. Built now: the entry tags him here too, so this file is on his page.',
     'Same man: keep|Another man: a separate entry'),
    ('d3', 'Connection: Chełmski\'s suit against the Prince (this file and the Prince\'s letters)',
     'On the site this puts a box on each document\'s page linking the others, each with a sentence. Triebenfeld\'s letters to the Prince '
     'of 1 April 1798 and 6 and 13 March 1799 follow "Chełmski\'s process" against the Prince (not yet appealed; lost in the second instance). '
     'This file is Chełmski\'s side: he held Trąbczyn on Prusimski\'s undertaking, had to give it up to the Prince after the judgment of '
     'revision, and then sued the Fiscus. The memorandum of 1815 in the same letters says the pledge was for 36,000 ducats; this file says '
     'the loan was 12,000 (the difference goes to the open questions). Dropping it removes the boxes; the documents stay.',
     'Keep|Drop'),
]


def main():
    corpus = io.open(os.path.join(UNIT, 'corpus.txt'), encoding='utf-8').read()
    cards = []
    for key, where, now, opts, note, (pid, box) in ROWS:
        assert now.split(' / ')[0] in corpus, (key, now)
        page = Image.open(SRC % pid)
        close = base.b64(page.crop(box), 1400)
        cy = (box[1] + box[3]) // 2
        wide = base.b64(page.crop((0, max(0, cy - 450), page.width, min(page.height, cy + 450))), 1400)
        btns = ''.join(f'<button class="opt" data-v="{html.escape(o)}">{html.escape(o)}</button>' for o in opts.split('|'))
        cards.append(f'''
<section class="row" data-key="{key}">
  <h2><span class="k">{key}</span> {html.escape(where)}</h2>
  <p class="q">{html.escape(note)}</p>
  <img src="{close}" alt="close crop on page {pid}">
  <details><summary>Show the lines around it</summary><img src="{wide}" alt="the lines around it on page {pid}"></details>
  <p class="ctx">Transcription now: <mark>{html.escape(now)}</mark></p>
  <div class="opts">{btns}<button class="opt" data-v="__unsure__">Can't tell</button><button class="opt" data-v="__other__">Something else</button></div>
  <input class="other" placeholder="What the page reads" hidden>
  <input class="note" placeholder="Note (optional)">
  <button class="miss" data-v="__wrongspot__">The picture doesn't show the word</button>
</section>''')
    for key, title, note, opts in DECISIONS:
        btns = ''.join(f'<button class="opt" data-v="{html.escape(o)}">{html.escape(o)}</button>' for o in opts.split('|'))
        cards.append(f'''
<section class="row" data-key="{key}">
  <h2><span class="k">{key}</span> {html.escape(title)}</h2>
  <p class="q">{html.escape(note)}</p>
  <div class="opts">{btns}<button class="opt" data-v="__other__">Something else</button></div>
  <input class="other" placeholder="Your word" hidden>
  <input class="note" placeholder="Note (optional)">
  <button class="miss" hidden></button>
</section>''')
    t = base.TEMPLATE.replace('Nr. 3067', 'Nr. 421').replace('ihagrrep7cnr3067', 'ihagrrep7cnr421')
    t = t.replace('__N__ readings the scans did not settle', '%d readings to check and %d decisions' % (len(ROWS), len(DECISIONS)))
    page = t.replace('__ROWS__', '\n'.join(cards)).replace('__N__', str(len(cards)))
    os.makedirs(REV, exist_ok=True)
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write(page)
    print(f'{len(cards)} rows -> {OUT} ({os.path.getsize(OUT) // 1024} KB)')
    if '--contact' in sys.argv:          # one picture of every close crop, to check them before handing over
        ims = []
        for key, where, now, opts, note, (pid, box) in ROWS:
            im = Image.open(SRC % pid).crop(box)
            im.thumbnail((1000, 150))
            ims.append(im)
        H = sum(i.height + 8 for i in ims)
        c = Image.new('RGB', (1000, H), 'white')
        y = 0
        for i in ims:
            c.paste(i, (0, y))
            y += i.height + 8
        c.save(sys.argv[sys.argv.index('--contact') + 1], quality=85)


if __name__ == '__main__':
    main()
