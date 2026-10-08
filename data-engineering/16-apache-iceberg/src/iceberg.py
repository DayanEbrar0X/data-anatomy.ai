from lake import catalog, orders, total

cat = catalog()  # SQLite catalog + local folder
t = cat.create_table("shop.orders",
                     schema=orders.schema)
t.append(orders)  # tonight's 8 orders

bad = orders.slice(0, 3)  # a buggy job lost rows
t.overwrite(bad)  # replaces the whole table

for n, s in enumerate(t.snapshots(), 1):
    op = s.summary.operation.value
    print(f"snap {n} {op}:",
          s.summary["total-records"], "rows")

good = t.snapshots()[0].snapshot_id
print("now:", total(t.scan()))
print("snap 1:", total(t.scan(snapshot_id=good)))

t.manage_snapshots().rollback_to_snapshot(
    good).commit()
print("rolled back:", total(t.scan()))
