---
layout: archive
title: "Research Group"
permalink: /group/
author_profile: true
---

{% assign students = site.data.students | default: empty %}

## Current Students

{% if students and students.size > 0 %}
<ul>
  {% for student in students %}
    <li>
      <strong>{{ student.name }}</strong><br>
      {{ student.role }}<br>
      {{ student.institution }}
      {% if student.year %}<br>Expected Graduation: {{ student.year }}{% endif %}
      {% if student.website %}<br><a href="{{ student.website }}">Website</a>{% endif %}
    </li>
  {% endfor %}
</ul>
{% else %}
<p>No current students listed.</p>
{% endif %}

## Alumni

*(This section will be populated as students graduate)*
