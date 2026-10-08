# The job around the load (same data as the long version, in
# ../data): a warehouse that already holds Oct 6, a two-step
# job that crashes once, and the report.
import csv
from pathlib import Path

import duckdb

DATA = Path(__file__).resolve().parents[1] / "data"

DAY = "2026-10-07"


def rows(name):
    with open(DATA / name) as f:
        return [(r["day"], int(r["id"]), int(r["usd"]))
                for r in csv.DictReader(f)]


def naive(db, day, rows):
    db.executemany("INSERT INTO revenue "
                   "VALUES (?, ?, ?)", rows)


def warehouse():
    db = duckdb.connect()
    db.sql("CREATE TABLE revenue "
           "(day DATE, id INT, usd INT)")
    naive(db, "2026-10-06", rows("history.csv"))
    return db


def crash_and_rerun(load):
    db = warehouse()  # already holds Oct 6
    load(db, DAY, rows("orders.csv"))  # run 1: load,
    # then step 2 (publish) crashes, so the scheduler
    load(db, DAY, rows("orders.csv"))  # reruns it all
    sql = ("SELECT count(*), sum(usd) FROM revenue "
           "WHERE day = ?")
    n, usd = db.execute(sql, [DAY]).fetchone()
    old = db.execute(sql, ["2026-10-06"]).fetchone()[1]
    print(f"{load.__name__}: Oct 7 ${usd:,} ({n} rows), "
          f"Oct 6 ${old:,}")
