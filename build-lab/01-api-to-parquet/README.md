# Build Lab 01 · API to Parquet

<img src="../../assets/thumbnails/build-lab-01-api-to-parquet.jpg" width="240" align="right" alt="API to Parquet video">

**JSON in. Parquet out.** A real data pipeline in three files: fetch orders from a paginated API, clean them with
pandas, write a Parquet file, and query it with DuckDB. 122 rows come in, 120 are kept, and 19.0 KB of JSON
becomes 5.6 KB of Parquet that any analytics tool can read.

Watch: [YouTube](https://www.youtube.com/@datanatomyai) · [TikTok](https://www.tiktok.com/@datanatomy.ai) · [Instagram](https://www.instagram.com/datanatomy.ai) (99 seconds) · Part 1 of 3

<br clear="right">

## What you'll build

```
orders_pipeline/
├── api/                 recorded API responses (3 pages)
│   ├── orders_p1.json
│   ├── orders_p2.json
│   └── orders_p3.json
├── data/
│   └── orders.parquet   created when you run the pipeline
├── scripts/
│   └── make_pages.py    made the recorded API pages
├── tests/
│   └── test_pipeline.py checks each step and the final output
├── fetch.py             1. fetch every page from the API
├── transform.py         2. clean the rows with pandas
└── main.py              3. write Parquet and query it with DuckDB
```

The three pipeline files sit at the top, exactly as in the video. Supporting files go in their own folders:
`scripts/` for one-off tools, `tests/` for checks. `data/` holds output only, so it's safe to delete and rebuild.
Run the tests with `pytest` from `orders_pipeline/`.

## Run it

```bash
pip install pandas pyarrow duckdb
cd orders_pipeline
python3 main.py
```

```
122 rows fetched, 120 kept
JSON 19.0 KB -> Parquet 5.6 KB
[('paid', 99), ('refunded', 21)]
```

## About the API

To keep every run identical, the API responses are recorded in `api/`. Each page holds up to 41 orders and a
`next_page` number, the way many real APIs paginate. In production, line 7 of `fetch.py` becomes a real request,
for example `requests.get(URL, params={"page": page}).json()`.

`scripts/make_pages.py` created those pages: 120 orders, where the last order of pages 1 and 2 shows up again on the next
page. Real APIs do this when new records arrive while you are paging, which is why `transform.py` removes
duplicates.

## File 1: `fetch.py`

| Line | Code | What it does |
|------|------|--------------|
| 1 to 2 | imports | `json` to parse responses, `Path` to read files. |
| 4 | `def fetch_orders():` | Return every order from every page. |
| 5 | `rows, page = [], 1` | Start with no rows, on page one. |
| 6 | `while page:` | Keep going while there is a page to fetch. |
| 7 | `# prod: requests.get(URL, params=...)` | Where the real HTTP call goes. |
| 8 to 9 | `raw = ...`, `body = json.loads(...)` | Read one page and parse it. |
| 10 | `rows += body["data"]` | Add this page's orders. |
| 11 | `page = body["next_page"]` | Follow the API's pointer. On the last page it's `None` and the loop ends. |
| 12 | `return rows` | All 122 rows, duplicates included. |

## File 2: `transform.py`

| Line | Code | What it does |
|------|------|--------------|
| 1 | `import pandas as pd` | Tables in Python. |
| 3 | `def clean(rows):` | Turn raw rows into a clean table. |
| 4 | `df = pd.DataFrame(rows)` | One row per order, one column per field. |
| 5 | `df["amount"] = df["amount"].astype(float)` | The API sends amounts as text (`"42.50"`). Make them numbers so you can sum them. |
| 6 | `df["created"] = pd.to_datetime(df["created"])` | Timestamps as text become real dates. |
| 7 | `df = df.drop_duplicates("order_id")` | Remove the two repeated orders. 122 rows become 120. |
| 8 | `return df` | |

## File 3: `main.py`

| Line | Code | What it does |
|------|------|--------------|
| 1 to 4 | imports | DuckDB, `Path`, and our two steps. |
| 6 | `PQ = "data/orders.parquet"` | Where the output goes. |
| 7 to 8 | `rows = fetch_orders()`, `df = clean(rows)` | Fetch, then clean. |
| 9 | `df.to_parquet(PQ, index=False)` | Write. pandas uses PyArrow under the hood. |
| 11 to 12 | `kb = ...`, `j = ...` | Sizes: the three JSON pages, and the Parquet file. |
| 13 to 14 | prints | Rows in and out, and the size comparison. |
| 15 to 17 | `sql = ...`, `duckdb.sql(sql)` | Query the Parquet file directly with SQL. No database server. |

## Why Parquet?

- **Columnar:** each column is stored together, so a query that needs two columns only reads those two.
- **Typed:** amounts stay numbers and dates stay dates, so every reader agrees on what the data is.
- **Compressed:** similar values sit next to each other and compress well. Here it's over 3 times smaller than JSON.

Spark, DuckDB, pandas, Polars and most data warehouses read Parquet directly, so it's a common hand-off format
between pipelines and analytics.

## Try this

1. Add a column in `clean()`: `df["day"] = df["created"].dt.date`, then group revenue by day in DuckDB.
2. Write the same data to CSV with `df.to_csv(...)` and compare the file size.
3. Change the SQL to the total paid revenue: `SELECT round(sum(amount), 2) FROM ... WHERE status = 'paid'`.
4. Point `fetch.py` at a real public API that paginates and keep the rest of the pipeline the same.

## Next in this project

Part 2: schedule the pipeline and catch bad rows before they reach the file.

---
Previous: [07 · Linear regression, no libraries](../../07-linear-regression-no-libraries) · [All lessons](../../README.md)
