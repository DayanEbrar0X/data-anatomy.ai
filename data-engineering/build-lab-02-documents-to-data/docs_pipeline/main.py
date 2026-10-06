import json
import duckdb
import pandas as pd
from ocr import ocr_folder
from parse import parse

texts = ocr_folder("invoices")
records = [parse(t) for t in texts.values()]
with open("data/docs.json", "w") as f:
    json.dump(records, f, indent=2)

df = pd.DataFrame(records)
df["date"] = pd.to_datetime(df["date"])
df.to_parquet("data/docs.parquet", index=False)
ok = df.drop(columns="text").notna()
n, t = ok.sum().sum(), ok.size
print(f"{len(df)} invoices read, {n}/{t} fields")
sql = """SELECT vendor, sum(total) AS spend
FROM 'data/docs.parquet'
GROUP BY vendor ORDER BY spend DESC LIMIT 3"""
for vendor, spend in duckdb.sql(sql).fetchall():
    print(f"{vendor:<26}{spend:>9,.2f}")
