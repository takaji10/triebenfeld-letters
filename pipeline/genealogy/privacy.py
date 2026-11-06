# The privacy pass (PLAN.md section 4.4).
#
# Living people are redacted at build time, so nothing sensitive reaches the
# published repos: their events, dates, places, notes, citations, sources
# and media are dropped; the name keeps only the surname ("Living Zelmer"),
# and sex and family links survive so the trees still read correctly.
#
# Detection mirrors Gramps' own "probably alive" so the editor can check the
# result against Gramps' privacy filter:
#
#   1. the GEDCOM's own [Living] name placeholder always marks a living
#      person (1,364 people carry it);
#   2. death, burial or cremation evidence makes a person dead;
#   3. a birth or baptism on or after the age limit (today - 100) makes a
#      person living; one well before it makes them dead;
#   4. without a birth date, a dated non-death event implies a birth year
#      at least 16 years earlier: the event is at or after (today - 84)
#      means living, well before it means dead;
#   5. people with no dates at all inherit the closest verdict among their
#      parents, spouses and children (fixpoint); if that is still open they
#      are treated as living - redaction errs on the safe side, and the
#      spot-check report lists every case for the editor.

from __future__ import annotations

from datetime import date

DEATH_LIKE = ("DEAT", "BURI", "CREM")
BIRTH_LIKE = ("BIRT", "BAPM", "CHR", "BAPL")

# The minimum age the bounds assume: a parent is at least this old at a
# child's birth, a spouse at least this old at a marriage. The parent age
# is deliberately the youngest plausible figure: the lower it is, the
# harder it is to prove a person has passed the ceiling, so redaction errs
# toward the living side.
MIN_PARENT_AGE = 14
MIN_MARRIAGE_AGE = 16


def _birth_year(person) -> int | None:
    for tag in BIRTH_LIKE:
        for e in person.events:
            if e.tag == tag and e.date and e.date.year:
                return e.date.year
    return None


def _dead_bound(model, x: str, child_cutoff: int, marr_cutoff: int) -> tuple:
    """True when the person must have passed the age limit whatever their
    own (missing) dates say: a child born long enough ago, or a marriage
    recorded long enough ago, pushes the person's birth past the ceiling.
    Returns (dead, evidence)."""
    p = model.people[x]
    for fx in p.fams:
        fam = model.families.get(fx)
        if not fam:
            continue
        for c in fam.chil:
            cp = model.people.get(c)
            if not cp:
                continue
            cb = _birth_year(cp)
            if cb is not None and cb <= child_cutoff:
                return True, f"a child was born {cb}"
        for e in fam.events:
            if (e.tag == "MARR" and e.date and e.date.y1
                    and e.date.y1 <= marr_cutoff):
                return True, f"a marriage was recorded {e.date.y1}"
    return False, ""


def _latest_year(person) -> int | None:
    years = [e.date.year for e in person.events
             if e.date and e.date.year]
    return max(years) if years else None


def _birth_year(person) -> int | None:
    for tag in BIRTH_LIKE:
        for e in person.events:
            if e.tag == tag and e.date and e.date.year:
                return e.date.year
    return None


