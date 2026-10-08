import duckdb
from shop import setup

db = duckdb.connect()
setup(db)  # 3 customers, 5 sales in Q2 and Q3

def by_region(dim, q=2, asof=""):
    rows = db.sql(f"""
      SELECT region, sum(usd) FROM sales
      JOIN {dim} ON cust = id {asof}
      WHERE quarter(day) = {q}
      GROUP BY region ORDER BY region""")
    return ", ".join(f"{r} ${u:,}"
                     for r, u in rows.fetchall())

print("Q2 before:", by_region("customers"))

# Type 1: overwrite the row in place
db.sql("CREATE TABLE t1 AS FROM customers")
db.sql("UPDATE t1 SET region='West' WHERE id=1")
print("Q2 type 1:", by_region("t1"))

# Type 2: close the old row, insert a new one
db.sql("""CREATE TABLE t2 AS SELECT *,
  DATE '2000-01-01' AS valid_from,
  DATE '9999-12-31' AS valid_to,
  true AS is_current FROM customers""")
db.sql("""UPDATE t2 SET is_current = false,
  valid_to = '2026-07-01'
  WHERE id = 1 AND is_current""")
db.sql("""INSERT INTO t2 VALUES (1, 'Ana', 'West',
  '2026-07-01', '9999-12-31', true)""")
asof = "AND day >= valid_from AND day < valid_to"
print("Q3 type 2:", by_region("t2", 3, asof))
print("Q2 type 2:", by_region("t2", 2, asof))
