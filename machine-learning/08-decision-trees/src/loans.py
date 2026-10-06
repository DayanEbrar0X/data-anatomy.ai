# Loads the 50 loan applicants.
# X[:, 0] = monthly income in $1000s, X[:, 1] = years at current job.
# y = 1 if the loan was approved, 0 if declined.
from pathlib import Path

import numpy as np

NAMES = ["income", "years"]
LABELS = ["declined", "approved"]

DATA = Path(__file__).resolve().parents[1] / "data" / "applicants.csv"
table = np.loadtxt(DATA, delimiter=",", skiprows=1)
X = table[:, :2]
y = table[:, 2].astype(int)
