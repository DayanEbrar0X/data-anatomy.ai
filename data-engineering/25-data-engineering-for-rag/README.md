# 25 · Data engineering for RAG

<img src="https://img.shields.io/badge/level-intermediate-B45309?style=flat-square" alt="intermediate"> <img src="https://img.shields.io/badge/video-112s_%2B_35s_short-7C3AED?style=flat-square&logo=youtube&logoColor=white" alt="video 112s + 35s short"> <img src="https://img.shields.io/badge/uses-fastembed_%C2%B7_lancedb_%C2%B7_pyarrow-2563EB?style=flat-square&logo=python&logoColor=white" alt="fastembed · lancedb · pyarrow"> <img src="https://img.shields.io/badge/topic-data_engineering-0E1525?style=flat-square" alt="data engineering">

**Your chatbot is only as good as the pipeline feeding it.** Three help-center docs, and overnight the refund window
went from 30 days to 14. The ingest job cleans, chunks, hashes and embeds the docs into LanceDB: 6 chunks created on
day one, all 6 skipped on the rerun, and on day two only the 2 chunks of the edited doc are re-embedded. Still 6
rows, all unique, and the answer changes from 30 days to 14.

Watch: [YouTube](https://www.youtube.com/@datanatomyai) · [TikTok](https://www.tiktok.com/@datanatomy.ai) · [Instagram](https://www.instagram.com/datanatomy.ai) (112 seconds, plus a 35-second short)

<br clear="right">

## The idea

Data engineering for RAG is everything before the prompt. Think of a librarian: shelve the new editions, leave the
rest alone. Every night the job runs these steps on each document:

1. **Clean:** drop markdown headings and bold marks, squash the whitespace.
2. **Chunk:** cut the text into 200-character pieces with 40 characters of overlap, so a fact cut at a boundary
   still appears whole in one of the chunks.
3. **Hash:** a SHA-256 of the document's text. If it equals the hash already stored for that source, nothing
   changed: skip it and pay nothing.
4. **Embed and tag:** turn each chunk of a new or changed document into a 384-number vector, and store it with its
   source, its update date, the hash and an id (`file#chunk`).
5. **Upsert on the id:** a known id is updated, a new one inserted, so a rerun never creates duplicates.

## Run it

You need `fastembed`, `lancedb` and `pyarrow` (`pip install fastembed lancedb pyarrow`). The first run downloads
the open embedding model BAAI/bge-small-en-v1.5 (about 64 MB) and caches it.

```bash
python3 src/ingest.py
```

```
run 1: 6 created, 0 re-embedded, 0 skipped
run 2: 0 created, 0 re-embedded, 6 skipped
  refunds.md, 2026-09-01: Refund window: 30 days
run 3: 0 created, 2 re-embedded, 4 skipped
6 rows, 6 unique
  refunds.md, 2026-10-08: Refund window: 14 days
```

The vector store is written to `src/store/`. It is deleted and rebuilt at the start of every run, so the output is
the same each time.

## The short version

The short splits the same pipeline into small functions in `short/pipeline.py` and shows only the nightly loop: read
the stored hashes, keep the documents whose hash changed, embed them, upsert, then ask.

```bash
python3 short/rag.py
```

```
day1: 6 chunks embedded
day1: 0 chunks embedded
day2: 2 chunks embedded
  refunds.md, 2026-10-08: Refund window: 14 days
```

## Files

```
25-data-engineering-for-rag/
├── data/
│   └── docs/
│       ├── day1/             the help center on September 1: refunds.md, shipping.md, warranty.md
│       └── day2/             the export on October 8: same files, refunds.md now says 14 days
├── src/
│   ├── ingest.py             the code from the video
│   ├── kb.py                 loads a day's docs, creates an empty LanceDB table
│   └── store/                the LanceDB vector store, generated, not committed
├── short/
│   ├── rag.py                the 9-line version from the short
│   ├── pipeline.py           the same steps as ingest.py, split into functions
│   ├── kb.py                 same as src/kb.py
│   └── store/                generated, not committed
└── .gitignore                keeps both store/ folders out of git
```

Each doc starts with an `updated: YYYY-MM-DD` line, the way a help-center export would carry its last-edited date.
`kb.py` reads that line into `updated_at` and passes the rest on as the text. The two days are full exports, not
diffs: the job has to work out for itself what changed. The long and short versions read the same `data/docs/`.

## The code

`src/ingest.py`, line by line:

| Line | Code | What it does |
|------|------|--------------|
| 1 to 5 | imports | `re` for cleaning, `Counter` for the totals, `sha256` for hashing, the embedding model, and the two helpers. |
| 7 | `model = TextEmbedding("BAAI/bge-small-en-v1.5")` | An open embedding model that runs locally on the CPU (ONNX). Each text becomes 384 floats. |
| 8 | `table = new_table()` | An empty LanceDB table: id, text, a 384-float vector, source, updated_at, hash. |
| 10 | `def chunk(text, size=200, overlap=40):` | Clean and split one document. |
| 11 | `re.sub(r"(?m)^#.*\|\*", "", text)` | Remove heading lines and the `**` bold marks. They are formatting, not facts. |
| 12 | `re.sub(r"\s+", " ", text).strip()` | Collapse line breaks and runs of spaces into single spaces. |
| 13 | `step = size - overlap` | Each chunk starts 160 characters after the previous one, so neighbours share 40. |
| 14 to 15 | `return [text[i:i + size] for i in range(...)]` | Slice the chunks. Each doc here is 304 to 355 characters, so each gives 2 chunks. |
| 17 | `def ingest(docs, run):` | One nightly run over a full export. |
| 18 to 19 | `old = table.to_arrow().to_pydict()`, `seen = dict(...)` | Read what is already stored: a map from each source file to its hash. |
| 20 | `rows, n = [], Counter()` | Rows to write, and counts of created, re-embedded and skipped chunks. |
| 21 to 22 | `for d in docs:`, `src, parts = ...` | For each document, its name and its chunks. |
| 23 | `h = sha256(d["text"].encode()).hexdigest()` | A fingerprint of the whole document. Any edit changes it. |
| 24 to 26 | `if seen.get(src) == h: ... continue` | Same hash as last time: count its chunks as skipped and move on. No embedding call. |
| 27 to 28 | `n["re-embedded" if src in seen else "created"] += len(parts)` | A known source with a new hash is re-embedded; an unknown one is created. |
| 29 | `for i, v in enumerate(model.embed(parts)):` | Embed all the document's chunks in one call. |
| 30 to 32 | `rows += [{**d, "id": f"{src}#{i}", ...}]` | One row per chunk: the doc's metadata, a stable id like `refunds.md#0`, the chunk text, the hash and the vector. |
| 33 to 37 | `table.merge_insert("id")...execute(rows)` | Upsert on `id`: a row whose id exists replaces it, a new id is inserted. |
| 38 to 40 | `print(...)` | The three counts for this run. |
| 42 to 43 | `def ask(q):`, `v = next(model.query_embed(q))` | Embed the question with the same model, so it lands in the same 384-number space as the chunks. `query_embed` returns a generator, hence `next`. |
| 44 | `hit = table.search(v).limit(1).to_list()[0]` | The nearest chunk by vector distance. |
| 45 to 47 | `fact = ...`, `meta = ...`, `print(...)` | Print its first sentence with the source and date it came from. |
| 49 | `ingest(load("day1"), 1)` | Day one: 6 chunks created. |
| 50 | `ingest(load("day1"), 2)` | The nightly rerun on the same export: all 6 skipped. |
| 51 | `ask(...)` | 30 days, from refunds.md dated 2026-09-01. |
| 52 | `ingest(load("day2"), 3)` | Day two: refunds.md has a new hash, so its 2 chunks are re-embedded; the other 4 are skipped. |
| 53 to 54 | `ids = ...`, `print(...)` | 6 rows, 6 unique ids: the upsert replaced the old refund chunks instead of adding new ones. |
| 55 | `ask(...)` | 14 days, dated 2026-10-08. |

`kb.py` has two helpers. `load(day)` reads every `.md` file in `data/docs/<day>/` and returns a list of dicts with
`source`, `text` and `updated_at`. `new_table()` deletes `src/store/` and creates the empty `chunks` table with a
fixed PyArrow schema, so the vector column is known to hold exactly 384 floats. Both find their folders from
`__file__`, so you can run the lesson from any directory.

## The hash check is your embedding bill

Here, 4 of 6 chunks were skipped on day two. In a real help center or wiki, most documents do not change on a given
night, so hashing first means you embed (and pay for, and wait for) only the small part that did. Two details make it
work: the hash is computed on the document, so one edit re-embeds all of that document's chunks and nothing else; and
the chunk id is stable (`refunds.md#0`), so the upsert replaces the old vector instead of leaving a stale "30 days"
next to the new "14 days". Without the upsert, the second ask could still return the old answer.

## What the video skips

- **Deleted documents.** If a file disappears from the export, its chunks stay in the table. Production jobs also
  delete rows whose source is gone.
- **Shrinking documents.** If refunds.md got shorter and produced 1 chunk instead of 2, the upsert would update
  `refunds.md#0` and leave the old `refunds.md#1` behind. A common fix: delete all rows for a changed source, then
  insert its new chunks.
- **Access rules.** Real knowledge bases tag each chunk with who may see it and filter on that at query time.
- **Chunking.** Fixed 200-character windows cut words in half. Real pipelines usually split on sentences, paragraphs
  or headings, and size chunks in tokens.

## Try this

1. Change the overlap to 0. How many chunks does each document give now, and does the refund question still find
   the right chunk?
2. Edit only `data/docs/day2/shipping.md` as well (say, free shipping over $40). What does run 3 print now?
3. Delete `data/docs/day2/warranty.md` and run again. How many rows are in the table at the end, and why is that a
   problem?
4. Change the size to 100. How many chunks are created on day one, and what does `ask` print?

---
Previous: [24 · Lake vs warehouse vs lakehouse](../24-lake-vs-warehouse-vs-lakehouse) · Next: [26 · Batch vs streaming](../26-batch-vs-streaming) · [All lessons](../../README.md)
