# -*- coding: utf-8 -*-
"""Cell noise triage: score every text cell of annex_md.json; flag the
noisy ones with a reason. Also scans the notes for the catalogued
strip-artifact classes."""
import json, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
md = json.load(open(OCR + r'\annex_md.json', encoding='utf-8'))

JUNK = re.compile(r'[=<>_%~§]{1}|—{2,}|--|\*{2,}')
# a cell is noise when: junk chars in word context, or impossible
# token shapes
SIGLUM = re.compile(r'^(AW\.|Rel\.|AGH|AM\.|Dom\.|Tp\.|Tod\.|Tołł\.|'
                    r'Verz|Kl\.|Kat\.|Q\b|G\b|GE\b|MGd?\b|MP\b|Szk\.|'
                    r'Kośc\.|Lustr\.|Inser\.|Decr\.|Werner|Goldmann|'
                    r'Cieplucha|Rutkowski|Bór\.|VO\b|OWK|O\s*83|TKS|'
                    r'Tb\.|St\.|ME\b|M\.|Parochia|ZHGP|Bir|Kniat|'
                    r'Sonder|Inscr\.|Repertorium|tamże|Por\.)')
DATE = re.compile(r'^\d{1,2}\s*[XIV]+\s*\d{3,4}$')
ROMAN = re.compile(r'^[XIV]+$')

def tok_score(tok):
    """0 = fine, 1 = suspect, 2 = junk."""
    core = tok.strip(' .,;:()[]|')
    if not core:
        return 0
    if re.fullmatch(r'[—\-=_*%<>"\'~.]+', core):
        return 2
    letters = sum(1 for c in core if c.isalpha())
    if letters and letters < len(core) * 0.55:
        return 2
    if JUNK.search(core):
        return 2
    return 0

flagged = []
for n in sorted(md):
    for r in md[n]['rows']:
        for ci, cell in enumerate(r['cells'][1:], start=1):
            if not cell or cell == '—':
                continue
            toks = cell.split(' ')
            bad = [t for t in toks if tok_score(t) == 2]
            if bad:
                flagged.append((n, r['num'], ci, cell, bad))
            elif ci == 7 and not DATE.match(cell.replace('  ', ' ')) \
                    and not ROMAN.match(cell):
                # the data column: a date or a bare year/roman
                if not re.match(r'^\d{4}$', cell.strip()) \
                        and not re.match(r'^\d{1,2}\s*[IVX]+', cell):
                    flagged.append((n, r['num'], ci, cell, ['DATE?']))
            elif ci == 6 and not SIGLUM.match(cell):
                flagged.append((n, r['num'], ci, cell, ['SIGLUM?']))
print('flagged cells:', len(flagged))
from collections import Counter
print('by column:', Counter(ci for _, _, ci, _, _ in flagged))
print('by sheet:', Counter(n for n, _, _, _, _ in flagged))
with open(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\noise1.txt',
          'w', encoding='utf-8') as fh:
    for f in flagged:
        fh.write('%s r%s c%d %r bad=%r\n' % f)
print('written noise1.txt')
