# Row counts per layer, and the gold table, for medallion.py.
FIRST = ("(SELECT DISTINCT ON (event_id) * "
         "FROM 'bronze.parquet')")
REV = {}


def report(db, v):
    q = lambda s: db.sql(s).fetchone()[0]
    raw = q("SELECT count(*) FROM 'bronze.parquet'")
    if not REV:
        ids = q("SELECT count(DISTINCT event_id) FROM 'bronze.parquet'")
        print(f"bronze {raw:,} rows | {ids:,} unique, raw text")
    kept = q("SELECT count(*) FROM silver")
    fixed = q(f"""SELECT count(*) FROM silver s JOIN {FIRST} b
      USING (event_id) WHERE b.country <> s.country
      OR b.amount LIKE '$%'""")
    REV[v] = q("SELECT sum(revenue) FROM gold")
    print(f"{v} silver {kept:,} | fixed {fixed:,} | "
          f"dropped {raw - kept:,}")
    print(f"{v} gold revenue ${REV[v]:,.0f}")


def show_gold(db):
    for c, n, usd in db.sql("FROM gold ORDER BY revenue DESC").fetchall():
        print(f"gold {c}: {n:,} orders, ${usd:,.0f}")
    v1, v2 = REV.values()
    print(f"replayed from bronze: ${v1:,.0f} -> ${v2:,.0f}")
