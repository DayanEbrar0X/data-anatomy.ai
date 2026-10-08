# The same six shop events, plus one bad write: an amount
# typed as text with a comma ("12,50"). Helpers for the
# three storage styles in three_ways.py.
import contextlib
import io
import os
import shutil

import pyarrow as pa
from pyiceberg.catalog.sql import SqlCatalog

DAY1 = [{"id": 1, "kind": "view", "usd": 0.0},
        {"id": 2, "kind": "buy", "usd": 19.5},
        {"id": 3, "kind": "view", "usd": 0.0}]
DAY2 = [{"id": 4, "kind": "buy", "usd": 42.0},
        {"id": 5, "kind": "view", "usd": 0.0},
        {"id": 6, "kind": "buy", "usd": 13.0}]
BAD = [{"id": 7, "kind": "buy", "usd": "12,50"}]
SCHEMA = pa.schema([("id", pa.int64()), ("kind", pa.string()),
                    ("usd", pa.float64())])


def fresh(path):
    shutil.rmtree(path, ignore_errors=True)
    os.makedirs(path)


def append(table, rows):
    """One Iceberg commit. The rows are typed only by what they hold,
    so a text amount reaches the table's schema check and is refused
    (pyiceberg also prints a field diff table; we keep it quiet)."""
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            table.append(pa.Table.from_pylist(rows))
        return True
    except ValueError:
        return False


def catalog(path):
    """A local Iceberg catalog: SQLite for commits, files for data."""
    fresh(path)
    cat = SqlCatalog("local", uri=f"sqlite:///{path}/catalog.db",
                     warehouse=f"file://{os.path.abspath(path)}")
    cat.create_namespace("shop")
    return cat
