# 16 · Apache Iceberg

<img src="https://img.shields.io/badge/level-intermediate-B45309?style=flat-square" alt="intermediate"> <img src="https://img.shields.io/badge/video-113s_%2B_34s_short-7C3AED?style=flat-square&logo=youtube&logoColor=white" alt="video 113s + 34s short"> <img src="https://img.shields.io/badge/uses-pyiceberg_%C2%B7_pyarrow-2563EB?style=flat-square&logo=python&logoColor=white" alt="pyiceberg · pyarrow"> <img src="https://img.shields.io/badge/topic-data_engineering-0E1525?style=flat-square" alt="data engineering">

**A folder of Parquet files can't undo a mistake. This table can.** We append 8 orders to an Iceberg table, then a
buggy job overwrites the whole table with 3 of them. Right now the table holds 3 rows, $545. Snapshot 1 still reads
8 rows, $2,050, and one rollback makes the table whole again. Nothing was deleted on disk: only a pointer moved.

Watch: [YouTube](https://www.youtube.com/@datanatomyai) · [TikTok](https://www.tiktok.com/@datanatomy.ai) · [Instagram](https://www.instagram.com/datanatomy.ai) (113 seconds, plus a 34-second short)

<br clear="right">

## The idea

Apache Iceberg is an open **table format**: a set of rules for turning a folder of data files into a table with a
history. Think of it like Git for a table.

1. **Data files.** The rows stay in plain Parquet files. They are never edited in place.
2. **Snapshots.** Every write is a commit, called a snapshot. A snapshot lists exactly which data files make up the
   table at that moment.
3. **Metadata.** A metadata file (JSON) records the schema, every snapshot, and which snapshot is current.
4. **Catalog.** The catalog stores one thing per table: where the current metadata file is. A commit writes a new
   metadata file, then swaps that pointer, all at once.

Because old snapshots keep pointing at old files, you can read the table as it was (**time travel**) or make an old
snapshot current again (**rollback**). Because a commit is a single pointer swap, readers see the table before the
write or after it, never halfway.

## Run it

You need PyIceberg with its PyArrow and SQLite extras (`pip install "pyiceberg[pyarrow,sql-sqlite]"`). The catalog
is a SQLite file and the warehouse is a local folder, so there is no server, Spark or Java to set up.

```bash
python3 src/iceberg.py
```

```
snap 1 append: 8 rows
snap 2 delete: 0 rows
snap 3 append: 3 rows
now: 3 rows, $545
snap 1: 8 rows, $2,050
rolled back: 8 rows, $2,050
```

Each run deletes and recreates `src/lake.db` and `src/warehouse/`, so it always starts from an empty table. Tested
with PyIceberg 0.12.0 and PyArrow 18.1.0.

### The short version

The short (`short/undo.py`, 9 lines) skips the snapshot listing and time travel: append, overwrite, print, roll
back, print. Its `lake.py` returns the empty table directly.

```bash
python3 short/undo.py
```

```
now: 3 rows, $545
rolled back: 8 rows, $2,050
```

## Files

```
16-apache-iceberg/
├── data/
│   └── orders.csv        tonight's 8 orders for Oct 7 ($2,050)
├── src/
│   ├── iceberg.py        the code from the video
│   ├── lake.py           a fresh SQLite catalog + warehouse folder, the orders, and total()
│   ├── lake.db           generated: the catalog, not committed
│   └── warehouse/        generated: the table's Parquet and metadata files, not committed
├── short/
│   ├── undo.py           the 9-line version from the short
│   └── lake.py           same, but table() also creates the table
└── .gitignore            keeps lake.db and warehouse/ out of git
```

`lake.py` finds `data/orders.csv` and creates `lake.db` and `warehouse/` next to itself, so the lesson runs from any
folder. After one run of `src/iceberg.py`, `src/warehouse/shop/orders/` holds:

- `data/`: 2 Parquet files, one with the 8 orders and one with the 3 the buggy job kept. The 8-row file is still
  there after the overwrite.
- `metadata/`: 4 `*.metadata.json` files (table created, append, overwrite, rollback), plus Avro files: a manifest
  list per snapshot (`snap-*.avro`) and manifests (`*-m0.avro`) that list the data files.

## The code

`src/iceberg.py`, line by line:

| Line | Code | What it does |
|------|------|--------------|
| 1 | `from lake import catalog, orders, total` | A fresh catalog, the 8 orders as a PyArrow table, and a helper that prints rows and revenue. |
| 3 | `cat = catalog()  # SQLite catalog + local folder` | PyIceberg's `SqlCatalog`, backed by `lake.db`, with a `shop` namespace. |
| 4 to 5 | `t = cat.create_table("shop.orders", schema=orders.schema)` | An empty Iceberg table whose schema comes from the Arrow table: `day`, `id`, `usd`. |
| 6 | `t.append(orders)` | Write the 8 orders to a new Parquet file and commit. Snapshot 1. |
| 8 | `bad = orders.slice(0, 3)` | The buggy job's output: only the first 3 rows. |
| 9 | `t.overwrite(bad)` | Replace the whole table. PyIceberg commits it as two snapshots: a delete of everything (2), then an append of the 3 rows (3). |
| 11 | `for n, s in enumerate(t.snapshots(), 1):` | Walk the history, oldest first. |
| 12 | `op = s.summary.operation.value` | What the write did: `append`, `delete`, `overwrite` or `replace`. |
| 13 to 14 | `print(f"snap {n} {op}:", s.summary["total-records"], "rows")` | Each snapshot's summary also records how many rows the table held after it. |
| 16 | `good = t.snapshots()[0].snapshot_id` | The ID of snapshot 1, the last good state. |
| 17 | `print("now:", total(t.scan()))` | Read the current table: 3 rows, $545. |
| 18 | `print("snap 1:", total(t.scan(snapshot_id=good)))` | Time travel: read the table as of snapshot 1. 8 rows, $2,050. |
| 20 to 21 | `t.manage_snapshots().rollback_to_snapshot(good).commit()` | Roll back: snapshot 1 becomes current again. |
| 22 | `print("rolled back:", total(t.scan()))` | The current table is whole again. |

`lake.py` deletes any old `lake.db` and `warehouse/`, creates the `SqlCatalog`, and reads `orders.csv` with
`pyarrow.csv`. `total()` reads a scan into Arrow and sums `usd` with `pyarrow.compute`.

## What a rollback really does

The rollback writes nothing to `data/`. It writes a fourth metadata file whose current snapshot is snapshot 1 again,
and the catalog now points at that file. Snapshots 2 and 3 are still listed in the metadata, and the snapshot log
shows the history in order: 1, 2, 3, then 1 again. That's why it is instant on a table of any size.

The same design gives Iceberg two other features the video mentions:

- **Schema evolution.** Columns are tracked by ID, not by name or position, so adding or renaming a column is a
  metadata change. No data file is rewritten.
- **One table, many engines.** The format is an open spec, so Spark, Trino, Flink and Snowflake can all read and
  write the same Iceberg tables.

## The gotcha: history costs storage

Every old snapshot keeps its data files alive. A table that is overwritten nightly keeps every night's files until
someone removes the snapshots, so teams expire them on a schedule (for example, keep 7 days). Expiring a snapshot
also ends your ability to time travel to it. Note that in PyIceberg 0.12, `t.maintenance.expire_snapshots()` removes
snapshots from the metadata but leaves the Parquet files on disk. Engines like Spark have procedures that also
delete the files no snapshot uses any more.

What the video simplified: a real catalog is a service (a REST catalog, AWS Glue, Hive Metastore, Nessie and
others) and the warehouse is object storage like S3. SQLite and a local folder follow the same rules, which is why
they work for learning.

## Try this

1. Time travel to snapshot 2 with `t.snapshots()[1].snapshot_id`. How many rows does it hold, and why?
2. Replace line 9 with `t.delete("id == 1002")`. How many snapshots are there now, and which operation is the last
   one? Count the Parquet files in `src/warehouse/shop/orders/data/`.
3. After line 6, add a column: `with t.update_schema() as u: u.add_column("note", StringType())`
   (`from pyiceberg.types import StringType`). Does the number of snapshots change? Did any Parquet file change?
4. Before the rollback, expire snapshot 1 with `t.maintenance.expire_snapshots().by_id(good).commit()`. What happens
   when you try to roll back to it? Is the 8-row Parquet file still on disk?

---
Previous: [15 · Idempotent pipelines](../15-idempotent-pipelines) · Next: [17 · Change data capture](../17-change-data-capture) · [All lessons](../../README.md)
