# -*- coding: utf-8 -*-
import re
p = r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947\scratch\rusinski1947\annex_rows2.py'
t = open(p, encoding='utf-8').read()
assert 'def cell_cands' not in t
block = '''def cell_cands(n, top):
    out = []
    for (x0, x1, sc, ac) in ((860, 1140, 5, False), (840, 1160, 6, False),
                             (860, 1140, 7, True)):
        c = img(n).crop((x0, max(0, top - 8), x1, top + 68))
        c = c.resize((c.size[0] * sc, c.size[1] * sc), Image.LANCZOS)
        if ac:
            c = ImageOps.autocontrast(c)
        c.save(TMP)
        for lang in ('pol', 'pol-std'):
            try:
                tt = read(TMP, lang=lang, psm=7).strip()
            except Exception:
                continue
            for m in re.finditer(r'\\d{1,3}', tt):
                v = int(m.group(0))
                if 1 <= v <= 200 and v not in out:
                    out.append(v)
    return out


'''
anchor = 'def cell_cands_PLACEHOLDER'
i = t.find('def prev_top')
t = t[:i] + block + t[i:]
open(p, 'w', encoding='utf-8').write(t)
print('inserted before prev_top')
