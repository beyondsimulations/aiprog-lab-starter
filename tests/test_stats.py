"""Tests for statistical summary functions in pipeline.stats module."""

import pandas as pd
import pytest
from pipeline.stats import station_summary


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
        assert result.loc["Bravo", "hum_max"] == pytest.approx(80.0)
        assert result.loc["Bravo", "hum_min"] == pytest.approx(70.0)
        assert result.loc["Bravo", "hum_count"] == 2
        
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
        assert list(result.columns) == [
            "temp_mean", "temp_max", "temp_min", "temp_count",
            "hum_mean", "hum_max", "hum_min", "hum_count"
        ]

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
        
        # Check columns
        expected_columns = [
            "temp_mean", "temp_max", "temp_min", "temp_count",
            "hum_mean", "hum_max", "hum_min", "hum_count"
        ]
        assert list(result.columns) == expected_columns

    def test_original_dataframe_not_modified(self):
        """Test that the original DataFrame is not modified by the function."""
        df = pd.DataFrame({
            "station": ["Alpha", "Alpha"],
            "temperature": ["10.0", "14.0"],  # String values
            "humidity_pct": ["50.0", "60.0"],
        })
        original_dtypes = df.dtypes.copy()
        original_values = df.copy()
        
        result = station_summary(df)
        
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
        # (the function doesn't strip whitespace - that's the caller's responsibility)
        assert " Alpha " in result.index
        assert "Alpha" in result.index
        assert "Bravo" in result.index
        assert len(result) == 3