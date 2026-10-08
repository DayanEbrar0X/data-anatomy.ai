# The consumer side: a DuckDB warehouse that already holds
# Oct 7, a loader with no checks, and the revenue report.
import json

import duckdb


def warehouse():
    db = duckdb.connect()
    db.sql("CREATE TABLE orders (day DATE, order_id BIGINT,"
           " amount DOUBLE, status VARCHAR)")
    load(db, json.load(open("oct7.json")), "2026-10-07")
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
