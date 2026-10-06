# Polars: the fast DataFrame library

<img src="https://img.shields.io/badge/Data_engineering-047857?style=flat-square" alt="Data engineering"> <img src="https://img.shields.io/badge/status-lesson_ready-047857?style=flat-square" alt="lesson ready">

> Same question, same data. One library reads the whole file, the other reads only what it needs.

## The idea

Polars is a DataFrame library written in Rust that uses every CPU core and Apache Arrow memory. Its lazy API builds a query plan first, and an optimizer improves it before anything runs.

Filters get pushed down into the file scan, and only the needed columns are read. On large files, that's the difference between reading everything and reading a fraction of it.

## What the lesson will build

- A million-row Parquet file
- A lazy query: scan, filter, group, aggregate
- The optimized plan, showing the pushdown

## Key ideas

- Expressions
- Lazy versus eager
- Predicate and projection pushdown
- Columnar memory

## The video

- **Long form:** A Parquet file drawn as column stripes, with the filter sliding down into the scan and only a few stripes lighting up.
- **Short:** Read less, finish sooner.

The lesson is ready: code and a line-by-line walkthrough in [`data-engineering/14-polars/`](../data-engineering/14-polars).

---
[All topics](README.md) · [Suggest a topic](https://github.com/DayanEbrar0X/data-anatomy.ai/issues/new?title=Topic+idea%3A+)
