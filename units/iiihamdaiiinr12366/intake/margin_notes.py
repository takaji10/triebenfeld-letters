# -*- coding: utf-8 -*-
"""The pencil notes in the margins of the Warsaw report (document 2), 2026-10-04.

    python units/iiihamdaiiinr12366/intake/margin_notes.py            # check only
    python units/iiihamdaiiinr12366/intake/margin_notes.py --write    # once

A reader in the Prussian ministry went through the report with a pencil,
underlined passages and wrote objections beside them in German. The editor
supplied a first reading of the notes and the passage each stands beside
(2026-10-04); every note was then read again on an enlarged, contrast-raised
crop of the scan, and the readings below are the result. Where they differ
from the editor's, the difference is listed in notes.md. Four doubtful words
went to the editor on a spot sheet; "Kr." and "weil" are their answers.

Each note is one line at the end of its page, listed in office_notes.yml so
the site sets it apart as written by the receiving office. On a page that
ends in mid-sentence the notes stand before the last, unfinished paragraph. The French words in
square brackets before a note are the passage it stands beside, quoted from
the page; they are the edition's, not the reader's.

Run once: it also takes the note "1803 Oct." out of the running text, where
the transcription had set it in brackets, and adds the "ne" that the
transcription dropped on 0008 right (editor, 2026-10-04).
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

NOTES = [
 ('0003_a', [
  ('à la charge du Gouvernement Prussien',
   'als ob Preußen für Regierungs Acte im ehem. Südpreußen irgend jemand verantwortlich wäre!'),
 ]),
 ('0004_a1', [
  ('de la santé du dit Staroste et de celle de son épouse',
   'nun ist er auch krank gewesen! sie ist erst in Venedig krank geworden'),
 ]),
 ('0005_a2', [
  ('à la maladie dont il était atteint', '1803. Oct.'),
  ('privée de tous les secours d’une tutelle légale', 'unwahr'),
  ('Cependant le Gouvernement Prussien en disposa',
   'Warum hat sie denn seit 1807, wo sie wieder in den Besitz gesetzt worden, geschwiegen?'),
 ]),
 ('0006_a1', [
  ('dont ils avaient été privés',
   'Nicht einmal Napoleon hat ihnen einen Anspruch wegen des in der Zwischenzeit geschehenen, zugestanden.'),
  ('Manieczki', '+) Kr. Kosten Rbz. Posen'),
 ]),
 ('0006_a2', [
  ('replacés dans le même état',
   'wo steht das geschrieben? Nicht einmal im Napoleon. Decrete.'),
  ('contre toute justice', 'unwahr'),
 ]),
 ('0007_a1', [
  ('le prouvèrent les événemens politiques',
   'aber so lang er es besessen, besaß er es rechtmäßig u. mit vollem Eigenthumsrecht'),
  ('injustement confisqués', 'wo steht das geschrieben?'),
 ]),
 ('0007_a2', [
  ('n’auraient recouvré qu’un titre d’héritage onéreux',
   'sie bekamen zurück, was da war.'),
  ('le Prince Hohenlohe avait obéré les biens', 'weil hier Schulden da sind.'),
 ]),
]

EDITS = [
 ('dont il était atteint (1803 Oct.), et qui', 'dont il était atteint, et qui'),
 ('(et qui pouvaient être autres', '(et qui ne pouvaient être autres'),
 # read on the scan while placing the note beside it: "de la santé"
 ('Le mauvais état de sa santé', 'Le mauvais état de la santé'),
]


def main():
    write = '--write' in sys.argv
    cp = os.path.join(UNIT_DIR, 'corpus.txt')
    L = io.open(cp, encoding='utf-8').read().split('\n')
    text = '\n'.join(L)
    for old, new in EDITS:
        if text.count(old) != 1:
            sys.exit(f'{old!r}: found {text.count(old)} times')
        text = text.replace(old, new)
    L = text.split('\n')
    blocks = []
    for pid, notes in NOTES:
        i = L.index(f'[PAGE {pid}]')
        j = next(k for k in range(i + 1, len(L)) if L[k].startswith('[PAGE ') or L[k].startswith('[DOC '))
        page = '\n'.join(L[i:j])
        lines = []
        for lemma, note in notes:
            if lemma not in page:
                sys.exit(f'{pid}: the passage {lemma!r} is not on the page')
            lines.append(f'[{lemma}:] {note}')
        # A page that ends in the middle of a sentence takes its notes before
        # that last, unfinished paragraph, so they do not part it from its
        # continuation on the next page.
        if not L[j - 1].rstrip().endswith(('.', '!', '?', ':')):
            j -= 1
        L[j:j] = lines
        blocks.append((pid, lines))
        print(pid)
        for l in lines:
            print('   ', l)
    if not write:
        return
    with io.open(cp, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(L))
    for pid, lines in blocks:
        tp = os.path.join(UNIT_DIR, 'transcriptions', pid + '.txt')
        t = io.open(tp, encoding='utf-8').read()
        for old, new in EDITS:
            t = t.replace(old, new)
        with io.open(tp, 'w', encoding='utf-8', newline='\n') as f:
            f.write(t.rstrip('\n') + '\n' + '\n'.join(lines) + '\n')
    tp = os.path.join(UNIT_DIR, 'transcriptions', '0008_a2.txt')
    t = io.open(tp, encoding='utf-8').read()
    for old, new in EDITS:
        t = t.replace(old, new)
    io.open(tp, 'w', encoding='utf-8', newline='\n').write(t)

    def q(s):
        return "'" + s.replace("'", "''") + "'"
    with io.open(os.path.join(UNIT_DIR, 'office_notes.yml'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(
            "# Text the receiving office wrote on someone else's paper. Here: the pencil\n"
            "# notes a reader in the Prussian ministry wrote in German in the margins of\n"
            "# the Warsaw report (document 2), beside passages he underlined. The lines\n"
            "# are ordinary text in corpus.txt; this file only says which they are, so\n"
            "# the site can set them apart. Each block stands at the end of its page.\n"
            "# The French in square brackets before a note is the passage it stands\n"
            "# beside (intake/margin_notes.py).\n"
            "#   first: the block's first line exactly as it stands in corpus.txt\n"
            "#   lines: how many lines the block has\n"
            "# A first line that is edited must be edited here too; build_db.py stops if a\n"
            "# block cannot be found.\n"
            "blocks:\n")
        for pid, lines in blocks:
            f.write(f"  - letter: '2'\n    page: '{pid}'\n    first: {q(lines[0])}\n    lines: {len(lines)}\n")
    print('written')


if __name__ == '__main__':
    main()
