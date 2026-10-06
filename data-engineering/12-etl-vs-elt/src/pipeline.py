import duckdb
import pandas as pd
from report import report

raw = pd.read_csv("orders.csv", dtype=str)

# ETL: transform in Python, then load
clean = raw.drop_duplicates()
del clean["email"]  # PII never lands
usd = clean["amount"].str.strip("$")
clean["amount"] = usd.astype(float)
etl = duckdb.connect()
etl.sql("CREATE TABLE orders AS FROM clean")

# ELT: load raw as-is, then transform in SQL
elt = duckdb.connect()
elt.sql("CREATE TABLE raw_orders AS FROM raw")
elt.sql("""CREATE TABLE orders AS
  SELECT DISTINCT order_id,
    CAST(LTRIM(amount, '$') AS DOUBLE) AS amount
  FROM raw_orders""")
report(etl, elt)
