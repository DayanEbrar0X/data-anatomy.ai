# The consumer side (same as src/shop.py): a DuckDB warehouse that
# already holds Oct 7, a loader with no checks, the revenue report,
# and run() that loads Oct 8 with or without a contract check in front.
import json
from pathlib import Path

import duckdb
from pydantic import ValidationError

HERE = Path(__file__).resolve().parent
oct8 = json.load(open(HERE / "oct8.json"))  # renamed + retyped upstream


def warehouse():
    db = duckdb.connect()
    db.sql("CREATE TABLE orders (day DATE, order_id BIGINT,"
           " amount DOUBLE, status VARCHAR)")
    load(db, json.load(open(HERE / "oct7.json")), "2026-10-07")
    return db


def load(db, rows, day="2026-10-08"):
    # Like many loaders: read the columns it expects,
    # anything missing quietly becomes NULL.
    for r in rows:
        db.execute("INSERT INTO orders VALUES (?, ?, ?, ?)",
                   [day, r.get("order_id"), r.get("amount"),
                    r.get("status")])


def report(db, name):
    print(name)
    sql = ("SELECT day, count(*), coalesce(sum(amount) "
           "FILTER (WHERE status = 'paid'), 0) "
           "FROM orders GROUP BY day ORDER BY day")
    for day, n, usd in db.sql(sql).fetchall():
        print(f"  {day:%b} {day.day}: {n} orders, ${usd:,.2f}")


def run(rows, check=None):
    db = warehouse()
    try:
        for row in rows if check else []:
            check(row)  # the contract, row by row
        load(db, rows)  # only if every row passed
    except ValidationError as e:
        print("Oct 8 rejected before load:")
        for err in e.errors():
            print(f"  {err['loc'][0]}: {err['msg']}")
    report(db, "with contract:" if check else "no contract:")
