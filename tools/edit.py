#!/usr/bin/env python3
"""
edit.py — One-stop CLI for maintaining the homepage.

Usage:
    python tools/edit.py add-news       # interactive: add a news item
    python tools/edit.py add-pub        # interactive: add a publication
    python tools/edit.py import-bib FILE.bib   # bulk-add publications from BibTeX
    python tools/edit.py new-post       # create a new blog post stub
    python tools/edit.py serve          # run `bundle exec jekyll serve` (preview locally)

The script is dependency-free for everything except `import-bib`, which
prefers `bibtexparser` if installed but falls back to a basic parser.
"""

import argparse
import datetime as dt
import os
import re
import subprocess
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "_data"
POSTS = ROOT / "_posts"


# ---------- helpers ---------------------------------------------------------

def _ask(prompt, default=""):
    suffix = f" [{default}]" if default else ""
    val = input(f"{prompt}{suffix}: ").strip()
    return val or default

def _ask_yn(prompt, default=False):
    suffix = " [Y/n]" if default else " [y/N]"
    val = input(f"{prompt}{suffix}: ").strip().lower()
    if not val:
        return default
    return val.startswith("y")

def _slugify(text):
    s = re.sub(r"[^\w\s-]", "", text.lower())
    s = re.sub(r"[\s_-]+", "-", s).strip("-")
    return s[:80] or "untitled"


# ---------- add-news --------------------------------------------------------

def cmd_add_news(_args):
    today = dt.date.today()
    print("Add a news item — leave blank to keep default.\n")

    display = _ask("Display date", today.strftime("%b %Y"))
    sort_d  = _ask("ISO sort date", today.isoformat())
    text    = _ask("News text (markdown allowed)").strip()
    if not text:
        sys.exit("News text cannot be empty.")
    link    = _ask("Optional link URL", "")

    block = [
        f'- date: "{display}"',
        f'  sort: "{sort_d}"',
        f'  text: "{text.replace(chr(34), chr(92)+chr(34))}"',
    ]
    if link:
        block.append(f'  link: "{link}"')
    block.append("")

    yml = DATA / "news.yml"
    content = yml.read_text(encoding="utf-8")
    # insert above the first existing entry
    m = re.search(r"^- date:", content, flags=re.MULTILINE)
    if m:
        new = content[:m.start()] + "\n".join(block) + "\n" + content[m.start():]
    else:
        new = content.rstrip() + "\n\n" + "\n".join(block) + "\n"
    yml.write_text(new, encoding="utf-8")
    print(f"\nAdded news entry to {yml.relative_to(ROOT)}")


# ---------- add-pub ---------------------------------------------------------

def cmd_add_pub(_args):
    print("Add a publication — leave blank to skip optional fields.\n")
    title = _ask("Title")
    if not title:
        sys.exit("Title is required.")
    authors  = _ask("Authors (wrap your name in <strong>...</strong>)",
                    "<strong>Jie Hu</strong>")
    venue    = _ask("Venue (e.g. ICML)")
    year     = _ask("Year", str(dt.date.today().year))
    location = _ask("Location (optional)", "")
    pdf      = _ask("PDF URL (optional)", "")
    arxiv    = _ask("arXiv URL (optional)", "")
    code     = _ask("Code URL (optional)", "")
    abstract = _ask("Abstract (optional, single paragraph)", "")
    badges   = _ask("Badges? oral / award:Best Paper / spotlight (comma-separated)", "")
    feature  = _ask_yn("Feature on homepage?", default=False)

    lines = [
        f'- title: "{title}"',
        f'  authors: "{authors}"',
        f'  venue: "{venue}"',
        f'  year: {year}',
    ]
    if location: lines.append(f'  location: "{location}"')
    if pdf:      lines.append(f'  pdf: "{pdf}"')
    if arxiv:    lines.append(f'  arxiv: "{arxiv}"')
    if code:     lines.append(f'  code: "{code}"')
    if abstract:
        lines.append(f"  abstract: >")
        for chunk in textwrap.wrap(abstract, 90) or [""]:
            lines.append(f"    {chunk}")
    if badges.strip():
        lines.append("  badges:")
        for b in [x.strip() for x in badges.split(",") if x.strip()]:
            if b.startswith("award:"):
                lines.append(f'    - award: "{b.split(":",1)[1].strip()}"')
            else:
                lines.append(f"    - {b}")
    if feature:
        lines.append("  featured: true")
    lines.append("")

    yml = DATA / "publications.yml"
    content = yml.read_text(encoding="utf-8")
    # insert above the first "- title:" entry
    m = re.search(r"^- title:", content, flags=re.MULTILINE)
    if m:
        new = content[:m.start()] + "\n".join(lines) + "\n" + content[m.start():]
    else:
        new = content.rstrip() + "\n\n" + "\n".join(lines) + "\n"
    yml.write_text(new, encoding="utf-8")
    print(f"\nAdded publication to {yml.relative_to(ROOT)}")


