# The Triebenfeld Letters

A digital edition of 318 documents from the correspondence of Peter Friedrich von
Triebenfeld, estate agent, and Friedrich Ludwig, Fürst zu Hohenlohe-Ingelfingen,
covering 1798 to 1816: the attempt to save an indebted Silesian and South Prussian
estate complex through the Napoleonic wars, the Congress of Vienna, and the
redrawing of Poland.

869 manuscript pages, transcribed from Kurrent. Each letter is presented four
ways: the page scan, a diplomatic transcription that preserves the manuscript
line for line, a reading text with abbreviations resolved, and an English
translation that marks its own uncertainty rather than smoothing it away. The
site is bilingual, English and German.

## Repository layout

```
site/            the Jekyll site - the entire published edition
  _letters/      318 letter pages with YAML front matter
  _data/         summaries, translations, people, places, timeline, i18n
  assets/scans/  872 page images
letters.json     the canonical database the site is generated from
verify_site.py   checks the built site against it
```

The research apparatus that produced the edition - the corpus text, review
sheets, model output caches, and the forty-odd scripts of the build and
translation pipeline - is kept out of this repository. See `.gitignore`. The
site does not depend on any of it: it links to nothing outside `site/`.

The archival page masters (1.08 GB) are also kept out; `site/assets/scans/`
holds downscaled copies.

## Building locally

```
cd site
bundle install
bundle exec jekyll serve
```

Then `python verify_site.py` from the repository root.

## Verification

The edition's central claim is that its diplomatic transcription reproduces the
manuscript line for line, and that nothing in the pipeline has silently altered
it. `verify_site.py` checks the built HTML against `letters.json` and fails if
any document is missing, if any transcription differs by a single character, if
an internal link does not resolve, or if a page fetches anything from an external
host. It runs on every deploy, and a failure blocks publication rather than
warning about it.

## Editorial method

The translation is a reading copy, not a critical text. Where the German is
damaged or ambiguous the English says so in line - `[illegible]`,
`[uncertain: word]`, `[text lost]` - rather than guessing fluently, because a
translation reads as confident whether or not it has grounds to be. Names,
numbers and dates are carried across unchanged and checked mechanically.

Any close scholarly use should go back to the scans. The point of the reading
copy is to make that unnecessary for everything else.

## Licence

Not yet determined. Until a `LICENSE` file is added, no reuse rights are granted.
The transcriptions and translations, and the page images, may end up under
different terms.

## Deployment

See [DEPLOY.md](DEPLOY.md).
