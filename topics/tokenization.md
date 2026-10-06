# Tokenization: why AI can't count letters

<img src="https://img.shields.io/badge/AI_engineering-2563EB?style=flat-square" alt="AI engineering"> <img src="https://img.shields.io/badge/status-planned-B45309?style=flat-square" alt="planned">

> Ask an AI how many r's are in 'strawberry'. Here's why it struggles.

## The idea

Language models don't read letters. They read tokens: chunks of text from a fixed vocabulary, where a common word might be one token and a rare word several. 'strawberry' may arrive as a few pieces, so the model never sees the individual letters it's asked to count.

Tokens also explain why models price by the token, why some languages cost more, and why numbers behave oddly. This lesson builds byte-pair encoding, the algorithm behind most tokenizers, from scratch.

## What the lesson will build

- A byte-pair encoder that learns merges from a small text
- Encoding and decoding a sentence, with every token shown
- A count of tokens per word, and the words that split the most

## Key ideas

- Vocabulary and merges
- Byte-pair encoding
- Why token counts drive cost and context limits
- Tokenization artifacts

## The video

- **Long form:** A sentence breaking into colored chunks as merges are learned, then 'strawberry' splitting into its tokens.
- **Short:** The model never sees the letters. It sees these chunks.

When it's published, the code will live in [`ai-engineering/`](../ai-engineering) and this page will link to it.

---
[All topics](README.md) · [Suggest a topic](https://github.com/DayanEbrar0X/data-anatomy.ai/issues/new?title=Topic+idea%3A+)
