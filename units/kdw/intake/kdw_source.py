# -*- coding: utf-8 -*-
"""Read one entry of the Kodeks Dyplomatyczny Wielkopolski from the digital library's text.

    python units/kdw/intake/kdw_source.py <volume> <number>      # print the entry

The Wielkopolska Digital Library (WBC) gives each volume of the Kodeks as one
HTML file, a proofed electronic text of the printed volume, not page images
and without the printed page numbers (2026-10-16). The eight volumes the
editor uses are saved in RAW as KDW_T<vv>_wbc<id>.html (VOLUMES below has the
links). In each, an entry is:

    Dokument Nr <n>                     the Kodeks's own number
    <place>, <date>                     the heading (volumes 6 to 11; in 1 to 5 the date is in the regest)
    [regest]                            the modern editors' summary (Latin in 1 to 5, Polish in 6 to 11)
    [sources]                           manuscripts and earlier editions (Kop., Or., Wyd., Reg. ...)
    [text]                              the document, in blue
    [notes]                             the editors' notes and their identifications of places

entry() returns these parts as plain text. Footnote numbers in the text are
given as "^1"; the page marks of the manuscript the editors printed from
("[s. 443]") are kept as they stand. Nothing here decides what the edition
transcribes: that is the holding's script.

The numbering runs 1-2073 through volumes 1 to 4, starts again at 1 in volume
5, and runs 1-2023 through volumes 6 to 11; an entry is therefore always
named by volume and number.
"""
import html
import io
import os
import re
import sys

RAW = r"J:\Documents\Archive\Genealogy\References\Kodeks Dyplomatyczny Wielkopolski"

# volume: (WBC edition id, published, the archive's title in WBC, years, numbers)
VOLUMES = {
    1: (20061, 1877, 'Kodeks Dyplomatyczny Wielkopolski T.1 Zawiera numera 1-616 lata 984-1287', '984-1287', '1-616'),
    2: (20067, 1878, 'Kodeks Dyplomatyczny Wielkopolski T.2 Zawiera numera 617-1292 lata 1288-1349', '1288-1349', '617-1292'),
    3: (20085, 1879, 'Kodeks Dyplomatyczny Wielkopolski T.3 Zawiera numera 1293-2053 lata 1350-1399', '1350-1399', '1293-2053'),
    5: (20103, 1908, 'Kodeks Dyplomatyczny Wielkopolski T.5 Zawierający dokumenta z lat 1400-1444', '1400-1444', '1-738'),
    6: (20109, 1982, 'Kodeks Dyplomatyczny Wielkopolski T.6 Zawiera dokumenty nr 1-400 z lat 1174-1400', '1174-1400', '1-400'),
    7: (20111, 1985, 'Kodeks Dyplomatyczny Wielkopolski T.7 Zawiera dokumenty nr 401-773 z lat 1401-1415', '1401-1415', '401-773'),
    10: (20117, 1993, 'Kodeks Dyplomatyczny Wielkopolski T.10 Zawiera dokumenty nr 1381-1699 z lat 1435-1444', '1435-1444', '1381-1699'),
    11: (20119, 1999, 'Kodeks Dyplomatyczny Wielkopolski T.11 Zawiera suplementy (dokumenty nr 1700-2023 z lat 1225-1444) '
                      'oraz erratę i indeksy do tomów VI-XI', '1225-1444', '1700-2023'),
}


def url(volume):
    return 'https://www.wbc.poznan.pl/dlibra/doccontent?id=%d' % VOLUMES[volume][0]


def _file(volume):
    return os.path.join(RAW, 'KDW_T%02d_wbc%d.html' % (volume, VOLUMES[volume][0]))


_CACHE = {}


def _volume(volume):
    if volume not in _CACHE:
        s = io.open(_file(volume), encoding='utf-8', errors='replace').read()
        parts = re.split(r'Dokument Nr\s*<font color="blue">\s*([^<]*?)\s*</font>\s*</DIV>', s)
        _CACHE[volume] = {parts[i].strip(): parts[i + 1] for i in range(1, len(parts) - 1, 2)}
    return _CACHE[volume]


def _plain(fragment):
    t = re.sub(r'<sup>\s*<font color="red">\s*([^<]*?)\s*</font>\s*</sup>', lambda m: '^' + m.group(1) if m.group(1) else '', fragment)
    t = re.sub(r'<br\s*/?>', '\n', t, flags=re.I)
    t = re.sub(r'<[^>]+>', '', t)
    t = html.unescape(t)
    lines = [re.sub(r'[ \t\r]+', ' ', l).strip() for l in t.split('\n')]
    return '\n'.join(l for l in lines if l)


def entry(volume, number):
    """The parts of one entry: heading, regest, sources, text, notes (plain text, '' where absent)."""
    raw = _volume(volume).get(str(number))
    if raw is None:
        raise KeyError('no entry %s in volume %s' % (number, volume))
    raw = re.split(r'<p>\s*<hr>\s*</p>', raw)[0]
    out = {'volume': volume, 'number': str(number), 'heading': '', 'regest': '', 'sources': '', 'text': '', 'notes': ''}
    m = re.search(r'<DIV style="display:block; font-size:14pt; margin-top:20px">(.*?)</DIV>', raw, re.S | re.I)
    if m:
        out['heading'] = _plain(m.group(1))
    m = re.search(r'<DIV STYLE="background-color:#EEEEAA">(.*?)</DIV>', raw, re.S)
    if m:
        out['regest'] = _plain(m.group(1))
    m = re.search(r'<LIST[^>]*>(.*?)</LIST>', raw, re.S)
    if m:
        out['sources'] = _plain(m.group(1))
    texts = re.findall(r'<DIV STYLE="color: blue; display: block;">(.*?)</DIV>', raw, re.S)
    out['text'] = '\n\n'.join(_plain(t) for t in texts)
    notes = re.findall(r'<DIV STYLE="color: brown; display: block;">(.*?)</DIV>', raw, re.S)
    out['notes'] = '\n'.join(_plain(n) for n in notes)
    return out


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    e = entry(int(sys.argv[1]), sys.argv[2])
    for k in ('heading', 'regest', 'sources', 'text', 'notes'):
        print('== %s ==\n%s\n' % (k, e[k]))
