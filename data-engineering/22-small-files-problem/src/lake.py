# Helpers for the small files demo: the click events, empty folders,
# a timed DuckDB query (one thread, 3 warm-ups, then the median CPU
# time of 7 runs), and rounded reporting.
# Timings depend on the machine; they are rounded so the printed
# numbers stay stable from run to run.
import os
import shutil
import statistics
import time

import duckdb
import pyarrow as pa
import pyarrow.parquet as pq

COUNTRIES = ["US", "DE", "IN", "BR", "JP", "FR", "GB", "CA", "MX", "AU"]
SQL = ("SELECT country, sum(amount) FROM '{}/*.parquet' "
       "GROUP BY country")


def clicks(n):
    # deterministic events: id, country, amount
    i = pa.array(range(n), pa.int64())
    country = pa.array([COUNTRIES[k * 7 % 10] for k in range(n)])
    amount = pa.array([(k * 37 % 500) / 10 for k in range(n)])
    return pa.table({"id": i, "country": country, "amount": amount})


def reset(*dirs):
    for d in dirs:
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)


def size(kb):
    return f"{kb / 1000:.1f} MB" if kb >= 1000 else f"{kb:.0f} KB"


def ms(x):  # wide buckets: steady on a busy machine
    if x >= 100:
        return f"about {round(x / 250) * 0.25:g} s"
    return "under 50 ms" if x < 50 else f"about {round(x, -1):.0f} ms"


def query(d, runs=7):
    files = sorted(os.listdir(d))
    mb = sum(os.path.getsize(f"{d}/{f}") for f in files) / 1e6
    kb = sum(pq.read_metadata(f"{d}/{f}").serialized_size
             for f in files) / 1e3
    os.sync()  # finish pending writes before timing
    db = duckdb.connect()
    db.sql("SET threads = 1")  # one core: steadier timings
    times = []
    for _ in range(3):  # warm-up runs, not counted
        db.sql(SQL.format(d)).fetchall()
    for _ in range(runs):
        t0 = time.process_time()  # CPU time: steady on a busy machine
        db.sql(SQL.format(d)).fetchall()
        times.append((time.process_time() - t0) * 1000)
    med = statistics.median(times)
    print(f"{d}: {len(files):,} files, {mb:.1f} MB")
    print(f"  footers {size(kb)} | query {ms(med)}")
    return med


def faster(slow, fast):
    x = slow / fast
    print(f"compacted: over {x // 10 * 10:.0f}x faster")
