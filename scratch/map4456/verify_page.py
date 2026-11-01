import re
import json

h = open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\oleders_map.html",
         encoding="utf-8").read()
assert "@@" not in h, "unreplaced token"
m = re.search(r'<script id="map-data" type="application/json">(.*?)</script>', h, re.S)
d = json.loads(m.group(1))
print("labels:", len(d["labels"]), "tiles:", d["tiles"][:70])
rows = re.findall(r'<li id="row-(\d+)" class="([^"]*)"', h)
print("rows:", len(rows),
      "located:", sum(1 for _, c in rows if "located" in c),
      "zelmer:", sum(1 for _, c in rows if "zelmer" in c),
      "proved:", sum(1 for _, c in rows if "proved" in c))
print("row 78 class:", [c for i, c in rows if i == "78"])
print("row 50 class:", [c for i, c in rows if i == "50"])
loc = [i for i, c in rows if re.search(r"\blocated\b", c)]
un = [i for i, c in rows if "unlocated" in c]
print("located:", len(loc), " unlocated:", len(un))
print("row 92 class:", [c for i, c in rows if i == "92"])
