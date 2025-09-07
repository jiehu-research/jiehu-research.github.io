#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBDIR = ROOT / '_publications'

def strip_strong(s: str) -> str:
    return s.replace('<strong>', '').replace('</strong>', '')

def build_authors_from_citation(citation: str) -> str:
    # authors appear before first '. ('
    head = citation.split('. (', 1)[0].strip()
    # Remove trailing period if present
    if head.endswith('.'):
        head = head[:-1]
    # Split by comma+space and pair as (Last, First)
    tokens = [t.strip() for t in head.split(',')]
    tokens = [t for t in tokens if t != '']
    pairs = []
    i = 0
    while i + 1 < len(tokens):
        last = tokens[i]
        first = tokens[i + 1]
        # if first looks like a year (numeric 4), break (robustness)
        if re.fullmatch(r'\d{4}', first):
            break
        # If there are embedded strong tags split across last/first, strip and rewrap
        last_clean = strip_strong(last)
        first_clean = strip_strong(first)
        name = f"{first_clean} {last_clean}".strip()
        if 'strong' in (last + first):
            name = f"<strong>{name}</strong>"
        pairs.append(name)
        i += 2
    # If odd tokens remain, append as-is
    if i < len(tokens):
        leftover = strip_strong(tokens[i]).strip()
        if leftover:
            pairs.append(leftover)
    return ', '.join(pairs)

def process_file(p: Path):
    s = p.read_text(encoding='utf-8')
    if not s.startswith('---'):
        return False
    parts = s.split('\n---\n', 1)
    if len(parts) != 2:
        return False
    fm = parts[0][3:]  # drop leading '---'
    body = parts[1]
    lines = fm.splitlines()
    citation_line_idx = next((i for i,l in enumerate(lines) if l.strip().startswith('citation:')), None)
    if citation_line_idx is None:
        return False
    # Extract citation value (single-line expected)
    m = re.match(r"citation:\s*'?\"?(.*)\"?'?\s*$", lines[citation_line_idx])
    if not m:
        return False
    citation = m.group(1)
    authors_pretty = build_authors_from_citation(citation)
    # Find authors line
    authors_idx = next((i for i,l in enumerate(lines) if l.strip().startswith('authors:')), None)
    authors_line = f"authors: '{authors_pretty}'"
    if authors_idx is not None:
        lines[authors_idx] = authors_line
    else:
        # insert after title line if present, else at top
        title_idx = next((i for i,l in enumerate(lines) if l.strip().startswith('title:')), 0)
        insert_at = min(title_idx + 1, len(lines))
        lines.insert(insert_at, authors_line)
    new_fm = '\n'.join(lines)
    p.write_text('---\n' + new_fm + '\n---\n' + body, encoding='utf-8')
    return True

def main():
    changed = 0
    for p in sorted(PUBDIR.glob('*.md')):
        if process_file(p):
            print('Updated authors in', p)
            changed += 1
    print('Done. Files updated:', changed)

if __name__ == '__main__':
    main()

