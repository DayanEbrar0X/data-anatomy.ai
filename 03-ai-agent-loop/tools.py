# Two tools the agent can call. In a company these would be real APIs.
WAREHOUSE = {"Q3 revenue": 4_200_000, "Q2 revenue": 3_900_000}


def search(query):
    return f"{query}: {WAREHOUSE[query]}"


def calculator(expr):
    a, b = expr.split(" * ")
    return float(a) * float(b)
