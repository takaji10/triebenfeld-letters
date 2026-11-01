# Why so few D-S labels? Inspect the re-read lines: how do dash-carrying
# lines look, how are two-line stacks split across clusters, and what do
# the failed parses contain?
import json
import re
import collections

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld"
LAB = json.load(open(ROOT + r"\scratch\map4456\region_labels.json", encoding="utf-8"))

def clean(s):
    s = s.replace(" ", "").replace("°", "").replace("o", "").replace("O", "")
    return s.strip(".")

dash = [l for lab in LAB for l in lab["lines"]
        if isinstance(l, str) and ("-" in l or "/" in l)]
print("lines carrying a dash or slash:", len(dash))
pat = collections.Counter()
for l in dash[:300]:
    s = clean(l)
    if re.fullmatch(r"\d{1,2}-\d{3,4}", s): pat["D-S clean"] += 1
    elif re.fullmatch(r"\d{1,2}[-/]+", s): pat["D- (saz on next line?)"] += 1
    elif re.fullmatch(r"[-/]?\d{3,4}", s): pat["-S (des on prev line?)"] += 1
    elif re.fullmatch(r"\d{1,2}[-/]\D*", s): pat["D- + junk"] += 1
    else: pat["other: " + s[:14]] += 1
for k, v in pat.most_common(20):
    print("   %-28s %d" % (k, v))
print("\nsample dash lines:")
for l in dash[:30]:
    print("   %r" % l)

# two-line stacks: labels with >=2 lines where one is small and one is big
two = [lab for lab in LAB if len(lab["lines"]) >= 2 and lab["ink"] == "black"]
print("\nblack labels with >=2 lines:", len(two))
small_then_big = 0
for lab in two[:400]:
    nums = []
    for l in lab["lines"]:
        s = clean(l) if isinstance(l, str) else clean(l["text"])
        if s.isdigit():
            nums.append(int(s))
    if len(nums) >= 2 and max(nums) >= 100 and min(nums) <= 60:
        small_then_big += 1
print("of which small-over-big numeric pairs:", small_then_big)

# how many black labels are single-line small numbers only?
one_small = 0
for lab in LAB:
    if lab["ink"] != "black" or len(lab["lines"]) != 1:
        continue
    s = clean(lab["lines"][0]) if isinstance(lab["lines"][0], str) else clean(lab["lines"][0]["text"])
    if s.isdigit() and int(s) <= 97:
        one_small += 1
print("black single-line small-number labels:", one_small)

# the red labels: how many read as clean 1-4 digit values?
red_ok = []
for lab in LAB:
    if lab["ink"] != "red" or len(lab["lines"]) != 1:
        continue
    s = clean(lab["lines"][0]) if isinstance(lab["lines"][0], str) else clean(lab["lines"][0]["text"])
    if s.isdigit() and 10 <= int(s) <= 2399:
        red_ok.append(int(s))
print("red single-line numeric labels 10..2399:", len(red_ok))
print("  values:", sorted(red_ok)[:70])
