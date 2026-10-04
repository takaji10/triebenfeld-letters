# -*- coding: utf-8 -*-
"""The spot sheet of words the scans did not settle (2026-10-04).

    python units/iiihamdaiiinr12366/intake/open_queries.py
    python pipeline/review/queries.py --unit iiihamdaiiinr12366

Writes review/<slug>/open_queries.csv (and a copy beside this script, since
review/ is not in the repository). Rows: (document, text that finds the line,
the word as it stands, the readings offered, the note the editor sees).
"""
import csv
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(UNIT_DIR))
sys.path.insert(0, ROOT)
import unitlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
SLUG = 'iiihamdaiiinr12366'

ROWS = [
 # the pencil notes in the margins of document 2
 ('2', '[Manieczki:]', 'L[?].', 'L.|Kr.|C.',
  'Scan 0006, left page, pencil note in the left margin beside "Manieczki", marked +). The letter before "Kosten". It looks like L to me; Kr. (for Kreis, district) is what one would expect.'),
 ('2', 'hier Schulden da sind', 'weil[?]', 'weil|wie|nur',
  'Scan 0007, right page, pencil note in the left margin near the foot, beside "le Prince Hohenlohe avait obéré". The first word, three or four faint letters. You read "wie"; "weil" (because) would answer the report\'s "why then".'),
 ('2', 'Warum hat sie', 'denn', 'denn|dann',
  'Scan 0005, right page, pencil note in the left margin: "Warum hat sie ... seit 1807". The first word of its second line. You read "dann".'),
 ('2', 'wo steht das geschrieben? Nicht einmal', 'Decrete.', 'Decrete.|Decrete!|Decret.',
  'Scan 0006, right page, pencil note in the left margin beside "replacés dans le même état". Its last line, very faint. You read "derwegen[?]".'),
 # the Warsaw report itself
 ('2', 'Il en agit également', 'Larna', 'Larna|Lama',
  'Scan 0008, left page, third line: "la terre appellée ...", the estate given to General Zastrow.'),
 # the Polish judgment
 ('6', 'Zapolski', 'Josef', 'Josef|Jozef',
  'Scan 0017, the list of judges at the top left, third name.'),
 ('6', 'Zapolski', 'Assistant', 'Assistant|Assessor',
  'Scan 0017, the same line: the word between "Zapolski" and "Sędziego".'),
 ('6', 'stawaiącemi przez Jozefa', 'Rozdayczer[?]', 'Rozdayczer|Rozdaycer',
  'Scan 0018, left page, second line: the name of the plaintiffs\' advocate. Your doubt mark; pick the first button to drop it.'),
 ('6', 'nie iest usprawiedliwione', 'Lublinca,', 'Lublinca,|Lublińca,',
  'Scan 0019, right page, second and third lines: "Dobr Lublin-ca", the estate whose court issued a death certificate. Is there an accent on the n?'),
 ('6', 'Ze sam Nayiaśnieyszy', 'ustalić', 'ustalić|uznać|ustaki',
  'Scan 0022, right page, third line from the foot, after "Pruski". I changed your "ustaki" to "ustalić" (to establish); "uznać" (to recognise) is the other candidate.'),
 ('6', 'Za zgodnosc', 'nieobiętym', 'nieobiętym|nieobciętym',
  'Scan 0025, second line: the word before "stęplu".'),
 ('6', 'za Pisarza', 'Karuecki', 'Karuecki|Karnecki|Kamecki',
  'Scan 0025, the signature under the certification: the surname.'),
 ('6', 'za Pisarza', 'Likrę[?]', 'Likrę[?]|Sekr.|Sekrę',
  'Scan 0025, the same signature: the word between the surname and "za Pisarza". Your doubt mark. It may be an abbreviation of Sekretarz.'),
]


def main():
    unit = unitlib.one_unit(SLUG)
    L = io.open(os.path.join(UNIT_DIR, 'corpus.txt'), encoding='utf-8').read().split('\n')
    doc, where = None, {}
    for i, l in enumerate(L, 1):
        if l.startswith('[DOC '):
            doc = l[5:-1]
        where[i] = doc
    out = []
    for k, (d, key, word, opts, note) in enumerate(ROWS, 1):
        hits = [i for i, l in enumerate(L, 1) if where[i] == d and key in l]
        if len(hits) != 1:
            sys.exit(f'{key!r}: on {len(hits)} lines')
        if L[hits[0] - 1].count(word) != 1:
            sys.exit(f'{word!r}: {L[hits[0] - 1].count(word)} times on line {hits[0]}')
        out.append({'key': f'q{k:02d}', 'letter': d, 'line': hits[0], 'word': word,
                    'options': opts, 'note': note})
    for d in (unitlib.review_dir(unit.slug), HERE):
        os.makedirs(d, exist_ok=True)
        with io.open(os.path.join(d, 'open_queries.csv'), 'w', encoding='utf-8-sig', newline='') as f:
            w = csv.DictWriter(f, fieldnames=list(out[0]))
            w.writeheader()
            w.writerows(out)
    print(len(out), 'questions')


if __name__ == '__main__':
    main()
