"""Tests for statistical summary functions in pipeline.stats module.

This test suite follows TDD principles and covers all functions specified
in docs/stats_module_spec.md.
"""

from pathlib import Path

import pandas as pd
import pytest

from pipeline.stats import (
    daily_summary,
    data_quality_report,
    export_summary_report,
    station_daily_summary,
    station_rankings,
    station_summary,
)


# =============================================================================
# Station Summary Tests
# =============================================================================

class TestStationSummary:
    """Test suite for station_summary function."""

    def test_basic_functionality(self):
        """Test basic functionality with multiple stations and values."""
        df = pd.DataFrame({
            "station": ["Alpha", "Alpha", "Bravo", "Bravo", "Charlie"],
            "temperature": [10.0, 14.0, 20.0, 25.0, 15.0],
            "humidity_pct": [50.0, 60.0, 80.0, 70.0, 55.0],
        })
        result = station_summary(df)
        
        # Check Alpha station statistics
        assert result.loc["Alpha", "temp_mean"] == pytest.approx(12.0)
        assert result.loc["Alpha", "temp_max"] == pytest.approx(14.0)
        assert result.loc["Alpha", "temp_min"] == pytest.approx(10.0)
        assert result.loc["Alpha", "temp_count"] == 2
        assert result.loc["Alpha", "hum_mean"] == pytest.approx(55.0)
        assert result.loc["Alpha", "hum_max"] == pytest.approx(60.0)
        assert result.loc["Alpha", "hum_min"] == pytest.approx(50.0)
        assert result.loc["Alpha", "hum_count"] == 2
        
        # Check Bravo station statistics
        assert result.loc["Bravo", "temp_mean"] == pytest.approx(22.5)
        assert result.loc["Bravo", "temp_max"] == pytest.approx(25.0)
        assert result.loc["Bravo", "temp_min"] == pytest.approx(20.0)
        assert result.loc["Bravo", "temp_count"] == 2
        assert result.loc["Bravo", "hum_mean"] == pytest.approx(75.0)
        
        # Check Charlie station statistics (single reading)
        assert result.loc["Charlie", "temp_mean"] == pytest.approx(15.0)
        assert result.loc["Charlie", "temp_max"] == pytest.approx(15.0)
        assert result.loc["Charlie", "temp_min"] == pytest.approx(15.0)
        assert result.loc["Charlie", "temp_count"] == 1

    def test_with_missing_values(self):
        """Test handling of missing/NaN values in the data."""
        df = pd.DataFrame({
            "station": ["Alpha", "Alpha", "Bravo"],
            "temperature": [10.0, 14.0, 20.0],
            "humidity_pct": [50.0, None, 80.0],
        })
        result = station_summary(df)
        
        # Alpha: temperature should use both values, humidity should use only one
        assert result.loc["Alpha", "temp_mean"] == pytest.approx(12.0)
        assert result.loc["Alpha", "temp_count"] == 2
        assert result.loc["Alpha", "hum_mean"] == pytest.approx(50.0)
        assert result.loc["Alpha", "hum_count"] == 1  # Only one non-NaN value
        
        # Bravo: temperature has one value, humidity has one value
        assert result.loc["Bravo", "temp_mean"] == pytest.approx(20.0)
        assert result.loc["Bravo", "hum_mean"] == pytest.approx(80.0)

    def test_with_all_missing_values_for_column(self):
        """Test handling when all values for a column are missing for a station."""
        df = pd.DataFrame({
            "station": ["Alpha", "Alpha", "Bravo"],
            "temperature": [10.0, 14.0, 20.0],
            "humidity_pct": [None, None, 80.0],
        })
        result = station_summary(df)
        
        # Alpha: temperature should work, humidity should be all NaN
        assert result.loc["Alpha", "temp_mean"] == pytest.approx(12.0)
        assert result.loc["Alpha", "hum_count"] == 0
        assert pd.isna(result.loc["Alpha", "hum_mean"])
        assert pd.isna(result.loc["Alpha", "hum_max"])
        assert pd.isna(result.loc["Alpha", "hum_min"])

    def test_single_station(self):
        """Test with only one station in the data."""
        df = pd.DataFrame({
            "station": ["Alpha", "Alpha", "Alpha"],
            "temperature": [10.0, 14.0, 18.0],
            "humidity_pct": [50.0, 60.0, 70.0],
        })
        result = station_summary(df)
        
        assert len(result) == 1
        assert result.loc["Alpha", "temp_mean"] == pytest.approx(14.0)
        assert result.loc["Alpha", "temp_max"] == pytest.approx(18.0)
        assert result.loc["Alpha", "temp_min"] == pytest.approx(10.0)
        assert result.loc["Alpha", "temp_count"] == 3

    def test_empty_dataframe(self):
        """Test with empty DataFrame."""
        df = pd.DataFrame({
            "station": pd.Series([], dtype=str),
            "temperature": pd.Series([], dtype=float),
            "humidity_pct": pd.Series([], dtype=float),
        })
        result = station_summary(df)
        
        assert len(result) == 0
        expected_columns = [
            "temp_mean", "temp_max", "temp_min", "temp_std", "temp_count",
            "hum_mean", "hum_max", "hum_min", "hum_std", "hum_count"
        ]
        assert list(result.columns) == expected_columns

    def test_string_columns_conversion(self):
        """Test that string columns are properly converted to numeric."""
        df = pd.DataFrame({
            "station": ["Alpha", "Alpha"],
            "temperature": ["10.5", "14.5"],  # String representations
            "humidity_pct": ["50", "60"],     # String representations
        })
        result = station_summary(df)
        
        assert result.loc["Alpha", "temp_mean"] == pytest.approx(12.5)
        assert result.loc["Alpha", "hum_mean"] == pytest.approx(55.0)

    def test_invalid_numeric_values(self):
        """Test handling of invalid numeric values in string columns."""
        df = pd.DataFrame({
            "station": ["Alpha", "Alpha", "Bravo"],
            "temperature": ["10.0", "invalid", "20.0"],
            "humidity_pct": ["50.0", "60.0", "80.0"],
        })
        result = station_summary(df)
        
        # Alpha: one valid temperature, two valid humidity values
        assert result.loc["Alpha", "temp_count"] == 1
        assert result.loc["Alpha", "temp_mean"] == pytest.approx(10.0)
        assert result.loc["Alpha", "hum_count"] == 2
        assert result.loc["Alpha", "hum_mean"] == pytest.approx(55.0)

    def test_result_structure(self):
        """Test that the result DataFrame has the expected structure."""
        df = pd.DataFrame({
            "station": ["Alpha", "Bravo"],
            "temperature": [10.0, 20.0],
            "humidity_pct": [50.0, 80.0],
        })
        result = station_summary(df)
        
        # Check index
        assert list(result.index) == ["Alpha", "Bravo"]
        
        # Check columns - now includes std
        expected_columns = [
            "temp_mean", "temp_max", "temp_min", "temp_std", "temp_count",
            "hum_mean", "hum_max", "hum_min", "hum_std", "hum_count"
        ]
        assert list(result.columns) == expected_columns

    def test_standard_deviation(self):
        """Test that standard deviation is calculated correctly."""
        df = pd.DataFrame({
            "station": ["Alpha", "Alpha", "Alpha"],
            "temperature": [10.0, 20.0, 30.0],  # std = 10.0
            "humidity_pct": [50.0, 50.0, 50.0],  # std = 0.0
        })
        result = station_summary(df)
        
        assert result.loc["Alpha", "temp_std"] == pytest.approx(10.0)
        assert result.loc["Alpha", "hum_std"] == pytest.approx(0.0)

    def test_original_dataframe_not_modified(self):
        """Test that the original DataFrame is not modified by the function."""
        df = pd.DataFrame({
            "station": ["Alpha", "Alpha"],
            "temperature": ["10.0", "14.0"],  # String values
            "humidity_pct": ["50.0", "60.0"],
        })
        original_dtypes = df.dtypes.copy()
        original_values = df.copy()
        
        _ = station_summary(df)
        
        # Original DataFrame should be unchanged
        assert df.equals(original_values)
        assert (df.dtypes == original_dtypes).all()

    def test_whitespace_in_station_names(self):
        """Test handling of whitespace in station names."""
        df = pd.DataFrame({
            "station": [" Alpha ", "Alpha", "Bravo"],
            "temperature": [10.0, 14.0, 20.0],
            "humidity_pct": [50.0, 60.0, 80.0],
        })
        result = station_summary(df)
        
        # Station names with whitespace should be treated as different stations
        assert " Alpha " in result.index
        assert "Alpha" in result.index
        assert "Bravo" in result.index
        assert len(result) == 3

    def test_missing_required_columns(self):
        """Test error handling when required columns are missing."""
        df = pd.DataFrame({
            "station": ["Alpha"],
            "temperature": [10.0],
            # Missing humidity_pct
        })
        
        with pytest.raises(ValueError, match="Missing required columns"):
            _ = station_summary(df)


