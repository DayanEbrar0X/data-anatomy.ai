<p align="center">
  <img src="assets/banner.png" alt="Datanatomy" width="100%">
</p>

<p align="center">
  <a href="https://www.youtube.com/@datanatomyai"><img src="https://img.shields.io/badge/YouTube-datanatomyai-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube"></a>
  <a href="https://www.tiktok.com/@datanatomy.ai"><img src="https://img.shields.io/badge/TikTok-datanatomy.ai-000000?style=for-the-badge&logo=tiktok&logoColor=white" alt="TikTok"></a>
  <a href="https://www.instagram.com/datanatomy.ai"><img src="https://img.shields.io/badge/Instagram-datanatomy.ai-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram"></a>
  <br>
  <a href="https://x.com/datanatomyai"><img src="https://img.shields.io/badge/X-datanatomyai-000000?style=for-the-badge&logo=x&logoColor=white" alt="X"></a>
  <a href="https://www.linkedin.com/company/datanatomy"><img src="https://img.shields.io/badge/LinkedIn-Datanatomy-0A66C2?style=for-the-badge" alt="LinkedIn"></a>
  <a href="https://www.threads.net/@datanatomy.ai"><img src="https://img.shields.io/badge/Threads-datanatomy.ai-000000?style=for-the-badge&logo=threads&logoColor=white" alt="Threads"></a>
</p>

<p align="center">
  <a href="https://github.com/DayanEbrar0X/data-anatomy.ai/actions/workflows/tests.yml"><img src="https://github.com/DayanEbrar0X/data-anatomy.ai/actions/workflows/tests.yml/badge.svg" alt="tests"></a>
  <img src="https://img.shields.io/badge/python-3.10%2B-2563EB?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/lessons-8-7C3AED?style=flat-square" alt="8 lessons">
  <img src="https://img.shields.io/badge/build_lab-1_project-B45309?style=flat-square" alt="1 Build Lab project">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-047857?style=flat-square" alt="MIT license"></a>
</p>

# Datanatomy

The code behind every Datanatomy video. Each lesson is a short, real program you can run in a few seconds,
paired with a video that walks through it line by line while an animation shows what each line does.

<p align="center">
  <img src="assets/gifs/hero.gif" alt="Gradient descent, k-means, ontologies and a data pipeline, animated" width="100%">
</p>

Two series:

- **Model Anatomy** opens up how ML and AI actually work: gradient descent, clustering, agents, RAG, evals.
- **Build Lab** builds real projects step by step, the way you would at work.

No black boxes: the models here are small enough to read in one sitting, and the numbers you see in the videos are
the numbers these files print.

<!-- latest:start -->
## Latest video

<a href="build-lab/01-api-to-parquet"><img src="assets/gifs/build-lab-01-api-to-parquet.gif" width="220" align="left" alt="API to Parquet"></a>

**Build Lab, Part 1: API to Parquet**

Build a real data pipeline in three Python files: fetch paginated JSON from an API, clean it with pandas,
write Parquet, and query it with DuckDB. 19.0 KB of JSON becomes 5.6 KB of Parquet.

