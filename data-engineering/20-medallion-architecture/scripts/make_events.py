# Writes events.csv into src/ and short/: 10,000 raw order events from three apps, with
# real-world mess. 400 are retries (same event_id sent twice), country codes come in mixed
# case and padding, the web app sends amounts as "$12.50", and a few rows are unreadable.
import csv
import random
from pathlib import Path

LESSON = Path(__file__).resolve().parent.parent
OUTS = [LESSON / "src" / "events.csv", LESSON / "short" / "events.csv"]

rng = random.Random(6)
COUNTRIES = ["US", "DE", "IN", "BR"]
rows = []
for i in range(9_600):
    cc = rng.choice(COUNTRIES)
    r = rng.random()
    country = cc if r < 0.7 else (f" {cc.lower()}" if r < 0.85 else cc.title() + " ")
    cents = rng.randint(500, 25_000)
    app = rng.choice(["ios", "android", "web"])
    amount = f"${cents / 100:.2f}" if app == "web" else f"{cents / 100:.2f}"
    ts = f"2026-10-07 {rng.randint(0, 23):02d}:{rng.randint(0, 59):02d}:{rng.randint(0, 59):02d}"
    bad = rng.random()
    if bad < 0.012:
        amount = rng.choice(["N/A", "", "null"])
    elif bad < 0.02:
        ts = rng.choice(["", "not-a-date", "07/10/2026 25:61"])
    rows.append({"event_id": f"e{i:05d}", "ts": ts, "country": country, "amount": amount})
for j in rng.sample(range(9_600), 400):  # retries: the same event sent again
    rows.append(dict(rows[j]))
rng.shuffle(rows)
for out in OUTS:
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
print(f"wrote src/events.csv and short/events.csv: {len(rows):,} rows each")
