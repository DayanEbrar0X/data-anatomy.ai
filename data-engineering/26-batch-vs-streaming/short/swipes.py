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


# The fraud rule and the simulated delivery delay, exactly as in the
# full episode (src/stream.py).
from collections import deque  # noqa: E402
from datetime import timedelta  # noqa: E402

WINDOW = timedelta(seconds=60)
LAG = timedelta(seconds=2)  # simulated broker + poll delay


def suspicious(win, e):  # 3 in 60 s, 2+ countries
    w = win.setdefault(e.card, deque())
    w.append(e)
    while e.ts - w[0].ts > WINDOW:
        w.popleft()
    return len(w) >= 3 and len({x.country for x in w}) >= 2
