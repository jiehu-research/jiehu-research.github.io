#!/usr/bin/env python3
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / 'files' / 'publications.bib'
OUTDIR = ROOT / '_publications'

def read_bib() -> str:
    return BIB.read_text(encoding='utf-8')

def iter_entries(bib_text: str):
    # Split by top-level @ occurrences
    # Keep braces balanced to capture full entries
    i = 0
    n = len(bib_text)
    while i < n:
        at = bib_text.find('@', i)
        if at == -1:
            break
        # find opening brace
        brace = bib_text.find('{', at)
        if brace == -1:
            break
        # walk to matching closing brace for the entry
        depth = 1
        j = brace + 1
        while j < n and depth > 0:
            if bib_text[j] == '{':
                depth += 1
            elif bib_text[j] == '}':
                depth -= 1
            j += 1
        entry_text = bib_text[at:j]
        i = j
        yield entry_text

def parse_entry(entry_text: str):
    m = re.match(r'@(?P<etype>\w+)\s*\{\s*(?P<key>[^,]+),', entry_text, re.S)
    if not m:
        return None
    etype = m.group('etype').strip().lower()
    key = m.group('key').strip()
    body = entry_text[m.end():].strip()
    # drop trailing }
    if body.endswith('}'): body = body[:-1]
    fields = {}
    k = 0
    while k < len(body):
        # skip whitespace and commas
        while k < len(body) and body[k] in ' \t\r\n,':
            k += 1
        if k >= len(body): break
        # read field name
        start = k
        while k < len(body) and re.match(r'[A-Za-z0-9_]', body[k]):
            k += 1
        name = body[start:k].strip().lower()
        # skip spaces and equals
        while k < len(body) and body[k] in ' \t\r\n=':
            k += 1
        if k >= len(body): break
        # value delimited by { } or " "
        if body[k] == '{':
            depth = 1
            k += 1
            val_start = k
            while k < len(body) and depth > 0:
                if body[k] == '{': depth += 1
                elif body[k] == '}': depth -= 1
                k += 1
            value = body[val_start:k-1]
        elif body[k] == '"':
            k += 1
            val_start = k
            while k < len(body) and body[k] != '"':
                k += 1
            value = body[val_start:k]
            k += 1
        else:
            # bare value until comma
            val_start = k
            while k < len(body) and body[k] != ',':
                k += 1
            value = body[val_start:k]
        fields[name] = value.strip()
        # move to next comma if present
        while k < len(body) and body[k] not in ',':
            k += 1
        if k < len(body) and body[k] == ',':
            k += 1
    return {
        'type': etype,
        'key': key,
        'fields': fields,
    }

def html_escape(s: str) -> str:
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def sanitize_slug(s: str) -> str:
    s = s.lower()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'\s+', '-', s).strip('-')
    return s[:80]

def bold_name_in_authors(authors: str) -> str:
    # Bold both "Jie Hu" and "Hu, Jie"
    return (authors
            .replace('Jie Hu', '<strong>Jie Hu</strong>')
            .replace('Hu, Jie', '<strong>Hu, Jie</strong>'))

def authors_for_citation(fields: dict) -> str:
    authors = fields.get('author', '').strip()
    # Normalize BibTeX author list to a readable string
    authors = re.sub(r'\s+and\s+', ', ', authors)
    authors = bold_name_in_authors(authors)
    return authors

def venue_and_category(fields: dict, etype: str):
    venue = fields.get('booktitle') or fields.get('journal') or ''
    category = 'conferences' if (fields.get('booktitle') or etype in ('inproceedings','conference')) else 'manuscripts'
    return venue, category

def build_citation(fields: dict, etype: str) -> str:
    authors = authors_for_citation(fields)
    title = html_escape(fields.get('title',''))
    year = fields.get('year', '')
    venue, _ = venue_and_category(fields, etype)
    parts = []
    if authors: parts.append(f"{authors}.")
    if year: parts.append(f"({year}).")
    if title:
        parts.append(f"&quot;{title}&quot;.")
    if venue:
        parts.append(f"<i>{html_escape(venue)}</i>.")
    return ' '.join(parts)

def extract_highlights(fields: dict):
    note = (fields.get('note','') + ' ' + fields.get('remarks','')).strip()
    award = None
    presentation = None
    low = note.lower()
    if 'outstanding' in low or 'best paper' in low:
        award = 'Outstanding Paper Award'
    if 'oral' in low:
        presentation = 'Oral presentation'
    return award, presentation

def write_pub(entry):
    etype = entry['type']
    f = entry['fields']
    title = f.get('title','').strip()
    year = f.get('year','').strip() or '1900'
    date = f"{year}-01-01"
    venue, category = venue_and_category(f, etype)
    url = f.get('url','').strip()
    abstract = f.get('abstract','').strip()
    citation = build_citation(f, etype)
    award, presentation = extract_highlights(f)
    slug = sanitize_slug(title)
    permalink = f"/publication/{year}-{slug}"
    # File name with year-month-day to keep order
    filename = f"{year}-01-01-{slug or 'paper'}.md"
    p = OUTDIR / filename
    yml = [
        '---',
        f'title: "{title}"',
        'collection: publications',
        f'category: {category}',
        f'permalink: {permalink}',
        f'date: {date}',
        f'venue: "{venue}"',
    ]
    if url:
        yml.append(f'paperurl: "{url}"')
    if abstract:
        # store in front matter so list can use collapsible abstract
        yml.append('abstract: >-')
        # indent abstract lines for YAML block scalar
        for line in abstract.splitlines():
            yml.append(f'  {line}')
    if award:
        yml.append(f'award: "{award}"')
    if presentation:
        yml.append(f'presentation: "{presentation}"')
    if citation:
        yml.append(f'citation: \'{citation}\'')
    yml.append('---')
    yml.append('')
    p.write_text("\n".join(yml), encoding='utf-8')
    return p

def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    text = read_bib()
    count = 0
    for raw in iter_entries(text):
        entry = parse_entry(raw)
        if not entry: continue
        p = write_pub(entry)
        count += 1
        print(f"Wrote {p.relative_to(ROOT)}")
    print(f"Imported {count} publications")

if __name__ == '__main__':
    main()

