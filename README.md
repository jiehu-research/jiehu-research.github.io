# Jie Hu - Academic Homepage

Source for [https://jiehu-research.github.io](https://jiehu-research.github.io).
Built with Jekyll, deployed on GitHub Pages.

> **Looking for the maintainer guide?** See [MAINTAINER.md](MAINTAINER.md) for
> the full how-to (editing content, git workflow, troubleshooting).

---

## Three ways to edit

### 1. Easiest -- edit on GitHub directly

Every section on the live site has a small `edit` link next to its header.
Click it to open the underlying YAML / Markdown file in GitHub's web editor,
make changes, and click "Commit changes". The site rebuilds in about 1 minute.

No local installation, no command line, nothing.

### 2. Fast -- ask Claude

Most updates are one-liners:

- *"Add a news item: paper accepted at NeurIPS 2026."*
- *"Add this publication: <paste BibTeX>"*
- *"Update the recruiting blurb to say Fall 2026."*
- *"Convert this LaTeX file to a blog post"*  (attach the .tex file)
- *"Pull the latest from GitHub"* / *"Push my changes."*

Claude reads from this folder, runs the helper scripts, and handles git for you.

### 3. Manual -- run the helper scripts

```bash
python tools/edit.py add-news                         # interactive prompt
python tools/edit.py add-pub                          # interactive prompt
python tools/edit.py import-bib assets/files/publications.bib
python tools/edit.py new-post                         # new blog post stub
python tools/latex_to_post.py paper.tex               # LaTeX -> blog post
python tools/edit.py serve                            # local preview
```

All scripts are pure-Python with no required dependencies.

---

## File map

```
_config.yml          - your name, links, recruiting blurb        EDIT
_data/news.yml       - news items                                EDIT
_data/publications.yml - publications, with abstracts/PDFs       EDIT
_data/teaching.yml   - courses (homepage only)                   EDIT
_posts/              - blog posts                                EDIT
assets/images/profile.png   - your photo                         REPLACE
assets/files/cv.pdf  - your CV                                   REPLACE
assets/files/publications.bib - bibtex of all your papers        REPLACE
index.md             - homepage layout (rarely needs editing)
publications/, blog/, news/  - sub-page layouts
_includes/, _layouts/  - shared template fragments
assets/css/main.css  - all styling, light + dark mode
tools/               - helper scripts (edit.py, latex_to_post.py)
```

---

## Local preview (optional)

```powershell
# one-time setup -- install Ruby and Bundler from
# https://jekyllrb.com/docs/installation/windows/
bundle install

# every time you want to preview
bundle exec jekyll serve --livereload
# open http://localhost:4000
```

You don't need this if you're only making content edits -- GitHub Pages
will rebuild and publish automatically.
