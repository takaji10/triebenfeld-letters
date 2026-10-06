# -*- coding: utf-8 -*-
"""The light correction pass on APP 53/17/0/-/Konin Gr.145, 2026-10-06.

    python units/app53170koningr145/intake/corrections.py            # check only
    python units/app53170koningr145/intake/corrections.py --write    # once

Run after build_pages.py --write, once. A record: do not run it again, and do
not run build_pages.py --write after it (that would write the uncorrected text
back).

What "light" means here. The editor's transcription had been worked over
before it came into the edition, and they asked for a light touch. It is in
modern Polish spelling, which is kept. Four of its 121 written pages were read
word for word against the scans (leaves 656, 673, 688, 707 verso), and the
signatures on leaf 715. What those pages showed is corrected here (ROWS).
Nothing else was compared with the scans, so slips of the same kinds remain on
the other pages: about one small misreading in a hundred words, more in the
abbreviated Latin, and now and then a dropped phrase (one in the four pages,
on leaf 673).

ACCENTS is a different kind of change, made through the whole text without
the scans: a word that lacks an accent, or has a wrong one, and is no Polish
word as it stands, where the transcription itself writes the right form many
times ("wyzej" 4 times beside "wyżej" 141 times). Word pairs that are both
Polish words (stara / starą, kaliska / kaliską, tędy / tedy) are left alone.

ROWS: (page, text as transcribed, text as on the scan, why). Each old text
must stand exactly once on its page. ADD: lines put after a given line of a
page. Applied to transcriptions/ and corpus.txt and logged in
transcription_decisions.csv.
"""
import csv
import hashlib
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
SLUG = 'app53170koningr145'

ROWS = [
    # -- the title page (leaf 654)
    ('0654_a2', 'cum Haereditatibus Trąpczyn', 'inter Haereditates Trąpczyn',
     'the scan has "inr Haredit" with marks of abbreviation: inter Haereditates, between the estates'),
    # -- leaf 656: the record of the Warsaw court, in abbreviated Latin, and the act of parliament
    ('0656_a2', 'jurysdykcja teraźniejszą', 'jurysdykcją teraźniejszą', 'the scan has "Jurysdykcyą"'),
    ('0656_a2', 'pridie Sacratissimi', 'pridie festi Sacratissimi', '"festi" is on the scan and was left out'),
    ('0656_a2', 'Mensio Junij', 'Mensis Junij', 'the scan has "Mensis"'),
    ('0656_a2', 'Millesimo Septingentesimi Septuagesimo Quarto', 'Millesimo Septingentesimo Septuagesimo Quarto',
     'the scan has "Septingentesimo"'),
    ('0656_a2', 'Florianus Janosza Drewnowski', 'Florianus Junosza Drewnowski',
     'the scan has "Junosza", the arms he bore'),
    ('0656_a2', 'Comitiorum Ordinariorum', 'Comitiorum extra Ordinariorum',
     '"extra" is on the scan and was left out: he was secretary of the extraordinary parliament'),
    ('0656_a2', 'czyli Nowa Wsią nazwaną', 'czyli Nową Wsią nazwaną', 'the scan has "nową Wsią"'),
    ('0656_a2', 'i innym w Województwie', 'i innymi w Województwie', 'the scan has "y innemi"'),
    # -- leaf 673
    ('0673_a2', 'tudzież nie prawność wizji', 'tudzież nieprawność wizji', 'one word on the scan'),
    ('0673_a2', 'drugiego ze znanej dokumentom', 'drugiego zeznanej, dokumentom',
     'the scan has "zeznaney," one word with a comma after it: the inspection of 1592 "as recorded"'),
    ('0673_a2', 'jako tez et vel maxime', 'jako też et vel maxime', 'the scan has "też"'),
    ('0673_a2', 'z szedłszy z pomieniony', 'zszedłszy z pomieniony', 'one word on the scan'),
    ('0673_a2', 'okrągłość i koroną mającego', 'okrągłość i koronę mającego', 'the scan has "Koronę"'),
    ('0673_a2', 'takich ze znacznych', 'takichże znacznych', 'the scan has "takich że", the particle'),
    ('0673_a2', 'ku mościskom się na kilka staj ciągnących item,',
     'ku mościskom się na kilka staj ciągnących las cały Lusnie zajmujących i zabierających item,',
     'six words left out, between two words of the same ending: the scan has "ciągnących las cały Lusnie '
     'zaymuiących y zabieraiących item"; given in the modern spelling of the rest'),
    # -- leaf 688
    ('0688_a2', 'ta droga aktualnia po między', 'ta droga aktualnie pomiędzy', 'the scan has "aktualnie pomiędzy"'),
    ('0688_a2', 'Wrąbczyna i gruntu w ich,', 'Wrąbczyna i gruntu ich,', 'no "w" on the scan'),
    ('0688_a2', 'i ścianę to po tej stronie', 'i ścianę tu po tej stronie', 'the scan has "tu"'),
    ('0688_a2', 'starą Pydrzka za Łukomiem', 'starą Pyzdrzką za Łukomiem', 'the scan has "Pyzdrzką"'),
    ('0688_a2', 'między drogami tymi omiema', 'między drogami tymi obiema', 'the scan has "obiema", both'),
    ('0688_a2', 'fundo et paniete suo', 'fundo et pariete suo', 'the scan has "pariete", wall'),
    ('0688_a2', 'to w tym miejscu okazują się', 'tu w tym miejscu okazują się', 'the scan has "tu"'),
]

ADD = [
    ('0654_a2', '1776', 'In Castro Brestensi Cujaviae',
     'the third line of the title page, "In Cro Brest Cujae" with marks of abbreviation, not transcribed'),
]

