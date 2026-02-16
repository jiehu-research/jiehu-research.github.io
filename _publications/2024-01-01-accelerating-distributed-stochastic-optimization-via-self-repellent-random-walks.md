---

title: "Accelerating Distributed Stochastic Optimization via Self-Repellent Random Walks"
authors: '<strong>Jie Hu</strong>, Vishwaraj Doshi, Do Young Eun'
collection: publications
selected: true
category: conferences
permalink: /publication/2024-accelerating-distributed-stochastic-optimization-via-self-repellent-random-walks
date: 2024-05-01
venue: "International Conference on Learning Representations"
paperurl: "https://openreview.net/pdf?id=BV1PHbTJzd"
abstract: >-
  We study a family of distributed stochastic optimization algorithms where gradients are sampled by a token traversing a network of agents in random-walk fashion. Typically, these random-walks are chosen to be Markov chains that asymptotically sample from a desired target distribution, and play a critical role in the convergence of the optimization iterates. In this paper, we take a novel approach by replacing the standard linear Markovian token by one which follows a nonlinear Markov chain - namely the Self-Repellent Radom Walk (SRRW). Defined for any given 'base' Markov chain, the SRRW, parameterized by a positive scalar {\alpha}, is less likely to transition to states that were highly visited in the past, thus the name. In the context of MCMC sampling on a graph, a recent breakthrough in Doshi et al. (2023) shows that the SRRW achieves O(1/{\alpha}) decrease in the asymptotic variance for sampling. We propose the use of a 'generalized' version of the SRRW to drive token algorithms for distributed stochastic optimization in the form of stochastic approximation, termed SA-SRRW. We prove that the optimization iterate errors of the resulting SA-SRRW converge to zero almost surely and prove a central limit theorem, deriving the explicit form of the resulting asymptotic covariance matrix corresponding to iterate errors. This asymptotic covariance is always smaller than that of an algorithm driven by the base Markov chain and decreases at rate O(1/{\alpha}^2) - the performance benefit of using SRRW thereby amplified in the stochastic optimization context. Empirical results support our theoretical findings.
citation: '<strong>Hu, Jie</strong>, Doshi, Vishwaraj, Eun, Do Young. (2024). &quot;Accelerating Distributed Stochastic Optimization via Self-Repellent Random Walks&quot;. <i>International Conference on Learning Representations</i>.'
presentation: "Oral presentation"
location: "Vienna Austria"
---
