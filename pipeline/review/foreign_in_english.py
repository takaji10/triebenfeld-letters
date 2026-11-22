"""List words in the published English translations that are not English.

Reads site/_data/translations/*.yml (field `en` of every segment only) and
writes review/foreign_in_english.tsv (one row per occurrence) and
review/foreign_in_english_tokens.tsv (aggregated), for a human to review.
Kinds, in order: fragment, latin, polish, german, sign. Lines starting
"[Written" are the edition's own labels and are skipped.
"""
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "site" / "_data" / "translations"
OUT = ROOT / "review"

PL = "ąćęłńóśźż"
DE = "äöüß"
FRAG = [
    re.compile(r"\b\w*\[[A-Za-zäöüßÄÖÜąćęłńóśźż]{1,4}\?\]\w*"),
    re.compile(r"\w+\[\?\]\w+"),
]
LATIN_PHRASES = [
    "ex quo", "aliunde", "in solidum", "ex chirographo", "chirographo", "eodem",
    "ita conclusum", "conclus.", "contra", "in simili", "sub dato", "ad acta",
    "pro memoria", "ad mandatum", "mandatum", "de dato", "praesentatum", "praes.",
    "cito", "in fidem", "copia vidimata", "salvo", "ad interim", "per extensum",
    "in natura", "in specie", "ipso facto", "de jure", "ex officio",
    "in contumaciam", "contumacia", "citatio", "actum", "datum", "manu propria",
    "mpp", "ut supra", "nota bene", "etc.", "et cetera", "idem", "ibidem",
    "item", "sub poena", "sub fide", "interim", "quasi", "vide", "vel", "seu",
    "alias", "vulgo", "contractus", "antichreticus", "hypotheca",
]
LATIN_RE = re.compile(
    r"(?<!\w)(" + "|".join(re.escape(p).replace(r"\ ", r"\s+")
                           for p in sorted(LATIN_PHRASES, key=len, reverse=True))
    + r")(?!\w)", re.I)
LATIN_END = re.compile(r".+(orum|arum|ibus|ione|ionis|atis)$", re.I)
EN_STOP = {"omnibus", "quorum", "forum", "decorum", "sanctorum", "carum", "ibus",
           "ione", "ionis", "atis", "bus", "mores", "gratis", "satis", "pro", "ratione",
           "ordinarium", "calamus", "sedibus"}
GERMAN = set("der die das und nicht werden worden wegen welche dieses solche daß dass "
             "sich nach noch den dem des ein eine einen ist sind hat haben auch von zu "
             "mit bey bei für über".split())
WORD = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)*")
SIGN = re.compile(r"\./\.")
CAP = re.compile(r"\s+[A-ZÄÖÜŁŚŻŹĆŃÓ]")


def ctx(text, a, b):
    return re.sub(r"\s+", " ", text[max(0, a - 60):a] + "\x00" + text[a:b] + "\x00" + text[b:b + 60]).replace("\x00", "")


def ctx_plain(text, a, b):
    left = re.sub(r"\s+", " ", text[max(0, a - 60):a])
    right = re.sub(r"\s+", " ", text[b:b + 60])
    return left + re.sub(r"\s+", " ", text[a:b]) + right


def scan(text):
    """Yield (kind, token, start, end)."""
    taken = []

    def free(a, b):
        return all(b <= x or a >= y for x, y in taken)

    found = []
    for rx in FRAG:
        for m in rx.finditer(text):
            if free(m.start(), m.end()):
                taken.append((m.start(), m.end()))
                found.append(("fragment", m.group(0), m.start(), m.end()))
    for m in SIGN.finditer(text):
        taken.append((m.start(), m.end()))
        found.append(("sign", "./.", m.start(), m.end()))
    for m in LATIN_RE.finditer(text):
        if free(m.start(), m.end()):
            taken.append((m.start(), m.end()))
            found.append(("latin", re.sub(r"\s+", " ", m.group(0).lower()), m.start(), m.end()))
    for m in WORD.finditer(text):
        a, b = m.start(), m.end()
        if not free(a, b):
            continue
        w = m.group(0)
        lw = w.lower()
        kind = None
        if LATIN_END.match(w) and lw not in EN_STOP:
            kind, tok = "latin", lw
        elif any(c in PL for c in lw):
            kind, tok = "polish", w
        elif any(c in DE for c in lw):
            kind, tok = "german", lw
        elif lw in GERMAN:
            if lw == "von" and CAP.match(text[b:b + 3]):
                continue
            kind, tok = "german", lw
        if kind:
            found.append((kind, tok, a, b))
    found.sort(key=lambda r: r[2])
    return found


def main():
    OUT.mkdir(exist_ok=True)
    rows = []
    for f in sorted(SRC.glob("*.yml")):
        data = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        for seg in data.get("segments") or []:
            en = seg.get("en") if isinstance(seg, dict) else None
            if not isinstance(en, str):
                continue
            # blank the edition's own label lines, keeping offsets
            en = re.sub(r"(?m)^\[Written[^\n]*", lambda m: " " * len(m.group(0)), en)
            for kind, tok, a, b in scan(en):
                rows.append((f.stem, seg.get("page", ""), kind, tok, ctx_plain(en, a, b)))
    with open(OUT / "foreign_in_english.tsv", "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["pad", "page", "kind", "token", "context"])
        w.writerows(rows)
    agg = defaultdict(list)
    for r in rows:
        agg[(r[2], r[3])].append(r)
    out = []
    for (kind, tok), rs in agg.items():
        pads = list(dict.fromkeys(r[0] for r in rs))
        out.append((kind, tok, len(rs), len(pads), ",".join(pads[:8]), rs[0][4]))
    out.sort(key=lambda r: (r[0], -r[2], r[1]))
    with open(OUT / "foreign_in_english_tokens.tsv", "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["kind", "token", "count", "documents", "pads", "sample"])
        w.writerows(out)
    for kind in ("fragment", "latin", "polish", "german", "sign"):
        occ = sum(1 for r in rows if r[2] == kind)
        dist = sum(1 for r in out if r[0] == kind)
        print(f"{kind}: {occ} occurrences, {dist} distinct")
        if kind in ("fragment", "latin", "german"):
            print("  top:", "; ".join(f"{r[1]} ({r[2]})" for r in [r for r in out if r[0] == kind][:10]))


if __name__ == "__main__":
    sys.exit(main())
