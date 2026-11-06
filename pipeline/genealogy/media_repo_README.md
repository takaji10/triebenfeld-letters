# genealogy-media

Web derivatives of the Zelmer family genealogy media, published for the
genealogy explorer embedded in the [Trąbczyn archive
site](https://takaji10.github.io/triebenfeld-letters/). The originals stay
in the editor's Gramps database; only resized JPEG copies (long edge
2,400 px), 400 px thumbnails and a manifest live here. Media showing
living people, and everything from the excluded branch, is not published.

The files are content-hashed and immutable: a rebuild only ever adds files.
Each publication is tagged (`v2026-11-06`); the site pins one tag, so a
rebuild can never break the live pages.

`manifest.json` maps the database's media paths (the folder layout of the
Gramps tree) to the published files, with dimensions and the focus
rectangles ("regions") the editor drew in Gramps.
