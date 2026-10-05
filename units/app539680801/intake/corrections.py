# -*- coding: utf-8 -*-
"""The correction pass on APP 53/968/0/-/801 (NEW_UNIT.md 3a), 2026-10-05.

    python units/app539680801/intake/corrections.py            # check only
    python units/app539680801/intake/corrections.py --write    # once

Every page was read against its scan, the doubtful words on enlarged crops.
A row is here only where the scan is plain, or where the scan and another
copy of the same text agree. Two of the three pieces have such a copy in the
edition:

  * the general power of attorney of 19 February 1805: APP 53/71/0/-/57
    (units/app5371057, pages 0018 to 0021), certified by the same court ten
    days later;
  * the chamber's consent of 28 January 1806: Oe 1 Bü 14526, document 8
    (pages 0045 to 0047).

The lease contract has no other copy; its formulas are those of the Trąbczyn
contracts in Oe 1 Bü 14526 and of APP 53/71/0/-/57.

Nothing was changed because another word would make better sense. The
copyist's own forms stay where the page has them ("Marianten", "Zagurowo",
"Trompczyn", "Lond", "Heinrichs", "bis auf denen ... Hufen befindliche
Holtz", "an den ganzen Gemeinde", "wer dürfen"), and so does the editor's
spelling where it differs from the page only in a letter that does not change
the word (ss for ß, t for th, "Dikhoff" for "Dickhoff"). What the scan does
not settle is in unresolved.md.

The crosses. Eleven of the eighteen lessees could not write; the page has three
crosses before each of their names, and "heißt" (is called) or a dash under it
before the name the clerk wrote for them. The transcription had kept "heißt"
and dropped the crosses. They are given as "xxx", the dash as "—".

ROWS: (text as transcribed, text as on the scan, why). Each `old` must stand
exactly once in the document; an `old` that begins with ^ is a whole line.
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
SLUG = 'app539680801'

VM = 'the same text in APP 53/71/0/-/57: '
CS = 'the same text in Oe 1 Bü 14526, document 8: '
CROSS = 'three crosses stand before the name: a party who signed with a mark'

ROWS = {'1': [
    # ---- the power of attorney (0036 to 0038)
    ('in betreffe der', 'in betreff der', '"in betreff", no final e'),
    ('Einfluß heben können', 'Einfluß haben können', 'the a of "haben"; ' + VM + '"Einfluß haben könnnen"'),
    ('beider hochlöblichen Kammer', 'bei der hochlöblichen Kammer', 'two words; ' + VM + '"bey der Hochlobl. Kammer"'),
    ('angemessen und nur nachtheilig', 'angemessen und mir nachtheilig', '"mir", with its dot; ' + VM + '"und mir nachtheilig"'),
    ('un eingeschränkt', 'uneingeschränkt', 'one word, broken at the line end'),
    ('Interesse am angenehmsten finden', 'Interesse am angemessensten finden', '"angemessensten", with the long double s; ' + VM + '"am angemeßen"'),
    ('an die Königlichen Kriegs- und Forst Rath', 'an den Königlichen Kriegs- und Forst Rath', '"den"; ' + VM + '"an den Königl. Krieges und Forst Rath"'),
    ('L. S. Petenck.', 'L. S. Schenck.', 'the S is that of "L. S." beside it; Schenck is the justiciary of the court who signs the engrossment below and ' + VM + '"Schenck"'),
    # ---- the consent (0039 to 0041)
    ('77 [] Ruten', '77 □ Ruten', 'the page has the square that stands for "Quadrat"; ' + CS + '"77 QuadratRuthen"'),
    ('Morgen Forst, und zwar', 'Morgen Forst gedachte Herrschaften nebst dem übrigen und größern Theil der Forst, und zwar',
     'a line and a half of the page left out; ' + CS + '"gedachte herrschaften nebst dem übrigen und größern theil der Forsten und zwar"'),
    ('Hohelohe', 'Hohenlohe', 'a typing slip'),
    ('Gouverneuers', 'Gouverneurs', 'a typing slip'),
    ('Cabintets', 'Cabinets', 'a typing slip'),
    ('jeden Individuums', 'jeden Individui', 'the Latin genitive; ' + CS + '"eines jeden Individui"'),
    ('in dem hier die Provinz', 'in dem für die Provinz', '"für"; ' + CS + '"in dem für die Provinz Schlesien"'),
    ('noch wie vor', 'nach wie vor', '"nach wie vor", as before'),
    ('des Nötigen deshalb', 'das Nöthige deshalb', '"das Nöthige"; ' + CS + '"das Nöthige deshalb"'),
    ('eingetragen wurden.', 'eingetragen werden.', 'one sentence with "abgeführt ... werden"; ' + CS + '"eingetragen werden"'),
    ('die Patalitact der nun als Dismembration', 'die Totalitaet der von der Dismembration',
     '"Tota-litaet der von der": the same words stand three lines below, "die von der Dismembration ausgenommenen Forsten"; ' + CS + '"die totalität, der von der dismembration reservirten"'),
    ('wogegen nur genehmigen', 'wogegen wir genehmigen', '"wir", with its dot; ' + CS + '"wogegen wir genehmigen"'),
    ('Südpreussiche  Kriegs-und', 'Südpreussische Kriegs- und', 'typing slips'),
    # ---- the lease contract (0042 to 0051)
    ('18. Johann Siemert', '18. Johann Liewert', 'the L of "Luckow" on the same line and of "L. S."; the w of "Luckow"'),
    ('ein ihm zu Ihrem Gute Drzewiec gehörigen Walde der Flächen. Inhalt', 'von dem zu Ihrem Gute Drzewiec gehörigen Walde den Flächen-Inhalt',
     '"von" is written above a struck word, then "dem"; "den Flächen-Inhalt" is one word broken at the line end'),
    ('Einhündert', 'Ein hundert', 'two words, no umlaut'),
    ('9. Christoph Friedrich Vagel', '9. Christ. Friedr. Vagel', 'the page abbreviates; he signs below as Christian Friedrich'),
    ('10. Johann Wilhelm Böttcher', '10. Johann Wilh. Böttcher', 'the page abbreviates'),
    ('16. Michael Just — 10 hufen', '16. Michael Just — 5 hufen', 'the page has 5; with 10 the eighteen shares come to 105 Hufen, not the 100 the contract gives twice'),
    ('18. Johann Liemert', '18. Johann Liewert', 'as on the page before'),
    ('hufen mußes mit Holz', 'hufen wüstes mit Holz', '"wüstes", waste land overgrown with wood'),
    ('mitder einen', 'mit der einen', 'a typing slip'),
    ('De wie vorgedacht', 'Da wie vorgedacht', '"Da"'),
    ('Ausrhoden uober machen', 'Ausrhoden urbar machen', '"urbar machen", to make arable'),
    ('so ebhalten sie', 'so erhalten sie', 'a typing slip'),
    ('so wie[?] der Andere', 'so wie der Andere', 'plain on the page'),
    ('dürfen di[e?] Erbpächtern', 'dürfen die Erbpächtern', 'plain on the page'),
    ('an Erszinß zahlen', 'an Erbzinß zahlen', 'a typing slip'),
    ('den rechten halbjährigen Erbzin[tz?]', 'den ersten halbjährigen Erbzinß', '"ersten": no h; the first half-yearly rent, due at St John 1809'),
    ('Kömplichen und anser öffentlichen Angeben', 'Königlichen und andern öffentlichen Angaben', '"König-lichen" broken at the line end; "andern"; "Angaben"'),
    ('etwoiges Brennholz oder Wiede', 'etwaiges Brennholz oder Weide', '"etwaiges"; "Weide", pasture'),
    ('Annehmer eblaubet, in denjenigen[?] Theil', 'Annehmer erlaubet, in denjenigen Theil', '"erlaubet"; "denjenigen" is plain'),
    ('verkaufet, sondere für', 'verkaufet, sondern für', '"sondern"'),
    ('Schoningen oder Holtzempflanzungen', 'Schonungen oder Holtzanpflanzungen', '"Schonungen", "Holtzanpflanzungen": young growth and plantations'),
    ('ihr Vich unentgeldlich zu hüten mn[?]dessen', 'ihr Vieh unentgeldlich zu hüten indessen', '"Vieh"; "in-dessen" broken at the line end'),
    ('werden, sondere es', 'werden, sondern es', '"sondern"'),
    ('Verkaufsfall eitrift', 'Verkaufsfall eintritt', '"eintritt"'),
    ('zu vräußern', 'zu veräußern', 'a typing slip'),
    ('zehnte Gröschen', 'zehnte Groschen', 'no umlaut'),
    ('an Kinde[r?] und', 'an Kinder und', 'plain on the page'),
    ('Erbzinß pro hüfe a dreißig', 'Erbzinß pro hufe a dreißig', 'the mark over the u is the u-bow, not an umlaut'),
    ('Reichsthaler pro hüfe bleibet', 'Reichsthaler pro hufe bleibet', 'the u-bow, not an umlaut'),
    ('jede gezählte Einhundert', 'jede gezahlte Einhundert', '"gezahlte", paid'),
    ('welche sie verziesen', 'welche sie verzinsen', '"verzinsen", on which they pay rent'),
    ('ein und zwänzig', 'ein und zwanzig', 'no umlaut'),
    ('Brandt[?] Hause oder Krüge', 'Brandt Hause oder Kruge', '"Brandt" is plain; "Kruge", the inn, as in APP 53/71/0/-/57 ("Brauerey und Kruge")'),
    ('aus freunden Gutern', 'aus fremden Gütern', '"fremden Gü-tern", from other estates; the Trąbczyn contracts have "fremdes Getränke"'),
    ('Quart Brandtwenn Ein Reichsthäler', 'Quart Brandtwein Ein Reichsthaler', 'typing slips'),
    ('fünf Reichsthäler Strafe', 'fünf Reichsthaler Strafe', 'no umlaut'),
    ('gehen Jedermanns', 'gegen Jedermanns', '"gegen"'),
    ('so gehen sie als denn', 'so gehen sie als dann', '"als-dann"'),
    ('ist befügt', 'ist befugt', 'the u-bow, not an umlaut'),
    ('Meliorationen verguteget', 'Meliorationen vergütiget', '"vergütiget"'),
    ('Bezahlung das festgesetzten Erbzieses', 'Bezahlung des festgesetzten Erbzinses', '"des ... Erbzinses"'),
    ('künftigen Annehmere,', 'künftigen Annehmer,', '"Anneh-mer," at the line end'),
    ('sich dieserfals entweder an di[e?] Einen oder den[die?] Andern', 'sich dieserhalb entweder an den Einen oder den Andern', '"dieserhalb"; "den" both times'),
    ('wird vor Sr. hochfürstlichen', 'wird von Sr. hochfürstlichen', '"von"'),
    ('daß Erbzächtern', 'daß Erbpächtern', 'a typing slip'),
    ('Mehr hatten Contratenten', 'Mehr hatten Contrahenten', 'the copyist writes h in Latin script like t, as in every "Johann"'),
    ('belehrt würden', 'belehrt wurden', 'the u-bow, not an umlaut'),
    ('die gänzlichen Verläst', 'den gänzlichen Verlust', '"den gänzlichen Verlust"'),
    ('und unterzeichnete.', 'und unterzeichnet.', 'no final e'),
    ('^heißt Martin Dikhoff', 'xxx heißt Martin Dickhoff', CROSS + '; "Dickhoff" with ck'),
    ('^Johann Martin Sydow', 'xxx — Johann Martin Sydow', CROSS),
    ('^heißt Michael Dikhoff', 'xxx heißt Michael Dikhoff', CROSS),
    ('^Gottfried Dikhoff', 'xxx — Gottfried Dikhoff', CROSS),
    ('^heißt Christian Friedrich Vagel', 'xxx heißt Christian Friedrich Vagel', CROSS),
    ('^Johann Wilhelm Böttcher', 'xxx Johann Wilhelm Böttcher', CROSS),
    ('^heißt Johann Büchner', 'xxx heißt Johann Büchner', CROSS),
    ('^heißt Johann Wendel Heilmann', 'xxx heißt Johann Wendel Heilmann', CROSS),
    ('^Martin Dikhoff', 'xxx Martin Dikhoff', CROSS),
    ('^Michael Just', 'xxx Michael Just', CROSS),
    ('^Johann Liemert', 'xxx Johann Liewert', CROSS + '; "Liewert" as in the list'),
    ('Gegentwart', 'Gegenwart', 'a typing slip'),
    ('Aeconomie', 'Oeconomie', '"Oe"'),
    ('Sr. durchlaucht dem regierende Herrn', 'Sr. Durchlaucht dem regierenden Herrn', '"Durchlaucht ... regierenden"'),
]}


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
        tp = os.path.join(tdir, pid + '.txt')
        t = io.open(tp, encoding='utf-8').read().split('\n')
        if t.count(before) != 1:
            sys.exit(f'{pid}.txt: line found {t.count(before)} time(s): {before[:50]!r}')
        t[t.index(before)] = after
        io.open(tp, 'w', encoding='utf-8', newline='\n').write('\n'.join(t))
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
