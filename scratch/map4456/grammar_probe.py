# The "D-S" grammar in the existing OCR tokens: black tokens carrying a
# des-saz pair (n-m with a hyphen or slash), and small tokens stacked above
# them (the parcel number). The user's reading: "3 // 1-662" = parcel 3,
# 1 des 662 saz. Do the pairs fall in plausible ranges (D 0..60, S 0..2399)?
import json
import re
import collections

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld"
BLACK = json.load(open(ROOT + r"\scratch\map4456\numbers_black.json", encoding="utf-8"))
RED = json.load(open(ROOT + r"\scratch\map4456\numbers_easy2.json", encoding="utf-8"))

def show(t):
    return ("%s %-8r conf %.2f drawn=%s at (%5d,%5d) %dx%d"
            % (t.get("kind", t.get("src", "?")), t["text"], t["conf"],
               t.get("drawn"), t["x"], t["y"], t["w"], t["h"]))

print("=== black tokens with a hyphen or slash ===")
pairs = []
for t in BLACK:
    s = t["text"].strip()
    if not t.get("drawn"):
        continue
    m = re.fullmatch(r"[-.\s]*(\d{1,2})\s*[-/.,]\s*(\d{3,4})[-.\s]*", s)
    if m:
        d, sa = int(m.group(1)), int(m.group(2))
        pairs.append({"d": d, "s": sa, "t": t})
        print("  ", show(t), " -> des %d saz %d %s" % (
            d, sa, "(plausible)" if d <= 60 and sa <= 2399 else "(OUT OF RANGE)"))
print("total D-S black pairs:", len(pairs))

print("\n=== black tokens that are bare 3-4 digit numbers (possible saz-only) ===")
n = 0
for t in BLACK:
    if not t.get("drawn") or t["conf"] < 0.6:
        continue
    s = t["text"].strip().strip(".,")
    if s.isdigit() and 100 <= int(s) <= 2399:
        n += 1
        if n <= 40:
            print("  ", show(t))
print("total:", n)

print("\n=== small black tokens (1-2 digits) near a D-S pair (the parcel no.) ===")
for p in pairs:
    t = p["t"]
    near = [b for b in BLACK
            if b.get("drawn") and b is not t
            and abs(b["x"] - t["x"]) < 90
            and 0 < t["y"] - b["y"] <= 130
            and b["text"].strip().strip(".,").isdigit()
            and int(b["text"].strip().strip(".")) <= 97]
    if near:
        print("   D-S %d-%d at (%d,%d) <- above: %s" % (
            p["d"], p["s"], t["x"], t["y"],
            ", ".join("'%s' conf %.2f dy %d" % (b["text"].strip(), b["conf"], t["y"] - b["y"])
                      for b in near)))
