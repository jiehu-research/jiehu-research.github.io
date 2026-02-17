---
permalink: /
title: "Jie Hu"
author_profile: true
redirect_from:
  - /about/
  - /about.html
---

I am an Assistant Professor in the Department of Computer Science and Engineering at Oakland University, based in Rochester, MI. My research focuses on machine learning theory and graph sampling. In particular, I'm interested in designing efficient algorithms for distributed optimization and graph mining, with the goal of pushing the boundaries of how quickly and effectively AI and ML tasks can be accomplished.

**Prospective Students:** I am recruiting PhD students to start in Winter 2026 with expertise in applied probability, optimization, machine learning algorithms, or Markov chain Monte Carlo.

## News

<ul>
  {% assign news = site.data.news | sort: 'date' | reverse %}
  {% for item in news limit:5 %}
    {% assign date_parts = item.date | split: '-' %}
    {% capture formatted_date %}{{ date_parts[2] }}-{{ date_parts[0] }}-{{ date_parts[1] }}{% endcapture %}
    <li><strong>{{ formatted_date | date: "%b %Y" }}</strong>: {{ item.text | markdownify | remove: '<p>' | remove: '</p>' }}</li>
  {% endfor %}
</ul>
<p><a href="/news/">More News</a></p>

## Selected Publications

{% assign selected_pubs = site.publications | where: "selected", true | sort: "date" | reverse %}
{% assign last_year = "" %}
{% for post in selected_pubs %}
  {% assign current_year = post.date | date: "%Y" %}
  {% if current_year != last_year %}
{% if last_year != "" %}</ul>{% endif %}
<h3 style="margin-top: 1.5em; color: #1e6b7d;">{{ current_year }}</h3>
<ul style="list-style-type: disc; padding-left: 20px;">
    {% assign last_year = current_year %}
  {% endif %}
  {% include archive-single-publication.html %}
{% endfor %}
{% if last_year != "" %}</ul>{% endif %}

<p><a href="/publications/">Full Publication List</a></p>

## Teaching

<ul>
  <li><strong>CSI 2470 Introduction to Computer Networks</strong> (Fall 2025)</li>
  <li><strong>CSI 2560 Computational Linear Algebra</strong> (Winter 2026)</li>
</ul>
