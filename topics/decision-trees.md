# How a decision tree thinks

<img src="https://img.shields.io/badge/Machine_learning-7C3AED?style=flat-square" alt="Machine learning"> <img src="https://img.shields.io/badge/status-planned-B45309?style=flat-square" alt="planned">

> This model plays 20 questions with your data, and you can read every answer.

## The idea

A decision tree predicts by asking yes-or-no questions: is the income above 50k? Is the account older than a year? Each question splits the data, and the tree picks the question that makes the groups as pure as possible.

Trees are the base of random forests and gradient boosting, which still win most competitions on tabular data. Unlike a neural network, you can print a tree and follow its reasoning.

## What the lesson will build

- A tree built from scratch on a small loan-approval dataset
- Gini impurity computed by hand to choose each split
- A printed tree you can read like a flowchart

## Key ideas

- Splits and impurity (Gini)
- Depth and overfitting
- Why trees handle mixed data types well
- From one tree to forests and boosting

## The video

- **Long form:** Data points split by a vertical line, then a horizontal one, as the tree grows. Each node lights up as the code computes its impurity.
- **Short:** Three questions, one prediction, and you can see why.

When it's published, the code will live in [`machine-learning/`](../machine-learning) and this page will link to it.

---
[All topics](README.md) · [Suggest a topic](https://github.com/DayanEbrar0X/data-anatomy.ai/issues/new?title=Topic+idea%3A+)
