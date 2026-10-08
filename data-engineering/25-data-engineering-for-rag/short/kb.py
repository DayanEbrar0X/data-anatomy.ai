# The knowledge base as two daily exports of the same
# help-center docs (data/docs/day1, data/docs/day2), and a fresh
# LanceDB table so every demo run starts from empty.
import shutil
from pathlib import Path

import lancedb
import pyarrow as pa

DOCS = Path(__file__).resolve().parents[1] / "data" / "docs"
STORE = Path(__file__).resolve().parent / "store"  # generated


def load(day):
    docs = []
    for f in sorted((DOCS / day).glob("*.md")):
        head, text = f.read_text().split("\n", 1)
        docs.append({"source": f.name, "text": text,
                     "updated_at": head.split(": ")[1]})
    return docs


def new_table():
    shutil.rmtree(STORE, ignore_errors=True)
    schema = pa.schema([
        ("id", pa.string()), ("text", pa.string()),
        ("vector", pa.list_(pa.float32(), 384)),
        ("source", pa.string()), ("updated_at", pa.string()),
        ("hash", pa.string())])
    return lancedb.connect(str(STORE)).create_table(
        "chunks", schema=schema)
