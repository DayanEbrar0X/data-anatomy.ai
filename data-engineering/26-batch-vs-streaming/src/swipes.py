# One day of card swipes (event time), the nightly batch slot,
# and the alert report shared by both pipelines.
import csv
from collections import namedtuple
from datetime import datetime
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "swipes.csv"

Swipe = namedtuple("Swipe", "ts card country usd")
DAY = "2026-10-08"
NIGHTLY = datetime.fromisoformat("2026-10-09 02:00:00")

with open(DATA) as f:
    day = [Swipe(datetime.fromisoformat(f"{DAY} {r['time']}"),
                 r["card"], r["country"], int(r["usd"]))
           for r in csv.DictReader(f)]


def report(mode, e, found):
    spent = sum(x.usd for x in day
                if x.card == e.card and x.ts <= found)
    print(f"{mode}: card {e.card} flagged after "
          f"{found - e.ts}")
    print(f"  ${spent:,} spent before the alert")
