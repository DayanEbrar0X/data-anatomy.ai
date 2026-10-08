# Data engineering

Moving and shaping data: pipelines, file formats, and the steps between a source system and an answer.

| # | Lesson | You'll learn | Video |
|---|--------|--------------|-------|
| 12 | [ETL vs ELT](12-etl-vs-elt) | Where the transform runs, and why it changes your data platform | 138s |
| 13 | [PySpark](13-pyspark) | Partitions, lazy plans and shuffles: how Spark scales | 108s |
| 14 | [Polars](14-polars) | Lazy queries that read only the columns and row groups they need | 118s |
| 15 | [Idempotent pipelines](15-idempotent-pipelines) | Why a rerun doubled revenue, and how delete-then-insert makes a load safe to repeat | 86s + 34s |
| 16 | [Apache Iceberg](16-apache-iceberg) | Snapshots and time travel: undo a bad write in a data lake table | 113s + 34s |
| 17 | [Change data capture](17-change-data-capture) | Why a nightly diff misses changes, and how a change log catches every one | 127s + 39s |
| 18 | [SCD Type 2](18-scd-type-2) | Keep history in a dimension: close the old row, open a new one | 108s + 38s |
| 19 | [Incremental loads](19-incremental-loads) | Load only what changed since a watermark instead of every row | 118s + 36s |
| 20 | [Medallion architecture](20-medallion-architecture) | Bronze, silver and gold layers, and why raw data is kept | 125s + 36s |
| 21 | [Data contracts](21-data-contracts) | A schema check that stops a renamed column from becoming a $0 day | 111s + 38s |
| 22 | [The small files problem](22-small-files-problem) | Why thousands of tiny files slow a query, and how compaction fixes it | 112s + 35s |
| 23 | [Data engineer vs data scientist vs ML engineer](23-data-engineer-vs-data-scientist-vs-ml-engineer) | One churn dataset, three jobs: the pipeline, the model and the service | 112s + 38s |
| 24 | [Lake vs warehouse vs lakehouse](24-lake-vs-warehouse-vs-lakehouse) | The same question answered three ways, and what each storage layer gives you | 115s + 37s |
| 25 | [Data engineering for RAG](25-data-engineering-for-rag) | An ingestion pipeline that re-embeds only the documents that changed | 112s + 35s |
| 26 | [Batch vs streaming](26-batch-vs-streaming) | When data can't wait for the nightly job: the same check as a batch and a stream | 107s + 39s |
| BL01 | [Build Lab 01 · API to Parquet](build-lab-01-api-to-parquet) | A three-file data pipeline: API pages to a clean, typed, queryable Parquet file | 99s |
| BL02 | [Build Lab 02 · Documents to data](build-lab-02-documents-to-data) | Invoice images to OCR, JSON, Parquet and SQL, then embeddings in LanceDB for RAG | 140s + 143s |

---
[All lessons](../README.md)
