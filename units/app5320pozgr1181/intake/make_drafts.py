# -*- coding: utf-8 -*-
"""Draft lineation for pp. 161v-167v: the editor's words wrapped at the
manuscript's characters-per-line (measured on their p. 161: ~85). Every
break is ESTIMATED - the session cannot see the scans, and its measured
boundary error on the editor's own p. 161 ground truth was 2-4 words per
line. These drafts are for the editor to correct at the desktop (or to
ignore in favour of laying the pages out themselves, as they did p. 161);
they are NOT the corpus, which keeps the paragraph layout until the editor's
lineation arrives."""
import io, os, re, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'lineation_draft')
CPL = 85

PAGES = ['0161_b', '0162_a', '0162_b', '0163_a', '0163_b', '0164_a',
         '0164_b', '0165_a', '0165_b', '0166_a', '0166_b', '0167_a',
         '0167_b']

def wrap(text, cpl):
    out = []
    cur = ''
    for w in text.split():
        # never split a word in the draft: the manuscript's hyphen breaks
        # are the editor's to place
        if cur and len(cur) + 1 + len(w) > cpl:
            out.append(cur)
            cur = w
        else:
            cur = (cur + ' ' + w).strip()
    if cur:
        out.append(cur)
    return out

def main():
    os.makedirs(OUT, exist_ok=True)
    for pid in PAGES:
        src = os.path.join(HERE, '..', 'transcriptions', pid + '.txt')
        text = open(src, encoding='utf-8').read()
        lines = wrap(text, CPL)
        with open(os.path.join(OUT, pid + '.draft.txt'), 'w',
                  encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(lines) + '\n')
        print('%s: %d lines' % (pid, len(lines)))
    with open(os.path.join(OUT, 'README.md'), 'w', encoding='utf-8',
              newline='\n') as f:
        f.write(
            '# Draft lineation, pp. 161v-167v (ESTIMATED - not the corpus)\n\n'
            'The words are the editor\'s; the line breaks are a machine wrap at\n'
            'the manuscript\'s average characters per line (85, measured on the\n'
            'editor\'s own layout of p. 161). Measured against that ground truth,\n'
            'the method\'s boundary error is 2-4 words per line and grows along\n'
            'the page - so these drafts are a typing aid, not a reading. The\n'
            'editor lays each page out against the scan (as they did p. 161) and\n'
            'the corrected text replaces the paragraph layout in the corpus; or\n'
            'they correct these drafts in place, whichever is faster. Nothing\n'
            'here is built until then.\n')

if __name__ == '__main__':
    main()
