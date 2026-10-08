# 24 · Lake vs warehouse vs lakehouse

<img src="https://img.shields.io/badge/level-intermediate-B45309?style=flat-square" alt="intermediate"> <img src="https://img.shields.io/badge/video-115s_%2B_37s_short-7C3AED?style=flat-square&logo=youtube&logoColor=white" alt="video 115s + 37s short"> <img src="https://img.shields.io/badge/uses-duckdb_%C2%B7_pyiceberg_%C2%B7_pyarrow-2563EB?style=flat-square&logo=python&logoColor=white" alt="duckdb · pyiceberg · pyarrow"> <img src="https://img.shields.io/badge/topic-data_engineering-0E1525?style=flat-square" alt="data engineering">

**Three names for where the data lives, and they're not the same.** Six shop events arrive in two batches, then one
bad write: an amount typed as text, `"12,50"`. Each store is asked for total revenue. The lake (a folder of JSON
files) takes all three files, then its query fails. The warehouse (a typed DuckDB table) rejects the bad rows and
answers $74.50. The lakehouse (an Apache Iceberg table) rejects them too, keeps two commits you can read back, and
also answers $74.50.

Watch: [YouTube](https://www.youtube.com/@datanatomyai) · [TikTok](https://www.tiktok.com/@datanatomy.ai) · [Instagram](https://www.instagram.com/datanatomy.ai) (115 seconds, plus a 37-second short)

<br clear="right">

## The idea

The three differ in *when* the data is checked and *where* it is stored:

1. **Data lake**: a storage unit. Cheap, takes anything. Files land in a folder as they are, and the schema is only
   worked out when someone reads them (*schema on read*). Bad data gets in, and the reader finds out.
2. **Data warehouse**: a library. Everything is checked on the way in against typed tables (*schema on write*), so
   it is easy to query and trust. The data usually lives in the warehouse's own storage format.
3. **Lakehouse**: keeps the lake's cheap, open files (Parquet), and adds a table format on top (Apache Iceberg, Delta
   Lake or Apache Hudi). The table format checks writes against a schema, records every change as a commit, and lets
   you read old versions. Any engine that speaks the format can read the same files.

## Run it

You need `duckdb`, `pyarrow` and `pyiceberg` with its SQL catalog support
(`pip install duckdb "pyiceberg[pyarrow,sql-sqlite]"`). The code writes `lake/`, `shop.duckdb` and `lakehouse/` by
relative name, so run it from inside `src/`:

```bash
cd src
python3 three_ways.py
```

```
lake: 3 files written
lake: query failed (BinderException)
warehouse: bad rows rejected
warehouse: revenue $74.50
lakehouse: bad rows rejected
lakehouse: 2 commits, commit 1 had 3 rows
lakehouse: revenue $74.50
```

All three stores are rebuilt from scratch on every run, so the output is the same each time. They are generated, so
they are not committed. After a run, `src/` holds:

```
lake/                       3 JSON files, one per batch, the bad one included
shop.duckdb                 the warehouse: one DuckDB file with the events table
lakehouse/
├── catalog.db              the Iceberg catalog (SQLite): which metadata file is current
└── shop/events/
    ├── data/               2 Parquet files, one per accepted commit
    └── metadata/           4 table versions (*.metadata.json), plus Avro manifest files
```

## The short version

The short (`short/ask_three.py`, 9 lines) imports the three store functions instead of showing them and keeps only
the loop that asks each one for revenue. It prints `query failed` without the error name:

```bash
cd short
python3 ask_three.py
```

```
lake: 3 files written
lake: query failed
warehouse: bad rows rejected
warehouse: revenue $74.50
lakehouse: bad rows rejected
lakehouse: 2 commits, commit 1 had 3 rows
lakehouse: revenue $74.50
```

## Files

