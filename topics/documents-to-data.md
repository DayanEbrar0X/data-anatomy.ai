# Documents to data: OCR, Parquet and a vector database

<img src="https://img.shields.io/badge/Data_engineering-047857?style=flat-square" alt="Data engineering"> <img src="https://img.shields.io/badge/status-in_production-7C3AED?style=flat-square" alt="in production">

> A folder of scanned invoices becomes a table you can query and a knowledge base an AI can search.

## The idea

Part 1 turns invoice images into data: OCR reads the pixels into text, a parser pulls out vendor, date and total into JSON, and the records land in Parquet, ready for SQL with DuckDB.

Part 2 embeds the same documents into vectors and stores them in LanceDB, so a question like 'which invoice was for printer toner?' finds the right document by meaning, with a citation, ready for a RAG prompt.

## What the lesson will build

- Generated invoice images, read with Tesseract OCR
- A parser that turns text into a schema
- Parquet plus DuckDB for analytics
- Embeddings in LanceDB for retrieval

## Key ideas

- OCR
- Schemas and structured extraction
- Columnar storage
- Embeddings and vector search for RAG

## The video

- **Long form:** One wide pipeline: invoices scanned line by line, JSON records, a Parquet table, then vectors settling into a map where a question finds its neighbors.
- **Short:** One folder of images, two consumers: SQL and AI.

When it's published, the code will live in [`data-engineering/`](../data-engineering) and this page will link to it.

---
[All topics](README.md) · [Suggest a topic](https://github.com/DayanEbrar0X/data-anatomy.ai/issues/new?title=Topic+idea%3A+)
