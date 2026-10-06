from cases import CASES

def route(text, rules):
    for team, words in rules.items():
        if any(w in text for w in words):
            return team
    return "other"

def score(v, rules):
    fails = [t for t, want in CASES
             if route(t, rules) != want]
    rate = 1 - len(fails) / len(CASES)
    print(v, "pass rate", f"{rate:.0%}")

rules = {"billing": ["refund", "charge"],
         "tech": ["crash", "error"]}
score("v1", rules)
rules["account"] = ["password", "log in"]
score("v2", rules)
rules["billing"].append("invoice")
score("v3", rules)
