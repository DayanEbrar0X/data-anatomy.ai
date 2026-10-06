# Loads the 3,000 customers (tenure, charges, tickets, contract, churn) as a pandas table.
# Empty cells in the CSV become NaN: those are the missing values the video counts.
from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data" / "customers.csv"


def load_customers():
    return pd.read_csv(DATA)
