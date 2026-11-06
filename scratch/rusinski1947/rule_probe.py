# -*- coding: utf-8 -*-
"""Profile the darkness around an editor separator line: is there a
print rule? What x-span does it cover?"""
import os, io, sys
sys.path.insert(0, r'C:\Users\Tersnaus\.local\share\opencode\worktree\14ffba\rusinski1947')
from PIL import Image

SRC = r'C:\Users\Tersnaus\Downloads\tom5'
n = sys.argv[1]
yc = int(sys.argv[2])
with open(os.path.join(SRC, f'tom5_{n}.tif'), 'rb') as fh:
    im = Image.open(io.BytesIO(fh.read())).convert('L')
im.load()
W, H = im.size
px = im.load()
for y in range(yc - 14, yc + 15):
    # darkness in 8 x-windows
    wins = []
    for x0 in range(200, 3800, 450):
        vals = [px[x, y] for x in range(x0, min(W, x0 + 450), 6)]
        wins.append(sum(1 for v in vals if v < 150))
    print(y, wins)
