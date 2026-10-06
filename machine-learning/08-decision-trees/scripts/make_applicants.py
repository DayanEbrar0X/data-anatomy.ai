# Makes data/applicants.csv: 50 past small-loan applicants and the bank's decision.
# Approval gets likely with steady income and a stable job, plus a few judgment calls.
import csv
from pathlib import Path

import numpy as np

rng = np.random.default_rng(6)
income = rng.uniform(1.5, 7.5, 50).round(1)   # monthly income, $1000s
years = rng.uniform(0.0, 9.0, 50).round(1)    # years at current job
p_income = 1 / (1 + np.exp(-4 * (income - 3.5)))
p_years = 1 / (1 + np.exp(-3 * (years - 2.0)))
approved = (rng.random(50) < p_income * p_years).astype(int)

out = Path(__file__).resolve().parents[1] / "data" / "applicants.csv"
with out.open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["income", "years", "approved"])
    w.writerows(zip(income.tolist(), years.tolist(), approved.tolist()))
print(f"wrote {len(approved)} applicants to {out.name}")
