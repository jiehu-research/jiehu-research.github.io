---

title: "Self-repellent random walks on general graphs-achieving minimal sampling variance via nonlinear Markov chains"
authors: 'Vishwaraj Doshi, <strong>Jie Hu</strong>, Do Young Eun'
collection: publications
selected: true
category: conferences
permalink: /publication/2023-self-repellent-random-walks-on-general-graphs-achieving-minimal-sampling-varianc
date: 2023-07-01
venue: "International Conference on Machine Learning"
paperurl: "https://proceedings.mlr.press/v202/doshi23a/doshi23a.pdf"
abstract: >-
  We consider random walks on discrete state spaces, such as general undirected graphs, where the random walkers are designed to approximate a target quantity over the network topology via sampling and neighborhood exploration in the form of Markov chain Monte Carlo (MCMC) procedures. Given any Markov chain corresponding to a target probability distribution, we design a self-repellent random walk (SRRW) which is less likely to transition to nodes that were highly visited in the past, and more likely to transition to seldom visited nodes. For a class of SRRWs parameterized by a positive real α, we prove that the empirical distribution of the process converges almost surely to the the target (stationary) distribution of the underlying Markov chain kernel. We then provide a central limit theorem and derive the exact form of the arising asymptotic co-variance matrix, which allows us to show that the SRRW with a stronger repellence (larger α) always achieves a smaller asymptotic covariance, in the sense of Loewner ordering of co-variance matrices. Especially for SRRW-driven MCMC algorithms, we show that the decrease in the asymptotic sampling variance is of the order O(1/α), eventually going down to zero. Finally, we provide numerical simulations complimentary to our theoretical results, also empirically testing a version of SRRW with α increasing in time to combine the benefits of smaller asymptotic variance due to large α, with empirically observed faster mixing properties of SRRW with smaller α.
citation: 'Doshi, Vishwaraj, <strong>Hu, Jie</strong>, Eun, Do Young. (2023). &quot;Self-repellent random walks on general graphs-achieving minimal sampling variance via nonlinear Markov chains&quot;. <i>International Conference on Machine Learning</i>.'
presentation: "Outstanding Paper Award"
location: "Honolulu, HI"
---
