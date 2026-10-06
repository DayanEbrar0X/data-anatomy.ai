# Loads the facts: rows from purchasing (ERP), product data (PLM)
# and orders (CRM), written as (subject, relation, object) triples.
import csv
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "facts.csv"
with DATA.open() as f:
    FACTS = [tuple(row) for row in csv.reader(f)][1:]
