import duckdb
from roles import engineer, scientist, ml_engineer
from report import report
db = duckdb.connect()
first = engineer(db)          # data engineer
df = engineer(db)             # scheduled rerun
m, acc, base = scientist(df)  # data scientist
predict, ms = ml_engineer(m)  # ML engineer
report(first, df, acc, base, predict, ms)
