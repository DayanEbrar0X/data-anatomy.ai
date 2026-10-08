# 21 · Data contracts

<img src="https://img.shields.io/badge/level-intermediate-B45309?style=flat-square" alt="intermediate"> <img src="https://img.shields.io/badge/video-111s_%2B_38s_short-7C3AED?style=flat-square&logo=youtube&logoColor=white" alt="video 111s + 38s short"> <img src="https://img.shields.io/badge/uses-pydantic_%C2%B7_duckdb-2563EB?style=flat-square&logo=python&logoColor=white" alt="pydantic · duckdb"> <img src="https://img.shields.io/badge/topic-data_engineering-0E1525?style=flat-square" alt="data engineering">

**Upstream renamed one column. Your dashboard died silently.** The team that sends orders renamed `amount` to
`amount_usd` and started sending `order_id` as text. Loaded as usual, October 8 shows 5 orders and $0.00 of revenue,
with no error anywhere. With a data contract checked before load, the batch is rejected with the two broken fields
named, and the dashboard keeps October 7's $412.40 instead of a fake zero.

Watch: [YouTube](https://www.youtube.com/@datanatomyai) · [TikTok](https://www.tiktok.com/@datanatomy.ai) · [Instagram](https://www.instagram.com/datanatomy.ai) (111 seconds, plus a 38-second short)

<br clear="right">

## The idea

A data contract is an agreement between the team that produces data and the teams that use it, written down so a
program can check it. Like a plug and a socket: agree on the shape, and the wrong plug won't fit. A contract names:

1. **The columns** that must be there.
2. **Their types**, for example "order_id is an integer, not text".
3. **What can't be null**, for example "every order has an amount".
4. **The allowed values**, for example "status is paid or refunded".

The check runs before the load. If any row breaks the contract, nothing is loaded, and the error names the field.
A silent wrong number becomes a loud, specific failure.

## Run it

You need `pydantic` (version 2) and `duckdb` (`pip install pydantic duckdb`). Like the video, `contract.py` opens
`oct8.json` by its file name, so run it from inside `src/`:

```bash
cd src
python3 contract.py
```

```
no contract:
  Oct 7: 5 orders, $412.40
  Oct 8: 5 orders, $0.00
Oct 8 rejected before load:
  order_id: Input should be a valid integer
  amount: Field required
with contract:
  Oct 7: 5 orders, $412.40
```

The short version (`short/contract.py`, 9 lines) moves the load-and-report steps into a `run()` helper and prints
the same thing. It works from the lesson folder:

```bash
python3 short/contract.py
```

```
no contract:
  Oct 7: 5 orders, $412.40
  Oct 8: 5 orders, $0.00
Oct 8 rejected before load:
  order_id: Input should be a valid integer
  amount: Field required
with contract:
  Oct 7: 5 orders, $412.40
```

## Files

```
21-data-contracts/
├── src/
│   ├── contract.py       the code from the video
│   ├── shop.py           the consumer side: DuckDB warehouse, a loader with no checks, the revenue report
│   ├── oct7.json         October 7: 5 orders in the agreed shape
│   └── oct8.json         October 8: 5 orders, amount renamed to amount_usd, order_id sent as text
└── short/
    ├── contract.py       the 9-line version from the short
    ├── shop.py           same as src/shop.py, plus run(), and it finds the JSON files from its own folder
    ├── oct7.json
    └── oct8.json
```

The two JSON files sit next to `contract.py` because the on-screen code (and `shop.py`) read them by name, exactly
as in the video. The short gets its own copies so the `short/` folder runs on its own.

The two batches, side by side:

```
oct7.json  {"order_id": 1001,   "amount": 120.0,     "status": "paid"}   ... 5 rows
oct8.json  {"order_id": "1006", "amount_usd": 99.0,  "status": "paid"}   ... 5 rows
```

`shop.py` plays the warehouse. `warehouse()` makes a fresh in-memory DuckDB database with an `orders` table and
loads October 7 into it. `load()` inserts rows the way many simple loaders do: it reads the columns it expects with
`r.get(...)`, so a missing column quietly becomes `NULL`. `report()` prints the order count and the paid revenue per
day.

## The code

`src/contract.py`, line by line:

| Line | Code | What it does |
|------|------|--------------|
| 1 to 2 | `import json`, `from typing import Literal` | Read the batch file; `Literal` lists allowed values. |
| 3 to 4 | `from pydantic import BaseModel, StrictInt`, `ValidationError` | Pydantic turns a Python class into a checker for data. |
| 5 | `from shop import warehouse, load, report` | The consumer side, from `shop.py`. |
| 7 | `class Order(BaseModel):  # the contract` | One row of orders, as both teams agreed it. |
| 8 | `order_id: StrictInt` | Must be a real integer. `StrictInt` refuses the text `"1006"`; a plain `int` would quietly convert it. |
| 9 | `amount: float  # required, never null` | No default value, so the field must be present, and `None` is not a number. |
| 10 | `status: Literal["paid", "refunded"]` | Only these two values pass. |
| 12 | `oct8 = json.load(open("oct8.json"))` | The producer's new batch: 5 rows with the rename and the text ids. |
| 14 | `db = warehouse()  # Oct 7 already loaded` | A warehouse that already holds yesterday's 5 orders. |
| 15 | `load(db, oct8)    # no contract` | Load October 8 with no checks. `amount` is missing, so every amount becomes `NULL`. |
| 16 | `report(db, "no contract:")` | October 8: 5 orders, $0.00. The orders arrived, the revenue didn't, and nothing failed. |
| 18 | `db = warehouse()` | A fresh warehouse with only October 7, for the second run. |
| 19 | `try:` | Any contract failure jumps to the `except` block. |
| 20 to 21 | `for row in oct8: Order.model_validate(row)` | Check every row against the contract. The first bad row raises `ValidationError`. |
| 22 | `load(db, oct8)  # only if every row passes` | Reached only when all rows passed, so a batch loads whole or not at all. |
| 23 to 24 | `except ValidationError as e: print(...)` | The batch is rejected before anything touched the table. |
| 25 to 27 | `for err in e.errors(): ... print(f"  {field}: {err['msg']}")` | One line per broken field. `err["loc"][0]` is the field name. |
| 28 | `report(db, "with contract:")` | Only October 7, still $412.40. No fake zero on the dashboard. |

$412.40 is the paid revenue of October 7: 120.00 + 89.50 + 158.40 + 44.50. Order 1003 is refunded, so it isn't
counted.

`short/contract.py` keeps lines 2, 3 and 7 to 10 (the contract) and replaces the rest with two calls:
`run(oct8)` loads without checks, and `run(oct8, check=Order.model_validate)` checks every row first. `run()` in
`short/shop.py` does what lines 14 to 28 do.

## Two silent fixes, not one

The renamed column is the obvious failure. The second one is easier to miss: in the run without a contract,
`"1006"` is text, but the `orders` table stores `order_id` as `BIGINT`, and DuckDB converts the text to a number on
insert without complaining. That one happened to work. If the producer had sent `"A-1006"`, the insert would have
failed halfway, or a different loader might have stored it as text and broken a join later. A contract decides
these cases up front instead of leaving them to whatever the loader happens to do.

The same goes for Pydantic's own defaults. With `order_id: int`, Pydantic converts `"1006"` to `1006` and the row
passes. That is why the contract uses `StrictInt`. Unknown extra fields such as `amount_usd` are ignored by default;
the error you see comes from `amount` being missing, not from the new name.

## What the video simplified

- **Only the first bad row is reported.** The loop stops at order 1006, so both errors come from that one row. A
  real check would validate every row, collect all the failures, and send the bad batch to a quarantine table with
  an alert that names the field and the row count.
- **The contract lives in consumer code.** In practice both teams agree on it, keep it in one shared place (often a
  YAML spec or a schema registry), and give it a version number. The producer runs the same check in its CI, so a
  rename shows up as a new version before it ships, not as a surprise on October 8.
- **Row-by-row Pydantic is fine for small batches.** For millions of rows, teams usually check whole columns at once
  (in SQL, or with a DataFrame validation library) instead of one Python object per row.
- **Real contracts cover more than shape**: ranges (amounts above zero), uniqueness of `order_id`, freshness (the
  batch arrives by 6 a.m.), and who owns the data.

## Try this

1. Change line 8 to `order_id: int`. Which error disappears, and why is that risky?
2. Add `model_config = ConfigDict(extra="forbid")` to `Order` (import `ConfigDict` from pydantic). What new error
   appears for October 8?
3. In `oct8.json`, fix the five rows (rename back to `amount`, ids as numbers) and set one status to `"PAID"`. What
   does the contract print, and what does the no-contract report show for October 8?
4. Change lines 19 to 27 so every row is checked and all errors are printed with the row's index. How many error
   lines do you get for the original October 8 batch?

---
Previous: [20 · Medallion architecture](../20-medallion-architecture) · Next: [22 · The small files problem](../22-small-files-problem) · [All lessons](../../README.md)
