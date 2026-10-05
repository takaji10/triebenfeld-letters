# -*- coding: utf-8 -*-
"""The correction pass on I. HA GR, Rep. 7 C, Nr. 1414 (NEW_UNIT.md 3a), 2026-10-05.

    python units/ihagrrep7cnr1414/intake/corrections.py            # check only
    python units/ihagrrep7cnr1414/intake/corrections.py --write    # once

Every page was read against its scan, the office marks and signatures on
enlarged crops (docs/GOVERNMENT_FILES.md). A row is here only where the scan
is plain, or where the scan and another line of the same file agree. Nothing
was changed because another word would make better sense. What the scan does
not settle is in unresolved.md.

Three readings identify people and rest on more than letter shapes:

  * Raumer. The extract is routed "Hr von Raumer" in Latin script, and the
    same name signs the direction on the slip and the "Ad acta" on Schrötter's
    letter. The transcription has "Rammer", "Maunes[?]" and "Maurer[?]". Karl
    Georg von Raumer was a councillor of the department of foreign affairs in
    these years; the three are one man and one name.
  * Goldbeck. The large hand in the left column of the draft adds a third
    addressee under "et in simili": "in simili des H. GK v. Goldbeck Excell.",
    the Grand Chancellor. The clerk's note below, "Gr. in triplo md.", fair
    copies in triplicate, counts three letters: Hoym, Schroetter, Goldbeck.
  * Haugwitz, and probably Alvensleben. The draft is signed by two of the
    ministers of the department. The second signature reads Haugwitz. The
    first begins with a tall A and runs out in minims; Alvensleben was the
    other minister who signed with Haugwitz in 1797. It is given with a mark
    of doubt.

ROWS: (text as transcribed, text as on the scan, why), by document. Each `old`
must stand exactly once in its document; an `old` that begins with ^ is a
whole line. Applied to corpus.txt and to transcriptions/, logged in
transcription_decisions.csv; office_notes.yml is then written, since it
quotes corrected lines.
"""
import csv
import hashlib
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
SLUG = 'ihagrrep7cnr1414'
PREFIX = 'I_HA_Rep_7_C_Nr_1414_'

RAUMER = 'the name is written out in Latin script on the extract, "Hr von Raumer"; the same signature stands on the slip, the extract\'s routing and Schrötter\'s letter'

ROWS = {
 '1': [
    ('Ministri Fuhl[?] u', 'Ministri Frhrn', '"Frh" with "rn" raised: Freiherrn, as "Grafen" stands before Hoym in the address above'),
    ('geben wir aus die Ehre', 'geben wir uns die Ehre', '"uns": the formula "geben wir uns die Ehre"'),
    ('ehemaligen Rupublik Pohlen anquirirten', 'ehemaligen Republik Pohlen acquirirten', 'typing slips; "acquirirten", acquired'),
    ('^Berlin, d. 11. Januar 1792.', 'Berlin, d. 11. Januar 1797.', 'the page has 1797, as at the head of the draft'),
    ('^in simuli[?] des', 'in simili des', '"in simili", as "et in simili" in the address above it'),
    ('^R[?]. G[?]. Goldbeim[?]', 'H. G[roß]K[anzlers] v. Goldbeck', 'the name is Goldbeck; before it "H." and the joined letters GK, for the Grand Chancellor. A third addressee: the note below orders fair copies in triplicate'),
    ('^Erfolg.', 'Excell.', '"Excell." with a flourish, as after Hoym and Schroetter'),
    ('^Au[?]', '[Alvensleben?]', 'the first of two ministers\' signatures: a tall A and a run of minims. Alvensleben signed for the department beside Haugwitz in 1797; given as uncertain'),
    ('^Keuglig[?]', 'Haugwitz', 'the second signature: H, a, u with its bow, g, w, i with its dot, z'),
    ('zur Inh:', 'zur Post.', 'the registry\'s mark of dispatch: on the 12th all were sent to the post; the same mark is in Nr. 3709'),
 ],
 '2': [
    ('^A. 10. d. 8. Jan[?] 1797.', 'A. 10. d. 8. Jan 1797.', 'the month is January: the extract was received on 2 January and the draft made on this direction is of the 11th'),
    ('2. dH. E[?] v. Schrötter', '2. dH. Frh. v. Schrötter', 'the abbreviation for Freiherr, as "Gr." for Graf in the line above'),
    ('^zu gefallen Gebrauche', 'zu gefällig. Gebrauch', '"zu gefälligem Gebrauch", abbreviated: the words the draft made on this direction uses'),
    ('^Maunes[?]', 'Raumer', RAUMER),
    ('^H p von Rammer', 'Hr von Raumer', '"Hr", Herr; ' + RAUMER),
    ("^jusqu'à l'accublement pour passer d'une maison à", "affatigué jusqu'à l'accablement pour passer d'une maison à", 'the line begins "affatigué", which the transcription left out; "accablement"'),
 ],
 '3': [
    ('^Februar 13. No 709.', 'Februar B. No 709.', 'the journal letter B, in the red hand that wrote "vide Journal A. No. 10." on the extract in January'),
    ('von Pohlen angesessenen, gegen', 'von Pohlen angesessenen, gegen¬', 'a word broken at the line end ("gegen-wärtig")'),
    ('^16 Ma[r?] 97', '16 Mart 97', '"Mart", March: the letter was received on 8 February'),
    ('^Maurer[?]', 'Raumer', RAUMER),
 ],
}

