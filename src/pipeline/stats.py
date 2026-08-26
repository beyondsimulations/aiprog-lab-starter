"""Statistical summary functions for measurements data.

This module provides functions to compute summary statistics for weather station data.
See docs/stats_module_spec.md for the full specification.
"""

from pathlib import Path
from typing import TypedDict, cast

import pandas as pd


class DateRange(TypedDict):
    """First and last timestamps represented in a dataset."""

    start: pd.Timestamp | None
    end: pd.Timestamp | None


class OutlierCounts(TypedDict):
    """Counts below and above an accepted measurement range."""

    low: int
    high: int


type OutlierReport = dict[str, OutlierCounts]


class StationActivity(TypedDict):
    """Reading counts and the most and least active stations."""

    reading_counts: dict[str, int]
    most_active: str | None
    least_active: str | None


class DataQualityReport(TypedDict):
    """Structured data quality metrics returned by data_quality_report."""

    total_readings: int
    total_stations: int
    date_range: DateRange
    completeness: dict[str, float]
    outliers: OutlierReport
    stations: StationActivity


def station_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Compute summary statistics for each weather station.
    
    Args:
        df: DataFrame containing weather station data with required columns:
            - station: Station identifier (str)
            - temperature: Temperature values (numeric or string)
            - humidity_pct: Humidity percentage values (numeric or string)
            (other columns are ignored)
    
    Returns:
        DataFrame indexed by station name with columns:
        - Temperature statistics: temp_mean, temp_max, temp_min, temp_std, temp_count
        - Humidity statistics: hum_mean, hum_max, hum_min, hum_std, hum_count
    
    Raises:
        ValueError: If required columns are missing
    """
    # Check for required columns
    required_columns = ["station", "temperature", "humidity_pct"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
    
    # Ensure we have a copy to avoid modifying the original
    df = df.copy()
    
    # Convert columns to numeric, coercing errors to NaN
    df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
    df["humidity_pct"] = pd.to_numeric(df["humidity_pct"], errors="coerce")
    
    # Group by station and compute statistics
    grouped = df.groupby("station")

    temp_stats = grouped["temperature"].agg(
        ["mean", "max", "min", "std", "count"]
    ).rename(
        columns={
            "mean": "temp_mean",
            "max": "temp_max",
            "min": "temp_min",
            "std": "temp_std",
            "count": "temp_count",
        }
    )
    hum_stats = grouped["humidity_pct"].agg(
        ["mean", "max", "min", "std", "count"]
    ).rename(
        columns={
            "mean": "hum_mean",
            "max": "hum_max",
            "min": "hum_min",
            "std": "hum_std",
            "count": "hum_count",
        }
    )

    result = pd.concat([temp_stats, hum_stats], axis=1)
    
    return result


# Stub functions for other imports (to be implemented)
def daily_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Compute daily summary statistics across all stations.
    
    Args:
        df: DataFrame with required columns:
            - timestamp: Datetime column
            - station: Station identifier
            - temperature: Temperature values
            - humidity_pct: Humidity percentage values
    
    Returns:
        DataFrame indexed by date with columns:
        - temp_mean: Mean temperature across all stations
        - temp_max: Maximum temperature across all stations
        - temp_min: Minimum temperature across all stations
        - hum_mean: Mean humidity across all stations
        - hum_max: Maximum humidity across all stations
        - hum_min: Minimum humidity across all stations
        - station_count: Number of stations reporting that day
        - reading_count: Total number of readings that day
    
    Raises:
        ValueError: If required columns are missing
    """
    # Check for required columns
    required_columns = ["timestamp", "station", "temperature", "humidity_pct"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
    
    # Ensure we have a copy to avoid modifying the original
    df = df.copy()
    
    timestamps: pd.Series[pd.Timestamp] = pd.to_datetime(df["timestamp"])
    df["timestamp"] = timestamps
    df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
    df["humidity_pct"] = pd.to_numeric(df["humidity_pct"], errors="coerce")
    df["date"] = timestamps.dt.date

    grouped = df.groupby("date")
    temp_stats = grouped["temperature"].agg(["mean", "max", "min"]).rename(
        columns={
            "mean": "temp_mean",
            "max": "temp_max",
            "min": "temp_min",
        }
    )
    hum_stats = grouped["humidity_pct"].agg(["mean", "max", "min"]).rename(
        columns={
            "mean": "hum_mean",
            "max": "hum_max",
            "min": "hum_min",
        }
    )
    
    # Compute station and reading counts
    station_count = grouped["station"].nunique().to_frame(name="station_count")
    reading_count = grouped.size().to_frame(name="reading_count")
    
    # Combine all statistics
    result = pd.concat([temp_stats, hum_stats, station_count, reading_count], axis=1)
    
    return result


def station_daily_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Compute daily summary statistics for each station (pivot table).
    
    Args:
        df: DataFrame with required columns:
            - timestamp: Datetime column
            - station: Station identifier
            - temperature: Temperature values
            - humidity_pct: Humidity percentage values
    
    Returns:
        Multi-index DataFrame with:
        - Index level 0: Station name
        - Index level 1: Date
        - Columns: Same statistics as station_summary but for each day
    
    Raises:
        ValueError: If required columns are missing
    """
    # Check for required columns
    required_columns = ["timestamp", "station", "temperature", "humidity_pct"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
    
    # Ensure we have a copy to avoid modifying the original
    df = df.copy()
    
    timestamps: pd.Series[pd.Timestamp] = pd.to_datetime(df["timestamp"])
    df["timestamp"] = timestamps
    df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
    df["humidity_pct"] = pd.to_numeric(df["humidity_pct"], errors="coerce")
    df["date"] = timestamps.dt.date

    grouped = df.groupby(["station", "date"])
    temp_stats = grouped["temperature"].agg(
        ["mean", "max", "min", "std", "count"]
    ).rename(
        columns={
            "mean": "temp_mean",
            "max": "temp_max",
            "min": "temp_min",
            "std": "temp_std",
            "count": "temp_count",
        }
    )
    hum_stats = grouped["humidity_pct"].agg(
        ["mean", "max", "min", "std", "count"]
    ).rename(
        columns={
            "mean": "hum_mean",
            "max": "hum_max",
            "min": "hum_min",
            "std": "hum_std",
            "count": "hum_count",
        }
    )

    result = pd.concat([temp_stats, hum_stats], axis=1)
    
    # Set the multi-index
    result.index.names = ["station", "timestamp"]
    
    return result


def data_quality_report(df: pd.DataFrame) -> DataQualityReport:
    """Generate a data quality report for the dataset.

    Args:
        df: DataFrame with weather station data.

    Returns:
        Counts, date range, completeness, outliers, and station activity.
    """
    working = df.copy()

    timestamps: pd.Series[pd.Timestamp] | None = None
    if "timestamp" in working.columns:
        timestamps = pd.to_datetime(working["timestamp"])
        working["timestamp"] = timestamps

    numeric_columns = [
        "temperature",
        "humidity_pct",
        "wind_ms",
        "pressure_hpa",
    ]
    for column in numeric_columns:
        if column in working.columns:
            working[column] = pd.to_numeric(working[column], errors="coerce")

    total_readings = len(working)
    total_stations = (
        working["station"].nunique() if "station" in working.columns else 0
    )

    date_range: DateRange = {"start": None, "end": None}
    if timestamps is not None and total_readings > 0:
        date_range = {"start": timestamps.min(), "end": timestamps.max()}

    completeness: dict[str, float] = {}
    for column in numeric_columns:
        if column in working.columns:
            non_null_mask: pd.Series[bool] = working[column].notna()
            non_null_count = sum(non_null_mask)
            completeness[column] = (
                non_null_count / total_readings * 100
                if total_readings > 0
                else 0.0
            )

    outliers: OutlierReport = {}
    if "temperature" in working.columns:
        temperature = cast(
            "pd.Series[float]", working["temperature"].dropna()
        )
        temperature_low: pd.Series[bool] = temperature < -50
        temperature_high: pd.Series[bool] = temperature > 60
        outliers["temperature"] = {
            "low": sum(temperature_low),
            "high": sum(temperature_high),
        }
    if "humidity_pct" in working.columns:
        humidity = cast("pd.Series[float]", working["humidity_pct"].dropna())
        humidity_low: pd.Series[bool] = humidity < 0
        humidity_high: pd.Series[bool] = humidity > 100
        outliers["humidity_pct"] = {
            "low": sum(humidity_low),
            "high": sum(humidity_high),
        }

    stations: StationActivity = {
        "reading_counts": {},
        "most_active": None,
        "least_active": None,
    }
    if "station" in working.columns and total_readings > 0:
        reading_counts = cast(
            "dict[str, int]", working["station"].value_counts().to_dict()
        )
        stations = {
            "reading_counts": reading_counts,
            "most_active": max(
                reading_counts, key=lambda station: reading_counts[station]
            ),
            "least_active": min(
                reading_counts, key=lambda station: reading_counts[station]
            ),
        }

    return {
        "total_readings": total_readings,
        "total_stations": total_stations,
        "date_range": date_range,
        "completeness": completeness,
        "outliers": outliers,
        "stations": stations,
    }


def station_rankings(df: pd.DataFrame, metric: str = "temp_mean", ascending: bool = False) -> pd.DataFrame:
    """Rank stations by a specific metric.
    
    Args:
        df: DataFrame with weather station data
        metric: Metric to rank by (default: "temp_mean")
            Valid metrics: any column from station_summary output
        ascending: Sort order (default: False = highest first)
    
    Returns:
        DataFrame with stations ranked by the specified metric, containing:
        - All columns from station_summary
        - Additional rank column with ranking (1 = highest/lowest depending on ascending)
    
    Raises:
        ValueError: If metric is invalid
    """
    # Get station summary
    summary = station_summary(df)
    
    # Check if metric is valid
    if metric not in summary.columns:
        raise ValueError(f"Invalid metric: {metric}. Valid metrics are: {', '.join(summary.columns)}")
    
    # Sort by the specified metric
    sorted_summary = summary.sort_values(by=metric, ascending=ascending)
    
    # Add rank column (handles ties properly)
    sorted_summary["rank"] = sorted_summary[metric].rank(method="min", ascending=ascending)
    
    return sorted_summary


def export_summary_report(
    df: pd.DataFrame,
    output_path: str | Path,
    format: str = "csv",
) -> Path:
    """Export a comprehensive summary report to file.
    
    Args:
        df: DataFrame with weather station data
        output_path: Path for the output file
        format: Output format ("csv", "json", "excel")
    
    Returns:
        Path to the created file
    
    Raises:
        ValueError: If format is invalid
    """
    # Convert output_path to Path object
    output_path = Path(output_path)
    
    # Validate format
    valid_formats = ["csv", "json", "excel"]
    if format not in valid_formats:
        raise ValueError(f"Invalid format: {format}. Valid formats are: {', '.join(valid_formats)}")
    
    # Create parent directories if they don't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Generate comprehensive report data
    report_data: dict[str, object] = {
        "station_summary": station_summary(df).to_dict(),
        "daily_summary": (
            daily_summary(df).to_dict() if "timestamp" in df.columns else None
        ),
        "data_quality": data_quality_report(df),
        "station_rankings": station_rankings(df).to_dict(),
    }
    
    # Export based on format
    if format == "csv":
        # For CSV, we'll export the station summary as the main report
        station_sum = station_summary(df)
        station_sum.to_csv(output_path, index=True)
    elif format == "json":
        import json

        with output_path.open("w", encoding="utf-8") as output_file:
            json.dump(report_data, output_file, indent=2, default=str)
    elif format == "excel":
        station_sum = station_summary(df)
        # pandas-stubs cannot resolve the optional Excel engine workbook type.
        station_sum.to_excel(  # pyright: ignore[reportUnknownMemberType]
            output_path, index=True
        )
    
    return output_path