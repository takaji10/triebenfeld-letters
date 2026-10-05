# -*- coding: utf-8 -*-
"""Mohrenheim's note (document 3, scan 0004) read a second time, 2026-10-05.

    python units/iiihamdaiiinr12367/intake/second_reading.py            # check only
    python units/iiihamdaiiinr12367/intake/second_reading.py --write    # once

The editor asked for two things the first pass (corrections.py) had left: the
end of the note's last sentence, and the line written sideways in its left
margin, to be put into the transcription and the translation. Both were read
on crops of the scan enlarged three to six times.

The sentence is plain once enlarged: "qui glace" (g with its descender, a
tall l), "mes passions" (the i dotted), "champêtres" (c, a tall h, p with its
descender, a crossed t before "res"). The weather chills his taste for the
country.

The margin line is smaller and the scan is coarse there (the whole page is
1,787 pixels wide). "Pourriez Vous m'accorder pour 2 j." is plain. The two
words after "le" are given as doubtful: seven letters beginning "Cou", and a
word with a tall first letter, two short letters, a tall one and "es". "le
Courier de Londres", a London newspaper, fits both and fits a request to
borrow something for two days. Nothing else proves it.

The same day the editor looked at the line and saw "rev... de P...": the two
guesses were wrong. The line now stands in corpus.txt as "le [Rev…?] de
[P…?] ?" (transcription_decisions.csv, key editor-0004). LINE below is what
this script wrote, kept as the record; do not run it again.

The line is added as the last line of the page and named in sideways.yml, so
the site sets it apart as written sideways. Logged in
transcription_decisions.csv.
"""
import csv
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
SLUG = 'iiihamdaiiinr12367'
PAGE_FILE = '0004_a.txt'

OLD = 'qui font parfois mon pain de négrêtes [?].'
NEW = 'qui glace parfois mes passions champêtres.'
WHY = ('read on the scan, enlarged: "qui glace" (g with a descender, tall l); "mes passions" (dotted i); '
       '"champêtres" (c, tall h, p with a descender, crossed t before "res"): dreadful weather '
       '"which at times chills my rustic passions"')
AFTER = 'Mardi.'
LINE = "Pourriez Vous m'accorder pour 2 j. le [Courier?] de [Londres?] ?"
WHY_LINE = ('read on the scan, enlarged: the line written sideways in the left margin, not transcribed before. '
            '"Pourriez Vous m\'accorder pour 2 j." is plain; the two words after "le" are doubtful '
            '(seven letters beginning "Cou"; a tall letter, two short, a tall one, "es")')

SIDEWAYS = """# Text written sideways on the page. Here: one line in the left margin of
# Baron Mohrenheim's note (scan 0004), read on 2026-10-05 at the editor's
# request (intake/second_reading.py). The line is ordinary text in corpus.txt;
# this file only says that it was written sideways, so the site can set it
# apart. It stands at the end of its page.
#   first: the block's first line exactly as it stands in corpus.txt
#   lines: how many lines the block has
# A first line that is edited must be edited here too; build_db.py stops if a
# block cannot be found.
blocks:
  - letter: '3'
    page: '0004_a'
    first: "%s"
    lines: 1
""" % LINE


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    write = '--write' in sys.argv
    cp = os.path.join(UNIT_DIR, 'corpus.txt')
    tp = os.path.join(UNIT_DIR, 'transcriptions', PAGE_FILE)
    out = {}
    for p in (cp, tp):
        s = io.open(p, encoding='utf-8', newline='').read()
        if s.count(OLD) != 1 or LINE in s:
            sys.exit(f'{p}: the sentence stands {s.count(OLD)} time(s), the margin line {s.count(LINE)}')
        s = s.replace(OLD, NEW)
        L = s.split('\n')
        if p == cp:
            a = L.index('[DOC 3]')
            i = L.index(AFTER, a)
            assert i < L.index('[DOC 4]'), 'Mardi. not in document 3'
            line_no = [k for k, x in enumerate(L) if NEW in x][0] + 1
        else:
            i = max(k for k, x in enumerate(L) if x.strip() == AFTER)
        L.insert(i + 1, LINE)
        out[p] = '\n'.join(L)
    print(f'corpus line {line_no}: {OLD} -> {NEW}')
    print(f'line added after "{AFTER}": {LINE}')
    if not write:
        return
    for p, s in out.items():
        io.open(p, 'w', encoding='utf-8', newline='').write(s)
    io.open(os.path.join(UNIT_DIR, 'sideways.yml'), 'w', encoding='utf-8', newline='\n').write(SIDEWAYS)
    with io.open(os.path.join(UNIT_DIR, 'transcription_decisions.csv'), 'a', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        k = hashlib.md5(f'3|{line_no}|{OLD}|{NEW}'.encode()).hexdigest()[:8]
        w.writerow([k, f'{SLUG}-003', 1, OLD, NEW, f'@{line_no} {OLD} -> {NEW}', WHY])
        k = hashlib.md5(f'3|add|{LINE}'.encode()).hexdigest()[:8]
        w.writerow([k, f'{SLUG}-003', 1, '', LINE, f'line added: {LINE}', WHY_LINE])
    print('written and logged; sideways.yml written')


if __name__ == '__main__':
    main()
