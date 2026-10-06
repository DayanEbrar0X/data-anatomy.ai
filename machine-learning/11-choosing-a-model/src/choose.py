from sklearn.model_selection import cross_validate
from customers import load_customers
from models import candidates

df = load_customers()
print("rows, cols:", df.shape,
      "missing:", df.isna().sum().sum())
print(f"churn rate: {df.churn.mean():.0%}")

X, y = df.drop(columns="churn"), df.churn
M = ["accuracy", "recall", "precision"]
print("model     acc  rec  prec")
recall = {}
for name, clf in candidates().items():
    r = cross_validate(clf, X, y, cv=5, scoring=M)
    s = [r["test_" + m].mean() for m in M]
    recall[name] = s[1]
    print(f"{name:<9}", *[f"{v:.2f}" for v in s])

top = max(recall.values()) - 0.02  # near the best
pick = next(n for n in recall if recall[n] >= top)
print(f"pick: {pick} (recall {recall[pick]:.2f})")
