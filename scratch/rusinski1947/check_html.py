# -*- coding: utf-8 -*-
import re
t = open(r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947\literature\rusinski1947\SPOT_SHEET.html',
         encoding='utf-8').read()
print('leftover tokens:', t.count('@@'))
print('data URIs:', t.count('data:image/png;base64'))
print('items:', t.count('class="item"'))
print('tables:', t.count('<table>'))
missing = [i for i in re.findall(r'<div class="item" id="([^"]+)"', t)
           if ('name="%s"' % i) not in t]
print('missing answer forms:', missing)
print('ids in JS:', t.count('const IDS'))
