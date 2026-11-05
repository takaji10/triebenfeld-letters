# -*- coding: utf-8 -*-
"""Text polish: rescue garbled strip notes with the per-note crops.

The strip (psm 4, 3x) is the text of record, but on warped sheets its
read collapses ('EZ A e oda U U Z Z...' on 0063). The per-note crops
(psm 6 on the note's own region) are a second 3x witness. For notes
whose strip text has a low LEXICON validity (fraction of alphabetic
tokens the book's own lexicon knows), adopt the crop text when it
scores clearly higher.

Output: updated structure4.json + polish_report.
"""
import json, os, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'


def main():
    lex = set(json.load(open(os.path.join(OCR, 'lexicon.json'),
                             encoding='utf-8'))['words'])
    s = json.load(open(os.path.join(OCR, 'structure4.json'),
                       encoding='utf-8'))

    def validity(text):
        toks = [t.lower() for t in
                re.findall(r'[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]{3,}', text)]
        if not toks:
            return 0.0
        return sum(1 for t in toks if t in lex) / len(toks)

    adopted = []
    for n in sorted(s):
        for note in s[n]['notes']:
            vs = validity(note['text'])
            if vs >= 0.75:
                continue
            p = os.path.join(OCR, 'notetexts', f"{n}_{note['num']}.json")
            if not os.path.isfile(p):
                continue
            d = json.load(open(p, encoding='utf-8'))
            cand = max((d['pol'].strip(), d['std'].strip()),
                       key=lambda t: len(re.sub(r'\s', '', t)))
            cand_clean = re.sub(
                r'^[\d!%*+$§£|.,)»\-—–?L\s]+(?=[A-ZĄĆĘŁŃÓŚŹŻ„"(])', '',
                cand).strip()
            vc = validity(cand_clean)
            if vc > vs + 0.02 and len(cand_clean) > 12:
                adopted.append((n, note['num'], round(vs, 2),
                                round(vc, 2), cand_clean[:60]))
                note['text'] = cand_clean
                note['src'] = 'crop3x'
    with open(os.path.join(OCR, 'structure4.json'), 'w',
              encoding='utf-8', newline='\n') as fh:
        json.dump(s, fh, ensure_ascii=False)
    print('polished:', len(adopted))
    for a in adopted:
        print(a)


if __name__ == '__main__':
    main()
