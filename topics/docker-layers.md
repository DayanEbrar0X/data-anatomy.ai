# Docker images, layer by layer

<img src="https://img.shields.io/badge/Cloud-0369A1?style=flat-square" alt="Cloud"> <img src="https://img.shields.io/badge/status-planned-B45309?style=flat-square" alt="planned">

> Why your Docker image is 2 GB.

## The idea

A Docker image is a stack of layers, one per build instruction. Layers are cached and shared, which makes builds fast, but a file added in one layer still takes up space even if a later layer deletes it.

Ordering instructions well and using multi-stage builds can cut an image from gigabytes to tens of megabytes.

## What the lesson will build

- A deliberately bloated Dockerfile and its layer sizes
- The same app rebuilt with good layer order
- A multi-stage build with a slim final image

## Key ideas

- Layers and the build cache
- Instruction order
- Multi-stage builds
- Base image choice

## The video

- **Long form:** An image stacking up layer by layer with sizes labeled, then collapsing to a thin final image.
- **Short:** 2 GB to 80 MB, same app.

When it's published, the code will live in [`cloud/`](../cloud) and this page will link to it.

---
[All topics](README.md) · [Suggest a topic](https://github.com/DayanEbrar0X/data-anatomy.ai/issues/new?title=Topic+idea%3A+)
