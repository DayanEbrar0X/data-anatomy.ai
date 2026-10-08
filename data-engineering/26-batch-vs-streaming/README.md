# 26 · Batch vs streaming

<img src="https://img.shields.io/badge/level-beginner-047857?style=flat-square" alt="beginner"> <img src="https://img.shields.io/badge/video-107s_%2B_39s_short-7C3AED?style=flat-square&logo=youtube&logoColor=white" alt="video 107s + 39s short"> <img src="https://img.shields.io/badge/uses-standard_library-2563EB?style=flat-square&logo=python&logoColor=white" alt="standard library"> <img src="https://img.shields.io/badge/topic-data_engineering-0E1525?style=flat-square" alt="data engineering">

**Some data can't wait for the nightly job.** One day of card swipes and one fraud rule: three swipes in 60
seconds, from two countries. The nightly batch job flags card 4417 eleven hours and 52 minutes after the swipe, when
$4,202 has been spent. The streaming version runs the same rule on each swipe as it arrives and flags it 2 seconds
after the swipe, at $1,442.

Watch: [YouTube](https://www.youtube.com/@datanatomyai) · [TikTok](https://www.tiktok.com/@datanatomy.ai) · [Instagram](https://www.instagram.com/datanatomy.ai) (107 seconds, plus a 39-second short)

<br clear="right">

## The idea

Batch is the morning paper. Streaming is the alert on your phone.

- **Batch** waits until the data is complete, then processes all of it in one job. Here: one run at 02:00 over the
  whole day.
- **Streaming** processes each event as it lands. Here: a minimal simulation of a Kafka-style topic, which is an
  append-only log where every event gets an offset (its position: 0, 1, 2, ...).

The streaming loop has three parts:

1. **Producer:** appends each swipe to the topic.
2. **Consumer:** reads the event at its current offset and runs the rule.
3. **Commit:** saves the offset it has finished, so after a crash it resumes from there instead of starting over.

The rule itself is the same in both: keep a small window of recent swipes per card, drop the ones older than 60
seconds, and flag the card if three or more are left from two or more countries.

## Run it

```bash
python3 src/stream.py
```

```
batch: card 4417 flagged after 11:51:55
  $4,202 spent before the alert
stream: card 4417 flagged after 0:00:02
  $1,442 spent before the alert
committed offset: 12
```

No packages to install: it uses only the Python standard library.

## The short version

The short (`short/fraud.py`, 9 lines) drops the topic and the offsets. It runs the same rule twice, swipe by swipe
for streaming and over the whole day for batch, so the streaming alert prints first:

```bash
python3 short/fraud.py
```

```
stream: card 4417 flagged after 0:00:02
  $1,442 spent before the alert
batch: card 4417 flagged after 11:51:55
  $4,202 spent before the alert
```

## Files

```
26-batch-vs-streaming/
├── data/
│   └── swipes.csv        12 card swipes on 2026-10-08: time, card, country, usd
├── src/
│   ├── stream.py         the code from the video
│   └── swipes.py         loads swipes.csv, the 02:00 batch slot, the alert report
└── short/
    ├── fraud.py          the 9-line version from the short
    └── swipes.py         same as src/swipes.py, plus the rule and the delay from stream.py
```

`swipes.csv` is small enough to read in full. Card 7731 swipes three times inside a minute in the morning, but all in
the US, so the rule leaves it alone. Card 4417 swipes in the US at 14:07:12, then in the UK at 14:07:39 and 14:08:05:
that third swipe trips the rule. Later UK swipes ($700, $1,200, $860) are the money a late alert lets through. The
long and short versions read the same `data/swipes.csv`.

## The code

`src/stream.py`, line by line:

| Line | Code | What it does |
|------|------|--------------|
| 1 to 3 | imports | `deque` for the per-card window, `timedelta` for durations, and the swipes, the 02:00 slot and the report. |
| 5 | `WINDOW = timedelta(seconds=60)` | How far back the rule looks. |
| 6 | `LAG = timedelta(seconds=2)` | A simulated delivery delay: the time from swipe to the consumer seeing it. |
| 8 | `def suspicious(win, e):` | The fraud rule. `win` holds one window per card; `e` is the new swipe. |
| 9 to 10 | `w = win.setdefault(e.card, deque())`, `w.append(e)` | Get this card's window (create it on first sight) and add the swipe. |
| 11 to 12 | `while e.ts - w[0].ts > WINDOW: w.popleft()` | Drop swipes more than 60 seconds older than this one. |
| 13 | `countries = {x.country for x in w}` | The distinct countries in the window. |
| 14 | `return len(w) >= 3 and len(countries) >= 2` | Three or more swipes, two or more countries: suspicious. |
| 16 to 20 | `win = {}`, `for e in day: ... report("batch", e, NIGHTLY)` | Batch: one pass over the whole day. The rule fires on the 14:08:05 swipe, but the job only runs at 02:00, so that is when the alert happens. |
| 23 | `topic, committed, win = [], 0, {}` | An empty topic, offset 0, fresh windows. |
| 24 | `for e in day:` | Swipes arrive live, one at a time. |
| 25 | `topic.append(e)` | The producer writes the swipe to the end of the log. |
| 26 | `e = topic[committed]` | The consumer reads the event at its committed offset. |
| 27 to 28 | `if suspicious(win, e): report("stream", e, e.ts + LAG)` | Same rule. The alert happens 2 seconds after the swipe. |
| 29 | `committed += 1` | Commit: this offset is done. |
| 30 | `print("committed offset:", committed)` | 12: all twelve swipes processed. |

`swipes.py` reads `data/swipes.csv` into a list of `Swipe(ts, card, country, usd)` tuples in event-time order, sets
`NIGHTLY` to 02:00 the next morning, and defines `report(mode, e, found)`. `report` prints how long after the swipe
the alert came (`found - e.ts`) and adds up everything that card spent up to the moment of the alert. In `short/`,
`swipes.py` also holds `suspicious`, `WINDOW` and `LAG`, copied from `stream.py`, so the short's file stays at 9 lines.

## What the simulation leaves out

In the loop, the producer and the consumer take turns in one Python process, so the consumer is never behind and the
"2 seconds" is a number we chose, not a measurement. In production:

- **Kafka** (or a similar log such as Kinesis or Pub/Sub) holds the topic on disk, replicated across machines. Producers
  and consumers are separate programs, and the consumer can fall behind and catch up.
- **Flink** (or Spark Structured Streaming, Kafka Streams) runs the windows. The window state is checkpointed together
  with the offsets, so after a restart the job does not lose or double-count swipes. Here the window is a dict in
  memory and is lost on a crash.
- **Event time vs arrival time.** Events can arrive late or out of order. Streaming engines use watermarks to decide
  how long to wait for stragglers. This data arrives in perfect order.

## Batch still wins, often

Batch is cheaper, simpler and easy to rerun: if the rule had a bug, fix it and run the day again. Reports, monthly
aggregates and backfills of history are batch jobs in most companies. Streaming costs always-on infrastructure and
harder failure handling, so it is worth it when the answer loses value by the minute. The question to ask is how late
is too late. For fraud, 2 seconds beats almost 12 hours.

## Try this

1. Change `WINDOW` to 20 seconds. Is card 4417 still flagged? Why?
2. Change `LAG` to 5 minutes. How much has the card spent before the streaming alert now?
3. Move `NIGHTLY` to 2026-10-08 18:00 (an evening batch run). What does the batch line print?
4. Add a swipe `09:13:30,7731,CA,25` to `swipes.csv`. Which cards are flagged, by which pipeline, and how many
   times?

---
Previous: [25 · Data engineering for RAG](../25-data-engineering-for-rag) · Next: [Build Lab 02 · Documents to data](../build-lab-02-documents-to-data) · [All lessons](../../README.md)
