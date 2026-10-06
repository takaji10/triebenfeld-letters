# -*- coding: utf-8 -*-
"""The editor's English translation of APP 53/17/0/-/Konin Gr.145, cut to the
edition's pages and written as doc1.yml.

    python units/app53170koningr145/intake/translation/build_doc1.py            # check only
    python units/app53170koningr145/intake/translation/build_doc1.py --write

The English is the editor's own, made before the holding came into the
edition ("Relationes-oblatae [protocollon] 1776 ... - English Translation.md",
beside the scans). It is not translated again. This script only carries it
over:

- The text between the heading "Oblata Frame" and the heading "Glossary" is
  the translation. The outline, the translator's notes and the glossary before
  and after it are the editor's apparatus; they are used in about.md and
  notes.md, not here.
- The file marks each page by its leaf, "[655]" and "[655v]", as the Polish
  does. Leaf N recto is page <N>_a2, leaf N verso page <N+1>_a1; the title
  stands before "[655]" and is page 0654_a2.
- Markdown is taken off (bold, italics, escapes, rules). A heading of the
  editor's becomes a line in square brackets, "[Section 2: ...]", because it
  is theirs and not the record's. A bullet becomes a line of its own.
- The twenty footnotes are the translator's notes. Each is set after the
  paragraph it belongs to as "[Translator's note: ...]".
- "[see Glossary]" is dropped: the edition marks its own glossary words.
- A doubt the editor marked "[word?]" becomes "[uncertain: word]", the
  edition's form. "[[place of the family seal]]" becomes "[place of the
  family seal]".
- FIXES are the few places where the Polish was corrected against the scan
  (intake/corrections.py) and the English had to follow.
- FIXES_FULL (fixes_full.py) are the changes that follow the full check of
  all 122 pages: the dropped phrases restored, and one paragraph the
  English lacked.
"""
import glob
import io
import os
import re
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fixes_full import FIXES_FULL  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = r"J:\Documents\Archive\Genealogy\References\Poznań State Archives\Relationes-oblatae [protocollon] 1776 (53.17.0.-.Konin Gr.145)"

# (page, English as it stood, English after the Polish was corrected, why)
FIXES = [
    ('0673_a2',
     'stretching toward the corduroy crossings for several staj. And likewise he showed',
     'stretching toward the corduroy crossings for several staj, occupying and taking in the whole Lusnia woodland. '
     'And likewise he showed',
     'six Polish words restored from the scan: "las cały Lusnie zajmujących i zabierających"'),
    ('0656_a2',
     'Secretary of the General Confederation and Ordinary Sejm of the Crown',
     'Secretary of the General Confederation and Extraordinary Sejm of the Crown',
     'the Latin on the scan has "Comitiorum extra Ordinariorum"'),
    ('0658_a1',
     'Radziwiłł, Marshal, Sword-bearer, of the General',
     'Radziwiłł, [uncertain: Marshal, Sword-bearer], of the General',
     'the Polish marks its expansion of "MM." as doubtful, "[Marszałek Miecznik?]"; the mark is carried over'),
    ('0654_a2',
     '1776',
     '1776\n\nAt the Brest Kuyavia Municipal Court',
     'the third line of the title page, "In Castro Brestensi Cujaviae", added to the Polish from the scan'),
]
# Where the English breaks a page far from where the Polish does. The editor's
# file ends each page at the end of a sentence, so its page marks stand a few
# words, sometimes a few lines, after the Polish ones; that is left as it is.
# In two places the mark stands most of a page late, and the English from the
# given words onward is moved to the head of the next page.
#   (page number in the document, the first words that belong to the next page)
MOVES = [
    (27, 'came a greater or lesser distance to an old wolf pit'),
    (107, 'the resolution and conclusion of that boundary to the twenty-first day of May'),
]
# Applied to every page: a name corrected on the scan.
EVERYWHERE = [
    ('Janosza Drewnowski', 'Junosza Drewnowski', 'the scan has "Junosza"'),
]


def page_id(leaf):
    if leaf.endswith('v'):
        return '%04d_a1' % (int(leaf[:-1]) + 1)
    return '%04d_a2' % int(leaf)


def clean(line, notes):
    line = line.rstrip()
    if re.fullmatch(r'-{3,}', line.strip()):
        return None
    m = re.match(r'^(#+)\s*(.*)$', line)
    if m:
        t = re.sub(r'[*_]', '', m.group(2)).strip()
        return '[' + t + ']'
    line = re.sub(r'^\s*\*\s+', '', line)                 # a bullet
    line = re.sub(r'\\([\[\]\.\-\*_#~()])', r'\1', line)   # escapes
    line = line.replace('**', '').replace('*', '')
    line = line.replace('[[', '[').replace(']]', ']')
    line = re.sub(r'\s*\[see Glossary\]', '', line)
    line = re.sub(r'([^\s\[\]]+)\[\?\]', lambda k: '[uncertain: %s]' % k.group(1), line)   # word[?]
    line = re.sub(r'\[([^\[\]]{1,60})\?\]', lambda k: '[uncertain: %s]' % k.group(1).strip(), line)
    refs = re.findall(r'\[\^(\d+)\]', line)
    line = re.sub(r'\[\^\d+\]', '', line)
    line = re.sub(r'\s+', ' ', line).strip()
    out = [line] if line else []
    for r in refs:
        out.append("[Translator's note: %s]" % notes[r])
    return out


