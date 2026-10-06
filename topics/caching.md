# Caching and the hardest problem in computer science

<img src="https://img.shields.io/badge/Backend-BE185D?style=flat-square" alt="Backend"> <img src="https://img.shields.io/badge/status-planned-B45309?style=flat-square" alt="planned">

> Your app got 50 times faster. Then it showed yesterday's prices.

## The idea

A cache keeps the answer to an expensive question so the next request is instant. The hard part is knowing when that answer is no longer true.

This lesson builds a cache with expiry and an LRU eviction policy, then breaks it with stale data and fixes it with invalidation.

## What the lesson will build

- A slow function wrapped in a cache, with hit and miss timings
- Time-based expiry and LRU eviction
- A stale read, and the invalidation that fixes it

## Key ideas

- Hits and misses
- TTL
- LRU eviction
- Cache invalidation strategies

## The video

- **Long form:** Requests racing to a slow database, then bouncing off a fast cache, until one returns an outdated value.
- **Short:** Fast, until it's wrong.

When it's published, the code will live in [`backend/`](../backend) and this page will link to it.

---
[All topics](README.md) · [Suggest a topic](https://github.com/DayanEbrar0X/data-anatomy.ai/issues/new?title=Topic+idea%3A+)
