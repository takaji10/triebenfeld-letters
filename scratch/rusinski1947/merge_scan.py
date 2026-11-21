# -*- coding: utf-8 -*-
"""Detect note-openers inside BODY paragraphs of the composed draft.

A note's opening ('1 Przywilej lokacyjny...', 'AW. Steinke, B. 942',
'Por. daty...') inside a body paragraph is a boundary leak. Scan every
paragraph of original.md; flag paragraphs containing a sentence that
OPENS with a citation sigla + folio/s.-pattern (the note idiom), where
the paragraph is body (not a [^..]: definition line).
"""
import re

T = open(r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947\literature\rusinski1947\original.md',
         encoding='utf-8').read()
pages = re.split(r'\[p\. ([IVX\d]+)\]', T)
# pages: ['', 'I', text, 'III', text, ...]
cur = None
hits = []
for k in range(1, len(pages), 2):
    pnum, ptxt = pages[k], pages[k + 1]
    for para in ptxt.split('\n\n'):
        para = para.strip()
        if not para or para.startswith('[^'):
            continue
        # find mid-paragraph note idioms: sentence end + optional marker
        # junk + sigla + fol./s./nr reference
        for m in re.finditer(
                r'[.!?]”?\s*(?:\d{0,2}\s*)?'
                r'((?:AW|AM|AGH|Rel|Dom|Kat|KI|Tp|Q|Inw|Verz)\.[^,;.]{0,40}'
                r'(?:fol\.|s\.|nr|vol\.|kart)[^,;.]{0,25})', para):
            hits.append((pnum, m.group(1)[:70]))
print('in-body citation idioms:', len(hits))
for h in hits:
    print('  p.%s | %s' % h)
