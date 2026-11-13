# reference/estate_tree.yml - the schema

```yaml

tree: {start: T010}          # the person the big tree opens on
sources:
  <key>:
    title: "..."             # required
    author: "..."            # optional
    url: "/documents/x/1/"   # optional; starts with / (no spaces) or https://
    kind: document | literature | database | web | report   # required; report = reported by the editor, not held by the edition (reference/sources/)
places:
  <key>:
    name: "Trabczyn, Konin district, Greater Poland"   # required
    lat: 52.215              # optional, both or neither
    lon: 17.83
    coord_source: "reference/place_coords.yml"  # required with lat/lon
people:
  <id>:                      # T001 ... (GEDCOM xref without @)
    given: "Jan"
    surname: "Otto-Trampczynski"
    sex: M | F | U
    rule: holder | spouse | child | connector | party
    page: "/people/jan/"     # optional
    events:
      - type: BIRT | DEAT | BURI | RESI | OCCU | EVEN
        label: "Held Trabczyn"   # EVEN: TYPE; OCCU: the occupation; else TYPE
        date: "BEF 6 OCT 1693"   # GEDCOM date phrase; optional
        place: trabczyn          # a places key; optional
        note: "..."              # optional
        cite: [{source: konin145, page: "doc 1, p. 2", exact: true}]  # >= 1
    notes: ["..."]
families:
  <id>:                      # F001 ...
    husb: T001
    wife: T002
    children: [T003, T004]
    cite: [{source: ..., page: ...}]     # required
    marr: {date: "...", place: ..., note: ..., cite: [...]}   # cite required
```

Validation: all references resolve; every person is in a family (unless alone);
every event/family/marriage is cited; a date citing a `database` source needs a
cite with exact: true; no "?", "ok.", "okolo", "prawdopodobnie" in dates; rule
and sex in their sets; lat/lon both or neither, numeric, inside lat 49-55 /
lon 14-25 (unless coord_source says "outside Poland") and with a coord_source;
a site-relative url has no space.

Build: `python pipeline/genealogy/build_estate.py [--yml F] [--ged F] [--out D] [--check]`.
The JSON has the Zelmer data's shape; post-processing adds `url`/`kind` to sources,
`rule`/`page` to person shards, `exact` to citations, `coord_source` to places, and
`tree`, `title`, `start`, `media`, `source` to meta.json.
