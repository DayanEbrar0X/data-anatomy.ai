# LLM as a judge

<img src="https://img.shields.io/badge/Methodologies-0E1525?style=flat-square" alt="Methodologies"> <img src="https://img.shields.io/badge/status-planned-B45309?style=flat-square" alt="planned">

> Grading AI with AI works, until it doesn't.

## The idea

Human review doesn't scale to thousands of outputs, so teams ask a second model to grade the first. It's fast and often agrees with people, but judges have known biases: they favor longer answers, the first option shown, and answers that sound like their own writing.

This lesson builds a judge, measures how often it agrees with human labels, and shows the checks that make its scores trustworthy.

## What the lesson will build

- A rubric-based judge prompt and a small labeled set
- Agreement rate between the judge and the human labels
- A position-bias test: the same pair, shown in both orders

## Key ideas

- Rubrics
- Agreement with human labels
- Position and length bias
- Calibrating a judge

## The video

- **Long form:** Two answers side by side, the judge's score appearing, then the same pair swapped and the score flipping.
- **Short:** Swap the order and the judge changes its mind.

When it's published, the code will live in [`methodologies/`](../methodologies) and this page will link to it.

---
[All topics](README.md) · [Suggest a topic](https://github.com/DayanEbrar0X/data-anatomy.ai/issues/new?title=Topic+idea%3A+)
