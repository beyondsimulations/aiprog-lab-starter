"""Tests for all cleaning specifications from docs/specs-cleaning.md"""
import pandas as pd
import pytest
from pathlib import Path
from pipeline.io import load_raw, clean


class TestTimestampParsing:
    """Test all three timestamp formats parse into one datetime column"""

    def test_mm_dd_yyyy_am_pm_format(self, tmp_path):
        """Test MM/DD/YYYY HH:MM AM/PM format"""
        p = tmp_path / "test.csv"
        p.write_text(
            "reading_id,station,timestamp,temperature,temp_unit,humidity_pct,wind_ms\n"
            "R0001,Alpha,03/15/2025 02:30 PM,20.0,C,50.0,5.0\n"
        )
        df = load_raw(p)
        cleaned_df, stats, _ = clean(df)
        
        # Should parse to datetime
        assert pd.api.types.is_datetime64_any_dtype(cleaned_df["timestamp"])
        # Check specific value
        expected = pd.to_datetime("2025-03-15 14:30:00")
        assert cleaned_df.loc[0, "timestamp"] == expected

    def test_yyyy_mm_dd_hh_mm_format(self, tmp_path):
        """Test YYYY-MM-DD HH:MM format"""
        p = tmp_path / "test.csv"
        p.write_text(
            "reading_id,station,timestamp,temperature,temp_unit,humidity_pct,wind_ms\n"
            "R0001,Alpha,2025-03-15 14:30,20.0,C,50.0,5.0\n"
        )
        df = load_raw(p)
        cleaned_df, stats, _ = clean(df)
        
        assert pd.api.types.is_datetime64_any_dtype(cleaned_df["timestamp"])
        expected = pd.to_datetime("2025-03-15 14:30:00")
        assert cleaned_df.loc[0, "timestamp"] == expected

    def test_dd_mm_yyyy_hh_mm_format(self, tmp_path):
        """Test DD.MM.YYYY HH:MM format"""
        p = tmp_path / "test.csv"
        p.write_text(
            "reading_id,station,timestamp,temperature,temp_unit,humidity_pct,wind_ms\n"
            "R0001,Alpha,15.03.2025 14:30,20.0,C,50.0,5.0\n"
        )
        df = load_raw(p)
        cleaned_df, stats, _ = clean(df)
        
        assert pd.api.types.is_datetime64_any_dtype(cleaned_df["timestamp"])
        expected = pd.to_datetime("2025-03-15 14:30:00")
        assert cleaned_df.loc[0, "timestamp"] == expected


class TestTemperatureConversion:
    """Test temperatures unified to °C"""

    def test_fahrenheit_to_celsius_conversion(self, tmp_path):
        """Test F to C conversion: C = (F - 32) * 5/9"""
        p = tmp_path / "test.csv"
        p.write_text(
            "reading_id,station,timestamp,temperature,temp_unit,humidity_pct,wind_ms\n"
            "R0001,Alpha,2025-03-15 14:30,32.0,F,50.0,5.0\n"  # 32°F = 0°C
            "R0002,Bravo,2025-03-15 14:30,212.0,F,50.0,5.0\n"  # 212°F = 100°C
            "R0003,Charlie,2025-03-15 14:30,50.0,C,50.0,5.0\n"  # 50°C stays 50°C
        )
        df = load_raw(p)
        cleaned_df, stats, _ = clean(df)
        
        # Check F to C conversions
        assert cleaned_df.loc[0, "temperature"] == pytest.approx(0.0, abs=0.01)
        assert cleaned_df.loc[1, "temperature"] == pytest.approx(100.0, abs=0.01)
        assert cleaned_df.loc[2, "temperature"] == pytest.approx(50.0, abs=0.01)
        
        # Check temp_unit column is dropped
        assert "temp_unit" not in cleaned_df.columns
        
        # Check stats
        assert stats["temperature_f_converted"] == 2


