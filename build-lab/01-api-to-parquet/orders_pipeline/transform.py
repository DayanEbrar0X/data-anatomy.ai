import pandas as pd

def clean(rows):
    df = pd.DataFrame(rows)
    df["amount"] = df["amount"].astype(float)
    df["created"] = pd.to_datetime(df["created"])
    df = df.drop_duplicates("order_id")
    return df
