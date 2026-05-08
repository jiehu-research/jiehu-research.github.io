---
layout: post
title: "A Gentle Introduction to Self-Repellent Random Walks"
date: 2025-08-15
description: "Why do classical random walks fail for distributed sampling, and how self-repellent walks fix the problem."
tags: [MCMC, graph-sampling, research-notes]
math: true
---

Standard random walks on graphs are the workhorse of many distributed algorithms.
But they have a fundamental flaw: the walker tends to revisit the same nodes
repeatedly, leading to high sampling variance. This post explains the intuition
behind **self-repellent random walks** and why they matter for distributed optimization.

## The Problem with Standard Random Walks

Consider a graph $G = (V, E)$ with $n$ nodes. A classical random walk generates
a sequence of nodes $X_0, X_1, X_2, \ldots$ where at each step the walker moves
to a uniformly random neighbor.

The stationary distribution of this walk is proportional to node degree:

$$\pi(v) = \frac{\deg(v)}{2|E|}.$$

For sampling purposes, we often want the *empirical average*

$$\hat{\mu}_T = \frac{1}{T} \sum_{t=0}^{T-1} f(X_t)$$

to converge to the true mean $\mu = \sum_v \pi(v) f(v)$. The convergence rate
is governed by the **asymptotic variance**

$$\sigma^2 = \lim_{T \to \infty} T \cdot \text{Var}(\hat{\mu}_T).$$

For a random walk on a path graph with $n$ nodes, $\sigma^2$ scales as $O(n^2)$ —
catastrophically bad.

## The Self-Repellent Idea

The key insight: what if the walk *actively avoids* recently visited nodes?

Define a **self-repellent random walk** by modifying the transition probability
based on local visit counts. Let $L_t(v)$ be the number of times node $v$ has
been visited up to time $t$. The transition kernel becomes:

$$P_t(u \to v) \propto \frac{\mathbf{1}[v \sim u]}{1 + \alpha \cdot L_t(v)},$$

where $\alpha > 0$ is a repulsion parameter and $v \sim u$ means $v$ is a
neighbor of $u$.

This is a **nonlinear** Markov chain — the transition probabilities depend on
the entire history, not just the current state.

## Why Does This Help?

Intuitively, the repulsion spreads the walk more evenly across the graph.
Formally, one can show that under mild conditions, the self-repellent walk
achieves **minimal asymptotic variance** among all history-dependent random walks
on the same graph.

For the path graph example above, the optimal self-repellent walk reduces
$\sigma^2$ from $O(n^2)$ to $O(n)$ — a quadratic improvement.

## Connection to Distributed Optimization

In distributed stochastic optimization, nodes of a network collaboratively
minimize an objective

$$\min_{x \in \mathbb{R}^d} \frac{1}{n} \sum_{v=1}^n f_v(x),$$

where each node $v$ holds a local function $f_v$. Random walk-based algorithms
use the walker's current location to determine which gradient to compute at each
step. Lower sampling variance directly translates to faster convergence of the
optimization algorithm.

Our [ICLR 2024 paper](/publications/) shows that replacing the standard random
walk with a self-repellent walk yields provably faster convergence rates, matching
lower bounds in several regimes.

## What's Next

In a follow-up post, I'll discuss how to extend these ideas beyond pairwise
repulsion to **history-driven target distributions** — the subject of our ICML
2025 work.

---

*Feedback or questions? Feel free to email me.*
