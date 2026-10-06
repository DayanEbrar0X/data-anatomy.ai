# Topics

What we're making next. Every topic here becomes a video, a page of explanation, and runnable code in this repo.
Each page already explains the idea, so you can start learning before the video is out.

Have an idea? [Suggest a topic](https://github.com/DayanEbrar0X/data-anatomy.ai/issues/new?title=Topic+idea%3A+).

## Machine learning

| Topic | Hook | Status |
|-------|------|--------|
| [What is machine learning](../machine-learning/00-what-is-machine-learning) | Watch the video and run the code | Published |
| [Gradient descent](../machine-learning/01-gradient-descent) | Watch the video and run the code | Published |
| [K-means clustering](../machine-learning/02-k-means) | Watch the video and run the code | Published |
| [Linear regression, no libraries](../machine-learning/07-linear-regression-no-libraries) | Watch the video and run the code | Published |
| [A neural network from scratch](neural-network-from-scratch.md) | One straight line can't solve this four-point puzzle. Two layers can. | [Lesson ready](../machine-learning/09-neural-network-from-scratch) |
| [How a decision tree thinks](decision-trees.md) | This model plays 20 questions with your data, and you can read every answer. | [Lesson ready](../machine-learning/08-decision-trees) |
| [Overfitting: why a perfect score is a red flag](overfitting.md) | This model scored 100%. That's the problem. | [Lesson ready](../machine-learning/10-overfitting) |
| [How to choose an ML algorithm in production](choosing-a-model.md) | There is no best algorithm. Here's how teams actually pick one. | [Lesson ready](../machine-learning/11-choosing-a-model) |

## AI engineering

| Topic | Hook | Status |
|-------|------|--------|
| [The AI agent loop](../ai-engineering/03-ai-agent-loop) | Watch the video and run the code | Published |
| [RAG from scratch](../ai-engineering/06-rag) | Watch the video and run the code | Published |
| [Tokenization: why AI can't count letters](tokenization.md) | Ask an AI how many r's are in 'strawberry'. Here's why it struggles. | Planned |
| [Temperature: how an AI picks the next word](temperature-and-sampling.md) | Same prompt, different answer every time. One number controls it. | Planned |
| [Embeddings and vector search](embeddings-and-vector-search.md) | Your search found 'car' when you typed 'vehicle'. Here's how. | Planned |
| [Tool calling: how an AI runs your code](tool-calling.md) | The model doesn't run your function. It writes a request, and your code decides. | Planned |

## Methodologies

| Topic | Hook | Status |
|-------|------|--------|
| [Ontologies for AI agents](../methodologies/04-ontology) | Watch the video and run the code | Published |
| [Evals and loop engineering](../methodologies/05-evals-loop-engineering) | Watch the video and run the code | Published |
| [LLM as a judge](llm-as-a-judge.md) | Grading AI with AI works, until it doesn't. | Planned |
| [Prompt injection](prompt-injection.md) | One sentence hidden in a web page can take over your AI agent. | Planned |

## Data engineering

| Topic | Hook | Status |
|-------|------|--------|
| [API to Parquet](../data-engineering/build-lab-01-api-to-parquet) | Watch the video and run the code | Published |
| [Incremental loads and change data capture](incremental-loads.md) | Your pipeline reloads 10 million rows to pick up 200 changes. | Planned |
| [Idempotent pipelines](idempotent-pipelines.md) | Your job failed halfway, you reran it, and now revenue is doubled. | Planned |
| [ETL vs ELT](etl-vs-elt.md) | Same three letters, different order, and it changes your whole data platform. | [Lesson ready](../data-engineering/12-etl-vs-elt) |
| [PySpark: data too big for one machine](pyspark.md) | Your laptop chokes on a billion rows. Spark splits the job across a cluster. | In production |
| [Polars: the fast DataFrame library](polars.md) | Same question, same data. One library reads the whole file, the other reads only what it needs. | In production |
| [Documents to data: OCR, Parquet and a vector database](documents-to-data.md) | A folder of scanned invoices becomes a table you can query and a knowledge base an AI can search. | In production |

## Data architecture

| Topic | Hook | Status |
|-------|------|--------|
| [Bronze, silver, gold: the medallion architecture](medallion-architecture.md) | Raw data in, trusted data out, in three layers. | Planned |
| [Star schemas: facts and dimensions](star-schema.md) | Why the analytics team keeps talking about facts and dimensions. | Planned |

## Exploratory data analysis

| Topic | Hook | Status |
|-------|------|--------|
| [Simpson's paradox](simpsons-paradox.md) | Treatment A wins in every group, and loses overall. | Planned |
| [When the average lies](mean-vs-median.md) | Ten people in a bar. A billionaire walks in. Now the average person is a millionaire. | Planned |

## Software engineering

| Topic | Hook | Status |
|-------|------|--------|
| [Big O, by experiment](big-o-by-experiment.md) | Fast on 100 rows. Dead on a million. Here's why. | Planned |
| [How Git actually stores your code](git-internals.md) | Git is a key-value store wearing a version control costume. | Planned |

## Backend

| Topic | Hook | Status |
|-------|------|--------|
| [Rate limiting with a token bucket](rate-limiting.md) | How an API tells you to slow down. | Planned |
| [Caching and the hardest problem in computer science](caching.md) | Your app got 50 times faster. Then it showed yesterday's prices. | Planned |

## Cloud

| Topic | Hook | Status |
|-------|------|--------|
| [Docker images, layer by layer](docker-layers.md) | Why your Docker image is 2 GB. | Planned |
| [What Terraform state actually is](terraform-state.md) | Terraform remembers what it built. Lose that memory and it builds everything again. | Planned |
| [Kubernetes and the reconciliation loop](kubernetes-self-healing.md) | Delete a container and watch it come back. | Planned |
| [How AWS decides allow or deny](aws-iam-policies.md) | Your Lambda has permission, and AWS still says Access Denied. | Planned |

## Build Projects

| Topic | Hook | Status |
|-------|------|--------|
| [A production RAG assistant, end to end](rag-assistant-end-to-end.md) | From a folder of PDFs to an assistant your team actually trusts. | Planned |
| [A data platform on AWS with Terraform](data-platform-on-aws.md) | From raw events to a live dashboard, all defined in code. | Planned |

---
[All lessons](../README.md)
