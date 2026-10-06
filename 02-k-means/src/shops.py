# Loads the 300 shop locations as a 300 x 2 array. No labels.
from pathlib import Path

import numpy as np

DATA = Path(__file__).resolve().parents[1] / "data" / "shops.csv"
X = np.loadtxt(DATA, delimiter=",", skiprows=1)
