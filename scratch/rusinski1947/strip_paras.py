# -*- coding: utf-8 -*-
import json, os, re, sys
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947\scratch\rusinski1947')
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
n = sys.argv[1] if len(sys.argv) > 1 else '0103'
j = json.load(open(os.path.join(OCR, 'widestrips', n + '.json'),
                  encoding='utf-8'))
for model in ('pol', 'std'):
    paras = [p.strip() for p in re.split(r'\n\s*\n', j[model]) if p.strip()]
    print('===', n, model, 'paragraphs:', len(paras))
    for i, p in enumerate(paras):
        print(i, '|', p[:85].replace('\n', ' / '))
