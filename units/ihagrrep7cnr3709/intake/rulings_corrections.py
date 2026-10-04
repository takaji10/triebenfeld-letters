# -*- coding: utf-8 -*-
"""The correction pass on I. HA GR, Rep. 7 C, Nr. 3709 (NEW_UNIT.md 3a), 2026-10-04.

    python review/ihagrrep7cnr3709/rulings_corrections.py --direct   # once: the French and the multi-word edits
    python review/ihagrrep7cnr3709/rulings_corrections.py            # writes rulings_corrections.tsv

Every row names its witness. The file's own twins did most of the work: the
decree of 7 December (document 7) against the three rescripts written from it
(8, 9, 10) and the letter to the Prince (11); the Poznań government's three
signature lists (1, 3, 12); its report 12 against the decree on it and draft 13.
Rows: (text that finds the line, old token, new token, reason). A key
beginning "=" is the whole line; "#2" takes its second occurrence.
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
CORPUS = os.path.join(ROOT, 'units', 'ihagrrep7cnr3709', 'corpus.txt')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

GB = ("the paraph of one hand on every paper issued in the Grand Chancellor's name "
      "(signatures sheet, hand 1); Goldbeck held the office")
ROWS = [
 # -- document 1: report of 18 June 1800
 ('unterkönigst Kopiam', 'unterkönigst', 'unterthänigst', 'no such word; the formula "allerunterthänigst", as in this government\'s report of 10 July'),
 ('ersterben in derotester', 'derotester', 'devotester', 'the closing formula "ersterben in devotester Treue"; no such word'),
 ('ersterben in derotester', 'Creue[?]', 'Treue', 'the same formula'),
 ('=ferner', 'ferner', 'Hering', 'a signature among signatures; the same man signs "Hering" on the report of 18 December (signatures sheet)'),
 ('=Darmenberg#1', 'Darmenberg', 'Dannenberg', 'the same signature on all three reports, read "Dannenberg[?]" on the third; n-n and r-m are the same minims, and Darmenberg is no name'),
 ('=[?]oening', '[?]oening', 'Hoening', 'the same signature, read "Hoening" on the report of 18 December'),
 ('=v Tischer[?]', 'Tischer[?]', 'Tischer', 'read without doubt on the report of 10 July'),
 ('=G[?]#1', 'G[?]', 'G[oldbeck]', GB),
 # -- document 2: cabinet order of 14 June 1800
 ('solche Ungesichts', 'Ungesichts', 'Angesichts', 'no such word; the chancery formula "Angesichts dieses"'),
 ('Die Regierung zu Bösen', 'Bösen', 'Posen', 'the address of an order to "der Regierung zu Posen", named six lines above'),
 # -- document 3: report of 10 July 1800
 ('zur Beweismufnahme', 'Beweismufnahme[?]', 'Beweisaufnahme', 'no such word; "Terminus zur Beweisaufnahme und zum Schluß Verfahren"'),
 ('=H[...]', 'H[...]', 'Hering', 'the same signature in the same place as on the other two reports'),
 ('=Darmenberg#2', 'Darmenberg', 'Dannenberg', 'as in document 1'),
 ('=G[?]#2', 'G[?]', 'G[oldbeck]', GB),
 # -- document 4: cabinet order of 1 July 1800
 ('sehr verpögerten', 'verpögerten', 'verzögerten', 'no such word; an Instruction delayed "durch zu viele Nachsicht" has one reading'),
 # -- document 6: the Prince's covering letter
 ('ach Innhalt des', 'ach', 'nach', '"nach Innhalt des Bittschreibens ... zu verfügen"; the n is on the scan'),
 ('entgehen sehen dürfte', 'entgehen', 'entgegen', 'the idiom "der Gewährung ... getrost entgegen sehen"; entgehen gives no sentence'),
 ('[L?]ebtagsRecht', '[L?]ebtagsRecht', 'LebtagsRecht', 'the same word written out three more times in this letter'),
 ('oder irgende', 'irgende', 'irgend', 'broken over the line on the scan: "irgend / einem andern ... Collegio"'),
 ('mein andern Südpreussischen', 'mein', 'einem', 'the same; "mein andern Collegio" gives no sentence'),
 # -- document 7: decree of 7 December 1800
 ('[?]undes der minorennen', '[?]undes', 'mundes', 'Vor¬mundes over the line end; "des Vormundes der minorennen" in the rescripts written from this decree'),
 ('Achtung hiemit bekommt', 'bekommt.', 'bekannt.', 'the rescript written from this line: "zur Nachricht und Achtung hierdurch bekannt"'),
 ('=Q[?]nz[?]', 'Q[?]nz[?]', 'G[oldbeck]', GB),
 # -- document 8: rescript to Poznań
 ('meißen Ræsche', 'meißen', 'meiſten', 'the decree: "Da die meiſten Räthe ihres Collegii"; this clerk\'s ſt is read ß'),
 ('meißen Ræsche', 'Ræsche', 'Räthe', 'the decree: "Räthe"; no such word'),
 ('Collegii Misglieder', 'Misglieder', 'Mitglieder', 'the decree: "Mitglieder des dortigen Vormundschafts. Collegii"; this clerk\'s t is read s'),
 ('anlaßt gezunden', 'gezunden,', 'gefunden,', 'the decree: "veranlaßt gefunden"'),
 # -- document 9: rescript to Warsaw
 ('=Schwolner[?]', 'Schwolner[?]', 'Schroener', 'the same clerk\'s signature under the rescript of 31 December, there read "Khroener[?]"; side by side the two read Schroener (signatures sheet)'),
 ('Schwebes zwischen', 'Schwebes', 'Schwebet', 'no such word; this clerk\'s final t is read s'),
 ('die meißen Räthe der Posener', 'meißen', 'meiſten', 'as in document 8; "meiſten Räthe" in document 10'),
 ('haben wir resolvire', 'resolvire,', 'resolvirt,', 'the same sentence in document 10: "so haben Wir resolvirt, daß"'),
 ('benachrichtiges worden', 'benachrichtiges', 'benachrichtiget', 'no such word; this clerk\'s final t is read s'),
 # -- document 10: rescript to the Kammergericht
 ('Schwebes bey der', 'Schwebes', 'Schwebet', 'as in document 9'),
 ('forcherhalb das', 'forcherhalb', 'solcherhalb', 'no such word; "solcherhalb das Nötige ... erlassen worden"'),
 ('=G[?]#3', 'G[?]', 'G[oldbeck]', GB),
 # -- document 11: draft to the Prince, 7 December
 ('terie, und Gouvernement', 'Gouvernement', 'Gouverneurs', 'a title in the genitive beside "Generals von der Infanterie"; the Prince was Gouverneur of Breslau; the ending is -eurs on the scan'),
 ('=zu munda[?]', 'munda[?]', 'mundiren', 'the registry direction "im Bureau zu mundiren", written the same way on the draft of 31 December'),
 ('zu Posen abgeurkelt', 'abgeurkelt', 'abgeurtelt', 'no such word; "abgeurtelt werde" fourteen lines on'),
 ('darauf den einzigen', 'darauf', 'durch', '"ist durch den einzigen Umstand ... so sehr begründet" is the only sentence; "durch" on the scan'),
 ('von dem Kleno', 'Kleno', 'Pleno', 'the decree and the rescripts: "von dem Pleno der Regierung zu Warschau"'),
 ('zu erklären gewähren', 'gewähren', 'geruhen', 'the form of address "zu erklären geruhen"; written above the line on the scan'),
 ('=G[?]#4', 'G[?]', 'G[oldbeck]', GB),
 # -- document 12: report of 18 December 1800
 ('Ingelfingen verfallen wir', 'verfallen', 'verfehlen', 'this government\'s formula, "verfehlen wir nicht", as in its report of 10 July'),
 ('in erster Instanz ver¬', 'ver¬', 'er¬', 'the decree written on this report: "in erster Instanz erkannt worden"'),
 ('so werden er', 'er', 'wir', '"so werden wir nicht ermangeln"; the report speaks as wir throughout'),
 ('Acta nach beei¬', 'beei¬', 'been¬', '"nach beendigter Instruction"; an Instruction is concluded, not sworn'),
 ('zur Aburkelung', 'Aburkelung', 'Aburtelung', 'no such word'),
 ('=Dannenberg[?]', 'Dannenberg[?]', 'Dannenberg', 'as in document 1'),
 ('=Gu[?]#1', 'Gu[?]', 'G[oldbeck]', GB),
 # -- document 13: rescript to Warsaw, 31 December
 ('zu unterrie¬', 'unterrie¬', 'unterzie¬', 'no such word; "Euch der Abfaßung ... zu unterziehen"'),
 ('=Gu[?]#2', 'Gu[?]', 'G[oldbeck]', GB),
 ('=Khroener[?]', 'Khroener[?]', 'Schroener', 'as in document 9'),
 # -- document 14: draft to the Prince, 31 December (rough)
 ('terie [a?] und Gouvernement', 'Gouvernement', 'Gouverneurs', 'as in document 11'),
 ('July d. 7. an dieselbe', '7.', 'J.', '"unterm 1ten July d. J."; the order is of 1 July 1800 (document 4)'),
 ('=Gunz[?]', 'Gunz[?]', 'G[oldbeck]', GB),
]

# Edits that change more than one word, made directly (logged in notes.md).
DIRECT = [
 ('mit G[o?]egu[?][g/y?] anfangen seyn allerunterthänigsten', 'mit Bezug auf unsern allerunterthänigsten'),
 ('pur Beweismufnahme[?]', 'zur Beweismufnahme[?]'),
 ('wenn ich mir die Freyheit nach', 'wenn ich mir die Freyheit neh¬'),
 ('in dem mein Bittschreiben noch', 'me, mein Bittschreiben noch'),
 ('nun dir.', 'mundiren.'),
]

# The editor's own reading of Prusimska's petition (2026-10-04), given in
# paragraphs and set here on the lines of the first transcription. "Sire." and
# "de Votre Majesté." stand on the page on lines of their own and are kept.
FRENCH = [
 ('Il y a dit huit mois', 'Il y à dix-huit mois qu’ayant en le bonheur d’etre présentée à Posen à Sa Majesté,'),
 ('je lui remise un Memoire', 'je lui remise un Mémoire où je la suplais de me faire rendre la fortune'),
 ('qui aprés le décèsé', 'qui après le décès de ma Mere, me revenait de juste droit. Vous reçutez'),
 ('ma priere avec bonté,', "ma priere avec bouté et me promitez d'accélérer la Justice que je Vous"),
 ('demandais. - Cependant', 'demandais. — Cependant, Sire, voici quatre aus que ce procés'),
 ('nʼest encore jugé', 'commencé a Posen, n’est encore jugé que dans la premiere instance, et au'),
 ('un second decret', 'moment où j’attendais un second decret, mon Tuteur me mande que'),
 ('la decision vient', 'la décision vient d’en etre remise à la Cour de Justice à Berlin.'),
 ('Je ne connaist point', "Je ne connais pour les degrés de Loix, mais tout infortuné et d'autant"),
 ('blasl une Orpheline', 'plus une Orpheline délaissée, ose recouvrir à la bienveillance de Votre Majesté'),
 ('la suplier de daigner', 'et la supplier de daigner presser le Jugement qui doit me restituer dans le bien'),
 ('dont je suis privée', 'dont je suis privée depuis si longtemps. C’est avec Confiance Sire, que je'),
 ('demande à Votre Caup', 'demande à Votre Coeur paternel, la grace de réaliser la promesse que Vous'),
 ('daignalez me faire', 'daiquatez me faire. Je le fais, je plaide contre le Prince de Hohenlohe,'),
 ('donc point la protection', 'si ce n’est donc point la protection de Votre Majesté qui me soutiendra, dénuée'),
 ('de tout secouril', 'de tout secours, je ferai abandonnée à la plus dure misère. Que la pitié'),
 ('joinée à la bonté', 'jointe à la bouté et la Clémence de Votre Majesté accueillent favorable¬'),
 ('Lui adresser, quand', 'ment la prière que j’ose Lui adresser, quand à moi je ne cesserai d’etre'),
 ('=1802', '1802.'),
 ('la tres dévouée et commise', 'la trés dévouée et soumise'),
 ('sujette Michaline Prusimska', 'sujette Michaline Prusimska.'),
]


def find(L, key):
    n = 1
    if '#' in key and key.rsplit('#', 1)[1].isdigit():
        key, n = key.rsplit('#', 1)[0], int(key.rsplit('#', 1)[1])
        hits = [i for i, l in enumerate(L, 1) if l == key[1:]]
        if len(hits) < n:
            sys.exit(f'{key!r}: only {len(hits)} such lines')
        return hits[n - 1]
    hits = [i for i, l in enumerate(L, 1)
            if (l == key[1:] if key.startswith('=') else key in l)]
    if len(hits) != 1:
        sys.exit(f'{key!r}: found on {len(hits)} lines')
    return hits[0]


def main():
    L = open(CORPUS, encoding='utf-8').read().split('\n')
    if '--direct' in sys.argv:
        for old, new in DIRECT:
            i = find(L, old)
            L[i - 1] = L[i - 1].replace(old, new)
            print(i, L[i - 1])
        for key, new in FRENCH:
            i = find(L, key)
            L[i - 1] = new
            print(i, new)
        with open(CORPUS, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(L))
        return
    # "#n" keys count occurrences as the corpus stood before any was changed,
    # so resolve them all against the same text.
    rows = sorted((find(L, key), old, new, why) for key, old, new, why in ROWS)
    with open(os.path.join(HERE, 'rulings_corrections.tsv'), 'w', encoding='utf-8',
              newline='\n') as f:
        for r in rows:
            f.write('\t'.join(map(str, r)) + '\n')
    print(len(rows), 'rows')


if __name__ == '__main__':
    main()
