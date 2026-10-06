"""Write src/trips.parquet: 1.2 million seeded taxi trips, one row group per month."""
from pathlib import Path

import numpy as np
import polars as pl

OUT = Path(__file__).resolve().parent.parent / "src" / "trips.parquet"
ZONES = ["Airport", "Downtown", "Harbor", "Midtown", "Uptown", "Old Town"]
TIP_PCT = np.array([17.0, 15.5, 13.0, 14.5, 19.0, 12.0])  # typical tip % per zone
PER_MONTH = 100_000

rng = np.random.default_rng(14)
n = PER_MONTH * 12
zone = rng.integers(0, len(ZONES), n)
distance = np.round(rng.gamma(2.0, 2.5, n) + 0.3, 2)
fare = np.round(3.0 + 1.9 * distance + rng.normal(0, 1.0, n).clip(-2, 2), 2)
tip_pct = (TIP_PCT[zone] + rng.normal(0, 4.0, n)).clip(0, None)

trips = pl.DataFrame({
    "trip_id": np.arange(n),
    "month": np.repeat(np.arange(1, 13), PER_MONTH),  # trips are stored in time order
    "hour": rng.integers(0, 24, n),
    "zone": np.array(ZONES)[zone],
    "passengers": rng.integers(1, 5, n),
    "distance_km": distance,
    "fare": fare,
    "tip": np.round(fare * tip_pct / 100, 2),
})
trips.write_parquet(OUT, row_group_size=PER_MONTH)
print(f"wrote {OUT.name}: {trips.height:,} rows x {trips.width} columns")
