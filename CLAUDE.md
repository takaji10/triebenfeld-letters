# Notes for Claude

Read at the start of every session. Short on purpose: the detail lives in the
files it points to.

## Start here

- `README.md`: what the edition is, the layout, how a holding is added.
- `docs/README.md`: which docs are standing reference. `docs/NEEDS_CONFIRMATION.md`
  is the live list of open questions; keep it current when something is settled.
- `docs/HOUSE_STYLE.md` governs everything written about the documents;
  `docs/EDITORIAL_RULES.md` the transcriptions, which are never "tidied".
- The editor is `takaji10`. They do not read German: German text is written
  here, and checked by the claim check or by Claude, not by them.

## "Access the dictionary hosts"

When the editor says this, they mean: the cloud environment now allows the
reference sites the glossary's draft definitions are to be checked against,
so check them.

1. Confirm the hosts answer: `curl -sS -o /dev/null -w '%{http_code}'` to
   `https://www.woerterbuchnetz.de/` (Adelung, Grimm),
   `https://kruenitz.uni-trier.de/` (Krünitz, Oekonomische Encyklopädie) and
   `https://pl.wikisource.org/wiki/Encyklopedia_staropolska` (Gloger). Try
   WebFetch too. If any is refused, say which, and how to allow it: the cloud
   environment menu in the session's title bar, Edit, Network access, add the
   host to the allowed domains (read `read_documentation` topic
   `environment.network` for the current wording). Do what the reachable
   hosts allow.
2. Work through `reference/glossary.yml`: every entry with `checked: false`
   names its `check_against` work. Look the term up there (Gloger for Polish
   terms: starosta, wójt, sołtys, olędrzy, propinacja, łan, komornik, sąd
   pokoju; Krünitz for land, money and measures; Adelung for words and
   formulas). Correct the English and German definitions where the work says
   otherwise, then set `checked: true` and a `source:` naming the work and
   the entry (with its URL). Leave `checked: false` where the work is not
   online here (the Allgemeines Landrecht, the Hypothekenordnung, Acta
   Borussica, Grotefend) and say so.
3. Rebuild and verify: `python3 pipeline/build/build_site_data.py`,
   `cd site && bundle exec jekyll build` (gems: `bundle config set --local
   path vendor/bundle && bundle install` first in a fresh container),
   `python3 verify_site.py`. Commit, and update `docs/NEEDS_CONFIRMATION.md`
   (Glossary section) and the changelog.

## How this project is worked

- **Branch and publishing.** Develop on the session's branch. The live site
  (https://takaji10.github.io/triebenfeld-letters/) is built from `main` by
  `.github/workflows/pages.yml`, which runs `verify_site.py` as a gate. To
  publish, fast-forward `main` to the branch and push, then confirm the
  "Build and deploy" run succeeded. Publish only when the editor says so.
- **Line endings.** Many files are CRLF (`docs/*.md`, `site/_data/i18n.yml`,
  `site/_layouts/*.html`, `README.md`, `browse.js`). Edit them preserving CRLF
  and check `git diff --stat` shows only the real change.
- **Not in the repository:** `review/` (generated sheets), `cache/` (model
  output, on the editor's machine), raw scans. There is no Anthropic API key
  here: paid runs (translate.py, summarise.py, read_letters.py) happen on the
  editor's machine. `regenerate.py` cannot run end to end in the cloud (its
  early steps fetch from DWDS and write into `review/`); run the later steps
  directly.
- **Fixing the English** without re-translating: rules go in
  `reference/english_forms.yml`, one-page corrections (with the German that
  decided them) in `reference/english_corrections.yml`. Both are applied by
  `pipeline/translate/english_forms.py --apply` and by publish_translations.py
  at every publish, so a re-publish keeps them. Never hand-edit
  `site/_data/translations/` alone.
- **The glossary** (`reference/glossary.yml`, plan in `docs/GLOSSARY_PLAN.md`):
  English and German written separately; read every new pattern against its
  matches in `review/glossary_matches.csv` before publishing.
  `glossary_candidates.py --check` is a gate in regenerate.py: a translated
  holding's qualifying words must each be an entry or ruled out under
  `excluded:` with a reason.
- **Sources supplied by the editor** go in `reference/sources/`, verbatim with
  a working translation, and entries cite them with `source:`.

## Where things stand (2026-10-02)

- Glossary live: 108 entries, 98 words ruled out. 55 checked: the
  patrimonial court (the editor's Szukaj w Archiwach source) and 54 read
  against Krünitz, Adelung, Grimm and Gloger. The other 53 wait on works not
  online here, or have no entry in those that are (NEEDS_CONFIRMATION).
- Deferred by the editor: redoing the 14525/14526 summaries the way the other
  holdings' were (paid, about $5-10, on their machine).
- Open before wider sharing: the archives' permission for the scans; the
  editor's full name for the licences (`site/_data/rights.yml` and `LICENSE`).
- Everything else open is in `docs/NEEDS_CONFIRMATION.md`.
