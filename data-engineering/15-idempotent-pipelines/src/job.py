# The job around the load: a warehouse that already holds
# yesterday (Oct 6), a two-step job, and the revenue report.
import csv
from pathlib import Path

import duckdb

DATA = Path(__file__).resolve().parents[1] / "data"

DAY = "2026-10-07"


def rows(name):
    with open(DATA / name) as f:
        return [(r["day"], int(r["id"]), int(r["usd"]))
                for r in csv.DictReader(f)]


def warehouse():
    db = duckdb.connect()
    db.sql("CREATE TABLE revenue "
           "(day DATE, id INT, usd INT)")
    db.executemany("INSERT INTO revenue VALUES (?, ?, ?)",
                   rows("history.csv"))
    return db


def run_job(db, load, crash=False):
    load(db, DAY, rows("orders.csv"))  # step 1: load
    if crash:                          # step 2: publish
        print(f"{load.__name__}: crashed at step 2")
        return
    print(f"{load.__name__}: rerun ok")


def report(db, name):
    sql = ("SELECT count(*), sum(usd) FROM revenue "
           "WHERE day = ?")
    n, usd = db.execute(sql, [DAY]).fetchone()
    old = db.execute(sql, ["2026-10-06"]).fetchone()[1]
    print(f"{name}: Oct 7 ${usd:,} ({n} rows), "
          f"Oct 6 ${old:,}")