# ---------- import-bib ------------------------------------------------------

def _strip_braces(s):
    s = s.strip()
    while s.startswith(("{", '"')) and s.endswith(("}", '"')):
        s = s[1:-1].strip()
    return s.replace("{", "").replace("}", "").strip()

def _split_authors(raw):
    """Best-effort BibTeX author list -> 'First Last, First Last, <strong>Jie Hu</strong>'.

    Handles both well-formed BibTeX ('A and B and C') and a common malformation
    found in publications.bib where commas separate Last,First pairs and only
    the last 'and' is present, e.g. 'Hu, Jie, Doshi, Vishwaraj and Eun, Do Young'.
    """
    raw = raw.strip()
    # First split on " and "
    chunks = re.split(r"\s+and\s+", raw)
    flattened = []
    for chunk in chunks:
        commas = chunk.count(",")
        # If a chunk has an even number of commas (>=2), it's likely
        # multiple "Last, First" pairs jammed together.
        if commas >= 2 and commas % 2 == 1:  # e.g. "Hu, Jie, Doshi, Vishwaraj" has 3 commas
            tokens = [t.strip() for t in chunk.split(",")]
            # pair consecutive: (Last, First)
            for i in range(0, len(tokens) - 1, 2):
                flattened.append(f"{tokens[i+1]} {tokens[i]}".strip())
        else:
            flattened.append(chunk)

    out = []
    for p in flattened:
        p = p.strip().rstrip(",")
        if not p:
            continue
        if "," in p:
            last, _, first = p.partition(",")
            name = f"{first.strip()} {last.strip()}".strip()
        else:
            name = p
        if name.lower() in ("jie hu", "hu jie"):
            name = "<strong>Jie Hu</strong>"
        out.append(name)
    return ", ".join(out)

def _parse_bibtex(text):
    """Minimal BibTeX parser → list of dicts."""
    entries = []
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,]+),\s*(.*?)\n\}\s*", text, flags=re.DOTALL):
        kind, key, body = m.group(1).lower(), m.group(2).strip(), m.group(3)
        # extract field = value
        fields = {}
        depth, buf, fname = 0, "", None
        i = 0
        while i < len(body):
            c = body[i]
            if fname is None:
                # find "field ="
                fm = re.match(r"\s*(\w+)\s*=\s*", body[i:])
                if not fm: break
                fname = fm.group(1).lower()
                i += fm.end()
                buf = ""
                continue
            buf += c
            if c == "{": depth += 1
            elif c == "}": depth -= 1
            if depth == 0 and (c == "," or i == len(body) - 1):
                fields[fname] = _strip_braces(buf.rstrip(", \n"))
                fname, buf = None, ""
            i += 1
        entries.append({"kind": kind, "key": key, **fields})
    return entries

