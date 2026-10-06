from loans import X, y, NAMES, LABELS

def gini(y):  # how mixed, weighted by size
    return 2 * y.mean() * (1 - y.mean()) * len(y)

def best_split(X, y):
    return min(
        (gini(y[x < t]) + gini(y[x >= t]), f, t)
        for f, x in enumerate(X.T)
        for t in sorted(set(x))[1:])

def grow(X, y, say="", d=0):  # d = depth
    vote = round(y.mean())
    if d == 2 or gini(y) == 0:
        print(say + LABELS[vote])
        return (y == vote).sum()
    _, f, t = best_split(X, y)
    q, m = f"{say}{NAMES[f]} < {t}? ", X[:, f] < t
    return (grow(X[m], y[m], q + "yes: ", d + 1)
        + grow(X[~m], y[~m], q + "no: ", d + 1))

print(f"accuracy: {grow(X, y) / len(y):.0%}")