def build():
    f = glob.glob(os.path.join(glob.escape(RAW), '*English Translation.md'))
    assert len(f) == 1, f
    s = io.open(f[0], encoding='utf-8-sig').read().replace('\r\n', '\n')
    notes = {}
    for m in re.finditer(r'(?m)^\[\^(\d+)\]:\s*(.*)$', s):
        t = re.sub(r'\\([\[\]\.\-\*_#~()])', r'\1', m.group(2)).replace('*', '')
        notes[m.group(1)] = re.sub(r'\s+', ' ', t).strip()
    s = re.sub(r'(?m)^\[\^\d+\]:.*\n?', '', s)
    a, b = s.index('# **Oblata Frame'), s.index('# **Glossary**')
    body = s[a:b]
    parts = re.split(r'(?m)^\\\[(\d+v?)\\\]\s*$', body)
    chunks = [('0654_a2', parts[0])] + [(page_id(l), t) for l, t in zip(parts[1::2], parts[2::2])]
    pages = []
    for pid, text in chunks:
        lines = []
        for raw in text.split('\n'):
            if not raw.strip():
                continue
            got = clean(raw, notes)
            if got is None:
                continue
            lines.extend([got] if isinstance(got, str) else got)
        pages.append([pid, lines])
    used = set()
    for pid, lines in pages:
        for i, l in enumerate(lines):
            for old, new, _ in EVERYWHERE:
                if old in l:
                    lines[i] = l = l.replace(old, new)
                    used.add(old)
    for pid, old, new, _ in FIXES:
        hit = [(p, i) for p, lines in pages if p == pid for i, l in enumerate(lines) if old in l]
        assert len(hit) == 1, (pid, old[:40], len(hit))
        p, i = hit[0]
        lines = dict((x[0], x[1]) for x in pages)[p]
        lines[i] = lines[i].replace(old, new)
    assert used == {o for o, _, _ in EVERYWHERE}, used
    for n, start in MOVES:
        lines, nxt = pages[n - 1][1], pages[n][1]
        hit = [i for i, l in enumerate(lines) if start in l]
        assert len(hit) == 1, (n, start, len(hit))
        i = hit[0]
        k = lines[i].index(start)
        moved = [lines[i][k:]] + lines[i + 1:]
        lines[i] = lines[i][:k].rstrip()
        del lines[i + 1:]
        if not lines[i]:
            del lines[i]
        nxt[:0] = moved
    # What the full check of the Polish changes in the English (fixes_full.py).
    # Searched through the whole text: the English page marks do not sit
    # exactly where the Polish ones do. A fix may cross a paragraph.
    for old, new, leaf, why in FIXES_FULL:
        hits = [k for k, (pid, lines) in enumerate(pages) if old in '\n\n'.join(lines)]
        assert len(hits) == 1, ('full-check fix, leaf %s: found on %d pages: %s' % (leaf, len(hits), old[:60]))
        k = hits[0]
        joined = '\n\n'.join(pages[k][1])
        assert joined.count(old) == 1, (leaf, old[:60])
        pages[k][1][:] = joined.replace(old, new).split('\n\n')
    return pages, notes


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    pages, notes = build()
    ids = [p for p, _ in pages]
    print(len(pages), 'pages;', sum(len(' '.join(l).split()) for _, l in pages), 'words;', len(notes), "translator's notes;",
          sum(1 for _, l in pages for x in l if x.startswith('[Section') or x.startswith('[Oblata') or x.startswith('[The ') or x.startswith('[Warsaw')),
          'headings')
    empty = [p for p, l in pages if not l]
    print('pages with no English:', empty)
    if '--write' not in sys.argv:
        for p, l in pages[:2]:
            print(p, l)
        return
    doc = {'pages': []}
    for n, (pid, lines) in enumerate(pages, 1):
        en = '\n\n'.join(lines)
        doc['pages'].append({
            'page': n,
            'confidence': 'high',
            'marker_count': len(re.findall(r'\[(?:uncertain: |illegible|text lost)', en)),
            'en': en,
            'names': [],
            'numbers': [],
            'flagged': [],
        })
    with io.open(os.path.join(HERE, 'doc1.yml'), 'w', encoding='utf-8', newline='\n') as f:
        yaml.safe_dump(doc, f, allow_unicode=True, sort_keys=False, width=100)
    print('wrote doc1.yml; page ids in order:', ids[0], '...', ids[-1])


if __name__ == '__main__':
    main()
