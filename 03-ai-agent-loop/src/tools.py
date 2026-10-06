# Two tools the agent can call. In a company these would be real APIs.
import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "warehouse.json"
WAREHOUSE = json.loads(DATA.read_text())


def search(query):
    return f"{query}: {WAREHOUSE[query]}"


def calculator(expr):
    a, b = expr.split(" * ")
    return float(a) * float(b)
