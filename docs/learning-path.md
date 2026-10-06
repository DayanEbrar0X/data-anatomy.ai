# Learning path

Every lesson is one short video plus the exact code from the video. The best way to learn from them:

1. **Watch** the video once, without pausing.
2. **Run** the code and check that you get the same output as the video.
3. **Read** the lesson README. It walks through the code line by line, using the line numbers you saw on screen.
4. **Break it.** Do the "Try this" exercises at the bottom of each README. Changing a number and predicting what
   happens teaches more than reading.

## Model Anatomy, in order

The lessons build on each other. If you are new, go in this order.

### Part 1: How models learn

| # | Lesson | You will understand |
|---|--------|---------------------|
| 00 | [What is machine learning](../machine-learning/00-what-is-machine-learning) | What "learning from examples" means, in 8 lines. |
| 01 | [Gradient descent](../machine-learning/01-gradient-descent) | How every model improves: feel the slope, step downhill. |
| 07 | [Linear regression, no libraries](../machine-learning/07-linear-regression-no-libraries) | The full training loop written out by hand, and what a bad learning rate does. |
| 02 | [K-means](../machine-learning/02-k-means) | How a program finds groups in data that has no labels. |

Lesson 07 comes right after 01 on purpose: it repeats lesson 00 with no NumPy, so you see every step.

### Part 2: Machine learning in practice

| # | Lesson | You will understand |
|---|--------|---------------------|
| 08 | [Decision trees](../machine-learning/08-decision-trees) | How a model picks its questions, and why you can read its decisions. |
| 09 | [A neural network from scratch](../machine-learning/09-neural-network-from-scratch) | Layers, a non-linearity and backpropagation, on the XOR puzzle. |
| 10 | [Overfitting](../machine-learning/10-overfitting) | Why a perfect training score is a warning, and how validation catches it. |
| 11 | [Choosing a model](../machine-learning/11-choosing-a-model) | How teams pick an algorithm: data first, goal second, model last. |

### Part 3: How AI systems are built

| # | Lesson | You will understand |
|---|--------|---------------------|
| 03 | [The AI agent loop](../ai-engineering/03-ai-agent-loop) | Think, act, observe, repeat: how agents use tools. |
| 06 | [RAG from scratch](../ai-engineering/06-rag) | How an assistant answers from your own documents. |
| 04 | [Ontologies](../methodologies/04-ontology) | How an agent connects facts across systems. |
| 05 | [Evals and loop engineering](../methodologies/05-evals-loop-engineering) | How to improve an AI system with measurements instead of guesses. |

## Build Lab

Build Lab episodes are projects. Each one builds a small, real piece of software across several parts.

| Project | Parts |
|---------|-------|
| [01 · API to Parquet](../data-engineering/build-lab-01-api-to-parquet) | Part 1: fetch, clean, write Parquet, query with DuckDB |

## What you need to know first

- **Python basics:** variables, lists, loops, functions. If you can read a `for` loop, you can follow every lesson.
- **No math background needed.** Where math shows up (a slope, an average, a distance), the README explains it in
  words first.

Words you don't know are in the [glossary](glossary.md). Want to know what's coming next? See the [topics](../topics/README.md).

---
[Back to all lessons](../README.md)