class TestHumidityCleaning:
    """Test humidity cleaning: empty, n/a, -99 → NaN; decimal commas parsed"""

    def test_empty_humidity_becomes_nan(self, tmp_path):
        """Test empty string humidity becomes NaN"""
        p = tmp_path / "test.csv"
        p.write_text(
            "reading_id,station,timestamp,temperature,temp_unit,humidity_pct,wind_ms\n"
            "R0001,Alpha,2025-03-15 14:30,20.0,C,,5.0\n"
        )
        df = load_raw(p)
        cleaned_df, stats, _ = clean(df)
        
        assert pd.isna(cleaned_df.loc[0, "humidity_pct"])
        assert stats["humidity_missing_values"] == 1

    def test_na_humidity_becomes_nan(self, tmp_path):
        """Test 'n/a' humidity becomes NaN"""
        p = tmp_path / "test.csv"
        p.write_text(
            "reading_id,station,timestamp,temperature,temp_unit,humidity_pct,wind_ms\n"
            "R0001,Alpha,2025-03-15 14:30,20.0,C,n/a,5.0\n"
        )
        df = load_raw(p)
        cleaned_df, stats, _ = clean(df)
        
        assert pd.isna(cleaned_df.loc[0, "humidity_pct"])
        assert stats["humidity_missing_values"] == 1

    def test_minus_99_humidity_becomes_nan(self, tmp_path):
        """Test '-99' humidity becomes NaN"""
        p = tmp_path / "test.csv"
        p.write_text(
            "reading_id,station,timestamp,temperature,temp_unit,humidity_pct,wind_ms\n"
            "R0001,Alpha,2025-03-15 14:30,20.0,C,-99,5.0\n"
        )
        df = load_raw(p)
        cleaned_df, stats, _ = clean(df)
        
        assert pd.isna(cleaned_df.loc[0, "humidity_pct"])
        assert stats["humidity_missing_values"] == 1

    def test_decimal_comma_humidity_parsed(self, tmp_path):
        """Test decimal comma in humidity is parsed (e.g., '35,5' → 35.5)"""
        p = tmp_path / "test.csv"
        p.write_text(
            "reading_id,station,timestamp,temperature,temp_unit,humidity_pct,wind_ms\n"
            'R0001,Alpha,2025-03-15 14:30,20.0,C,"35,5",5.0\n'
            'R0002,Bravo,2025-03-15 14:30,20.0,C,"70,4",5.0\n'
        )
        df = load_raw(p)
        cleaned_df, stats, _ = clean(df)
        
        assert cleaned_df.loc[0, "humidity_pct"] == pytest.approx(35.5, abs=0.01)
        assert cleaned_df.loc[1, "humidity_pct"] == pytest.approx(70.4, abs=0.01)
        assert stats["humidity_decimal_commas"] == 2

    def test_humidity_column_is_float(self, tmp_path):
        """Test humidity_pct column is float type"""
        p = tmp_path / "test.csv"
        p.write_text(
            "reading_id,station,timestamp,temperature,temp_unit,humidity_pct,wind_ms\n"
            "R0001,Alpha,2025-03-15 14:30,20.0,C,50.5,5.0\n"
        )
        df = load_raw(p)
        cleaned_df, stats, _ = clean(df)
        
        assert pd.api.types.is_float_dtype(cleaned_df["humidity_pct"])


class TestWindCleaning:
    """Test wind cleaning: 'calm' → 0.0; column numeric (float)"""

    def test_calm_wind_becomes_zero(self, tmp_path):
        """Test 'calm' wind becomes 0.0"""
        p = tmp_path / "test.csv"
        p.write_text(
            "reading_id,station,timestamp,temperature,temp_unit,humidity_pct,wind_ms\n"
            "R0001,Alpha,2025-03-15 14:30,20.0,C,50.0,calm\n"
        )
        df = load_raw(p)
        cleaned_df, stats, _ = clean(df)
        
        assert cleaned_df.loc[0, "wind_ms"] == 0.0
        assert stats["wind_calm_converted"] == 1

    def test_wind_column_is_float(self, tmp_path):
        """Test wind_ms column is float type"""
        p = tmp_path / "test.csv"
        p.write_text(
            "reading_id,station,timestamp,temperature,temp_unit,humidity_pct,wind_ms\n"
            "R0001,Alpha,2025-03-15 14:30,20.0,C,50.0,5.5\n"
        )
        df = load_raw(p)
        cleaned_df, stats, _ = clean(df)
        
        assert pd.api.types.is_float_dtype(cleaned_df["wind_ms"])


class TestStationCleaning:
    """Test station names stripped of whitespace"""

    def test_station_whitespace_stripped(self, tmp_path):
        """Test station names with leading/trailing whitespace are stripped"""
        p = tmp_path / "test.csv"
        p.write_text(
            "reading_id,station,timestamp,temperature,temp_unit,humidity_pct,wind_ms\n"
            "R0001, Alpha ,2025-03-15 14:30,20.0,C,50.0,5.0\n"
            "R0002,Bravo,2025-03-15 14:30,20.0,C,50.0,5.0\n"
        )
        df = load_raw(p)
        cleaned_df, stats, _ = clean(df)
        
        assert cleaned_df.loc[0, "station"] == "Alpha"
        assert cleaned_df.loc[1, "station"] == "Bravo"
        assert stats["station_whitespace_stripped"] == 1


class TestDuplicateRemoval:
    """Test exact duplicate rows dropped"""

    def test_duplicate_rows_dropped(self, tmp_path):
        """Test exact duplicate rows are dropped and counted"""
        p = tmp_path / "test.csv"
        p.write_text(
            "reading_id,station,timestamp,temperature,temp_unit,humidity_pct,wind_ms\n"
            "R0001,Alpha,2025-03-15 14:30,20.0,C,50.0,5.0\n"
            "R0001,Alpha,2025-03-15 14:30,20.0,C,50.0,5.0\n"
            "R0001,Alpha,2025-03-15 14:30,20.0,C,50.0,5.0\n"
            "R0002,Bravo,2025-03-15 14:30,20.0,C,50.0,5.0\n"
        )
        df = load_raw(p)
        cleaned_df, stats, _ = clean(df)
        
        # Should have 2 unique rows (1 duplicate dropped from 3, plus the unique one)
        assert len(cleaned_df) == 2
        assert stats["duplicate_rows_dropped"] == 2
        assert stats["original_rows"] == 4
        assert stats["final_rows"] == 2


