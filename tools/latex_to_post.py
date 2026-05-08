#!/usr/bin/env python3
"""
latex_to_post.py — Convert a LaTeX file to a Jekyll blog post
=============================================================

Usage:
    python tools/latex_to_post.py  path/to/paper.tex
    python tools/latex_to_post.py  path/to/paper.tex  --title "My Post Title"
    python tools/latex_to_post.py  path/to/paper.tex  --date 2026-01-15
    python tools/latex_to_post.py  path/to/paper.tex  --tags "MCMC, optimization"
    python tools/latex_to_post.py  path/to/paper.tex  --output _posts/

Requirements:
    Option A (recommended): Install pandoc  →  https://pandoc.org/installing.html
    Option B (fallback):    Pure Python regex-based conversion (handles most cases)

The script:
  1. Extracts title / authors / abstract from the .tex file
  2. Converts the body to Markdown (via pandoc or built-in regex)
  3. Preserves $...$ and $$...$$ math (rendered by MathJax on the site)
  4. Writes a ready-to-publish _posts/YYYY-MM-DD-slug.md file
"""

import argparse
import datetime
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path


# ─────────────────────────────────────────────────────────────
#  LaTeX metadata extraction
# ─────────────────────────────────────────────────────────────

def extract_command(tex: str, cmd: str) -> str:
    """Extract the first argument of a LaTeX command like \\title{...}."""
    pattern = rf"\\{cmd}\s*\{{((?:[^{{}}]|\{{[^{{}}]*\}})*)\}}"
    m = re.search(pattern, tex, re.DOTALL)
    if not m:
        return ""
    # Strip nested LaTeX commands for plain text
    val = m.group(1).strip()
    val = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", val)   # \cmd{arg} → arg
    val = re.sub(r"\\[a-zA-Z]+",            "",  val)       # bare \cmd → ""
    val = re.sub(r"\s+",                    " ", val)
    return val.strip()


def extract_abstract(tex: str) -> str:
    """Extract the abstract environment."""
    m = re.search(
        r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex, re.DOTALL
    )
    if not m:
        return ""
    abstract = m.group(1).strip()
    # Clean up common LaTeX commands
    abstract = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", abstract)
    abstract = re.sub(r"\\[a-zA-Z]+", "", abstract)
    abstract = re.sub(r"\s+", " ", abstract)
    return abstract.strip()


def extract_body(tex: str) -> str:
    """Extract content between \\begin{document} and \\end{document},
    removing the abstract and preamble commands."""
    m = re.search(
        r"\\begin\{document\}(.*?)\\end\{document\}", tex, re.DOTALL
    )
    body = m.group(1) if m else tex

    # Remove maketitle, abstract env, bibliography
    body = re.sub(r"\\maketitle", "", body)
    body = re.sub(r"\\begin\{abstract\}.*?\\end\{abstract\}", "", body, flags=re.DOTALL)
    body = re.sub(r"\\bibliography\{[^}]*\}", "", body)
    body = re.sub(r"\\bibliographystyle\{[^}]*\}", "", body)
    return body.strip()


# ─────────────────────────────────────────────────────────────
#  Conversion: pandoc (preferred) or regex fallback
# ─────────────────────────────────────────────────────────────

def has_pandoc() -> bool:
    return shutil.which("pandoc") is not None


