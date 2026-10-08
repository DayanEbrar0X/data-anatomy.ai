# The same source, day and change log as the long version (src/shop.py), plus the helpers the short uses.
import csv
import sqlite3
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
DAY = (DATA / "day.sql").read_text()  # six writes, in order

with (DATA / "orders.csv").open() as f:
    START = [(int(r["id"]), r["status"]) for r in csv.DictReader(f)]


def source():
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE orders(id INT PRIMARY KEY, status)")
    db.executemany("INSERT INTO orders VALUES (?, ?)", START)
    db.execute("CREATE TABLE changes"
               "(seq INTEGER PRIMARY KEY, op, id, status)")
    return db


def triggers(db):
    """One trigger per write appends to `changes`: a stand-in for the database's write-ahead log."""
    for op, row in [("INSERT", "NEW.id, NEW.status"),
                    ("UPDATE", "NEW.id, NEW.status"),
                    ("DELETE", "OLD.id, NULL")]:
        db.execute(f"""CREATE TRIGGER log_{op} AFTER {op} ON orders BEGIN
          INSERT INTO changes(op, id, status) VALUES ('{op}', {row}); END""")


def snap(db):
    return dict(db.execute("SELECT id, status FROM orders"))


def diff(old, new):
    return {k: new.get(k) for k in old | new if old.get(k) != new.get(k)}
