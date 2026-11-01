# Are the red single values (10..98) the sazhen halves of stacked des/saz
# pairs whose desiatina half was clustered separately? For each, look for a
# red small token (1..30) above it within stack distance, re-pair, and see
# how many of the 71 singles close as stacks. Also: the alternative that
# they are the areas of tiny parcels (single number = square sazhens).
import json
import math
import re
import collections

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld"
LAB = json.load(open(ROOT + r"\scratch\map4456\region_labels.json", encoding="utf-8"))

def clean(s):
    s = s.replace(" ", "").replace("°", "").replace("o", "").replace("O", "")
    return s.strip(".")

# all red labels with their crop boxes (to compute line positions properly)
redlabs = []
for lab in LAB:
    if lab["ink"] != "red":
        continue
    for l in lab["lines"]:
        s = clean(l) if isinstance(l, str) else clean(l["text"])
        if not s:
            continue
        redlabs.append({"text": s, "x": lab["x"], "y": lab["y"],
                        "w": lab["w"], "h": lab["h"], "n": lab["n_tokens"]})

singles = [r for r in redlabs if re.fullmatch(r"\d{2}", r["text"])
           and 10 <= int(r["text"]) <= 98]
smalls = [r for r in redlabs if re.fullmatch(r"\d{1,2}", r["text"])
          and 1 <= int(r["text"]) <= 30]
bigs4 = [r for r in redlabs if re.fullmatch(r"\d{3,4}", r["text"])
         and 100 <= int(r["text"]) <= 2399]
print("red singles 10..98:", len(singles), " red smalls 1..30:", len(smalls),
      " red bigs 100..2399:", len(bigs4))

# for each single, the best small above it (stack)
paired = 0
examples = []
used = set()
for s in sorted(singles, key=lambda r: r["y"]):
    sx = s["x"] + s["w"] / 2
    sy = s["y"] + s["h"] / 2
    best = None
    for sm in smalls:
        if id(sm) in used:
            continue
        mx = sm["x"] + sm["w"] / 2
        my = sm["y"] + sm["h"] / 2
        if abs(mx - sx) > 150:
            continue
        dy = sy - my
        if not (12 <= dy <= 250):
            continue
        if best is None or abs(dy) < best[0]:
            best = (dy, sm)
    if best:
        used.add(id(best[1]))
        paired += 1
        if len(examples) < 12:
            examples.append((best[1]["text"], s["text"], int(best[0]),
                             int(sx), int(sy)))
print("singles that pair with a small red above:", paired, "of", len(singles))
for d, s_, dy, x, y in examples:
    print("   %s over %s  dy %d  at (%d,%d)  -> %s des %s saz" % (d, s_, dy, x, y, d, s_))

# the singles that did NOT pair: their spatial pattern
unpaired = [s for s in singles if not any(
    abs((sm["x"] + sm["w"] / 2) - (s["x"] + s["w"] / 2)) <= 150
    and 12 <= (s["y"] + s["h"] / 2) - (sm["y"] + sm["h"] / 2) <= 250
    for sm in smalls if id(sm) not in used)]
print("\nunpaired singles:", len(unpaired))
cc = collections.Counter(int(s["text"]) for s in unpaired)
print("  values:", sorted(cc.items()))
