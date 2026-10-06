# A neural network from scratch

<img src="https://img.shields.io/badge/Machine_learning-7C3AED?style=flat-square" alt="Machine learning"> <img src="https://img.shields.io/badge/status-lesson_ready-047857?style=flat-square" alt="lesson ready">

> One straight line can't solve this four-point puzzle. Two layers can.

## The idea

XOR is the simplest problem a single straight line can't solve: four points, two classes, arranged so no line separates them. In 1969, Minsky and Papert showed that a single-layer perceptron can't learn it, and interest in neural networks cooled for years.

Add one hidden layer and the problem falls apart. The hidden layer bends the space so the classes become separable, and backpropagation tells every weight how to move. This lesson builds that network with nothing but NumPy.

## What the lesson will build

- A two-layer network: inputs, a hidden layer of 4 neurons, one output
- The forward pass, the loss, and backpropagation written out by hand
- A training loop that takes XOR from 50% to 100% correct

## Key ideas

- Neurons as weighted sums plus an activation
- Why stacking layers needs a non-linearity
- Backpropagation as the chain rule, applied layer by layer
- Decision boundaries

## The video

- **Long form:** The four XOR points on a grid, a single line failing to split them, then the hidden layer warping the space until a line works. Code typed below: forward, backward, update.
- **Short:** The line fails, the second layer bends the space, 100%.

The lesson is ready: code and a line-by-line walkthrough in [`machine-learning/09-neural-network-from-scratch/`](../machine-learning/09-neural-network-from-scratch).

---
[All topics](README.md) · [Suggest a topic](https://github.com/DayanEbrar0X/data-anatomy.ai/issues/new?title=Topic+idea%3A+)
