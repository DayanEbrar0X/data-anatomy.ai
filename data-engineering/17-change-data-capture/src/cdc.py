from shop import source, target, DAY

src = source()  # orders 1 and 2, both 'new'
SNAP = "SELECT id, status FROM orders"
yday = dict(src.execute(SNAP))

# one trigger per write: our stand-in for the WAL
for op, row in [("INSERT", "NEW.id, NEW.status"),
                ("UPDATE", "NEW.id, NEW.status"),
                ("DELETE", "OLD.id, NULL")]:
    src.execute(f"""CREATE TRIGGER log_{op}
      AFTER {op} ON orders BEGIN
      INSERT INTO changes(op, id, status)
      VALUES ('{op}', {row}); END""")

src.executescript(DAY)  # six writes

# the nightly job: diff two snapshots
night = dict(src.execute(SNAP))
diff = {k: night.get(k) for k in yday | night
        if yday.get(k) != night.get(k)}

# CDC: replay the log, in order
log = list(src.execute(
    "SELECT op, id, status FROM changes "
    "ORDER BY seq"))
tgt = target(yday)
UPSERT = ("INSERT INTO orders VALUES (?, ?) ON "
          "CONFLICT(id) DO UPDATE SET status=?")
DELETE = "DELETE FROM orders WHERE id = ?"
for op, k, st in log:
    if op == "DELETE":
        tgt.execute(DELETE, [k])
    else:
        tgt.execute(UPSERT, [k, st, st])

missed = [s for _, k, s in log if diff[k] != s]
print(f"changes today: {len(log)}")
print("diff missed:", ", ".join(missed))
same = dict(tgt.execute(SNAP)) == night
print(f"target matches source: {same}")
print(f"nightly diff: {len(diff)} of {len(log)}"
      f" | cdc: {len(log)} of {len(log)}")
