import time, duckdb, joblib
from sklearn import linear_model as lm
from report import report
X = ["tenure", "calls"]

def engineer(db):  # raw file -> typed table
    db.sql("""CREATE OR REPLACE TABLE churn AS
      SELECT DISTINCT id::INT id,
        tenure::INT tenure, calls::INT calls,
        churned::BOOL churned
      FROM read_csv('churn.csv', all_varchar=1)
      WHERE tenure <> ''""")
    return db.sql("FROM churn ORDER BY id").df()

def scientist(df):  # question -> model + metric
    test = df.id % 4 == 0
    tr, te = df[~test], df[test]
    m = lm.LogisticRegression()
    m.fit(tr[X].values, tr.churned)
    acc = m.score(te[X].values, te.churned)
    p = te.churned.mean()  # always-guess baseline
    return m, acc, max(p, 1 - p)

def ml_engineer(m):  # model -> safe, fast service
    joblib.dump(m, "churn.joblib")
    model = joblib.load("churn.joblib")
    def predict(tenure, calls):
        if tenure < 0 or calls < 0:
            raise ValueError("bad input")
        return model.predict_proba(
            [[tenure, calls]])[0, 1]
    t0 = time.perf_counter()
    for _ in range(1000): predict(12, 2)
    ms = time.perf_counter() - t0  # s / 1000 = ms
    return predict, ms

db = duckdb.connect()
first = engineer(db)
df = engineer(db)  # the scheduler reruns it
m, acc, base = scientist(df)
predict, ms = ml_engineer(m)
report(first, df, acc, base, predict, ms)
