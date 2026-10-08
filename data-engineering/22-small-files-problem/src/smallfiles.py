import pyarrow.parquet as pq
from lake import clicks, reset, query, faster

day = clicks(4_400_000)  # one day of events
reset("tiny", "big")

# streaming: one small file per micro-batch
for i in range(5500):
    part = day.slice(i * 800, 800)
    pq.write_table(part, f"tiny/{i:04}.parquet")
slow = query("tiny")  # median of 7 runs

# compaction: read them all, write 4 big files
t = pq.read_table("tiny").combine_chunks()
for i in range(4):
    part = t.slice(i * 1_100_000, 1_100_000)
    pq.write_table(part, f"big/{i}.parquet")
fast = query("big")

faster(slow, fast)
