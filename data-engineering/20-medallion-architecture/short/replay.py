import duckdb
from medallion import bronze, silver, gold
from layers import report
db = duckdb.connect()
bronze(db)  # raw events, kept untouched
silver(db, "amount"); gold(db); report(db, "v1")
silver(db, "ltrim(amount, '$')"); gold(db)
report(db, "v2")  # the fix, replayed from bronze
