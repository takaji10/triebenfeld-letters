# -*- coding: utf-8 -*-
"""Compose original.md for Rusinski 1947 from the OCR products.

Inputs (all in Temp\\opencode\\tom5_ocr\\):
  <scan>.json      the two page passes ('pol' best, 'std' witness) + TSV
  structure.json   per-page lines and the footnote blocks (structure.py)
  lines/<scan>.json  the full-line re-reads (full_lines.py): line-level
                   witness and the superscript markers
  annex_rows.json  the annex tables' rows (annex_rows.py)
  strips/<scan>.json  the weak sheets' strip reads (strip_rows.py)

Format (the editor's rulings of 2026-11-05):
  - [p. N] page marks; the front matter before the first mark;
  - footnotes as markdown reference definitions with PAGE-PREFIXED labels
    [^<page>-<n>] (the print restarts numbering every page); the mapping
    recorded in notes.md;
  - the annex tables as HTML tables;
  - the four plates (plans + map) recorded, not transcribed;
  - nothing tidied: the print's own slips stand; OCR artifacts are
    corrected only where the witnesses agree on the print's form.

Draft status: the marker reconstruction and the tables are the parts still
under construction; this script composes what is settled and reports what
is not.
"""
import sys, os, json, re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paragraphs import assemble

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
OUT = os.path.join(OCR, 'original_draft.md')

BODY = [f'{i:04d}' for i in range(16, 138)]      # printed pp. 1-122
ANEX2 = [f'{i:04d}' for i in range(160, 166)]    # pp. 145-150
ANEX3 = [f'{i:04d}' for i in range(166, 172)]    # pp. 151-156


def label(n):
    return str(int(n) - 15)


def page_label(n):
    if n in BODY or n in ANEX2 or n in ANEX3:
        return label(n)
    return None


def notes_block(n, struct):
    """The page's footnote definitions in page-prefixed labels."""
    out = []
    for note in struct[n]['notes']:
        lab = f"{label(n)}-{note['num']}"
        text = note['text'].strip()
        out.append(f'[^{lab}]: {text}')
    return out


def body_md(n, struct):
    """The page's body as paragraphs (the print's own paragraphing)."""
    paras = assemble(n)
    return '\n\n'.join(paras)


def main():
    struct = json.load(open(os.path.join(OCR, 'structure.json'),
                            encoding='utf-8'))
    parts = []
    # ---- front matter -------------------------------------------------
    parts.append(FRONT_MATTER)
    # ---- body ---------------------------------------------------------
    for n in BODY:
        lab = label(n)
        parts.append(f'[p. {lab}]\n')
        parts.append(body_md(n, struct))
        nb = notes_block(n, struct)
        if nb:
            parts.append('\n'.join(nb))
    # ---- Aneks II and III (printed sources, prose) ---------------------
    for group, title in ((ANEX2, None), (ANEX3, None)):
        for n in group:
            lab = label(n)
            parts.append(f'[p. {lab}]\n')
            parts.append(body_md(n, struct))
            nb = notes_block(n, struct)
            if nb:
                parts.append('\n'.join(nb))
    text = '\n\n'.join(parts)
    with open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(text)
    print('written', OUT, len(text), 'chars')


FRONT_MATTER = ''  # set in front.py (composed separately)


if __name__ == '__main__':
    main()
