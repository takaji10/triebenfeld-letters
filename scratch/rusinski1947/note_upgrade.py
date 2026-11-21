# -*- coding: utf-8 -*-
"""Upgrade the note texts from the 3x strips, by alignment.

structure2's inventory passed the independent gate (verify_notes2: zero
suspects), but its texts are the page passes' (small type, mangled
digits). The 3x strips read the same blocks better. For each page:

  - parse the strip's note paragraphs (note_reconcile.strip_notes);
  - align them to structure2's notes by their read numbers where the
    strip read a digit, else by order;
  - where a strip paragraph's opening (first ~40 chars, folded) matches
    the structure2 note's opening, the strip text replaces it (the
    higher-resolution reading), keeping structure2's num;
  - unmatched strip paragraphs are recorded (strip_extra) - they are
    usually the strip's paragraph-merge artifacts, but each is kept for
    the spot sheet's check;
  - structure2 notes whose opening matches no strip paragraph are
    flagged (strip_missing).

Output: structure3.json (the upgraded inventory) + note_upgrade.csv.
"""
import json, os, re, csv

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
sys_path = os.path.dirname(os.path.abspath(__file__))


def fold(s):
    return re.sub(r'[^a-ząćęłńóśźż0-9]', '', s.lower())


def main():
    import sys
    sys.path.insert(0, sys_path)
    from note_reconcile import strip_notes
    struct = json.load(open(os.path.join(OCR, 'structure2.json'),
                            encoding='utf-8'))
    rows = []
    out = {}
    for n in sorted(struct):
        page = struct[n]
        notes = page['notes']
        sp = os.path.join(OCR, 'notestrips', n + '.json')
        if not notes or not os.path.isfile(sp):
            out[n] = page
            continue
        d = json.load(open(sp, encoding='utf-8'))
        sstarts = strip_notes(d['pol']) + strip_notes(d['std'])
        # dedupe strip starts by their opening
        seen = set()
        suniq = []
        for s in sstarts:
            k = fold(s['text'])[:24]
            if k and k not in seen:
                seen.add(k)
                suniq.append(s)
        used = set()
        new_notes = []
        for note in notes:
            key = fold(note['text'])[:24]
            hit = None
            for i, s in enumerate(suniq):
                if i in used:
                    continue
                sk = fold(s['text'])[:24]
                if key and sk and (sk.startswith(key[:16])
                                   or key.startswith(sk[:16])):
                    hit = i
                    break
            if hit is not None:
                used.add(hit)
                s = suniq[hit]
                new_notes.append({'num': note['num'],
                                  'top': note['top'],
                                  'text': s['text'],
                                  'src': 'strip3x'})
            else:
                new_notes.append(dict(note, src='page'))
                rows.append([n, note['num'], 'no-strip-match',
                             note['text'][:60]])
        for i, s in enumerate(suniq):
            if i not in used:
                rows.append([n, '-', 'strip-extra', s['text'][:60]])
        out[n] = {'lines': page['lines'], 'notes': new_notes,
                  'height': page['height']}
    with open(os.path.join(OCR, 'structure3.json'), 'w', encoding='utf-8',
              newline='\n') as fh:
        json.dump(out, fh, ensure_ascii=False)
    with open(os.path.join(OCR, 'note_upgrade.csv'), 'w', encoding='utf-8',
              newline='\n') as fh:
        w = csv.writer(fh)
        w.writerow(['scan', 'note', 'kind', 'text'])
        w.writerows(rows)
    upgraded = sum(1 for p in out.values()
                   for x in p['notes'] if x.get('src') == 'strip3x')
    total = sum(len(p['notes']) for p in out.values())
    print('notes:', total, 'upgraded from strips:', upgraded,
          'flagged:', len(rows))


if __name__ == '__main__':
    main()
