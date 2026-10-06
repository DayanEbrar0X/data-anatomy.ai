# Makes data/customers.csv: 3,000 customers of a subscription company, about 20% of whom churned.
# Churn risk rises with monthly contracts, higher charges, more support tickets and short tenure,
# plus a little extra for new customers on pricey plans. A few values are blanked out on purpose.
from pathlib import Path

import numpy as np
import pandas as pd

n = 3000
rng = np.random.default_rng(11)
contract = rng.choice(["monthly", "one_year", "two_year"],
                      size=n, p=[0.55, 0.25, 0.20])
tenure = rng.integers(1, 73, size=n).astype(float)
charges = rng.normal(70, 22, size=n).clip(20, 120).round(2)
tickets = rng.poisson(1.2, size=n)
logit = (-2.9 - 0.035 * tenure + 0.02 * charges + 0.45 * tickets
         + np.select([contract == "monthly", contract == "one_year"],
                     [1.0, -0.2], -1.2)
         + 1.0 * ((tenure < 12) & (charges > 80)))  # new + pricey
churn = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
df = pd.DataFrame({"tenure": tenure, "monthly_charges": charges,
                   "support_tickets": tickets, "contract": contract,
                   "churn": churn})
# real exports have gaps: a few customers miss charges or tenure
df.loc[rng.random(n) < 0.03, "monthly_charges"] = np.nan
df.loc[rng.random(n) < 0.02, "tenure"] = np.nan

out = Path(__file__).resolve().parents[1] / "data" / "customers.csv"
df.to_csv(out, index=False)
print(f"wrote {len(df)} customers to {out.name}")
