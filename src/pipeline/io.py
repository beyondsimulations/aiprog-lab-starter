"""Data loading and cleaning pipeline for measurements data.

This module provides functions to load and clean the raw measurements CSV data,
handling various edge cases like mixed timestamp formats, temperature units,
and missing/invalid values.
"""

from pathlib import Path
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    import pandas as pd


def load_raw(path: str | Path) -> "pd.DataFrame":
    """Load raw measurements CSV file into a pandas DataFrame.

    Args:
        path: Path to the CSV file, relative to project root.

    Returns:
        DataFrame containing the raw data with all columns.

    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.ParserError: If the CSV file is malformed.
    """
    import pandas as pd

    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_csv(file_path, dtype=str, keep_default_na=False)
    return df


def clean(df: "pd.DataFrame") -> tuple["pd.DataFrame", dict[str, int | str], str]:
    """Clean the raw measurements DataFrame.

    Performs the following cleaning operations:
    - Parse all timestamp formats into a single datetime64 column
    - Convert temperatures from Fahrenheit to Celsius, then drop temp_unit column
    - Clean humidity: empty, "n/a", -99 -> NaN; replace decimal commas
    - Convert wind: "calm" -> 0.0
    - Strip whitespace from station names
    - Drop exact duplicate rows
    - Ensure correct dtypes for all columns

    Args:
        df: Raw DataFrame from load_raw().

    Returns:
        Tuple of (cleaned DataFrame, summary_dict, summary_string).
    """
    import pandas as pd

    # Make a copy to avoid modifying the original
    cleaned = df.copy()

    # Track cleaning statistics
    stats: dict[str, int | str] = {
        "original_rows": len(cleaned),
        "duplicate_rows_dropped": 0,
        "temperature_f_converted": 0,
        "humidity_missing_values": 0,
        "humidity_decimal_commas": 0,
        "wind_calm_converted": 0,
        "station_whitespace_stripped": 0,
    }

    # 1. Parse timestamps - three formats:
    # MM/DD/YYYY HH:MM AM/PM, YYYY-MM-DD HH:MM, DD.MM.YYYY HH:MM
    timestamp_formats = [
        "%m/%d/%Y %I:%M %p",  # MM/DD/YYYY HH:MM AM/PM
        "%Y-%m-%d %H:%M",  # YYYY-MM-DD HH:MM
        "%d.%m.%Y %H:%M",  # DD.MM.YYYY HH:MM
    ]

    def parse_timestamp(ts: str) -> pd.Timestamp | None:
        """Try to parse timestamp with multiple formats."""
        for fmt in timestamp_formats:
            try:
                return pd.to_datetime(ts, format=fmt)
            except ValueError:
                continue
        return None

    cleaned["timestamp"] = cleaned["timestamp"].apply(parse_timestamp)
    # Any that failed to parse will be None, which pandas will convert to NaT

    # 2. Convert temperatures from F to C
    # First, identify F rows
    f_mask = cleaned["temp_unit"] == "F"
    stats["temperature_f_converted"] = int(f_mask.sum())

    # Convert temperature column to numeric first
    cleaned["temperature"] = pd.to_numeric(cleaned["temperature"], errors="coerce")

    # Convert F to C using: C = (F - 32) * 5/9
    f_temps = cast(
        "pd.Series[float]", cleaned.loc[f_mask, "temperature"].copy()
    )
    cleaned.loc[f_mask, "temperature"] = ((f_temps - 32) * 5 / 9).round(2)

    # Drop temp_unit column
    cleaned = cleaned.drop(columns=["temp_unit"])

    # 3. Clean humidity
    # Replace empty, "n/a", -99 with NaN
    humidity_missing_mask = (
        (cleaned["humidity_pct"] == "")
        | (cleaned["humidity_pct"] == "n/a")
        | (cleaned["humidity_pct"] == "-99")
    )
    stats["humidity_missing_values"] = int(humidity_missing_mask.sum())

    # Replace decimal commas (e.g., "35,5" -> "35.5")
    def clean_humidity(val: str) -> str:
        if "," in val and "." not in val:
            # Replace comma with dot
            return val.replace(",", ".")
        return val

    # Track decimal comma replacements
    humidity_before = cleaned["humidity_pct"].copy()
    cleaned["humidity_pct"] = cleaned["humidity_pct"].apply(clean_humidity)
    # Count how many values had commas replaced
    # Use regex=False to avoid regex special characters (dot matches any char in regex)
    decimal_comma_mask = (humidity_before.str.contains(",", regex=False) & ~humidity_before.str.contains(".", regex=False))
    stats["humidity_decimal_commas"] = int(decimal_comma_mask.sum())

    # Now set missing values to NaN
    cleaned.loc[humidity_missing_mask, "humidity_pct"] = None

    # 4. Convert wind: "calm" -> 0.0
    calm_mask = cleaned["wind_ms"] == "calm"
    stats["wind_calm_converted"] = int(calm_mask.sum())
    cleaned.loc[calm_mask, "wind_ms"] = "0.0"

    # 5. Strip whitespace from station names
    station_before = cleaned["station"].copy()
    cleaned["station"] = cleaned["station"].str.strip()
    stats["station_whitespace_stripped"] = int(
        (station_before != cleaned["station"]).sum()
    )

    # 6. Drop exact duplicate rows
    duplicate_mask: pd.Series[bool] = cleaned.duplicated()
    stats["duplicate_rows_dropped"] = sum(duplicate_mask)
    cleaned = cleaned.drop_duplicates()

    # 7. Ensure correct dtypes
    cleaned["timestamp"] = pd.to_datetime(cleaned["timestamp"])
    cleaned["temperature"] = pd.to_numeric(cleaned["temperature"], errors="coerce")
    cleaned["humidity_pct"] = pd.to_numeric(cleaned["humidity_pct"], errors="coerce")
    cleaned["wind_ms"] = pd.to_numeric(cleaned["wind_ms"], errors="coerce")

    # 8. Save to data/processed/cleaned_measurements.csv
    output_path = Path("data/processed/cleaned_measurements.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(output_path, index=False)

    # Build summary string
    summary_lines = [
        "Data Cleaning Summary:",
        f"  Original rows: {stats['original_rows']}",
        f"  Duplicate rows dropped: {stats['duplicate_rows_dropped']}",
        f"  Final rows: {len(cleaned)}",
        f"  Temperature F->C conversions: {stats['temperature_f_converted']}",
        f"  Humidity missing values (empty, n/a, -99): {stats['humidity_missing_values']}",
        f"  Wind 'calm' -> 0.0 conversions: {stats['wind_calm_converted']}",
        f"  Station whitespace stripped: {stats['station_whitespace_stripped']}",
        f"  Cleaned data saved to: {output_path}",
    ]
    summary_str = "\n".join(summary_lines)

    # Add final stats to dict
    stats["final_rows"] = len(cleaned)
    stats["output_path"] = str(output_path)

    return cleaned, stats, summary_str
