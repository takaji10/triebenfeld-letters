# -*- coding: utf-8 -*-
"""Structure each page of tom5 into body and footnote block.

The print's footnotes sit at the page foot, each beginning with its own
number (1..n, restarting every page); wrapped note lines do not begin with
a digit. Body paragraphs can begin with a year or figure, so a leading
digit alone is not enough: a footnote line must lie in the bottom 40% of
the page, follow a blank line that ends the body (or another note), and
its leading number must be the expected next note number.

The TSV boxes give every line's y, so the structuring works on the word
boxes, not the raw text: lines are rebuilt from the boxes in reading order.

Writes structure.json: per scan, lines = [(top, text)], body_top, notes =
[(num, first_top, text)], and the marker counts for the order-based
in-text reconstruction.
"""
import sys, os, json, re
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'


def lines_of(page):
    """The page's lines from the TSV boxes: [(top, x, text)], reading order.
    A line is a run of words whose tops sit within 30 px."""
    ws = [(x[1], x[0], x[5].strip(), x[4])
          for x in page['words'] if x[5].strip()]
    ws.sort()
    lines = []
    for top, left, word, conf in ws:
        if lines and abs(lines[-1][0] - top) < 30:
            lines[-1][2].append((left, word))
        else:
            lines.append([top, left, [(left, word)]])
    out = []
    for top, left, parts in lines:
        parts.sort()
        out.append({'top': top, 'text': ' '.join(w for _, w in parts)})
    return out


def split_notes(lines, height):
    """Return (body_lines, notes) where notes = [(num, top, text)]."""
    foot_limit = height * 0.60
    # find candidate note starts: lines whose text begins with 1-2 digits
    # and sit in the foot
    starts = []
    for i, ln in enumerate(lines):
        m = re.match(r'^(\d{1,2})\s+(\S.*)$', ln['text'])
        if m and ln['top'] > foot_limit:
            starts.append((i, int(m.group(1)), ln))
    if not starts:
        return lines, []
    # walk from the last plausible chain: the first note number should be 1
    # (or the page's notes continue 1..n); build the chain where each next
    # note's number is the previous + 1
    chains = []
    for j, (i0, n0, _) in enumerate(starts):
        if n0 != 1:
            continue
        chain = [(i0, n0)]
        cur = n0
        cur_i = i0
        for i, num, _ in starts[j + 1:]:
            if num == cur + 1 and i > cur_i:
                chain.append((i, num))
                cur, cur_i = num, i
        chains.append(chain)
    if not chains:
        return lines, []
    chain = max(chains, key=len)
    first = chain[0][0]
    body = lines[:first]
    notes = []
    for k, (i, num) in enumerate(chain):
        last = chain[k + 1][0] if k + 1 < len(chain) else len(lines)
        text = ' '.join(lines[j]['text'] for j in range(i, last))
        m = re.match(r'^\d{1,2}\s+(.*)$', text, re.S)
        notes.append({'num': num, 'top': lines[i]['top'],
                      'text': m.group(1) if m else text})
    return body, notes


def main():
    files = sorted(f for f in os.listdir(OCR)
                   if f.endswith('.json') and len(f) == 9 and f[:4].isdigit())
    out = {}
    for fn in files:
        n = fn[:4]
        with open(os.path.join(OCR, fn), encoding='utf-8') as fh:
            d = json.load(fh)
        lns = lines_of(d)
        if not lns:
            continue
        height = max(l['top'] for l in lns) + 100
        body, notes = split_notes(lns, height)
        out[n] = {'lines': [{'top': l['top'], 'text': l['text']}
                            for l in lns],
                  'notes': notes,
                  'height': height}
        if notes:
            print(n, 'notes:', [x['num'] for x in notes])
    with open(os.path.join(OCR, 'structure.json'), 'w', encoding='utf-8',
              newline='\n') as fh:
        json.dump(out, fh, ensure_ascii=False)
    print('pages:', len(out))


if __name__ == '__main__':
    main()
