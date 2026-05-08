---
layout: default
title: News
permalink: /news/
---

<div class="page-container">
  <div class="section-header" style="margin-top:0">
    <h1 class="page-title" style="margin-bottom:0;border:none">News</h1>
    <a class="edit-link" href="https://github.com/{{ site.repository }}/edit/{{ site.branch | default: "master" }}/_data/news.yml"
       target="_blank" rel="noopener" title="Edit news on GitHub">✎ edit</a>
  </div>

  <ul class="news-list news-list-full">
    {% for item in site.data.news %}
    <li class="news-item">
      <span class="news-date">{{ item.date }}</span>
      <span class="news-text">
        {{ item.text | markdownify | remove: '<p>' | remove: '</p>' }}
        {% if item.link %} <a class="news-link" href="{{ item.link }}" target="_blank" rel="noopener">↗</a>{% endif %}
      </span>
    </li>
    {% endfor %}
  </ul>
</div>
