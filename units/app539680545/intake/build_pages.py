# -*- coding: utf-8 -*-
"""Copy the ten photographed sheets of APP 53/968/0/-/545 into processed/.

Each archive image is one photographed sheet (no fold, no two-up opening),
so intake is a copy: Image00025.jpg to Image00034.jpg become
Image0025_a.jpg ... Image0034_a.jpg in <raw_dir>/processed/ (four digits,
the page-id grammar the pipeline parses).

Image00024.jpg is left out on purpose (the editor, 2026-10-25): it is the
photograph of the folder that holds the sheets, not a page, and is not
transcribed. stage_pages.py will report it as left out; that is the record.

Run:  python units/app539680545/intake/build_pages.py
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), 'pipeline'))
import unitlib

UNIT = unitlib.one_unit('app539680545')
RAW = os.path.join(UNIT.raw_dir, 'processed')
os.makedirs(RAW, exist_ok=True)

# The folder photograph 00024 is not a page and is not copied.
for n in range(25, 35):
    src = os.path.join(UNIT.raw_dir, f'Image{n:05d}.jpg')
    dst = os.path.join(RAW, f'Image{n:04d}_a.jpg')
    if not os.path.isfile(dst):
        shutil.copyfile(src, dst)
        print('copied', os.path.basename(dst))
    else:
        print('already there', os.path.basename(dst))
