# What did the projection re-read actually see? Line counts per label, how
# many labels carry digit-bearing lines, and a sample of read lines.
import json
import re
import collections

ROOT = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld"
LAB = json.load(open(ROOT + r"\scratch\map4456\region_labels3.json", encoding="utf-8"))

nl = collections.Counter(len(lab["lines"]) for lab in LAB)
print("lines per label:", sorted(nl.items()))
with_digits = 0
with_ds = 0
sample = []
for lab in LAB:
    texts = [l["text"] for l in lab["lines"]]
    joined = " ".join(texts)
    if re.search(r"\d", joined):
        with_digits += 1
    if re.search(r"\d{1,2}[-/]\d{3,4}", joined.replace(" ", "")):
        with_ds += 1
    elif texts and len(sample) < 40:
        sample.append((lab["ink"], texts))
print("labels with any digit:", with_digits, "of", len(LAB))
print("labels whose joined text holds D-S:", with_ds)
print("\nsample non-D-S digit labels:")
for ink, texts in sample[:25]:
    print("  ", ink, texts)