# =============================================================================
# Daily Summary Tests
# =============================================================================

class TestDailySummary:
    """Test suite for daily_summary function."""

    def test_basic_daily_summary(self):
        """Test basic daily summary functionality."""
        dates = pd.date_range("2025-01-01", periods=3, freq="D")
        df = pd.DataFrame({
            "timestamp": [dates[0], dates[0], dates[1], dates[2]],
            "station": ["Alpha", "Bravo", "Alpha", "Bravo"],
            "temperature": [10.0, 15.0, 12.0, 18.0],
            "humidity_pct": [50.0, 60.0, 55.0, 65.0],
        })
        result = daily_summary(df)
        
        # Should have 3 rows (one for each date)
        assert len(result) == 3
        
        # Check first day
        first_day = result[result.index == dates[0].date()].iloc[0]
        assert first_day["temp_mean"] == pytest.approx(12.5)
        assert first_day["temp_max"] == pytest.approx(15.0)
        assert first_day["temp_min"] == pytest.approx(10.0)
        assert first_day["station_count"] == 2
        assert first_day["reading_count"] == 2

    def test_empty_dataframe(self):
        """Test daily summary with empty DataFrame."""
        df = pd.DataFrame({
            "timestamp": pd.Series([], dtype="datetime64[ns]"),
            "station": pd.Series([], dtype=str),
            "temperature": pd.Series([], dtype=float),
            "humidity_pct": pd.Series([], dtype=float),
        })
        result = daily_summary(df)
        
        assert len(result) == 0
        expected_columns = [
            "temp_mean", "temp_max", "temp_min",
            "hum_mean", "hum_max", "hum_min",
            "station_count", "reading_count"
        ]
        assert list(result.columns) == expected_columns

    def test_missing_required_columns(self):
        """Test error handling when required columns are missing."""
        df = pd.DataFrame({
            "timestamp": pd.date_range("2025-01-01", periods=1),
            "station": ["Alpha"],
            # Missing temperature and humidity_pct
        })
        
        with pytest.raises(ValueError, match="Missing required columns"):
            _ = daily_summary(df)


