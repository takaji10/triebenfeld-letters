# -*- coding: utf-8 -*-
import re
t = open(r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba'
         r'\rusinski1947\literature\rusinski1947\SPOT_SHEET.html',
         encoding='utf-8').read()
print('item divs:', t.count('class="item"'))
print('id="S01" div:', t.count('id="S01"'))
print('radio name="S01":', t.count('name="S01"'))
ids = re.findall(r'class="item" id="([^"]+)"', t)
print('ids:', ids)
i = t.find('class="nav"')
j = t.find('</div>', i)
print('nav:', t[i:j][:250])
