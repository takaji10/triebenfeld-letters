# Hosting this edition on GitHub Pages

Everything in this file has been prepared and tested locally. What remains needs
your GitHub account, and is listed under "What you have to do" below.

## What the repository contains

1,547 files, 241 MB. The Jekyll site in `site/` is the whole of it, bar four
files: `letters.json`, `verify_site.py`, this file and the README.

Of the 241 MB, 229 MB is the 872 page images in `site/assets/scans/`. Everything
else together is about 12 MB, so the repository is essentially the scans plus a
rounding error.

`letters.json` and `verify_site.py` are kept because they are what makes the
deploy gate possible: the workflow uses them to prove the published text is
character-identical to the corpus. Dropping them would not break the site, only
the guarantee about it.

Deliberately not committed, enforced by root-anchored rules in `.gitignore` so
they cannot reach into `site/`:

| Excluded | Why |
|---|---|
| `pages/` | 1.08 GB of archival masters. The site serves the 229 MB derivatives instead. |
| `.anthropic_key` | API credential. |
| `Friedrich Ludwig ... (2018, Seidel) (German).md` | Copyrighted book text, a research reference only. |
| The pipeline: ~40 scripts, the corpus `.txt` files, review sheets, notes | Not needed to build or serve the site, which links to nothing outside `site/`. |
| `translation-raw/`, `summaries-raw/`, `summaries-raw-de/`, and three more | Model output caches, 965 files. |
| `site/_site/` | Build output, rebuilt by the workflow on every push. |
| `*.bak*` | Working backups of the corpus. |

All of it stays on the working machine. Only the repository is narrowed.

The `*.bak*` rule was widened from `*.bak[0-9]`, which matched a single digit and
would have committed `.bak10` through `.bak16` and `.bak_review`.

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