ACCENTS = {
    'wyzej': 'wyżej', 'takze': 'także', 'tegoz': 'tegoż', 'tymze': 'tymże', 'tudziez': 'tudzież',
    'tychze': 'tychże', 'tylez': 'tyleż', 'az': 'aż', 'iz': 'iż', 'juz': 'już', 'azeby': 'ażeby',
    'bydz': 'bydź', 'nizej': 'niżej', 'zadnej': 'żadnej', 'naroznik': 'narożnik', 'naroznych': 'narożnych',
    'lezący': 'leżący', 'lezące': 'leżące', 'kopcow': 'kopców', 'naciosow': 'naciosów', 'wschod': 'wschód',
    'częsci': 'części', 'trzydziesci': 'trzydzieści', 'czterdziesci': 'czterdzieści',
    'przytomnosci': 'przytomności', 'swiadkami': 'świadkami', 'najswiętszej': 'najświętszej',
    'sprawiedliwosci': 'sprawiedliwości', 'jasnie': 'jaśnie', 'koncem': 'końcem', 'najprzod': 'najprzód',
    'procz': 'prócz', 'mowi': 'mówi', 'osmiu': 'ośmiu', 'gorami': 'górami', 'ługow': 'ługów',
    'wyrazono': 'wyrażono', 'sciany': 'ściany', 'sciane': 'ścianę', 'ściane': 'ścianę', 'strone': 'stronę',
    'osinskiej': 'osińskiej', 'obłatowany': 'oblatowany', 'łasów': 'lasów', 'wśi': 'wsi', 'teraż': 'teraz',
    'nię': 'nie', 'poł': 'pół', 'poniewaz': 'ponieważ', 'tychze': 'tychże', 'toz': 'toż', 'isć': 'iść',
}
LETTER = 'A-Za-zÀ-ÿĀ-ž'


def page_ids():
    ids = []
    for n in range(654, 716):
        for half in ('a1', 'a2'):
            pid = '%04d_%s' % (n, half)
            if pid not in ('0654_a1', '0655_a1'):
                ids.append(pid)
    return ids


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    write = '--write' in sys.argv
    tdir = os.path.join(UNIT_DIR, 'transcriptions')
    ids = page_ids()
    text = {pid: io.open(os.path.join(tdir, pid + '.txt'), encoding='utf-8').read().rstrip('\n').split('\n') for pid in ids}
    log, bad = [], []
    pad = SLUG + '-001'

    def pno(pid):
        return ids.index(pid) + 1

    for pid, old, new, why in ROWS:
        hits = [i for i, l in enumerate(text[pid]) if old in l]
        n = sum(text[pid][i].count(old) for i in hits)
        if n != 1:
            bad.append('%s %r: found %d time(s)' % (pid, old, n))
            continue
        i = hits[0]
        text[pid][i] = text[pid][i].replace(old, new)
        key = hashlib.md5(('%s|%s|%s' % (pid, old, new)).encode()).hexdigest()[:8]
        log.append([key, pad, pno(pid), old, new, '%s: %s -> %s' % (pid, old, new), 'read on the scan: ' + why])
    for pid, after, line, why in ADD:
        hits = [i for i, l in enumerate(text[pid]) if l == after]
        if len(hits) != 1:
            bad.append('%s %r: found %d time(s)' % (pid, after, len(hits)))
            continue
        text[pid].insert(hits[0] + 1, line)
        key = hashlib.md5(('%s|add|%s' % (pid, line)).encode()).hexdigest()[:8]
        log.append([key, pad, pno(pid), '', line, '%s: line added: %s' % (pid, line), 'read on the scan: ' + why])
    if bad:
        sys.exit('NOT WRITTEN\n' + '\n'.join(bad))
    n_acc = 0
    for old, new in ACCENTS.items():
        rx = re.compile(r'(?<![%s])(%s)(?![%s])' % (LETTER, re.escape(old), LETTER), re.IGNORECASE)
        for pid in ids:
            for i, l in enumerate(text[pid]):
                def fix(m):
                    w = m.group(1)
                    return new.capitalize() if w[0].isupper() else new
                l2, k = rx.subn(fix, l)
                if k:
                    text[pid][i] = l2
                    n_acc += k
                    key = hashlib.md5(('%s|%d|%s|%s' % (pid, i, old, new)).encode()).hexdigest()[:8]
                    log.append([key, pad, pno(pid), old, new, '%s: %s -> %s (%d)' % (pid, old, new, k),
                                'accent: no Polish word as written; the transcription itself writes "%s" elsewhere. '
                                'Not compared with the scan' % new])
    print(len(ROWS), 'readings corrected on the scans,', len(ADD), 'line added,', n_acc, 'accents put right on',
          len({r[2] for r in log if r[6].startswith('accent')}), 'pages')
    if not write:
        return
    for pid in ids:
        io.open(os.path.join(tdir, pid + '.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(text[pid]) + '\n')
    out = ['[DOC 1]']
    for pid in ids:
        out.append('[PAGE %s]' % pid)
        out.extend(text[pid])
    io.open(os.path.join(UNIT_DIR, 'corpus.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
    p = os.path.join(UNIT_DIR, 'transcription_decisions.csv')
    new_file = not os.path.isfile(p) or os.path.getsize(p) == 0
    with io.open(p, 'a', encoding='utf-8-sig' if new_file else 'utf-8', newline='') as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(['key', 'pad', 'page', 'transcribed', 'proposed', 'decision', 'why'])
        w.writerows(log)
    print('written and logged:', len(log), 'rows')


if __name__ == '__main__':
    main()
