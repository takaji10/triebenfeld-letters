# -*- coding: utf-8 -*-
"""The correction pass on AGAD 1/174/0/1/6 (NEW_UNIT.md 3a), 2026-10-04.

    python units/agad1174016/intake/corrections.py            # check only
    python units/agad1174016/intake/corrections.py --write    # once

The register is in a clear copyist's hand, and each page was read against its
scan. The transcription of page 331 spells out the abbreviations and writes j
where the page has y or i; the entry is put back as the page has it, because
the edition gives the scribe's own spelling. The abbreviations are explained
in units/agad11740273/intake/corrections.py. What is left is in unresolved.md.

ROWS: (text as transcribed, text as on the scan, why); each `old` must stand
exactly once in its document. A row whose first item is LINE replaces the
whole line that begins with the second item. ADD: (the line it follows, the
new line, why). Applied to corpus.txt and to transcriptions/, and logged in
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
SLUG = 'agad1174016'
LINE = 'LINE'
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROWS = {
 # -- the order of 12 July 1807 on Wybicki's estates (0028_a2, 0029_a1)
 '1': [
  ('Kommissja Rządząca', 'Kommissya Rządząca', "the scribe's spelling"),
  ('r. b. W Finckenstein', 'r. b. w Finckenstein', 'small w'),
  ('I któremi', 'i któremi', 'small i: the sentence runs on from page 47'),
  ('niewłocznie', 'niezwłocznie', '"without delay"; a typing slip'),
 ],
 # -- the resolution of 21 July 1807, with the heading of its section (0180_a2)
 '2': [
  ('Kommissyi Rządzącej pod bytność Jej w Dreznie wydanych, lub do Directorium Generalnego jako i do',
   'Kommissyi Rządzącey pod bytność Jey w Dreznie wydanych, tak do Directorium Generalnego iako i do',
   '"tak do ... iako i do": issued both to the general directorate and to the directors singly'),
  ('Michaliny Dambskiej, Generała Niemoiewskiego i Wichrowskiego', 'Michaliny Dąmbskiey, G[enera]ła Niemoiewskiego i Wichrowskiego', 'the scribe wrote "Dąbskiey" and set an m above it; "Gła" abbreviated'),
  ('pod Wyrok Najjaśniejszego Cesarza na rzecz Jaśnie Wielmożnego Wybickiego wydany:', 'pod Wyrok N° Cesarza na rzecz JW° Wybickiego wydany:', 'abbreviated on the scan'),
  ('Komissja Rządząca', 'Kommissya Rządząca', "the scribe's spelling"),
  (LINE, 'Gdy Interess Jaśnie Pani',
   'Gdy Interess JPani Michaliny z Prusińskich Dambskiey, żądaiącey zwrotu Dóbr swoich Dziedzicznych za przeszłego Rządu skonfiskowanych i komu innemu oddanych do Nas przez N° Cesarza został odesłany; biorąc przykład z wymierzoney przez JCK. Mość sprawiedliwości JW. Wybickiemu Kolledze Naszemu przez Dekret dnia 5° Czerwca w Finkenstein wydany i chcąc w tak słusznem żądaniu ścisłą dla każdego zachować sprawiedliwość, Wyrok N° Cesarza JW° Wybickiemu służący, tak co do przypadku JP. Michaliny Dambskiey, iako JP. Generała Niemojewskiego i JP. Wichrowskiego rozciągamy, mieć chcąc ażeby tych wyżey wyrażonych Osob Dobra dziedziczne przez zeszły Rząd Pruski skonfiskowane do prawdziwych Włascicielów wróciły. — Działo się w Dreznie na Sessyi dnia 21. Lipca 1807.',
   'the entry as the page has it: the abbreviations JPani, N°, JCK. Mość, JW., JP. not spelled out, y and i not changed to j; no "i" before "biorąc" or before "mieć chcąc"'),
 ],
}

ADD = {}


def main():
    write = '--write' in sys.argv
    cp = os.path.join(UNIT_DIR, 'corpus.txt')
    L = io.open(cp, encoding='utf-8').read().split('\n')

    def index():
        doc = page = None
        pno, where = 0, {}
        for i, l in enumerate(L):
            m = re.match(r'\[DOC (\S+)\]', l)
            if m:
                doc, pno = m.group(1), 0
                continue
            m = re.match(r'\[PAGE (\S+)\]', l)
            if m:
                page, pno = m.group(1), pno + 1
                continue
            where[i] = (doc, page, pno)
        return where

    where = index()
    log, bad, edits = [], [], []
    for d, rows in ROWS.items():
        for row in rows:
            if row[0] == LINE:
                _, head, new, why = row
                hits = [i for i in where if where[i][0] == d and L[i].startswith(head)]
                if len(hits) != 1:
                    bad.append(f'[{d}] line "{head}": found {len(hits)} time(s)')
                    continue
                i, old = hits[0], L[hits[0]]
                L[i] = new
            else:
                old, new, why = row
                hits = [i for i in where if where[i][0] == d and old in L[i]]
                n = sum(L[i].count(old) for i in hits)
                if n != 1:
                    bad.append(f'[{d}] {old!r}: found {n} time(s)')
                    continue
                i = hits[0]
                L[i] = L[i].replace(old, new)
            key = hashlib.md5(f'{d}|{i + 1}|{old}|{new}'.encode()).hexdigest()[:8]
            log.append((key, f'{SLUG}-{int(d):03d}', where[i][2], old, new,
                        f'@{i + 1} {old} -> {new}', 'read on the scan: ' + why))
            edits.append((where[i][1], old, new))
    adds = []
    for d, rows in ADD.items():
        for head, line, why in rows:
            hits = [i for i in where if where[i][0] == d and L[i].startswith(head)]
            if len(hits) != 1:
                bad.append(f'[{d}] add after "{head}": found {len(hits)} time(s)')
                continue
            i = hits[0]
            key = hashlib.md5(f'{d}|add|{line}|{head}'.encode()).hexdigest()[:8]
            log.append((key, f'{SLUG}-{int(d):03d}', where[i][2], '', line,
                        f'line added: {line}', 'read on the scan: ' + why))
            adds.append((i, where[i][1], L[i], line))
    if bad:
        sys.exit('NOT WRITTEN\n' + '\n'.join(bad))
    for i, _, _, line in sorted(adds, reverse=True):
        L.insert(i + 1, line)
    print(len(log), 'corrections')
    if not write:
        return
    with io.open(cp, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(L))
    tdir = os.path.join(UNIT_DIR, 'transcriptions')
    for pid, old, new in edits:
        tp = os.path.join(tdir, pid + '.txt')
        t = io.open(tp, encoding='utf-8').read()
        if t.count(old) != 1:
            sys.exit(f'{pid}.txt: {old!r} found {t.count(old)} time(s)')
        io.open(tp, 'w', encoding='utf-8', newline='\n').write(t.replace(old, new))
    for _, pid, after, line in adds:
        tp = os.path.join(tdir, pid + '.txt')
        t = io.open(tp, encoding='utf-8').read()
        if t.count(after + '\n') != 1:
            sys.exit(f'{pid}.txt: the line to add after was not found once')
        io.open(tp, 'w', encoding='utf-8', newline='\n').write(
            t.replace(after + '\n', after + '\n' + line + '\n'))
    dp = os.path.join(UNIT_DIR, 'transcription_decisions.csv')
    new_file = not os.path.isfile(dp) or os.path.getsize(dp) == 0
    with io.open(dp, 'a', encoding='utf-8-sig' if new_file else 'utf-8', newline='') as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(['key', 'pad', 'page', 'transcribed', 'proposed', 'decision', 'why'])
        w.writerows(log)
    print('written and logged')


if __name__ == '__main__':
    main()
