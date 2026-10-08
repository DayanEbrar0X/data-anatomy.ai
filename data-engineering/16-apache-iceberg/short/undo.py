from lake import table, orders, total
t = table()  # empty Iceberg table, local disk
t.append(orders)  # snapshot 1: 8 orders
t.overwrite(orders.slice(0, 3))  # buggy job
print("now:", total(t.scan()))
good = t.snapshots()[0].snapshot_id
t.manage_snapshots().rollback_to_snapshot(
    good).commit()
print("rolled back:", total(t.scan()))
