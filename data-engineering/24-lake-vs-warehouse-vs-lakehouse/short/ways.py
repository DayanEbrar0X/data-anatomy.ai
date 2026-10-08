# The three storage functions from ../src/three_ways.py, without the loop that runs them.
import os, json, duckdb
from pyiceberg.types import StringType
from store import DAY1, DAY2, BAD, SCHEMA
from store import fresh, catalog, append
SUM = "SELECT sum(usd) FROM "

def lake():  # files in a folder, schema on read
    fresh("lake")
    for i, rows in enumerate([DAY1, DAY2, BAD]):
        with open(f"lake/{i}.json", "w") as f:
            json.dump(rows, f)  # any shape lands
    n = len(os.listdir("lake"))
    print(f"lake: {n} files written")
    return duckdb.sql(SUM + "'lake/*.json'")

def warehouse():  # typed table, schema on write
    db = duckdb.connect("shop.duckdb")
    db.sql("""CREATE OR REPLACE TABLE events
      (id INT, kind TEXT, usd DOUBLE)""")
    for rows in (DAY1, DAY2, BAD):
        try:
            db.executemany("INSERT INTO events "
                "VALUES ($id, $kind, $usd)", rows)
        except duckdb.Error:
            print("warehouse: bad rows rejected")
    return db.sql(SUM + "events")

def lakehouse():  # Iceberg: Parquet + metadata
    cat = catalog("lakehouse")
    t = cat.create_table("shop.events", SCHEMA)
    for rows in (DAY1, DAY2, BAD):
        if not append(t, rows):  # 1 commit each
            print("lakehouse: bad rows rejected")
    with t.update_schema() as s:  # schema change
        s.add_column("country", StringType())
    v1 = t.snapshots()[0].snapshot_id
    then = t.scan(snapshot_id=v1).to_arrow()
    n = len(t.snapshots())
    print(f"lakehouse: {n} commits, "
          f"commit 1 had {then.num_rows} rows")
    now = t.scan().to_arrow()
    return duckdb.sql(SUM + "now")
