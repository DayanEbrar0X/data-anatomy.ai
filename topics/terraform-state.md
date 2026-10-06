# What Terraform state actually is

<img src="https://img.shields.io/badge/Cloud-0369A1?style=flat-square" alt="Cloud"> <img src="https://img.shields.io/badge/status-planned-B45309?style=flat-square" alt="planned">

> Terraform remembers what it built. Lose that memory and it builds everything again.

## The idea

Terraform compares three things: the code you wrote, the state file it saved last time, and what really exists in the cloud. The plan is the difference between them.

The state file maps each resource in your code to a real ID, which is why it must be stored remotely, locked during changes, and never edited by hand. Terragrunt adds structure for running the same code across many environments.

## What the lesson will build

- A small Terraform config and its plan
- The state file opened and explained, line by line
- Drift: a change made by hand, and how plan detects it

## Key ideas

- Desired versus actual state
- Plan and apply
- Remote state and locking
- Drift

## The video

- **Long form:** Code on one side, the cloud on the other, and the state file in the middle drawing lines between them.
- **Short:** Code, state, reality. The plan is the gap.

When it's published, the code will live in [`cloud/`](../cloud) and this page will link to it.

---
[All topics](README.md) · [Suggest a topic](https://github.com/DayanEbrar0X/data-anatomy.ai/issues/new?title=Topic+idea%3A+)
