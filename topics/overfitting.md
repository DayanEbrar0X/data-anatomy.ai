# Overfitting: why a perfect score is a red flag

<img src="https://img.shields.io/badge/Machine_learning-7C3AED?style=flat-square" alt="Machine learning"> <img src="https://img.shields.io/badge/status-planned-B45309?style=flat-square" alt="planned">

> This model scored 100%. That's the problem.

## The idea

A model that memorizes its training data looks perfect until it meets new data. Fit a curve through ten points with a degree-9 polynomial and it passes through every one, then swings wildly between them.

The fix is to hold data back. The gap between training and validation error is the most useful number in machine learning, and this lesson shows it moving as model complexity grows.

## What the lesson will build

- Polynomial fits of degree 1, 3 and 9 on the same noisy data
- A train and validation split, with both errors printed
- The classic U-shaped validation curve

## Key ideas

- Training versus validation error
- Bias and variance
- Regularization
- Why more data helps

## The video

- **Long form:** Three curves over the same points: too simple, about right, and a wild one that hits every point. The validation error climbs as the curve gets more perfect.
- **Short:** 100% on training, terrible on new data. Here's why.

When it's published, the code will live in [`machine-learning/`](../machine-learning) and this page will link to it.

---
[All topics](README.md) · [Suggest a topic](https://github.com/DayanEbrar0X/data-anatomy.ai/issues/new?title=Topic+idea%3A+)
