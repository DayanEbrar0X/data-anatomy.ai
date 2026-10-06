# Bronze, silver, gold: the medallion architecture

<img src="https://img.shields.io/badge/Data_architecture-0F766E?style=flat-square" alt="Data architecture"> <img src="https://img.shields.io/badge/status-planned-B45309?style=flat-square" alt="planned">

> Raw data in, trusted data out, in three layers.

## The idea

Most lakehouses organize data in three layers. Bronze keeps raw data exactly as it arrived. Silver cleans, deduplicates and types it. Gold shapes it for a business question, like daily revenue by region.

The layers make problems traceable: when a dashboard number looks wrong, you can walk back through gold and silver to the raw record that caused it.

## What the lesson will build

- The same orders data stored as bronze, silver and gold Parquet files
- The transformation between each layer, and the tests that guard it
- A gold table answering one business question

## Key ideas

- Raw versus cleaned versus modeled data
- Lineage
- Where to put data quality checks
- Lakehouse table formats

## The video

- **Long form:** Three stacked layers filling one after another, with a single bad record caught between bronze and silver.
- **Short:** Bronze, silver, gold. Each with one job.

When it's published, the code will live in [`data-architecture/`](../data-architecture) and this page will link to it.

---
[All topics](README.md) · [Suggest a topic](https://github.com/DayanEbrar0X/data-anatomy.ai/issues/new?title=Topic+idea%3A+)
