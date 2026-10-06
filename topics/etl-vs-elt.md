# ETL vs ELT

<img src="https://img.shields.io/badge/Data_engineering-047857?style=flat-square" alt="Data engineering"> <img src="https://img.shields.io/badge/status-in_production-7C3AED?style=flat-square" alt="in production">

> Same three letters, different order, and it changes your whole data platform.

## The idea

ETL transforms data before loading it: clean it in Python or a tool, then load only the result. ELT loads the raw data first and transforms it inside the warehouse with SQL.

ELT took over as storage got cheap and warehouses got powerful: keeping the raw data means you can rerun new logic without extracting again. ETL still wins when sensitive data must be cleaned or masked before it lands anywhere.

## What the lesson will build

- The same messy orders data run both ways
- ETL with pandas, ELT with SQL inside DuckDB
- A side-by-side of what each one keeps

## Key ideas

- Extract, transform, load
- Raw versus modeled data
- Masking PII before it lands
- Where dbt fits

## The video

- **Long form:** Two pipelines stacked, with the T block sliding to a new position and a PII column masked in one lane but not the other.
- **Short:** Transform first, or load first. Here's when each wins.

When it's published, the code will live in [`data-engineering/`](../data-engineering) and this page will link to it.

---
[All topics](README.md) · [Suggest a topic](https://github.com/DayanEbrar0X/data-anatomy.ai/issues/new?title=Topic+idea%3A+)
