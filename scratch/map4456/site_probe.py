# Probe the strong black sites: all red tokens within 450 px, their row
# matches, and the neighbouring rows. Sites: 49/50 cluster, 92, 84, 11, 78.
import json
import math
import collections
from geo_fit import px_to_ll

REF = json.load(open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\reference_numbers.json", encoding="utf-8"))
BLACK = json.load(open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\numbers_black.json", encoding="utf-8"))
RED = json.load(open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\numbers_easy2.json", encoding="utf-8"))
stmt = REF["statement"]

def norm_parts(t):
    t = t.strip().strip(".,-/").strip()
    out = []
    for p in t.replace("/", " ").replace(",", " ").replace(".", " ").replace("-", " ").split():
        if p.isdigit():
            out.append(int(p))
    if t.isdigit() and int(t) not in out:
        out.append(int(t))
    return out

reds = []
for t in RED:
    if t["conf"] < 0.4 or t["kind"] != "red":
        continue
    ps = norm_parts(t["text"])
    if not ps:
        continue
    reds.append({**t, "v": max(ps)})

val_rows = collections.defaultdict(list)
for rn in stmt:
    if not rn.isdigit():
        continue
    row = stmt[rn]
    for col in ("buildings", "arable", "meadow", "pasture", "unusable", "total"):
        d, s = row[col]["des"], row[col]["saz"]
        if d:
            val_rows[d].append((rn, col + "/des"))
        if s:
            val_rows[s].append((rn, col + "/saz"))

SITES = [
    ("49 conf0.99", 5423, 8654, (49,)),
    ("49 conf0.86", 5246, 10534, (49,)),
    ("50 conf0.93", 5974, 10546, (50,)),
    ("50 conf0.76", 3248, 9224, (50,)),
    ("92 school?", 9504, 9896, (92, 93, 94, 95)),
    ("84 anchor", 4751, 5713, (84,)),
    ("11 strong", 17769, 11984, (11,)),
    ("78 strong", 3847, 6371, (78, 79)),
    ("66 pair", 4926, 5902, (66,)),
    ("86 strong", 6970, 5153, (86,)),
    ("54 east", 19612, 10949, (54,)),
    ("64 east", 18798, 12315, (64,)),
]
R = 460
for label, x, y, rows_of_interest in SITES:
    print("=== %s at (%d,%d) ll(%.5f,%.5f)" % (label, x, y, *px_to_ll(x, y)))
    for rn in rows_of_interest:
        if str(rn) in stmt:
            row = stmt[str(rn)]
            cols = ", ".join("%s %d/%d" % (c[:4], row[c]["des"], row[c]["saz"])
                             for c in ("buildings", "arable", "meadow", "pasture", "unusable", "total"))
            print("    row %s %s: %s" % (rn, row["name"][:24], cols))
    near = [r for r in reds if math.hypot(r["x"] - x, r["y"] - y) <= R]
    near.sort(key=lambda r: math.hypot(r["x"] - x, r["y"] - y))
    for r in near[:14]:
        refs = val_rows.get(r["v"], [])
        mine = [f for f in refs if f[0] in [str(rn) for rn in rows_of_interest]]
        mark = "  <<< " + "; ".join("%s/%s" % f for f in mine) if mine else ""
        uniq = " (1 row)" if len({f[0] for f in refs}) == 1 else ""
        print("    red %-7s conf %.2f d %4d%s%s" % (
            r["text"], r["conf"], int(math.hypot(r["x"] - x, r["y"] - y)),
            (" -> " + ", ".join("%s/%s" % f for f in refs[:5]) + uniq) if refs else "", mark))
    print()