```
24-lake-vs-warehouse-vs-lakehouse/
├── src/
│   ├── three_ways.py     the code from the video
│   └── store.py          the events, the bad write, the Iceberg schema, and three small helpers
├── short/
│   ├── ask_three.py      the 9-line version from the short
│   ├── ways.py           the three store functions, without the loop
│   └── store.py          same as src/store.py
└── .gitignore            keeps lake/, lakehouse/ and shop.duckdb out of git
```

There is no data folder: the seven events are written out in `store.py`, so you can read the whole input at once.
`short/` has its own copy of everything it needs, so it runs on its own.

```python
DAY1 = [{"id": 1, "kind": "view", "usd": 0.0},
        {"id": 2, "kind": "buy", "usd": 19.5},
        {"id": 3, "kind": "view", "usd": 0.0}]
DAY2 = [{"id": 4, "kind": "buy", "usd": 42.0},
        {"id": 5, "kind": "view", "usd": 0.0},
        {"id": 6, "kind": "buy", "usd": 13.0}]
BAD = [{"id": 7, "kind": "buy", "usd": "12,50"}]
```

## The code

`src/three_ways.py`, line by line:

| Line | Code | What it does |
|------|------|--------------|
| 1 to 4 | imports | DuckDB to query all three stores, Iceberg's `StringType` for the schema change, and the data and helpers from `store.py`. |
| 5 | `SUM = "SELECT sum(usd) FROM "` | The one question every store answers: total revenue. |
| 7 | `def lake():` | Files in a folder, schema on read. |
| 8 | `fresh("lake")` | Deletes and recreates the folder, so each run starts empty. |
| 9 to 11 | `for i, rows in enumerate(...)` ... `json.dump(rows, f)` | Each batch is dumped as its own JSON file. Nothing checks it, so the bad batch lands as `lake/2.json`. |
| 12 to 13 | `n = len(os.listdir("lake"))`, print | All 3 files were written. |
| 14 | `return duckdb.sql(SUM + "'lake/*.json'")` | DuckDB reads the three files and only now works out the schema. `usd` is a number in two files and text in the third, so the query fails (see below). |
| 16 | `def warehouse():` | A typed table, schema on write. |
| 17 | `db = duckdb.connect("shop.duckdb")` | A DuckDB database stored in one file. |
| 18 to 19 | `CREATE OR REPLACE TABLE events (id INT, kind TEXT, usd DOUBLE)` | The schema is declared before any data arrives. `usd` must be a number. |
| 20 to 23 | `for rows in ...: db.executemany("INSERT INTO events VALUES ($id, $kind, $usd)", rows)` | Inserts each batch. The `$id`-style placeholders are filled from each row's dictionary keys. |
| 24 to 25 | `except duckdb.Error:` | `"12,50"` cannot be converted to `DOUBLE`, so that insert fails with a `ConversionException` and nothing from the bad batch is stored. |
| 26 | `return db.sql(SUM + "events")` | The same sum over the 6 good rows: $74.50. |
| 28 | `def lakehouse():` | An Iceberg table: Parquet files plus metadata. |
| 29 | `cat = catalog("lakehouse")` | A local Iceberg catalog. SQLite tracks the commits, plain files hold the data. |
| 30 | `t = cat.create_table("shop.events", SCHEMA)` | A table with a declared schema: `id` long, `kind` string, `usd` double. |
| 31 to 33 | `if not append(t, rows):` | Each successful append is one commit that writes a Parquet file. The bad batch has a text `usd`, so its schema does not match the table's and pyiceberg refuses it before writing anything. |
| 34 to 35 | `with t.update_schema() as s: s.add_column("country", StringType())` | A schema change. It only writes new metadata. No data files are rewritten, and old rows read `country` as null. |
| 36 to 37 | `v1 = t.snapshots()[0].snapshot_id`, `then = t.scan(snapshot_id=v1).to_arrow()` | Time travel: every commit is a snapshot, and you can read the table as it was after the first one. |
| 38 to 40 | `n = len(t.snapshots())`, print | 2 commits, and commit 1 had 3 rows. |
| 41 | `now = t.scan().to_arrow()` | The current table as an Arrow table: 6 rows. |
| 42 | `return duckdb.sql(SUM + "now")` | DuckDB finds the Python variable `now` by name and sums it: $74.50. |
| 44 to 45 | `for way in (lake, warehouse, lakehouse):`, `name = way.__name__` | One loop asks all three stores. |
| 46 to 48 | `usd = way().fetchone()[0]`, print | Runs the store's query and prints the revenue. |
| 49 to 51 | `except duckdb.Error as e:` | A store whose query fails prints the error type instead. Only the lake gets here. |

