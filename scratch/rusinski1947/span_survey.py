# -*- coding: utf-8 -*-
"""Survey the spanning-note pattern: small-type lines ABOVE a page's
first detected note top (below the last body-type line). The print
continues the previous page's last note at the top of the note block;
the parse assigned those lines to the body.

Survey: for every note page, list the small-type lines above the first
note top; flag pages where such lines exist and the PREVIOUS page's
last note ends mid-sentence."""
import json, os, re, difflib

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
s = json.load(open(os.path.join(OCR, 'structure2.json'),
                  encoding='utf-8'))
ORDER = sorted(s)


def fold(x):
    return re.sub(r'[^a-ząćęłńóśźż0-9]', '', x.lower())


rows = []
for i, n in enumerate(ORDER):
    page = s[n]
    notes = page['notes']
    if not notes:
        continue
    first_top = min(x['top'] for x in notes)
    lines = page['lines']
    # the type reference: the page's top-third 90th pct
    top3 = lines[:max(1, len(lines) // 3)]
    hs = sorted(l['h'] for l in top3 if l['h'] >= 30)
    BH = hs[min(len(hs) - 1, int(0.9 * len(hs)))] if hs else 80
    # lines above first_top that are small-type
    lead = [l for l in lines if l['top'] < first_top
            and l['h'] <= 0.88 * BH and l['h'] >= 25]
    if not lead:
        continue
    # the last small-type line before a run of body-type? simpler: the
    # lead lines form a CONTIGUOUS tail above first_top
    tail = []
    for l in reversed(lines):
        if l['top'] >= first_top:
            continue
        if l['h'] <= 0.88 * BH and l['h'] >= 25:
            tail.append(l)
        else:
            break
    tail.reverse()
    if len(tail) < 1:
        continue
    # sanity: the previous note page's LAST note should end mid-sentence
    prevnote = None
    for j in range(i - 1, -1, -1):
        if s[ORDER[j]]['notes']:
            pn = ORDER[j]
            prevnote = s[pn]['notes'][-1]
            break
    ends_mid = False
    fit = 0.0
    if prevnote:
        t = prevnote['text'].rstrip()
        ends_mid = not re.search(r'[.!?»”]\s*$', t)
        if ends_mid and tail:
            f1 = fold(t)[-40:]
            f2 = fold(tail[0]['text'])[:40]
            fit = difflib.SequenceMatcher(None, f1, f2).ratio()
    rows.append((n, len(tail), tail[0]['top'], ends_mid, round(fit, 2),
                 tail[0]['text'][:50]))

print('pages with small-type lead-in above first note:', len(rows))
for r in rows:
    print('scan %s: %d lead lines (top %d) | prev ends mid: %s | fit %.2f | %s'
          % r)
