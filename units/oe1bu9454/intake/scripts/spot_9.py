# -*- coding: utf-8 -*-
"""The spot sheet "Letter 9" (2026-10-15).

    python units/oe1bu9454/intake/scripts/spot_9.py
    python pipeline/review/queries.py --unit oe1bu9454 --sheet letter_9.csv --port 4104

Where the text of letter 9 (letter_9.py) departs from the editor's transcription,
or keeps a reading of theirs that the scan does not confirm: eleven rows, each
with a picture of its line on the scan (0015_b). The text stands on the first
option of each row until the editor answers.
"""
import csv
import io
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT = os.path.dirname(os.path.dirname(HERE))
ROOT = os.path.dirname(os.path.dirname(UNIT))
SCAN = (r'J:\Documents\Archive\Genealogy\References\Hohenlohe-Zentralarchiv Neuenstein\Oe 1_Bü 9454\processed'
        r'\Oe 1_Bü 9454_0015_b.jpg')
L9 = 'Letter 9 (Vienna, about January 1815), '

# (key, a piece of the line, the word as it stands, options, note, the line's middle as a part of the page height)
ROWS = [
    ('v01', 'betreibe ich durch ihn', 'betreibe ich durch ihn', 'betreibe ich durch ihn|betreiben ich durch ihm',
     L9 + 'line 2: "the Koschentin business I am pursuing through him". Your file has "betreiben ich durch ihm"; '
     'on the scan I see no n after betreibe, and "ihn".', 0.143),
    ('v02', 'Kedl [...]', 'Kedl', 'Kedl|[Kedl?]',
     L9 + 'line 3, the first word, a name: "... has told him that he could have the whole lordship [Ko]schentin". '
     'Kept as you read it, Kedl; I cannot confirm it on the scan. Choose [Kedl?] to mark it as doubtful.', 0.168),
    ('v03', 'gerne [säh?] ich', '[säh?]', '[säh?]|säh|seie',
     L9 + 'line 4: "gerne ... ich dem Patron[...] / Gesicht" (I would gladly ... the Patron [in the] face). Your file '
     'has "seie"; I read säh (would see), with doubt.', 0.195),
    ('v04', '[St. K. F. H.?]', '[St. K. F. H.?]', '[St. K. F. H.?]|St. K. F. H.|St. K. F. A.',
     L9 + 'line 6: four initials before "was anzubringen ist" (what is to be brought forward). Your file has '
     '"St. K. F. A[?]."; the fourth looks to me like a Kurrent H: Staats Kanzler Fürst Hardenberg would fit. Not expanded.', 0.25),
    ('v05', 'weiß ich das wie und wo', 'weiß', 'weiß|aus',
     L9 + 'line 7: "... I know the how and where, so I am doing everything possible here". Your file has "aus ich '
     'das wie und wo"; I read weiß (know).', 0.283),
    ('v06', 'wenn nur erst die 112/m', 'wenn', 'wenn|wann',
     L9 + 'line 9: "everything is already agreed, if only the 112/m rt. are first granted". Your file has "wann"; '
     'I read wenn. Either means "if" here.', 0.34),
    ('v07', 'Eben so gl[...]', 'Eben so gl[...]', 'Eben so gl[...]|Eben so [...]',
     L9 + 'line 11, at the edge of the hole: "Likewise ...". Your file has "Eben so [...]"; I see the letters gl '
     'before the hole.', 0.405),
    ('v08', '[vorgerübene?]', '[vorgerübene?]', '[vorgerübene?]|vorgerübene|morgen reisen',
     L9 + 'line 12: "As soon as there is only a little breathing space, I shall ...". Your file has "vorgerübene", '
     'which I keep with a mark of doubt, as it is not a word I can find. I wondered about "morgen reisen" (travel '
     'tomorrow); please type what you see.', 0.433),
    ('v09', 'zum Borgen nehmen', 'Borgen', 'Borgen|Bergen',
     L9 + 'line 14: "in 6-7 days I must already again take my refuge in ...". Your file has "Bergen"; the vowel '
     'looks round to me, Borgen (borrowing), and letter 8 says "ich lebe blos von erborgten Gelde".', 0.493),
    ('v10', 'davon läuft der Bösewicht', 'davon läuft der Bösewicht', 'davon läuft der Bösewicht|daran läuft der Böse wirft',
     L9 + 'line 16: "... so that he does not run away; the scoundrel has angered me". Your file has "daran läuft '
     'der Böse wirft"; I read "davon läuft der Bösewicht".', 0.557),
    ('v11', 'hat mich schändlich geärgert', 'schändlich', 'schändlich|schrecklich',
     L9 + 'line 16: "has angered me ...". Your file has "schrecklich"; I read schändlich (shamefully). Line 17\'s '
     '"Streiche" I read without your mark of doubt.', 0.557),
]


def main():
    corpus = io.open(os.path.join(UNIT, 'corpus.txt'), encoding='utf-8').read().split('\n')
    i = corpus.index('[DOC 9]')
    j = corpus.index('[DOC 10]')
    rev = os.path.join(ROOT, 'review', 'oe1bu9454')
    img_dir = os.path.join(rev, 'spot_img')
    os.makedirs(img_dir, exist_ok=True)
    im = Image.open(SCAN).convert('L')
    W, H = im.size
    out = []
    for key, locate, word, options, note, y in ROWS:
        hits = [k + 1 for k in range(i, j) if locate in corpus[k]]
        assert len(hits) == 1, (key, hits)
        assert word in corpus[hits[0] - 1], key
        crop = im.crop((0, int((y - 0.035) * H), W, int((y + 0.035) * H)))
        crop = crop.resize((crop.width * 2, crop.height * 2))
        name = 'l9_%s.jpg' % key
        crop.save(os.path.join(img_dir, name), quality=88)
        out.append({'key': key, 'letter': '9', 'line': hits[0], 'word': word, 'options': options, 'note': note,
                    'image': name})
    with io.open(os.path.join(rev, 'letter_9.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['key', 'letter', 'line', 'word', 'options', 'note', 'image'])
        w.writeheader()
        w.writerows(out)
    print(len(out), 'rows')


if __name__ == '__main__':
    main()
