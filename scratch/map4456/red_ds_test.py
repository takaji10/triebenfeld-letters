# The editor's red D-S readings: if the areas can be red, the 26 red D-S
# pairs may be the actual parcels of the farms marked by the red numbers.
# Test 1: does any red D-S label sit near a red n whose row total equals
# the D-S value alone (a one-parcel farm)? Test 2: do the red D-S labels
# near each other sum, with a nearby red n, to that row's total? Full
# subset search per red value with ALL D-S labels (both inks) at once.
import json
import re
import math
import itertools
import collections

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld"
D = json.load(open(ROOT + r"\scratch\map4456\reds_all.json", encoding="utf-8"))
REF = json.load(open(ROOT + r"\scratch\map4456\reference_numbers.json", encoding="utf-8"))
stmt = REF["statement"]
row_total = {int(n): r["total"]["des"] * 2400 + r["total"]["saz"]
             for n, r in stmt.items() if n.isdigit()}

def canon(t):
    t = t.strip()
    unc = "[" in t
    t = t.replace("[", "").replace("?]", "").replace("?", "")
    return t.strip(), unc

sites, ds = [], []
def take(text, x, y, src):
    c, unc = canon(text)
    m = re.fullmatch(r"(\d{1,2})-(\d{3,4})", c)
    if m and int(m.group(1)) <= 60 and int(m.group(2)) <= 2399:
        ds.append({"d": int(m.group(1)), "s": int(m.group(2)),
                   "x": x, "y": y, "src": src, "unc": unc})
        return
    if re.fullmatch(r"\d{1,2}", c):
        sites.append({"v": int(c), "x": x, "y": y, "unc": unc})
for a in D["answered"]:
    x, y = a["x"], a["y"]
    if a.get("fixed"):
        x = a["fixed"]["x"]; y = a["fixed"]["y"]
    take(a["text"], x, y, "sheet")
for n in D["added"]:
    take(n["text"], n["x"] + (n.get("w", 0)) // 2, n["y"] + (n.get("h", 0)) // 2,
         "added")
print("red sites:", len(sites), " red D-S labels:", len(ds))

# the black-OCR parcels as extra candidates
P = json.load(open(ROOT + r"\scratch\map4456\region_parsed.json", encoding="utf-8"))
for p in P.get("parcels", []):
    ds.append({"d": p["d"], "s": p["s"], "x": p["x"], "y": p["y"],
               "src": "black-ocr", "unc": False})
print("D-S candidates total:", len(ds))

R = 700
print("\n== subset-sum test: red n vs ALL nearby D-S labels ==")
hits = []
for n in sorted(set(s["v"] for s in sites)):
    rt = row_total.get(n)
    if not rt:
        continue
    for site in [s for s in sites if s["v"] == n]:
        near = [p for p in ds
                if math.hypot(p["x"] - site["x"], p["y"] - site["y"]) <= R]
        found = None
        for k in range(1, min(9, len(near) + 1)):
            for combo in itertools.combinations(near, k):
                tot = sum(p["d"] * 2400 + p["s"] for p in combo)
                if abs(tot - rt) <= 0.06 * rt:
                    found = (combo, tot)
                    break
            if found:
                break
        if found:
            hits.append((n, site, found))
            break
for n, site, (combo, tot) in hits:
    rt = row_total[n]
    print("  red %2d at (%5.0f,%5.0f): %d parcels [%s] sum %d/%d ~ row %2d %d/%d [%s]"
          % (n, site["x"], site["y"], len(combo),
             "+".join("%d-%d(%s)" % (p["d"], p["s"], p["src"][:4]) for p in combo),
             tot // 2400, tot % 2400, n, rt // 2400, rt % 2400,
             stmt[str(n)]["name"][:22]))
print("hits: %d of %d red values" % (len(hits), len(set(s['v'] for s in sites))))

# the singles: a one-parcel farm's label should equal the row total alone
print("\n== single D-S == row total (one-parcel farms) ==")
for p in ds:
    for n, rt in row_total.items():
        if p["d"] * 2400 + p["s"] == rt:
            near = [s for s in sites
                    if abs(s["v"] - 0) >= 0 and math.hypot(s["x"] - p["x"], s["y"] - p["y"]) <= 500]
            print("  %d-%d at (%5.0f,%5.0f) [%s] == row %d total; red values within 500px: %s"
                  % (p["d"], p["s"], p["x"], p["y"], p["src"], n,
                     sorted(set(s["v"] for s in near))[:12]))
