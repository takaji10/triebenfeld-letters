# -*- coding: utf-8 -*-
"""The translation QA battery: source (original.md) vs target
(english.md). Zones: pp. 1-122 + pp. 145-157 are compared 1:1; the
ANEKS-I zone (pp. 123-144) is skipped (decision D6).
Checks:
  1. label sequence equality
  2. per-page digit multiset equality (separators stripped; decade
     forms '1780s' allowed as additions)
  3. per-page fraction-glyph multiset equality
  4. per-page footnote ref/def label multisets
  5. per-page 'zł'/'gr' token counts
  6. siglum inventory over the covered zone
  7. table row/column counts per table region"""
import re
from collections import Counter

BASE = (r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba'
        r'\rusinski1947\literature\rusinski1947')
S = open(BASE + r'\original.md', encoding='utf-8').read()
T = open(BASE + r'\english.md', encoding='utf-8').read()

FR = '½⅓⅔¼¾⅛⅜⅝⅞⅑⅕⅖⅗⅘⅙⅚⅐⅑'
def norm(txt):
    """Normalize known OCR garbles so BOTH texts count equally."""
    for a, b in (('ĄW.', 'AW.'), ('A.M ', 'AM. '),
                 ('Rel. Posn,', 'Rel. Posn.'), ('K]. ', 'Kl. '),
                 ("'T'ol.", 'Tol.'), ('złŁ', 'zł')):
        txt = txt.replace(a, b)
    return txt



REF = re.compile(r'\[\^(\d+)-(\d+)\](?!:)')
DEFC = re.compile(r'^\[\^(\d+)-(\d+)\]:', re.M)

# ---- the adjudicated deviations (each verified against the agents'
# reports and, where noted, against the page pixels) -----------------
# extra = tokens present only in the target; miss = only in the source
DIGIT_OK = {
    '58': ({'15': 1}, {'5': 1, '7': 1},
           'print reads 1 złotego 15 groszy (pixels: I@2151 + 1@2422 + '
           '5groszy@2446): the OCR split 15 into 1+5; 7 = the Z-garble '
           'of def 58-5 "Z reguły"'),
    '63': ({}, {'1': 1}, "junk '1'=i dropped (agent-documented)"),
    '67': ({'7': 3}, {'71': 3, '1': 2},
           "'71/,' -> 7½ normalizations (x3) + junk 1s"),
    '68': ({'1': 1}, {'2': 2, '4': 1, '11': 2},
           'garbled fractions -> 1½/¼ normalizations'),
    '69': ({'32': 1, '27': 1, '17': 1, '18': 1, '20': 1, '21': 1},
           {'2': 1, '11': 1, '5': 1, '4': 2, '279': 1, '171': 1,
            '181': 1, '201': 1, '211': 1, '321': 1, '33': 1},
           'def 69-1 Folsztyn fraction-list reconstruction '
           '(corroborated by fn 98-4)'),
    '70': ({}, {'1': 4, '4': 1},
           'junk digits in the garbled Kawczyn quote tail, rendered by '
           'sense'),
    '71': ({}, {'4': 1}, 'fraction normalization residue'),
    '72': ({}, {'1': 1}, "junk '1'=i"),
    '73': ({}, {'2': 1}, "junk ('d 2' tail of def 73-4)"),
    '74': ({}, {'1': 1}, "junk '1'=i"),
    '75': ({}, {'1': 2}, "junk '1'=i (def)"),
    '76': ({'7': 1}, {'71': 1, '1': 2}, "7½ normalization + junk 1s"),
    '77': ({}, {'1': 1}, "junk '1'=i (def 77-8)"),
    '78': ({}, {'1': 1}, "junk '1'=i (def 78-8)"),
    '79': ({}, {'1': 5}, "junk '1'=i (x5)"),
    '87': ({}, {'1': 1}, "junk '1'=i"),
    '146': ({}, {'1': 4}, "'1'=i in the printed document -> 'and'"),
    '147': ({}, {'1': 1}, "'1'=i"),
    '148': ({}, {'20': 1, '1': 1},
            "garble '20' (nie akceptowania 20 przyczyny) + '1'=i, "
            'rendered by sense'),
    '149': ({}, {'1': 1}, "'1'=i"),
    '152': ({'2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1,
             '9': 1}, {'1': 2},
            'clause numbers 2-9 restored (the print numbers its '
            'clauses; the OCR lost the numerals)'),
    '153': ({}, {'1': 3}, "'1'=i (x3)"),
    '154': ({'26': 1}, {'1': 4}, 'clause 26 restored + 1=i (x4)'),
    '155': ({}, {'1': 1}, "'1'=i"),
    '156': ({}, {'1': 1}, "'1'=i"),
}
FRACTION_OK = {
    '67': ({'⅓': 1, '½': 3}, {}), '68': ({'½': 5, '¼': 1}, {}),
    '69': ({'½': 16, '¾': 2, '¼': 2, '⅜': 1, '⅗': 1, '⅝': 1}, {}),
    '70': ({'¼': 1, '½': 1}, {}), '71': ({'⅛': 2, '¼': 1, '½': 1}, {}),
    '76': ({'½': 3}, {}), '78': ({'½': 1}, {}), '79': ({'½': 1}, {}),
    '98': ({'¼': 1}, {}), '99': ({'½': 2}, {}), '107': ({'½': 1}, {}),
    '108': ({'½': 2}, {}), '110': ({'½': 1}, {}), '114': ({'½': 3}, {}),
}
CUR_OK = {'86': ({}, {'gr': 1},
                 "garble '(Hb gr)' rendered by sense ('a szóstak, a coin "
                 'of six groszy)')}


