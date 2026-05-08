---
layout: default
title: Blog
permalink: /blog/
---

<div class="page-container">
  <div class="section-header" style="margin-top:0">
    <h1 class="page-title" style="margin-bottom:0;border:none">Blog</h1>
    <a class="section-more" href="{{ '/feed.xml' | prepend: site.baseurl }}" target="_blank" rel="noopener">RSS &uarr;</a>
  </div>
  <p class="page-subtitle">Notes on research, math, and ideas. Math is rendered with MathJax.</p>

  {% assign all_tags = "" | split: "" %}
  {% for post in site.posts %}
    {% for tag in post.tags %}
      {% assign all_tags = all_tags | push: tag %}
    {% endfor %}
  {% endfor %}
  {% assign all_tags = all_tags | uniq | sort %}

  {% if all_tags.size > 0 %}
  <div class="blog-tag-bar" id="blog-tag-bar">
    <button class="blog-tag-chip active" data-tag="" type="button">All</button>
    {% for t in all_tags %}
      <button class="blog-tag-chip" data-tag="{{ t | downcase }}" type="button">{{ t }}</button>
    {% endfor %}
  </div>
  {% endif %}

  {% if site.posts.size == 0 %}
    <p style="color:var(--text-secondary);margin-top:32px">No posts yet &mdash; check back soon!</p>
  {% else %}
  <ul class="blog-list" id="blog-list">
    {% for post in site.posts %}
    <li class="blog-item" data-tags="{% for t in post.tags %}{{ t | downcase }} {% endfor %}">
      <div class="blog-item-meta">
        <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%B %-d, %Y" }}</time>
        {% for tag in post.tags %}<span class="tag">{{ tag }}</span>{% endfor %}
      </div>
      <div class="blog-item-title">
        <a href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a>
      </div>
      {% if post.description %}
        <p class="blog-item-excerpt">{{ post.description }}</p>
      {% elsif post.excerpt %}
        <p class="blog-item-excerpt">{{ post.excerpt | strip_html | truncate: 200 }}</p>
      {% endif %}
    </li>
    {% endfor %}
  </ul>
  {% endif %}
</div>

<script>
(function () {
  var bar = document.getElementById('blog-tag-bar');
  if (!bar) return;
  bar.addEventListener('click', function (e) {
    var btn = e.target.closest('.blog-tag-chip');
    if (!btn) return;
    bar.querySelectorAll('.blog-tag-chip').forEach(function (b) { b.classList.remove('active'); });
    btn.classList.add('active');
    var tag = btn.dataset.tag;
    document.querySelectorAll('#blog-list .blog-item').forEach(function (li) {
      li.style.display = (!tag || (' ' + li.dataset.tags + ' ').indexOf(' ' + tag + ' ') !== -1) ? '' : 'none';
    });
  });
})();
</script>
