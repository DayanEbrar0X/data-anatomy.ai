# 15 · Idempotent pipelines

<img src="https://img.shields.io/badge/level-beginner-047857?style=flat-square" alt="beginner"> <img src="https://img.shields.io/badge/video-86s_%2B_34s_short-7C3AED?style=flat-square&logo=youtube&logoColor=white" alt="video 86s + 34s short"> <img src="https://img.shields.io/badge/uses-duckdb-2563EB?style=flat-square&logo=python&logoColor=white" alt="duckdb"> <img src="https://img.shields.io/badge/topic-data_engineering-0E1525?style=flat-square" alt="data engineering">

**Your job failed halfway. You reran it. Revenue just doubled.** A nightly job loads 8 orders for Oct 7 into a
warehouse that already holds Oct 6, then crashes before it can publish the report, so the scheduler reruns it. The
naive load appends the same orders again: Oct 7 shows $4,100 in 16 rows. The idempotent load rewrites the day:
$2,050 in 8 rows, the real number. Oct 6 stays at $1,730 both times.

Watch: [YouTube](https://www.youtube.com/@datanatomyai) · [TikTok](https://www.tiktok.com/@datanatomy.ai) · [Instagram](https://www.instagram.com/datanatomy.ai) (86 seconds, plus a 34-second short)

<br clear="right">

## The idea

An operation is **idempotent** when running it once or five times gives the same result. Pipelines need this
because reruns are normal: schedulers retry failed jobs, and backfills rerun old days on purpose.

The naive load is one `INSERT`. It appends whatever it gets and never checks whether those rows are already there.
The idempotent load treats the day as a **partition**, a slice of the table it owns completely:

1. **Begin** a transaction, so the next two steps happen all together or not at all.
2. **Delete** every row for that day.
3. **Insert** the day's rows fresh.
4. **Commit.**

Rerun it and the day is rewritten, never added to. The other common pattern is a **merge** (upsert) on a key:
update the rows whose key already exists and insert the rest.

## Run it

You need `duckdb` (`pip install duckdb`).

```bash
python3 src/load.py
```

```
naive: crashed at step 2
naive: rerun ok
naive: Oct 7 $4,100 (16 rows), Oct 6 $1,730
idempotent: crashed at step 2
idempotent: rerun ok
idempotent: Oct 7 $2,050 (8 rows), Oct 6 $1,730
```

### The short version

The short (`short/rerun.py`, 9 lines) moves the naive load and the crash-and-rerun harness into its `job.py`, so
the screen holds only the idempotent load and the two runs. Same data, same numbers:

```bash
python3 short/rerun.py
```

```
naive: Oct 7 $4,100 (16 rows), Oct 6 $1,730
idempotent: Oct 7 $2,050 (8 rows), Oct 6 $1,730
```

## Files

```
15-idempotent-pipelines/
├── data/
│   ├── history.csv       6 orders for Oct 6, already in the warehouse ($1,730)
│   └── orders.csv        tonight's 8 orders for Oct 7 ($2,050)
├── src/
│   ├── load.py           the code from the video
│   └── job.py            the warehouse, the two-step job and the report
└── short/
    ├── rerun.py          the 9-line version from the short
    └── job.py            same data, plus the naive load and crash_and_rerun()
```

The warehouse is an in-memory DuckDB database, rebuilt from `history.csv` for each load, so nothing is written to
disk and every run starts clean. The long and short versions read the same two files in `data/`.

## The code

`src/load.py`, line by line:

| Line | Code | What it does |
|------|------|--------------|
| 1 | `from job import warehouse, run_job, report` | The harness: a fresh warehouse, the job that runs a load, and the report. |
| 3 to 5 | `def naive(db, day, rows): db.executemany("INSERT ...", rows)` | The naive load: one insert of every row. It ignores `day` and never looks at what is already there. |
| 7 | `def idempotent(db, day, rows):` | Same signature, so the job can run either one. |
| 8 | `db.begin()  # all or nothing` | Start a transaction. Nothing below is visible or permanent until the commit. |
| 9 to 10 | `db.execute("DELETE FROM revenue WHERE day = ?", [day])` | Remove everything already loaded for this day. On the first run there is nothing to remove. |
| 11 | `naive(db, day, rows)` | Then the very same insert as the naive load. |
| 12 | `db.commit()` | Make the delete and the insert permanent together. |
| 14 | `for load in (naive, idempotent):` | Test both loads the same way. |
| 15 | `db = warehouse()  # already holds Oct 6` | A fresh DuckDB warehouse with the 6 Oct 6 rows. |
| 16 | `run_job(db, load, crash=True)` | Run 1: step 1 (the load) finishes, step 2 (publish) crashes. |
| 17 | `run_job(db, load)  # the rerun` | The scheduler reruns the whole job, load included. |
| 18 | `report(db, load.__name__)` | Rows and revenue for Oct 7, and the Oct 6 total. |

`job.py` creates the `revenue` table (`day`, `id`, `usd`), reads the CSVs from `data/`, and runs the job: step 1
calls the load you pass in, and with `crash=True` it prints the crash and returns before step 2. `report()` runs
`count(*)` and `sum(usd)` for Oct 7 and `sum(usd)` for Oct 6.

## The gotcha: one transaction

The delete and the insert must share one transaction. Without `begin()` and `commit()`, DuckDB commits each
statement on its own. If the job dies after the delete and before the insert, the day is left empty: no rows for Oct
7 at all, which is arguably worse than doubled, because nothing looks broken until someone reads the report. Inside
a transaction, a crash before the commit leaves the old rows in place.

## What the video simplified

- **The crash is polite.** `run_job` prints "crashed" and returns. A real failure raises an error, and the
  scheduler starts a new process for the retry. The lesson is the same: whatever step 1 committed is still there.
- **The load trusts the day.** `idempotent` deletes `day = '2026-10-07'` but inserts every row it is given. If a row
  for another day sneaks in (a late order from Oct 6), it is appended on every rerun, and the Oct 6 total drifts.
  The partition you delete must match the rows you insert.
- **Production versions of the same idea.** Warehouses and table formats offer it built in: `MERGE` on a key,
  overwriting one partition (`INSERT OVERWRITE` in Spark SQL and Hive), or a write that replaces the rows matching a
  filter. The rule is the same in all of them: the output depends only on the input, never on how many times the
  job ran.

## Try this

1. Call `run_job(db, load)` two more times inside the loop. How many Oct 7 rows does each load end with?
2. Add a late order for the previous day to `data/orders.csv`: `2026-10-06,997,100`. What does the Oct 6 total
   become for each load, and why does the idempotent load not protect it?
3. Remove `db.begin()` and `db.commit()`, then simulate a crash between the delete and the insert (call only the
   `DELETE` and stop). How many Oct 7 rows are left?
4. Write a third load that merges on `id` instead of deleting the day, with DuckDB's
   `MERGE INTO revenue USING incoming ON revenue.id = incoming.id`. Is it still idempotent if you run it three times?
   What happens when an order's `usd` changes between runs?

---
Previous: [14 · Why Polars is fast](../14-polars) · Next: [16 · Apache Iceberg](../16-apache-iceberg) · [All lessons](../../README.md)
