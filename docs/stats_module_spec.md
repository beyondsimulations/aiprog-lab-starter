# Statistics Module Specification

## Overview

The `pipeline.stats` module provides statistical analysis functions for weather station measurement data. This specification defines the functionality, inputs, outputs, and edge cases for all statistical functions in the module.

**Status**: ✅ Completed (TDD Approach)

---

## Module Purpose

Compute comprehensive summary statistics and analytical insights from cleaned weather station data, supporting:

- [x] Basic descriptive statistics (mean, max, min, count, std)
- [x] Time-based aggregations (daily, monthly, yearly)
- [x] Station comparisons and rankings
- [x] Data quality metrics
- [x] Exportable reports

---

## Functions

### 1. `station_summary(df: pd.DataFrame) -> pd.DataFrame`

**Purpose**: Compute summary statistics for each weather station.

**Status**: ✅ Completed

**Inputs**:
- [x] `df`: DataFrame containing weather station data with required columns:
  - [x] `station`: Station identifier (str)
  - [x] `temperature`: Temperature values (numeric or string)
  - [x] `humidity_pct`: Humidity percentage values (numeric or string)
  - [x] Optional: `timestamp`, `wind_ms`, `pressure_hpa` (ignored if present)

**Outputs**:
- [x] DataFrame indexed by station name with columns:
  - [x] Temperature statistics:
    - [x] `temp_mean`: Mean temperature (°C)
    - [x] `temp_max`: Maximum temperature (°C)
    - [x] `temp_min`: Minimum temperature (°C)
    - [x] `temp_std`: Standard deviation of temperature (°C)
    - [x] `temp_count`: Number of valid temperature readings
  - [x] Humidity statistics:
    - [x] `hum_mean`: Mean humidity (%)
    - [x] `hum_max`: Maximum humidity (%)
    - [x] `hum_min`: Minimum humidity (%)
    - [x] `hum_std`: Standard deviation of humidity (%)
    - [x] `hum_count`: Number of valid humidity readings

**Behavior**:
- [x] Automatically converts string columns to numeric (coerces errors to NaN)
- [x] Handles missing/NaN values gracefully
- [x] Does not modify the original DataFrame
- [x] Preserves station name case and whitespace
- [x] Returns empty DataFrame with correct columns if input is empty

**Edge Cases**:
- [x] Empty DataFrame → Returns empty DataFrame with expected columns
- [x] Single station → Returns single-row DataFrame
- [x] All NaN values for a column → Returns NaN for statistics, 0 for count
- [x] Mixed valid/invalid values → Uses only valid values for calculations
- [x] String representations of numbers → Converts to numeric

**Tests**:
- [x] Test basic functionality with multiple stations and values
- [x] Test handling of missing/NaN values in the data
- [x] Test handling when all values for a column are missing for a station
- [x] Test with only one station in the data
- [x] Test with empty DataFrame
- [x] Test that string columns are properly converted to numeric
- [x] Test handling of invalid numeric values in string columns
- [x] Test that the result DataFrame has the expected structure
- [x] Test standard deviation calculation
- [x] Test that the original DataFrame is not modified
- [x] Test handling of whitespace in station names
- [x] Test error handling when required columns are missing

---

### 2. `daily_summary(df: pd.DataFrame) -> pd.DataFrame`

**Purpose**: Compute daily summary statistics across all stations.

**Status**: ✅ Completed

**Inputs**:
- [x] `df`: DataFrame with required columns:
  - [x] `timestamp`: Datetime column
  - [x] `station`: Station identifier
  - [x] `temperature`: Temperature values
  - [x] `humidity_pct`: Humidity percentage values

**Outputs**:
- [x] DataFrame indexed by date with columns:
  - [x] `temp_mean`: Mean temperature across all stations
  - [x] `temp_max`: Maximum temperature across all stations
  - [x] `temp_min`: Minimum temperature across all stations
  - [x] `hum_mean`: Mean humidity across all stations
  - [x] `hum_max`: Maximum humidity across all stations
  - [x] `hum_min`: Minimum humidity across all stations
  - [x] `station_count`: Number of stations reporting that day
  - [x] `reading_count`: Total number of readings that day

**Behavior**:
- [x] Groups data by date (ignoring time component)
- [x] Computes statistics across all stations for each day
- [x] Handles missing dates (no data for a day = no row in output)

**Tests**:
- [x] Test basic daily summary functionality
- [x] Test daily summary with empty DataFrame
- [x] Test error handling when required columns are missing

---

### 3. `station_daily_summary(df: pd.DataFrame) -> pd.DataFrame`

**Purpose**: Compute daily summary statistics for each station (pivot table).

**Status**: ✅ Completed

**Inputs**:
- [x] Same as `daily_summary`

**Outputs**:
- [x] Multi-index DataFrame with:
  - [x] Index level 0: Station name
  - [x] Index level 1: Date
  - [x] Columns: Same statistics as `station_summary` but for each day

**Behavior**:
- [x] Creates a pivot-style summary with stations as rows and dates as columns
- [x] Facilitates station comparison over time

**Tests**:
- [x] Test basic station daily summary functionality
- [x] Test station daily summary with empty DataFrame

---

### 4. `data_quality_report(df: pd.DataFrame) -> dict`

**Purpose**: Generate a data quality report for the dataset.

**Status**: ✅ Completed

**Inputs**:
- [x] `df`: DataFrame with weather station data

