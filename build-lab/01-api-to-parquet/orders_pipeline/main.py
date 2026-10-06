import duckdb
from pathlib import Path
from fetch import fetch_orders
from transform import clean

PQ = "data/orders.parquet"
rows = fetch_orders()
df = clean(rows)
df.to_parquet(PQ, index=False)

kb = lambda p: Path(p).stat().st_size / 1024
j = sum(kb(p) for p in Path("api").glob("*"))
print(len(rows), "rows fetched,", len(df), "kept")
print(f"JSON {j:.1f} KB -> Parquet {kb(PQ):.1f} KB")
sql = f"SELECT status, count(*) FROM '{PQ}'"
sql += " GROUP BY 1 ORDER BY 1"
print(duckdb.sql(sql).fetchall())
