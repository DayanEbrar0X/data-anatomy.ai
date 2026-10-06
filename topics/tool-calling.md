# Tool calling: how an AI runs your code

<img src="https://img.shields.io/badge/AI_engineering-2563EB?style=flat-square" alt="AI engineering"> <img src="https://img.shields.io/badge/status-planned-B45309?style=flat-square" alt="planned">

> The model doesn't run your function. It writes a request, and your code decides.

## The idea

When an assistant books a meeting or queries a database, the model itself only produces text: a structured request naming a tool and its arguments. Your code validates that request, runs the tool, and sends the result back.

This is the contract behind agents and protocols like MCP. Getting it right, with schemas, validation and permission checks, is most of what makes an agent safe to deploy.

## What the lesson will build

- Tool definitions written as JSON schemas
- A loop that parses a tool request, validates it and runs it
- A rejected call, when the model asks for something it isn't allowed to do

## Key ideas

- Function schemas
- Structured output
- Validation and permissions
- Where MCP fits

## The video

- **Long form:** A request leaving the model as JSON, passing through a validation gate, and the result flowing back into the chat.
- **Short:** The model asks. Your code decides.

When it's published, the code will live in [`ai-engineering/`](../ai-engineering) and this page will link to it.

---
[All topics](README.md) · [Suggest a topic](https://github.com/DayanEbrar0X/data-anatomy.ai/issues/new?title=Topic+idea%3A+)
