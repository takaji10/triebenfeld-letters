# -*- coding: utf-8 -*-
"""Trace the strip parse for one page: every line, every decision."""
import json, os, re, sys
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947\scratch\rusinski1947')
import structure2 as S

n = sys.argv[1] if len(sys.argv) > 1 else '0061'
j = json.load(open(os.path.join(S.OCR, 'widestrips', n + '.json'),
                  encoding='utf-8'))
CAP = r'[A-ZĄĆĘŁŃÓŚŹŻ„"(]'
ABBR = re.compile(
    r'(?:[A-ZĄĆĘŁŃÓŚŹŻ]{1,4}|fol|s|nr|vol|t|cz|it|nd|tj|d|j|w|m|z|[IVX]+)\.$',
    re.UNICODE)
lines = [l.strip() for l in j['pol'].split('\n') if l.strip()]

def ends_sent(i):
    if i <= 0:
        return True
    prev = lines[i - 1]
    if not re.search(r'[.!?]”?\s*$', prev):
        return False
    toks = prev.split()
    if toks and ABBR.match(toks[-1]):
        return False
    return True

expected = None
starts = []
for idx, l in enumerate(lines):
    m = re.match(r'^(\d{1,2})[.,)%/*!?+§$£]{0,2}\s+(' + CAP + r'.*)$', l)
    tag = ''
    if m:
        num = int(m.group(1))
        if expected is None or (num == expected and ends_sent(idx)) \
                or (not starts and ends_sent(idx)):
            tag = 'START(read=%d)' % num
            starts.append(num)
            expected = num + 1
        elif starts and ends_sent(idx):
            tag = 'START-misread(read=%d)' % num
            starts.append(num)
            expected = num + 1
        else:
            tag = 'cont'
    else:
        tok = l.split()[0] if l.split() else ''
        rest = l[len(tok):].lstrip()
        if tok and len(tok) <= 2 and rest and re.match(CAP, rest):
            strong = all(c in '!%*+$§£|?' for c in tok)
            LOOK = re.compile(r'^[iIlLsSzZżźćńółąę?*BqgOo]{1,2}$')
            look = bool(LOOK.match(tok))
            if strong and ends_sent(idx):
                tag = 'START-artifact(%r)' % tok
                starts.append(None)
                expected = (expected + 1) if expected is not None else None
            elif starts and look and expected is not None and ends_sent(idx):
                tag = 'START-look(%r)' % tok
                starts.append(None)
                expected += 1
            else:
                tag = 'cont'
        else:
            tag = 'cont'
    print('%3d %-24s %s' % (idx, tag, l[:70]))
print('starts:', len(starts))
