# 23 · Data engineer vs data scientist vs ML engineer

<img src="https://img.shields.io/badge/level-beginner-047857?style=flat-square" alt="beginner"> <img src="https://img.shields.io/badge/video-112s_%2B_38s_short-7C3AED?style=flat-square&logo=youtube&logoColor=white" alt="video 112s + 38s short"> <img src="https://img.shields.io/badge/uses-duckdb_%C2%B7_scikit--learn_%C2%B7_joblib-2563EB?style=flat-square&logo=python&logoColor=white" alt="duckdb · scikit-learn · joblib"> <img src="https://img.shields.io/badge/topic-data_engineering-0E1525?style=flat-square" alt="data engineering">

**Same data. Three jobs. Here's who builds what.** One raw churn export of 42 rows goes through three functions,
one per role. The data engineer turns it into a clean, typed table of 40 customers that stays at 40 when the job
reruns. The data scientist fits a model that gets 90% of unseen customers right, where always guessing gets 50%.
The ML engineer saves the model, serves it behind a `predict` that rejects bad input, and scores a new customer at
0.85 in under a millisecond.

Watch: [YouTube](https://www.youtube.com/@datanatomyai) · [TikTok](https://www.tiktok.com/@datanatomy.ai) · [Instagram](https://www.instagram.com/datanatomy.ai) (112 seconds, plus a 38-second short)

<br clear="right">

## The idea

Think of a restaurant: one person preps the ingredients, one invents the dish, one runs the kitchen. A data team
splits the work the same way, and each role hands its output to the next:

1. **Data engineer**: raw files in, a table people can trust out. Duplicates removed, bad rows skipped, every column
   given a real type, and safe to rerun on a schedule.
2. **Data scientist**: a question in ("who churns?"), a model and an honest measurement out. The model is scored on
   customers it never saw, against a baseline.
3. **ML engineer**: a model in, a service out. Saved, loaded the way a server would load it, guarded against bad
   input, and fast enough to call from an app.

## Run it

You need `duckdb`, `pandas`, `scikit-learn` and `joblib` (`pip install duckdb pandas scikit-learn joblib`). Like the
video, `roles.py` opens `churn.csv` by its file name, so run it from inside `src/`:

```bash
cd src
python3 roles.py
```

```
engineer: 42 raw -> 40 rows, rerun 40
scientist: accuracy 90%, guessing 50%
ml engineer: (-3, 2) -> bad input
ml engineer: p(churn) 0.85, under 1 ms a call
```

The run writes `src/churn.joblib`, the saved model. It is generated, so it is not committed. The speed line depends
on your machine: here, 1,000 calls took 0.18 seconds in total.

`src/churn.csv` is already included. To regenerate it (same seed, same rows), run `python3 scripts/make_churn.py`
from the lesson folder. It writes the same file into `src/` and `short/`.

## The short version

The short (`short/three_jobs.py`, 9 lines) imports the three role functions instead of showing them, and runs the
same hand-off: engineer, scheduled rerun, scientist, ML engineer. Same data, same output:

```bash
cd short
python3 three_jobs.py
```

```
engineer: 42 raw -> 40 rows, rerun 40
scientist: accuracy 90%, guessing 50%
ml engineer: (-3, 2) -> bad input
ml engineer: p(churn) 0.85, under 1 ms a call
```

## Files

```
23-data-engineer-vs-data-scientist-vs-ml-engineer/
├── scripts/
│   └── make_churn.py     writes churn.csv into src/ and short/ (seeded, 42 raw rows)
├── src/
│   ├── roles.py          the code from the video
│   ├── report.py         prints one line of real output per role
│   ├── churn.csv         the raw export: id, tenure, calls, churned
│   └── churn.joblib      the saved model, written by the run, not committed
├── short/
│   ├── three_jobs.py     the 9-line version from the short
│   ├── roles.py          the three role functions, without the lines that run them
│   ├── report.py         same as src/report.py
│   └── churn.csv         same as src/churn.csv
└── .gitignore            keeps churn.joblib out of git
```

`churn.csv` sits next to the code because the on-screen file reads it by name, exactly as in the video. `short/`
has its own copy of everything it needs, so it runs on its own. The printing lives in `report.py` so `roles.py`
can show only the three jobs.

The raw export has 40 customers (tenure in months, support calls, churned or not) and the two kinds of mess a real
export has. Customer 9 was exported twice, and customer 41 has no tenure:

```
id,tenure,calls,churned
...
8,25,2,0
9,44,3,0
9,44,3,0
10,5,7,1
...
41,,2,0
```

## The code

`src/roles.py`, line by line:

| Line | Code | What it does |
|------|------|--------------|
| 1 to 3 | imports | `time` for the speed check, DuckDB for the engineer, `joblib` to save the model, scikit-learn's linear models for the scientist, and `report` to print the results. |
| 4 | `X = ["tenure", "calls"]` | The two input columns (features) the model learns from. |
| 6 | `def engineer(db):` | The data engineer: raw file in, typed table out. |
| 7 | `CREATE OR REPLACE TABLE churn AS` | Builds the table from scratch each run. That makes the step idempotent: run it twice and you get the same table, not twice the rows. |
| 8 | `SELECT DISTINCT id::INT id,` | `DISTINCT` drops the second copy of customer 9. `::INT` casts the text to a whole number. |
| 9 to 10 | `tenure::INT tenure, calls::INT calls,` / `churned::BOOL churned` | Every column gets a real type. `0` and `1` become `false` and `true`. |
| 11 | `FROM read_csv('churn.csv', all_varchar=1)` | Reads every column as text, the safest way to load a file you don't trust yet. The casts above decide the types, not DuckDB's guess. |
| 12 | `WHERE tenure <> ''` | Skips the row with no tenure. 42 raw rows become 40. |
| 13 | `return db.sql("FROM churn ORDER BY id").df()` | Hands the clean table to the next role as a pandas DataFrame. |
| 15 | `def scientist(df):` | The data scientist: a question in, a model and a metric out. |
| 16 to 17 | `test = df.id % 4 == 0` / `tr, te = df[~test], df[test]` | Every fourth customer (10 of 40) is held out as a test set. The model trains on the other 30. |
| 18 to 19 | `m = lm.LogisticRegression()` / `m.fit(...)` | A logistic regression learns how tenure and support calls relate to churn. |
| 20 | `acc = m.score(te[X].values, te.churned)` | Accuracy on the 10 unseen customers: 9 right, 90%. |
| 21 | `p = te.churned.mean()` | The share of test customers who churned (5 of 10). |
| 22 | `return m, acc, max(p, 1 - p)` | The baseline is the accuracy of always guessing the more common answer: 50%. A model has to beat it to be worth anything. |
| 24 | `def ml_engineer(m):` | The ML engineer: model in, safe and fast service out. |
| 25 to 26 | `joblib.dump(...)` / `model = joblib.load(...)` | Save the model to a file, then load it back, the way a server would at startup. |
| 27 to 29 | `def predict(tenure, calls):` ... `raise ValueError("bad input")` | The service refuses negative values instead of returning a confident-looking guess. |
| 30 to 31 | `return model.predict_proba([[tenure, calls]])[0, 1]` | Returns the probability that this customer churns. |
| 32 to 33 | `t0 = time.perf_counter()` / `for _ in range(1000): predict(12, 2)` | A speed check: a thousand calls, timed. |
| 34 | `ms = time.perf_counter() - t0  # s / 1000 = ms` | Total seconds for 1,000 calls is the same number as milliseconds per call, so no division is needed. |
| 35 | `return predict, ms` | Hands back the service and its speed. |
| 37 | `db = duckdb.connect()` | An in-memory DuckDB database. |
| 38 to 39 | `first = engineer(db)` / `df = engineer(db)` | The pipeline runs twice, the second time like a scheduler rerunning it. Both give 40 rows. |
| 40 to 41 | `scientist(df)`, `ml_engineer(m)` | Each role takes the previous role's output. |
| 42 | `report(first, df, acc, base, predict, ms)` | Prints one line per role. |

`report.py` counts the raw lines in `churn.csv` (minus the header), prints both table sizes, the accuracy and the
baseline, then calls `predict(-3, 2)` to show the rejection, and `predict(12, 2)` for a new customer with 12 months
of tenure and 2 support calls.

## A gotcha on line 12: the empty tenure is NULL

`WHERE tenure <> ''` works, but not for the reason it seems to. Even with `all_varchar=1`, DuckDB reads an empty
CSV field as `NULL`, not as an empty string. `NULL <> ''` is neither true nor false, it is `NULL`, and `WHERE` only
keeps rows where the condition is true, so the row is dropped. The clearer way to say what you mean is
`WHERE tenure IS NOT NULL`. Neither check catches a missing value written as text, like `n/a`: the row is kept and
the `::INT` cast on line 9 fails with a `ConversionException`. `WHERE TRY_CAST(tenure AS INT) IS NOT NULL` skips any
tenure that is not a whole number.

`DISTINCT` on line 8 has a limit too: it only removes rows that are identical in every column. If the second copy of
customer 9 had a different call count, both rows would stay. A real pipeline deduplicates on the key (`id`).

## What the video simplified

- **The roles blur in real teams.** All three write Python and SQL. Data scientists build pipelines, and ML
  engineers train models. Titles vary by company, so look at what each role owns: trusted data, a tested answer, and
  a model running in production.
- **The scientist's evaluation is tiny.** 10 test customers means one mistake moves accuracy by 10 points. Real work
  uses more data, cross-validation, and metrics like precision and recall when one class is rare.
- **The ML engineer's service is a function.** In production it sits behind an HTTP endpoint, with input validation
  on every field, logging, monitoring for drift, and a versioned model file. Only load model files you trust:
  `joblib.load` can run code from the file.

## Try this

1. Change line 12 to `WHERE tenure IS NOT NULL`. Is the output the same? Now edit the last row of `churn.csv` to
   `41,n/a,2,0`. What error do you get, and how would you change line 12 to skip that row?
2. Change line 7 to `CREATE TABLE churn AS`. What happens on the rerun in line 39, and why does `OR REPLACE` matter
   for a scheduled job?
3. Change the second copy of customer 9 to `9,44,4,0`. How many rows does the engineer keep now?
4. Call `predict(1, 8)` and `predict(55, 0)`. Which customer is more likely to churn, and does that match how the
   data was made in `scripts/make_churn.py`?

---
Previous: [22 · The small files problem](../22-small-files-problem) · Next: [24 · Lake vs warehouse vs lakehouse](../24-lake-vs-warehouse-vs-lakehouse) · [All lessons](../../README.md)
