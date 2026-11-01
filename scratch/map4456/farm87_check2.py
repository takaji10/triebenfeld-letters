# Farm 87, take two: the reading is grouped by its site clusters. The 87
# sites: two at (9506-9552, 9721-9879) [the south pair, 132 px apart],
# and (3718-4058, 9213-9556) [the west pair], (3754,7083)/(5329,6913)
# [the north]. Ask the editor which figures belong to which, but first
# test the plausible groupings arithmetically.
import itertools

readings = [
    ("1.", "288"), ("1.", "1-50"), ("", "68"), ("", "47"),
    ("2.", "1-867"), ("-", "102"), ("", "37"), ("", "28"),
    ("2.", "1-2005"), ("-", "74"), ("-", "8"), ("-", "432"),
    ("", "301"), ("", "36"), ("", "12"), ("", "2"),
]
def val(a):
    if "-" in a:
        d, s = a.split("-")
        return int(d) * 2400 + int(s) if d else int(s)
    return int(a)
pieces = [(l, a, val(a)) for l, a in readings]

# the row's figures
rt = 7 * 2400 + 2330           # 19130
cols = {"buildings": 321, "arable": 9221, "meadow": 0, "pasture": 9180,
        "unusable": 408}

# Try: the SLED (the homestead) is plot 1 near the south pair; the sum of
# all identified = rt. Which subset assignment closes? Since identified
# total was only 4/1957 of 19130, MOST of the farm was outside the crops.
# The question the check can still answer: does 288+1-50 (plot 1) = a
# column? 338 vs buildings 321: off 17 (digit misread 1-45 -> 298+... no).
# Test alternatives:
print("plot sums:")
p1 = 288 + (1 * 2400 + 50)
p2 = (1 * 2400 + 867) + (1 * 2400 + 2005)
print("  plot 1: 288 + 1-50 =", p1, "(vs buildings 321, off %+d)" % (p1 - 321))
print("  plot 2: 1-867 + 1-2005 =", p2, "(vs pasture 9180, off %+d)" % (p2 - 9180))
print("  plot 1+2 =", p1 + p2, " (vs arable 9221, off %+d)" % (p1 + p2 - 9221))
# the tracks sum 1147 vs unusable 408: too big; but 408 = 301+68+37+2? = 408!
cands = [301, 68, 37, 2]
print("\nthe unusable hunt: 408 = ")
for c in itertools.combinations([68, 47, 102, 37, 28, 74, 8, 432, 301, 36, 12, 2], 4):
    if sum(c) == 408:
        print("   ", c)
for c in itertools.combinations([68, 47, 102, 37, 28, 74, 8, 432, 301, 36, 12, 2], 3):
    if sum(c) == 408:
        print("   ", c)
# nearest single-piece explanations of buildings 321: 301 (off -20), 288 (off -33)
# the reading "1. 288" + "301"? or plot 1 = 301?
print("\nbuildings 321: candidates 288 (off -33), 301 (off -20), 432 (off +111)")
print("  301 + 2? = 303;  288 + 2 + 12 + ... ")
for c in itertools.combinations([2, 12, 36], 2):
    print("   288 +", c, "=", 288 + sum(c))
