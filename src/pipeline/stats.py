"""Statistical summary functions for measurements data.

This module provides functions to compute summary statistics for weather station data.
See docs/stats_module_spec.md for the full specification.
"""

import pandas as pd
from pathlib import Path
from typing import Union
from datetime import datetime


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
    
    # Compute temperature statistics
    temp_stats = grouped["temperature"].agg([
        ("temp_mean", "mean"),
        ("temp_max", "max"),
        ("temp_min", "min"),
        ("temp_std", "std"),
        ("temp_count", "count")
    ])
    
    # Compute humidity statistics
    hum_stats = grouped["humidity_pct"].agg([
        ("hum_mean", "mean"),
        ("hum_max", "max"),
        ("hum_min", "min"),
        ("hum_std", "std"),
        ("hum_count", "count")
    ])
    
    # Combine the statistics
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
    
    # Convert timestamp to datetime if it's not already
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    
    # Convert columns to numeric, coercing errors to NaN
    df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
    df["humidity_pct"] = pd.to_numeric(df["humidity_pct"], errors="coerce")
    
    # Extract date from timestamp for grouping
    df["date"] = df["timestamp"].dt.date
    
    # Group by date and compute statistics
    grouped = df.groupby("date")
    
    # Compute temperature statistics
    temp_stats = grouped["temperature"].agg([
        ("temp_mean", "mean"),
        ("temp_max", "max"),
        ("temp_min", "min")
    ])
    
    # Compute humidity statistics
    hum_stats = grouped["humidity_pct"].agg([
        ("hum_mean", "mean"),
        ("hum_max", "max"),
        ("hum_min", "min")
    ])
    
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
    
    # Convert timestamp to datetime if it's not already
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    
    # Convert columns to numeric, coercing errors to NaN
    df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
    df["humidity_pct"] = pd.to_numeric(df["humidity_pct"], errors="coerce")
    
    # Extract date from timestamp for grouping
    df["date"] = df["timestamp"].dt.date
    
    # Group by station and date
    grouped = df.groupby(["station", "date"])
    
    # Compute temperature statistics
    temp_stats = grouped["temperature"].agg([
        ("temp_mean", "mean"),
        ("temp_max", "max"),
        ("temp_min", "min"),
        ("temp_std", "std"),
        ("temp_count", "count")
    ])
    
    # Compute humidity statistics
    hum_stats = grouped["humidity_pct"].agg([
        ("hum_mean", "mean"),
        ("hum_max", "max"),
        ("hum_min", "min"),
        ("hum_std", "std"),
        ("hum_count", "count")
    ])
    
    # Combine the statistics
    result = pd.concat([temp_stats, hum_stats], axis=1)
    
    # Set the multi-index
    result.index.names = ["station", "timestamp"]
    
    return result


def data_quality_report(df: pd.DataFrame) -> dict:
    """Generate a data quality report for the dataset.
    
    Args:
        df: DataFrame with weather station data
    
    Returns:
        Dictionary containing:
        - total_readings: int
        - total_stations: int
        - date_range: {"start": datetime, "end": datetime}
        - completeness: dict with percentage of non-null values for each column
        - outliers: dict with low/high outlier counts for temperature and humidity
        - stations: dict with most_active, least_active, and reading_counts
    """
    # Ensure we have a copy to avoid modifying the original
    df = df.copy()
    
    # Convert timestamp to datetime if it exists and is not already
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    
    # Convert numeric columns to numeric, coercing errors to NaN
    numeric_cols = ["temperature", "humidity_pct", "wind_ms", "pressure_hpa"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    
    # Basic counts
    total_readings = len(df)
    total_stations = df["station"].nunique() if "station" in df.columns else 0
    
    # Date range
    date_range = {}
    if "timestamp" in df.columns and total_readings > 0:
        date_range["start"] = df["timestamp"].min()
        date_range["end"] = df["timestamp"].max()
    else:
        date_range["start"] = None
        date_range["end"] = None
    
    # Completeness
    completeness = {}
    for col in numeric_cols:
        if col in df.columns:
            non_null_count = df[col].notna().sum()
            completeness[col] = (non_null_count / total_readings * 100) if total_readings > 0 else 0.0
    
    # Outliers
    outliers = {}
    if "temperature" in df.columns:
        temp_valid = df["temperature"].dropna()
        outliers["temperature"] = {
            "low": (temp_valid < -50).sum(),
            "high": (temp_valid > 60).sum()
        }
    if "humidity_pct" in df.columns:
        hum_valid = df["humidity_pct"].dropna()
        outliers["humidity_pct"] = {
            "low": (hum_valid < 0).sum(),
            "high": (hum_valid > 100).sum()
        }
    
    # Station activity
    stations = {}
    if "station" in df.columns and total_readings > 0:
        reading_counts = df["station"].value_counts().to_dict()
        stations["reading_counts"] = reading_counts
        stations["most_active"] = max(reading_counts, key=reading_counts.get)
        stations["least_active"] = min(reading_counts, key=reading_counts.get)
    else:
        stations["reading_counts"] = {}
        stations["most_active"] = None
        stations["least_active"] = None
    
    return {
        "total_readings": total_readings,
        "total_stations": total_stations,
        "date_range": date_range,
        "completeness": completeness,
        "outliers": outliers,
        "stations": stations
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


def export_summary_report(df: pd.DataFrame, output_path: Union[str, Path], format: str = "csv") -> Path:
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
    report_data = {
        "station_summary": station_summary(df).to_dict(),
        "daily_summary": daily_summary(df).to_dict() if "timestamp" in df.columns else None,
        "data_quality": data_quality_report(df),
        "station_rankings": station_rankings(df).to_dict()
    }
    
    # Export based on format
    if format == "csv":
        # For CSV, we'll export the station summary as the main report
        station_sum = station_summary(df)
        station_sum.to_csv(output_path, index=True)
    elif format == "json":
        import json
        with open(output_path, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
    elif format == "excel":
        station_sum = station_summary(df)
        station_sum.to_excel(output_path, index=True)
    
    return output_path