class TestColumnTypes:
    """Test column types are correct"""

    def test_all_column_types(self, tmp_path):
        """Test all column types: timestamp is datetime64; temperature, humidity_pct, wind_ms are float"""
        p = tmp_path / "test.csv"
        p.write_text(
            "reading_id,station,timestamp,temperature,temp_unit,humidity_pct,wind_ms\n"
            "R0001,Alpha,2025-03-15 14:30,20.0,C,50.0,5.0\n"
        )
        df = load_raw(p)
        cleaned_df, stats, _ = clean(df)
        
        # Check timestamp is datetime64
        assert pd.api.types.is_datetime64_any_dtype(cleaned_df["timestamp"])
        
        # Check numeric columns are float
        assert pd.api.types.is_float_dtype(cleaned_df["temperature"])
        assert pd.api.types.is_float_dtype(cleaned_df["humidity_pct"])
        assert pd.api.types.is_float_dtype(cleaned_df["wind_ms"])
        
        # Check reading_id and station are string
        assert pd.api.types.is_string_dtype(cleaned_df["reading_id"])
        assert pd.api.types.is_string_dtype(cleaned_df["station"])


class TestOutputFile:
    """Test cleaned data saved to data/processed/cleaned_measurements.csv"""

    def test_output_file_created(self, tmp_path, monkeypatch):
        """Test that clean() saves output to data/processed/cleaned_measurements.csv"""
        # Create a temporary directory structure
        test_data_dir = tmp_path / "data"
        test_data_dir.mkdir()
        raw_dir = test_data_dir / "raw"
        raw_dir.mkdir()
        
        # Create test CSV
        test_csv = raw_dir / "measurements.csv"
        test_csv.write_text(
            "reading_id,station,timestamp,temperature,temp_unit,humidity_pct,wind_ms\n"
            "R0001,Alpha,2025-03-15 14:30,20.0,C,50.0,5.0\n"
        )
        
        # Change working directory to tmp_path for the test
        import os
        original_cwd = os.getcwd()
        
        try:
            os.chdir(tmp_path)
            df = load_raw(test_csv)
            cleaned_df, stats, summary = clean(df)
            
            # Check that output path is set
            output_path = Path("data/processed/cleaned_measurements.csv")
            assert output_path.exists()
            assert stats["output_path"] == str(output_path)
            
            # Check summary string contains output path
            assert "data/processed/cleaned_measurements.csv" in summary
            
        finally:
            os.chdir(original_cwd)


class TestReturnValues:
    """Test clean() function return values"""

    def test_clean_returns_tuple(self, tmp_path):
        """Test clean() returns (DataFrame, dict, str)"""
        p = tmp_path / "test.csv"
        p.write_text(
            "reading_id,station,timestamp,temperature,temp_unit,humidity_pct,wind_ms\n"
            "R0001,Alpha,2025-03-15 14:30,20.0,C,50.0,5.0\n"
        )
        df = load_raw(p)
        result = clean(df)
        
        # Should return a tuple of 3 elements
        assert isinstance(result, tuple)
        assert len(result) == 3
        
        cleaned_df, stats, summary = result
        assert isinstance(cleaned_df, pd.DataFrame)
        assert isinstance(stats, dict)
        assert isinstance(summary, str)

    def test_stats_dict_keys(self, tmp_path):
        """Test stats dict contains expected keys"""
        p = tmp_path / "test.csv"
        p.write_text(
            "reading_id,station,timestamp,temperature,temp_unit,humidity_pct,wind_ms\n"
            "R0001,Alpha,2025-03-15 14:30,20.0,C,50.0,5.0\n"
        )
        df = load_raw(p)
        cleaned_df, stats, _ = clean(df)
        
        expected_keys = [
            "original_rows", "duplicate_rows_dropped", "temperature_f_converted",
            "humidity_missing_values", "humidity_decimal_commas", "wind_calm_converted",
            "station_whitespace_stripped", "final_rows", "output_path"
        ]
        for key in expected_keys:
            assert key in stats, f"Missing key: {key}"


class TestSummaryString:
    """Test summary string content"""

    def test_summary_string_content(self, tmp_path):
        """Test summary string contains expected information"""
        p = tmp_path / "test.csv"
        p.write_text(
            "reading_id,station,timestamp,temperature,temp_unit,humidity_pct,wind_ms\n"
            "R0001,Alpha,2025-03-15 14:30,20.0,C,50.0,5.0\n"
        )
        df = load_raw(p)
        cleaned_df, stats, summary = clean(df)
        
        # Check summary contains key information
        assert "Data Cleaning Summary:" in summary
        assert "Original rows:" in summary
        assert "Final rows:" in summary
        assert "Temperature F->C conversions:" in summary
        assert "Humidity missing values" in summary
        assert "Wind 'calm' -> 0.0 conversions:" in summary
        assert "Station whitespace stripped:" in summary
