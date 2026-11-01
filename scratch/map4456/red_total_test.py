# The closing test: the red D-S labels equal row totals — do they sit near
# the red n of the same row? And record the whole red system in the notes.
import json
import re
import math
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
for a in D["answered"]:
    c, unc = canon(a["text"])
    x, y = a["x"], a["y"]
    if a.get("fixed"):
        x = a["fixed"]["x"]; y = a["fixed"]["y"]
    m = re.fullmatch(r"(\d{1,2})-(\d{3,4})", c)
    if m:
        ds.append({"d": int(m.group(1)), "s": int(m.group(2)),
                   "x": x, "y": y, "src": "sheet", "unc": unc, "text": c})
        continue
    if re.fullmatch(r"\d{1,2}", c):
        sites.append({"v": int(c), "x": x, "y": y, "unc": unc})
for n in D["added"]:
    c, unc = canon(n["text"])
    x = n["x"] + (n.get("w", 0)) // 2
    y = n["y"] + (n.get("h", 0)) // 2
    m = re.fullmatch(r"(\d{1,2})-(\d{3,4})", c)
    if m:
        ds.append({"d": int(m.group(1)), "s": int(m.group(2)),
                   "x": x, "y": y, "src": "added", "unc": unc, "text": c})
        continue
    if re.fullmatch(r"\d{1,2}", c):
        sites.append({"v": int(c), "x": x, "y": y, "unc": unc})

by_v = collections.defaultdict(list)
for s in sites:
    by_v[s["v"]].append(s)

print("== red D-S == row total, with the same row's red n nearby ==")
confirmed = []
for p in ds:
    v = p["d"] * 2400 + p["s"]
    rows = [n for n, rt in row_total.items() if rt == v]
    near = {}
    for n in rows:
        pts = by_v.get(n, [])
        if pts:
            dmin = min(math.hypot(s["x"] - p["x"], s["y"] - p["y"]) for s in pts)
            near[n] = dmin
    if rows:
        confirmed.append((p, rows, near))
        print("  %s at (%5.0f,%5.0f)%s == row %s total; red-n %s within %s px" % (
            p["text"], p["x"], p["y"], " [unc]" if p["unc"] else "",
            ",".join(map(str, rows)),
            {n: int(d) for n, d in near.items()} or "NONE nearby",
            {n: sorted(set(s2['v'] for s2 in by_v.get(n, []))) and int(min(
                math.hypot(s["x"] - p["x"], s["y"] - p["y"]) for s in by_v[n]))
             for n, d in near.items()} if near else ""))

# and the reverse: for each red value with sites, is there a D-S == its row
# total within reach?
print("\n== red n whose row total appears as a red D-S label within 800 px ==")
ok = 0
for n in sorted(by_v):
    rt = row_total.get(n)
    if not rt:
        continue
    ds_match = [p for p in ds if p["d"] * 2400 + p["s"] == rt]
    if not ds_match:
        continue
    for site in by_v[n]:
        for p in ds_match:
            d = math.hypot(p["x"] - site["x"], p["y"] - site["y"])
            if d <= 800:
                ok += 1
                print("  red %2d at (%5.0f,%5.0f) + %s %d px away == row %2d [%s]"
                      % (n, site["x"], site["y"], p["text"], int(d), n,
                         stmt[str(n)]["name"][:24]))
                break
        else:
            continue
        break
print("red values whose row-total D-S label sits within 800 px: %d" % ok)
