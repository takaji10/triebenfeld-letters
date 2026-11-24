# -*- coding: utf-8 -*-
"""Alphabetical order for place names (the editor, 2026-11-24: the Places
lists kept alphabetical whatever order places are added in). Polish letters
in their Polish places (Ł after L, Ś after S, Ż last), German umlauts with
their base letter; case and punctuation ignored. Used by build_site_data.py
(the Places index) and cemetery_pages.py (the cemeteries)."""
import unicodedata

_PL_ORDER = 'aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźż'


def place_sort_key(name):
    out = []
    for ch in (name or '').lower():
        if ch in _PL_ORDER:
            out.append(_PL_ORDER.index(ch) + 10)
            continue
        base = unicodedata.normalize('NFKD', ch)[:1]
        if base in _PL_ORDER:
            out.append(_PL_ORDER.index(base) + 10)
        elif ch.isdigit():
            out.append(ord(ch) - 48)
        elif ch == ' ':
            out.append(0)
    return out