def living_set(model, age_limit: int = 100, reasons: dict | None = None) -> set:
    today = date.today().year
    birth_cutoff = today - age_limit          # born this year -> 100 now
    event_cutoff = today - (age_limit - 16)   # event year implies birth +16
    child_cutoff = today - (age_limit - MIN_PARENT_AGE)   # today-86
    marr_cutoff = today - (age_limit + MIN_MARRIAGE_AGE)  # today-116

    verdict: dict = {}    # xref -> True (living) / False (dead)
    why: dict = {}
    marker: set = set()   # [Living] placeholders: exempt from the ceiling

    def set_verdict(x, v, reason) -> bool:
        if verdict.get(x) is v:
            return False
        verdict[x] = v
        if v:
            why[x] = reason
        else:
            why.pop(x, None)
        return True

    # 1-4: the direct evidence
    for x, p in model.people.items():
        name = p.name.raw
        if "[Living]" in name or name.strip().startswith("[Living]"):
            marker.add(x)
            set_verdict(x, True, "the GEDCOM's [Living] name marker")
            continue
        if any(e.tag in DEATH_LIKE for e in p.events):
            set_verdict(x, False, "death recorded")
            continue
        by = _birth_year(p)
        if by is not None:
            set_verdict(x, by >= birth_cutoff,
                        f"born {by}" if by >= birth_cutoff else "")
            continue
        ly = _latest_year(p)
        if ly is not None:
            set_verdict(x, ly >= event_cutoff,
                        f"latest event {ly}" if ly >= event_cutoff else "")
            continue
        verdict.setdefault(x, None)   # undecided for the fixpoint

    # the hard ceiling: nobody over the age limit counts as living, and the
    # inference below cannot overturn it. The explicit [Living] marker is
    # the editor's own ruling and stays.
    for x in [x for x, v in verdict.items() if v is True and x not in marker]:
        bound, _ = _dead_bound(model, x, child_cutoff, marr_cutoff)
        if bound:
            verdict[x] = False
            why.pop(x, None)

    # 5: propagate through family links, with the same ceiling honoured:
    # an undated person may be called living through a living parent only
    # (a living parent bounds the birth), never past a dead bound.
    def links(x):
        p = model.people[x]
        out = []
        for f in p.famc + p.fams:
            fam = model.families.get(f)
            if not fam:
                continue
            for s in (fam.husb, fam.wife):
                if s and s != x:
                    out.append(s)
            out.extend(c for c in fam.chil if c != x)
        return out

    def parents(x):
        out = []
        for f in model.people[x].famc:
            fam = model.families.get(f)
            if not fam:
                continue
            for s in (fam.husb, fam.wife):
                if s and s != x:
                    out.append(s)
        return out

    changed = True
    while changed:
        changed = False
        for x, p in model.people.items():
            if verdict.get(x) is not None:
                continue
            bound, _ = _dead_bound(model, x, child_cutoff, marr_cutoff)
            if bound:
                verdict[x] = False
                changed = True
                continue
            kin = [verdict.get(k) for k in links(x) if k in verdict]
            if any(verdict.get(par) is True for par in parents(x)
                   if par in verdict):
                verdict[x] = True
                why[x] = (f"undated, but a living parent bounds the birth "
                          f"to after {child_cutoff}")
                changed = True
            elif any(k is True for k in kin):
                verdict[x] = True
                why[x] = "undated, but a close relative is living"
                changed = True
            elif kin and all(k is False for k in kin):
                verdict[x] = False
                changed = True

    # still open: treated as living (the safe side)
    for x, p in model.people.items():
        if verdict.get(x) is None:
            verdict[x] = True
            why[x] = "undated and unresolved; treated as living to be safe"
    if reasons is not None:
        reasons.update(why)
    return {x for x, v in verdict.items() if v}


def redact(model, living: set) -> dict:
    """Strip the living people in place; returns counts for the report."""
    counts = {"people": 0, "events": 0, "notes": 0, "media": 0}
    for x, p in model.people.items():
        if x not in living:
            continue
        counts["people"] += 1
        counts["events"] += len(p.events)
        counts["notes"] += len(p.notes)
        counts["media"] += len(p.media)
        surname = p.name.surname
        p.events = []
        p.citations = []
        p.notes = []
        p.media = []
        p.refs = {}
        p.names = [type(p.name)(raw=f"[Living] /{surname}/",
                                given="[Living]", surname=surname)]
    # family events (marriages) hide when either spouse is living
    for fx, fam in model.families.items():
        if fam.husb in living or fam.wife in living:
            counts["events"] += len(fam.events)
            counts["media"] += len(fam.media)
            fam.events = []
            fam.media = []
            fam.citations = []
    return counts


def media_privacy(model, living: set) -> set:
    """Media paths that must not be published because their context is a
    living person or a family with a living spouse."""
    withheld = set()
    for x, p in model.people.items():
        if x in living:
            for m in p.media:
                withheld.add(m.path)
            for e in p.events:
                for cit in e.citations:
                    for m in cit.media:
                        withheld.add(m.path)
    for fx, fam in model.families.items():
        if fam.husb in living or fam.wife in living:
            for m in fam.media:
                withheld.add(m.path)
            for e in fam.events:
                for cit in e.citations:
                    for m in cit.media:
                        withheld.add(m.path)
    return withheld
