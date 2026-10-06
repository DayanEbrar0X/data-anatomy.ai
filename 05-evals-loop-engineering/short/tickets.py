# The eval set, the system under test (a stand-in for an LLM prompt),
# and three versions of its rules, each one fix after reading failures.
CASES = [
    ("refund my last order", "billing"),
    ("app crashes on start", "tech"),
    ("reset my password", "account"),
    ("invoice shows wrong total", "billing"),
    ("error 500 at checkout", "tech"),
    ("charged twice this month", "billing"),
    ("can't log in", "account"),
    ("upload crashes midway", "tech"),
    ("need a copy of my invoice", "billing"),
    ("page shows an error", "tech"),
]


def route(text, rules):
    for team, words in rules.items():
        if any(w in text for w in words):
            return team
    return "other"


v1 = {"billing": ["refund", "charge"], "tech": ["crash", "error"]}
v2 = {**v1, "account": ["password", "log in"]}             # fix 1
v3 = {**v2, "billing": ["refund", "charge", "invoice"]}    # fix 2
VERSIONS = [v1, v2, v3]
