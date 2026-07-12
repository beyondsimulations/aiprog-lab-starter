"""Per-station summary statistics."""
from __future__ import annotations

import pandas as pd


def station_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return a per-station summary indexed by station.

    Columns: temp_mean, temp_min, temp_max, hum_mean.
    NaN-aware: pandas aggregations skip NaN, so missing humidity/temperature
    values are ignored rather than poisoning the result. Do NOT fillna here.
    """
    grouped = df.groupby("station")
    summary = pd.DataFrame(
        {
            "temp_mean": grouped["temperature"].mean(),
            "temp_min": grouped["temperature"].min(),
            "temp_max": grouped["temperature"].max(),
            "hum_mean": grouped["humidity_pct"].mean(),
        }
    )
    return summary
