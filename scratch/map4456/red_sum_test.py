# The decisive sum test with the editor's true positions: for each red
# value n, take the D-S area labels (the editor's red D-S readings + the
# OCR's black D-S parcels + red stacks) near its sites, and test whether
# subsets sum to row n's statement total.
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

# red sites (as in analyze_reds)
sites = []
ds_all = []     # every D-S label with a position: red (editor) + black (OCR)
for a in D["answered"]:
    c, unc = canon(a["text"])
    x, y = a["x"], a["y"]
    if a.get("fixed"):
        x = a["fixed"]["x"]; y = a["fixed"]["y"]
    m = re.fullmatch(r"(\d{1,2})-(\d{3,4})", c)
    if m and int(m.group(1)) <= 60 and int(m.group(2)) <= 2399:
        ds_all.append({"d": int(m.group(1)), "s": int(m.group(2)),
                       "x": x, "y": y, "src": "red-read", "unc": unc})
        continue
    if re.fullmatch(r"\d{1,2}", c):
        sites.append({"v": int(c), "x": x, "y": y, "unc": unc})
for n in D["added"]:
    c, unc = canon(n["text"])
    x = n["x"] + (n.get("w", 0)) // 2
    y = n["y"] + (n.get("h", 0)) // 2
    m = re.fullmatch(r"(\d{1,2})-(\d{3,4})", c)
    if m and int(m.group(1)) <= 60 and int(m.group(2)) <= 2399:
        ds_all.append({"d": int(m.group(1)), "s": int(m.group(2)),
                       "x": x, "y": y, "src": "red-added", "unc": unc})
        continue
    if re.fullmatch(r"\d{1,2}", c):
        sites.append({"v": int(c), "x": x, "y": y, "unc": unc})

# the OCR's black D-S parcels (region labels, take-3 parse) and red stacks
P = json.load(open(ROOT + r"\scratch\map4456\region_parsed.json", encoding="utf-8"))
for p in P.get("parcels", []):
    ds_all.append({"d": p["d"], "s": p["s"], "x": p["x"], "y": p["y"],
                   "src": "black-ocr", "unc": False})
print("sites:", len(sites), " D-S labels:", len(ds_all),
      " (red-read %d, red-added %d, black-ocr %d)" % (
          sum(1 for p in ds_all if p['src'] == 'red-read'),
          sum(1 for p in ds_all if p['src'] == 'red-added'),
          sum(1 for p in ds_all if p['src'] == 'black-ocr')))

by_v = collections.defaultdict(list)
for s in sites:
    by_v[s["v"]].append(s)

R = 700
print("\n== red n with nearby D-S parcels summing to row n's total ==")
hits = []
tested = 0
for n in sorted(by_v):
    rt = row_total.get(n)
    if not rt:
        continue
    tested += 1
    for site in by_v[n]:
        near = [p for p in ds_all
                if math.hypot(p["x"] - site["x"], p["y"] - site["y"]) <= R]
        found = None
        for k in range(1, min(8, len(near) + 1)):
            for combo in itertools.combinations(near, k):
                tot = sum(p["d"] * 2400 + p["s"] for p in combo)
                if abs(tot - rt) <= 0.06 * rt:
                    found = (combo, tot)
                    break
            if found:
                break
        if found:
            hits.append((n, site, found[0], found[1], rt))
            break
for n, site, combo, tot, rt in hits:
    print("  red %2d at (%5.0f,%5.0f): %d parcels %s sum %d/%d ~ row %2d %d/%d [%s]"
          % (n, site["x"], site["y"], len(combo),
             "+".join("%d-%d" % (p["d"], p["s"]) for p in combo),
             tot // 2400, tot % 2400, n, rt // 2400, rt % 2400,
             stmt[str(n)]["name"][:24]))
print("hits: %d of %d red values tested" % (len(hits), tested))
json.dump({"hits": [{"n": n, "site": [site["x"], site["y"]],
                     "parcels": [{"d": p["d"], "s": p["s"],
                                  "x": p["x"], "y": p["y"], "src": p["src"]}
                                 for p in combo],
                     "tot": [tot // 2400, tot % 2400],
                     "row": [rt // 2400, rt % 2400]}
                    for n, site, combo, tot, rt in hits]},
          open(ROOT + r"\scratch\map4456\red_sum_hits.json", "w",
               encoding="utf-8"), indent=1)
