# The Triebenfeld Letters — site

A Jekyll site presenting the von Triebenfeld / Hohenlohe-Ingelfingen correspondence
(1798–1816). Built to run on GitHub Pages without any custom plugins.

## Regenerating and previewing

The site's letter pages are **generated** from the research database — don't edit them
by hand, they are overwritten.

```sh
# 0. from the project root: after adding or renaming scans (skips existing)
python3 make_scan_derivatives.py

# 1. from the project root: regenerate letter pages + data + search index
python3 build_site_data.py

# 2. from site/: preview at http://localhost:4000
bundle install          # first time only
bundle exec jekyll serve

# 3. from the project root: verify the built site
python3 ../verify_site.py
```

`build_site_data.py` asserts that every generated page reproduces its corpus text
character-for-character and refuses to finish if anything was altered.

Open the site through `jekyll serve`, not by double-clicking a file — browsers block the
search index from loading over `file://`.

## What is generated vs. hand-maintained

| Path | |
|---|---|
| `_letters/*.html` | **Generated.** Never edit. |
| `assets/search-index.json` | **Generated.** Never edit. |
| `_data/people.yml`, `places.yml`, `stats.yml` | **Generated.** Never edit. |
| `assets/scans/*.jpg` | **Generated** by `make_scan_derivatives.py` from `pages/`. ~229 MB. |
| `_data/timeline.yml` | Hand-maintained — add historical events here. |
| `_data/translations/*.yml` | Hand-maintained — English translations. |
| `_layouts/`, `assets/style.css`, `assets/*.js`, `*.html`, `*.md` | Hand-maintained. |

## Deploying to GitHub Pages

The site lives in `site/`, so point Pages at that directory (Settings → Pages → deploy
from a branch → `/site`), or move `site/*` to the repository root.

Set `baseurl` in `_config.yml` to `"/<repository-name>"` for a project site; leave it
empty for a user site or a custom domain.

**Before making the repository public**, confirm two things:

1. You have the archive's permission to publish the transcript.
2. `.gitignore` is still excluding the Seidel biography — it is copyrighted and must not
   be committed.
