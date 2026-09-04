# Hosting this edition on GitHub Pages

Everything in this file has been prepared and tested locally. What remains needs
your GitHub account, and is listed under "What you have to do" below.

## What the repository contains

About 1935 files. Most of the bytes are the 872 page images in
`site/assets/scans/` (229 MB); everything else together is roughly 20 MB.

The repository now has to be able to rebuild the site from scratch, not merely
serve it, so it carries the whole chain:

| | |
|---|---|
| `units/<slug>/` | each holding's transcription, rulings and provenance |
| `pipeline/` | intake, build, translation and review scripts |
| `reference/` | glossary, name rulings, place canon, shared across units |
| `corpus/` | the merged, generated database |
| `site/` | the Jekyll site and the scan derivatives |
| `regenerate.py`, `verify_site.py`, `unitlib.py`, `new_unit.py` | entry points |

`corpus/letters.json` and `verify_site.py` are what make the deploy gate
possible: the workflow uses them to prove the published text is
character-identical to the transcription.

Deliberately not committed:

| Excluded | Why |
|---|---|
| `pages/` | 1.08 GB of archival masters. The site serves the 229 MB derivatives instead. |
| `cache/` | Model output, about $29 of API spend, re-derivable by paying again. |
| `review/` | Generated review sheets. What they lead to is recorded in `units/<slug>/rulings.yml` and `reference/`, which are tracked. |
| `.anthropic_key` | API credential. |
| `Friedrich Ludwig ... (2018, Seidel) (German).md` | Copyrighted book text, a research reference only. |
| `site/_site/` | Build output, rebuilt by the workflow on every push. |

Raw scans live outside the project entirely; `units/<slug>/unit.yml` records
where.

## How deployment works

`.github/workflows/pages.yml` builds on every push to `main`. GitHub's built-in
Pages builder only reads a Jekyll site from the repository root or `/docs`, and
this one lives in `site/`, so the build is explicit.

The workflow runs `verify_site.py` against the built HTML **before** deploying, so
a build whose diplomatic text has drifted from the corpus, or whose links no
longer resolve, fails instead of publishing.

`base_path` comes from `actions/configure-pages`, so one workflow serves both
layouts without editing `_config.yml`:

- **User site** - repository named `<your-username>.github.io`, published at
  `https://<your-username>.github.io/`. Base path is empty.
- **Project site** - any other repository name, e.g. `vonTriebenfeld`, published at
  `https://<your-username>.github.io/vonTriebenfeld/`. Base path is `/vonTriebenfeld`.

Both were tested locally: a `--baseurl "/vonTriebenfeld"` build passes all 12,385
internal links. No template hardcodes an absolute path; everything uses
`relative_url`.

`site/Gemfile.lock` now lists `x86_64-linux` alongside `x64-mingw-ucrt`. Without
that, `bundle install` on the Ubuntu runner fails outright.

## What you have to do

1. Create an empty repository on GitHub. Do not initialise it with a README,
   `.gitignore` or licence, as the local repository already has commits.
2. Authenticate this machine, once. Either install the GitHub CLI and run
   `gh auth login`, or push over HTTPS and let Git Credential Manager open a
   browser window on the first push.
3. Add the remote and push:

   ```
   git remote add origin https://github.com/<username>/<repo>.git
   git push -u origin main
   ```

4. In the repository, open **Settings -> Pages** and set **Source** to
   **GitHub Actions**. Nothing deploys until this is set. With the GitHub CLI
   authenticated you can do it without the browser:

   ```
   gh api -X POST repos/<username>/<repo>/pages -f build_type=workflow
   ```
5. Watch the run under the **Actions** tab. The first one takes a few minutes,
   mostly installing gems; later runs reuse the bundler cache.

## Things worth deciding before you push

- **Scope.** The repository publishes the full working apparatus, including the
  review sheets (`translation_review.csv` and others) and the research notes.
  That suits a project whose argument is that its methods are inspectable, but it
  is a choice, and narrowing it later means rewriting history rather than adding
  a commit.
- **Licence.** There is no `LICENSE` file. Without one, the default is exclusive
  copyright: readers may view the site but have no right to reuse the text.
  Editions of this kind usually carry different terms for the transcription and
  translation than for the scans.
- **Scan rights.** The 872 images are reproduced from an archive. Confirm you
  hold the right to publish them before the repository goes public.
