# Temperature: how an AI picks the next word

<img src="https://img.shields.io/badge/AI_engineering-2563EB?style=flat-square" alt="AI engineering"> <img src="https://img.shields.io/badge/status-planned-B45309?style=flat-square" alt="planned">

> Same prompt, different answer every time. One number controls it.

## The idea

At every step, a language model outputs a probability for every token in its vocabulary. Something then has to pick one. Temperature reshapes those probabilities before the pick: low temperature makes the top choice dominate, high temperature flattens everything.

Top-k and top-p sampling cut off the long tail of unlikely tokens. Together these settings decide whether an assistant is predictable or surprising.

## What the lesson will build

- A softmax over a small vocabulary of next-word scores
- Sampling at temperature 0.2, 1.0 and 2.0, with the results counted
- Top-k and top-p filters added on top

## Key ideas

- Logits and softmax
- Temperature scaling
- Greedy decoding versus sampling
- Top-k and top-p

## The video

- **Long form:** A bar chart of next-word probabilities sharpening and flattening as the temperature dial turns.
- **Short:** Turn the dial: from always the same word to chaos.

When it's published, the code will live in [`ai-engineering/`](../ai-engineering) and this page will link to it.

---
[All topics](README.md) · [Suggest a topic](https://github.com/DayanEbrar0X/data-anatomy.ai/issues/new?title=Topic+idea%3A+)
