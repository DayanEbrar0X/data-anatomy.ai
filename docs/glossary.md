# Glossary

Every term used in the videos, in plain words. The lesson in brackets is where it first shows up.

**Agent** [03]
A language model running in a loop: it picks an action, your code runs it, and the result goes back in for the next
decision.

**Centroid / center** [02]
The middle of a group of points: the average of their positions.

**Chunk** [06]
A small piece of a document. RAG systems split documents into chunks so they can retrieve just the relevant part.

**Clustering** [02]
Sorting data into groups of similar items without being told what the groups are.

**Columnar format** [Build Lab 01]
A file layout that stores each column together instead of each row. Fast for analytics, because a query only reads
the columns it needs.

**Cosine similarity** [06]
How much two vectors point the same way. 1 means the same direction, 0 means unrelated.

**DuckDB** [Build Lab 01]
A database that runs inside your Python process and can query files like Parquet directly with SQL.

**Embedding** [06]
A list of numbers that represents the meaning of a piece of text. Similar meanings get similar numbers.

**Epoch** [00]
One full pass over the training data.

**Eval set** [05]
A fixed list of examples with known right answers, used to score a system the same way every time.

**Gradient** [01]
The direction in which the loss rises fastest, and how steeply. Training steps the opposite way.

**Gradient descent** [01]
Improving a model by repeatedly stepping its weights a little way downhill on the loss.

**Guardrail** [03]
A limit that stops an AI system from doing too much: a maximum number of steps, a budget, an allowed list of tools.

**Hallucination** [04]
When a model states something false with confidence, usually because it guessed instead of looking it up.

**Learning rate** [00]
How big each training step is. Too small learns slowly; too big overshoots and can blow up.

**Linear regression** [07]
Fitting a straight line to data, `y = w × x + b`, to predict one number from another.

**LLM (large language model)** [03]
A model trained on a huge amount of text that predicts what comes next. Chat assistants are built on them.

**Loss** [01]
One number that says how wrong the model is. Training tries to make it small.

**Loop engineering** [05]
Improving an AI system in cycles: run it on an eval set, score it, fix the failures, run it again.

**Model** [00]
The numbers a program learned (its weights), plus the formula that uses them to make predictions.

**Ontology** [04]
A shared description of what kinds of things exist in a domain and how they may be connected.

**Pagination** [Build Lab 01]
When an API returns results a page at a time, with a pointer to the next page.

**Parquet** [Build Lab 01]
A compressed, typed, columnar file format for tables. The standard hand-off format in data engineering.

**Pass rate** [05]
The share of eval cases a system gets right.

**Pipeline** [Build Lab 01]
A chain of steps that moves data from a source to a destination, for example fetch, clean, write.

**RAG (retrieval-augmented generation)** [06]
Finding relevant pieces of your own documents and putting them in the prompt, so the model answers from them.

**Tool** [03]
A function an agent can ask your code to run, like a search or a calculator.

**Triple** [04]
One fact written as (subject, relation, object), like ("Acme", "supplies", "bolt").

**Unsupervised learning** [02]
Learning patterns from data that has no labels, like finding clusters.

**Vector** [06]
A list of numbers. Embeddings are vectors.

**Weights** [00]
The numbers inside a model that training adjusts. In lesson 00 there are two: `w` and `b`.

---
[Back to all lessons](../README.md)
