"""Compare the top-level shape of an estate build against the Zelmer data."""
import json, sys
from pathlib import Path
a, b = Path(sys.argv[1]), Path(sys.argv[2])   # reference data, new data
def keys(d):
    if isinstance(d, dict): return set(d)
    return set()
ok = True
for n in ["index","families","places","sources","repos","surnames","meta","media","media_files"]:
    x = json.loads((a/f"{n}.json").read_text(encoding="utf-8")); y = json.loads((b/f"{n}.json").read_text(encoding="utf-8"))
    if n in ("meta",):
        miss, extra = keys(x)-keys(y), keys(y)-keys(x)
    else:  # compare the inner record keys
        def inner(d):
            s=set()
            for v in d.values():
                if isinstance(v, dict): s|=set(v)
            return s
        miss, extra = inner(x)-inner(y), inner(y)-inner(x)
    print(f"{n}: type {type(x).__name__}/{type(y).__name__}; keys in reference only (often optional): {sorted(miss)}; new only: {sorted(extra)}")
    if type(x)!=type(y): ok=False
px = json.loads(next((a/"people").glob("*.json")).read_text(encoding="utf-8"))
py = json.loads(next((b/"people").glob("*.json")).read_text(encoding="utf-8"))
print("person shard keys ref-only:", sorted(set(px)-set(py)), "new-only:", sorted(set(py)-set(px)))
print("SHAPE OK" if ok else "SHAPE MISMATCH")
