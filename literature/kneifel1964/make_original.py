# -*- coding: utf-8 -*-
"""
Make original.md and english.md for kneifel1964 (docs/LITERATURE_PLAN.md,
section 24): the excerpt of Eduard Kneifel, "Geschichte der
Evangelisch-Augsburgischen Kirche in Polen" (self-published, Niedermarschacht
1964) that bears on the edition's ground - Trabczyn, Zagorow and the
neighbouring parishes and colonies of the Kalisch land.

The editor's two files, in
  J:\\Documents\\Archive\\Genealogy\\References\\Books\\
    History of the Evangelical-Augsburg Church in Poland (DE) (Kneifel, 1964)\\
are a German transcription (with printed page numbers in [N] and GFM
footnotes) and an English translation that pairs it page for page. The files
are NOT kept in the repository: the book runs to 313 printed pages and most
of it does not bear on the edition (the editor, 2026-10-22: only the relevant
sections are to be shown on the site). The scripts read them from the folder
named below and write the excerpt.

The excerpt, by printed page (the two files agree page for page):

  pp. 39-42   the section "Die laendliche Kolonisation" (III.1): the rural
              colonisation of central Poland, its growth after 1725, and
              p. 41 the passage on the Kalisch land that names the Starost
              ("Paul von Kolno-Prusinski, Grundherr von Trombezyn") and the
              founding of the colony Lazinsk Hol. in 1746; Orlina 1784.
              p. 42 is kept only to the section's five concluding points,
              before "Die staedtische Einwanderung".
  pp. 89-93   the section "Die preussische Kolonisation in Mittelpolen"
              (VI.1): the Prussian colonisation of 1793-1806, its figures
              and its colonies; p. 92 names the towns Konin, Zagerow and
              Kolo; p. 93 carries the section's close and the start of
              VI.2 (the schools of the Kalisch land).
  p. 45       the German schools of the Kalisch land to 1795: Wladyslawow-
              Rosterschuetz 1740, ..., Orlina, Lazinsk; the Kantorat system.
  p. 94       the Grodziec parish contract of 1796 (the Hollaender villages
              include Orlina) and the founding of Babiak.
  p. 102      the parishes Stawiszyn, Prazuchy, Sobiesenki, Lask and Slesin
              (its preaching-place Butter-Holl = Maslaki).
  p. 112      the schools of the 1840s: "im Bezirk Zagerow sieben", Orlina
              Wielka and Lazinsk with their school lands.
  p. 123      the parishes of the diocese of Kalisch: "Zagerow mit dem
              Filial Lissewo-Pyzdry, Konin mit dem Filial Maslaki". Kept
              from the paragraph on the dioceses' division to the end of
              the Kalisch list.
  p. 165      the churches of the region's parishes: Wladyslawow 1872,
              Stawiszyn 1875/76, Grodziec 1846-1866, the filial Maslaki 1888.
  p. 166      the church of Zagerow: foundation stone 8 May 1878, dedicated
              1st Advent Sunday 1882, a parsonage bought 1896; the Kolo
              church 1882/83. Kept from the foundation stone to the
              Wladyslawow filial's church of 1861.
  p. 179      the parish of Konin in the first decade of the 20th century
              and the filial Maslaki's quashed church project (Maslaki or
              Kleczew).
  p. 226      the inter-war parishes: Konin's pastor Robert Badke 1928-1939,
              Maslaki made a parish, and "Von 1923 bis 1945 war in Zagerow
              Pastor Alexander Gross taetig ...". Kept to that sentence.
  pp. 235-236 the Hahnsche Gemeinschaft "In Lazinsk, in der Gemeinde
              Zagerow" (p. 235, to the page's end) and the Lazinsker
              Bruederkreis (p. 236, to "verloren die Brueder an Boden.").
  p. 256      the statistics of 1938: "die rein deutsche evangelische
              Gemeinde Zagerow", the diocese of Kalisch's figures corrected
              from the editor's own book of 1937 on the parishes of the
              Kalisch diocese (its Zagerow Kirchspiel, 3800 souls in 1934).

Each kept page opens with its page mark [p. N]; where a page is cut, the
left-out parts are marked "[...]" (the Karwowski pattern). The footnotes
belonging to kept text are kept with it: the book's GFM footnotes are named
per page ([^p41-4]) and stand at the foot of their own page, so a marker
never reaches across pages. Nothing else is changed.

Run from the repository root:  python literature/kneifel1964/make_original.py
"""
import io, os, re, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(
    "J:", os.sep, "Documents", "Archive", "Genealogy", "References", "Books",
    "History of the Evangelical-Augsburg Church in Poland (DE) (Kneifel, 1964)")
DE_NAME = ("History of the Evangelical-Augsburg Church in Poland (DE) "
           "(Kneifel, 1964) (complete, with page numbers, GFM footnotes).md")
EN_NAME = ("History of the Evangelical-Augsburg Church in Poland (EN) "
           "(Kneifel, 1964).md")

WHOLE = {}

