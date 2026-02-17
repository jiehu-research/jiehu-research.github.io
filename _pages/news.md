---
layout: archive
title: "News Archive"
permalink: /news/
author_profile: true
---

{% assign news = site.data.news | sort: 'date' | reverse %}
<ul>
  {% for item in news %}
    {% assign date_parts = item.date | split: '-' %}
    {% capture formatted_date %}{{ date_parts[2] }}-{{ date_parts[0] }}-{{ date_parts[1] }}{% endcapture %}
    <li><strong>{{ formatted_date | date: "%b %Y" }}</strong>: {{ item.text | markdownify | remove: '<p>' | remove: '</p>' }}</li>
  {% endfor %}
</ul>
