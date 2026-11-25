# The to-do page: plan (2026-11-25)

The editor's request: turn the to-do list into a page on the site, linked from
the footer, set up like a spot sheet so that they can give answers there, with
links to the documents an item concerns, and a rule that the page is updated
whenever the list changes. **Planned, nothing built.** The decisions marked
"Editor" at the end are asked before the work begins.

## 1. What is there now

- `docs/TODO.md`: 1,805 lines, 70 numbered sections (one per holding or
  project, in the order they were added), 133 open boxes and 286 ticked. Free
  prose inside each box, written for the editor but not in a fixed shape: a box
  can be a question ("is the office note's 13 April 1816?"), a task for the
  editor ("name the ones left unplaced"), work for Claude ("glossary entries
  for desiatin, sazhen and mansi") or a wait ("the German summaries, all at
  once, your word").
- `docs/NEEDS_CONFIRMATION.md`: 2,599 lines, the real store of open
  questions about readings and identifications; the to-do list points into it.
- Spot sheets (`pipeline/review/queries.py`): a local page with one card per
  question, buttons for the candidate readings, "Something else", a note, saved
  at once to `review/<slug>/..._answers.json` on the editor's machine, applied
  by a script afterwards. The English layout editor (`?edit`) is the
  precedent for a tool on the live site: the editor works in the browser and
  **exports a file** the session applies ("Apply my layout file").

## 2. The central decision: one source, and it is not the prose

A page cannot be built reliably from 1,800 lines of free prose, and two
copies (prose and page) would drift the first week. So:

- **`reference/todo.yml` becomes the one source** of every open item. Each item
  has a stable `id`, and these fields:
  `group`, `title`, `kind`, `text` (what it is and why it matters, standing on
  its own, HOUSE_STYLE "No cryptic statements"), `links` (the documents,
  people, places, works it concerns), `options` (for a choice),
  `needs_confirmation` (the anchor in NEEDS_CONFIRMATION, if any), `added`,
  `status`.
- **`docs/TODO.md` is generated from it** by the same script (a heading and a
  box per item, the ticked ones kept in an archive section of the YAML, so the
  list's history is not lost). Nobody edits TODO.md by hand again; its first
  line says so. This makes the page and the list one thing.
- The 286 ticked boxes are not on the page. They are kept in the YAML under
  `done:` (id, title, date) for the record.

## 3. The kinds of item (what the page does with each)

| Kind | Example | On the page |
|---|---|---|
| `question` | Chełmski's loan: 12,000 ducats or 36,000? | buttons for the candidate answers, "Something else", a note |
| `decision` | Is the Jezierski of the documents the General at Venice? | Yes / No / Can't tell, note |
| `task` (yours) | Look at the four crops of Nr. 1414 | "Done", "Later", a note |
| `claude` | Glossary entries for desiatin, sazhen, mansi | shown in a collapsed "Claude's queue", no answer needed; the editor can reorder or strike |
| `waiting` | The German summaries, all at once | "Now" / "Not yet", with the editor's word recorded |

The default view is **For you**: questions, decisions and your tasks, about
fifty items once the 133 boxes are sorted. Claude's queue is one click away,
so the page stays an action list and not an inventory.

## 4. The page

- Address `/todo/` (a working page: `noindex`, English only; see Editor 1 and
  2). Linked from the footer, one line beside "Rights".
- **Top:** the count ("38 for you, 61 in Claude's queue"), a search box (the
  site's bar, so this is its first use on a non-source page), filters by group
  (a holding, the literature, places, people, the site) and by kind, a
  progress line ("12 answered, not yet handed in").
- **Body:** the cards, grouped by holding or project, the group heading naming
  it as the list does now ("I. HA GR, Rep. 7 C, Nr. 421: Chełmski's claim on
  Prusimski, 1799"). A card is: the title; two or three sentences that say who
  and what and why it matters; **links** as chips ("Nr. 421, document 3",
  "Prusimski", "Konin Gr.145 p. 12"), each a real page address the build checks;
  the answer controls; the note box; a link to the full discussion in
  NEEDS_CONFIRMATION where there is one.
- **Answers** are kept in the browser as the editor goes (`localStorage`, the
  same as the spot sheet saves "at once"), and shown as a green edge on the
  card. **Export answers** downloads `todo_answers_<date>.json`; **Import**
  reads one back, so the work can move between the desktop and a phone (the
  editor works in both; the storage is per device). An item whose text has
  changed since the answer was given is marked "changed since you answered".
- Mobile-first: one column, big buttons, as the spot sheets the editor
  answers from a phone (WORKING_NOTES).

## 5. Applying the answers ("Apply my to-do answers")

The page cannot write to the repository (it is a static site), so the loop is
the layout file's: the editor exports the file and hands it over; Claude runs
`python pipeline/todo/import_answers.py <file>` (a check: lists every answer
with its item, refuses ids that no longer exist), then `--write`:

1. the answer is recorded in the item's `answer:` and the item moves to
   `done:` (or stays open with the note, if the answer was "Later" or a
   question back to Claude);
2. a settled question is also written where it belongs (`rulings.yml`, the
   unit's `notes.md`, NEEDS_CONFIRMATION taken off the list, the changelog),
   as CLAUDE.md already requires for any ruling, by Claude, since each ruling
   changes a text;
3. the page and TODO.md are rebuilt, the answered cards disappear, the commit
   says which ids were closed. The editor's own words are never edited.

## 6. The rule that keeps it current (to go in CLAUDE.md and WORKING_NOTES)

> **The to-do list is `reference/todo.yml`; the page `/todo/` and
> `docs/TODO.md` are built from it.** Adding, changing, completing or removing
> an item means editing the YAML, running `pipeline/todo/build_todo.py`, and
> committing the YAML, the page data and TODO.md together. A session that ends
> a piece of work ticks or moves its items in the same sitting. Every report
> that closes an item says so.

And three checks so the rule does not rest on memory:

1. `pipeline/todo/build_todo.py --check` (a gate in `pipeline/verify_site.py`,
   so the Pages workflow stops on it): the generated TODO.md and the page data
   equal what the YAML gives; every id unique; every link resolves to a built
   page; every `question` has options or says why not.
2. The existing `lessons_check.py` stop hook is extended: committed work in
   which a `units/*/notes.md` or `docs/NEEDS_CONFIRMATION.md` changed but
   `reference/todo.yml` did not asks once whether an item was closed.
3. A hand edit of `docs/TODO.md` fails the gate (it differs from the build).

## 7. Building it (in this order; each step offered first to a script, then to
a Sonnet sub-agent, as CLAUDE.md says)

1. **Convert** (script + Sonnet readers): parse the 70 sections and 133 open
   boxes into draft items, one Sonnet reader per ten sections rewriting each to
   stand alone, naming the documents it concerns, and proposing the kind; the
   script checks every named unit slug and document number exists. Claude
   reads and corrects every item and settles the kinds. The 286 ticked boxes
   go into `done:` by script, untouched.
2. **Link the items to documents:** a `links:` entry is a unit slug and
   optionally a document number or page (`units/<slug>`), a person or place
   slug, or a literature work; the build turns each into the site address
   through the data the site already has, so a renamed page is caught by the
   gate, not found by the editor.
3. **Build the page** (`site/todo.html`, `assets/todo.js`, the data file
   `site/_data/todo.json`, the footer link): the cards, filters, autosave,
   export and import, in the site's styles (the new search-bar look).
4. **The importer** (`pipeline/todo/import_answers.py`), tested on a made-up
   answer file.
5. **The rule and the gates** (section 6), a WORKING_NOTES section, the
   changelog, and the first real use: the editor answers the 70a differences
   (the nine open points on the relevant people) from the page.
6. **Later, if wanted:** the open questions of NEEDS_CONFIRMATION as items of
   the same page (about 2,600 lines, a different job: each question already
   has a context paragraph and often candidate readings, so they are the
   best fit for the answer buttons).

Size: steps 1-2 are the bulk of the work (reading 133 items); 3-5 are a normal
page build.

## 8. Decisions for the editor

1. **A public page.** The live site is public. A page of working notes is
   readable by anyone with the address, and the footer link makes it easy to
   find. Recommended: `noindex`, English only, a first line saying it is the
   editor's working list. (If the repository is public, `docs/TODO.md` is
   already readable there.) Or: a page not linked from the footer, only by
   address.
2. **English only.** The editor does not read German; the page has no German
   twin, which the build and `verify_site.py` must be told to allow for one
   page. Recommended: yes.
3. **One source.** `reference/todo.yml` as the single source with TODO.md
   generated (section 2), against keeping TODO.md as the source and parsing
   it. Recommended: the YAML; it is the only way the page cannot drift.
4. **Claude's own items on the page** (collapsed "Claude's queue") or only
   the editor's. Recommended: both, collapsed, so the editor can see what is
   waiting on Claude and strike or reorder it.
5. **NEEDS_CONFIRMATION** in the first build, or later (step 6). Recommended:
   later; the to-do list first, since it points into it.
