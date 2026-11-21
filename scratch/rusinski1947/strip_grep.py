# -*- coding: utf-8 -*-
import json, os, sys
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
n = sys.argv[1] if len(sys.argv) > 1 else '0021'
needle = sys.argv[2] if len(sys.argv) > 2 else 'Kaczmarczyk'
j = json.load(open(os.path.join(OCR, 'widestrips', n + '.json'),
                  encoding='utf-8'))
for model in ('pol', 'std'):
    for l in j[model].split('\n'):
        if needle in l:
            print(model, repr(l[:100]))