# =============================================================================
# Station Daily Summary Tests
# =============================================================================

class TestStationDailySummary:
    """Test suite for station_daily_summary function."""

    def test_basic_station_daily_summary(self):
        """Test basic station daily summary functionality."""
        dates = pd.date_range("2025-01-01", periods=2, freq="D")
        df = pd.DataFrame({
            "timestamp": [dates[0], dates[0], dates[1], dates[1]],
            "station": ["Alpha", "Bravo", "Alpha", "Bravo"],
            "temperature": [10.0, 15.0, 12.0, 18.0],
            "humidity_pct": [50.0, 60.0, 55.0, 65.0],
        })
        result = station_daily_summary(df)
        
        # Should have MultiIndex with stations and dates
        assert isinstance(result.index, pd.MultiIndex)
        assert result.index.names == ["station", "timestamp"]
        
        # Check Alpha station, first day
        indexed_result = result.reset_index()
        alpha_day1 = indexed_result[
            (indexed_result["station"] == "Alpha")
            & (indexed_result["timestamp"] == dates[0].date())
        ].iloc[0]
        assert alpha_day1["temp_mean"] == pytest.approx(10.0)
        assert alpha_day1["temp_count"] == 1

    def test_empty_dataframe(self):
        """Test station daily summary with empty DataFrame."""
        df = pd.DataFrame({
            "timestamp": pd.Series([], dtype="datetime64[ns]"),
            "station": pd.Series([], dtype=str),
            "temperature": pd.Series([], dtype=float),
            "humidity_pct": pd.Series([], dtype=float),
        })
        result = station_daily_summary(df)
        
        assert len(result) == 0


