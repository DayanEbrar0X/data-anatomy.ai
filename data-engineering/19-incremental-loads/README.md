# 19 · Incremental loads

<img src="https://img.shields.io/badge/level-intermediate-B45309?style=flat-square" alt="intermediate"> <img src="https://img.shields.io/badge/video-118s_%2B_36s_short-7C3AED?style=flat-square&logo=youtube&logoColor=white" alt="video 118s + 36s short"> <img src="https://img.shields.io/badge/uses-duckdb-2563EB?style=flat-square&logo=python&logoColor=white" alt="duckdb"> <img src="https://img.shields.io/badge/topic-data_engineering-0E1525?style=flat-square" alt="data engineering">

**You reload a million rows to pick up 200 changes.** An incremental load reads only what changed since the last
run, like a bookmark. We load 1,000,000 orders, change 200 of them (one arrives late), and compare three loads. The
full reload reads 1,000,050 rows. A plain watermark reads 199 and misses the late order. A watermark with a one hour
lookback reads 1,588, writes 200, and matches the source exactly.

Watch: [YouTube](https://www.youtube.com/@datanatomyai) · [TikTok](https://www.tiktok.com/@datanatomy.ai) · [Instagram](https://www.instagram.com/datanatomy.ai) (118 seconds, plus a 36-second short)

<br clear="right">

## The idea

Every row in the source has an `updated_at` time. After each load you save the newest time you loaded: the
**high-watermark**. The next run starts there.

1. **Read** the rows with `updated_at` after the watermark, minus a **lookback** window, so rows that arrive late
   (stamped before the mark, but landing after the load) are still picked up.
2. **Merge** them into the warehouse on the key: update a row only if the incoming copy is newer, insert rows that
   are new. Rows you read twice change nothing.
3. **Move the watermark** up to the newest row you now hold.

The work now grows with the number of changes, not with the size of the table.

## Run it

You need `duckdb` 1.4 or newer, for `MERGE INTO` (`pip install duckdb`). Everything runs in memory, no files:

```bash
python3 src/load.py
```

```
full: read 1,000,050, wrote 1,000,050, match True
watermark: read 199, wrote 199, match False
lookback 1h: read 1,588, wrote 200, match True
```

`match` compares the warehouse table with the source, row by row. Tested with DuckDB 1.5.4; it takes about two
seconds.

### The short version

The short (`short/incremental.py`, 9 lines) runs only the winning strategy: a one hour lookback, then the merge.

```bash
python3 short/incremental.py
```

```
lookback 1h: read 1,588, wrote 200, match True
```

## Files

```
19-incremental-loads/
├── src/
│   ├── load.py           the code from the video: three loads, side by side
│   └── orders.py         the source and the warehouse: night_one(), day_two(), report()
└── short/
    ├── incremental.py    the 9-line version from the short
    └── orders.py         same as src/orders.py
```

There is no data folder: `orders.py` builds the data inside DuckDB with SQL, so every run starts from the same
million rows.

- `night_one()` creates `src` with 1,000,000 orders spread over 30 days (Sep 8 to Oct 8, 00:00), copies all of them
  into the warehouse table `wh`, and saves the newest `updated_at` in a one-row `state` table: the watermark,
  Oct 8 00:00.
- `day_two()` makes 200 changes in the source: 150 updates and 49 new orders during Oct 8, plus one late arrival, an
  order stamped Oct 7 23:40 from a phone that was offline.
- `report()` prints the counts and checks that `wh` and `src` hold exactly the same rows.

## The code

`src/load.py`, line by line:

| Line | Code | What it does |
|------|------|--------------|
| 1 | `from orders import night_one, day_two, report` | The setup and the check. |
| 3 | `def full(db, _):` | The full reload. It ignores the lookback argument. |
| 4 to 5 | `CREATE OR REPLACE TABLE wh AS FROM src` | Throw the warehouse table away and copy the whole source. `FROM src` is DuckDB shorthand for `SELECT * FROM src`. The statement returns the number of rows it wrote. |
| 6 | `return n, n` | Read everything, wrote everything. |
| 8 | `def incremental(db, minutes):` | The incremental load, with a lookback in minutes. |
| 9 to 10 | `CREATE TABLE new AS FROM src WHERE updated_at > (SELECT wm` | Copy only the rows newer than the stored watermark into a staging table, `new`. |
| 11 to 12 | `FROM state) - INTERVAL (?) MINUTE""", [minutes]` | Minus the lookback. `?` is a query parameter, filled with `minutes` (0 or 60). |
| 13 to 14 | `MERGE INTO wh USING new USING (id)` | Merge the staged rows into the warehouse. The first `USING` names the source table; `USING (id)` matches rows on the order id. |
| 14 to 16 | `WHEN MATCHED AND new.updated_at > wh.updated_at THEN UPDATE` | An existing order is overwritten only if the incoming copy is newer. Rows the lookback re-read are skipped. |
| 16 | `WHEN NOT MATCHED THEN INSERT` | New orders, and the late one, are inserted. |
| 17 | `.fetchone()[0]` | `MERGE` returns how many rows it changed: the "wrote" number. |
| 18 to 19 | `UPDATE state SET wm = (SELECT max(updated_at) FROM wh)` | Move the watermark to the newest row in the warehouse. The next run starts here. |
| 20 | `return read, wrote` | |
| 22 to 25 | `for name, load, minutes in [...]` | Three runs: full, watermark only (lookback 0), and a one hour lookback. |
| 26 | `db = night_one()` | Each run starts from a fresh copy of last night: 1M rows loaded, watermark saved. |
| 27 | `day_two(db)` | Today's 200 changes land in the source. |
| 28 | `report(db, name, *load(db, minutes))` | Run the load, then print what it read, what it wrote, and whether the warehouse matches the source. |

Where the numbers come from:

- **Watermark only** reads the 199 rows stamped after Oct 8 00:00. The late order is stamped 23:40, before the
  watermark, so it is never read, and after this run the watermark moves to Oct 8 15:59. No later run will see it.
- **Lookback 1h** reads everything after Oct 7 23:00: the same 199, the late order, and 1,388 orders from the last
  hour of night one that are already in the warehouse, unchanged. `MERGE` writes the 200 real changes and skips
  the 1,388.

## Why always MERGE

The lookback only works because the write is a `MERGE` on the key. With a plain `INSERT`, the 1,388 re-read rows
would become duplicates. With the merge, reading a row twice is harmless, so you can make the lookback as wide as
your latest data needs, and you can rerun a failed load without cleaning up first (lesson
[15 · Idempotent pipelines](../15-idempotent-pipelines) covers that idea).

Size the lookback from real data: how late do rows arrive in your source? Mobile apps, batch exports from partners
and replicas that lag behind all produce late rows. Too small and you miss them silently, as the watermark-only run
shows; too large and you re-read more than you need, which costs time but not correctness.

## What the video simplified

- **Deletes are invisible.** A deleted row has no `updated_at` to compare, so no watermark query can find it. Run a
  full reload now and then (weekly, for example) to catch them, or use change data capture
  ([17 · Change data capture](../17-change-data-capture)), which reads the database log and sees deletes.
- **One database for everything.** Here the source, the warehouse and the watermark all live in the same in-memory
  DuckDB database. In production the extract query runs on the source system (where `updated_at` should be
  indexed), the rows land in a staging table in the warehouse, and the watermark is saved in the same transaction
  as the merge, so a crash cannot move the mark without the data.
- **`updated_at` must be trustworthy.** The method assumes every write to the source updates `updated_at`. If one
  code path forgets, those changes are never loaded. Check how your source sets it before you rely on it.

## Try this

1. Change the lookback from 60 to 30 minutes, then to 15. Does each run still match the source? Why does one of
   them fail?
2. Delete a row in `day_two()`: `db.sql("DELETE FROM src WHERE id = 7")`. Which of the three runs still match?
3. Remove `AND new.updated_at > wh.updated_at` from the merge. How many rows does the lookback run write now, and
   does it still match?
4. Change line 9 to `CREATE OR REPLACE TABLE new` and call `incremental(db, 60)` twice on the same database. What
   does the second run read and write, and why is that safe?

---
Previous: [18 · SCD Type 2](../18-scd-type-2) · Next: [20 · Medallion architecture](../20-medallion-architecture) · [All lessons](../../README.md)
