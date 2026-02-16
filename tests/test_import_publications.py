import sys
from pathlib import Path

# Add scripts directory to sys.path
scripts_dir = str(Path(__file__).resolve().parents[1] / 'scripts')
if scripts_dir not in sys.path:
    sys.path.append(scripts_dir)

from import_publications import parse_entry, sanitize_slug, html_escape, extract_highlights

def test_parse_entry_basic():
    bibtex = """@article{key1,
  title = {Title One},
  author = {Author One},
  year = {2023}
}"""
    entry = parse_entry(bibtex)
    assert entry is not None
    assert entry['type'] == 'article'
    assert entry['key'] == 'key1'
    assert entry['fields']['title'] == 'Title One'
    assert entry['fields']['author'] == 'Author One'
    assert entry['fields']['year'] == '2023'

def test_parse_entry_quotes():
    bibtex = """@inproceedings{key2,
  title = "Title Two",
  author = "Author Two",
  year = "2022"
}"""
    entry = parse_entry(bibtex)
    assert entry is not None
    assert entry['type'] == 'inproceedings'
    assert entry['key'] == 'key2'
    assert entry['fields']['title'] == 'Title Two'
    assert entry['fields']['author'] == 'Author Two'
    assert entry['fields']['year'] == '2022'

def test_parse_entry_bare_values():
    bibtex = """@misc{key3,
  title = {Title Three},
  year = 2021,
  note = something
}"""
    entry = parse_entry(bibtex)
    assert entry is not None
    assert entry['fields']['title'] == 'Title Three'
    assert entry['fields']['year'] == '2021'
    assert entry['fields']['note'] == 'something'

def test_parse_entry_nested_braces():
    bibtex = """@article{key4,
  title = {Title with {Nested} Braces},
  author = {Jie Hu}
}"""
    entry = parse_entry(bibtex)
    assert entry is not None
    assert entry['fields']['title'] == 'Title with {Nested} Braces'

def test_parse_entry_multiline():
    bibtex = """@article{key5,
  abstract = {This is a
long abstract.}
}"""
    entry = parse_entry(bibtex)
    assert entry is not None
    assert entry['fields']['abstract'] == 'This is a\nlong abstract.'

def test_parse_entry_various_whitespace():
    bibtex = """@article { key6 ,
  title={Spaceless},
  year = 2020 ,
}"""
    entry = parse_entry(bibtex)
    assert entry is not None
    assert entry['type'] == 'article'
    assert entry['key'] == 'key6'
    assert entry['fields']['title'] == 'Spaceless'
    assert entry['fields']['year'] == '2020'

def test_parse_entry_invalid():
    assert parse_entry("Not a bibtex entry") is None
    assert parse_entry("@article{missing_comma_and_fields}") is None

def test_sanitize_slug():
    assert sanitize_slug("Hello World!") == "hello-world"
    assert sanitize_slug("Paper Title: Subtitle") == "paper-title-subtitle"
    assert sanitize_slug("A" * 100) == "a" * 80

def test_html_escape():
    assert html_escape("A & B < C > D") == "A &amp; B &lt; C &gt; D"

def test_extract_highlights():
    fields = {'note': 'This is an outstanding paper.', 'remarks': ''}
    award, presentation = extract_highlights(fields)
    assert award == 'Outstanding Paper Award'
    assert presentation is None

    fields = {'note': 'oral presentation', 'remarks': ''}
    award, presentation = extract_highlights(fields)
    assert award is None
    assert presentation == 'Oral presentation'

    fields = {'note': 'Best paper award', 'remarks': 'oral'}
    award, presentation = extract_highlights(fields)
    assert award == 'Outstanding Paper Award'
    assert presentation == 'Oral presentation'
