# Writes churn.csv into src/ and short/: 40 customers (seeded), plus one
# exported-twice row and one row with a missing tenure, like a real raw export.
import csv
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent

rng = np.random.default_rng(16)
rows = []
for i in range(1, 41):
    tenure = int(rng.integers(1, 61))
    calls = int(rng.poisson(1.5 + 3.5 * (tenure < 12)))
    z = 1.2 - 0.09 * tenure + 0.55 * calls
    churned = int(rng.random() < 1 / (1 + np.exp(-z)))
    rows.append([i, tenure, calls, churned])
rows.insert(9, rows[8])            # exported twice
rows.append([41, "", 2, 0])        # tenure missing
for folder in ("src", "short"):
    with open(ROOT / folder / "churn.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "tenure", "calls", "churned"])
        w.writerows(rows)
print(len(rows), "raw rows")
