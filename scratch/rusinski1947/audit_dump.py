# -*- coding: utf-8 -*-
"""Marker audit dump for the short pages: every candidate token that
could be a missed footnote marker, from BOTH the line-pass reads and
the page-pass (structure2) lines, with context - plus the page's note
defs (num + first words) so each marker can be paired semantically.

The editor's demonstrated pattern: the print's inline full-size markers
fuse with the preceding token in OCR ('608' = '60' + marker 6, '702' =
'70' + marker 2, 'lata %' = 'lata' + marker 3) or become artifact
glyphs ('$' = marker 4)."""
import json, os, re, sys

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
s = json.load(open(os.path.join(OCR, 'structure2.json'), encoding='utf-8'))
mk = json.load(open(os.path.join(OCR, 'markers.json'), encoding='utf-8'))

DIGITISH = re.compile(r'(?:^|[^\w])(\d{1,4}[.,;:%*?]*|[^\W\d_][\wąćęłńóśźż.\-]*\d{1,2}[.,;:*?]*|[A-ZŁ]{1,3}\d{0,2}|[*$§£|?][.,;:]?)')


def flags(text):
    out = []
    toks = text.split()
    for i, w in enumerate(toks):
        ctx = ' '.join(toks[max(0, i - 4):i + 3])
        if re.search(r'\d', w) and len(re.sub(r'\D', '', w)) <= 4 \
                and not re.fullmatch(r'\d{3,4}', w) \
                and not re.fullmatch(r'(1[678]\d\d|18\d\d)', w):
            out.append((w, ctx))
        elif re.fullmatch(r'[*$§£|?]+[.,;:»"]?', w):
            out.append((w, ctx))
    return out


pages = sys.argv[1:]
if not pages:
    want_pages = [n for n in sorted(s) if len(mk.get(n, [])) < len(s[n]['notes'])]
else:
    want_pages = pages

for n in want_pages:
    page = s[n]
    notes = page['notes']
    N = len(notes)
    found = mk.get(n, [])
    print('=' * 20, '%s  found %d/%d' % (n, len(found), N))
    print('  DEFS:', ' | '.join(
        '%d:%s' % (x['num'], re.sub(r'\s+', ' ', x['text'])[:44])
        for x in notes))
    ft = min(x['top'] for x in notes)
    lp = []
    p = os.path.join(OCR, 'lines', n + '.json')
    if os.path.isfile(p):
        lp = json.load(open(p, encoding='utf-8'))
    for l in page['lines']:
        if l['top'] >= ft:
            continue
        txt = l['text']
        fl = flags(txt)
        if not fl:
            continue
        near = [r for r in lp if abs(r['top'] - l['top']) <= 50]
        line_ctx = ' '.join(r.get('line_pol') or '' for r in near)[:130]
        line_ctx2 = ' '.join(r.get('line_std') or '' for r in near)[:130]
        print('  L%5d | %s' % (l['top'], txt[:88]))
        for w, ctx in fl:
            print('        tok %-12s ctx: %s' % (w, ctx[:70]))
        if line_ctx.strip() and line_ctx.strip() != txt[:130]:
            print('        lp-pol: %s' % line_ctx)
        if line_ctx2.strip():
            print('        lp-std: %s' % line_ctx2)
    print()