OFFICE = '''# Text the receiving office wrote on someone else's paper. Here the office is
# the department of foreign affairs: its councillor's direction on the slip
# (0003), its marks on the extract of the envoy's dispatch (0004), and its
# marks on Schrötter's letter (0005). The lines are ordinary text in
# corpus.txt; this file only says which they are, so the site can set them
# apart. Each block stands at the end of its page, wherever it is written on
# the sheet (intake/build_pages.py).
#   first: the block's first line exactly as it stands in corpus.txt
#   lines: how many lines the block has
# A first line that is edited must be edited here too; build_db.py stops if a
# block cannot be found.
blocks:
  - letter: '2'
    page: '0003_a2'
    first: 'A. 10. d. 8. Jan 1797.'
    lines: 6
  - letter: '2'
    page: '0004_a2'
    first: 'Hr von Raumer'
    lines: 3
  - letter: '3'
    page: '0005_a2'
    first: 'N 5 d 11 Jan'
    lines: 6
'''


def main():
    write = '--write' in sys.argv
    cp = os.path.join(UNIT_DIR, 'corpus.txt')
    L = io.open(cp, encoding='utf-8').read().split('\n')
    doc = page = None
    pno = 0
    where = {}
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
    log, bad, edits = [], [], []
    for d, rows in ROWS.items():
        for old, new, why in rows:
            if old.startswith('^'):
                old = old[1:]
                hits = [i for i in where if where[i][0] == d and L[i] == old]
                n = len(hits)
            else:
                hits = [i for i in where if where[i][0] == d and old in L[i]]
                n = sum(L[i].count(old) for i in hits)
            if n != 1:
                bad.append(f'[{d}] {old!r}: found {n} time(s)')
                continue
            i = hits[0]
            before = L[i]
            L[i] = new if before == old else before.replace(old, new)
            key = hashlib.md5(f'{d}|{i + 1}|{old}|{new}'.encode()).hexdigest()[:8]
            log.append((key, f'{SLUG}-{int(d):03d}', where[i][2], old, new,
                        f'@{i + 1} {old} -> {new}', 'read on the scan: ' + why))
            edits.append((where[i][1], before, L[i]))
    if bad:
        sys.exit('NOT WRITTEN\n' + '\n'.join(bad))
    print(len(log), 'corrections')
    if not write:
        return
    with io.open(cp, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(L))
    tdir = os.path.join(UNIT_DIR, 'transcriptions')
    for pid, before, after in edits:
        tp = os.path.join(tdir, PREFIX + pid + '.txt')
        t = io.open(tp, encoding='utf-8').read().split('\n')
        if t.count(before) != 1:
            sys.exit(f'{pid}: line found {t.count(before)} time(s): {before[:50]!r}')
        t[t.index(before)] = after
        io.open(tp, 'w', encoding='utf-8', newline='\n').write('\n'.join(t))
    with io.open(os.path.join(UNIT_DIR, 'transcription_decisions.csv'), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['key', 'pad', 'page', 'transcribed', 'proposed', 'decision', 'why'])
        w.writerows(log)
    io.open(os.path.join(UNIT_DIR, 'office_notes.yml'), 'w', encoding='utf-8', newline='\n').write(OFFICE)
    print('written and logged; office_notes.yml written')


if __name__ == '__main__':
    main()