`store.py` holds the data and three helpers. `fresh(path)` deletes and recreates a folder. `append(table, rows)`
turns the rows into an Arrow table (its types come only from the values, so the bad row's `usd` is a string), tries
one Iceberg append, and returns `False` on the `ValueError` pyiceberg raises for a schema mismatch. pyiceberg also
prints a table of the mismatched fields, which `append` hides. `catalog(path)` creates a `SqlCatalog` backed by
`catalog.db` in SQLite, with the table files stored under the same folder, and a `shop` namespace.

## Why the lake query fails

DuckDB's `read_json` looks at all the files and merges their schemas. `usd` holds numbers in `0.json` and `1.json`
and the string `"12,50"` in `2.json`. No single SQL type fits both, so DuckDB gives the column the `JSON` type, and
there is no `sum` for `JSON`:

```
Binder Error: No function matches the given name and argument types 'sum(JSON)'.
```

That is schema on read: the bad file was accepted hours ago, and the first person to query it finds the problem.
The obvious fix is worse. Change line 5 to `SELECT sum(TRY_CAST(usd AS DOUBLE)) FROM ` and the lake answers $74.50
with no error at all: the bad row silently turns into null. In a lake, data quality is the reader's problem, and
every reader has to solve it again.

## What the video simplified

- **Rejected is not the same as handled.** `"12,50"` is most likely 12.50 written with a European decimal comma,
  so the real revenue is $87.00. The warehouse and lakehouse kept bad data out, but they also dropped a sale. Real
  pipelines send rejected rows to a quarantine table and alert someone.
- **Everything is local.** A real lake is object storage (Amazon S3, Azure Data Lake Storage, Google Cloud
  Storage), a real warehouse is a service like Snowflake, BigQuery or Redshift, and a real Iceberg catalog is a
  shared service (a REST catalog, AWS Glue, Hive). DuckDB and a SQLite file stand in for them here.
- **DuckDB does not read the Iceberg table directly here.** pyiceberg scans it into Arrow on line 41, and DuckDB
  sums that. The point of a lakehouse is that Spark, Trino, Flink or DuckDB (through its `iceberg` extension) can
  all read the same files. Many teams use all three kinds of store: a lake for raw files, a lakehouse or warehouse
  for trusted tables.

## Try this

1. In `store.py`, change the bad amount to the number `12.5`. What does each store report now, and how many commits
   does the lakehouse make?
2. Change line 5 to `SUM = "SELECT sum(TRY_CAST(usd AS DOUBLE)) FROM "`. The lake now answers. Is its answer
   right, and how would a reader of the lake know a row was lost?
3. After a run, load the table again with pyiceberg and scan each snapshot in `t.snapshots()`. Does the old
   snapshot have the `country` column?
4. Open the warehouse with `duckdb.connect("shop.duckdb").sql("FROM events")`. Which event is missing, and where
   would you look for it in the lake?

---
Previous: [23 · Data engineer vs data scientist vs ML engineer](../23-data-engineer-vs-data-scientist-vs-ml-engineer) · Next: [25 · Data engineering for RAG](../25-data-engineering-for-rag) · [All lessons](../../README.md)
