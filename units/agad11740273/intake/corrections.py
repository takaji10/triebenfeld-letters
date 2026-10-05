# -*- coding: utf-8 -*-
"""The correction pass on AGAD 1/174/0/2/73 (NEW_UNIT.md 3a), 2026-10-04.

    python units/agad11740273/intake/corrections.py            # check only
    python units/agad11740273/intake/corrections.py --write    # once

Every page was read against its scan on enlarged crops. A row is here only
where the scan is plain. The transcription spells out abbreviations and writes
j where the pages have y or i ("Kommissji Rządzącej" for "Kommissyi
Rządzącey", "jaki" for "iaki"); those are put back as the pages have them,
because the edition gives the writers' own spelling. What the scan does not
settle is in unresolved.md.

The abbreviations that now stand as written: "JW." is Jaśnie Wielmożny (a
form of address for a senator or high official), "JP." and "JPani" Jaśnie Pan
and Jaśnie Pani, "N° Cesarza" Nayiaśnieyszego Cesarza (the Most Serene
Emperor, Napoleon), "Jego C°K. Mość" Jego Cesarsko-Królewska Mość (His
Imperial and Royal Majesty), "W. X[ię]cia Dyrektora Woyny" the Prince
Director of War, "a. c." anni currentis (of this year).

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
SLUG = 'agad11740273'
LINE = 'LINE'
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROWS = {
 # -- the commission's draft resolution, 21 July 1807 (0005_a2)
 '1': [
  ('Interess JW. Pani', 'Interess JPani', '"JPani", one word; the register copy has the same'),
  ('do Nas przez W° Cesarza', 'do Nas przez N° Cesarza', 'N°, for Nayiaśnieyszego: written in above the line; clear in the register copy (1/174/0/1/6, page 331)'),
  ('Wyrok W° Cesarza dla JW.', 'Wyrok N° Cesarza JW.', 'N° as above; "dla" is struck out on the scan'),
  ('Jego C°K.mość', 'Jego C°K. Mość', 'written in the left margin, capital M'),
  ('aźeby', 'ażeby', 'a typing slip'),
  ('21. [Lipca] 1807.', '21. Lipca 1807.', '"Lipca" is written plainly above a struck-out "Czerwca"; no doubt remains'),
 ],
 # -- her Polish petition, 20 July 1807 (0006_a2)
 '2': [
  ('do Kommissji Rządzącej w celu', 'do Kommissyi Rządzącey w celu', 'the writer\'s spelling'),
  ('nie mając jeszcze zadnej dotąd', 'nie mając ieszcze żadney dotąd', 'the writer\'s spelling; ż has its mark'),
  ('dobr a swoje, rownie jak moje', 'dobra swoje, rownie iak moje', 'one word: "his estates, confiscated like mine"'),
  ('przez Najiaśniejszego Cesarza', 'przez Nayiaśnieyszego Cesarza', 'the writer\'s spelling'),
  ('prosić Kommissji Rządzącej aby raczyła w stawić', 'prosić Kommissyi Rządzącey aby raczyła wstawić', '"wstawić się za mną" (to intercede for me), one word'),
  ('sposobnośc', 'sposobność', 'a typing slip'),
  ('jaki od Najjasniejszego Cesarza', 'iaki od Nayiaśnieyszego Cesarza', 'the writer\'s spelling'),
  ('Presentatum 21. Julii', 'Praesent. d. 21. July', 'the received note as written, numbered 1 in the margin'),
 ],
 # -- her French petition to the Emperor, 21 July 1807 (0007_a2, 0008_a1)
 '3': [
  ('Monsieur le Comte de Wybicki', 'Mr. le Comte de Wybicki', 'abbreviated on the scan'),
  ('Presentatum 21. Lipca 1807 na sessji Extraordynaryiney w Dreznie przez Wielmożnego Książęcego Dyrektor Wojny z rozkazem Najjasniejszego Cesarza i Króla',
   'Presentatum 21. Lipca 1807. na Sessyi Extraordynaryiney w Dreznie przez W. X[ię]cia Dyrektora Woyny z rozkazu Nayiaśnieyszego Cesarza y Króla',
   '"presented at the extraordinary session at Dresden by the Prince Director of War, by order of the Most Serene Emperor and King": "W. Xcia Dyrektora", genitive, and "z rozkazu"'),
  (LINE, 'Jaśnie Wielmożnemu Jegomości',
   'Jaśnie Wielmożnemu JMci Panu Małachowskiemu Prezesowi Kommissyi Rządzącey Kawalerowi Orderow Polskich — JWWMci Panu Dobrodzieiowi w Dreznie',
   'the address on the back of the leaf, six lines: the abbreviations "JMci Panu" and "JWWMci Panu" as written, not spelled out'),
 ],
 # -- her petition of 23 July 1807 (0047_a2)
 '4': [
  ('Kommissja Rządząca!', 'Kommissyo Rządząca!', 'the vocative, ending in o'),
  ('wymierzający', 'wymierzaiący', 'the writer\'s spelling'),
  ('wymierzenia rownej', 'wymierzenia rowney', 'the writer\'s spelling'),
  ('w Dekrecie Kommissji Rządzącej wydanym dnia 21 Lipca ac[?] Nizej podpisana', 'w Dekrecie Kommissyi Rządzącey wydanym dnia 21 Lipca a. c. Niżey podpisana', '"a. c.", anni currentis, written small after the date; then a new sentence'),
  ('że Kommissja Rządząca rowny sposób', 'że Kommissya Rządząca rowny sposob', 'the writer\'s spelling'),
  ('wskaże, jaki wskazany był dla Jaśnie Wielmożnego Wybickiego i zalecie raczy Dyrekcji', 'wskaże, iaki wskazany był dla JW. Wybickiego i zalecić raczy Dyrekcyi', '"JW." abbreviated on the scan; "zalecić raczy" (will be pleased to direct)'),
  ('Administracyjnym', 'Administracyinym', 'the writer\'s spelling'),
  ('nakazala', 'nakazała', 'ł on the scan'),
  ('prośby mojej zostaję z najwyższem', 'prośby moiey zostaię z naywyższem', 'the writer\'s spelling'),
 ],
}

ADD = {
 '1': [('Gdy Interess JPani', 'St[anisław] Mał[achowski]', 'the paraph "St Mał" under the draft: the president of the commission signs it')],
 '3': [('Presentatum 21. Lipca 1807.', 'St[anisław] Mał[achowski]', 'the same paraph under the received note')],
}


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
