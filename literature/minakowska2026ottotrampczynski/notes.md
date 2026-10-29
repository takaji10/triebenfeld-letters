# Minakowska (2026): the page of Wojciech Otto-Trąmpczyński in Wielka genealogia Minakowskiej

The page of Wojciech Otto-Trąmpczyński, person sw.35437 of M. J. Minakowska's
online database (https://www.sejm-wielki.pl/b/sw.35437), its own citation
line "wydanie z 22.10.2026". Added 2026-10-22 at the editor's word. The
fourth of the database's pages (`minakowska2026prusimski`,
`minakowska2026zielonacka`, `minakowska2026miaczynski`; the standing rule
is docs/LITERATURE_PLAN.md, section 22).

## The subject and why he matters

Wojciech Otto-Trąmpczyński is of the family of the edition's `trampczynski`
entry - the family that held Trąbczyn before the Prusimskis and took its
name from it, with the by-name Otto. The edition's documents name the
family five times (1589 Albertus's suit over the pond at Łukom; the decree
of 1644 against the brothers Marcin, Wojciech, Władysław and Andrzej, sons
of the late Stanisław, and their widow Anna of Słończyce; 1776; 1791). The
database's page is of the sixteenth-century Wojciech: no biography, no
parents, no tree, no siblings - only the marriage about 1590 (its
estimate) to Anna Cerekwicka, the son Stanisław, and the descent through
him (Władysław and Andrzej and Anna and the second Władysław among the
grandchildren - **the names of the decree of 1644's brothers**), down to
Dorota (died 1722..1724).

## The source

The editor's saved page, in their Downloads folder ("Wojciech
Otto-Trampczynski (M.J. Minakowska, Genealogia potomków Sejmu
Wielkiego).htm", the name ASCII-folded). Not kept in the repository (the
editor's login in the header, the visitor's IP in the footer).
`make_original.py` makes `original.md` and `full.md` from it and says what
it does.

Polish interface again (the work's language is the saved page's own),
ISO-8859-2. **The person number is of the database's "sw." branch** -
sw.35437, the numbers of the Teki Dworzaczka regests, not of a Boniecki
article (2.976.…), not of a family branch (4.285.…): this person came into
the database from a regest, and the regest is the page's one source. A
fourth kind of number, standing beside the other two.

The page carries the author's book advertisement **inside the marriages
section** (before the Najbliżsi heading), not in the footer; the chrome
rule takes it out the same way. The first work's script keyed the book's
lines as footer chrome; this page proves the key is positional - it works
wherever the advertisement sits.

## What is brought in (the standing selection, section 22)

The biographical line and the marriage with the children and the
grandchildren - everything the page has but the nearest PSB persons and
the Uwagi. There is no Rodzice section, no ancestor tree (the "#
Przodkowie" heading the first and third works' scripts add is not added),
no Rodzeństwo, no mother's other marriages: the subject of the sixteenth
century is known to the database by his marriage and descent alone. The
page has no "Wnuki" heading of its own; the grandchildren run inside the
one marriages heading, as on the second page, and no added heading is
needed.

## Against the documents (the documents first)

- **The descent fits the decree of 1644.** The database's grandchildren
  Władysław and Andrzej and Anna (and a second Władysław, and the second
  Wojciech) are of the generation of the decree's brothers Marcin,
  Wojciech, Władysław and Andrzej, "sons of the late Stanisław", and
  their widow Anna of Słończyce; the database's Stanisław's wife is
  **Anna Słonecka of Słończyce** - the same settlement. The page's
  Stanisław is the decree's late father. The database's marriage
  generation fits the documents' one.
- **The regest of 1614** (the Uwagi; Teki Dworzaczka, Księgi grodzkie
  pyzdrskie, cz. 1, nr 2152, Nr 137): Stanisław Trąmpczyński, son of
  Wojciech Otha Trąmpczyński, promises Jan Słonecki, son of Marcin, that
  after the wedding of Anna Słonecka (daughter of the late Stanisław
  Słonecki, cup-bearer of Kalisz, by Elżbieta Chwalibowska) he will
  secure her 7,000 zł on half the estates (fol. 255). This is the record
  behind the marriage the page dates about 1590 - and it names **the
  subject** ("s. o. Wojc. Otha Tr."), so the database's person came from
  it. The register (Pyzdry court books) is not one the edition holds;
  whether to seek it is the editor's (NEEDS_CONFIRMATION).
- **The dates.** "Born probably in 1560" is the database's estimate; the
  marriage "about 1590" likewise; every date of the descent carries the
  question mark (?1570-, ?1600-, ?1630-, ?1650-, ?1690-) - and none is
  used anywhere in the edition. The regest's own date, 1614, is stated
  and is the one date of the family's story the page carries.
- **The by-name.** The regest writes "Otha", the page "Otto-" - the
  record's own form, kept as printed in both.

## The index, and the pipeline fix the work forced

The work's text has 9 hits of the family's name, all ruled
(`literature/index.yml`): the subject and his descendants - yes; "w
Trąmpczyńskich Ol." in Chodyła (2015) n. 34 - the Olędry colony named for
the family, not a person - no; "Janem Trąmpczyńskim herbu Topór (1700)"
in Żychliński (1885) p. 187 - a Trąmpczyński of the Opaliński genealogy,
not shown to be of the family - no.

**But the hits could not be had at all until
`pipeline/literature/literature_index.py` was fixed.** The edition's
`trampczynski` entry carries `only_in` (the five documents), so its
pattern matches nothing in a literature uid; the literature extra-pattern
route would have supplied the hits, but the dedup in `hits()` dropped
them, because the edition's pattern fullmatches the same surfaces whether
or not it applies to the record. The dedup now asks `applies()` first:
an extra hit is dropped only where an edition pattern of the same slug
can actually fire in the record. Without it, a work whose subject is an
`only_in` person could never have its hits counted - this work would
have been silently invisible to the index. (The fix is general, not
particular to this work: any future `only_in` person stands the same
way.)

Also new in `literature/index.yml`: the `patterns:` entry
`trampczynski: 'Trąmpczy[nń]sk\w*'` (the bare form, beside the first
work's pattern keys) and the `people:` section's first rulings for the
slug.

## The person's page

/people/wojciech-otto-trampczynski/
(/de/personen/wojciech-otto-trampczynski/), a standalone person (the
block's own heading and bio, no documents, the literature named by hand).
**The slug is deliberately not the family entry's** (`trampczynski`):
the family is an entry of the edition with a heading and biography and
five documents of its own, and a block keyed by that slug would collide
with it in the layout - the page would show the family's heading and
bio. The first try did exactly that and was caught in the build; the
block was renamed and a comment in `reference/genealogy.yml` records
both the collision and the rule: **a standalone block's slug must not be
an entry's slug.** The family entry itself has no page (it never had a
genealogy block); whether it is to have one is the editor's.

## Links

None written yet. The obvious one, when the editor wants it: the work's
descent section against the decree of 1644 (APP 53/6/0/-/36) - the same
family, the database's page giving the brothers' father's father.

## Why it is here

Kept from the work's account, which said it on the page until the voice review of 2026-10-29 (the editor: the reasoning for why a work is relevant is for the notes, not the reader):

> The second Wojciech's marriage to Marianna née Zawadzka carries the line of
> the Trąmpczyńskis that the documents of the seventeenth century name (the
> brothers Marcin, Wojciech, Władysław and Andrzej, sons of the late
> Stanisław, condemned in 1644 at the suit of Jerzy Chełmski). The whole page
> is kept in the work's folder as full.md.
