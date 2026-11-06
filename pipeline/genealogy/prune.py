# The exclusion pass (PLAN.md section 4.3).
#
# The editor's ruling: the ancestors of Larry Charles Lacko are not part of
# this project. The cut takes Larry's parents (Nicholas Lacko and Parania
# Rychlicki), all of their blood ancestors, and every blood descendant of
# those people except through Larry himself - his siblings and the whole
# Lacho branch, however far down it runs. Spouses married only into the
# removed lines go too. Larry himself, his descendants and everyone on the
# Zelmer side stay.
#
# The removal set is computed in three passes, which replaces the earlier
# fixpoint whose "a child with one kept parent stays" rule deadlocked
# against the same rule keeping the spouse: a removed sibling's children
# kept the outsider spouse alive, the spouse kept the children alive, and
# the sibling's whole line survived the cut it was ruled out of (seen in
# the 2026-11-06 build: I0100's children I2190-I2192 stayed through their
# mother I2189).
#
#   seed      = the blood ancestors of the roots (removed by ruling);
#   protected = the roots and their blood descendants - the "except through
#               I0005" of the plan; a person reached by both walks stays;
#   removed   = the seed plus every blood descendant of the seed that the
#               downward walk reaches without passing the protected line.
#
# Then a fixpoint sweeps the hangers-on the plan names: a spouse whose
# every marriage now runs into removed people (co-spouses and children)
# goes - deliberately regardless of their own natal family, which the
# ruling does not remove: the spouse married into the branch, their
# parents and siblings did not marry into anything. And the ancestors of
# anyone newly removed go when no kept child anchors them any more.
#
# Every removal is written to the exclusion report for the editor's
# sign-off before anything is published.

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


def _blood_descendants(model, starts: list, blocked: set) -> set:
    """Everyone descends from starts through child links alone, never
    passing a blocked person (a blocked person is not removed and the
    walk does not continue through them)."""
    seen = set()
    frontier = list(starts)
    while frontier:
        x = frontier.pop()
        if x in seen:
            continue
        seen.add(x)
        for fam_xref in model.people[x].fams:
            fam = model.families.get(fam_xref)
            if not fam:
                continue
            for c in fam.chil:
                if c not in seen and c not in blocked and c in model.people:
                    frontier.append(c)
    return seen


def prune(model, roots: list[str]) -> Exclusion:
    roots = [r if r.startswith("@") else f"@{r}@" for r in roots]
    for r in roots:
        if r not in model.people:
            raise ValueError(f"exclusion root {r} is not in the database")

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

    # --- protected: the roots and their blood descendants --------------
    protected = _blood_descendants(model, roots, blocked=set())

    # --- the branch: the seed's blood descendants, cut at the protected
    #     line (a person descended from both stays - the plan's "except
    #     through I0005")
    removed = _blood_descendants(model, sorted(seed), blocked=protected)
    removed |= seed

    # --- fixpoint: spouses married only into removed lines, and the
    #     ancestors of the newly removed with no kept child left ---------
    changed = True
    while changed:
        changed = False

        # (c) every marriage runs into removed people
        for x, p in model.people.items():
            if x in removed or x in protected:
                continue
            fams = [model.families.get(f) for f in p.fams]
            fams = [f for f in fams if f]
            if not fams:
                continue
            dead = 0
            for f in fams:
                cos = [s for s in (f.husb, f.wife) if s and s != x]
                kids = f.chil
                if not cos and not kids:
                    continue  # a one-person family is no evidence either way
                if all(s in removed for s in cos) and \
                        all(k in removed for k in kids):
                    dead += 1
            if dead == len(fams):
                removed.add(x)
                changed = True

        # (d) the ancestors of anyone newly removed, unless a kept child
        #     anchors them or they sit on the protected line
        for x in list(removed):
            for par in _parents_of(model, x):
                if par in removed or par in protected:
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
