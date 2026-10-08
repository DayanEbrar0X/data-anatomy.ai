from orders import night_one, day_two, report
db = day_two(night_one())  # 1M rows + 200 changes
read = db.execute("""CREATE TABLE new AS FROM src
  WHERE updated_at > (SELECT wm FROM state)
  - INTERVAL 1 HOUR""").fetchone()[0]
report(db, "lookback 1h", read, db.execute("""
  MERGE INTO wh USING new USING (id) WHEN MATCHED
  AND new.updated_at > wh.updated_at THEN UPDATE
  WHEN NOT MATCHED THEN INSERT""").fetchone()[0])