# =============================================================================
# Data Quality Report Tests
# =============================================================================

class TestDataQualityReport:
    """Test suite for data_quality_report function."""

    def test_basic_quality_report(self):
        """Test basic data quality report functionality."""
        dates = pd.date_range("2025-01-01", periods=3, freq="D")
        df = pd.DataFrame({
            "timestamp": dates,
            "station": ["Alpha", "Bravo", "Alpha"],
            "temperature": [10.0, None, 12.0],
            "humidity_pct": [50.0, 60.0, None],
            "wind_ms": [5.0, None, None],
            "pressure_hpa": [1013.0, 1015.0, 1014.0],
        })
        report = data_quality_report(df)
        
        # Check basic structure
        assert "total_readings" in report
        assert "total_stations" in report
        assert "date_range" in report
        assert "completeness" in report
        assert "outliers" in report
        assert "stations" in report
        
        # Check values
        assert report["total_readings"] == 3
        assert report["total_stations"] == 2
        assert report["date_range"]["start"] == dates[0]
        assert report["date_range"]["end"] == dates[-1]
        
        # Check completeness
        assert report["completeness"]["temperature"] == pytest.approx(2/3 * 100)
        assert report["completeness"]["humidity_pct"] == pytest.approx(2/3 * 100)
        assert report["completeness"]["wind_ms"] == pytest.approx(1/3 * 100)
        assert report["completeness"]["pressure_hpa"] == pytest.approx(100.0)

    def test_outlier_detection(self):
        """Test outlier detection in quality report."""
        df = pd.DataFrame({
            "timestamp": pd.date_range("2025-01-01", periods=4, freq="D"),
            "station": ["Alpha"] * 4,
            "temperature": [-100.0, 10.0, 20.0, 100.0],  # -100 and 100 are outliers
            "humidity_pct": [50.0, 150.0, 60.0, 70.0],   # 150 is outlier
        })
        report = data_quality_report(df)
        
        # Temperature outliers: < -50 or > 60
        assert report["outliers"]["temperature"]["low"] == 1  # -100
        assert report["outliers"]["temperature"]["high"] == 1  # 100
        
        # Humidity outliers: < 0 or > 100
        assert report["outliers"]["humidity_pct"]["low"] == 0
        assert report["outliers"]["humidity_pct"]["high"] == 1  # 150

    def test_station_activity(self):
        """Test station activity metrics in quality report."""
        df = pd.DataFrame({
            "timestamp": pd.date_range("2025-01-01", periods=5, freq="D"),
            "station": ["Alpha", "Alpha", "Alpha", "Bravo", "Charlie"],
            "temperature": [10.0, 11.0, 12.0, 15.0, 20.0],
            "humidity_pct": [50.0, 55.0, 60.0, 65.0, 70.0],
        })
        report = data_quality_report(df)
        
        assert report["stations"]["most_active"] == "Alpha"
        assert report["stations"]["least_active"] in ["Bravo", "Charlie"]
        assert report["stations"]["reading_counts"]["Alpha"] == 3
        assert report["stations"]["reading_counts"]["Bravo"] == 1
        assert report["stations"]["reading_counts"]["Charlie"] == 1

    def test_empty_dataframe(self):
        """Test quality report with empty DataFrame."""
        df = pd.DataFrame({
            "timestamp": pd.Series([], dtype="datetime64[ns]"),
            "station": pd.Series([], dtype=str),
            "temperature": pd.Series([], dtype=float),
            "humidity_pct": pd.Series([], dtype=float),
        })
        report = data_quality_report(df)
        
        assert report["total_readings"] == 0
        assert report["total_stations"] == 0


# =============================================================================
# Station Rankings Tests
# =============================================================================

