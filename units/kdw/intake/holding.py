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
- the estates of focus are from the editor's list of sixteen, by hand, per
  entry (ESTATES below): Zagórów, Skokum, Kopojno, Ląd, Szetlew, Szetlewek,
  Łukom, Trąbczyn, Wrąbczyn, Wrąbczynek, Świątniki, Oleśnica, Łazy, Adamierz,
  Drzewce, Przybysław. Łazy and Szetlewek are not in these entries;
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

# (document, volume, the Kodeks's number, [year, month, day], place of issue or "", doc_type, estates, why)
# In order of date. The date and place are the editors' heading's (volumes 5 to 11)
# or their regest's (1 to 3), which read the document's own dateline.
ENTRIES = [
    (1, 1, 20, [1173, 8, 31], 'Gniezno', 'donation', ['wrabczynek', 'lad'],
     'Mieszko gives "parvum Vronchin", Wrąbczynek, to the Cistercians of Ląd'),
    (2, 1, 222, [1240, 9, 30], '', 'donation', ['lad', 'zagorowo', 'skokum', 'kopojno', 'trabczyn', 'szetlew', 'lukom', 'wrabczyn'],
     'the tithes of Zagórów, Skokum, Kopojno, Trąbczyn, Szetlew, Łukom and Wrąbczyn given to Ląd; "s. l.", no place'),
    (3, 1, 238, [1243, 5, 4], 'Gniezno', 'donation', [],
     'the hospital of Gniezno given to the Holy Sepulchre of Miechów; none of the sixteen estates'),
    (4, 1, 393, [1261, 12, 10], 'Sechowa', 'confirmation', ['lad', 'szetlew', 'swiatniki', 'zagorowo', 'skokum', 'olesnica', 'kopojno'],
     'the possessions of Ląd confirmed: Szethowo (Szetlew), the Sanctuarii (Świątniki), Zagorowo, Skokom, Oleszyno, Capayn; '
     'place as written, the editors take it to be Czechowo or Szetlew'),
    (5, 1, 460, [1276, 3, 27], 'Dłusk', 'donation', ['trabczyn'],
     'Trąbczyn given to Count Nicholas, treasurer of Ląd'),
    (6, 6, 27, [1280, 10, 18], 'Kalisz', 'confirmation', ['lad', 'szetlew', 'swiatniki'],
     'the possessions of Ląd confirmed: Szechouo (probably Szetlew, note 7), Irgouo with the Sanctuarii (Świątniki, note 8)'),
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
]

SCANS = []
LEAF = {}
ROWS = []
DOCS = [(e[0], ['%04d_a' % e[0]]) for e in ENTRIES]


def read_file():
    """{(volume, number): [lines]} from the editor's file, every line as it stands, blank lines left out."""
    out, vol, key = {}, None, None
    for raw in io.open(SOURCE, encoding='utf-8-sig').read().replace('\r\n', '\n').split('\n'):
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
