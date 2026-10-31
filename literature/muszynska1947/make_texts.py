"""Assemble the literature work muszynska1947 from the translation package.

original.md: the Polish source, front matter through the notes, without the
bibliography, index and errata (the apparatus is not part of the passages,
as with Frost 2007's endnotes-only text; see notes.md).
english.md: the corrected English, front matter + contents + chapters + notes.
"""
import os, re, sys

SRC = r"C:\Users\Tersnaus\Downloads\wielkopolska-translation"
DST = r"C:\Users\Tersnaus\Downloads\vonTriebenfeld\literature\muszynska1947"

os.makedirs(DST, exist_ok=True)

src = open(os.path.join(SRC, "source", "wielkopolska-w-powstaniu-kosciuszkowskim-1947.md"), encoding="utf-8").read()
cut = src.index("## Źródła i literatura")
original = src[:cut].rstrip() + "\n"

front = open(os.path.join(SRC, "translation", "front.en.md"), encoding="utf-8").read().rstrip()
toc = open(os.path.join(SRC, "translation", "toc.en.md"), encoding="utf-8").read().rstrip()
body = open(os.path.join(SRC, "translation", "wielkopolska-en-qa.md"), encoding="utf-8").read().rstrip()
english = front + "\n\n" + toc + "\n\n" + body + "\n"

open(os.path.join(DST, "original.md"), "w", encoding="utf-8", newline="\n").write(original)
open(os.path.join(DST, "english.md"), "w", encoding="utf-8", newline="\n").write(english)

for name, text in (("original", original), ("english", english)):
    marks = re.findall(r"^\[(\d+)\] <!-- p\.\d+ -->\s*$", text, re.M)
    print(name, len(text), "chars", len(marks), "pages", marks[:3], "...", marks[-3:])
