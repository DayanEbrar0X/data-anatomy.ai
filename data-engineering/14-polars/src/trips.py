import polars as pl

trips = pl.scan_parquet("trips.parquet")

query = (
    trips.filter(pl.col("month") == 12)
    .with_columns(
        tip_pct=pl.col("tip") / pl.col("fare")
    )
    .group_by("zone")
    .agg(pl.len(), pl.col("tip_pct").mean())
    .sort("tip_pct", descending=True)
)

for line in query.explain().splitlines()[-3:-1]:
    print(line.strip())

df = query.collect()
for zone, n, tip in df.head(3).iter_rows():
    print(f"{zone:<9} {n:,} trips  {tip:.1%} tip")
print("Best tippers in December:", df["zone"][0])
