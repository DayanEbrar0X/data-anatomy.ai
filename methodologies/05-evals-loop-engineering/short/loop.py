from tickets import CASES, route, VERSIONS

for rules in VERSIONS:
    ok = [route(t, rules) == want
          for t, want in CASES]
    rate = sum(ok) / len(ok)
    print(f"{rate:.0%} pass")
