from collections import deque
from datetime import timedelta
from swipes import day, NIGHTLY, report

WINDOW = timedelta(seconds=60)
LAG = timedelta(seconds=2)  # simulated delay

def suspicious(win, e):  # 3 in 60 s, 2+ countries
    w = win.setdefault(e.card, deque())
    w.append(e)
    while e.ts - w[0].ts > WINDOW:
        w.popleft()
    countries = {x.country for x in w}
    return len(w) >= 3 and len(countries) >= 2

# Batch: one job at 02:00 reads the whole day
win = {}
for e in day:
    if suspicious(win, e):
        report("batch", e, NIGHTLY)

# Streaming: a Kafka-style topic, simulated
topic, committed, win = [], 0, {}
for e in day:              # swipes arrive live
    topic.append(e)        # producer writes
    e = topic[committed]   # consumer reads offset
    if suspicious(win, e):
        report("stream", e, e.ts + LAG)
    committed += 1         # commit the offset
print("committed offset:", committed)
