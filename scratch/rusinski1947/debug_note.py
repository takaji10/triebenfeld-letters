# -*- coding: utf-8 -*-
import json, os, re, difflib, sys
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'

def fold(s):
    return re.sub(r'[^a-ząćęłńóśźż0-9]', '', s.lower())

n, k = sys.argv[1], int(sys.argv[2])
s = json.load(open(os.path.join(OCR, 'structure2.json'), encoding='utf-8'))
note = [x for x in s[n]['notes'] if x['num'] == k][0]
d = json.load(open(os.path.join(OCR, 'notetexts', f'{n}_{k}.json'),
                  encoding='utf-8'))
cand = max((d['pol'].strip(), d['std'].strip()),
           key=lambda t: len(re.sub(r'\s', '', t)))
cand_clean = re.sub(r'^[\d!%*+$§£|.,)»\-—–?L\s]+(?=[A-ZĄĆĘŁŃÓŚŹŻ„"(])',
                    '', cand).strip()
pg_clean = re.sub(r'^[\d!%*+$§£|.,)»\-—–\s]+(?=[A-ZĄĆĘŁŃÓŚŹŻ„"(])',
                  '', note['text']).strip()
print('CAND:', repr(cand_clean[:120]))
print('PG  :', repr(pg_clean[:120]))
cw = re.findall(r'[a-ząćęłńóśźż0-9]+', fold(cand_clean))
pw = re.findall(r'[a-ząćęłńóśźż0-9]+', fold(pg_clean))
print('first3 cand:', cw[:3], 'pg:', pw[:3])
print('first-match ratio:', difflib.SequenceMatcher(
    None, ' '.join(cw[:3]), ' '.join(pw[:3])).ratio())
print('len fold cand:', len(fold(cand_clean)), 'pg:', len(fold(pg_clean)),
      'ratio:', difflib.SequenceMatcher(None, fold(cand_clean),
                                        fold(pg_clean)).ratio())
