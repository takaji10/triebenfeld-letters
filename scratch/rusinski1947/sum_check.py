# -*- coding: utf-8 -*-
"""Column-sum check of the annex series against the printed totals."""
import re

t = open(r'literature\rusinski1947\original.md', encoding='utf-8').read()
i0 = t.find('<!-- annex sheet 0139 -->')
i1 = t.find('<!-- annex sheet 0147 -->')
i2 = t.find('<!-- annex sheet 0158 -->')
i3 = t.find('<!-- annex sheet 0159 -->')


def parse(seg):
    rows = {}
    for ln in seg.splitlines():
        m = re.match(r'\| (\d+) \| ', ln)
        if m:
            cells = [c.strip(' |') for c in ln.split(' | ')]
            rows[int(m.group(1))] = cells
    return rows


def val(cells, k):
    v = cells[k].replace('*', '').strip()
    if re.fullmatch(r'[\d.]+', v):
        return float(v.replace('.', ''))
    return None


a = parse(t[i0:i1])
b = parse(t[i1:i2])
c = parse(t[i2:i3])
for tag, rows, tot in (('a', a, (2386, 92, 12967)),
                       ('b', b, (2071, 38, 4484)),
                       ('c', c, None)):
    print('===', tag, len(rows), 'rows')
    for k, want in ((8, tot[0] if tot else None),
                    (9, tot[1] if tot else None),
                    (10, tot[2] if tot else None)):
        s = 0
        n = 0
        bad = []
        dash = 0
        for num, cells in sorted(rows.items()):
            v = val(cells, k)
            if v is None:
                if cells[k].strip() in ('—', '-', ''):
                    dash += 1
                else:
                    bad.append((num, cells[k]))
            else:
                s += v
                n += 1
        print(' col%d: sum=%s clean=%d dash/empty=%d JUNK=%d want=%s'
              % (k + 1, s, n, dash, len(bad), want))
        for num, j in bad:
            print('    r%d %r' % (num, j[:44]))
