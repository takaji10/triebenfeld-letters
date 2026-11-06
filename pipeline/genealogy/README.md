# The genealogy explorer's build pipeline.

The family database lives in Gramps on the editor's machine; the explorer
lives on the site. This pipeline is the one-way road between them: it reads
the GEDCOM and the gpkg export, applies the editor's two standing rulings
(the excluded branch, the redaction of living people), and writes the public
JSON the site serves and the web media the genealogy-media repo publishes.
Nothing private ever reaches a repository.

## Updating the database

Export a fresh GEDCOM and gpkg from Gramps anywhere on disk, then point the
build at them (defaults come from config.yml):

```bat
python pipeline\genealogy\build.py --ged J:\Zelmer\new.ged --gpkg J:\Zelmer\new.gpkg
python pipeline\genealogy\media_build.py --dest J:\genealogy-media
```

Every build writes its reports to `review/genealogy/` (gitignored) in two
forms: `excluded.yml`, `privacy_spotcheck.yml` and `build_report.txt` for
the diff, and `index.html`, `excluded.html`, `privacy.html`,
`build_report.html` for reading - the HTML pages are the ones to review,
the text files the ones to compare between builds.

## The files

    config.yml        inputs, the exclusion roots, the privacy age limit
    gedcom.py         the GEDCOM parser -> people, families, events,
                      citations, media, notes, places with coordinates
    grampsxml.py      reads data.gramps out of the gpkg: the media focus
                      rectangles (regions) and checksums, per owner
    prune.py          the excluded branch: Larry Charles Lacko's ancestors,
                      his siblings and everyone attached only through them
    privacy.py        living-person detection (Gramps' "probably alive"
                      rules) and redaction
    build_data.py     the public JSON: index, per-person shards, families,
                      places, sources, the media manifest
    build.py          the orchestrator: runs everything, writes the reports
    media_build.py    the web derivatives: display JPEGs (<= 2400 px,
                      quality 82), 400 px thumbnails, hash-named and
                      immutable; docx kept as originals until LibreOffice
                      converts them

## The media regions

Gramps lets the editor draw a rectangle on a media reference - the focus of
a photograph or the corner of a census page where the person sits. These
regions survive only in data.gramps (the GEDCOM drops them). Each is keyed
by the person it belongs to, because one file can carry several rectangles
(a marriage photo: one for the husband, one for the wife). The site's media
manifest carries them as `regions: {person: [x1, y1, x2, y2]}` in percent
coordinates; the viewer draws the outline for the person whose page is open.

## The two rulings

**Excluded branch.** `config.yml` names the exclusion root (I0005, Larry
Charles Lacko). The cut takes his parents, their blood ancestors, his
siblings through either parent and everyone whose only connection runs
through those people; Larry, his family and the Zelmer side stay. Family
links into the removed set are cleared (they are listed under
`sanitised_references` in the report). Media whose only owners are removed
people is not built.

**Living people.** The GEDCOM's own `[Living]` placeholder, death evidence,
the 100-year birth rule and propagation through parents, spouses and
children decide; anyone still undecided is treated as living. Redaction
keeps only the surname, sex and family links; events, notes, citations and
media never leave the machine.
