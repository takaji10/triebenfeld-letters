# The exclusion pass (PLAN.md section 4.3, as ruled on 2026-11-06).
#
# The editor's ruling, in its final form: everything connected to Larry
# Charles Lacko ONLY through his ancestors leaves the database - their
# whole family world, walked in every direction (up through the
# ancestors, down through all their children, sideways through every
# marriage, and onward through the spouses' own parents and other
# marriages: the natal Trzeciaks, Chikowskis, Klowaks, Roths and the
# rest that earlier passes left standing behind an in-law). Larry
# himself, his blood descendants and the whole world reachable from him
# - the Zelmer side and its in-laws - stay.
#
# The cut is therefore a partition by connectivity, not a fixpoint of
# pairwise rules. (Two fixpoint attempts failed in instructive ways: the
# first kept a child whenever one parent was kept, which let a removed
# sibling's line keep its outsider spouse alive and survive its own
# exclusion; the second followed blood alone, which left the in-laws'
# natal families standing behind the removed spouses. A connected
# component has no rules to deadlock: )
#
#   seed   = the blood ancestors of the roots (both parents at every
#            step, so the wives' lines walk up too);
#   kept   = everything reachable from the roots through ANY family link
#            without entering the seed - Larry's world: his descendants
#            and their spouses' families, the Zelmer side entire;
#   removed= the seed plus everything reachable from the seed through
#            any family link without entering the kept set - the
#            ancestors' world entire.
#
# A person reachable from both worlds stays (a branch member who married
# back into Larry's world, say): belonging to both, neither walk may
# take them, and the sanitising pass keeps their links honest. Every
# removal is written to the exclusion report for the editor's sign-off
# before anything is published.

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Exclusion:
    removed_people: set = field(default_factory=set)
    removed_media: set = field(default_factory=set)     # media paths
    removed_families: set = field(default_factory=set)
    cut_links: list = field(default_factory=list)       # kept people whose
    # famc had to be cleared because their parents left (the root's case)
    sanitized: list = field(default_factory=list)       # other cleared refs
    report_rows: list = field(default_factory=list)


def _parents_of(model, xref: str) -> list:
    out = []
    for fam_xref in model.people[xref].famc:
        fam = model.families.get(fam_xref)
        if not fam:
            continue
        for role in ("husb", "wife"):
            if getattr(fam, role):
                out.append(getattr(fam, role))
    return out


def _neighbours(model, xref: str) -> list:
    """Every person one family link away: parents, co-spouses, children."""
    p = model.people[xref]
    out = []
    for fam_xref in p.famc:
        fam = model.families.get(fam_xref)
        if fam:
            out.extend(s for s in (fam.husb, fam.wife) if s)
    for fam_xref in p.fams:
        fam = model.families.get(fam_xref)
        if fam:
            out.extend(s for s in (fam.husb, fam.wife) if s and s != xref)
            out.extend(fam.chil)
    return out


def _closure(model, start: list, blocked: set) -> set:
    """All people reachable from start through any family link, never
    stepping into blocked (a blocked person is neither visited nor
    passed through)."""
    seen = set()
    frontier = list(start)
    while frontier:
        x = frontier.pop()
        if x in seen:
            continue
        seen.add(x)
        for n in _neighbours(model, x):
            if n not in seen and n not in blocked and n in model.people:
                frontier.append(n)
    return seen


