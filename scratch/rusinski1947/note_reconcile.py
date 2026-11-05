# -*- coding: utf-8 -*-
"""Reconcile the note inventory against the 3x note-strip reads.

For each page: parse the strip text for its note starts (leading 1-2
digit numbers; the strip is one text block, so a start is a line or an
in-line 'N Capital' boundary after a sentence end) and compare the count
with structure2's parse. Disagreements are listed with both readings'
first words, for reconciliation by reading - the strip's higher
resolution wins where its chain is complete and structure2's is not;
where both are doubtful, the page goes to the spot sheet.
"""
import json, os, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'


def strip_notes(text):
    """Note starts from a strip TEXT. The print's note numbers 1-4 read
    as artifact glyphs ('!', '%', '*') even at 3x (the small ornamental
    digits); 5+ read as digits. A note start is a strip paragraph
    beginning with a 1-2 digit number OR an artifact glyph, followed by
    a capital/quote/siglum; numbers are assigned by POSITION, with the
    digit reads kept as num_read when present."""
    paras = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
    ART = '!%*+$§£|.,)»-'
    starts = []
    for p in paras:
        m = re.match(r'^(\d{1,2})[.,)]?\s+(\S.*)$', p, re.S)
        if m and re.match(r'[A-ZĄĆĘŁŃÓŚŹŻ„"(]', m.group(2)):
            starts.append({'read': int(m.group(1)), 'text': m.group(2)})
            continue
        if p[0] in ART and len(p) > 2:
            rest = p[1:].lstrip()
            if re.match(r'[A-ZĄĆĘŁŃÓŚŹŻ„"(]', rest):
                starts.append({'read': None, 'text': rest})
            continue
        m2 = re.match(r'^(\d{1,2})[.,)]?(\S.*)$', p, re.S)
        if m2 and re.match(r'[A-ZĄĆĘŁŃÓŚŹŻ„"(]', m2.group(2)):
            starts.append({'read': int(m2.group(1)), 'text': m2.group(2)})
    for i, s in enumerate(starts):
        s['num'] = i + 1
    return starts


def main():
    struct = json.load(open(os.path.join(OCR, 'structure2.json'),
                            encoding='utf-8'))
    out = {}
    agree = disagree = 0
    lines = []
    for n in sorted(struct):
        sp = os.path.join(OCR, 'notestrips', n + '.json')
        if not os.path.isfile(sp):
            continue
        d = json.load(open(sp, encoding='utf-8'))
        starts = strip_notes(d['pol'])
        starts2 = strip_notes(d['std'])
        # the two strip passes should agree; take the longer
        best = starts if len(starts) >= len(starts2) else starts2
        src = 'pol' if len(starts) >= len(starts2) else 'std'
        got = len(struct[n]['notes'])
        cnt = len(best)
        entry = {'strip_count': cnt, 'src': src,
                 'strip_firsts': [s['text'][:40] for s in best[:14]],
                 'reads': [s['read'] for s in best[:14]],
                 'struct_count': got}
        out[n] = entry
        if cnt == got:
            agree += 1
        else:
            disagree += 1
            lines.append((n, got, cnt, entry['strip_firsts'][:4]))
    with open(os.path.join(OCR, 'noteparse.json'), 'w', encoding='utf-8',
              newline='\n') as fh:
        json.dump(out, fh, ensure_ascii=False)
    print('agree:', agree, 'disagree:', disagree)
    for l in lines:
        print(l)


if __name__ == '__main__':
    main()
