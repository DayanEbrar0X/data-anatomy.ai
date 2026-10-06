# Loads the eval set: real tickets, each labeled with the right team.
import csv
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "cases.csv"
with DATA.open() as f:
    CASES = [tuple(row) for row in csv.reader(f)][1:]
