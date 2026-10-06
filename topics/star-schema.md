# Star schemas: facts and dimensions

<img src="https://img.shields.io/badge/Data_architecture-0F766E?style=flat-square" alt="Data architecture"> <img src="https://img.shields.io/badge/status-planned-B45309?style=flat-square" alt="planned">

> Why the analytics team keeps talking about facts and dimensions.

## The idea

Analytics databases are often modeled as a star: one central fact table of events, like sales, surrounded by dimension tables describing who, what, where and when. It's the shape most BI tools expect.

The design keeps queries simple and fast, and it makes the grain explicit: exactly what one row of the fact table means.

## What the lesson will build

- A sales fact table with customer, product and date dimensions
- SQL queries that slice revenue by any dimension
- The same questions answered against a flat table, for comparison

## Key ideas

- Facts and dimensions
- Grain
- Surrogate keys
- Slowly changing dimensions

## The video

- **Long form:** A fact table in the center with dimension tables snapping into place around it, then a query lighting up the joins.
- **Short:** One fact table, many ways to slice it.

When it's published, the code will live in [`data-architecture/`](../data-architecture) and this page will link to it.

---
[All topics](README.md) · [Suggest a topic](https://github.com/DayanEbrar0X/data-anatomy.ai/issues/new?title=Topic+idea%3A+)
