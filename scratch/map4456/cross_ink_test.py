# The editor's second field observation: the black leading n stays small
# (1..8 - a parcel index), the red numbers run into the 60s and higher
# (candidate farm numbers, 1..97). Test on the region's tokens:
# 1) the red small-value distribution; 2) the cross-ink test: a red n with
#    black D-S labels nearby whose areas sum to row n's statement total.
import json
import math
import re
import collections

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld"
REF = json.load(open(ROOT + r"\scratch\map4456\reference_numbers.json", encoding="utf-8"))
REG = json.load(open(ROOT + r"\scratch\map4456\region_tokens.json", encoding="utf-8"))
stmt = REF["statement"]
row_total = {int(n): r["total"]["des"] * 2400 + r["total"]["saz"]
             for n, r in stmt.items() if n.isdigit()}

def norm_parts(t):
    t = t.strip().strip(".,-/").strip()
    out = []
    for p in t.replace("/", " ").replace(",", " ").replace(".", " ").replace("-", " ").split():
        if p.isdigit():
            out.append(int(p))
    if t.isdigit() and int(t) not in out:
        out.append(int(t))
    return out

reds, blacks = REG["red"], REG["black"]
print("region tokens: red %d, black %d" % (len(reds), len(blacks)))

# ---- 1) the red small-value distribution ------------------------------------
small_red = []
for t in reds:
    ps = norm_parts(t["text"])
    if len(ps) == 1 and 1 <= ps[0] <= 97 and t["conf"] >= 0.5:
        small_red.append({"v": ps[0], "x": t["x"] + t["w"] // 2,
                          "y": t["y"] + t["h"] // 2, "conf": t["conf"]})
cnt = collections.Counter(r["v"] for r in small_red)
print("\nred small values (1..97, conf>=0.5):", len(small_red), "tokens,",
      len(cnt), "distinct")
print("distribution:", sorted(cnt.items()))
buckets = collections.Counter()
for v, c in cnt.items():
    buckets[(v - 1) // 10] += c
print("by decade:", sorted(buckets.items()))

# ---- 2) the cross-ink test ---------------------------------------------------
# black D-S labels from the existing tokens (few; the region re-read will
# add more, but the test is worth running on what we have)
pairs = []
for t in blacks:
    s = t["text"].strip()
    m = re.fullmatch(r"[-.\s]*(\d{1,2})\s*[-/.,]\s*(\d{3,4})[-.\s]*", s)
    if m:
        d, sa = int(m.group(1)), int(m.group(2))
        if d <= 60 and sa <= 2399:
            pairs.append({"d": d, "s": sa, "x": t["x"] + t["w"] // 2,
                          "y": t["y"] + t["h"] // 2, "conf": t["conf"]})
# plus the stacked pairs from the earlier stack work
STACKS = json.load(open(ROOT + r"\scratch\map4456\red_stacks.json", encoding="utf-8"))
# (red stacks: des above saz; keep only those inside the region? they were
#  built from the whole map; keep all, the radius test guards)
for st in STACKS:
    if st.get("d") is not None:
        pairs.append({"d": st["d"], "s": st["s"], "x": st["x"], "y": st["y"],
                      "conf": st["conf"]})
print("\nblack D-S pairs available:", len(pairs))

R = 520
hits = []
for r in small_red:
    n = r["v"]
    near = [p for p in pairs if math.hypot(p["x"] - r["x"], p["y"] - r["y"]) <= R]
    # try every subset sum? cheap version: all subsets up to 6 pairs
    best = None
    for k in range(1, min(7, len(near) + 1)):
        from itertools import combinations
        for combo in combinations(near, k):
            tot = sum(p["d"] * 2400 + p["s"] for p in combo)
            rt = row_total.get(n)
            if rt and abs(tot - rt) <= 0.06 * rt:
                best = (combo, tot, rt)
                break
        if best:
            break
    if best:
        combo, tot, rt = best
        hits.append((n, r, combo, tot, rt))
print("\nred n with a nearby black-parcel sum == row n's total (6%):", len(hits))
for n, r, combo, tot, rt in hits:
    print("  red %2d at (%d,%d): %d parcels sum %d/%d ~ row %d %d/%d  [%s]" % (
        n, r["x"], r["y"], len(combo), tot // 2400, tot % 2400, n,
        rt // 2400, rt % 2400,
        stmt[str(n)]["name"][:22]))
