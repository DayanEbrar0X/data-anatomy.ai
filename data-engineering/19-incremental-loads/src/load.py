from orders import night_one, day_two, report

def full(db, _):
    n = db.execute("CREATE OR REPLACE TABLE wh "
                   "AS FROM src").fetchone()[0]
    return n, n  # read all, write all

def incremental(db, minutes):
    read = db.execute("""CREATE TABLE new AS
      FROM src WHERE updated_at > (SELECT wm
        FROM state) - INTERVAL (?) MINUTE""",
      [minutes]).fetchone()[0]
    wrote = db.execute("""MERGE INTO wh
      USING new USING (id) WHEN MATCHED
      AND new.updated_at > wh.updated_at
      THEN UPDATE WHEN NOT MATCHED THEN INSERT
      """).fetchone()[0]
    db.sql("UPDATE state SET wm = "
           "(SELECT max(updated_at) FROM wh)")
    return read, wrote

for name, load, minutes in [
        ("full", full, 0),
        ("watermark", incremental, 0),
        ("lookback 1h", incremental, 60)]:
    db = night_one()  # 1M rows loaded, wm saved
    day_two(db)       # 200 changes, 1 late
    report(db, name, *load(db, minutes))
