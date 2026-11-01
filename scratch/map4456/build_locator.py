# The farm locator: every clean black number n (1..97) with the statement's
# holder name and the map position, marked where a nearby red figure
# supports it (value unique to row n in the statement). Output:
# scratch/map4456/farm_locations.csv + .json
import csv
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

blacks = []
for t in BLACK:
    if not t.get("drawn"):
        continue
    ps = norm_parts(t["text"])
    if len(ps) == 1 and 1 <= ps[0] <= 97 and t["conf"] >= 0.6:
        lon, lat = px_to_ll(t["x"] + t["w"] / 2, t["y"] + t["h"] / 2)
        blacks.append({"n": ps[0], "conf": t["conf"], "x": t["x"], "y": t["y"],
                       "lon": round(float(lon), 6), "lat": round(float(lat), 6)})

reds = []
for t in RED:
    if t["conf"] < 0.45 or t["kind"] != "red" or not t.get("drawn"):
        continue
    ps = norm_parts(t["text"])
    if ps:
        reds.append({"v": max(ps), "x": t["x"], "y": t["y"]})

val_rows = collections.defaultdict(set)
for rn in stmt:
    if not rn.isdigit():
        continue
    row = stmt[rn]
    for col in ("buildings", "arable", "meadow", "pasture", "unusable", "total"):
        if row[col]["des"]:
            val_rows[row[col]["des"]].add(int(rn))
        if row[col]["saz"]:
            val_rows[row[col]["saz"]].add(int(rn))

R = 420
out = []
for b in sorted(blacks, key=lambda b: (b["n"], -b["conf"])):
    n = b["n"]
    name = stmt.get(str(n), {}).get("name", "?")
    support = []
    for r in reds:
        if r["v"] < 100:
            continue
        if math.hypot(r["x"] - b["x"], r["y"] - b["y"]) > R:
            continue
        rows = val_rows.get(r["v"], set())
        if n in rows and len(rows) <= 3:
            support.append(r["v"])
    out.append({**b, "holder": name,
                "support": support,
                "status": "supported" if support else "candidate"})

with open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\farm_locations.csv", "w",
          newline="", encoding="utf-8") as f:
    wr = csv.DictWriter(f, fieldnames=["n", "holder", "conf", "lon", "lat", "x", "y",
                                       "status", "support"])
    wr.writeheader()
    wr.writerows(out)

sup = [o for o in out if o["status"] == "supported"]
print("black farm-number sites:", len(out), " supported:", len(sup))
for o in sup:
    print("  farm %2d %-30s conf %.2f ll(%.5f,%.5f) support %s"
          % (o["n"], o["holder"][:30], o["conf"], o["lon"], o["lat"], o["support"]))
json.dump(out, open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\farm_locations.json", "w",
                    encoding="utf-8"), ensure_ascii=False, indent=1)
