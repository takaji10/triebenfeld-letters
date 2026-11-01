# Around the two confirmed anchors, do the neighbouring tokens carry the
# same row's other figures? (the strongest local check)
import json
import math
import collections

REF = json.load(open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\reference_numbers.json", encoding="utf-8"))
TOK = json.load(open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\numbers_easy2.json", encoding="utf-8"))
stmt = REF["statement"]

for rn in ("84", "21"):
    r = stmt[rn]
    print("row", rn, r["name"])
    for k, v in r.items():
        if k != "name":
            print("   %-10s %d des %4d saz" % (k, v["des"], v["saz"]))

def norm_parts(t):
    t = t.strip().strip(".,-/").strip()
    out = []
    for p in t.replace("/", " ").replace(",", " ").replace(".", " ").replace("-", " ").split():
        if p.isdigit():
            out.append(int(p))
    if t.isdigit() and int(t) not in out:
        out.append(int(t))
    return out

toks = []
for t in TOK:
    if t["conf"] < 0.35:
        continue
    toks.append({**t, "parts": norm_parts(t["text"])})

ANCHORS = [("84 total (4,1684)", 4751, 5713, "84"),
           ("21 unusable (0,219)", 5373, 1071, "21")]
R = 550
for label, ax, ay, rn in ANCHORS:
    row = stmt[rn]
    rvals = {}   # value -> kinds
    for k, v in row.items():
        if k == "name":
            continue
        if v["des"]:
            rvals.setdefault(v["des"], []).append(k + "/des")
        if v["saz"]:
            rvals.setdefault(v["saz"], []).append(k + "/saz")
    print("\n=== %s at (%d,%d); row %s = %s; looking within %d px:" %
          (label, ax, ay, rn, row["name"], R))
    near = [t for t in toks if math.hypot(t["x"] - ax, t["y"] - ay) <= R]
    near.sort(key=lambda t: (t["y"], t["x"]))
    for t in near:
        hits = [", ".join(rvals[v]) for v in t["parts"] if v in rvals]
        mark = "  <<< " + "; ".join(hits) if hits else ""
        print("   %-9s conf %.2f at (%5d,%5d) rel (%+4d,%+4d)%s" %
              (t["text"], t["conf"], t["x"], t["y"], t["x"] - ax, t["y"] - ay, mark))
