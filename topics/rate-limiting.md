# Rate limiting with a token bucket

<img src="https://img.shields.io/badge/Backend-BE185D?style=flat-square" alt="Backend"> <img src="https://img.shields.io/badge/status-planned-B45309?style=flat-square" alt="planned">

> How an API tells you to slow down.

## The idea

APIs protect themselves by limiting how many requests each client can make. The token bucket is the classic algorithm: tokens drip into a bucket at a steady rate, each request spends one, and an empty bucket means wait.

It allows short bursts while enforcing an average rate, which is why so many APIs use it.

## What the lesson will build

- A token bucket in about 15 lines
- A burst of requests, some allowed and some rejected
- The HTTP 429 response and Retry-After header

## Key ideas

- Token bucket versus fixed window
- Bursts and refill rate
- HTTP 429
- Limiting per user or per key

## The video

- **Long form:** A bucket filling drop by drop, requests arriving as balls, and the bucket running dry during a burst.
- **Short:** Tokens in, requests out, and a 429 when it's empty.

When it's published, the code will live in [`backend/`](../backend) and this page will link to it.

---
[All topics](README.md) · [Suggest a topic](https://github.com/DayanEbrar0X/data-anatomy.ai/issues/new?title=Topic+idea%3A+)
