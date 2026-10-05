# -*- coding: utf-8 -*-
"""The correction pass on I. HA Rep. 162, Nr. 295 (NEW_UNIT.md 3a), 2026-10-05.

    python units/iharep162nr295/intake/corrections.py            # check only
    python units/iharep162nr295/intake/corrections.py --write    # once

Every page was read against its page image (the joined photographs), on
enlarged halves. A row is here only where the image is plain. Nothing was
changed because another word would make better sense. Left as the editor
wrote them: place names in their usual form where the clerk spells them
otherwise (Kopojno for "Kopoyno", Skokum for "Skokom", Olesnica for
"Olesznica", Trąbczyn for "Trąpczyn", Grądzyn for "Grądzin" on 0011), and
the abbreviations of the fee notes. What the image does not settle is in
unresolved.md.

Three kinds of row recur:

  * The sign for the Reichsthaler, which the transcription gives as rt and
    also as rn, rd, rl and rue: it is one sign throughout, and is "rt".
  * A word broken at the line end is marked with ¬ (docs/EDITORIAL_RULES.md).
    Where the transcription has no mark, or a hyphen, the ¬ is put in. A
    hyphen stays where the page breaks a compound at its own hyphen
    ("General-/Invaliden-Casse").
  * "Königl" where the clerk's abbreviation was read as "König".

ROWS: (text as transcribed, text as on the image, why), by document; "0" is
the cover. Each `old` must stand exactly once in its document; an `old` that
begins with ^ is a whole line. Applied to corpus.txt and to transcriptions/,
and logged in transcription_decisions.csv.
"""
import csv
import hashlib
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
SLUG = 'iharep162nr295'
PREFIX = '%04d_I_HA_Rep_162_Nr_295_%s.txt'

RT = 'the Reichsthaler sign, the same as where the transcription has "rt"'
BREAK = 'a word broken at the line end'

