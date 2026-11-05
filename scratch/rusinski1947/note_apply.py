# -*- coding: utf-8 -*-
"""Apply the per-note 3x readings to the inventory - with verification.

For each note, the per-note 3x crop (notetexts/<n>_<k>.json) is aligned
against structure2's page-pass text by difflib on the folded tokens:

  - ratio >= 0.75 and the 3x reading is longer: the 3x text is adopted
    (the higher resolution, same note);
  - ratio >= 0.75 and similar lengths: the 3x text is adopted where it
    differs in the mangled leading token ('ty', 'es', '%'...) which the
    page pass mangled and the 3x reading cleans ('2', '3'...);
  - ratio < 0.75: the crop caught a different note (the artifact-leading
    lines' tops can shift) - the page text stands, the case is flagged.

The adopted text keeps structure2's num (the inventory's authority); the
leading number token of the crop is stripped (the crop carries it or its
artifact).
"""
import json, os, re, difflib, csv

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'


def fold(s):
    return re.sub(r'[^a-ząćęłńóśźż0-9]', '', s.lower())


def main():
    struct = json.load(open(os.path.join(OCR, 'structure2.json'),
                            encoding='utf-8'))
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from note_adjudicate import ADJUDICATED
    rows = []
    out = {}
    adopted = kept = rejected = spot = 0
    for n in sorted(struct):
        notes = struct[n]['notes']
        if not notes:
            out[n] = struct[n]
            continue
        new = []
        for note in notes:
            p = os.path.join(OCR, 'notetexts', f'{n}_{note["num"]}.json')
            page_text = note['text']
            entry = {'num': note['num'], 'top': note['top']}
            verdict = ADJUDICATED.get((n, note['num']))
            if os.path.isfile(p) and verdict != 'keeppage':
                d = json.load(open(p, encoding='utf-8'))
                cand = max((d['pol'].strip(), d['std'].strip()),
                           key=lambda s: len(re.sub(r'\s', '', s)))
                cand_clean = re.sub(
                    r'^[\d!%*+$§£|.,)»\-—–?L\s]+(?=[A-ZĄĆĘŁŃÓŚŹŻ„"(])', '',
                    cand).strip()
                if verdict == 'adopt3x':
                    entry['text'] = cand_clean
                    entry['src'] = 'per-note-3x'
                    adopted += 1
                elif verdict == 'spot':
                    entry['text'] = page_text
                    entry['src'] = 'spot'
                    spot += 1
                    rows.append([n, note['num'], 'SPOT', cand_clean[:60],
                                 page_text[:60]])
                else:
                    # unadjudicated: the automatic same-note test
                    pg_clean = re.sub(
                        r'^[\d!%*+$§£|.,)»\-—–\s]+(?=[A-ZĄĆĘŁŃÓŚŹŻ„"(])',
                        '', page_text).strip()
                    r = difflib.SequenceMatcher(None, fold(cand_clean),
                                                fold(pg_clean)).ratio()
                    cw = re.findall(r'[a-ząćęłńóśźż0-9]+', fold(cand_clean))
                    pw = re.findall(r'[a-ząćęłńóśźż0-9]+', fold(pg_clean))
                    first_match = (cw[:3] and pw[:3]
                                   and difflib.SequenceMatcher(
                                       None, ' '.join(cw[:3]),
                                       ' '.join(pw[:3])).ratio() >= 0.6)
                    if first_match and len(fold(cand_clean)) >= \
                            len(fold(pg_clean)) * 0.8:
                        entry['text'] = cand_clean
                        entry['src'] = 'per-note-3x'
                        adopted += 1
                    else:
                        entry['text'] = page_text
                        entry['src'] = 'page'
                        rejected += 1
                        rows.append([n, note['num'], round(r, 2),
                                     cand_clean[:50], page_text[:50]])
            else:
                entry['text'] = page_text
                entry['src'] = 'page'
                kept += 1
            new.append(entry)
        out[n] = {'lines': struct[n]['lines'], 'notes': new,
                  'height': struct[n]['height']}
    with open(os.path.join(OCR, 'structure4.json'), 'w',
              encoding='utf-8', newline='\n') as fh:
        json.dump(out, fh, ensure_ascii=False)
    with open(os.path.join(OCR, 'note_reject.csv'), 'w', encoding='utf-8',
              newline='\n') as fh:
        w = csv.writer(fh)
        w.writerow(['scan', 'note', 'ratio', 'reread3x', 'page'])
        w.writerows(rows)
    print('notes: adopted', adopted, 'kept', kept, 'rejected', rejected,
          'spot', spot)


if __name__ == '__main__':
    main()