def prune(model, roots: list[str], extra_people: list[str] | None = None) -> Exclusion:
    roots = [r if r.startswith("@") else f"@{r}@" for r in roots]
    for r in roots:
        if r not in model.people:
            raise ValueError(f"exclusion root {r} is not in the database")
    extra = ["@" + x.strip("@") + "@" for x in (extra_people or [])]
    for x in extra:
        if x not in model.people:
            raise ValueError(f"excluded person {x} is not in the database")

    ex = Exclusion()

    # --- seed: the blood ancestors of the roots ------------------------
    seed = set()
    frontier = list(roots)
    while frontier:
        x = frontier.pop()
        for par in _parents_of(model, x):
            if par not in seed:
                seed.add(par)
                frontier.append(par)

    # --- the kept world: from the roots through any link, cut at the
    #     seed (Larry's descendants, their spouses and in-laws, the
    #     Zelmer side - everything the editor keeps) --------------------
    kept = _closure(model, roots, blocked=seed)

    # --- the excluded world: from the seed through any link, cut at
    #     the kept set (the ancestors' world: descendants in every
    #     branch, the spouses married into it, and the spouses' own
    #     families behind them) ----------------------------------------
    removed = _closure(model, sorted(seed), blocked=kept)
    removed |= seed
    # islands named explicitly in the config: no recorded link joins them
    # to either world, so no walk can reach them
    removed |= set(extra)

    # --- families: gone when both spouses and all children are ----------
    for fx, fam in model.families.items():
        members = [s for s in (fam.husb, fam.wife) if s] + fam.chil
        if members and all(m in removed for m in members):
            ex.removed_families.add(fx)

    # --- the root's own famc: its parents are gone; clear the link and
    #     note it, so the tree renders the root honestly
    for r in roots:
        p = model.people[r]
        for fam_xref in list(p.famc):
            fam = model.families.get(fam_xref)
            if fam is None:
                continue
            par = [s for s in (fam.husb, fam.wife) if s]
            if par and all(s in removed for s in par):
                p.famc.remove(fam_xref)
                fam.chil = [c for c in fam.chil if c != r]
                ex.cut_links.append({"person": r, "family": fam_xref})

    # --- media: anything whose only owners are removed people -----------
    owners: dict = {}   # media path -> set of owner xrefs
    for x, p in model.people.items():
        for m in p.media:
            owners.setdefault(m.path, set()).add(x)
    for x, p in model.people.items():
        for e in p.events:
            for cit in e.citations:
                for m in cit.media:
                    owners.setdefault(m.path, set()).add(x)
    for fx, fam in model.families.items():
        members = [s for s in (fam.husb, fam.wife) if s] + fam.chil
        for m in fam.media:
            owners.setdefault(m.path, set()).update(members)
        for e in fam.events:
            for cit in e.citations:
                for m in cit.media:
                    owners.setdefault(m.path, set()).update(members)
    for sx, s in model.sources.items():
        for m in s.media:
            owners.setdefault(m.path, set()).add(sx)
    for path, own in owners.items():
        if own and all(o in removed or o in ex.removed_families
                       for o in own):
            ex.removed_media.add(path)

    ex.removed_people = removed
    # --- sanitise the kept graph: no reference into the removed set ------
    sanitized = []
    for fx, fam in model.families.items():
        if fx in ex.removed_families:
            continue
        if fam.husb in removed:
            sanitized.append(f"family {fx}: parent link to {fam.husb} cleared")
            fam.husb = ""
        if fam.wife in removed:
            sanitized.append(f"family {fx}: parent link to {fam.wife} cleared")
            fam.wife = ""
        kept_chil = [c for c in fam.chil if c not in removed]
        if len(kept_chil) != len(fam.chil):
            sanitized.append(
                f"family {fx}: {len(fam.chil) - len(kept_chil)} child "
                f"link(s) cleared")
            fam.chil = kept_chil
    for x, p in model.people.items():
        if x in removed:
            continue
        kept_famc = [f for f in p.famc if f not in ex.removed_families]
        if len(kept_famc) != len(p.famc):
            sanitized.append(f"person {x}: famc link(s) cleared")
            p.famc = kept_famc
        kept_fams = [f for f in p.fams if f not in ex.removed_families]
        if len(kept_fams) != len(p.fams):
            sanitized.append(f"person {x}: fams link(s) cleared")
            p.fams = kept_fams
    ex.sanitized = sanitized
    # report rows, sorted for a stable diff between builds
    ex.report_rows = sorted(
        ({"xref": x, "name": model.people[x].display}
         for x in removed if x in model.people),
        key=lambda r: r["xref"])
    return ex
