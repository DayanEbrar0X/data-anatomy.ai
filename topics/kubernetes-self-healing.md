# Kubernetes and the reconciliation loop

<img src="https://img.shields.io/badge/Cloud-0369A1?style=flat-square" alt="Cloud"> <img src="https://img.shields.io/badge/status-planned-B45309?style=flat-square" alt="planned">

> Delete a container and watch it come back.

## The idea

You don't tell Kubernetes what to do. You tell it what you want, like three copies of this app, and controllers keep comparing that to what's running and fixing the difference.

That reconciliation loop is why pods restart, deployments roll out gradually, and clusters recover from failed machines without anyone typing a command.

## What the lesson will build

- A toy reconciliation loop in Python
- A deployment of three replicas, one deleted and replaced
- A rolling update from version 1 to version 2

## Key ideas

- Desired state
- Controllers
- Pods, ReplicaSets and Deployments
- Rolling updates

## The video

- **Long form:** Three pods on a node, one disappearing, and a new one fading in as the controller notices the gap.
- **Short:** You declare three. It keeps three.

When it's published, the code will live in [`cloud/`](../cloud) and this page will link to it.

---
[All topics](README.md) · [Suggest a topic](https://github.com/DayanEbrar0X/data-anatomy.ai/issues/new?title=Topic+idea%3A+)
