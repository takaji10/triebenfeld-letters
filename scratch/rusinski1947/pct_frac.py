# -*- coding: utf-8 -*-
"""The percent/fraction artifact settlement.

Two artifact families in the body text:
  A. the print's PERCENT glyph: '2%', '5%', '10%'... OCR splits the %
     into '9/,', '%/,', '%,', '%/' etc. Context test: the token follows
     a number and the sentence speaks of shares (ludności, ogółu,
     mieszkańców, dymów...). The print form is '<num>%'.
  B. the print's VULGAR FRACTIONS: 8½, 17½, 3¾, ¼... - resolved by the
     5x re-reads (frac_rereads.py): where both 5x models agree on
     '<num>/<den>', the print form is that fraction; where they
     disagree or the reading is a percent-fraction ambiguity (5/9 vs
     5%), the case goes to the spot sheet.

Output: pct_frac.json: per token box, {print form, evidence, resolved?}
plus spot entries appended to spot_words.csv.
"""
import sys, os, json, re, csv
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from PIL import Image
from pipeline.ocr import read

OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
SRC = r'C:\Users\Tersnaus\Downloads\tom5'
BODY = {f'{i:04d}' for i in range(16, 138)} | \
       {f'{i:04d}' for i in range(160, 172)}

PCT = re.compile(r'^(\d{1,3})(?:[.,]\d+)?\s*[%9]\s*[/,]', re.UNICODE)
FRAC5 = re.compile(r'(\d{1,3})\s*/\s*(\d{1,2})')


