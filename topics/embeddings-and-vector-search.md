# Embeddings and vector search

<img src="https://img.shields.io/badge/AI_engineering-2563EB?style=flat-square" alt="AI engineering"> <img src="https://img.shields.io/badge/status-planned-B45309?style=flat-square" alt="planned">

> Your search found 'car' when you typed 'vehicle'. Here's how.

## The idea

An embedding turns text into a list of numbers, placed so that similar meanings land close together. Search then becomes geometry: embed the query, find the nearest vectors.

Word2vec famously showed that directions can carry meaning, so king minus man plus woman lands near queen. Vector databases exist to do this nearest-neighbor search fast over millions of items.

## What the lesson will build

- Small word vectors plotted in 2D
- Nearest-neighbor search with cosine similarity
- A brute-force index compared with a simple approximate one

## Key ideas

- Embedding spaces
- Cosine similarity
- Exact versus approximate nearest neighbors
- What vector databases add

## The video

- **Long form:** Words drifting into clusters on a map, then a query point dropping in and pulling its nearest neighbors into view.
- **Short:** Meaning, turned into distance.

When it's published, the code will live in [`ai-engineering/`](../ai-engineering) and this page will link to it.

---
[All topics](README.md) · [Suggest a topic](https://github.com/DayanEbrar0X/data-anatomy.ai/issues/new?title=Topic+idea%3A+)
