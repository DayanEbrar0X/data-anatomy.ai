from shop import source, triggers, snap, diff, DAY
src = source()          # orders 1 and 2: 'new'
triggers(src)           # every write -> changes
yday = snap(src)        # last night's snapshot
src.executescript(DAY)  # six writes today
seen = diff(yday, snap(src))
log = list(src.execute("SELECT * FROM changes"))
print(f"nightly diff: {len(seen)} of {len(log)}"
      f" | cdc: {len(log)} of {len(log)}")
