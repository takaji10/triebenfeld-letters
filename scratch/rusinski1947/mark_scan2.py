# -*- coding: utf-8 -*-
"""Loose trailing-mark scan over the a/b-series sheets: for every row,
list the nazwa cell's trailing ink groups with bbox and a high-zoom OCR
of the last group, so genuine superscript refs can be told apart from
name letters. Report -> $env:TEMP\\opencode\\marks2.txt"""
import io, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from pipeline.ocr import read
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
OCR = r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\tom5_ocr'
at = json.load(open(os.path.join(OCR, 'annex_table.json'), encoding='utf-8'))

# rule x-positions per sheet (mid-table band scans, verified above)
RULES = {
    '0139': [798, 996, 1865, 2361, 2917, 3202, 3693, 4189, 4528, 4794, 5025, 5255],
    '0140': [856, 1052, 1920, 2415, 2960, 3242, 3738, 4227, 4565, 4829, 5060, 5290],
    '0141': [823, 1019, 1882, 2375, 2927, 3210, 3699, 4195, 4531, 4796, 5027, 5253],
    '0142': [877, 1070, 1930, 2425, 2967, 3247, 3742, 4232, 4567, 4830, 5057, 5281],
    '0143': [863, 1056, 1925, 2413, 2957, 3241, 3725, 4217, 4546, 4809, 5037, 5263],
    '0144': [892, 1084, 1944, 2437, 2978, 3254, 3744, 4238, 4566, 4827, 5053, 5275],
    '0145': [869, 1064, 1929, 2417, 2962, 3245, 3727, 4218, 4550, 4814, 5041, 5268],
    '0146': [882, 1075, 1929, 2419, 2962, 3242, 3731, 4218, 4549, 4809, 5036, 5263],
    '0147': [865, 1058, 1917, 2408, 2955, 3236, 3721, 4217, 4552, 4813, 5040, 5264],
    '0148': [874, 1067, 1927, 2421, 2967, 3246, 3741, 4233, 4566, 4828, 5055, 5279],
    '0149': [857, 1054, 1914, 2404, 2950, 3233, 3720, 4212, 4544, 4805, 5031, 5258],
    '0150': [868, 1059, 1913, 2406, 2944, 3222, 3717, 4212, 4544, 4808, 5037, 5264],
    '0151': [865, 1060, 1920, 2404, 2950, 3233, 3720, 4212, 4544, 4805, 5031, 5258],
    '0152': [899, 1088, 1913, 2402, 2946, 3247, 3738, 4228, 4561, 4822, 5050, 5277],
    '0153': [852, 1047, 1906, 2399, 2946, 3232, 3718, 4208, 4542, 4804, 5029, 5256],
    '0154': [873, 1064, 1919, 2408, 2955, 3228, 3723, 4211, 4545, 4809, 5037, 5263],
    '0155': [861, 1056, 1919, 2408, 2954, 3238, 3724, 4214, 4548, 4810, 5035, 5262],
    '0156': [899, 1088, 1913, 2402, 2946, 3247, 3738, 4228, 4561, 4822, 5050, 5277],
    '0157': [829, 1025, 1890, 2385, 2934, 3218, 3705, 4199, 4536, 4799, 5027, 5255],
}

out = []
for n in sorted(RULES):
    with open(os.path.join(SRC, 'tom5_%s.tif' % n), 'rb') as fh:
        im = Image.open(io.BytesIO(fh.read())).convert('L')
    im.load()
    px = im.load()
    rules = RULES[n]
    nums = sorted(int(k) for k in at[n]['rows'] if k.isdigit())
    out.append('=== %s rows %d-%d' % (n, nums[0], nums[-1]))
    for num in nums:
        y0, y1 = at[n]['rows'][str(num)]['y']
        cols = []
        prev = False
        for x in range(rules[1] + 6, rules[2] - 6):
            dark = any(px[x, y] < 175 for y in range(y0 + 10, y1 - 5))
            if dark and not prev:
                a = x
            if prev and not dark:
                if x - a > 1:
                    cols.append((a, x))
            prev = dark
        if len(cols) < 2:
            continue
        last = cols[-1]
        gap = last[0] - cols[-2][1]
        w = last[1] - last[0]
        ys = [y for y in range(y0, y1) if any(px[x, y] < 175
              for x in range(last[0], last[1] + 1))]
        h = (max(ys) - min(ys)) if ys else 0
        # candidate sup: small width, some gap, low height
        if gap >= 8 and 8 <= w <= 45 and h <= 40:
            c = im.crop((last[0] - 4, min(ys) - 4, last[1] + 5,
                         max(ys) + 5))
            c = c.resize((c.size[0] * 8, c.size[1] * 8), Image.LANCZOS)
            p = os.path.join(OCR, 'cell_tmp.png')
            c.save(p)
            outs = []
            for psm in (10, 8):
                try:
                    t = read(p, lang='pol', psm=psm).strip()
                    if t and t not in outs:
                        outs.append(t)
                except Exception:
                    pass
            out.append('  r%d SUP? x%d-%d w%d gap%d h%d ocr=%s | %r'
                       % (num, last[0], last[1], w, gap, h,
                          '/'.join(outs),
                          at[n]['rows'][str(num)].get('raw', '')[:55]))
with open(r'C:\Users\Tersnaus\AppData\Local\Temp\opencode\marks2.txt',
          'w', encoding='utf-8') as fh:
    fh.write('\n'.join(out) + '\n')
print('done')
