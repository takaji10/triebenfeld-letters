# -*- coding: utf-8 -*-
"""Copy the scan of APP 53/4/0/-/62, page 222, into processed/.

The holding is one page taken from the archive's online unit
(szukajwarchiwach.gov.pl, jednostka 980058, scan 231 of 349): the editor's
download 53_4_0_-_62_18049603.jpg, manuscript page 222. Intake is a copy:
the file becomes 0222_a.jpg in <raw_dir>/processed/ (four digits, the page-id
grammar the pipeline parses; the number is the manuscript's own pagination).

The rest of the volume is not among the scans; the entry is the one the
editor chose, at the foot of the page.

Run:  python units/app534062/intake/build_pages.py
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), 'pipeline'))
import unitlib

UNIT = unitlib.one_unit('app534062')
RAW = os.path.join(UNIT.raw_dir, 'processed')
os.makedirs(RAW, exist_ok=True)

src = os.path.join(UNIT.raw_dir, '53_4_0_-_62_18049603.jpg')
dst = os.path.join(RAW, '0222_a.jpg')
if not os.path.isfile(dst):
    shutil.copyfile(src, dst)
    print('copied', os.path.basename(dst))
else:
    print('already there', os.path.basename(dst))