def blocks(txt):
    out, cur = {}, None
    for ln in txt.splitlines():
        m = re.match(r'^\[p\. (\w+)\]$', ln.strip())
        if m:
            cur = m.group(1)
            out[cur] = []
            continue
        if cur is not None:
            out[cur].append(ln)
    return {k: '\n'.join(v) for k, v in out.items()}


sb, tb = blocks(S), blocks(T)

ok = True


def check(name, cond, detail=''):
    global ok
    if not cond:
        ok = False
    print('%s %s %s' % ('PASS' if cond else 'FAIL', name, detail))


# 1. labels
skip = set(range(123, 145))
ls = [l for l in sb if l.isdigit() and int(l) not in skip
      and 1 <= int(l) <= 157]
lt = [l for l in tb if l.isdigit() and int(l) not in skip
      and 1 <= int(l) <= 157]
check('label sequence', ls == lt,
      'src %d labels / tgt %d' % (len(ls), len(lt)))
if ls != lt:
    ss, st = set(ls), set(lt)
    print('   only-src:', sorted(ss - st)[:10],
          'only-tgt:', sorted(st - ss)[:10])


def digits(txt):
    txt = txt.replace('.', '').replace(',', '').replace('—', '-')
    txt = REF.sub(' ', txt)
    toks = re.findall(r'\d+', txt)
    # decade forms (the sanctioned additions)
    toks = [x for x in toks if not re.fullmatch(r'1[6-9]\d0s?', x)]
    return Counter(toks)


def reconcile(extra, miss):
    """Accept split/merge token pairs on the EXPANDED multisets: a
    target token is satisfied by one source token (exact) or by a
    group of 2-3 source tokens whose some-permutation concatenation
    equals it (and symmetrically). Returns the true residue."""
    import itertools
    e = []
    for k, n in extra.items():
        e += [k] * n
    m = []
    for k, n in miss.items():
        m += [k] * n
    # exact matches first
    me, mm = Counter(e), Counter(m)
    common = me & mm
    e = list((me - common).elements())
    m = list((mm - common).elements())
    # split/merge groups (both directions on the same live lists)
    for tgt, src in ((e, m), (m, e)):
        i = 0
        while i < len(tgt):
            hit = False
            for r in (2, 3):
                if len(src) < r:
                    continue
                for combo in itertools.permutations(src, r):
                    if ''.join(combo) == tgt[i]:
                        for c in combo:
                            src.remove(c)
                        tgt.pop(i)
                        hit = True
                        break
                if hit:
                    break
            if not hit:
                i += 1
    return Counter(e), Counter(m)