Watch: [YouTube](https://www.youtube.com/@datanatomyai) · [TikTok](https://www.tiktok.com/@datanatomy.ai) · [Instagram](https://www.instagram.com/datanatomy.ai)
Code: [`build-lab/01-api-to-parquet`](build-lab/01-api-to-parquet)

<br clear="left">
<!-- latest:end -->

## Lessons

### Model Anatomy: how ML and AI work from the inside

| # | Lesson | You'll learn | Video |
|---|--------|--------------|-------|
| 00 | [Machine learning](00-machine-learning) | What "learning from examples" means, with a line that fits itself to 40 house prices | 35s |
| 01 | [Gradient descent](01-gradient-descent) | How every model improves: feel the slope, take a small step, repeat | 32s |
| 02 | [K-means clustering](02-k-means) | Finding groups in data nobody labeled | 31s |
| 03 | [The AI agent loop](03-ai-agent-loop) | Think, act, observe: the loop behind every AI agent, with tools and a guardrail | 83s |
| 04 | [Ontologies for AI agents](04-ontology) | Why agents need named relationships to answer multi-hop questions | 92s + 34s |
| 05 | [Evals and loop engineering](05-evals-loop-engineering) | Measuring an AI system, fixing it, and keeping it from breaking again | 100s + 34s |
| 06 | [RAG from scratch](06-rag) | How an assistant answers from your own documents, with a source | 95s + 30s |
| 07 | [Linear regression, no libraries](07-linear-regression-no-libraries) | The full training loop in plain Python, and what breaks it | 80s + 32s |

### Build Lab: real projects, built step by step

| # | Project | You'll build | Video |
|---|---------|--------------|-------|
| 01 | [API to Parquet](build-lab/01-api-to-parquet) | A three-file data pipeline: API pages to a clean, typed, queryable Parquet file | 99s |

New to this? Start with the [learning path](docs/learning-path.md).

## Gallery

Every lesson, moving. Click one to open its code and walkthrough.

<table>
  <tr>
    <td align="center" width="33%"><a href="00-machine-learning"><img src="assets/gifs/00-machine-learning.gif" width="220" alt="00 · Machine learning"></a><br><b><a href="00-machine-learning">00 · Machine learning</a></b></td>
    <td align="center" width="33%"><a href="01-gradient-descent"><img src="assets/gifs/01-gradient-descent.gif" width="220" alt="01 · Gradient descent"></a><br><b><a href="01-gradient-descent">01 · Gradient descent</a></b></td>
    <td align="center" width="33%"><a href="02-k-means"><img src="assets/gifs/02-k-means.gif" width="220" alt="02 · K-means"></a><br><b><a href="02-k-means">02 · K-means</a></b></td>
  </tr>
  <tr>
    <td align="center" width="33%"><a href="03-ai-agent-loop"><img src="assets/gifs/03-ai-agent-loop.gif" width="220" alt="03 · The agent loop"></a><br><b><a href="03-ai-agent-loop">03 · The agent loop</a></b></td>
    <td align="center" width="33%"><a href="04-ontology"><img src="assets/gifs/04-ontology.gif" width="220" alt="04 · Ontologies"></a><br><b><a href="04-ontology">04 · Ontologies</a></b></td>
    <td align="center" width="33%"><a href="05-evals-loop-engineering"><img src="assets/gifs/05-evals-loop-engineering.gif" width="220" alt="05 · Evals"></a><br><b><a href="05-evals-loop-engineering">05 · Evals</a></b></td>
  </tr>
  <tr>
    <td align="center" width="33%"><a href="06-rag"><img src="assets/gifs/06-rag.gif" width="220" alt="06 · RAG from scratch"></a><br><b><a href="06-rag">06 · RAG from scratch</a></b></td>
    <td align="center" width="33%"><a href="07-linear-regression-no-libraries"><img src="assets/gifs/07-linear-regression-no-libraries.gif" width="220" alt="07 · Linear regression"></a><br><b><a href="07-linear-regression-no-libraries">07 · Linear regression</a></b></td>
    <td align="center" width="33%"><a href="build-lab/01-api-to-parquet"><img src="assets/gifs/build-lab-01-api-to-parquet.gif" width="220" alt="Build Lab 01 · API to Parquet"></a><br><b><a href="build-lab/01-api-to-parquet">Build Lab 01 · API to Parquet</a></b></td>
  </tr>
</table>

## Run the code

You need Python 3.10 or newer.

```bash
git clone https://github.com/DayanEbrar0X/data-anatomy.ai.git
cd data-anatomy.ai
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python3 03-ai-agent-loop/src/agent.py    # run any lesson
pytest                                  # check every lesson still matches its video
```

Lessons 03, 04, 05, 06 and 07 use only the Python standard library. Lessons 00 to 02 need NumPy, and the Build Lab
project needs pandas, PyArrow and DuckDB. More detail in [docs/setup.md](docs/setup.md).

## How the repo is organized

```
data-anatomy.ai/
├── 00-machine-learning/ ... 07-linear-regression-no-libraries/    Model Anatomy lessons
├── build-lab/                                                      Build Lab projects
├── docs/                                                           learning path, setup, glossary
├── assets/                                                         banner, logo, GIFs
├── .github/workflows/tests.yml                                     runs every test on each push
└── requirements.txt
```

Every lesson uses the same layout, the one real Python projects use:

```
04-ontology/
├── README.md         the idea, how to run it, a line-by-line walkthrough, things to try
├── data/             the data, as plain CSV or JSON files
├── scripts/          one-off scripts that generated the data (when there are any)
├── src/              the code from the video, plus the helpers it imports
├── short/            the code from the 30-second version (when there is one)
└── tests/            checks that the code still prints what the video shows
```

Keeping data, code and tests apart is a habit worth copying. You can change the data without touching the logic,
and the tests tell you right away if an edit broke something. The file from the video is always in `src/`, line
for line, so you can pause on any frame and find the same line here.

## Docs

- [Learning path](docs/learning-path.md): what to watch and run, in order
- [Setup](docs/setup.md): Python, virtual environments, and troubleshooting
- [Glossary](docs/glossary.md): every term used in the videos, in plain words

## License

[MIT](LICENSE). Use the code to learn, teach, or build. A link back to the channel is appreciated.
