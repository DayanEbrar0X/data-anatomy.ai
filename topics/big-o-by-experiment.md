# Big O, by experiment

<img src="https://img.shields.io/badge/Software_engineering-4338CA?style=flat-square" alt="Software engineering"> <img src="https://img.shields.io/badge/status-planned-B45309?style=flat-square" alt="planned">

> Fast on 100 rows. Dead on a million. Here's why.

## The idea

Big O notation describes how running time grows with input size. It's easier to feel than to read: time a loop inside a loop at 1,000, 10,000 and 100,000 items and watch the gap explode.

The fix is often a different data structure, like a set lookup instead of a list scan, and the difference is measurable in a few lines.

## What the lesson will build

- The same duplicate check written two ways: nested loops and a set
- Timings at growing input sizes
- A plot of both curves

## Key ideas

- O(n), O(n log n), O(n²)
- Lists versus sets and dictionaries
- Measuring instead of guessing
- When it doesn't matter

## The video

- **Long form:** Two runners on a track as the input grows: one keeps pace, the other falls further behind with every step.
- **Short:** Same answer. One is 1,000 times slower.

When it's published, the code will live in [`software-engineering/`](../software-engineering) and this page will link to it.

---
[All topics](README.md) · [Suggest a topic](https://github.com/DayanEbrar0X/data-anatomy.ai/issues/new?title=Topic+idea%3A+)
