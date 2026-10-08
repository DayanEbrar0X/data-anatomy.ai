# 18 · SCD Type 2

<img src="https://img.shields.io/badge/level-intermediate-B45309?style=flat-square" alt="intermediate"> <img src="https://img.shields.io/badge/video-108s_%2B_38s_short-7C3AED?style=flat-square&logo=youtube&logoColor=white" alt="video 108s + 38s short"> <img src="https://img.shields.io/badge/uses-duckdb-2563EB?style=flat-square&logo=python&logoColor=white" alt="duckdb"> <img src="https://img.shields.io/badge/topic-data_engineering-0E1525?style=flat-square" alt="data engineering">

**Your customer moved, and your report rewrote history.** Ana lives in the East region until July 1, when she moves
West. Overwrite her row (Type 1) and Q2 revenue for the East drops from $6,700 to $2,500, because her spring sales
follow her West. Nothing new was sold. Keep one row per version instead (Type 2) and Q2 stays at $6,700, while her
August sale of $1,800 lands in the West.

Watch: [YouTube](https://www.youtube.com/@datanatomyai) · [TikTok](https://www.tiktok.com/@datanatomy.ai) · [Instagram](https://www.instagram.com/datanatomy.ai) (108 seconds, plus a 38-second short)

<br clear="right">

## The idea

A warehouse splits data into **facts** (things that happened: sales, with a date and an amount) and **dimensions**
(the things they happened to: customers, with a name and a region). Dimensions change slowly, now and then. A
slowly changing dimension (SCD) is a rule for what to do when they do.

- **Type 1 is a whiteboard:** erase the old value and write the new one. Simple, but every old fact now joins to the
  new value, so past reports change.
- **Type 2 is a ledger:** add a line. Each version of a customer gets its own row, with the dates it was valid.

A Type 2 change takes two steps:

1. **Close** the current row: set its `valid_to` to the change date and `is_current` to false.
2. **Insert** the new version: valid from the change date, open-ended (`9999-12-31`), current.

Reports then join each sale to the version that was valid on the day of the sale (an as-of join).

## Run it

You need `duckdb` (`pip install duckdb`).

```bash
python3 src/scd.py
```

```
Q2 before: East $6,700, West $3,000
Q2 type 1: East $2,500, West $7,200
Q3 type 2: West $1,800
Q2 type 2: East $6,700, West $3,000
```

Tested with DuckDB 1.5.4. Everything runs in an in-memory database, so nothing is written to disk.

## The short version

The 38-second short uses the same customers and sales. Its helper (`short/shop.py`) builds both dimension tables up
front and does the as-of join for `t2`, so the on-screen file is just the two changes and two reports:

```bash
python3 short/scd.py
```

```
Q2 type 1: East $2,500, West $7,200
Q2 type 2: East $6,700, West $3,000
```

## Files

```
18-scd-type-2/
├── data/
│   ├── customers.csv     3 customers: id, name, region
│   └── sales.csv         5 sales in Q2 and Q3 2026: customer, day, usd
├── src/
│   ├── scd.py            the code from the video
│   └── shop.py           loads data/ into DuckDB tables
└── short/
    ├── scd.py            the 9-line version from the short
    └── shop.py           same data, plus the t1 and t2 tables and by_region()
```

The customers and sales are data, so they live in `data/` as CSV files and both versions read them. Ana (id 1) has
two sales in Q2 (April and May) and one in Q3 (August), which is what makes her move visible in the totals.

## The code

`src/scd.py`, line by line:

| Line | Code | What it does |
|------|------|--------------|
| 1 to 2 | imports | DuckDB, and the helper that loads the data. |
| 4 | `db = duckdb.connect()` | An in-memory DuckDB database. |
| 5 | `setup(db)` | Creates `customers` (id, name, region) and `sales` (cust, day, usd) from the CSV files. |
| 7 | `def by_region(dim, q=2, asof=""):` | The revenue report. `dim` is which customers table to join, `q` the quarter, `asof` an optional extra join condition. |
| 8 to 12 | `rows = db.sql(f"""SELECT region, sum(usd) ...""")` | Join each sale to its customer, keep one quarter, sum by region. |
| 13 to 14 | `return ", ".join(f"{r} ${u:,}" ...)` | Format the result as `East $6,700, West $3,000`. |
| 16 | `print("Q2 before:", by_region("customers"))` | Q2 as it stands, before Ana moves: East $6,700, West $3,000. |
| 19 | `db.sql("CREATE TABLE t1 AS FROM customers")` | Type 1 starts as a plain copy. `AS FROM ...` is DuckDB shorthand for `AS SELECT * FROM ...`. |
| 20 | `db.sql("UPDATE t1 SET region='West' WHERE id=1")` | Overwrite Ana's region in place. The old value is gone. |
| 21 | `print("Q2 type 1:", by_region("t1"))` | Q2 again: East $2,500, West $7,200. Ana's $4,200 of spring sales moved West. |
| 24 to 27 | `CREATE TABLE t2 AS SELECT *, ... valid_from, ... valid_to, true AS is_current` | Type 2 adds three columns. Every row starts valid from 2000-01-01 until 9999-12-31, and current. |
| 28 to 30 | `UPDATE t2 SET is_current = false, valid_to = '2026-07-01' WHERE id = 1 AND is_current` | Close Ana's current row on the day she moves. `AND is_current` makes sure only the open version is closed. |
| 31 to 32 | `INSERT INTO t2 VALUES (1, 'Ana', 'West', '2026-07-01', '9999-12-31', true)` | Her new version: West, from July 1, open-ended. Ana now has two rows. |
| 33 | `asof = "AND day >= valid_from AND day < valid_to"` | The as-of condition: a sale joins only the version valid on its day. |
| 34 | `print("Q3 type 2:", by_region("t2", 3, asof))` | Q3: her August sale, $1,800, counts for the West. |
| 35 | `print("Q2 type 2:", by_region("t2", 2, asof))` | Q2: back to East $6,700, West $3,000. History kept. |

`shop.py` reads the two CSV files (paths resolved from its own location), turns numeric fields into integers, and
inserts them into typed tables. The `day` column is a `DATE`, which is what lets `quarter(day)` and the date
comparisons work.

## The gotcha: join on the date range, not just the id

Leave out `asof` on line 35 (`by_region("t2", 2)`) and each of Ana's Q2 sales matches both of her rows. The report
says East $6,700, West $7,200: her $4,200 is counted twice, once in each region, and the total goes from $9,700 to
$13,900. Every query against a Type 2 table must either use the date range or filter to `is_current` when it wants
only today's view.

The range is half-open: `valid_from` is included and `valid_to` is not. A sale on July 1 itself joins only the West
row, so no day ever matches two versions.

## In production

- **Real dimensions change all the time:** addresses, sales reps, price tiers, account owners. Type 2 is the usual
  choice whenever reports by those attributes must stay stable over time.
- **dbt snapshots** build exactly this table for you. They add `dbt_valid_from` and `dbt_valid_to` to every row and,
  by default, leave `dbt_valid_to` empty (null) for the current version instead of using `9999-12-31`.
- **Surrogate keys.** In a classic warehouse each version gets its own key (say, `customer_key` 17 for Ana in the East,
  42 for Ana in the West), and each sale stores the key that was current when it was loaded. Reports then join on
  that key alone, without the date range. This lesson keeps the natural id and joins on dates, which shows the idea
  with fewer moving parts.
- **Close and insert together.** The two statements on lines 28 to 32 belong in one transaction (or one `MERGE`),
  so no reader ever sees Ana with no current row or with two.
- **Simplified here:** `quarter(day)` ignores the year, which is fine because every sale is in 2026, and the change
  date is typed in by hand. A real pipeline detects the change by comparing the source with the current rows.

## Try this

1. Change line 35 to `print("Q2 type 2:", by_region("t2", 2))`, without `asof`. What does it print, and where does
   the extra $4,200 come from?
2. Ben moves East on 2026-05-01. Add a close and an insert for him, like lines 28 to 32, right after line 32. What does
   Q2 type 2 print now?
3. Add a sale for Ana on the day she moves: the line `1,2026-07-01,500` in `data/sales.csv`. Which region gets it, and
   why not both?
4. Print `db.sql("FROM t2 WHERE is_current ORDER BY id")`. How does it compare with `t1`? What does Type 2 give you
   that Type 1 cannot?

---
Previous: [17 · Change data capture](../17-change-data-capture) · Next: [19 · Incremental loads](../19-incremental-loads) · [All lessons](../../README.md)
