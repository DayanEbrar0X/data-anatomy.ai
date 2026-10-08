# The source database, the day's writes, and an empty target.
import csv
import sqlite3
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
TABLE = "CREATE TABLE orders(id INT PRIMARY KEY, status)"
DAY = (DATA / "day.sql").read_text()  # six writes, in order

with (DATA / "orders.csv").open() as f:
    START = [(int(r["id"]), r["status"]) for r in csv.DictReader(f)]


def source():
    db = sqlite3.connect(":memory:")
    db.execute(TABLE)
    db.executemany("INSERT INTO orders VALUES (?, ?)", START)
    db.execute("CREATE TABLE changes"
               "(seq INTEGER PRIMARY KEY, op, id, status)")
    return db


def target(rows):
    db = sqlite3.connect(":memory:")
    db.execute(TABLE)
    db.executemany("INSERT INTO orders VALUES (?, ?)", rows.items())
    return db
