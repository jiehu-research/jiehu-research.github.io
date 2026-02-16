---

title: "Beyond Self-Repellent Kernels: History-Driven Target Towards Efficient Nonlinear MCMC on General Graphs"
authors: '<strong>Jie Hu</strong>, Yi-Ting Ma, Do Young Eun'
collection: publications
selected: true
category: conferences
permalink: /publication/2025-beyond-self-repellent-kernels-history-driven-target-towards-efficient-nonlinear-
date: 2025-07-01
venue: "International Conference on Machine Learning"
paperurl: "https://openreview.net/pdf?id=0yzOEMbShU"
abstract: >-
  We propose a history-driven target (HDT) framework in Markov Chain Monte Carlo (MCMC) to improve any random walk algorithm on discrete state spaces, such as general undirected graphs, for efficient sampling from target distribution $\boldsymbol{\mu}$. With broad applications in network science and distributed optimization, recent innovations like the self-repellent random walk (SRRW) achieve near-zero variance by prioritizing under-sampled states through transition kernel modifications based on past visit frequencies. However, SRRW's reliance on explicit computation of transition probabilities for all neighbors at each step introduces substantial computational overhead, while its strict dependence on time-reversible Markov chains excludes advanced non-reversible MCMC methods. To overcome these limitations, instead of direct modification of transition kernel, HDT introduces a history-dependent target distribution $\boldsymbol{\pi}[\mathbf{x}]$ to replace the original target $\boldsymbol{\mu}$ in any graph sampler, where $\mathbf{x}$ represents the empirical measure of past visits. This design preserves lightweight implementation by requiring only local information between the current and proposed states and achieves compatibility with both reversible and non-reversible MCMC samplers, while retaining unbiased samples with target distribution $\boldsymbol{\mu}$ and near-zero variance performance. Extensive experiments in graph sampling demonstrate consistent performance gains, and a memory-efficient Least Recently Used (LRU) cache ensures scalability to large general graphs.
citation: '<strong>Hu, Jie</strong>, Ma, Yi-Ting, Eun, Do Young. (2025). &quot;Beyond Self-Repellent Kernels: History-Driven Target Towards Efficient Nonlinear MCMC on General Graphs&quot;. <i>International Conference on Machine Learning</i>.'
presentation: "Oral presentation"
location: "Vancouver, Canada"
---
