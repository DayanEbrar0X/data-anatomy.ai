import duckdb
from ways import lake, warehouse, lakehouse
for way in (lake, warehouse, lakehouse):
    name = way.__name__
    try:
        usd = way().fetchone()[0]
        print(f"{name}: revenue ${usd:.2f}")
    except duckdb.Error:
        print(f"{name}: query failed")