ROWS = {
 '0': [
    ('lig Med: Maerz 1827.', 'bis med: Maerz 1827.', '"bis med:", to the middle of March: the end of the span that begins "1820" above it'),
 ],
 '1': [
    ('50000. rn schreibe Fünfzig', '50000. rt schreibe Fünfzig', RT),
    ('Verhandlungs-Obligationen', 'Seehandlungs-Obligationen', '"Seehandlungs": bonds of the Seehandlung, the Prussian state bank; the word is in Oe 1 Bü 9454 fourteen times'),
    ('^einzusenden. Zu mehrerer Sicherheit die', 'einzusenden. Zu mehrerer Sicherheit die¬', BREAK + ' ("die-ses")'),
    ('sondern ich verpfände dersel-', 'sondern ich verpfände dersel¬', BREAK + ' ("dersel-ben")'),
    ('und auf dessen in Süd-', 'und auf dessen in Süd¬', BREAK + ' ("Süd-preussen")'),
    ('Wrąbczyn und Trąbczyn', 'Wrąbczyn und Grądzyn', 'the page has "Grądzyn", its G like that of "General"; the same list on 0011 ends "Wrąbczyn, Grądzin", and Trąbczyn is not among the estates the bond was registered on'),
    ('^gen ist, eventualiter cedire ich von der', 'gen ist, eventualiter cedire ich von der¬', BREAK + ' ("der-selben")'),
    ('200000. rt einramme.', '200000. rt einräume.', '"einräume", concede'),
    ('^ich willige auch in die Subingroßation die', 'ich willige auch in die Subingroßation die¬', BREAK + ' ("die-ser")'),
    ('minus[?] 1804. über 250000. rd Cur.', 'nius 1804. über 250000. rt Cur.', '"Ju-nius", June, broken at the line end; ' + RT),
    ('stehenden 200000. rl verpfändet', 'stehenden 200000. rt verpfändet', RT),
    ('unter Vordre¬', 'unter Vordrü¬', '"Vordrü-ckung", the impression of the seal'),
    ('erstes [T?]hurmarkisches', 'erstes Churmärkisches', '"Churmärkisches", of the Kurmark: the C is that of "Courant"'),
 ],
 '2': [
    ('daß coram Commissario Unserm Regierung', 'daß coram Commissario Unserm Regierungs¬', '"Regierungs-Rath", with its s and the mark of the break'),
    ('über die Summe von 50000. rn', 'über die Summe von 50000. rt', RT),
    ('^Invaliden-Casse von Seiten des König', 'Invaliden-Casse von Seiten des Königl', 'the clerk\'s abbreviation "Königl"'),
    ('^Ober-Krieges-Collegii als Darlehn er', 'Ober-Krieges-Collegii als Darlehn er¬', BREAK + ' ("er-halten")'),
 ],
 '3': [
    ('Kommer Kreise', 'Koniner Kreise', '"Koniner": the docket of this certificate has "im Koniner Kreise"'),
    ('ex decreta vom', 'ex decreto vom', '"ex decreto", as on 0010'),
    ('^1., ist gehöscht.', '1., — ist gelöscht.', '"gelöscht", struck out; a long dash stands where the entry was'),
    ('5. gg. 9. pt. i. e.', '5. gg. 9. pf. i. e.', 'the pfennig sign'),
    ('Rthlr. 5 gg. 9 pt.', 'Rthlr. 5 gg. 9 pf.', 'the pfennig sign'),
    ('^ge Forsten und die Bezahlung der über', 'ge Forsten und die Bezahlung der über¬', BREAK + ' ("über-schießenden")'),
    ('Försten zu genießen', 'Forsten zu genießen', 'no umlaut; "Forsten" as on 0009'),
    ('beiden Theilen freustehende Auf', 'beiden Theilen freistehende Auf¬', '"freistehende"; ' + BREAK),
    ('kundigungsfrist, sind', 'kündigungsfrist, sind', 'the umlaut is on the page'),
    ('Summe der 250000. rue hat', 'Summe der 250000. rt hat', RT),
    ('der Köhnig[?]. Krieges-', 'der Königl. Krieges-', 'the clerk\'s abbreviation "Königl"'),
    ('monatlicher Aufkündigungs¬', 'monatlicher Aufkündigungs-', 'the next line begins with a capital: "Aufkündigungs-Frist"'),
    ('^Ernst erhaltenes gleich hohes Anlehn, der', 'Frist erhaltenes gleich hohes Anlehn, der', '"Frist", the term of notice'),
    ('eventueliter eigenthumlich', 'eventualiter eigenthümlich', '"eventualiter", as in the bond; the umlaut is on the page'),
    ('kenschein der König. General', 'kenschein der Königl. General', 'the clerk\'s abbreviation "Königl"'),
    ('^Die in der Provinz Südpreussen, und', '(Sechs ggr. Stempel)\nDie in der Provinz Südpreussen und deren',
     'the page has "und deren", and in the margin beside the line the note of the stamped paper, as on 0002 and 0008'),
 ],
}


def main():
    write = '--write' in sys.argv
    cp = os.path.join(UNIT_DIR, 'corpus.txt')
    L = io.open(cp, encoding='utf-8').read().split('\n')
    doc, page, pno, seq = '0', None, 0, 0
    where, order = {}, {}
    for i, l in enumerate(L):
        m = re.match(r'\[DOC (\S+)\]', l)
        if m:
            doc, pno = m.group(1), 0
            continue
        m = re.match(r'\[PAGE (\S+)\]', l)
        if m:
            page, pno = m.group(1), pno + 1
            if page not in order:
                seq += 1
                order[page] = seq
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
            log.append((key, f'{SLUG}-{int(d):03d}', where[i][2], old, new.replace('\n', ' / '),
                        f'@{i + 1} {old} -> ' + new.replace('\n', ' / '), 'read on the page image: ' + why))
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
        tp = os.path.join(tdir, PREFIX % (order[pid], pid))
        t = io.open(tp, encoding='utf-8').read().split('\n')
        if t.count(before) != 1:
            sys.exit(f'{pid}: line found {t.count(before)} time(s): {before[:50]!r}')
        t[t.index(before)] = after
        io.open(tp, 'w', encoding='utf-8', newline='\n').write('\n'.join(t))
    dp = os.path.join(UNIT_DIR, 'transcription_decisions.csv')
    with io.open(dp, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['key', 'pad', 'page', 'transcribed', 'proposed', 'decision', 'why'])
        w.writerows(log)
    print('written and logged')


if __name__ == '__main__':
    main()
