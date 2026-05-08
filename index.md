---
layout: default
title: Home
math: true
---

{% capture edit_base %}https://github.com/{{ site.repository }}/edit/{{ site.branch | default: "master" }}{% endcapture %}

<div class="home-layout">

  <!-- ============== Left Sidebar ============== -->
  <aside class="profile-sidebar">
    <img class="profile-photo"
         src="{{ '/assets/images/profile.png' | prepend: site.baseurl }}"
         alt="Photo of {{ site.author.name }}">

    <h1 class="profile-name">
      {{ site.author.name }}
      {% if site.author.name_zh %}<span class="profile-name-zh">{{ site.author.name_zh }}</span>{% endif %}
    </h1>
    {% if site.author.pronouns %}<p class="profile-pronouns">{{ site.author.pronouns }}</p>{% endif %}
    <p class="profile-title">
      {{ site.author.title }}<br>
      {% if site.author.department_url %}<a href="{{ site.author.department_url }}" target="_blank" rel="noopener">{{ site.author.department }}</a>{% else %}{{ site.author.department }}{% endif %}<br>
      {% if site.author.university_url %}<a href="{{ site.author.university_url }}" target="_blank" rel="noopener">{{ site.author.university }}</a>{% else %}{{ site.author.university }}{% endif %}
    </p>
    {% if site.author.location %}<p class="profile-location">&#128205; {{ site.author.location }}</p>{% endif %}

    <ul class="profile-links">
      {% if site.links.email           != "" %}<li><a href="mailto:{{ site.links.email }}"><span class="link-icon">&#9993;</span> Email</a></li>{% endif %}
      {% if site.links.cv              != "" %}<li><a href="{{ site.links.cv }}" target="_blank" rel="noopener"><span class="link-icon">&#128196;</span> CV</a></li>{% endif %}
      {% if site.links.google_scholar  != "" %}<li><a href="{{ site.links.google_scholar }}"  target="_blank" rel="noopener"><span class="link-icon">&#127891;</span> Google Scholar</a></li>{% endif %}
      {% if site.links.semantic_scholar!= "" %}<li><a href="{{ site.links.semantic_scholar }}" target="_blank" rel="noopener"><span class="link-icon">&#128221;</span> Semantic Scholar</a></li>{% endif %}
      {% if site.links.dblp            != "" %}<li><a href="{{ site.links.dblp }}"            target="_blank" rel="noopener"><span class="link-icon">&#128218;</span> DBLP</a></li>{% endif %}
      {% if site.links.orcid           != "" %}<li><a href="{{ site.links.orcid }}"           target="_blank" rel="noopener"><span class="link-icon">&#128300;</span> ORCID</a></li>{% endif %}
      {% if site.links.github          != "" %}<li><a href="{{ site.links.github }}"          target="_blank" rel="noopener"><span class="link-icon">&#9881;</span> GitHub</a></li>{% endif %}
      {% if site.links.linkedin        != "" %}<li><a href="{{ site.links.linkedin }}"        target="_blank" rel="noopener"><span class="link-icon">&#128188;</span> LinkedIn</a></li>{% endif %}
    </ul>
  </aside>

  <!-- ============== Main Content ============== -->
  <div class="profile-main">

    <!-- Bio -->
    <p class="bio-text">
      I am an Assistant Professor in the
      <a href="{{ site.author.department_url }}" target="_blank" rel="noopener">{{ site.author.department }}</a>
      at <a href="{{ site.author.university_url }}" target="_blank" rel="noopener">{{ site.author.university }}</a>,
      based in {{ site.author.location }}. My research focuses on
      machine learning theory, distributed optimization,
      and graph sampling. In particular, I design efficient algorithms
      grounded in applied probability and Markov chain theory &mdash; pushing the boundaries
      of how quickly and effectively learning tasks can be performed over networks.
    </p>

    {% if site.recruiting.show %}
    <div class="recruiting-notice">
      <strong>Prospective Students:</strong>
      {{ site.recruiting.text | markdownify | remove: '<p>' | remove: '</p>' }}
      <a class="edit-link" href="{{ edit_base }}/_config.yml" target="_blank" rel="noopener" title="Edit recruiting blurb">&#9998;</a>
    </div>
    {% endif %}

    <!-- News -->
    <div class="section-header">
      <h2 class="section-title">News</h2>
      <span class="section-meta">
        <a class="edit-link" href="{{ edit_base }}/_data/news.yml" target="_blank" rel="noopener" title="Edit news on GitHub">&#9998; edit</a>
        <a class="section-more" href="{{ '/news/' | prepend: site.baseurl }}">All news &rarr;</a>
      </span>
    </div>
    <ul class="news-list">
      {% assign news_items = site.data.news | slice: 0, site.homepage.news_count %}
      {% for item in news_items %}
      <li class="news-item">
        <span class="news-date">{{ item.date }}</span>
        <span class="news-text">
          {{ item.text | markdownify | remove: '<p>' | remove: '</p>' }}
          {% if item.link %} <a class="news-link" href="{{ item.link }}" target="_blank" rel="noopener">&#8599;</a>{% endif %}
        </span>
      </li>
      {% endfor %}
    </ul>

    <!-- Selected Publications -->
    <div class="section-header">
      <h2 class="section-title">Selected Publications</h2>
      <span class="section-meta">
        <a class="edit-link" href="{{ edit_base }}/_data/publications.yml" target="_blank" rel="noopener" title="Edit publications on GitHub">&#9998; edit</a>
        <a class="section-more" href="{{ '/publications/' | prepend: site.baseurl }}">All publications &rarr;</a>
      </span>
    </div>

    {% assign featured = site.data.publications | where: "featured", true | sort: "year" | reverse %}
    <ul class="pub-list">
      {% for pub in featured %}
        {% include publication.html pub=pub %}
      {% endfor %}
    </ul>

    <!-- Teaching -->
    <div class="section-header">
      <h2 class="section-title">Teaching</h2>
      <span class="section-meta">
        <a class="edit-link" href="{{ edit_base }}/_data/teaching.yml" target="_blank" rel="noopener" title="Edit teaching on GitHub">&#9998; edit</a>
      </span>
    </div>
    <ul class="teaching-list">
      {% for course in site.data.teaching %}
      <li class="teaching-item">
        <span>
          <span class="teaching-code">{{ course.code }}</span>
          <span class="teaching-course">{{ course.title }}</span>
        </span>
        <span class="teaching-term">{{ course.term }}</span>
      </li>
      {% endfor %}
    </ul>

  </div>
</div>
