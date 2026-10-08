# A fresh local Iceberg table for every run: a SQLite
# catalog (lake.db) + a warehouse folder of Parquet files,
# both created next to this file. Same orders as src/.
import shutil
from pathlib import Path

import pyarrow.compute as pc
import pyarrow.csv as pv
from pyiceberg.catalog.sql import SqlCatalog

HERE = Path(__file__).resolve().parent
DB = HERE / "lake.db"
WAREHOUSE = HERE / "warehouse"

# 8 orders, Oct 7
orders = pv.read_csv(HERE.parent / "data" / "orders.csv")


def table():
    shutil.rmtree(WAREHOUSE, ignore_errors=True)
    DB.unlink(missing_ok=True)
    WAREHOUSE.mkdir()
    cat = SqlCatalog(
        "lake", uri=f"sqlite:///{DB}",
        warehouse=WAREHOUSE.as_uri())
    cat.create_namespace("shop")
    return cat.create_table("shop.orders",
                            schema=orders.schema)


def total(scan):
    rows = scan.to_arrow()
    usd = pc.sum(rows["usd"]).as_py() or 0
    return f"{rows.num_rows} rows, ${usd:,}"
