# Choose and prepare the test farm for the editor's read: the best is one
# where the red catalogue and the statement agree on a clear case.
# Candidates: row 84 (the proved stack 4/1684), row 78 (proved by 888/936),
# row 92 (the school, 9 des 2219), row 50 (the Zelmer). Compare the red
# sites' positions with the statement rows and print a reading sheet plan.
import json
import math
import collections

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld"
D = json.load(open(ROOT + r"\scratch\map4456\reds_all.json", encoding="utf-8"))
REF = json.load(open(ROOT + r"\scratch\map4456\reference_numbers.json", encoding="utf-8"))
stmt = REF["statement"]

def canon(t):
    t = t.strip()
    t = t.replace("[", "").replace("?]", "").replace("?", "")
    return t.strip()

sites = collections.defaultdict(list)
for a in D["answered"]:
    c = canon(a["text"])
    x, y = a["x"], a["y"]
    if a.get("fixed"):
        x = a["fixed"]["x"]; y = a["fixed"]["y"]
    if c.isdigit():
        sites[int(c)].append((x, y))
for n in D["added"]:
    c = canon(n["text"])
    x = n["x"] + (n.get("w", 0)) // 2
    y = n["y"] + (n.get("h", 0)) // 2
    if c.isdigit():
        sites[int(c)].append((x, y))

CAND = [78, 84, 92, 50, 47, 25]
for n in CAND:
    r = stmt.get(str(n))
    if not r:
        continue
    t = r["total"]
    pts = sites.get(n, [])
    cx = sum(p[0] for p in pts) / len(pts) if pts else 0
    cy = sum(p[1] for p in pts) / len(pts) if pts else 0
    print("row %2d %-28s total %d/%d  red sites %d %s" % (
        n, r["name"][:28], t["des"], t["saz"], len(pts),
        "centred (%.0f,%.0f)" % (cx, cy) if pts else "-"))
