# -*- coding: utf-8 -*-
"""Note text of record = the wide strip's line-level text (3x, psm 4).

The per-note CROPS proved geometrically fragile: a matched top off by
one line makes the crop catch the neighbouring note or body text, and
the crop-vs-structure test then rejects on geometry, not content. The
strip's text does not depend on crop geometry: psm 4 preserves the
print's line breaks, and the note's text is its lines from the matched
start to the next start.

Verification is therefore against the PAGE PASS (an independent scale):
the v1 lines between the note's top and the next note's top are joined
and compared with the strip text (first-words + rough ratio). The strip
text stands everywhere; disagreements are listed for reading - they
are either strip errors, page-pass mangling, or a boundary mismatch,
and each is decided by looking at the strip's own lines.

Output: structure4.json (text of record, src=strip3x) + note_verify.csv
(the disagreements, strip vs page).
"""
import json, os, re, difflib, csv

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'


def fold(s):
    return re.sub(r'[^a-ząćęłńóśźż0-9]', '', s.lower())


def words3(text):
    ws = [fold(t) for t in
          re.findall(r'[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż0-9]+', text)][:3]
    return ' '.join(ws)


def main():
    struct = json.load(open(os.path.join(OCR, 'structure2.json'),
                            encoding='utf-8'))
    rows = []
    out = {}
    ok = disagree = 0
    for n in sorted(struct):
        notes = struct[n]['notes']
        if not notes:
            out[n] = struct[n]
            continue
        # the REBUILT lines (structure2's own) share the same lineation
        # as the note tops; v1's top-sort lineation differs by a line on
        # warped pages and misaligned every range comparison
        v1lines = sorted(struct[n]['lines'], key=lambda l: l['top'])
        new = []
        for i, note in enumerate(notes):
            nxt = notes[i + 1]['top'] if i + 1 < len(notes) else 10 ** 9
            page_range = ' '.join(
                l['text'] for l in v1lines
                if note['top'] - 10 <= l['top'] < nxt - 10)
            strip_text = re.sub(
                r'^[\d!%*+$§£|.,)»\-—–?\s]+(?=[A-ZĄĆĘŁŃÓŚŹŻ„"(])', '',
                note['text']).strip()
            # the page range keeps the print's leading note number and
            # OCR junk tokens ('a Np.', 'Ul: 2', 'Ooz———— 1'); strip
            # leading non-word tokens before comparing
            page_clean = re.sub(
                r'^(?:[\d!%*+$§£|.,)»\-—–?\s]|[^A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż0-9]){1,6}'
                r'(?=[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż„"(])', '', page_range).strip()
            first_ok = (words3(strip_text) and words3(page_clean)
                        and difflib.SequenceMatcher(
                            None, words3(strip_text),
                            words3(page_clean)).ratio() >= 0.6)
            ratio = difflib.SequenceMatcher(None, fold(strip_text),
                                            fold(page_clean)).ratio()
            if first_ok:
                ok += 1
                src = 'strip3x+page-agree'
            else:
                disagree += 1
                src = 'strip3x'
                rows.append([n, note['num'], round(ratio, 2),
                             strip_text[:70], page_clean[:70]])
            new.append({'num': note['num'], 'top': note['top'],
                        'num_read': note.get('num_read'),
                        'text': strip_text, 'src': src})
        out[n] = {'lines': struct[n]['lines'], 'notes': new,
                  'height': struct[n]['height']}
    with open(os.path.join(OCR, 'structure4.json'), 'w',
              encoding='utf-8', newline='\n') as fh:
        json.dump(out, fh, ensure_ascii=False)
    with open(os.path.join(OCR, 'note_verify.csv'), 'w',
              encoding='utf-8', newline='\n') as fh:
        w = csv.writer(fh)
        w.writerow(['scan', 'note', 'ratio', 'strip3x', 'page'])
        w.writerows(rows)
    print('notes:', ok + disagree, '| strip+page agree:', ok,
          '| disagreements to read:', disagree)


if __name__ == '__main__':
    main()
