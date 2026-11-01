# Which OCR tokens sit in the drawn map, and which in the information
# blocks? The blocks are known sheet-1 content (title + certification texts,
# the explication, the legend, the adjoining-lands list); their zones come
# from the ASCII density art of sheet 1 (ascii_sheet1.py) and the token
# evidence, with generous margins. Everything outside the zones is drawn map.
# Output: drawn.json (the zones + stats), the two token files annotated with
# "drawn", numbers_auto.json (tokens auto-classified "not a number").
import json

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld"

# mosaic-px rectangles of the information blocks (x0, y0, x1, y1) — the
# certain blocks only; the contested strips stay with the drawn map, where
# the spot sheet's "not a number" catches any residue
ZONES = [
    ("title + certification", 0, 0, 3800, 2750),
    ("explication", 4950, 800, 5800, 1750),
    ("legend + adjoining lands", 5850, 5600, 7300, 7100),
]

def inside_zone(x, y):
    for name, x0, y0, x1, y1 in ZONES:
        if x0 <= x <= x1 and y0 <= y <= y1:
            return name
    return None

# ---- validation against known points ---------------------------------------
MAP_CHECK = [(3847, 6371), (5423, 8654), (4751, 5713), (17769, 11984),
             (5974, 10546), (9504, 9896), (6970, 5153), (19978, 12188),
             (18798, 12315), (19612, 10949), (9416, 4596)]
INFO_CHECK = [(5338, 1286), (5335, 1483), (5379, 1559), (5373, 1071),
              (952, 1352), (3064, 1750), (1570, 1476), (2592, 1766),
              (1260, 1880)]
bad = [p for p in MAP_CHECK if inside_zone(*p)]
bad2 = [p for p in INFO_CHECK if not inside_zone(*p)]
print("map points wrongly in a zone:", bad)
print("info points wrongly outside:", bad2)
assert not bad and not bad2, "zone validation failed"

RED = json.load(open(ROOT + r"\scratch\map4456\numbers_easy2.json", encoding="utf-8"))
BLACK = json.load(open(ROOT + r"\scratch\map4456\numbers_black.json", encoding="utf-8"))

auto = []
for t in RED:
    cx, cy = t["x"] + t["w"] / 2, t["y"] + t["h"] / 2
    z = inside_zone(cx, cy)
    t["drawn"] = z is None
    t["zone"] = z
for t in BLACK:
    cx, cy = t["x"] + t["w"] / 2, t["y"] + t["h"] / 2
    z = inside_zone(cx, cy)
    t["drawn"] = z is None
    t["zone"] = z

def norm_parts(t):
    t = t.strip().strip(".,-/").strip()
    out = []
    for p in t.replace("/", " ").replace(",", " ").replace(".", " ").replace("-", " ").split():
        if p.isdigit():
            out.append(int(p))
    if t.isdigit() and int(t) not in out:
        out.append(int(t))
    return out

for t in RED:
    if t["drawn"]:
        core = t["text"]
        for ch in "/.,- ":
            core = core.replace(ch, "")
        if len(core) > 4:
            auto.append({"src": "red", "text": t["text"], "conf": t["conf"],
                         "x": t["x"], "y": t["y"], "reason": "too many digits"})
for t in BLACK:
    if not t["drawn"]:
        auto.append({"src": "black", "text": t["text"], "conf": t["conf"],
                     "x": t["x"], "y": t["y"],
                     "reason": "info-block: " + (t["zone"] or "")})
    else:
        ps = norm_parts(t["text"])
        if len(ps) == 1 and 1 <= ps[0] <= 97 and t["conf"] < 0.45:
            auto.append({"src": "black", "text": t["text"], "conf": t["conf"],
                         "x": t["x"], "y": t["y"], "reason": "confidence too low"})

n_ri = sum(1 for t in RED if not t["drawn"])
n_bi = sum(1 for t in BLACK if not t["drawn"])
print("red in info blocks: %d of %d   black in info blocks: %d of %d"
      % (n_ri, len(RED), n_bi, len(BLACK)))
print("auto not-a-number: %d (info-block %d, too-many-digits %d, low-conf %d)"
      % (len(auto),
         sum(1 for a in auto if a["reason"].startswith("info-block")),
         sum(1 for a in auto if a["reason"] == "too many digits"),
         sum(1 for a in auto if a["reason"] == "confidence too low")))

json.dump(RED, open(ROOT + r"\scratch\map4456\numbers_easy2.json", "w", encoding="utf-8"),
          ensure_ascii=False)
json.dump(BLACK, open(ROOT + r"\scratch\map4456\numbers_black.json", "w", encoding="utf-8"),
          ensure_ascii=False)
json.dump(auto, open(ROOT + r"\scratch\map4456\numbers_auto.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
json.dump({"zones": [{"name": n, "rect": [x0, y0, x1, y1]} for n, x0, y0, x1, y1 in ZONES],
           "red_info": n_ri, "black_info": n_bi, "auto": len(auto)},
          open(ROOT + r"\scratch\map4456\drawn.json", "w", encoding="utf-8"),
          indent=1)
print("saved drawn.json, numbers_auto.json; token files annotated")
