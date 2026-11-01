# The corrected red tokens (post fix_ink): value distribution, single vs
# hyphenated, sizes, and where the big area figures went (red or black?).
import re
import json
import collections

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld"
REG = json.load(open(ROOT + r"\scratch\map4456\region_tokens.json", encoding="utf-8"))
reds = REG["red"]
blacks = REG["black"]

def norm_parts(t):
    t = t.strip().strip(".,-/").strip()
    out = []
    for p in t.replace("/", " ").replace(",", " ").replace(".", " ").replace("-", " ").split():
        if p.isdigit():
            out.append(int(p))
    if t.isdigit() and int(t) not in out:
        out.append(int(t))
    return out

print("region: red %d, black %d" % (len(reds), len(blacks)))

def profile(name, toks):
    vals = []
    hyph = 0
    for t in toks:
        if "-" in t["text"] or "/" in t["text"]:
            hyph += 1
        ps = norm_parts(t["text"])
        vals.extend(ps)
    singles = [v for v in vals if v <= 99]
    bigs = [v for v in vals if v >= 100]
    print("\n%s: %d tokens, %d carry a hyphen/slash" % (name, len(toks), hyph))
    c = collections.Counter(singles)
    print("  small values (<=99):", sorted(c.items()))
    print("  big values (>=100): %d, sample %s" % (len(bigs), sorted(set(bigs))[:20]))

profile("RED", reds)
profile("BLACK", blacks)

# where did the 4-digit area figures go?
for name, toks in (("red", reds), ("black", blacks)):
    big4 = [t for t in toks
            if any(1000 <= v <= 2399 for v in norm_parts(t["text"]))]
    print("\n%s tokens with a 1000..2399 value: %d" % (name, len(big4)))
    for t in big4[:12]:
        print("   %-10r conf %.2f at (%5d,%5d)" % (t["text"], t["conf"], t["x"], t["y"]))
