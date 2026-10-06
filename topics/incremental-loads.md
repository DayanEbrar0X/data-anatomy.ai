# Incremental loads and change data capture

<img src="https://img.shields.io/badge/Data_engineering-047857?style=flat-square" alt="Data engineering"> <img src="https://img.shields.io/badge/status-planned-B45309?style=flat-square" alt="planned">

> Your pipeline reloads 10 million rows to pick up 200 changes.

## The idea

Full reloads are simple and get slower every day. Incremental loads only move what changed, either by tracking a watermark like the last updated timestamp, or by reading the database's own change log (change data capture).

Doing this correctly means handling updates, deletes and late-arriving rows, which is where most pipeline bugs live.

## What the lesson will build

- A watermark-based incremental load over a small orders table
- An upsert (merge) into the target table
- Late and deleted rows, handled explicitly

## Key ideas

- Watermarks
- Upserts and merges
- Change data capture
- Soft deletes and late data

## The video

- **Long form:** A table of rows where only the changed ones light up and travel down the pipeline, while the rest stay put.
- **Short:** Move 200 rows, not 10 million.

When it's published, the code will live in [`data-engineering/`](../data-engineering) and this page will link to it.

---
[All topics](README.md) · [Suggest a topic](https://github.com/DayanEbrar0X/data-anatomy.ai/issues/new?title=Topic+idea%3A+)
