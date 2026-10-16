# -*- coding: utf-8 -*-
"""Kodeks Dyplomatyczny Wielkopolski: the entries the editor names, as documents of one holding.

    python units/kdw/intake/holding.py               # check: every entry found, the corpus agrees
    ... --write       page files and corpus.txt from the entries (and the citations in rulings.yml)
    ... --english     write translation/doc<N>.yml from intake/english_kdw.py
    ... --cache       put them into the translation cache
    ... --summaries   write the summaries S (intake/english_kdw.py) everywhere they are kept

How the holding is made (the editor, 2026-10-16):
- one holding for all entries, whatever the volume; each entry is one document,
  numbered 1, 2, 3 ... in the order the editor gives them (ENTRIES). The
  Kodeks's own volume and number are the document's citation, shown on its page
  (rulings.yml `documents: citation:`, written by --write);
- text only: the WBC has no page images of the Kodeks, only its electronic
  text (intake/kdw_source.py). Each document is one page, id NNNN_a with NNNN
  the document's number, and has no image;
- the whole entry is the transcription, one paragraph to a line
  (pages: by_paragraph): the Kodeks's number ("Nr 198"), the editors' heading,
  their summary, their list of sources, the text, their notes. Nothing is
  corrected: what the electronic text has is what the printed volume has, as
  far as the library's proofing went.
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

# (document number, volume, the Kodeks's number). The editor gives them; add at the end.
ENTRIES = [
]

SCANS = []
LEAF = {}
ROWS = []
DOCS = [(n, ['%04d_a' % n]) for n, _v, _k in ENTRIES]


def paragraphs(volume, number):
    """The whole entry, one paragraph to a line, in the order of the volume."""
    e = kdw_source.entry(volume, number)
    out = ['Nr %s' % e['number']]
    for part in ('heading', 'regest', 'sources', 'text', 'notes'):
        txt = e[part].strip()
        if not txt:
            continue
        # a paragraph of the electronic text may be wrapped over several lines: join them
        for para in re.split(r'\n\s*\n', txt):
            if part in ('sources', 'notes'):
                out.extend(l.strip() for l in para.split('\n') if l.strip())
            else:
                out.append(re.sub(r'\s*\n\s*', ' ', para).strip())
    return out


def read_source():
    return {(n, '%04d_a' % n): paragraphs(v, k) for n, v, k in ENTRIES}


def citations():
    return {str(n): {'work': WORK, 'volume': v, 'number': str(k)} for n, v, k in ENTRIES}


def write_citations():
    """The `documents: citation:` block of rulings.yml, written from ENTRIES (the rest of the file is by hand)."""
    path = os.path.join(UNIT_DIR, 'rulings.yml')
    s = io.open(path, encoding='utf-8').read()
    block = '  citation:\n' + ''.join(
        '    "%s": {work: "%s", volume: %d, number: "%s", url: "%s"}\n' % (n, WORK, v, k, kdw_source.url(v))
        for n, v, k in ENTRIES)
    s = re.sub(r'  citation:\n(?:    .*\n)*', block, s)
    pages = ', '.join('"%04d_a"' % n for n, _v, _k in ENTRIES)
    s = re.sub(r'  by_paragraph: \[.*\]\n', '  by_paragraph: [%s]\n' % pages, s)
    io.open(path, 'w', encoding='utf-8', newline='\n').write(s)


def english():
    import english_kdw
    return {n: [english_kdw.ENGLISH[n]] for n, _v, _k in ENTRIES}


def _summaries():
    try:
        import english_kdw
        return english_kdw.S, english_kdw.HOW
    except ImportError:
        return {}, ''


S, HOW = _summaries()

if __name__ == '__main__':
    if '--write' in sys.argv:
        write_citations()
    courtbook.holding_main(globals())
