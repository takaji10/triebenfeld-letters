"""Split the 9454 per-scan transcriptions into one file per page image.

A record of how units/oe1bu9454/transcriptions/ was made; that folder, not this
script's output, is now the source import_pages.py reads.

Each txt in ../per_scan_txt/ is one archival scan, which may hold one or two
pages. The page images in pages/ are already split, and the old page_scan_map.csv
(retired to Trash/oe1bu9454_old/) gives the old corpus.txt line range for each
page. For two-page scans the split point in the (corrected) new text is found by
fuzzy-matching its lines against the old text of each page.

Output: txt_pages/<page image name>.txt and split_report.csv, next to this file.
The pages were then copied into transcriptions/ as <seq>_Oe 1_Bue 9454_<page>.txt,
with letter 48's pages (0093_a, 0094_a1) placed before letter 49's (0092_a).
"""
import collections
import csv
import difflib
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
OLD = os.path.normpath(os.path.join(HERE, '..', '..', '..', '..'))   # project root
TXT_DIR = os.path.join(HERE, '..', 'per_scan_txt')
OUT_DIR = os.path.join(HERE, 'txt_pages')
REPORT = os.path.join(HERE, 'split_report.csv')

# Manual corrections after review: {"SSSS_x": number of non-blank lines on page 1}
OVERRIDES = {
    '0241_a': 15,  # "v Triebenfeld" signs page 1
    '0343_a': 30,  # "D." heads the amortisation plan on page 2
    '0490_a': 20,  # "v Triebenfeld" signs letter 269 on page 1; 269a opens page 2
    # Creditor tables: page 2 starts at its "Continuatio" header
    '0543_a': 74,
    '0544_a': 67,
    '0545_a': 42,
    '0546_a': 34,
}

BARE_NUMBER = re.compile(r'^\s*\d{1,3}[a-z]?\s*$')


def load_old_pages():
    # The old transcription was retired to Trash once the re-import began.
    unit = os.path.join(OLD, 'Trash', 'oe1bu9454_old', 'units', 'oe1bu9454')
    with open(os.path.join(unit, 'corpus.txt'), encoding='utf-8') as f:
        corpus = f.read().split('\n')
    old = {}
    with open(os.path.join(unit, 'page_scan_map.csv'), encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            if not r['image']:
                continue
            if r['line_start']:
                lines = corpus[int(r['line_start']) - 1:int(r['line_end'])]
                old[r['image']] = [l.strip() for l in lines if l.strip()]
            else:
                old[r['image']] = []
    return old


def page_groups():
    groups = collections.defaultdict(list)
    for f in sorted(os.listdir(os.path.join(OLD, 'pages'))):
        m = re.match(r'Oe_1_Bu_9454_(\d{4})_([a-z])(\d?)', f)
        if m:
            groups[f'{m[1]}_{m[2]}'].append((m[3], f))
    return {k: [f for _, f in sorted(v)] for k, v in groups.items()}


def best_ratio(line, candidates):
    line = line.strip()
    if BARE_NUMBER.match(line):
        # Letter numbers are new in this transcription; leave them to tiebreak().
        return 0.0
    return max((difflib.SequenceMatcher(None, line, c, autojunk=False).ratio()
                for c in candidates), default=0.0)


def find_split(new, o1, o2):
    """Return (k, info): page 1 gets the first k non-blank lines of new."""
    s1 = [best_ratio(n, o1) for n in new]
    s2 = [best_ratio(n, o2) for n in new]
    scores = [sum(s1[:k]) + sum(s2[k:]) for k in range(len(new) + 1)]
    top = max(scores)
    tied = [k for k, s in enumerate(scores) if top - s < 1e-9]

    def tiebreak(k):
        # A letter-number header ("240") starts page 2; otherwise stay close
        # to the old page-1 length.
        header = k < len(new) and BARE_NUMBER.match(new[k]) is not None
        return (not header, abs(k - len(o1)))

    k = min(tied, key=tiebreak)
    others = [s for i, s in enumerate(scores) if i not in tied]
    margin = top - max(others) if others else 99.0
    first = k
    while first < len(new) - 1 and BARE_NUMBER.match(new[first]):
        first += 1
    return k, {
        'margin': margin,
        'last_score': s1[k - 1] if k > 0 else 0.0,
        'first_score': s2[first] if first < len(new) else 0.0,
    }


def split_raw(raw_lines, k):
    """Split raw lines (with endings) after the k-th non-blank line.

    Blank lines between the pages stay at the end of page 1.
    """
    if k == 0:
        return [], raw_lines
    seen = 0
    for i, line in enumerate(raw_lines):
        if line.strip():
            seen += 1
            if seen == k:
                j = i + 1
                while j < len(raw_lines) and not raw_lines[j].strip():
                    j += 1
                return raw_lines[:j], raw_lines[j:]
    return raw_lines, []


def out_name(image):
    return os.path.splitext(image)[0] + '.txt'


def write(name, lines):
    with open(os.path.join(OUT_DIR, name), 'w', encoding='utf-8', newline='') as f:
        f.writelines(lines)


def main():
    old = load_old_pages()
    groups = page_groups()
    os.makedirs(OUT_DIR, exist_ok=True)
    report = []
    counts = collections.Counter()

    for txt in sorted(os.listdir(TXT_DIR)):
        m = re.match(r'\d{4}_Oe 1_Bue 9454_(\d{4})_([a-z])\.txt$', txt)
        key = f'{m[1]}_{m[2]}'
        images = [i for i in groups[key] if 'notapage' not in i]
        with open(os.path.join(TXT_DIR, txt), encoding='utf-8', newline='') as f:
            raw = f.readlines()

        if len(images) == 1:
            write(out_name(images[0]), raw)
            counts['copied'] += 1
            continue

        p1, p2 = images
        new = [l.strip() for l in raw if l.strip()]
        o1, o2 = old[p1], old[p2]
        k, info = find_split(new, o1, o2)
        overridden = key in OVERRIDES
        if overridden:
            k = OVERRIDES[key]
        a, b = split_raw(raw, k)
        write(out_name(p1), a)
        write(out_name(p2), b)
        counts['split'] += 1

        check = (info['margin'] < 0.3 or info['last_score'] < 0.6
                 or info['first_score'] < 0.6 or abs(k - len(o1)) > 2)
        report.append({
            'txt': txt,
            'page1': out_name(p1),
            'page2': out_name(p2),
            'split_after_line': k,
            'new_lines': len(new),
            'old_p1_lines': len(o1),
            'old_p2_lines': len(o2),
            'margin': round(info['margin'], 2),
            'p1_last_score': round(info['last_score'], 2),
            'p2_first_score': round(info['first_score'], 2),
            'p1_last_line': new[k - 1] if k > 0 else '',
            'p2_first_line': new[k] if k < len(new) else '',
            'flag': 'override' if overridden else ('check' if check else ''),
        })

    with open(REPORT, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(report[0]))
        w.writeheader()
        w.writerows(report)

    flagged = sum(1 for r in report if r['flag'] == 'check')
    print(f"copied {counts['copied']}, split {counts['split']}, flagged {flagged}")


if __name__ == '__main__':
    main()
