# How Git actually stores your code

<img src="https://img.shields.io/badge/Software_engineering-4338CA?style=flat-square" alt="Software engineering"> <img src="https://img.shields.io/badge/status-planned-B45309?style=flat-square" alt="planned">

> Git is a key-value store wearing a version control costume.

## The idea

Every file, folder and commit in Git is an object, stored under the hash of its contents. A commit points to a tree, a tree points to files and other trees, and a branch is just a name pointing to a commit.

Once you see that, branches, merges and rebases stop being mysterious: they're all ways of creating new objects and moving pointers.

## What the lesson will build

- A tiny content-addressed store in Python
- Blobs, trees and commits built by hand
- A branch created by writing one pointer

## Key ideas

- Content addressing
- Blobs, trees and commits
- Branches as pointers
- Why history is hard to change

## The video

- **Long form:** Files hashing into objects, objects linking into a tree, and a branch label sliding from commit to commit.
- **Short:** A branch is one line in a file.

When it's published, the code will live in [`software-engineering/`](../software-engineering) and this page will link to it.

---
[All topics](README.md) · [Suggest a topic](https://github.com/DayanEbrar0X/data-anatomy.ai/issues/new?title=Topic+idea%3A+)
