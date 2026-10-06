# PySpark: data too big for one machine

<img src="https://img.shields.io/badge/Data_engineering-047857?style=flat-square" alt="Data engineering"> <img src="https://img.shields.io/badge/status-lesson_ready-047857?style=flat-square" alt="lesson ready">

> Your laptop chokes on a billion rows. Spark splits the job across a cluster.

## The idea

Spark splits a DataFrame into partitions and processes them in parallel. Transformations like filter and groupBy are lazy: Spark only builds a plan. An action like show or write makes it run.

A groupBy needs a shuffle, moving rows with the same key to the same place. The same code runs on a laptop or a cluster of hundreds of machines.

## What the lesson will build

- A deterministic event dataset built inside Spark
- Filter, new columns, groupBy and aggregate
- The moment the plan actually runs

## Key ideas

- Partitions
- Lazy transformations and actions
- Shuffles
- Local mode versus a cluster

## The video

- **Long form:** Rows split into lanes, a plan building up dimly while nothing runs, then lighting up on the action, with a shuffle in the middle.
- **Short:** Nothing runs until you ask for an answer.

The lesson is ready: code and a line-by-line walkthrough in [`data-engineering/13-pyspark/`](../data-engineering/13-pyspark).

---
[All topics](README.md) · [Suggest a topic](https://github.com/DayanEbrar0X/data-anatomy.ai/issues/new?title=Topic+idea%3A+)