def convert_with_pandoc(tex_body: str, tex_path: Path) -> str:
    """Write body to a temp .tex file and run pandoc → markdown."""
    # Wrap body in minimal preamble so pandoc can parse it
    minimal_tex = textwrap.dedent(r"""
        \documentclass{article}
        \usepackage{amsmath,amssymb,amsthm}
        \begin{document}
    """) + tex_body + "\n\\end{document}\n"

    with tempfile.NamedTemporaryFile(suffix=".tex", mode="w",
                                     delete=False, encoding="utf-8") as f:
        f.write(minimal_tex)
        tmp_path = f.name

    try:
        result = subprocess.run(
            [
                "pandoc", tmp_path,
                "--from=latex",
                "--to=markdown",
                "--wrap=none",
                "--atx-headers",
            ],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0:
            print(f"[pandoc warning] {result.stderr[:300]}", file=sys.stderr)
        md = result.stdout
    finally:
        os.unlink(tmp_path)

    return md


def convert_with_regex(tex_body: str) -> str:
    """Basic regex-based LaTeX → Markdown conversion (no pandoc needed)."""
    md = tex_body

    # Sections
    md = re.sub(r"\\section\*?\{([^}]+)\}",      r"\n## \1\n",     md)
    md = re.sub(r"\\subsection\*?\{([^}]+)\}",   r"\n### \1\n",    md)
    md = re.sub(r"\\subsubsection\*?\{([^}]+)\}",r"\n#### \1\n",   md)

    # Text formatting
    md = re.sub(r"\\textbf\{([^}]+)\}",  r"**\1**", md)
    md = re.sub(r"\\textit\{([^}]+)\}",  r"*\1*",   md)
    md = re.sub(r"\\emph\{([^}]+)\}",    r"*\1*",   md)
    md = re.sub(r"\\texttt\{([^}]+)\}",  r"`\1`",   md)
    md = re.sub(r"\\text\{([^}]+)\}",    r"\1",     md)

    # Itemize / enumerate
    md = re.sub(r"\\begin\{itemize\}",   "",   md)
    md = re.sub(r"\\end\{itemize\}",     "\n", md)
    md = re.sub(r"\\begin\{enumerate\}", "",   md)
    md = re.sub(r"\\end\{enumerate\}",   "\n", md)
    md = re.sub(r"\\item\s*",            "- ", md)

    # Theorem-like environments
    for env in ["theorem", "lemma", "proposition", "corollary",
                "definition", "remark", "example", "proof"]:
        label = env.capitalize()
        md = re.sub(rf"\\begin\{{{env}\}}(\[[^\]]*\])?",
                    lambda m, l=label: f"\n**{l}{'(' + m.group(1)[1:-1] + ')' if m.group(1) else ''}.**\n",
                    md)
        md = re.sub(rf"\\end\{{{env}\}}", "\n", md)

    # Equation environments — wrap in $$...$$
    for env in ["equation", "align", "gather", "multline", "eqnarray"]:
        md = re.sub(rf"\\begin\{{{env}\*?\}}", r"\n$$\n", md)
        md = re.sub(rf"\\end\{{{env}\*?\}}",   r"\n$$\n", md)

    # Other environments to just unwrap
    md = re.sub(r"\\begin\{[a-z*]+\}(\[[^\]]*\])?", "", md)
    md = re.sub(r"\\end\{[a-z*]+\}",                "", md)

    # Footnotes
    md = re.sub(r"\\footnote\{([^}]+)\}", r" (\1)", md)

    # Href / url
    md = re.sub(r"\\href\{([^}]+)\}\{([^}]+)\}", r"[\2](\1)", md)
    md = re.sub(r"\\url\{([^}]+)\}",              r"<\1>",     md)

    # Citations — just keep the key for now
    md = re.sub(r"\\cite[tp]?\{([^}]+)\}", r"[\1]", md)
    md = re.sub(r"\\ref\{([^}]+)\}",       r"[ref]", md)
    md = re.sub(r"\\label\{([^}]+)\}",     "",       md)

    # Quotes
    md = md.replace("``", "“").replace("''", "”")
    md = md.replace("`",  "‘").replace("'",  "’")

    # Dashes
    md = md.replace("---", "—")
    md = md.replace("--",  "–")

    # Tilde (non-breaking space in LaTeX)
    md = re.sub(r"(?<!\\)~", " ", md)

    # Remove remaining single-arg commands that are safe to strip
    md = re.sub(r"\\(?:noindent|newline|linebreak|pagebreak|clearpage|hspace|vspace)\b\*?(?:\{[^}]*\})?", "", md)

    # Remove remaining \cmd{} wrappers we don't know about
    md = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", md)

    # Remove leftover bare commands
    md = re.sub(r"\\[a-zA-Z]+\b\*?", "", md)

    # Clean up whitespace
    md = re.sub(r"\n{3,}", "\n\n", md)

    return md.strip()


# ─────────────────────────────────────────────────────────────
#  Jekyll front matter & output
# ─────────────────────────────────────────────────────────────

def slugify(title: str) -> str:
    slug = title.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = slug.strip("-")
    return slug[:60]


def build_post(title: str, date_str: str, description: str,
               tags: list[str], body_md: str) -> str:
    tag_yml = "[" + ", ".join(tags) + "]" if tags else "[]"
    front = textwrap.dedent(f"""\
        ---
        layout: post
        title: "{title}"
        date: {date_str}
        description: "{description}"
        tags: {tag_yml}
        math: true
        ---
    """)
    return front + "\n" + body_md + "\n"


# ─────────────────────────────────────────────────────────────
#  Main
# ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Convert a LaTeX file to a Jekyll blog post."
    )
    parser.add_argument("tex_file",    help="Path to the .tex file")
    parser.add_argument("--title",     help="Override post title (default: extracted from \\title{})")
    parser.add_argument("--date",      help="Post date YYYY-MM-DD (default: today)")
    parser.add_argument("--tags",      help="Comma-separated tags, e.g. 'MCMC, optimization'")
    parser.add_argument("--output",    default="_posts",
                        help="Output directory (default: _posts)")
    parser.add_argument("--no-pandoc", action="store_true",
                        help="Force regex-based conversion even if pandoc is available")
    args = parser.parse_args()

    tex_path = Path(args.tex_file)
    if not tex_path.exists():
        sys.exit(f"Error: file not found: {tex_path}")

    tex = tex_path.read_text(encoding="utf-8", errors="replace")

    # ── Extract metadata ──
    title       = args.title or extract_command(tex, "title") or tex_path.stem
    abstract    = extract_abstract(tex)
    date_str    = args.date or datetime.date.today().isoformat()
    tags        = [t.strip() for t in args.tags.split(",")] if args.tags else []
    description = abstract[:200].rstrip() + ("…" if len(abstract) > 200 else "") if abstract else ""

    print(f"  Title    : {title}")
    print(f"  Date     : {date_str}")
    print(f"  Tags     : {tags or '(none)'}")
    print(f"  Abstract : {description[:80]}..." if description else "  Abstract : (none found)")

    # ── Convert body ──
    body_tex = extract_body(tex)

    if not args.no_pandoc and has_pandoc():
        print("  Converter: pandoc")
        body_md = convert_with_pandoc(body_tex, tex_path)
    else:
        if not args.no_pandoc:
            print("  Converter: regex (pandoc not found — install it for better results)")
        else:
            print("  Converter: regex (--no-pandoc flag set)")
        body_md = convert_with_regex(body_tex)

    # ── Optionally prepend abstract as a callout ──
    if abstract:
        body_md = f"> **Abstract.** {description}\n{{: .abstract-callout}}\n\n" + body_md

    # ── Write output ──
    out_dir  = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    slug     = slugify(title)
    filename = f"{date_str}-{slug}.md"
    out_path = out_dir / filename

    post_content = build_post(title, date_str, description, tags, body_md)
    out_path.write_text(post_content, encoding="utf-8")

    print(f"\n✅  Post written to: {out_path}")
    print(f"   Preview at: http://localhost:4000/blog/{date_str.replace('-','/')}/{slug}/")
    print("\nNext steps:")
    print("  1. Review the file and clean up any leftover LaTeX artifacts")
    print("  2. Add the file to your GitHub repo (git add, commit, push)")
    print("  3. The post will appear on your blog automatically")


if __name__ == "__main__":
    main()
