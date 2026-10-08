from shop import setup, by_region  # same data
db = setup()  # t1: customers; t2: + valid dates
db.sql("UPDATE t1 SET region='West' WHERE id=1")
db.sql("UPDATE t2 SET valid_to='2026-07-01', "
       "is_current=false WHERE id=1")
db.sql("INSERT INTO t2 VALUES (1, 'Ana', 'West', "
       "'2026-07-01', '9999-12-31', true)")
print("Q2 type 1:", by_region(db, "t1"))
print("Q2 type 2:", by_region(db, "t2"))
