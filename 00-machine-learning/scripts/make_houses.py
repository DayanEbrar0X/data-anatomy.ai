# Makes data/houses.csv: 40 houses whose price is 3 x size + 4, plus random noise.
# The fixed seed means everyone gets the same 40 houses.
import csv
from pathlib import Path

import numpy as np

r = np.random.default_rng(7)
size = np.round(r.uniform(1, 9, 40), 2)
price = np.round(3 * size + 4 + r.normal(0, 2, 40), 2)

out = Path(__file__).resolve().parents[1] / "data" / "houses.csv"
with out.open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["size", "price"])
    w.writerows(zip(size.tolist(), price.tolist()))
print(f"wrote {len(size)} houses to {out.name}")
