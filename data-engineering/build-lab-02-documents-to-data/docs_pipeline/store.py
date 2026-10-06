import lancedb
import pandas as pd
from embed import embed


def build_index():
    df = pd.read_parquet("data/docs.parquet")
    df["vector"] = embed(df["text"].tolist())
    db = lancedb.connect("data/lancedb")
    return db.create_table("invoices", df,
                           mode="overwrite")
