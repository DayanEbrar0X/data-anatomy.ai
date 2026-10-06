# A data platform on AWS with Terraform

<img src="https://img.shields.io/badge/Build_Projects-B91C1C?style=flat-square" alt="Build Projects"> <img src="https://img.shields.io/badge/status-planned-B45309?style=flat-square" alt="planned">

> From raw events to a live dashboard, all defined in code.

## The idea

This project builds a small but real data platform: events land in S3, a pipeline turns them into bronze, silver and gold tables, a query engine serves them, and a dashboard reads the gold layer.

Every piece of infrastructure is written in Terraform, so the whole platform can be created and destroyed with one command.

## What the lesson will build

- Terraform for S3, IAM, and compute
- An ingestion and transformation pipeline
- Medallion tables queried with SQL
- A dashboard, and a teardown

## Key ideas

- Infrastructure as code
- Lakehouse layers
- Least-privilege IAM
- Cost awareness

## The video

- **Long form:** A series: an empty AWS account diagram filling in service by service as each part is applied.
- **Short:** One command builds it. One command removes it.

When it's published, the code will live in [`build-projects/`](../build-projects) and this page will link to it.

---
[All topics](README.md) · [Suggest a topic](https://github.com/DayanEbrar0X/data-anatomy.ai/issues/new?title=Topic+idea%3A+)
