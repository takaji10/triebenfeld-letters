# -*- coding: utf-8 -*-
"""Copy the photographed pages of APP 53/968/0/-/782 into processed/.

The holding is one photographed document of two pages (no fold, no two-up
opening), so intake is a copy: Image00002.jpg and Image00003.jpg become
Image0002_a.jpg and Image0003_a.jpg in <raw_dir>/processed/ (four digits,
the page-id grammar the pipeline parses).

Image00001.jpg is left out on purpose (the editor, 2026-10-25): it is the
title page of the holding, not a page of the document, and is not
transcribed. stage_pages.py will report it as left out; that is the record.

Run:  python units/app539680782/intake/build_pages.py
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
import unitlib

UNIT = unitlib.one_unit('app539680782')
RAW = os.path.join(UNIT.raw_dir, 'processed')
os.makedirs(RAW, exist_ok=True)

# The title page 00001 is not a page of the document and is not copied.
for n in (2, 3):
    src = os.path.join(UNIT.raw_dir, f'Image{n:05d}.jpg')
    dst = os.path.join(RAW, f'Image{n:04d}_a.jpg')
    if not os.path.isfile(dst):
        shutil.copyfile(src, dst)
        print('copied', os.path.basename(dst))
    else:
        print('already there', os.path.basename(dst))
