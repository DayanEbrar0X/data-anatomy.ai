import duckdb
from layers import report, show_gold

def bronze(db):  # land raw events as-is, all text
    db.sql("""COPY (FROM read_csv('events.csv',
      all_varchar=true)) TO 'bronze.parquet'""")

def silver(db, amount):  # clean, dedupe, type
    db.sql(f"""CREATE OR REPLACE TABLE silver AS
      SELECT DISTINCT ON (event_id) event_id,
        upper(trim(country)) AS country,
        TRY_CAST(ts AS TIMESTAMP) AS time,
        TRY_CAST({amount} AS DECIMAL(9,2)) AS usd
      FROM 'bronze.parquet'
      WHERE time IS NOT NULL
        AND usd IS NOT NULL""")

def gold(db):  # the business table
    db.sql("""CREATE OR REPLACE TABLE gold AS
      SELECT country, count(*) AS orders,
        round(sum(usd)) AS revenue
      FROM silver GROUP BY country""")

if __name__ == "__main__":
    db = duckdb.connect()
    bronze(db)  # once
    silver(db, "amount"); gold(db)  # v1: the bug
    report(db, "v1")
    silver(db, "ltrim(amount, '$')"); gold(db)
    report(db, "v2")  # the fix, replayed
    show_gold(db)
