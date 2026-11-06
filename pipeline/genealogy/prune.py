# The exclusion pass (PLAN.md section 4.3).
#
# The editor's ruling: the ancestors of Larry Charles Lacko are not part of
# this project. The agreed cut removes Larry's parents (Nicholas Lacko and
# Parania Rychlicki), all of their blood ancestors, Larry's siblings through
# either of his parents (the Lacho branch), and anyone whose only connection
# to the kept tree runs through those people (a step-parent's own line, for
# instance). Larry himself, his wife and children, and everyone on the
# Zelmer side stay.
#
# The rules run to a fixpoint and every removal is written to the exclusion
# report for the editor's sign-off before anything is published.

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


def _children_of(model, xref: str) -> list:
    out = []
    for fam_xref in model.people[xref].fams:
        fam = model.families.get(fam_xref)
        if not fam:
            continue
        out.extend(fam.chil)
    return out


def prune(model, roots: list[str]) -> Exclusion:
    roots = [r if r.startswith("@") else f"@{r}@" for r in roots]
    for r in roots:
        if r not in model.people:
            raise ValueError(f"exclusion root {r} is not in the database")

    ex = Exclusion()

    # --- seed: the blood ancestors of the roots ------------------------
    removed = set()
    frontier = list(roots)
    while frontier:
        x = frontier.pop()
        for p in _parents_of(model, x):
            if p not in removed:
                removed.add(p)
                frontier.append(p)

    # --- fixpoint: children, spouses, ancestors -------------------------
    changed = True
    while changed:
        changed = False

        # (b) a person whose parents are all removed goes, unless they are
        #     a root or have a parent that stays (a mixed marriage into the
        #     kept tree keeps the child)
        for x, p in model.people.items():
            if x in removed or x in roots:
                continue
            parents = _parents_of(model, x)
            if parents and all(par in removed for par in parents):
                removed.add(x)
                changed = True

        # (c) a person all of whose own family links run into removed
        #     people goes (the step-parent's line, remarried-out spouses)
        for x, p in model.people.items():
            if x in removed or x in roots:
                continue
            if _parents_of(model, x) and not all(
                    par in removed for par in _parents_of(model, x)):
                continue  # anchored by a kept parent
            dead_families = 0
            fams = [model.families.get(f) for f in p.fams]
            fams = [f for f in fams if f]
            if not fams:
                continue  # no spouse links: nothing to decide here
            for f in fams:
                cos = [s for s in (f.husb, f.wife) if s and s != x]
                kids = f.chil
                if not cos and not kids:
                    continue  # a one-person family is no evidence either way
                if all(s in removed for s in cos) and \
                        all(k in removed for k in kids):
                    dead_families += 1
            if dead_families == len(fams):
                removed.add(x)
                changed = True

        # (d) the ancestors of anyone newly removed, unless they are also
        #     ancestors of a kept person through another child
        for x in list(removed):
            for par in _parents_of(model, x):
                if par in removed:
                    continue
                kept_kids = [k for k in _children_of(model, par)
                             if k not in removed]
                if not kept_kids:
                    removed.add(par)
                    changed = True

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
