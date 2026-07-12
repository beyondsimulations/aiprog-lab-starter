"""Load and clean raw field-study measurements."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

# The three timestamp formats used across the raw file.
_TIMESTAMP_FORMATS = (
    "%Y-%m-%d %H:%M",
    "%d.%m.%Y %H:%M",
    "%m/%d/%Y %I:%M %p",
)

# Values that mean "missing" for humidity.
_HUMIDITY_MISSING = {"", "n/a", "-99"}


def load_raw(path: str | Path) -> pd.DataFrame:
    """Read the raw CSV as strings (no type coercion) and return it."""
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def _parse_timestamp(value: str) -> pd.Timestamp:
    value = value.strip()
    for fmt in _TIMESTAMP_FORMATS:
        try:
            return pd.to_datetime(value, format=fmt)
        except (ValueError, TypeError):
            continue
    raise ValueError(f"unrecognized timestamp format: {value!r}")


def _parse_humidity(value: str) -> float:
    value = value.strip().lower()
    if value in _HUMIDITY_MISSING:
        return float("nan")
    # European decimal comma -> dot.
    return float(value.replace(",", "."))


def _parse_wind(value: str) -> float:
    value = value.strip()
    if value.lower() == "calm":
        return 0.0
    return float(value)


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned copy of the raw frame, fixing every data problem."""
    df = df.copy()

    # (f) drop exact duplicate rows.
    df = df.drop_duplicates()

    # (e) strip whitespace in station names.
    df["station"] = df["station"].str.strip()

    # (a) parse all three timestamp formats into one datetime column.
    df["timestamp"] = df["timestamp"].map(_parse_timestamp)

    # (b) convert F -> C using temp_unit, then drop temp_unit.
    temp = df["temperature"].astype(float)
    is_f = df["temp_unit"].str.strip().str.upper() == "F"
    temp = temp.where(~is_f, (temp - 32.0) * 5.0 / 9.0)
    df["temperature"] = temp.astype(float)
    df = df.drop(columns=["temp_unit"])

    # (c) humidity: missing sentinels -> NaN, decimal commas -> float.
    df["humidity_pct"] = df["humidity_pct"].map(_parse_humidity)

    # (d) wind: "calm" -> 0.0, numeric float column.
    df["wind_ms"] = df["wind_ms"].map(_parse_wind)

    return df.reset_index(drop=True)
