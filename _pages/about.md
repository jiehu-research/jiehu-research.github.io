---
permalink: /
title: "Jie Hu"
author_profile: true
redirect_from:
  - /about/
  - /about.html
---

I am an Assistant Professor in the Department of Computer Science and Engineering at Oakland University, based in Rochester, MI. My research focuses on machine learning theory and graph sampling. In particular, I'm interested in designing efficient algorithms for distributed optimization and graph mining, with the goal of pushing the boundaries of how quickly and effectively AI and ML tasks can be accomplished.

Research Areas
======
- Machine learning theory
- Graph mining
- Distributed optimization and algorithms

Prospective Students:
======
I am recruiting PhD students to start in Winter 2026 with expertise in applied probability, optimization, machine learning algorithms, or Markov chain Monte Carlo, and a passion for leveraging advanced algorithms to tackle complex, discipline-specific challenges.

News
======
{% assign news_items = site.data.news | default: empty %}
{% if news_items and news_items.size > 0 %}
<ul>
  {% for item in news_items %}
    <li><strong>{{ item.date }}</strong>: {{ item.text | markdownify | remove: '<p>' | remove: '</p>' }}</li>
  {% endfor %}
  </ul>
{% else %}
<p>No news yet. Add items in <code>_data/news.yml</code>.</p>
{% endif %}


Selected Publication
=====
ICML'25 &nbsp;&nbsp;&nbsp;&nbsp; **Jie Hu**, Yi-Ting Ma, and Do Young Eun, “Beyond Self-Repellent Kernels: History-Driven Target Towards Efficient Nonlinear MCMC on General Graphs“, International Conference on Machine Learning, Vancouver, Canada, July 2025 (Oral Presentation) (within 1% out of 12107 submissions)

ICLR'24 &nbsp;&nbsp;&nbsp;&nbsp; **Jie Hu**, Vishwaraj Doshi, and Do Young Eun, “Accelerating Distributed Stochastic Optimization via Self-Repellent Random Walks”, in International Conference on Learning Representations, Vienna, Austria, May 2024 (Oral Presentation) (within 1.2% out of 7262 submissions)

ICML'23 &nbsp;&nbsp;&nbsp;&nbsp; Vishwaraj Doshi, **Jie Hu**, and Do Young Eun, “Self-Repellent Random Walks on General Graphs – Achieving Minimal Sampling Variance via Nonlinear Markov Chains”, in International Conference on Machine Learning, Hawaii, July 2023 (Outstanding Paper Award)

Full Publication List
=====
Please refer to the full list on Google Scholar.

Mentoring
======
- Yi-Ting Ma, Ph.D. student at North Carolina State University