class TestStationRankings:
    """Test suite for station_rankings function."""

    def test_basic_rankings(self):
        """Test basic station rankings functionality."""
        df = pd.DataFrame({
            "station": ["Alpha", "Alpha", "Bravo", "Bravo", "Charlie"],
            "temperature": [10.0, 14.0, 20.0, 25.0, 15.0],
            "humidity_pct": [50.0, 60.0, 80.0, 70.0, 55.0],
        })
        result = station_rankings(df, metric="temp_mean")
        
        # Check that rank column exists
        assert "rank" in result.columns
        
        # Check rankings (Bravo has highest temp_mean, then Charlie, then Alpha)
        assert result.loc["Bravo", "rank"] == 1
        assert result.loc["Charlie", "rank"] == 2
        assert result.loc["Alpha", "rank"] == 3

    def test_ascending_rankings(self):
        """Test ascending rankings."""
        df = pd.DataFrame({
            "station": ["Alpha", "Bravo", "Charlie"],
            "temperature": [10.0, 20.0, 15.0],
            "humidity_pct": [50.0, 80.0, 70.0],
        })
        result = station_rankings(df, metric="temp_mean", ascending=True)
        
        # Ascending: Alpha (10.0) = rank 1, Charlie (15.0) = rank 2, Bravo (20.0) = rank 3
        assert result.loc["Alpha", "rank"] == 1
        assert result.loc["Charlie", "rank"] == 2
        assert result.loc["Bravo", "rank"] == 3

    def test_tied_rankings(self):
        """Test handling of tied values in rankings."""
        df = pd.DataFrame({
            "station": ["Alpha", "Bravo", "Charlie"],
            "temperature": [15.0, 15.0, 10.0],  # Alpha and Bravo tied
            "humidity_pct": [50.0, 60.0, 70.0],
        })
        result = station_rankings(df, metric="temp_mean")
        
        # Alpha and Bravo should have same rank, Charlie next
        assert result.loc["Alpha", "rank"] == 1
        assert result.loc["Bravo", "rank"] == 1
        assert result.loc["Charlie", "rank"] == 3  # Skip rank 2

    def test_invalid_metric(self):
        """Test error handling for invalid metric."""
        df = pd.DataFrame({
            "station": ["Alpha"],
            "temperature": [10.0],
            "humidity_pct": [50.0],
        })
        
        with pytest.raises(ValueError, match="Invalid metric"):
            _ = station_rankings(df, metric="invalid_metric")

    def test_empty_dataframe(self):
        """Test rankings with empty DataFrame."""
        df = pd.DataFrame({
            "station": pd.Series([], dtype=str),
            "temperature": pd.Series([], dtype=float),
            "humidity_pct": pd.Series([], dtype=float),
        })
        result = station_rankings(df)
        
        assert len(result) == 0


# =============================================================================
# Export Summary Report Tests
# =============================================================================

class TestExportSummaryReport:
    """Test suite for export_summary_report function."""

    def test_export_csv(self, tmp_path: Path) -> None:
        """Test exporting summary report to CSV."""
        df = pd.DataFrame({
            "station": ["Alpha", "Bravo"],
            "temperature": [10.0, 20.0],
            "humidity_pct": [50.0, 80.0],
        })
        
        # Use temp directory for testing
        output_path = tmp_path / "summary_report.csv"
        result_path = export_summary_report(df, output_path, format="csv")
        
        assert result_path.exists()
        assert result_path == output_path
        
        # Check file content
        content = output_path.read_text()
        assert "station" in content
        assert "Alpha" in content

    def test_export_json(self, tmp_path: Path) -> None:
        """Test exporting summary report to JSON."""
        df = pd.DataFrame({
            "station": ["Alpha", "Bravo"],
            "temperature": [10.0, 20.0],
            "humidity_pct": [50.0, 80.0],
        })
        
        output_path = tmp_path / "summary_report.json"
        result_path = export_summary_report(df, output_path, format="json")
        
        assert result_path.exists()
        assert result_path == output_path

    def test_invalid_format(self):
        """Test error handling for invalid format."""
        df = pd.DataFrame({
            "station": ["Alpha"],
            "temperature": [10.0],
            "humidity_pct": [50.0],
        })
        
        with pytest.raises(ValueError, match="Invalid format"):
            _ = export_summary_report(df, "output.xyz", format="invalid")

    def test_creates_parent_directories(self, tmp_path: Path) -> None:
        """Test that parent directories are created if they don't exist."""
        df = pd.DataFrame({
            "station": ["Alpha"],
            "temperature": [10.0],
            "humidity_pct": [50.0],
        })
        
        output_path = tmp_path / "subdir" / "nested" / "report.csv"
        result_path = export_summary_report(df, output_path, format="csv")
        
        assert result_path.exists()
        assert (tmp_path / "subdir").exists()
        assert (tmp_path / "subdir" / "nested").exists()