def fracs(txt):
    return Counter(c for c in txt if c in FR)


digit_bad, frac_bad, ref_bad, def_bad, cur_bad = [], [], [], [], []
for lab in ls:
    a, b = sb[lab], tb.get(lab, '')
    da, db = digits(a), digits(b)
    db2, da2 = reconcile(dict(db - da), dict(da - db))
    wl = DIGIT_OK.get(lab)
    if wl:
        wextra, wmiss = Counter(wl[0]), Counter(wl[1])
        db2, da2 = Counter(db2) - wextra, Counter(da2) - wmiss
        if db2 or da2:
            digit_bad.append((lab, dict(+db2), dict(+da2),
                              'BEYOND WHITELIST: ' + wl[2]))
    elif db2 or da2:
        digit_bad.append((lab, dict(db2), dict(da2), 'no whitelist'))
    fa, fb = fracs(a), fracs(b)
    fex, fmi = dict(fb - fa), dict(fa - fb)
    fw = FRACTION_OK.get(lab)
    if fw:
        wex, wmi = Counter(fw[0]), Counter(fw[1])
        fex2, fmi2 = Counter(fex) - wex, Counter(fmi) - wmi
        if fex2 or fmi2:
            frac_bad.append((lab, dict(+fex2), dict(+fmi2)))
    elif fex or fmi:
        frac_bad.append((lab, fex, fmi))
    ra = Counter(REF.findall(a.replace('[p.', '[')))
    rb = Counter(REF.findall(b.replace('[p.', '[')))
    if ra != rb:
        ref_bad.append((lab, dict(rb - ra), dict(ra - rb)))
    la = Counter(DEFC.findall(a))
    lb = Counter(DEFC.findall(b))
    if la != lb:
        def_bad.append((lab, dict(lb - la), dict(la - lb)))
    ca, cb = (Counter(re.findall(r'\bzł\b|\bgr\b', norm(a))),
              Counter(re.findall(r'\bzł\b|\bgr\b', norm(b))))
    cex, cmi = dict(cb - ca), dict(ca - cb)
    cw = CUR_OK.get(lab)
    if cw:
        wex, wmi = Counter(cw[0]), Counter(cw[1])
        cex2, cmi2 = Counter(cex) - wex, Counter(cmi) - wmi
        if cex2 or cmi2:
            cur_bad.append((lab, dict(+cex2), dict(+cmi2)))
    elif cex or cmi:
        cur_bad.append((lab, cex, cmi))

check('digit multisets per page', not digit_bad,
      '%d diffs' % len(digit_bad))
for lab, extra, miss in digit_bad[:40]:
    print('   p.%s extra=%s missing=%s' % (lab, extra, miss))
check('fraction glyphs per page', not frac_bad, '%d diffs' % len(frac_bad))
for lab, extra, miss in frac_bad[:40]:
    print('   p.%s extra=%s missing=%s' % (lab, extra, miss))
check('footnote refs per page', not ref_bad, '%d diffs' % len(ref_bad))
for lab, extra, miss in ref_bad[:20]:
    print('   p.%s extra=%s missing=%s' % (lab, extra, miss))
check('footnote defs per page', not def_bad, '%d diffs' % len(def_bad))
for lab, extra, miss in def_bad[:20]:
    print('   p.%s extra=%s missing=%s' % (lab, extra, miss))
check('zł/gr tokens per page', not cur_bad, '%d diffs' % len(cur_bad))
for lab, extra, miss in cur_bad[:20]:
    print('   p.%s extra=%s missing=%s' % (lab, extra, miss))

# 6. sigla inventory over the covered zone
def zone(txt, blocks_d):
    out = []
    for lab, bl in blocks_d.items():
        if lab.isdigit() and 1 <= int(lab) <= 122 or \
           lab.isdigit() and 145 <= int(lab) <= 157:
            out.append(bl)
    return norm('\n'.join(out))


