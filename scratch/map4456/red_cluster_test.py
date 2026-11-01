# The spatial test of red = farm number: for each red value with >=2
# occurrences, how tightly do its sites cluster (vs random values)? And do
# the red 78 sites agree with the proved black-78 site (3847, 6371)?
import json
import math
import random
import re
import collections

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld"
REF = json.load(open(ROOT + r"\scratch\map4456\reference_numbers.json", encoding="utf-8"))
LAB = json.load(open(ROOT + r"\scratch\map4456\region_labels.json", encoding="utf-8"))
stmt = REF["statement"]

def clean(s):
    s = s.replace(" ", "").replace("°", "").replace("o", "").replace("O", "")
    return s.strip(".")

red_sites = collections.defaultdict(list)
for lab in LAB:
    if lab["ink"] != "red" or lab["n_tokens"] != 1:
        continue
    s = clean(lab["lines"][0]) if lab["lines"] else ""
    if re.fullmatch(r"\d{2}", s):
        v = int(s)
        if 10 <= v <= 97:
            red_sites[v].append((lab["x"] + lab["w"] / 2, lab["y"] + lab["h"] / 2))

def spread(pts):
    """mean pairwise distance"""
    if len(pts) < 2:
        return 0.0
    ds = [math.hypot(a[0] - b[0], a[1] - b[1])
          for i, a in enumerate(pts) for b in pts[i + 1:]]
    return sum(ds) / len(ds)

print("red value  count  spread(px)   sites")
multi = {v: pts for v, pts in red_sites.items() if len(pts) >= 2}
for v in sorted(multi, key=lambda v: -len(multi[v])):
    pts = multi[v]
    print("  %2d        %d     %6.0f      %s" % (
        v, len(pts), spread(pts),
        " ".join("(%4.0f,%4.0f)" % p for p in pts)))

# control: random values placed at all red sites' positions
allpos = [p for pts in red_sites.values() for p in pts]
rng = random.Random(9)
ctrl = []
for _ in range(3000):
    k = rng.choice([len(p) for p in multi.values()])
    pts = rng.sample(allpos, k)
    ctrl.append(spread(pts))
ctrl.sort()
obs = sorted(spread(pts) for pts in multi.values())
print("\nspreads observed: %s" % ["%.0f" % x for x in obs])
print("control mean %.0f, p25 %.0f, p50 %.0f" %
      (sum(ctrl) / len(ctrl), ctrl[len(ctrl) // 4], ctrl[len(ctrl) // 2]))
tight = sum(1 for o in obs if o < ctrl[len(ctrl) // 4])
print("observed spreads below the control's p25: %d of %d" % (tight, len(obs)))

# red 78 vs the proved black-78 site
for v in (78, 88, 84, 18):
    pts = red_sites.get(v, [])
    if not pts:
        continue
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    print("red %d centroid (%.0f,%.0f), n=%d" % (v, cx, cy, len(pts)))
print("\nproved black-78 site: (3847, 6371); proved red-84 stack: (4751, 5713)")
