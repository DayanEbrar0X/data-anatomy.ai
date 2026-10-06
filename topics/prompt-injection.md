# Prompt injection

<img src="https://img.shields.io/badge/Methodologies-0E1525?style=flat-square" alt="Methodologies"> <img src="https://img.shields.io/badge/status-planned-B45309?style=flat-square" alt="planned">

> One sentence hidden in a web page can take over your AI agent.

## The idea

An agent that reads email, documents or web pages treats all of it as text in its context. If that text contains instructions, the model may follow them. That's prompt injection, and it's the main security risk for agents with tools.

There's no single fix, so the defense is layered: separate trusted and untrusted content, give tools the least access they need, and require confirmation for anything risky.

## What the lesson will build

- A toy agent that summarizes documents and can send email
- A poisoned document that tries to redirect it
- Defenses added one at a time, with the attack retried after each

## Key ideas

- Trusted versus untrusted input
- Least privilege for tools
- Confirmation steps
- Why filtering alone fails

## The video

- **Long form:** A document scrolling past with one hidden line glowing red, and the agent's next action changing because of it.
- **Short:** The attack is just a sentence.

When it's published, the code will live in [`methodologies/`](../methodologies) and this page will link to it.

---
[All topics](README.md) · [Suggest a topic](https://github.com/DayanEbrar0X/data-anatomy.ai/issues/new?title=Topic+idea%3A+)
