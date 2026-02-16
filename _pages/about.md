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
    <li><strong>{{ item.date }}</strong>: {{ item.text | markdownify | remove: '<p>' | remove: '</p>' }}</li>
  {% endfor %}
</ul>
<p><a href="/news/">More News</a></p>

## Selected Publications

{% assign selected_pubs = site.publications | where: "selected", true | sort: "date" | reverse %}
{% for post in selected_pubs %}
  {% include archive-single.html %}
{% endfor %}

<p><a href="/publications/">Full Publication List</a></p>

## Teaching

<ul>
  <li><strong>CSI 2470 Introduction to Computer Networks</strong> (Fall 2025)</li>
  <li><strong>CSI 2560 Computational Linear Algebra</strong> (Winter 2026)</li>
</ul>
