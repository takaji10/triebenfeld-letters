# Sanity checks on the rebuilt spot sheet: the payload parses, every card
# carries its crop and a box inside the crop, and the export's box math
# (crop-local + crop origin) reconstructs the token's mosaic box.
import base64
import json
import re

h = open(r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\scratch\map4456\spot_sheet.html",
         encoding="utf-8").read()
m = re.search(r'<script id="sheet-data" type="application/json">(.*?)</script>', h, re.S)
items = json.loads(m.group(1))
print("cards:", len(items))
bad = []
for it in items:
    assert it["img"].startswith("data:image/jpeg;base64,")
    base64.b64decode(it["img"].split(",", 1)[1])
    if not (0 <= it["bx"] <= it["cw"] - it["bw"]):
        bad.append((it["id"], "bx", it["bx"], it["cw"], it["bw"]))
    if not (0 <= it["by"] <= it["ch"] - it["bh"]):
        bad.append((it["id"], "by", it["by"], it["ch"], it["bh"]))
print("cards with a mis-sited box:", len(bad), bad[:5])
print("crop sizes:", sorted({(it["cw"], it["ch"]) for it in items}))
it0 = items[0]
print("card 1:", it0["grp"], it0["my"], "conf", it0["conf"],
      "box mosaic", (it0["ox"] + it0["bx"], it0["oy"] + it0["by"], it0["bw"], it0["bh"]),
      "== token", (it0["x"], it0["y"], it0["w"], it0["h"]))
