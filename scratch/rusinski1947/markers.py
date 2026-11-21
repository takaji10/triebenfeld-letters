# -*- coding: utf-8 -*-
"""Reconstruction of the in-text footnote markers of tom5.

The print marks its notes with superscript numbers in the body; the page
passes mostly lose them (they glue to the previous word or vanish). This
module reconstructs them from three witnesses, per body line:

  1. the page TSV: tokens whose text ends in 1-2 digits after a letter
     ('Ujskich1') or carries the artifact tails (*?, ?, *), with their
     confidence (a glued superscript drags the confidence down);
  2. the line re-reads (full_lines.py): the same token shapes at 2.5x,
     where the markers read separately ('Charłub 4 (O Chromiec 5');
  3. the printed notes themselves: a page's markers must number exactly
     its notes (structure.py's count), numbered 1..n in reading order.

Assignment: candidates are collected in reading order and numbered 1..n;
if the count falls short of the notes, the lines whose two passes
disagree on their token tail are re-read at 4x (the .big passes) before
anything is left to the spot sheet.
"""
import sys, os, json, re

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'

# token-tail shapes a marker can take
TAIL = re.compile(
    r'^(?P<base>[^\W\d_][\wąćęłńóśźż.-]*?)'
    r'(?P<tail>[*?]*\d{1,2}[*?]?[.,;:]?)$', re.UNICODE)


def line_candidates(toks, confs):
    """Marker candidates in one line's tokens: [(idx, tok, why)]."""
    out = []
    for i, (tok, conf) in enumerate(zip(toks, confs)):
        m = TAIL.match(tok)
        if not m:
            continue
        base, tail = m.group('base'), m.group('tail')
        digits = re.sub(r'\D', '', tail)
        if not digits:
            continue
        # a real marker tail: 1-2 digits after letters, or the ?/* forms
        if len(digits) <= 2 and base and len(base) >= 2:
            why = []
            if conf and conf < 80:
                why.append('lowconf')
            if '*' in tok or '?' in tok:
                why.append('artifact')
            if digits and conf and conf >= 80 and '*' not in tok \
                    and '?' not in tok:
                # a plain glued digit at high confidence can still be a
                # year or a figure; kept as a weak candidate
                why.append('weak')
            out.append((i, tok, '+'.join(why) or 'plain'))
    return out


def main():
    struct = json.load(open(os.path.join(OCR, 'structure.json'),
                            encoding='utf-8'))
    short = []
    for n in sorted(struct):
        notes = struct[n]['notes']
        if not notes:
            continue
        want = len(notes)
        # candidates from the raw page text (in order)
        found = 0
        for raw in struct[n].get('raw', []):
            pass
        print(n, 'notes:', want)


if __name__ == '__main__':
    main()
