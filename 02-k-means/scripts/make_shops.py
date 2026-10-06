# Makes data/shops.csv: 300 shop locations in three groups of 100.
# The group each shop came from is not saved, so k-means has to find it.
import csv
from pathlib import Path

import numpy as np

r = np.random.default_rng(3)
centers = [(-2.6, 1.2), (2.4, 1.6), (0.2, -1.6)]
X = np.round(np.vstack([r.normal(c, 0.55, (100, 2)) for c in centers]), 3)

out = Path(__file__).resolve().parents[1] / "data" / "shops.csv"
with out.open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["x", "y"])
    w.writerows(X.tolist())
print(f"wrote {len(X)} shops to {out.name}")