# One rule per excerpted page. "whole" keeps the page as the file has it;
# otherwise start/end are substrings: the kept text runs from the first
# occurrence of start (or the page's head if none) to the end of end (or the
# page's foot if none). end_exclusive cuts before the marker (a heading).
RULES = {
    39: {"de": {"start": "## III. Das Aufblühen"},
         "en": {"start": "## III. The flowering of new evangelical life"}},
    40: WHOLE,
    41: WHOLE,
    42: {"de": {"end": "### 2. Die städtische Einwanderung", "exclusive": True},
         "en": {"end": "### 2. Urban immigration", "exclusive": True}},
    45: WHOLE,
    89: {"de": {"start": "## VI. Die Kirche zu preußischer Zeit"},
         "en": {"start": "## VI. The Church in the Prussian Period"}},
    90: WHOLE,
    91: WHOLE,
    92: WHOLE,
    93: WHOLE,
    94: WHOLE,
    102: WHOLE,
    112: WHOLE,
    123: {"de": {"start": "Verwaltungsmäßig wurde die augsburgische Kirche",
                 "end": "Es waren also in sie 19 Pfarr-und zwölf Filialgemeinden einbezogen."},
          "en": {"start": "Administratively the Augsburg church was divided into the dioceses",
                 "end": "Thus 19 parishes and twelve filial congregations were included in it."}},
    165: WHOLE,
    166: {"de": {"start": "Der Grundstein zum Bau der lutherischen Kirche in Zagórów",
                 "end": "wurde 1861 eine massive Kirche errichtet."},
          "en": {"start": "The foundation stone for the building of the Lutheran church in Zagórów",
                 "end": "a massive church was erected in 1861."}},
    179: {"de": {"start": "Im ersten Jahrzehnt des 20. Jahrhunderts",
                 "end": "vereitelten die Realisierung des Projekts."},
          "en": {"start": "In the first decade of the 20th century",
                 "end": "thwarted the realization of the project."}},
    226: {"de": {"start": "Von 1930 bis 1939 verwaltete die Gemeinde Sobiesenki",
                 "end": "sehr angelegen sein."},
          "en": {"start": "From 1930 to 1939 Pastor Viktor Maczewski administered",
                 "end": "very much his concern."}},
    235: {"de": {"start": "In Lazinsk, in der Gemeinde Zagörow"},
          "en": {"start": "In Lazinsk, in the congregation of Zagörow"}},
    236: {"de": {"end": "verloren die „Brüder\" an Boden."},
          "en": {"end": "the „brothers\" lost ground."}},
    256: {"de": {"start": "Pastor Adolf Doberstein schrieb",
                 "end": "davon deutsch 1558, polnisch 157."},
          "en": {"start": "Pastor Adolf Doberstein wrote",
                 "end": "of them German 1558, Polish 157."}},
}

PAGE_MARK_RX = re.compile(r"(?m)^\[(\d+)\]$")
DEF_RX = re.compile(r"(?m)^\[\^([^\]\s]+)\]:")
MARKER_RX = re.compile(r"\[\^([^\]\s]+)\]")


def load_pages(path):
    text = open(path, encoding="utf-8").read()
    parts = PAGE_MARK_RX.split(text)
    pages = {}
    for i in range(1, len(parts), 2):
        pages[int(parts[i])] = parts[i + 1]
    return pages


def slice_page(body, rule):
    """The kept part of a page's text, with "[...]" where it is cut."""
    start, end = rule.get("start"), rule.get("end")
    exclusive = rule.get("exclusive", False)
    if start is None and end is None:
        return body, False, False
    a = 0 if start is None else body.find(start)
    if a < 0:
        raise SystemExit(f"start not found: {start!r}")
    if end is None:
        b = len(body)
        cut_end = a > 0
    else:
        e = body.find(end)
        if e < 0:
            raise SystemExit(f"end not found: {end!r}")
        b = e if exclusive else e + len(end)
        cut_end = b < len(body)
    kept = body[a:b].strip("\n")
    return kept, a > 0, cut_end


def footnotes(body, kept):
    """The footnote definitions the kept text needs and does not already carry.

    The book's definitions stand at the foot of their own page, so a slice
    that runs to the page's end already has them; only a cut before the foot
    loses the ones its kept markers point to."""
    def_lines = []                  # (id, line) in the page's own order
    for line in body.split("\n"):
        m = DEF_RX.match(line)
        if m:
            def_lines.append((m.group(1), line))
    present = {m.group(1) for line in kept.split("\n") if (m := DEF_RX.match(line))}
    markers = set(MARKER_RX.findall(kept))
    append = [line for d, line in def_lines if d in markers and d not in present]
    orphans = [d for d, _ in def_lines if d not in markers]
    missing = [m for m in markers if m not in {d for d, _ in def_lines}]
    return append, orphans, missing


def make(which, pages):
    out = []
    for n in sorted(RULES):
        body = pages[n]
        rule = RULES[n]
        if rule is WHOLE or rule == {}:
            kept, cut_start, cut_end = body.strip("\n"), False, False
            whole = True
        else:
            kept, cut_start, cut_end = slice_page(body, rule["de" if which == "original" else "en"])
            whole = False
        parts = [f"[p. {n}]", ""]
        if cut_start:
            parts += ["[…]", ""]
        parts.append(kept)
        defs, orphans, missing = footnotes(body, kept)
        tail = []
        if cut_end:
            tail += ["", "[…]"]
        if defs:
            tail += ["", *defs]
        out.append("\n".join(parts + tail))
        note = f"p. {n}: whole" if whole else f"p. {n}: cut"
        if orphans:
            note += f"; defs dropped: {', '.join(orphans)}"
        if missing:
            note += f"; MARKERS WITHOUT DEF: {', '.join(missing)}"
        print(note)
    return "\n\n".join(out) + "\n"


def main():
    de = load_pages(os.path.join(SRC, DE_NAME))
    en = load_pages(os.path.join(SRC, EN_NAME))
    missing = [n for n in RULES if n not in de or n not in en]
    if missing:
        raise SystemExit(f"pages not in both files: {missing}")
    for name, path, pages in (("original", os.path.join(HERE, "original.md"), de),
                              ("english", os.path.join(HERE, "english.md"), en)):
        text = make(name, pages)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        print(f"wrote {name}.md ({len(text)} chars)")


if __name__ == "__main__":
    main()
