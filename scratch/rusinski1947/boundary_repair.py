# -*- coding: utf-8 -*-
"""Boundary-merge repair: find pages where the note block's top sits
BELOW the true first-note line (the note's opening then leaks into the
body - the readers' 'footnote merged into running text' class).

Detection: the first note's opening (folded, from the strip - the text
of record) is matched against the BODY lines (lines above the parsed
note top). A strong match (ratio >= 0.7) means the true boundary is at
that body line: lift the first note's top to it. Also the same check
for EVERY note (a mid-block note estimated too low leaks ITS opening
into the previous note's text? no - into the body only if it is note
1; later notes leak into the previous note's text, which the strip
text of record already handles correctly - only note 1's boundary
matters for the body cut).

Writes structure5.json (structure4 with corrected first-note tops) and
the repair report.
"""
import json, os, re, difflib

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'


def fold(s):
    return re.sub(r'[^a-ząćęłńóśźż0-9]', '', s.lower())


def main():
    s = json.load(open(os.path.join(OCR, 'structure4.json'),
                       encoding='utf-8'))
    repairs = []
    for n in sorted(s):
        notes = s[n]['notes']
        if not notes:
            continue
        note_top = min(x['top'] for x in notes)
        body = [l for l in s[n]['lines'] if l['top'] < note_top]
        if not body:
            continue
        f1 = fold(notes[0]['text'])[:30]
        if len(f1) < 10:
            continue
        # scan the last 6 body lines for the note's opening
        for l in body[-6:]:
            fl = fold(l['text'])[:30]
            r = difflib.SequenceMatcher(None, fl, f1).ratio()
            if r >= 0.7:
                repairs.append((n, notes[0]['num'], notes[0]['top'],
                                l['top'], round(r, 2)))
                notes[0]['top'] = l['top']
                break
    with open(os.path.join(OCR, 'structure5.json'), 'w',
              encoding='utf-8', newline='\n') as fh:
        json.dump(s, fh, ensure_ascii=False)
    print('boundary repairs:', len(repairs))
    for r in repairs:
        print('  scan %s note %d: top %d -> %d (r=%.2f)' % r)


if __name__ == '__main__':
    main()
