# -*- coding: utf-8 -*-
"""The editor's spot sheet for I. HA GR, Rep. 7 C, Nr. 3132 as one
self-contained HTML file (as units/ihagrrep7cnr3067/intake/spot_sheet_html.py,
whose page template it uses). Written 2026-11-20.

    python units/ihagrrep7cnr3132/intake/spot_sheet_html.py
      -> review/ihagrrep7cnr3132/spot_sheet.html

Readings the four readers and Claude could not settle from the scans, and
the readings Claude corrected on a witness that the editor should see; then
four decisions (a person entry, three connections). The first option of each
reading is what the transcription has now. Answers come back as JSON pasted
into the chat and are applied through intake/holding.py (CORRECTIONS), never
here.
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

REV = os.path.join(ROOT, 'review', 'ihagrrep7cnr3132')
OUT = os.path.join(REV, 'spot_sheet.html')
SRC = r'C:/Users/Tersnaus/Downloads/74344_Lacko/I_HA_Rep_7_C_Nr_3132/processed/I_HA_Rep_7_C_Nr_3132_%s.jpg'

# key, where, transcription now, options, question, (page, box)
ROWS = [
    ('q1', 'document 1 (Goldbeck, 19 Feb.), line 14', 'mitzuzeichnen',
     'mitzuzeichnen|mitzuziehnen',
     'Your transcription had "mitzuziehnen", which is no word; Claude changed it to "mitzuzeichnen" (to countersign), '
     'the words of Goldbeck\'s next letter ("solches gefälligst mitzuzeichnen"). Is that what the page has?',
     ('0002_a2', (0, 1440, 2566, 1760))),
    ('q2', 'document 3 (Haugwitz\'s draft), left column, first line', 'An d 29 Apr. 1803',
     'An d 29 Apr. 1803|Berl. d 29 Apr. 1803|Praes. d 29 Apr. 1803',
     'The first word before the date. One reader sees "Berl." (Berlin), one "Praes." (received); Claude cannot settle it.',
     ('0005_a2', (0, 60, 1500, 400))),
    ('q3', 'document 3, left column, the address', 'des tot[?] lit Herrn von',
     'des tot[?] lit Herrn von|tit. tit. Herrn von',
     'The address to Goldbeck. Claude sees the formula "tit. tit." ("titulo titulo", with all titles) and cannot read the first word.',
     ('0005_a2', (0, 540, 1100, 800))),
    ('q4', 'document 3, left column, the subject', '[?]n Prusiemski &',
     '[?]n Prusiemski &|In re Prusiemski &|In Prusiemski &',
     'The word before "Prusiemski". One reader sees "In re" (in the matter of).',
     ('0005_a2', (0, 920, 1100, 1220))),
    ('q5', 'document 3, line 27', 'hinzufügen in[?] müssen',
     'hinzufügen in[?] müssen|hinzufügen zu müssen|hinzuzufügen müssen',
     'Both readers see no "in" here, but a "zu" written above the line over "hinzufügen", with letters struck through in the word.',
     ('0005_a2', (900, 3380, 2544, 3700))),
    ('q6', 'document 5 (the joint report), page 3, line 18', 'da solcher',
     'da solcher|derselben|da selbiger',
     '"... mich enthalte, da solcher nicht meines Ressorts ist". A reader and Claude see one word here, not two; '
     'which, neither can settle.',
     ('0009_a2', (0, 2190, 2517, 2440))),
    ('q7', 'document 5, page 3, line 13', 'gegen sie',
     'gegen sie|sagen sie',
     'Your transcription had "sagen sie"; Claude changed it to "gegen sie" ("noch sonst eine Lebensstrafe gegen sie festgesetzt"), '
     'the only reading that makes a sentence. Is that what the page has?',
     ('0009_a2', (0, 1640, 2517, 1960))),
    ('q8', 'document 8 (the resolution), first line', 'U. A. H.',
     'U. A. H.|U. A. B.|etc. etc. etc.',
     'Your transcription had "[U?]. A. B."; Claude made it "U. A. H." (Unser allergnädigster Herr), the fixed formula of a '
     'resolution in the King\'s name. One reader saw "etc. etc. etc.".',
     ('0012_a2', (0, 2880, 2531, 3180))),
    ('q9', 'document 7 (the rescript to Poznań), above the signatures', 'Auzl p.',
     'Auzl p.|Ausz. p.|Auf p.',
     'The word before "p. Special-Befehl" (here and at the foot of document 8). One reader saw "Auszl:".',
     ('0012_a2', (400, 1600, 2200, 1840))),
    ('q10', 'document 4, the slip, lines 3 and 4', 'Sr[?] / [?] Unterschrift vorzulegen[?]',
     'Sr[?] / [?] Unterschrift vorzulegen[?]|Sr / Excellenz Unterschrift vorzulegen',
     '"Die munda sind zu Sr ... Unterschrift vorzulegen" (the fair copies are to be laid before ... for signature). '
     'Claude reads the second line\'s first word as "Excellenz", abbreviated; not sure.',
     ('0013_a2', (0, 1150, 2137, 1580))),
    ('q11', 'document 4, the slip, line 12', 'einem [?]',
     'einem [?]|einem Schreiben',
     '"2, Exp. 2. neml. einem ..." - the word after "einem" is not read (it does not begin with h, as your transcription had).',
     ('0013_a2', (0, 2480, 2137, 2740))),
    ('q12', 'document 4, the slip verso, line 4', 'geschehen sey anhero an¬',
     'geschehen sey anhero an¬|ausfertigen an¬',
     'Claude and one reader read "geschehen sey anhero an-" (as the Chamber\'s order: "wie solches geschehen anhero zu berichten"); '
     'the other reader saw "ausfertigen an-".',
     ('0014_a1', (0, 1720, 2062, 2000))),
    ('q13', 'document 4, the slip verso, line 8', '[?] Haug[witz]',
     '[?] Haug[witz]|zeichnung Haug[witz]|Graf Haug[witz]',
     'The word after "v. Voss zur Mit-", before the paraph. One reader sees "zeichnung" (Mitzeichnung), the other "Graf".',
     ('0014_a1', (0, 2360, 2062, 2680))),
    ('q14', 'document 9 (the draft to Voss), line 24', 'seiner beigefügte',
     'seiner beigefügte|für königliche|zur königlichen',
     '"... im Concept und Mundo seiner beigefügte Notificatorium". The first word: one reader sees "für königliche", the other "zur königlichen".',
     ('0014_a2', (700, 2330, 2538, 2540))),
]

DECISIONS = [
    ('d1', 'A person entry for Xaver Jezierski',
     'Built: Jezierski, the canon of Włocławek who petitioned with Prusimski, has an entry on the People page (only in this file). '
     'For Nr. 3067 you wanted no entries for the condemned; he is a party here, not a name in a list.',
     'Keep the entry|No entry'),
    ('d2', 'Connection: the wife in Italy (Nr. 1414, Nr. 12366 and this report)',
     'The report says his wife stayed in Italy for her health and died there, as the Venice dispatch of 1796 and the daughter\'s claim '
     'of 1818 do. The claim also says he survived her "only a short time", while this report has him alive at Dresden in 1803.',
     'Keep|Drop'),
    ('d3', 'Connection: the three generals (Michalina\'s petition of 1807 and this report)',
     'Her petition names Hohenlohe, Bischoffswerder and Zanitz as the generals given her father\'s estates; the report of 1803 says '
     'which estate went to whom (Trąbczyn to Hohenlohe, Pawłów to Sanitz, Smiłowice to Bischofswerder).',
     'Keep|Drop'),
    ('d4', 'Connection: Goldbeck keeps the confiscation (Nr. 3067 and this report)',
     'In 1797 Goldbeck advised that the fled ringleaders\' confiscation stand; in 1803 he and Haugwitz call it unalterable when Prusimski is let home.',
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
    t = base.TEMPLATE.replace('Nr. 3067', 'Nr. 3132').replace('ihagrrep7cnr3067', 'ihagrrep7cnr3132')
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
            im.thumbnail((1000, 160))
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
