---
layout: archive
title: "News Archive"
permalink: /news/
author_profile: true
---

{% assign news = site.data.news | sort: 'date' | reverse %}
<ul>
  {% for item in news %}
    <li><strong>{{ item.date }}</strong>: {{ item.text | markdownify | remove: '<p>' | remove: '</p>' }}</li>
  {% endfor %}
</ul>
