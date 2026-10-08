# One line of real output per role.


def report(first, df, acc, base, predict, ms):
    with open("churn.csv") as f:
        raw = sum(1 for _ in f) - 1
    print(f"engineer: {raw} raw -> {len(first)} rows, "
          f"rerun {len(df)}")
    print(f"scientist: accuracy {acc:.0%}, "
          f"guessing {base:.0%}")
    try:
        predict(-3, 2)
    except ValueError as e:
        print(f"ml engineer: (-3, 2) -> {e}")
    fast = "under" if ms < 1 else "over"
    print(f"ml engineer: p(churn) {predict(12, 2):.2f}, "
          f"{fast} 1 ms a call")
