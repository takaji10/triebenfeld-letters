# How discriminating is the buildings figure? The statement's buildings
# column per row: how many rows share the same value, how many rows have
# buildings in a given sazhen range, and how the "n. area" readings would
# score against the map's red catalogue.
import json
import collections

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld"
REF = json.load(open(ROOT + r"\scratch\map4456\reference_numbers.json", encoding="utf-8"))
stmt = REF["statement"]
D = json.load(open(ROOT + r"\scratch\map4456\reds_all.json", encoding="utf-8"))

def canon(t):
    t = t.strip().replace("[", "").replace("?]", "").replace("?", "")
    return t.strip()

# red sites per value
sites = collections.defaultdict(list)
for a in D["answered"]:
    c = canon(a["text"])
    x, y = a["x"], a["y"]
    if a.get("fixed"):
        x, y = a["fixed"]["x"], a["fixed"]["y"]
    if c.isdigit():
        sites[int(c)].append((x, y))
for n in D["added"]:
    c = canon(n["text"])
    x = n["x"] + (n.get("w", 0)) // 2
    y = n["y"] + (n.get("h", 0)) // 2
    if c.isdigit():
        sites[int(c)].append((x, y))

# buildings in saz per row
b = {int(n): r["buildings"]["des"] * 2400 + r["buildings"]["saz"]
     for n, r in stmt.items() if n.isdigit()}
cnt = collections.Counter(b.values())
print("distinct buildings values:", len(cnt), "of", len(b), "rows")
dups = {v: c for v, c in cnt.items() if c > 1}
print("values shared by 2+ rows:", len(dups), "covering",
      sum(dups.values()), "rows")
print("\nthe shared values (buildings saz -> rows):")
for v, c in sorted(dups.items()):
    rows = sorted(n for n, vv in b.items() if vv == v)
    print("  %4d saz  x%d  rows %s" % (v, c, rows))

# how many rows have buildings <= 600 (the yard-scale range)?
yard = sorted((v, n) for n, v in b.items() if v <= 700)
print("\nrows with buildings <= 700 saz:", len(yard))
for v, n in yard[:25]:
    tag = ""
    if v in sites or n in sites:
        tag = "  <- red-%d sites on the map: %d" % (n, len(sites.get(n, [])))
    print("  row %2d: %4d saz%s" % (n, v, tag))
