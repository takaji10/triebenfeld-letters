# -*- coding: utf-8 -*-
import json, os
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
tokmap = {}
pf = json.load(open(os.path.join(OCR, 'pct_frac.json'), encoding='utf-8'))
for k, v in pf.items():
    if v.get('resolved') and v.get('print') not in (None, 'MARKER') \
            and v['print'] != v['tok']:
        key = v['tok'].strip('.,;:!?»”"()')
        tokmap[key] = v['print']
tokmap.update({'5%/': '5%', '10%/': '10%', '36%/': '36%', '20%/': '20%',
               '13.6%%': '13.6%', '750/y': '75%'})
print('map size:', len(tokmap))
text = 'a po doliczeniu szacunkowych 5%/, na szlachtę'
out = []
for tok in text.split(' '):
    core = tok.strip('.,;:!?»”"()')
    if core in tokmap:
        out.append(tok.replace(core, tokmap[core]))
    else:
        out.append(tok)
print(' '.join(out))
