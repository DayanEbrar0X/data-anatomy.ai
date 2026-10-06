# Writes src/orders.csv: a small, seeded raw export with real-world mess.
# amount is text with a "$", one order was exported twice,
# and email is personal data (PII).
import csv
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "src" / "orders.csv"

rng = random.Random(12)
NAMES = ["ana", "ben", "chen", "dina", "eli", "fay", "gus"]

rows = []
for i, name in enumerate(NAMES, start=101):
    cents = rng.randint(1500, 25000)
    rows.append({"order_id": str(i),
                 "amount": f"${cents / 100:.2f}",
                 "email": f"{name}@mail.com"})
rows.insert(4, dict(rows[3]))  # the duplicate export

with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
print(f"wrote {OUT.name}: {len(rows)} rows")
