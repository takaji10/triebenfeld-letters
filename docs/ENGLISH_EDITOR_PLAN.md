# A layout editor for the English translations

Plan written 2026-11-22 at the editor's word: "The formatting of translations in
archival documents rarely matches the format on the page. I don't have
confidence that AI can do a good job at detecting paragraph breaks and
formatting, so I'm wondering if there's some sort of 'editor' mode that we can
build for the website where it becomes possible to do in-line editing of the
English translations to fix the paragraph formatting. I would need to have a
very simple editor where I can change the breaks, and perhaps create
indentations where text was indented in the original. Adding Italic to text
could be good as well. When finished, there could be a button where I export
changes to my local machine (since the site is static), and then use it to
update the formatting when I work with the text." Nothing is built yet.

## What there is today

- The English of a document is `site/_data/translations/<pad>.yml`: one
  `segments` entry per manuscript page, its `en` plain text, paragraphs
  separated by a blank line, and the edition's label lines ("[Written by the
  receiving office:]", "[Written in the margin:]", "[Written in another
  hand:]", "[The document continues:]").
- That file is **generated**: publish_translations.py writes it from the
  translation cache, then applies `reference/english_forms.yml` (rules) and
  `reference/english_corrections.yml` (one-page find/replace). A hand edit of
  the file is lost at the next publish (CLAUDE.md).
- `site/assets/letter.js` (fillTranslation) turns each paragraph into a `<p>`
  and the label lines into boxes. There is no indentation, no italic and no
  line break inside a paragraph.

So the editor's changes need a home of their own that every publish applies,
and the page needs to show what they say.

## The design

### 1. What can be changed, and nothing else

Only the layout, never a word: the editor cannot type, paste or delete text.
Allowed:

- **Paragraph break**: Enter splits a paragraph at the cursor; Backspace at the
  start of a paragraph (or Delete at its end) joins it to the one before (after).
- **Line break inside a paragraph**: Shift+Enter (addresses, signature blocks,
  lists written one under the other).
- **Indent**: a paragraph indented one, two or three steps (buttons, or Tab /
  Shift+Tab), for text indented on the page.
- **Italic**: on a selection (button, or Ctrl+I).
- **Set apart** (second phase, if wanted): mark a paragraph as written by the
  receiving office, in the margin, or in another hand, or end such a block. This
  writes the label lines the site already understands, so the voices of a
  document can be fixed by eye too.

After every operation the page's text, with all spacing and marks removed, is
compared with the original's; if they differ (a stray keystroke got through),
the operation is undone. That check is what makes it safe to let the editor
work on the live site.

### 2. Where the layout is kept: a markup over the same words

One file per document, `reference/english_layout/<pad>.yml`, written only by
the import script (step 4), holding for each page it touches:

    pages:
      - page: 1
        fingerprint: 9f2c...        # the page's plain text, letters only, hashed
        en: |-
          Most Serene ... King and Lord!

          > Kalisz, 8 October 1799.

          I gave the Starost *von Prusimski* ...

The markup is deliberately small: a blank line ends a paragraph, a single line
end is a line break, `>` / `>>` / `>>>` at a paragraph's start indents it, and
`*...*` is italic (the English never contains an asterisk today; the import
refuses one that is not markup). Readable in a text editor and in a diff.

**Applied at every publish**, after the forms and the corrections, in
`pipeline/translate/english_forms.py` (apply_page), so a re-publish keeps it.
It is applied only if the page's text still has the same fingerprint: if the
words have changed since (a new translation, a correction), the layout is not
applied and the publish reports it, so nothing is laid over the wrong text.
Then the editor lays the page out again.

### 3. The editor on the page

- Reached by adding `?edit` to a document's address (on the live site or the
  local build); nobody else sees it, and nothing is saved anywhere but in the
  editor's own browser until they export, so there is nothing to protect.
- A small bar above the English: *Indent*, *Outdent*, *Italic*, *Line break*,
  *Undo*, *Reset page*, and *Export*; a note of how many pages have changes.
- The English pane becomes editable with the guards of section 1 (the browser's
  `beforeinput` events: only paragraph and line breaks, joins and formatting
  get through).
- Work in progress is kept in the browser's local storage per document, so a
  reload or a closed tab loses nothing; a list of the documents with unsaved
  layout is shown on the bar.
- **Export** downloads one file, `english_layout_<date>.json`, with every
  changed page of every document: pad, page, fingerprint, the marked-up text.

### 4. Bringing the export home

`python pipeline/translate/import_layout.py <file>`: checks each page's
fingerprint against the current English, writes or updates
`reference/english_layout/<pad>.yml`, reports pages whose text has changed
since the export, and then re-publishes the documents touched
(publish_translations, english_forms) so the site data follows. A session told
"apply my layout file" runs it, rebuilds and verifies, and commits.

### 5. Showing it

`letter.js` (fillTranslation) learns the markup: `>` levels as a class
(`indent-1` ... `indent-3`), `*...*` as `<em>`, a single line end as `<br>`,
all built with DOM nodes, never by inserting the text as HTML. The same
markup is read in the dataset exports (plain text with the marks removed),
and verify_site checks that no `*` or `>` mark reaches a page unrendered.

## Steps, and who does them

1. **The markup and its application** (Claude): english_forms.py applies
   `reference/english_layout/`, with the fingerprint check; a test page laid
   out by hand. Small.
2. **Rendering** (Claude, a Sonnet agent for the CSS and the dataset side to a
   spec): letter.js, the style, verify_site's check.
3. **The editor** (Claude: the guarded editing is the delicate part, and is
   tested against every kind of page, the boxed voices, the tables, which are
   not editable, and a page with marks of doubt).
4. **Export and import** (a Sonnet agent writes import_layout.py to a spec;
   Claude checks it on a real export).
5. **A trial with the editor** on one holding (Nr. 421 suggests itself), then
   the rules written into WORKING_NOTES and NEW_UNIT.md, and a line in
   HOUSE_STYLE that the layout of the English is the editor's.
6. **Second phase, if wanted**: setting voices apart from the bar; the same for
   the German reading text (its paragraphs come from paragraph_decisions.csv,
   which the editor could then set by eye too).

Paid runs: none.

## For the editor

1. The markup (blank line, line end, `>` for indent, `*` for italic): agreed,
   or would you rather never see it (the editor shows the result only, and the
   file is for the machine)?
2. The editor reachable on the live site with `?edit` (my recommendation: it
   saves nothing anywhere, so it can be open), or only on your local build?
3. Should the second phase (setting voices apart by eye; the German reading
   text's paragraphs) come with the first?
4. Indentation in three steps enough, or do you also want centred lines (for
   headings and addresses centred on the page)?

## The editor's answers (2026-11-22)

1. No markup in the finished translation; the Tab key indents in the editor.
   (The stored layout is the machine's affair; its form is free.)
2. On the live site.
3. Yes: setting voices apart, and the German reading text's paragraphs, in
   the first version.
4. Yes: alignment left, right and centre.
5. (Massow: no person entry.)

Next session: build it in the plan's steps with these answers.
