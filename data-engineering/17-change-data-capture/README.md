# 17 · Change data capture

<img src="https://img.shields.io/badge/level-intermediate-B45309?style=flat-square" alt="intermediate"> <img src="https://img.shields.io/badge/video-127s_%2B_39s_short-7C3AED?style=flat-square&logo=youtube&logoColor=white" alt="video 127s + 39s short"> <img src="https://img.shields.io/badge/uses-standard_library-2563EB?style=flat-square&logo=python&logoColor=white" alt="standard library"> <img src="https://img.shields.io/badge/topic-data_engineering-0E1525?style=flat-square" alt="data engineering">

**Your nightly job missed 3 updates. CDC catches every one.** An orders table takes six writes in one day: an
insert, four updates and a delete. A nightly job that compares last night's snapshot with tonight's sees only where
each order ended up, so it never sees `paid`, `cancelled` or `shipped`. Change data capture (CDC) records every write
in order, replays all six into a copy, and the copy matches the source.

Watch: [YouTube](https://www.youtube.com/@datanatomyai) · [TikTok](https://www.tiktok.com/@datanatomy.ai) · [Instagram](https://www.instagram.com/datanatomy.ai) (127 seconds, plus a 39-second short)

<br clear="right">

## The idea

A nightly diff is two photos of a parking lot: you see which cars are new and which are gone, never who came and
went in between. CDC is the security camera: it records every car, in order.

1. **Snapshot diff:** read the whole table last night and again tonight, and keep the rows that differ. You get the
   end state of each changed row.
2. **CDC:** every write the database makes is also written to a log (in a real database, the write-ahead log). A CDC
   tool reads that log and gets every insert, update and delete, in the order they happened.
3. **Replay:** apply the log to a copy of the table, in order. Inserts and updates become an upsert, deletes become
   deletes. The copy ends up identical to the source, and you also kept every step on the way.

Here SQLite triggers stand in for the write-ahead log: each write to `orders` appends a row to a `changes` table.

## Run it

Only the Python standard library (`sqlite3`) is needed.

```bash
python3 src/cdc.py
```

```
changes today: 6
diff missed: paid, cancelled, shipped
target matches source: True
nightly diff: 3 of 6 | cdc: 6 of 6
```

## The short version

The 39-second short builds the same source, triggers and day of writes, but moves the trigger setup, the snapshot and
the diff into helpers (`short/shop.py`), so the on-screen file is 9 lines and prints only the final comparison:

```bash
python3 short/cdc.py
```

```
nightly diff: 3 of 6 | cdc: 6 of 6
```

## Files

```
17-change-data-capture/
├── data/
│   ├── orders.csv        the table before the day starts: orders 1 and 2, both 'new'
│   └── day.sql           the day's six writes, in order
├── src/
│   ├── cdc.py            the code from the video
│   └── shop.py           builds the source and target databases, loads data/
└── short/
    ├── cdc.py            the 9-line version from the short
    └── shop.py           same data, plus triggers(), snap() and diff()
```

The starting rows and the day's writes are data, so they live in `data/` and both versions read the same files. Both
databases are in memory, so nothing is written to disk and every run starts clean.

## The code

`src/cdc.py`, line by line:

| Line | Code | What it does |
|------|------|--------------|
| 1 | `from shop import source, target, DAY` | The source database builder, the target builder, and the day's writes as one SQL script. |
| 3 | `src = source()` | An in-memory SQLite database with `orders` (1 and 2, both `new`) and an empty `changes` table. |
| 4 | `SNAP = "SELECT id, status FROM orders"` | The query a snapshot job runs. |
| 5 | `yday = dict(src.execute(SNAP))` | Last night's snapshot: `{1: 'new', 2: 'new'}`. |
| 7 to 10 | `for op, row in [...]` | One entry per kind of write. Inserts and updates log the new row (`NEW.id, NEW.status`); a delete logs the old id and no status. |
| 11 to 14 | `src.execute(f"""CREATE TRIGGER log_{op} ...""")` | Three triggers. After every insert, update or delete on `orders`, SQLite appends `(op, id, status)` to `changes`. This is the stand-in for the write-ahead log. |
| 16 | `src.executescript(DAY)` | The day runs: insert order 3, order 1 goes paid, shipped, delivered, order 2 is cancelled and then deleted. |
| 19 | `night = dict(src.execute(SNAP))` | Tonight's snapshot: `{1: 'delivered', 3: 'new'}`. |
| 20 to 21 | `diff = {k: night.get(k) ... if yday.get(k) != night.get(k)}` | The nightly job: every id whose value differs. `{1: 'delivered', 2: None, 3: 'new'}`, where `None` means deleted. |
| 24 to 26 | `log = list(src.execute("... ORDER BY seq"))` | CDC reads the log in the order it was written. `seq` is an `INTEGER PRIMARY KEY`, so it counts up with each change. |
| 27 | `tgt = target(yday)` | The copy downstream, starting from last night's state. |
| 28 to 29 | `UPSERT = ("INSERT ... ON CONFLICT(id) DO UPDATE SET status=?")` | Insert the row, or update it if the id already exists. One statement for both inserts and updates. |
| 30 | `DELETE = "DELETE FROM orders WHERE id = ?"` | Deletes stay deletes. |
| 31 to 35 | `for op, k, st in log: ...` | Replay every change, in order. |
| 37 | `missed = [s for _, k, s in log if diff[k] != s]` | Every status the log saw that the diff does not show: `paid`, `cancelled`, `shipped`. |
| 38 to 39 | prints | Six changes today, and what the diff missed. |
| 40 to 41 | `same = dict(tgt.execute(SNAP)) == night` | After the replay, the target holds exactly what the source holds. |
| 42 to 43 | `print(f"nightly diff: ...")` | The diff saw 3 changed rows. The log has all 6 changes. |

`shop.py` reads `data/orders.csv` and `data/day.sql` (paths resolved from its own location), creates the `orders`
table with `id` as the primary key, and creates the `changes` table. `target(rows)` makes a second in-memory database
with the same `orders` table, filled from a snapshot dict.

## What the diff gets right, and what it cannot see

The diff is not useless: it does find all three orders that changed, including the delete (order 2 shows up as
`None`). What it cannot see is anything in between. Order 1 went `paid`, `shipped`, `delivered`; the diff sees only
`delivered`. Order 2 was cancelled before it was deleted; the diff has no trace of the cancel. So if someone asks how
many orders were cancelled today, the diff answers zero. A row that is inserted and deleted on the same day is
invisible to it altogether (try exercise 2).

The `3 of 6` compares changed rows with logged changes, so it is a fair summary of the gap, not a count of identical
things.

## In production

- **Debezium** is the common open-source CDC tool. It reads the database's own change log (logical decoding of the
  write-ahead log in Postgres, the binlog in MySQL) and streams every change to Kafka. Nothing is added to the
  application's transactions.
