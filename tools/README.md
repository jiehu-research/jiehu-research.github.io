# tools/

Helper scripts for maintaining the homepage.

## Quick reference

| Command                                              | What it does                                                   |
|------------------------------------------------------|----------------------------------------------------------------|
| `python tools/edit.py add-news`                      | Interactive prompt to add a news item                          |
| `python tools/edit.py add-pub`                       | Interactive prompt to add a publication                        |
| `python tools/edit.py import-bib FILE.bib`           | Bulk-import publications from a BibTeX file (preview only)     |
| `python tools/edit.py new-post`                      | Create a `_posts/YYYY-MM-DD-slug.md` stub                      |
| `python tools/edit.py serve`                         | Run `bundle exec jekyll serve --livereload` for local preview  |
| `python tools/latex_to_post.py paper.tex`            | Convert a LaTeX file into a Markdown blog post                 |

All scripts are pure-Python with no required dependencies.
The BibTeX importer **prefers** `bibtexparser` if installed (`pip install bibtexparser`)
but falls back to a built-in parser. The LaTeX converter **prefers** `pandoc` if
installed but falls back to a regex-based converter.

## Editing without the command line

You don't have to run any scripts. Every page on the live site has a small
✎ **edit** link next to its section header. Clicking it opens the underlying
YAML or Markdown file in GitHub's web editor — make changes there, click
"Commit changes", and the site rebuilds automatically in about a minute.

## Asking Claude

Most of the time, just describe the change in plain English:

- "Add a news item: paper accepted at NeurIPS 2026"
- "Add this publication: [paste BibTeX]"
- "Update the recruiting blurb to say Fall 2026"
- "Convert this LaTeX file to a blog post"  (attach the .tex file)
- "Pull the latest from GitHub" / "Push my changes"

Claude has read access to this folder and can run the helper scripts directly.
