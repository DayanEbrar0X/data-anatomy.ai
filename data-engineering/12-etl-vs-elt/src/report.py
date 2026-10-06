# Prints what each warehouse holds after its pipeline ran.


def summary(name, db):
    tables = [t for (t,) in db.sql("SHOW TABLES").fetchall()]
    n, total = db.sql(
        "SELECT count(*), sum(amount) FROM orders").fetchone()
    pii = db.sql("SELECT count(*) FROM information_schema.columns "
                 "WHERE column_name = 'email'").fetchone()[0] > 0
    print(f"{name} orders: {n} rows, total ${total:,.2f}")
    print(f"{name} tables: {', '.join(tables)}")
    return round(total, 2), pii


def report(etl, elt):
    etl_total, etl_pii = summary("ETL", etl)
    elt_total, elt_pii = summary("ELT", elt)
    kept = [n for n, pii in [("ETL", etl_pii), ("ELT", elt_pii)] if pii]
    print(f"same total: {etl_total == elt_total} | "
          f"raw + PII kept: {', '.join(kept) or 'none'}")