zs, zt = zone(norm(S), sb), zone(norm(T), tb)
SIGLA = [(r'(?<![A-Za-z])A[WV]\.', 'AW.'), (r'(?<![A-Za-z])A\.?M\.', 'AM.'),
         (r'(?<![A-Za-z])AGH', 'AGH'),
         (r'(?<![A-Za-z])Rel\.? ?Posn[.,]', 'Rel. Posn.'),
         (r'(?<![A-Za-z])Rel\.? ?Cost[.,]', 'Rel. Cost.'),
         (r'(?<![A-Za-z])Rel\.? ?Valc', 'Rel. Valc.'),
         (r'(?<![A-Za-z])Rel\.? ?Vsch', 'Rel. Vsch.'),
         (r'(?<![A-Za-z])Decr\.? ?Posn', 'Decr. Posn.'),
         (r'(?<![A-Za-z])Inscr\.? ?Valc', 'Inscr. Valc.'),
         (r'(?<![A-Za-z])Dom\.? ?P', 'Dom. P.'),
         (r'(?<![A-Za-z])K[l\]]\. ?XII', 'Kl. XII'),
         (r'(?<![A-Za-z])K[l\]]\. ?M\b', 'Kl. M.'),
         (r'(?<![A-Za-z])Tp\.? 89', 'Tp. 89'), (r'(?<![A-Za-z])Tp\.? 90', 'Tp. 90'),
         (r'(?<![A-Za-z])To[d]\.? 89', 'Tod. 89'),
         (r'(?<![A-Za-z])Tol\.', 'Tol.'),
         (r'(?<![A-Za-z])Tołł\.', 'Tołł.'), (r'(?<![A-Za-z])TKS\.? 72', 'TKS. 72'),
         (r'(?<![A-Za-z])TW\b', 'TW'), (r'(?<![A-Za-z])MP\b', 'MP'),
         (r'(?<![A-Za-z])MGd', 'MGd'), (r'(?<![A-Za-z])M\. ?Schr\.', 'M. Schr.'),
         (r'(?<![A-Za-z])O 83', 'O 83'), (r'(?<![A-Za-z])VO\b', 'VO'),
         (r'(?<![A-Za-z])Szk\.', 'Szk.'), (r'(?<![A-Za-z])Kośc\.', 'Kośc.'),
         (r'(?<![A-Za-z])Kat\.', 'Kat.'), (r'Verz/1800', 'Verz/1800'),
         (r'Verz/1845', 'Verz/1845'), (r'(?<![A-Za-z])Wol\.? ?Leg', 'Wol. Leg.')]
for pat, name in SIGLA:
    ns = len(re.findall(pat, zs))
    nt = len(re.findall(pat, zt))
    if ns != nt:
        check('siglum %s (%d)' % (name, ns), False, 'tgt %d' % nt)
check('siglum inventory', ok)

# 7. table structure: count pipe rows per contiguous table region
def tables(txt_blocks):
    regs, cur = [], None
    for lab in ls:
        rows = [l for l in txt_blocks[lab].splitlines()
                if l.strip().startswith('|')]
        if rows:
            if cur is None:
                cur = [lab, 0, len(rows[0].split('|')) - 2]
            cur[1] += len(rows)
        else:
            if cur is not None:
                regs.append(cur)
                cur = None
    if cur is not None:
        regs.append(cur)
    # a lone '|' line is scan noise, not a table (p. 17 dropped in the
    # translation, agent-documented); regions with no columns skip
    return [r for r in regs if r[2] > 0]


ts, tt = tables(sb), tables(tb)
check('table regions', len(ts) == len(tt),
      'src %s / tgt %s' % ([(r[0], r[1], r[2]) for r in ts],
                           [(r[0], r[1], r[2]) for r in tt]))
for a, b in zip(ts, tt):
    check('table @p.%s rows %d cols %d' % (a[0], a[1], a[2]),
          a[1:] == b[1:], 'tgt p.%s rows %d cols %d' % (b[0], b[1], b[2]))

print()
print('BATTERY %s' % ('ALL PASS' if ok else 'FAILURES PRESENT'))
