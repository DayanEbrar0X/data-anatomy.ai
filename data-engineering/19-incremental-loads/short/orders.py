# The source system and the warehouse around the load.
# night_one(): 1,000,000 orders, loaded in full, and the
# high-watermark saved. day_two(): 200 changes land in
# the source, one of them late (stamped before the mark).
import duckdb


def night_one():
    db = duckdb.connect()
    db.sql("""CREATE TABLE src AS
      SELECT i AS id, (i * 7919) % 50000 / 100 AS usd,
        TIMESTAMP '2026-09-08'
          + to_milliseconds(i * 2592) AS updated_at
      FROM range(1, 1_000_001) t(i)""")  # 30 days
    db.sql("CREATE TABLE wh AS FROM src")
    db.sql("CREATE TABLE state AS "
           "SELECT max(updated_at) AS wm FROM wh")
    return db


def day_two(db):
    # 150 updates to existing orders, during Oct 8
    db.sql("""UPDATE src SET usd = usd + 5,
        updated_at = TIMESTAMP '2026-10-08 06:00'
          + to_minutes((id % 600)::BIGINT)
      WHERE id IN (SELECT k * 6661 % 1_000_000 + 1
                   FROM range(1, 151) t(k))""")
    # 49 new orders during Oct 8
    db.sql("""INSERT INTO src SELECT 1_000_000 + k,
        k * 3 + 0.99, TIMESTAMP '2026-10-08 09:00'
          + to_minutes(k::BIGINT)
      FROM range(1, 50) t(k)""")
    # 1 late arrival: a phone that was offline syncs
    # an order it took at 23:40, after the load ran
    db.sql("""INSERT INTO src VALUES (1_000_050, 42.5,
        TIMESTAMP '2026-10-07 23:40')""")
    return db


def report(db, name, read, wrote):
    diff = db.sql("""SELECT count(*) FROM (
      (FROM src EXCEPT FROM wh)
      UNION ALL (FROM wh EXCEPT FROM src))""").fetchone()[0]
    print(f"{name}: read {read:,}, wrote {wrote:,}, "
          f"match {diff == 0}")
