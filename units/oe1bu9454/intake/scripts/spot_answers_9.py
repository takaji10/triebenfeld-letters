# -*- coding: utf-8 -*-
"""Oe 1 Bü 9454, letter 9: the editor's answers on the spot sheet "Letter 9" (2026-10-15).

    python units/oe1bu9454/intake/scripts/spot_answers_9.py            # check only
    python units/oe1bu9454/intake/scripts/spot_answers_9.py --write    # once

All eleven rows answered (intake/letter_9_answers.json keeps them). Confirmed as the text had
them: betreibe ich durch ihn, wenn, Eben so gl[...], [vorgerübene?], Borgen, davon läuft der
Bösewicht, schändlich. Changed:
  v02 Kedl -> [Kedl?]          the editor cannot tell either; neither reading confirms the name;
  v03 [säh?] -> [seie?]        the editor: "seie", "Possibly";
  v04 [St. K. F. H.?] -> St[aats]. K[anzler]. F[ürst]. H[ardenberg].   the editor confirms the
                               four initials; expanded as the holding expands title initials
                               (F[ürst]. H[ardenberg].), Hardenberg being Staatskanzler at Vienna;
  v05 weiß -> [weiß?]          the editor cannot tell (their file had "aus").
The English (intake/translation/doc9.yml) and the reading record follow.
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT = os.path.dirname(os.path.dirname(HERE))
ROOT = os.path.dirname(os.path.dirname(UNIT))
KEY = 'oe1bu9454-009'
PAGE_FILE = os.path.join(UNIT, 'transcriptions', '0021_Oe 1_Bue 9454_0015_b.txt')

TEXT = [
    ('Kedl [...] hat ihm gesagt', '[Kedl?] [...] hat ihm gesagt'),
    ('gerne [säh?] ich dem Patron', 'gerne [seie?] ich dem Patron'),
    ('für [...] [St. K. F. H.?] was anzubringen', 'für [...] St[aats]. K[anzler]. F[ürst]. H[ardenberg]. was anzubringen'),
    ('mit da [...] weiß ich das wie', 'mit da [...] [weiß?] ich das wie'),
]
ENGLISH = [
    ('Kedl [text lost] has told him', '[uncertain: Kedl] [text lost] has told him'),
    ('I should gladly [uncertain: see] the Patron', 'I should gladly [uncertain: seie] the Patron'),
    ('for [text lost] [uncertain: St. K. F. H.] is to be brought forward',
     'for [text lost] the State Chancellor Prince Hardenberg is to be brought forward'),
    ('with the [text lost] I know the how and where', 'with the [text lost] I [uncertain: know] the how and where'),
    ('marker_count: 20', 'marker_count: 21'),
    ('words read with doubt are "[uncertain: ...]", as in the rest of the holding: 17 and 3, as in the German.',
     'words read with doubt are "[uncertain: ...]", as in the rest of the holding: 17 and 4, as in the German\n'
     '# (after the editor\'s answers on the spot sheet, intake/scripts/spot_answers_9.py).'),
]
DOUBT = [('[Kedl?]', 'a name; neither the editor nor the session can confirm it on the scan'),
         ('[seie?]', 'the editor\'s reading ("Possibly"); säh (would see) was the other reading'),
         ('[weiß?]', 'the editor cannot tell; their file had "aus"'),
         ('[vorgerübene?]', 'the letters as the editor read them; no word is found in them')]


def rep(s, pairs, what):
    for a, b in pairs:
        assert s.count(a) == 1, (what, a)
        s = s.replace(a, b)
    return s


def main():
    write = '--write' in sys.argv
    sys.stdout.reconfigure(encoding='utf-8')
    cp = os.path.join(UNIT, 'corpus.txt')
    corpus = rep(io.open(cp, encoding='utf-8', newline='').read(), TEXT, 'corpus')
    page = rep(io.open(PAGE_FILE, encoding='utf-8', newline='').read(), TEXT, 'page')
    ep = os.path.join(UNIT, 'intake', 'translation', 'doc9.yml')
    eng = rep(io.open(ep, encoding='utf-8', newline='').read(), ENGLISH, 'english')
    rdp = os.path.join(UNIT, 'reading.json')
    rraw = io.open(rdp, encoding='utf-8', newline='').read()
    reading = json.loads(rraw)
    lines = page.strip().split('\n')
    doubt = []
    for w, note in DOUBT:
        hit = [n for n, l in enumerate(lines, 1) if w in l]
        assert len(hit) == 1, w
        doubt.append({'line': hit[0], 'word': w, 'note': note})
    reading[KEY]['doubtful_words'] = doubt
    reading[KEY]['read_against'] += '; the editor\'s spot-sheet answers (intake/scripts/spot_answers_9.py)'
    print('letter 9: %d marks of doubt after the answers' % len(doubt))
    if write:
        io.open(cp, 'w', encoding='utf-8', newline='').write(corpus)
        io.open(PAGE_FILE, 'w', encoding='utf-8', newline='').write(page)
        io.open(ep, 'w', encoding='utf-8', newline='').write(eng)
        indent = 1 if rraw.startswith('{\n "') else (2 if rraw.startswith('{\n  "') else None)
        out = json.dumps(reading, ensure_ascii=False, indent=indent)
        if '\r\n' in rraw:
            out = out.replace('\n', '\r\n')
        io.open(rdp, 'w', encoding='utf-8', newline='').write(
            out + ('\r\n' if rraw.endswith('\r\n') else '\n' if rraw.endswith('\n') else ''))
        print('written')


if __name__ == '__main__':
    main()