def cmd_import_bib(args):
    bib_path = Path(args.file)
    if not bib_path.exists():
        sys.exit(f"File not found: {bib_path}")

    try:
        import bibtexparser  # type: ignore
        with open(bib_path, encoding="utf-8") as f:
            db = bibtexparser.load(f)
        entries = db.entries
    except ImportError:
        print("(bibtexparser not installed — using fallback parser. "
              "For better results: pip install bibtexparser)")
        entries = _parse_bibtex(bib_path.read_text(encoding="utf-8"))

    out_lines = []
    for e in entries:
        title  = e.get("title", "").replace("\n", " ").strip()
        authors = _split_authors(e.get("author", ""))
        year   = e.get("year", "").strip()
        venue  = e.get("booktitle") or e.get("journal") or ""
        pdf    = e.get("url") or e.get("paperurl") or ""
        abstract = e.get("abstract", "").replace("\n", " ").strip()

        block = [
            f'- title: "{title}"',
            f'  authors: "{authors}"',
            f'  venue: "{venue}"',
            f'  year: {year}',
        ]
        if pdf: block.append(f'  pdf: "{pdf}"')
        if abstract:
            block.append("  abstract: >")
            for chunk in textwrap.wrap(abstract, 90):
                block.append(f"    {chunk}")
        block.append("")
        out_lines.append("\n".join(block))

    print(f"Parsed {len(entries)} BibTeX entries.")
    out_path = ROOT / "_data" / "publications.imported.yml"
    out_path.write_text("\n".join(out_lines), encoding="utf-8")
    print(f"Wrote preview to {out_path.relative_to(ROOT)}")
    print("Review it, then copy/paste the entries you want into _data/publications.yml.")


# ---------- new-post --------------------------------------------------------

def cmd_new_post(_args):
    title = _ask("Post title")
    if not title:
        sys.exit("Title required.")
    desc  = _ask("One-sentence description", "")
    tags  = _ask("Tags (comma-separated)", "research, notes")
    math  = _ask_yn("Will the post contain LaTeX math?", default=True)
    today = dt.date.today()
    slug  = _slugify(title)
    fname = POSTS / f"{today.isoformat()}-{slug}.md"
    if fname.exists():
        sys.exit(f"{fname} already exists.")
    body = f"""---
layout: post
title: "{title}"
date: {today.isoformat()}
description: "{desc}"
tags: [{', '.join(t.strip() for t in tags.split(',') if t.strip())}]
math: {'true' if math else 'false'}
---

Write your post here. Math works inline like $E = mc^2$ and as display:

$$\\int_0^\\infty e^{{-x^2}} dx = \\frac{{\\sqrt{{\\pi}}}}{{2}}$$

Use `## Heading 2`, `### Heading 3`, normal markdown lists, code fences, etc.
"""
    POSTS.mkdir(exist_ok=True)
    fname.write_text(body, encoding="utf-8")
    print(f"Created {fname.relative_to(ROOT)}")
    print("Open it in your editor and start writing.")


# ---------- serve -----------------------------------------------------------

def cmd_serve(_args):
    print("Starting local Jekyll server. Press Ctrl-C to stop.")
    try:
        subprocess.run(["bundle", "exec", "jekyll", "serve", "--livereload"], cwd=ROOT)
    except FileNotFoundError:
        sys.exit("Bundler not installed. See README.md → 'Running Locally'.")


# ---------- main ------------------------------------------------------------

def main():
    p = argparse.ArgumentParser(prog="edit.py", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("add-news",  help="Interactively add a news item")
    sub.add_parser("add-pub",   help="Interactively add a publication")
    ip = sub.add_parser("import-bib", help="Bulk-import publications from a .bib file")
    ip.add_argument("file", help="Path to .bib file")
    sub.add_parser("new-post",  help="Create a new blog post stub")
    sub.add_parser("serve",     help="Run jekyll serve locally")
    args = p.parse_args()

    {
        "add-news":   cmd_add_news,
        "add-pub":    cmd_add_pub,
        "import-bib": cmd_import_bib,
        "new-post":   cmd_new_post,
        "serve":      cmd_serve,
    }[args.cmd](args)


if __name__ == "__main__":
    main()
