# -*- coding: utf-8 -*-
"""Stage the ten Kodeks entries the gazetteer cites and the holding lacks.

Reads each entry from the WBC HTML on the editor's drive (units/kdw/intake/
kdw_source.py) and from Igor's independent conversion of the same HTML
(C:\\Users\\Tersnaus\\Downloads\\polish-place-name-sources\\sources\\kdw\\),
and writes both readings beside each other for a line-by-line comparison.

    python units/kdw/intake/stage_missing.py          # compare, print the report
    python units/kdw/intake/stage_missing.py --write  # also write intake/kodeks_missing.txt

The volumes 1 to 3 have no heading in the WBC's text (the date is in the
regest) and no glued footnote markers (their last line is the editors' list
of place names), so an entry's lines are: the marker line, the regest, the
sources, a blank line, the text, a blank line, the notes.
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
import kdw_source  # noqa: E402

IGOR = r'C:\Users\Tersnaus\Downloads\polish-place-name-sources\sources\kdw'

# (volume, number) in the Kodeks's own numbering; ids 22 to 31 follow the
# holding's existing 21, by date below.
WANTED = [(1, 228), (1, 535), (2, 672), (2, 795), (2, 1044),
          (3, 1363), (3, 1478), (3, 1490), (3, 1491), (3, 1519)]


def lines_from_parts(e):
    # the kodeks.txt convention: the marker line, then one line per part
    out = [' Dokument Nr %s' % e['number']]

    def one_line(s):
        return ' '.join(s.split())

    parts = {}
    for k in ('regest', 'sources', 'text', 'notes'):
        parts[k] = one_line(e[k]) if e[k] else ''
    # the WBC's HTML carries the editors' note twice for these entries: the
    # blue text div ends with a copy of the brown note div's content, and
    # the note itself is not repeated in the printed entry (the editor's
    # kodeks.txt has it once). Strip the copy from the text's tail.
    if parts['notes'] and parts['text'].endswith(parts['notes']):
        parts['text'] = parts['text'][:-len(parts['notes'])].rstrip()
    for k in ('regest', 'sources', 'text', 'notes'):
        if parts[k]:
            out.append(parts[k])
    return out


def igor_lines(volume, number):
    path = os.path.join(IGOR, 'kdw%02d.md' % volume)
    s = io.open(path, encoding='utf-8').read()
    # a volume's file may carry a charter more than once: volumes 6 to 11
    # end with their own Polish regest index, and volume 1 runs a first
    # sequence of regests alone before the full entries. The full entry is
    # the longest match, and it alone is compared.
    pat = r'(?ms)^## Dokument Nr %d\s*$(.*?)(?=^## Dokument Nr |\Z)' % number
    hits = re.findall(pat, s)
    if not hits:
        raise KeyError('no entry %s in %s' % (number, path))
    body = max(hits, key=len)
    body = re.sub(r'<!--.*?-->\n?', '', body)
    body = re.sub(r'(?m)^> ?', '', body)
    body = body.replace('*', '')
    lines = [l.rstrip() for l in body.split('\n')]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def norm(line):
    """Loosen what the two conversions may differ in honestly: the marker
    line, the spaces round punctuation, the bold markers."""
    t = line.strip()
    t = re.sub(r'^Dokument Nr \d+$', 'MARK', t)
    t = re.sub(r'\*\*', '', t)
    t = re.sub(r'\s+([,;:.])', r'\1', t)
    t = re.sub(r'\s+', ' ', t)
    return t


def flatten(lines):
    """One string with every space gone: the two conversions break their
    lines and glue their words differently, so only the characters count."""
    return ''.join(norm(l) for l in lines if l.strip()).replace(' ', '')


def main():
    write = '--write' in sys.argv
    report = []
    staged = []
    for volume, number in WANTED:
        e = kdw_source.entry(volume, number)
        ours = lines_from_parts(e)
        theirs = igor_lines(volume, number)
        staged.append((volume, number, ours))
        # the marker line " Dokument Nr N" is the staged file's own marker,
        # not the WBC's text: it is dropped for the comparison
        ours_body = [l for l in ours if not re.match(r'^\s*Dokument Nr \d+$', l)]
        same = flatten(ours_body) == flatten(theirs)
        report.append('vol. %d no. %d: ours %d, Igor %d characters, %s'
                      % (volume, number, len(flatten(ours_body)), len(flatten(theirs)),
                         'agree' if same else 'DIFFER'))
        if not same:
            a, b = flatten(ours_body), flatten(theirs)
            i = 0
            while i < min(len(a), len(b)) and a[i] == b[i]:
                i += 1
            report.append('  first difference at character %d:' % i)
            report.append('   wbc : ...%s' % a[max(0, i - 40):i + 140])
            report.append('   igor: ...%s' % b[max(0, i - 40):i + 140])
    print('\n'.join(report))
    if write:
        out = []
        volume = None
        for v, n, lines in staged:
            if v != volume:
                out.append('Volume %d:' % v)
                volume = v
            out.extend(lines)
            out.append('')
        path = os.path.join(HERE, 'kodeks_missing.txt')
        io.open(path, 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
        print('wrote', path)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
