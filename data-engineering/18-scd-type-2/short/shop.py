# The same customers and sales as the long version (src/shop.py), plus both dimension tables.
import csv
from pathlib import Path

import duckdb

DATA = Path(__file__).resolve().parents[1] / "data"
ASOF = "AND day >= valid_from AND day < valid_to"


def rows(name):
    with (DATA / name).open() as f:
        return [tuple(int(v) if v.isdigit() else v for v in r)
                for r in list(csv.reader(f))[1:]]


CUSTOMERS = rows("customers.csv")  # (id, name, region)
SALES = rows("sales.csv")          # (customer, day, usd)


def setup():
    db = duckdb.connect()
    db.sql("CREATE TABLE customers (id INT, name TEXT, region TEXT)")
    db.executemany("INSERT INTO customers VALUES (?, ?, ?)", CUSTOMERS)
    db.sql("CREATE TABLE sales (cust INT, day DATE, usd INT)")
    db.executemany("INSERT INTO sales VALUES (?, ?, ?)", SALES)
    db.sql("CREATE TABLE t1 AS FROM customers")  # Type 1: one row per customer
    db.sql("""CREATE TABLE t2 AS SELECT *, DATE '2000-01-01' AS valid_from,
              DATE '9999-12-31' AS valid_to, true AS is_current FROM customers""")  # Type 2
    return db


def by_region(db, dim, q=2):
    asof = ASOF if dim == "t2" else ""  # Type 2 joins each sale to the version valid on its day
    rows = db.sql(f"""SELECT region, sum(usd) FROM sales JOIN {dim} ON cust = id {asof}
                      WHERE quarter(day) = {q} GROUP BY region ORDER BY region""").fetchall()
    return ", ".join(f"{r} ${u:,}" for r, u in rows)
