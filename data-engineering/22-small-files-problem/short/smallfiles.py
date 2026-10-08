import pyarrow.parquet as pq
from lake import day, query, faster  # 4.4M rows
def write(d, n):  # same rows, split into n files
    size = len(day) // n
    for i in range(n):
        pq.write_table(day.slice(i * size, size),
                       f"{d}/{i}.parquet")
write("tiny", 5500); write("big", 4)
faster(query("tiny"), query("big"))
