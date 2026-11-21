# -*- coding: utf-8 -*-
"""Kodeks Dyplomatyczny Wielkopolski: the editor's entries, as documents of one holding.

    python units/kdw/intake/holding.py               # check: every entry found, the corpus agrees
    ... --write       page files, corpus.txt and the generated parts of rulings.yml
    ... --english     write translation/doc<N>.yml from intake/english_kdw.py
    ... --cache       put them into the translation cache
    ... --summaries   write the summaries S (intake/english_kdw.py) everywhere they are kept

How the holding is made (the editor, 2026-10-16):
- one holding for all entries, whatever the volume; each entry is one document,
  numbered by date (ENTRIES, in order). The Kodeks's own volume and number are
  the document's citation, shown on its page and linked to the volume online;
- the text is the editor's file intake/kodeks.txt, entry by entry, exactly as it
  stands ("it should be taken as secure"): every line of the entry is a line of
  the document (pages: by_paragraph), from "Dokument Nr ..." to the last note.
  Nothing is corrected;
- text only: no page images. Each document is one page, id NNNN_a;
- the footnote markers of the volumes 5 to 11 stand in the text glued to their
  words ("Mezeconis1", "quatuordecimoa"); footnotes.yml records where each is,
  and the site raises them and sets the notes apart. The text is unchanged.
- the estates of focus are from the editor's list of seventeen, by hand, per
  entry (ESTATES below): Zagórów, Skokum, Kopojno, Ląd, Szetlew, Szetlewek,
  Łukom, Trąbczyn, Wrąbczyn, Wrąbczynek, Świątniki, Oleśnica, Łazy, Adamierz,
  Drzewce, Przybysław, and Imielno (added by the editor the same day, for the
  gift of 1243). Łazy and Szetlewek are not in these entries;
  Przybysław occurs only as a man's name.
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(UNIT_DIR))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'intake'))
sys.path.insert(0, HERE)
import courtbook  # noqa: E402
import kdw_source  # noqa: E402

SLUG = 'kdw'
REF = 'BK PAN Kodeks Dyplomatyczny Wielkopolski'
RAW = kdw_source.RAW
WORK = 'Kodeks Dyplomatyczny Wielkopolski'
SOURCE = os.path.join(HERE, 'kodeks.txt')
# The ten entries the gazetteer cited and the holding lacked, staged 2026-10-24
# (intake/stage_missing.py: read from the WBC HTML, checked against Igor's
# independent conversion of the same HTML, all ten agreeing character for
# character once the WBC's own copy of the editors' note at the end of the
# text div is stripped).
SOURCE2 = os.path.join(HERE, 'kodeks_missing.txt')

# (document, volume, the Kodeks's number, [year, month, day], place of issue or "", doc_type, estates, why)
# In order of date. The date and place are the editors' heading's (volumes 5 to 11)
# or their regest's (1 to 3), which read the document's own dateline.
ENTRIES = [
    (1, 1, 20, [1173, 8, 31], 'Gniezno', 'donation', ['wrabczynek', 'lad'],
     'Mieszko gives "parvum Vronchin", Wrąbczynek, to the Cistercians of Ląd'),
    (2, 1, 222, [1240, 9, 30], '', 'donation', ['lad', 'zagorowo', 'skokum', 'kopojno', 'trabczyn', 'szetlew', 'lukom', 'wrabczyn'],
     'the tithes of Zagórów, Skokum, Kopojno, Trąbczyn, Szetlew, Łukom and Wrąbczyn given to Ląd; "s. l.", no place'),
    (3, 1, 238, [1243, 5, 4], 'Gniezno', 'donation', ['imielno'],
     'the hospital of Gniezno given to the Holy Sepulchre of Miechów; among its villages "Chemelino", Imielno (the editor)'),
    (4, 1, 393, [1261, 12, 10], 'Sechowa', 'confirmation', ['lad', 'szetlew', 'swiatniki', 'rzgow', 'zagorowo', 'skokum', 'olesnica', 'kopojno'],
     'the possessions of Ląd confirmed: Szethowo (Szetlew), Rzgowo with its sanctuary people (Świątniki), Zagorowo, Skokom, Oleszyno, Capayn; '
     'place as written, the editors take it to be Czechowo or Szetlew'),
    (5, 1, 460, [1276, 3, 27], 'Dłusk', 'donation', ['trabczyn'],
     'Trąbczyn given to Count Nicholas, treasurer of Ląd'),
    (6, 6, 27, [1280, 10, 18], 'Kalisz', 'confirmation', ['lad', 'szetlew', 'rzgow', 'swiatniki'],
     'the possessions of Ląd confirmed: Szechouo (probably Szetlew, note 7), Irgouo with the Sanctuarii (Świątniki, note 8), '
     'and Rzgowo (Rzgów, added at the editor\'s word 2026-10-21)'),
    (7, 2, 678, [1291, 10, 21], 'Gniezno', 'confirmation', ['kopojno', 'lad'],
     'Kopojno exchanged to Ląd for Głowiew, Sławsk and Chocicza'),
    (8, 2, 685, [1292, 9, 29], 'Kalisz', 'confirmation', ['wrabczyn'],
     'the exchange of Wroncino (Wrąbczyn) and Bieganin for Niałek confirmed'),
    (9, 2, 1252, [1346, 11, 13], 'Pyzdry', 'decree', ['trabczyn'],
     'Stropiszyn and Pępocin adjudged to the church of Gniezno against Jan and Przedpełk, heirs of Trąbczyn'),
    (10, 2, 1253, [1346, 11, 13], 'Pyzdry', 'decree', ['trabczyn'],
     'the same, against Andrzej, heir of Trąbczyn, and his kin'),
    (11, 3, 1739, [1377, 5, 27], 'Gniezno', 'attestation', ['wrabczynek', 'adamierz', 'lad'],
     'the judges attest that Wrąbczynek with Adamierz belong to Ląd'),
    (12, 6, 283, [1384, 1, 31], 'Poznań', 'decree', ['wrabczyn', 'wrabczynek', 'lad'],
     'Vronczino adjudged to Ląd; the editors: Wrąbczyn or Wrąbczynek (note 11)'),
    (13, 3, 2014, [1399, 10, 13], 'Ląd', 'decree', ['trabczyn', 'lad'],
     'the sheaf tithe of Trąbczyn adjudged to Ląd against the parish priest of Trąbczyn'),
    (14, 5, 117, [1407, 11, 19], 'Niepołomice', 'privilege', ['zagorowo', 'lad'],
     'the King allows Ląd to found a town at Zagórów'),
    (15, 5, 191, [1411, 11, 30], 'Ląd', 'contract', ['zagorowo', 'drzewce', 'lad'],
     'the abbot of Ląd exchanges with the schultheiss of Nowe Zagórowo alias Drzewiec'),
    (16, 7, 733, [1414, 6, 13], 'Ląd', 'notarial_attestation', ['zagorowo', 'lad'],
     'the parish church of Zagórów handed over to Ląd'),
    (17, 7, 755, [1415, 4, 16], 'Gniezno', 'certification', ['lad'],
     'a plot at Gniezno sold to Ląd; Mikołaj and Andrzej of Trąbczyn among the witnesses'),
    (18, 5, 280, [1418, 6, 3], 'Ląd', 'contract', ['wrabczyn', 'drzewce', 'zagorowo', 'lad'],
     'the abbot of Ląd exchanges the farm in Wrąbczyn Wielki for one in Drzewce'),
    (19, 11, 2000, [1434, 5, 15], 'Trąbczyn', 'power_of_attorney', ['trabczyn'],
     'Wojciech of Trąbczyn, canon of Kruszwica, empowers his brother Jan of Trąbczyn'),
    (20, 10, 1520, [1440, 8, 10], 'Buda', 'donation', ['wrabczynek', 'adamierz'],
     'the King charges 300 marks on Wrąbczynek, Adamierz and Borzykowo for Stanisław Czarny'),
    (21, 10, 1532, [1440, 11, 22], 'Buda', 'donation', ['adamierz', 'wrabczynek'],
     'the King charges 200 marks on Adamierz, Borzykowo and Wrąbczynek for Stanisław Czarny'),
    # 22 to 31: the ten entries the gazetteer cites and the holding lacked
    # (docs/MISSING_SOURCES.md; brought in 2026-10-24 at the editor's word,
    # "add them to the site like the other ones"). Text in kodeks_missing.txt,
    # read from the WBC HTML and checked against Igor's independent
    # conversion of the same HTML (intake/stage_missing.py: all ten agree).
    (22, 1, 228, [1241, 6, 17], 'Kopojno', 'contract', ['wrabczyn', 'lad'],
     'Kazimierz, duke of Kujawy and Ląd, exchanges his estates of Głowiewo and Wrąbczyn (Wronecino), once the hunters\' '
     'land, for the abbey\'s estate of Koszanów, and grants the villages the same liberty the brothers have in their '
     'other estates'),
    (23, 1, 535, [1284, 2, 18], 'Kalisz', 'privilege', ['trabczyn'],
     'Przemysł II allows Count Mikołaj, treasurer of Ląd, to locate his estate of Trąbczyn (Tropcssino) under German '
     'law, the estate freed for ever of all the Polish dues — the naraz, the povoz, the prevod, the stroza, the '
     'podvorove, the castle\'s summons, the opole, the ox and the cow, the cifo of honey — and the settlers not to '
     'owe the poradlne; the gazetteer\'s footnote 83'),
    (24, 2, 672, [1291, 8, 1], 'Pyzdry', 'privilege', ['wrabczyn'],
     'Przemysł II gives his village Wrąbczyn (Wronchino), held under Polish law, to Henryk, citizen of Pyzdry, to '
     'locate under the German law of Pyzdry: the sixth mansus free, a tavern, a fishpond, a mill and the shoemakers\' '
     'free shop, the woods and marshes for pasture, the meadows, twelve years free of dues, then six measures of rye '
     'and of oats and a ferton from each mansus; the village joined to the duke\'s town of Sal, and hares and '
     'partridges free to hunt'),
    (25, 2, 795, [1298, 9, 9], 'Pyzdry', 'privilege', ['wrabczyn'],
     'Władysław, duke of the kingdom of Poland, grants Count Wojsław the right to locate his village Wrąbczyn '
     '(Vronztino) under German law, the village and its people freed of all the Polish dues and answerable to the '
     'duke alone, and Wojsław and his heirs to judge all causes within its bounds and keep the fines'),
    (26, 2, 1044, [1324, 8, 9], 'Pyzdry', 'donation', ['wrabczyn', 'lad'],
     'King Władysław gives the abbey of Ląd the site of a water mill on the Warta below the castle of Pyzdry, in '
     'remission of sins and for the great desolation his army had worked on the abbey, and confirms its estates '
     'given by nobles or honestly bought, among them Wrąbczyn (Wronchyno) with the lake called Seborowo, their people '
     'to have the liberty of Mieszko\'s founding privilege'),
    (27, 3, 1363, [1357, 8, 14], 'Konin', 'attestation', ['wrabczyn'],
     'Wyrzbenta, the general captain of Poland, attests the exchange made of their free will between Abbot Jan of '
     'Ląd, with his convent, and Zemka, wife of Albert: the abbey\'s Szczonowo (Usczonowo) for her third part of '
     'great Wrąbczyn, and she is to move no claim in that third part when her mother dies'),
    (28, 3, 1478, [1362, 5, 31], 'Konin', 'contract', ['wrabczyn', 'lad'],
     'Wyrzbenta, castellan of Poznań and general captain of Poland, attests that Laurentius, heir of Królikowo and '
     'castellan of Ląd, sold the third part of great Wrąbczyn he had held peaceably for three years to Abbot Jan and '
     'the abbey for 56 marks of grossi, at 24 scotos the mark and 2 grossi the scotus'),
    (29, 3, 1490, [1363, 3, 16], 'Ląd', 'contract', ['wrabczyn', 'lad'],
     'Wyrzbenta attests that Stasco with his consort the lady Iachna, heirs of great Wrąbczyn, sold their third part '
     'of the estate, with all its uses, revenues and jurisdictions, to Abbot Jan and the abbey for 70 marks of grossi'),
    (30, 3, 1491, [1363, 3, 16], 'Ląd', 'contract', ['wrabczyn', 'lad'],
     'Wyrzbenta attests that Mikołaj, subdapifer of the bishop of Poznań, with his consort the honoured lady Czerska, '
     'sold the half of the lordship (medium dominium) in the village of great Wrąbczyn to Abbot Jan and his convent '
     'for 14 marks of grossi'),
    (31, 3, 1519, [1364, 4, 27], 'Ląd', 'attestation', ['wrabczyn', 'lad'],
     'Wyrzbenta attests that Dobrocha, heiress of great Wrąbczyn, sound and well by the grace of Jesus Christ, '
     'acknowledged publicly that all her substance, untamed beasts and cattle and all she has and possesses, is not '
     'hers but Abbot Jan of Ląd\'s and his monastery\'s, and that after her death neither children nor any of her '
     'friends shall have right or regard in it'),
]

SCANS = []
LEAF = {}
ROWS = []
DOCS = [(e[0], ['%04d_a' % e[0]]) for e in ENTRIES]


def read_file():
    """{(volume, number): [lines]} from the editor's file and the staged
    file of 2026-10-24, every line as it stands, blank lines left out."""
    out, vol, key = {}, None, None
    for source in (SOURCE, SOURCE2):
        for raw in io.open(source, encoding='utf-8-sig').read().replace('\r\n', '\n').split('\n'):
            m = re.match(r'^Volume (\d+):\s*$', raw)
            if m:
                vol, key = int(m.group(1)), None
                continue
            m = re.match(r'^\s*Dokument Nr (\d+)\s*$', raw)
            if m:
                key = (vol, int(m.group(1)))
                assert key not in out, key
                out[key] = [raw.strip()]
                continue
            if key and raw.strip():
                out[key].append(raw.rstrip())
    return out


def read_source():
    f = read_file()
    assert set(f) == {(e[1], e[2]) for e in ENTRIES}, sorted(set(f) ^ {(e[1], e[2]) for e in ENTRIES})
    return {(e[0], '%04d_a' % e[0]): f[(e[1], e[2])] for e in ENTRIES}


def write_rulings():
    """The parts of rulings.yml made from ENTRIES; the rest of the file is by hand."""
    path = os.path.join(UNIT_DIR, 'rulings.yml')
    s = io.open(path, encoding='utf-8').read()

    def block(name, indent, rows):
        nonlocal s
        body = ''.join('%s  %s\n' % (indent, r) for r in rows)
        s, n = re.subn(r'(?m)^%s%s:.*\n(?:%s  .*\n)*' % (indent, name, indent), '%s%s:\n%s' % (indent, name, body), s)
        assert n == 1, name
    block('read', '  ', ['"%d": [%d, %d, %d, "day"]   # %s, vol. %d no. %d' % (e[0], e[3][0], e[3][1], e[3][2], e[7][:60].replace('"', "'"), e[1], e[2])
                         for e in ENTRIES])
    block('overrides', '  ', ['"%d": "%s"' % (e[0], e[4]) for e in ENTRIES])
    block('doc_type', '  ', ['"%d": %s' % (e[0], e[5]) for e in ENTRIES])
    block('language', '  ', ['"%d": "la"' % e[0] for e in ENTRIES])
    block('estates', '  ', ['"%d": [%s]' % (e[0], ', '.join(e[6])) for e in ENTRIES])
    block('citation', '  ', ['"%d": {work: "%s", volume: %d, number: "%d", url: "%s"}' % (e[0], WORK, e[1], e[2], kdw_source.url(e[1]))
                             for e in ENTRIES])
    pages = ', '.join('"%04d_a"' % e[0] for e in ENTRIES)
    s = re.sub(r'  by_paragraph: \[.*\]\n', '  by_paragraph: [%s]\n' % pages, s)
    io.open(path, 'w', encoding='utf-8', newline='\n').write(s)


def english():
    import english_kdw
    return {e[0]: [english_kdw.ENGLISH[e[0]]] for e in ENTRIES}


def _summaries():
    try:
        import english_kdw
        return english_kdw.S, english_kdw.HOW
    except ImportError:
        return {}, ''


S, HOW = _summaries()

if __name__ == '__main__':
    if '--write' in sys.argv:
        write_rulings()
    courtbook.holding_main(globals())
