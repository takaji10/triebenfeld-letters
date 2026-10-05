# -*- coding: utf-8 -*-
"""The correction pass on III. HA MdA, III. Nr. 12367 (NEW_UNIT.md 3a), 2026-10-04.

    python units/iiihamdaiiinr12367/intake/corrections.py            # check only
    python units/iiihamdaiiinr12367/intake/corrections.py --write    # once

Every page was read against its scan, the hurried notes (0003, 0004) and the
Polish and German pages on enlarged crops. A row is here only where the scan
is plain. Nothing was changed because another word would make better sense,
and the writers' own spelling stays (tems, succes, deja, "wierżytelności" with
its dotted z, y for j in the Polish). The names the editor wrote in their
usual form where the scribe did not also stay (Trąbczyn for "Trąpczyn",
Hohenlohe for "Hohenloe", Weigel for "Weigl"). What the scan does not settle
is in unresolved.md.

Beside each of Prince Lubecki's Polish letters (0008, 0009 right, 0010) the
file has a German translation of the time; it is not transcribed, but it was
used as a witness for the Polish ("nach den bei uns geltenden Gesetzen" for
"podług praw u nas obowiązujących", "diese Taxe" for "taxa takowa").

The editor asked whose signature "[L. C. d. Mo…heim?]" is. It is Baron
Mohrenheim's, written four ways; each is given here as it stands on its page,
the abbreviated title expanded in brackets. His signature on 0004, which the
transcription left out, is added with the day he wrote under the note.

ROWS: (text as transcribed, text as on the scan, why). Each `old` must stand
exactly once in its document. ADD: lines appended to a document's last page.
Applied to corpus.txt and to transcriptions/, and logged in
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
SLUG = 'iiihamdaiiinr12367'
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROWS = {
 # -- Mohrenheim to Schmidt, 7 February 1828 (0002)
 '1': [
  ('[L. C. d. Mo…heim?]', 'Le B[ar]on d[e] Mohrenheim', 'the signature: "Le Bon D. Mohrenheim", "on" raised; the same hand and flourish sign 0003, 0004 and 0006'),
 ],
 # -- his note on the council (0003)
 '2': [
  ('vérele [?] les quoi on délibérera.', 'voilà sur quoi on délibérera.', '"How? That is what will be deliberated"; the S of "sur" is the one in "sur l\'affaire" above'),
  ('Me[?]', 'M[ohrenheim]', 'the initial M alone, with the flourish of his full signature'),
 ],
 # -- his note returning a book or paper (0004)
 '3': [
  ('voici votre Devoir :', 'voici votre Dubois ;', 'the word has a b with its ascender, "Dubois": something of that name which Schmidt had lent him'),
  ('couver l\'affaire Weigel le Soyez tranquille. Sur le reste je', 'pousser l\'affaire Weigel & soyez tranquille sur le reste je', '"I shall not fail to push the Weigel matter, and be easy about the rest"; "&" as in his other note'),
  ('J\'ai ici mes tiens affaires qui', 'J\'ai ici un tems affreux qui', '"dreadful weather here"; the rest of the sentence is not settled, see unresolved.md'),
 ],
 # -- Mohrenheim to Schmidt, 20 February 1830 (0005-0006)
 '4': [
  ('m’avex', 'm’avez', 'a typing slip'),
  ('Tribuneaux', 'Tribunaux', 'a typing slip'),
  ('banqiuers', 'banquiers', 'a typing slip'),
  ('par la nature', 'par sa nature', '"par sa nature"'),
  ('[L. C. d. Mo…heim?]', 'Mohrenheim', 'the signature, here the bare name'),
 ],
 # -- to Schmidt, 29 September 1830 (0007)
 '5': [
  ('empressé deporter', 'empressé de porter', 'two words'),
  ('à saison des dettes', 'à raison des dettes', '"on account of the debts"'),
  ('conformément à vos[?] désirs', 'conformément à vos désirs', 'plain on the scan; this writer\'s final s looks like r'),
  ('qui l’out débouté', 'qui l’ont débouté', 'a typing slip'),
  ('que vos[?] communications', 'que vos communications', 'plain on the scan'),
  ('à tems[?] de', 'à tems de', 'plain on the scan'),
  ('des titiges à dessus mentionnér', 'des litiges ci-dessus mentionnés', '"the lawsuits mentioned above"'),
 ],
 # -- Lubecki to Weigel, 22 September 1830 (0008)
 '6': [
  ('w Kom. Rzad.', 'w Kom. Rząd.', '"Rząd." for Rządowey, as in the letter of 27 November'),
  ('r. b. I ponoqioną z d. 14 Wrzes. r. B.', 'r. b. i ponowioną z d. 14 Wrzes. r. b.', '"and renewed on 14 September of this year"; German column: "die Erneuerung desselben vom 14 7br"'),
  ('Mastrat[?][?] jakie', 'Mu strat, jakie', '"Mu" ends one line, "strat" begins the next: "compensation to him for the losses"'),
  ('Jego, wierżytelności', 'Jego wierżytelności', 'no comma on the scan'),
  ('to wygórowaniem,', 'to wygórowanem,', '"finding this demand excessive"; no i on the scan'),
  ('pod _ag praw a nas', 'podług praw u nas', '"according to the laws in force with us"; the ł is written over a correction'),
  ('Chcąc[?] z', 'Chcąc z', 'plain on the scan'),
  ('mieyscu przekonanie się', 'mieyscu przekonania się', 'ends in a, run together with "się"'),
  ('i ocernienie tym', 'i ocenienie tym', '"and the assessment"'),
  ('stopnia realniey wartości', 'stopnia realney wartości', '"of the real value"'),
  ('Kapitalu -', 'Kapitału —', 'ł on the scan; the dash is punctuation'),
  ('sigę. X. X. Lubecki', 'sig. X. X. Lubecki', '"sig." for signatum, underlined; the German column has "gez."'),
 ],
 # -- Weigel to Lubecki, 14 October 1830 (0009)
 '7': [
  ('der Schiff. Roggen', 'der Schfl. Roggen', '"Schfl." for Scheffel, as twice more in the sentence'),
  ('die Häffte', 'die Hälfte', 'l and f, not ff: "half the harvest"'),
  ('brutto Einnahme abgegeben.', 'brutto Einnahme abgezogen.', '"deducted"; z and g with their descenders'),
  ('daß Hoch', 'daß Hoch¬', '"Hochdieselben", broken at the line end'),
  ('zu he[g?]u pp.', 'zu seyn pp.', 'the closing formula "habe die Ehre zu seyn"'),
 ],
 # -- Lubecki to Weigel, 27 November 1830 (0009 right, 0010)
 '8': [
  ('Przych. I Skarbu do..', 'Przych. i Skarbu do', '"i Skarbu"; "do" (to) stands alone above the space left for the address'),
  ('zrobienia wżytku', 'zrobienia użytku', '"to make use of"'),
  ('przez Niegotascy sądowey', 'przez Niego taxy sądowey', '"the court valuation sent by him": Niego, then "taxy" on the next line'),
  ('gdy taka takowa', 'gdy taxa takowa', '"that valuation"; the x is written over a k; German column: "diese Taxe"'),
  ('ocienioną bydźwinna', 'ocenioną bydź winna', '"must be assessed"'),
  ('exekucyine rozwinać', 'exekucyine rozwinąć', 'ą on the scan'),
  ('do wkładu warunków', 'do układu warunków', '"terms for an agreement"; German column: "einer Uebereinkunft"'),
  ('r. b. Nadmieniłem', 'r. b. nadmieniłem', 'small n'),
  ('sigę. X. X. Lubecki', 'sig. X. X. Lubecki', 'as on 0008'),
 ],
 # -- Fuhrmann to Schmidt, 14 December 1831 (0011-0012)
 '9': [
  ('Monsieur le Conseiller (Schmidt),', 'Monsieur le Conseiller [Schmidt],', 'the name is the editor\'s addition; square brackets, as they wrote it on 0007'),
  ('la Commision des', 'la Commission des', 'broken at the line end: "Commis-sion"'),
  ('presenter cette affaires.', 'presenter cette affaire.', 'the final stroke is this writer\'s flourish, not an s'),
  ('j’ais l’honneur', 'j’ai l’honneur', 'the same flourish'),
  ('circonstances j’ai fait', 'circonstance j’ai fait', 'the same flourish, on the page and on the catchword before it'),
  ('Votre très honorable et très obiesant Serviteur', 'Votre très h[um]ble et très ob[éissan]t Serviteur', 'abbreviated on the scan, "hble" and "obt" with raised endings: humble, not honorable'),
 ],
 # -- Engel to Schmidt, 13 March 1832 (0013)
 '10': [
  ('Monsieur (Schmidt)!', 'Monsieur [Schmidt]!', 'the name is the editor\'s addition'),
  ('que j’ai en l’honneur', 'que j’ai eu l’honneur', 'a typing slip'),
  ('J’ai tout bien d’espérer', 'J’ai tout lieu d’espérer', '"every reason to hope"'),
  ('s’efforiant', 's’efforçant', 'ç on the scan'),
 ],
 # -- Fuhrmann to Schmidt, 20 March 1832 (0014)
 '11': [
  ('Varsovie le 8/21 mars 1832', 'Varsovie le 8/20 mars 1832', '8 over 20 on the scan; the two calendars were twelve days apart'),
  ('(Monsieur Schmidt,)', '[Monsieur Schmidt,]', 'the salutation is the editor\'s addition; the head of the page is cut off on the scan'),
  ('Vous avex bien', 'Vous avez bien', 'a typing slip'),
  ('que j’ai priser,', 'que j’ai prises,', 'a typing slip'),
  ('dont j’ai en l’honneur', 'dont j’ai eu l’honneur', 'a typing slip'),
  ('l’éestimation', 'l’éstimation', 'one e'),
  ('Vous serez sa[?] même', 'Vous serez à même', '"as you will be able to judge"'),
  ('très obiessant Serviteur', 'très obéissant Serviteur', 'a typing slip'),
 ],
}

# Lines the transcription does not have, appended to the document's last page.
ADD = {
 '3': [
  ('L. B. d. Mohrenheim', 'his signature at the foot of 0004, "Le Baron de Mohrenheim" in initials, not transcribed'),
  ('Mardi.', '"Tuesday", at the foot on the left: the note\'s only date'),
 ],
}


def main():
    write = '--write' in sys.argv
    cp = os.path.join(UNIT_DIR, 'corpus.txt')
    L = io.open(cp, encoding='utf-8').read().split('\n')
    doc = page = None
    pno = 0
    where, last = {}, {}
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
        if l.strip():
            last[doc] = i
    log, bad, edits = [], [], []
    for d, rows in ROWS.items():
        for old, new, why in rows:
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
    if bad:
        sys.exit('NOT WRITTEN\n' + '\n'.join(bad))
    adds = []
    for d, rows in ADD.items():
        i = last[d]
        for n, (line, why) in enumerate(rows):
            key = hashlib.md5(f'{d}|add|{line}'.encode()).hexdigest()[:8]
            log.append((key, f'{SLUG}-{int(d):03d}', where[i][2], '', line,
                        f'line added: {line}', 'read on the scan: ' + why))
            adds.append((i + 1 + n, where[i][1], line))
    for at, _, line in sorted(adds, reverse=True):
        L.insert(at, line)
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
    for _, pid, line in sorted(adds):
        tp = os.path.join(tdir, pid + '.txt')
        t = io.open(tp, encoding='utf-8').read()
        io.open(tp, 'w', encoding='utf-8', newline='\n').write(t.rstrip('\n') + '\n' + line + '\n')
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
