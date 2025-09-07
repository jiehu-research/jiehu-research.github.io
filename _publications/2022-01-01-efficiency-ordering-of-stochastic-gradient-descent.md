---

title: "Efficiency ordering of stochastic gradient descent"
authors: '<strong>Jie Hu</strong>, Vishwaraj Doshi, Do Young Eun'
collection: publications
category: conferences
permalink: /publication/2022-efficiency-ordering-of-stochastic-gradient-descent
date: 2022-12-01
venue: "Advances in Neural Information Processing Systems"
paperurl: "https://proceedings.neurips.cc/paper_files/paper/2022/file/65ccdfe02045fa0b823c5fa7ffd56b66-Paper-Conference.pdf"
abstract: >-
  We consider the stochastic gradient descent (SGD) algorithm driven by a general stochastic sequence, including i.i.d noise and random walk on an arbitrary graph, among others; and analyze it in the asymptotic sense. Specifically, we employ the notion of `efficiency ordering', a well-analyzed tool for comparing the performance of Markov Chain Monte Carlo (MCMC) samplers, for SGD algorithms in the form of Loewner ordering of covariance matrices associated with the scaled iterate errors in the long term. Using this ordering, we show that input sequences that are more efficient for MCMC sampling also lead to smaller covariance of the errors for SGD algorithms in the limit. This also suggests that an arbitrarily weighted MSE of SGD iterates in the limit becomes smaller when driven by more efficient chains. Our finding is of particular interest in applications such as decentralized optimization and swarm learning, where SGD is implemented in a random walk fashion on the underlying communication graph for cost issues and/or data privacy. We demonstrate how certain non-Markovian processes, for which typical mixing-time based non-asymptotic bounds are intractable, can outperform their Markovian counterparts in the sense of efficiency ordering for SGD. We show the utility of our method by applying it to gradient descent with shuffling and mini-batch gradient descent, reaffirming key results from existing literature under a unified framework. Empirically, we also observe efficiency ordering for variants of SGD such as accelerated SGD and Adam, open up the possibility of extending our notion of efficiency ordering to a broader family of stochastic optimization algorithms.
citation: '<strong>Hu, Jie</strong>, Doshi, Vishwaraj, Eun, Do Young. (2022). &quot;Efficiency ordering of stochastic gradient descent&quot;. <i>Advances in Neural Information Processing Systems</i>.'
location: "New Orleans, LA"
---
