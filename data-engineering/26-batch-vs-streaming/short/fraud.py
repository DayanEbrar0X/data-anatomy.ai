from swipes import day, NIGHTLY, LAG
from swipes import suspicious, report
batch, stream = {}, {}
for e in day:  # streaming: swipe by swipe, live
    if suspicious(stream, e):
        report("stream", e, e.ts + LAG)
for e in day:  # batch: the whole day at 02:00
    if suspicious(batch, e):
        report("batch", e, NIGHTLY)