- **Triggers work, but they cost.** Every write now also writes a row to `changes`, inside the same transaction. That
  is fine for a demo or a small table, and real overhead on a busy one.
- **The gotcha: replay in order per key.** If two changes to the same order arrive out of order, `delivered` turns
  back into `shipped`. Kafka keeps order within a partition, so CDC pipelines partition by the primary key. Try
  exercise 1 to see what happens when the order is wrong.
- **Deletes need care.** Here the delete carries only the id. Real CDC events usually carry the row before and after
  the change, and downstream tables often keep a "deleted" flag rather than removing the row.

## Try this

1. Change line 26 to `"ORDER BY seq DESC"` to replay the log backwards. Does the target still match the source?
   Which status does order 1 end with?
2. Add two lines to the end of `data/day.sql`: `INSERT INTO orders VALUES (4, 'new');` and
   `DELETE FROM orders WHERE id=4;`. What does line 37 do now, and what does that tell you about the diff?
3. Add `UPDATE orders SET status='delivered' WHERE id=1;` to `data/day.sql` (a write that changes nothing). Does
   the log grow? How would you change the UPDATE trigger so it logs only real changes? (Hint: SQLite triggers accept
   `WHEN OLD.status IS NOT NEW.status`.)
4. Replay the log twice into the same target. Is the result still correct? What makes this replay safe to repeat?

---
Previous: [16 · Apache Iceberg](../16-apache-iceberg) · Next: [18 · SCD Type 2](../18-scd-type-2) · [All lessons](../../README.md)
