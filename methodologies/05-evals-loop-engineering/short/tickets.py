# The eval set, the system under test (a stand-in for an LLM prompt),
# and three versions of its rules, each one fix after reading failures.
import csv
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "cases.csv"
with DATA.open() as f:
    CASES = [tuple(row) for row in csv.reader(f)][1:]


def route(text, rules):
    for team, words in rules.items():
        if any(w in text for w in words):
            return team
    return "other"


v1 = {"billing": ["refund", "charge"], "tech": ["crash", "error"]}
v2 = {**v1, "account": ["password", "log in"]}             # fix 1
v3 = {**v2, "billing": ["refund", "charge", "invoice"]}    # fix 2
VERSIONS = [v1, v2, v3]