def main():
    import io
    rows = []
    out = {}
    spot = []
    # the 5x re-read queue: every PCT candidate, conf-0 included
    queue = []
    for fn in sorted(os.listdir(OCR)):
        if not (fn.endswith('.json') and len(fn) == 9):
            continue
        n = fn[:4]
        if n not in BODY:
            continue
        d = json.load(open(os.path.join(OCR, fn), encoding='utf-8'))
        text = d['pol']
        for x in d['words']:
            tok = x[5].strip()
            if PCT.match(tok):
                queue.append((n, x))
    # run the 5x re-reads (fraction-style, ±300px)
    for n, x in queue:
        l, t, w_, h = x[0], x[1], x[2], x[3]
        f5 = os.path.join(OCR, 'fractions', f'{n}_{l}_{t}.txt')
        if not os.path.isfile(f5):
            try:
                with open(os.path.join(SRC, f'tom5_{n}.tif'), 'rb') as fh:
                    data = fh.read()
                im = Image.open(io.BytesIO(data))
                im.load()
                W, H = im.size
                a, b = max(0, t - 12), min(H, t + h + 12)
                lo, hi = max(0, l - 300), min(W, l + w_ + 300)
                c = im.crop((lo, a, hi, b))
                c = c.resize((c.size[0] * 5, c.size[1] * 5), Image.LANCZOS)
                sp = os.path.join(OCR, 'fractions', 'tmp.png')
                c.save(sp)
                t1 = read(sp, lang='pol', psm=7).strip()
                t2 = read(sp, lang='pol-std', psm=7).strip()
                with open(f5, 'w', encoding='utf-8', newline='\n') as fh:
                    fh.write(tok + '\n---\n' + t1 + '\n@@@\n' + t2)
            except Exception as e:
                print('reread fail', n, tok, type(e).__name__)
    print('queued+read:', len(queue))
    for fn in sorted(os.listdir(OCR)):
        if not (fn.endswith('.json') and len(fn) == 9):
            continue
        n = fn[:4]
        if n not in BODY:
            continue
        d = json.load(open(os.path.join(OCR, fn), encoding='utf-8'))
        text = d['pol']
        for x in d['words']:
            tok = x[5].strip()
            m = PCT.match(tok)
            if not m:
                continue
            num = m.group(1)
            # context: 30 chars before the token
            i = text.find(tok)
            ctx = text[max(0, i - 60):i + len(tok) + 20].replace('\n', ' ')
            # the fraction 5x re-read, if one exists for this box
            f5 = os.path.join(OCR, 'fractions', f'{n}_{x[0]}_{x[1]}.txt')
            f5t = open(f5, encoding='utf-8').read() if os.path.isfile(f5) \
                else None
            entry = {'scan': n, 'tok': tok, 'ctx': ctx[-70:]}
            if f5t:
                orig, _, rest = f5t.partition('\n---\n')
                pol, _, std = rest.partition('\n@@@\n')
                entry['reread5x'] = [pol.strip(), std.strip()]
                # THE GLYPH DECIDES: a real % shows its shape at 5x; a
                # year or folio number reads as plain digits ('fol. 239,'
                # -> 'fol. 239,'; 'r. 1729' -> 'r. 1729'). The print form
                # of a percent is '<num>%'.
                both = pol + ' ' + std
                after = ''
                i = text.find(tok)
                if i >= 0:
                    after = text[i + len(tok):i + len(tok) + 30]
                MEASURE = re.compile(
                    r'[\s,.]*(wł|włó|włók|włóki|morg|morgów|morgi'
                    r'|korc|korca|korce|garn|garnc|garnca|ziarn|hub|łan'
                    r'|łoki)', re.U)
                SHARE = re.compile(
                    r'[\s,.]*(ludno|ogół|ogółu|mieszkań|dym|dymów|osad'
                    r'|sumy|grunty|płac|stanowi|wynosi|przypad|dochodzi'
                    r'|tworz)', re.U)
                has_pct = bool(re.search(re.escape(num) + r'\s*%', both))
                if not has_pct:
                    # plain digits at 5x: a year or a folio number - the
                    # original token stands
                    entry['print'] = tok
                    entry['resolved'] = True
                    entry['evidence'] = 'plain digits at 5x (year/folio)'
                elif SHARE.search(after) or SHARE.search(' ' + ctx[-40:]):
                    entry['print'] = f'{num}%'
                    entry['resolved'] = True
                    entry['evidence'] = 'percent glyph + share context'
                elif MEASURE.search(after):
                    m1 = FRAC5.search(pol)
                    m2 = FRAC5.search(std)
                    if m1 and m2 and m1.group(2) == m2.group(2):
                        entry['print'] = f'{num}/{m1.group(2)}'
                        entry['resolved'] = True
                        entry['evidence'] = 'fraction, denominators agree'
                    else:
                        entry['print'] = None
                        entry['resolved'] = False
                        spot.append([n, x[0], x[1], x[2], x[3], tok,
                                     'fraction?'])
                elif not after.strip() or after.lstrip()[:1].isupper():
                    entry['print'] = 'MARKER'
                    entry['resolved'] = True
                    entry['evidence'] = 'footnote marker artifact'
                else:
                    entry['print'] = None
                    entry['resolved'] = False
                    spot.append([n, x[0], x[1], x[2], x[3], tok, '?pct'])
            else:
                # no 5x re-read (rare): flag for the spot sheet - the
                # context test alone misdecoded folio numbers
                entry['print'] = None
                entry['resolved'] = False
                spot.append([n, x[0], x[1], x[2], x[3], tok, '?pct'])
            out[f'{n}_{x[0]}_{x[1]}'] = entry
            rows.append([n, x[0], x[1], tok, entry.get('print', ''),
                         entry.get('resolved', ''), ctx[-50:]])
    with open(os.path.join(OCR, 'pct_frac.json'), 'w', encoding='utf-8',
              newline='\n') as fh:
        json.dump(out, fh, ensure_ascii=False)
    with open(os.path.join(OCR, 'pct_frac.csv'), 'w', encoding='utf-8',
              newline='\n') as fh:
        w = csv.writer(fh)
        w.writerow(['scan', 'left', 'top', 'tok', 'print', 'resolved',
                    'ctx'])
        w.writerows(rows)
    res = sum(1 for v in out.values() if v.get('resolved'))
    print('tokens:', len(out), 'resolved:', res, 'spot:', len(spot))
    with open(os.path.join(OCR, 'spot_pct.csv'), 'w', encoding='utf-8',
              newline='\n') as fh:
        w = csv.writer(fh)
        w.writerow(['scan', 'left', 'top', 'width', 'height', 'word',
                    'alt'])
        w.writerows(spot)


if __name__ == '__main__':
    main()
