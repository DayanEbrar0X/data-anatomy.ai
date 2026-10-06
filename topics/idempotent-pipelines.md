# Idempotent pipelines

<img src="https://img.shields.io/badge/Data_engineering-047857?style=flat-square" alt="Data engineering"> <img src="https://img.shields.io/badge/status-planned-B45309?style=flat-square" alt="planned">

> Your job failed halfway, you reran it, and now revenue is doubled.

## The idea

Pipelines fail and get retried. If running a step twice produces a different result from running it once, every retry risks duplicates or gaps. An idempotent step gives the same result no matter how many times it runs.

The usual patterns are writing to a partition and replacing it whole, merging on a key instead of appending, and keeping outputs deterministic.

## What the lesson will build

- A naive append job that double-counts on rerun
- The same job rewritten to overwrite a date partition
- A rerun showing identical results

## Key ideas

- Idempotency
- Partition overwrite
- Merge on key
- Deterministic outputs

## The video

- **Long form:** A revenue counter doubling on a rerun, then the fixed job rerun three times with the number holding steady.
- **Short:** Run it twice. Same answer.

When it's published, the code will live in [`data-engineering/`](../data-engineering) and this page will link to it.

---
[All topics](README.md) · [Suggest a topic](https://github.com/DayanEbrar0X/data-anatomy.ai/issues/new?title=Topic+idea%3A+)
