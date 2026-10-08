# 20 · Medallion architecture

<img src="https://img.shields.io/badge/level-intermediate-B45309?style=flat-square" alt="intermediate"> <img src="https://img.shields.io/badge/video-125s_%2B_36s_short-7C3AED?style=flat-square&logo=youtube&logoColor=white" alt="video 125s + 36s short"> <img src="https://img.shields.io/badge/uses-duckdb-2563EB?style=flat-square&logo=python&logoColor=white" alt="duckdb"> <img src="https://img.shields.io/badge/topic-data_engineering-0E1525?style=flat-square" alt="data engineering">

**Every serious data platform has three layers. Here's why.** Bronze lands the raw data as it is, silver cleans it
once, gold shapes it for the business. We push 10,000 messy order events through all three. Version one of the
cleaning has a bug that silently drops every web order: revenue comes out at $804,262. Fix one expression, replay
from the same bronze, and revenue is $1,200,704, with nothing re-sent by the apps.

Watch: [YouTube](https://www.youtube.com/@datanatomyai) · [TikTok](https://www.tiktok.com/@datanatomy.ai) · [Instagram](https://www.instagram.com/datanatomy.ai) (125 seconds, plus a 36-second short)

<br clear="right">

## The idea

Think of a kitchen: groceries are delivered, then chopped, then plated.

1. **Bronze: land it raw.** Copy the source exactly as it arrives, every column as text, and never edit it.
   It is the record of what you received.
2. **Silver: clean it once.** Remove duplicates, fix formats, give every column a real type, and drop what cannot
   be read. This is the one trusted copy that everyone builds on.
3. **Gold: shape it for the business.** Small tables that answer real questions, here orders and revenue per
   country.

Because bronze keeps everything, a bug in silver is not a disaster: fix the code and rebuild silver and gold from
bronze. That replay is the main reason for the extra layer.

## Run it

You need `duckdb` (`pip install duckdb`). Generate the raw events first, then run from inside `src/`, because the
code opens `events.csv` and writes `bronze.parquet` by their file names, exactly as in the video:

```bash
python3 scripts/make_events.py
cd src
python3 medallion.py
```

```
wrote src/events.csv and short/events.csv: 10,000 rows each
```

```
bronze 10,000 rows | 9,600 unique, raw text
v1 silver 6,287 | fixed 1,882 | dropped 3,713
v1 gold revenue $804,262
v2 silver 9,420 | fixed 5,015 | dropped 580
v2 gold revenue $1,200,704
gold BR: 2,416 orders, $306,313
gold DE: 2,345 orders, $298,983
gold US: 2,315 orders, $297,767
gold IN: 2,344 orders, $297,641
replayed from bronze: $804,262 -> $1,200,704
```

`fixed` counts silver rows that differ from their raw bronze row (a country code cleaned or a dollar sign
stripped). `dropped` is bronze rows minus silver rows. Tested with DuckDB 1.5.4.

### The short version

The short (`short/replay.py`, 8 lines) imports the same three layer functions and shows only the bug and the
replay. Run it from inside `short/` (after `scripts/make_events.py`, which writes a copy of the events there too):

```bash
cd short
python3 replay.py
```

```
bronze 10,000 rows | 9,600 unique, raw text
v1 silver 6,287 | fixed 1,882 | dropped 3,713
v1 gold revenue $804,262
v2 silver 9,420 | fixed 5,015 | dropped 580
v2 gold revenue $1,200,704
```

## Files

```
20-medallion-architecture/
├── scripts/
│   └── make_events.py    writes events.csv into src/ and short/ (seeded, 10,000 rows)
├── src/
│   ├── medallion.py      the code from the video
│   ├── layers.py         prints row counts per layer and the gold table
│   ├── events.csv        generated, about 380 KB, not committed
│   └── bronze.parquet    written by medallion.py, not committed
├── short/
│   ├── replay.py         the 8-line version from the short
│   ├── medallion.py      same as src/medallion.py
│   ├── layers.py         same as src/layers.py
│   ├── events.csv        generated, not committed
│   └── bronze.parquet    written by replay.py, not committed
└── .gitignore            keeps the generated files out of git
```

`events.csv` sits next to the code because the on-screen file reads it by name. It is generated rather than
committed: a fixed seed makes every run write the same file, byte for byte. The raw events come from three apps
and carry the mess real sources have:

- 9,600 orders, plus 400 retries: the same event sent twice, so 10,000 rows.
- Country codes mostly clean (`US`), but some padded and lower case (` us`) or title case with a trailing space
  (`Us `).
- The web app sends amounts as `$12.50`; iOS and Android send `12.50`.
- A few rows are unreadable: amounts like `N/A`, `null` or empty, timestamps like `not-a-date` or
  `07/10/2026 25:61`.

## The code

`src/medallion.py`, line by line:

| Line | Code | What it does |
|------|------|--------------|
| 1 to 2 | imports | DuckDB, plus the reporting helpers. |
| 4 | `def bronze(db):` | Land the raw events as they are. |
| 5 to 6 | `COPY (FROM read_csv('events.csv', all_varchar=true)) TO 'bronze.parquet'` | Read the CSV with every column as text (`all_varchar`), so nothing is guessed or lost, and store it as Parquet: compressed and cheap to keep. Bronze is never edited after this. |
| 8 | `def silver(db, amount):` | Build the clean table. `amount` is a SQL expression for the amount column, so the two versions can differ in one place. |
| 9 | `CREATE OR REPLACE TABLE silver AS` | Silver is rebuilt from scratch on every run. |
| 10 | `SELECT DISTINCT ON (event_id) event_id,` | Keep one row per event id. The 400 retries are gone. |
| 11 | `upper(trim(country)) AS country,` | ` us` and `Us ` both become `US`. |
| 12 | `TRY_CAST(ts AS TIMESTAMP) AS time,` | Text to a real timestamp. `TRY_CAST` returns null when it cannot read the value, instead of failing. |
| 13 | `TRY_CAST({amount} AS DECIMAL(9,2)) AS usd` | The amount expression, cast to a decimal with two places. |
| 14 | `FROM 'bronze.parquet'` | Silver reads bronze, never the source file. |
| 15 to 16 | `WHERE time IS NOT NULL AND usd IS NOT NULL` | Drop the rows that could not be read. DuckDB lets `WHERE` use the column names from the `SELECT`. |
| 18 to 22 | `def gold(db): ... GROUP BY country` | The business table: per country, the number of orders and the revenue, rounded to whole dollars. |
| 24 | `if __name__ == "__main__":` | Run the steps only when this file is run directly, so `short/replay.py` can import the functions. |
| 25 | `db = duckdb.connect()` | An in-memory database for silver and gold. |
| 26 | `bronze(db)  # once` | Land the data once. |
| 27 to 28 | `silver(db, "amount"); gold(db)` then `report(db, "v1")` | Version one passes the raw amount column. |
| 29 to 30 | `silver(db, "ltrim(amount, '$')"); gold(db)` then `report(db, "v2")` | Version two strips a leading dollar sign first, then rebuilds silver and gold from the same bronze. |
| 31 | `show_gold(db)` | Print the gold table and the revenue before and after. |

`layers.py` holds the reporting. `report()` counts the rows in bronze (and, the first time, the unique event ids),
the rows in silver, the rows it fixed and dropped, and the gold revenue. `show_gold()` prints the gold table and the
two revenue totals.

## The bug, and why bronze saves you

`TRY_CAST('$42.21' AS DECIMAL(9,2))` is null: the cast cannot read a dollar sign. So in version one every web
order becomes null and the filter drops it. Nothing errors. Silver simply has 6,287 rows instead of 9,420, and gold
reports $804,262 of revenue instead of $1,200,704.

The 3,713 rows dropped in version one are the 400 retries, 180 unreadable rows (107 bad amounts and 73 bad
timestamps) and 3,133 perfectly good web orders. After the fix, only the 580 that should go are dropped.

If the pipeline had cleaned the data on the way in and kept only the result, those 3,133 orders would be gone, and
getting them back would mean asking every app to send them again. With bronze, the fix is one changed expression and
a rebuild.

The deeper lesson is the silent drop. `TRY_CAST` plus a filter is a common cleaning pattern, and it hides mistakes.
Count what each layer drops, as `layers.py` does, and alert when the number jumps: version one dropped 37% of the
rows. Many teams also write rejected rows to a separate table so someone can look at them.

## What the video simplified

- **Real layers are tables in a lakehouse**, usually Delta Lake or Iceberg ([16 · Apache Iceberg](../16-apache-iceberg)),
  not one Parquet file and an in-memory database. Bronze is append-only and usually adds load metadata (load time,
  source file) to every row.
- **Silver is usually incremental.** Here it is rebuilt from scratch, which is fine for 10,000 rows. At scale, silver
  merges in only the new bronze rows ([19 · Incremental loads](../19-incremental-loads)), and a replay is a
  deliberate backfill.
- **`DISTINCT ON` without an `ORDER BY` keeps an arbitrary row.** That is safe here because the retries are exact
  copies. When duplicates can differ, order by load time and keep the latest.
- **Bronze keeps raw personal data too.** Names, emails and addresses that silver might mask are still in bronze.
  Lock it down, and set a retention period.

## Try this

1. Remove `DISTINCT ON (event_id)` from line 10. How much does version two's revenue go up, and would anyone
   reading the gold table notice?
2. Use `replace(amount, '$', '')` as the version two expression. Is the result the same? When would the two differ?
3. Write the rejected rows to a table: the bronze rows whose `time` or `usd` is null. How many are bad amounts and
   how many are bad timestamps?
4. Add a second gold table with revenue per hour of the day, built from the same silver. Which hour earns the most?

---
Previous: [19 · Incremental loads](../19-incremental-loads) · Next: [21 · Data contracts](../21-data-contracts) · [All lessons](../../README.md)
