# The customers dimension and the sales facts (Q2 and Q3 2026), loaded from data/.
import csv
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"


def rows(name):
    with (DATA / name).open() as f:
        return [tuple(int(v) if v.isdigit() else v for v in r)
                for r in list(csv.reader(f))[1:]]


CUSTOMERS = rows("customers.csv")  # (id, name, region)
SALES = rows("sales.csv")          # (customer, day, usd)


def setup(db):
    db.sql("CREATE TABLE customers (id INT, name TEXT, region TEXT)")
    db.executemany("INSERT INTO customers VALUES (?, ?, ?)", CUSTOMERS)
    db.sql("CREATE TABLE sales (cust INT, day DATE, usd INT)")
    db.executemany("INSERT INTO sales VALUES (?, ?, ?)", SALES)