**Outputs**:
- [x] Dictionary containing:
  ```python
  {
      "total_readings": int,
      "total_stations": int,
      "date_range": {"start": datetime, "end": datetime},
      "completeness": {
          "temperature": float,  # percentage of non-null values
          "humidity_pct": float,
          "wind_ms": float,
          "pressure_hpa": float
      },
      "outliers": {
          "temperature": {"low": int, "high": int},
          "humidity_pct": {"low": int, "high": int}
      },
      "stations": {
          "most_active": str,      # station with most readings
          "least_active": str,     # station with fewest readings
          "reading_counts": dict   # station -> reading count
      }
  }
  ```

**Behavior**:
- [x] Defines outliers as values outside reasonable ranges:
  - [x] Temperature: < -50°C or > 60°C
  - [x] Humidity: < 0% or > 100%
- [x] Calculates data completeness as percentage of non-null values
- [x] Identifies most and least active stations

**Tests**:
- [x] Test basic data quality report functionality
- [x] Test outlier detection in quality report
- [x] Test station activity metrics in quality report
- [x] Test quality report with empty DataFrame

---

### 5. `station_rankings(df: pd.DataFrame, metric: str = "temp_mean", ascending: bool = False) -> pd.DataFrame`

**Purpose**: Rank stations by a specific metric.

**Status**: ✅ Completed

**Inputs**:
- [x] `df`: DataFrame with weather station data
- [x] `metric`: Metric to rank by (default: "temp_mean")
  - [x] Valid metrics: any column from `station_summary` output
- [x] `ascending`: Sort order (default: False = highest first)

**Outputs**:
- [x] DataFrame with stations ranked by the specified metric, containing:
  - [x] All columns from `station_summary`
  - [x] Additional `rank` column with ranking (1 = highest/lowest depending on `ascending`)

**Behavior**:
- [x] Uses `station_summary` internally to get statistics
- [x] Handles ties by assigning same rank, then skipping next rank(s)
- [x] Example: ranks 1, 1, 3 for tied first place

**Tests**:
- [x] Test basic station rankings functionality
- [x] Test ascending rankings
- [x] Test handling of tied values in rankings
- [x] Test error handling for invalid metric
- [x] Test rankings with empty DataFrame

---

### 6. `export_summary_report(df: pd.DataFrame, output_path: str | Path, format: str = "csv") -> Path`

**Purpose**: Export a comprehensive summary report to file.

**Status**: ✅ Completed

**Inputs**:
- [x] `df`: DataFrame with weather station data
- [x] `output_path`: Path for the output file
- [x] `format`: Output format ("csv", "json", "excel")

**Outputs**:
- [x] Path to the created file

**Behavior**:
- [x] Creates a comprehensive report including:
  - [x] Overall statistics
  - [x] Station summaries
  - [x] Data quality metrics
  - [x] Station rankings
- [x] Saves to the specified format
- [x] Creates parent directories if they don't exist
- [x] Validates output path is within project directory

**Tests**:
- [x] Test exporting summary report to CSV
- [x] Test exporting summary report to JSON
- [x] Test error handling for invalid format
- [x] Test that parent directories are created if they don't exist

---

## Data Assumptions

- [x] **Temperature**: Values in Celsius (°C), numeric
- [x] **Humidity**: Values as percentage (0-100), numeric
- [x] **Station Names**: String identifiers, may contain spaces/special characters
- [x] **Timestamps**: Datetime objects or parseable strings
- [x] **Missing Values**: Represented as NaN, None, or empty strings

## Error Handling

- [x] **Missing Required Columns**: Raise `ValueError` with descriptive message
- [x] **Invalid Data Types**: Attempt conversion, raise `TypeError` if impossible
- [x] **Empty DataFrame**: Return appropriate empty structure (not an error)
- [x] **Invalid Output Paths**: Raise `ValueError` for paths outside project root

## Dependencies

- [x] `pandas` for DataFrame operations
- [x] `pathlib` for path manipulation
- [x] Standard library only (no additional dependencies)

## Testing Requirements

- [x] Each function must have comprehensive test coverage including:
  - [x] Basic functionality tests
  - [x] Edge case tests (empty, single value, all NaN)
  - [x] Error handling tests
  - [x] Data type conversion tests
  - [x] Side effect tests (original DataFrame unchanged)
  - [ ] Performance tests for large datasets (>10,000 rows)

---

## Implementation Checklist

### Phase 1: Core Functionality
- [x] Implement `station_summary()` function
- [x] All `TestStationSummary` tests passing

### Phase 2: Time-based Analysis
- [x] Implement `daily_summary()` function
- [x] Implement `station_daily_summary()` function
- [x] All daily summary tests passing

### Phase 3: Quality & Rankings
- [x] Implement `data_quality_report()` function
- [x] Implement `station_rankings()` function
- [x] All quality and ranking tests passing

### Phase 4: Export & Integration
- [x] Implement `export_summary_report()` function
- [x] All export tests passing
- [ ] Integration tests with other modules

### Final Validation
- [x] All 30 tests passing
- [x] Code follows PEP 8 guidelines
- [x] Type hints added for all functions
- [x] Docstrings completed for all functions
- [ ] Performance validated with large datasets

---

## Summary

**Completion Date**: 2026-08-26
**Total Functions**: 6/6 ✅
**Total Tests**: 30/30 ✅
**Status**: 🎉 **FULLY IMPLEMENTED AND TESTED**