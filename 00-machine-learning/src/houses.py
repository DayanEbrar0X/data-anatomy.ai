# Loads the 40 example houses: x is the size, y is the price.
from pathlib import Path

import numpy as np

DATA = Path(__file__).resolve().parents[1] / "data" / "houses.csv"
x, y = np.loadtxt(DATA, delimiter=",", skiprows=1, unpack=True)
