---
layout: default
title: Publications
permalink: /publications/
math: true
---

{% capture edit_link %}https://github.com/{{ site.repository }}/edit/{{ site.branch | default: "master" }}/_data/publications.yml{% endcapture %}

<div class="page-container">

  <div class="section-header" style="margin-top:0">
    <h1 class="page-title" style="margin-bottom:0;border:none">Publications</h1>
    <span class="section-meta">
      <a class="edit-link" href="{{ edit_link }}" target="_blank" rel="noopener" title="Edit publications on GitHub">&#9998; edit</a>
      {% if site.links.google_scholar != "" %}
      <a class="section-more" href="{{ site.links.google_scholar }}" target="_blank" rel="noopener">Google Scholar &uarr;</a>
      {% endif %}
    </span>
  </div>

  <p class="page-subtitle">
    Click any title to view the PDF. <strong>Bold</strong> indicates this author.
    <span class="kbd-hint">Press <kbd>/</kbd> to search.</span>
  </p>

  <div class="pub-filter-bar">
    <input type="search" id="pub-filter" placeholder="Filter by title, author, venue, or year..." autocomplete="off">
    <span id="pub-filter-count" class="pub-filter-count"></span>
  </div>

  {% assign pubs_by_year = site.data.publications | group_by: "year" | sort: "name" | reverse %}
  {% for year_group in pubs_by_year %}
    <div class="pub-year-group" data-year="{{ year_group.name }}">
      <div class="pub-year-label">{{ year_group.name }}</div>
      <ul class="pub-list">
        {% for pub in year_group.items %}
          {% include publication.html pub=pub %}
        {% endfor %}
      </ul>
    </div>
  {% endfor %}

  <p class="page-footer-note" style="margin-top:2rem">
    Need a single BibTeX file?
    <a href="{{ '/assets/files/publications.bib' | prepend: site.baseurl }}" target="_blank" rel="noopener">Download .bib</a>.
  </p>
</div>

<script>
(function () {
  var input = document.getElementById('pub-filter');
  var count = document.getElementById('pub-filter-count');
  if (!input) return;

  document.addEventListener('keydown', function (e) {
    if (e.key === '/' && document.activeElement !== input) {
      e.preventDefault();
      input.focus();
    }
  });

  function filter() {
    var q = input.value.trim().toLowerCase();
    var items = document.querySelectorAll('.pub-list .pub-item');
    var shown = 0;
    items.forEach(function (item) {
      var match = !q || item.textContent.toLowerCase().indexOf(q) !== -1;
      item.style.display = match ? '' : 'none';
      if (match) shown++;
    });
    document.querySelectorAll('.pub-year-group').forEach(function (g) {
      var any = g.querySelector('.pub-item:not([style*="display: none"])');
      g.style.display = any ? '' : 'none';
    });
    count.textContent = q ? shown + ' match' + (shown === 1 ? '' : 'es') : '';
  }

  input.addEventListener('input', filter);
})();
</script>
