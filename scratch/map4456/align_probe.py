# Do row/column alignment of tokens separate the info blocks from the map?
# For the labeled points, count token row-mates (same y-band) and
# column-mates (same x-band) among all OCR tokens.
import json
import math

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld"
RED = json.load(open(ROOT + r"\scratch\map4456\numbers_easy2.json", encoding="utf-8"))
BLACK = json.load(open(ROOT + r"\scratch\map4456\numbers_black.json", encoding="utf-8"))
ALL = [{"src": "red", **t} for t in RED] + [{"src": "black", **t} for t in BLACK]

INFO = [
    ("expl 1454", 5338, 1286), ("expl 1883", 5335, 1483),
    ("expl 335", 5379, 1559), ("expl 219", 5373, 1071),
    ("title 1896a", 952, 1352), ("title 1896b", 3064, 1750),
    ("s1 11a", 1570, 1476), ("s1 11b", 2592, 1766),
    ("s1 47", 1260, 1880), ("s1 14", 4683, 1505),
]
MAP_ = [
    ("farm78", 3847, 6371), ("farm49", 5423, 8654), ("farm84", 4751, 5713),
    ("farm11e", 17769, 11984), ("farm50a", 5974, 10546),
    ("farm92", 9504, 9896), ("farm86", 6970, 5153), ("farm88", 19978, 12188),
    ("farm64", 18798, 12315), ("farm54", 19612, 10949),
]
for tag, pts in (("INFO", INFO), ("MAP ", MAP_)):
    print(tag)
    for name, x, y in pts:
        col = sum(1 for t in ALL
                  if abs(t["x"] - x) <= 60 and 80 < abs(t["y"] - y) <= 700)
        row = sum(1 for t in ALL
                  if abs(t["y"] - y) <= 45 and 80 < abs(t["x"] - x) <= 2400)
        print("   %-12s col-mates %2d  row-mates %2d" % (name, col, row))
