# Statistics Module Specification

## Overview

The `pipeline.stats` module provides statistical analysis functions for weather station measurement data. This specification defines the functionality, inputs, outputs, and edge cases for all statistical functions in the module.

**Status**: 🟡 In Development (TDD Approach)

---

## Module Purpose

Compute comprehensive summary statistics and analytical insights from cleaned weather station data, supporting:

- [ ] Basic descriptive statistics (mean, max, min, count, std)
- [ ] Time-based aggregations (daily, monthly, yearly)
- [ ] Station comparisons and rankings
- [ ] Data quality metrics
- [ ] Exportable reports

---

## Functions

### 1. `station_summary(df: pd.DataFrame) -> pd.DataFrame`

**Purpose**: Compute summary statistics for each weather station.

**Status**: ⬜ Not Started

**Inputs**:
- [ ] `df`: DataFrame containing weather station data with required columns:
  - [ ] `station`: Station identifier (str)
  - [ ] `temperature`: Temperature values (numeric or string)
  - [ ] `humidity_pct`: Humidity percentage values (numeric or string)
  - [ ] Optional: `timestamp`, `wind_ms`, `pressure_hpa` (ignored if present)

**Outputs**:
- [ ] DataFrame indexed by station name with columns:
  - [ ] Temperature statistics:
    - [ ] `temp_mean`: Mean temperature (°C)
    - [ ] `temp_max`: Maximum temperature (°C)
    - [ ] `temp_min`: Minimum temperature (°C)
    - [ ] `temp_std`: Standard deviation of temperature (°C)
    - [ ] `temp_count`: Number of valid temperature readings
  - [ ] Humidity statistics:
    - [ ] `hum_mean`: Mean humidity (%)
    - [ ] `hum_max`: Maximum humidity (%)
    - [ ] `hum_min`: Minimum humidity (%)
    - [ ] `hum_std`: Standard deviation of humidity (%)
    - [ ] `hum_count`: Number of valid humidity readings

**Behavior**:
- [ ] Automatically converts string columns to numeric (coerces errors to NaN)
- [ ] Handles missing/NaN values gracefully
- [ ] Does not modify the original DataFrame
- [ ] Preserves station name case and whitespace
- [ ] Returns empty DataFrame with correct columns if input is empty

**Edge Cases**:
- [ ] Empty DataFrame → Returns empty DataFrame with expected columns
- [ ] Single station → Returns single-row DataFrame
- [ ] All NaN values for a column → Returns NaN for statistics, 0 for count
- [ ] Mixed valid/invalid values → Uses only valid values for calculations
- [ ] String representations of numbers → Converts to numeric

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

**Status**: ⬜ Not Started

**Inputs**:
- [ ] `df`: DataFrame with required columns:
  - [ ] `timestamp`: Datetime column
  - [ ] `station`: Station identifier
  - [ ] `temperature`: Temperature values
  - [ ] `humidity_pct`: Humidity percentage values

**Outputs**:
- [ ] DataFrame indexed by date with columns:
  - [ ] `temp_mean`: Mean temperature across all stations
  - [ ] `temp_max`: Maximum temperature across all stations
  - [ ] `temp_min`: Minimum temperature across all stations
  - [ ] `hum_mean`: Mean humidity across all stations
  - [ ] `hum_max`: Maximum humidity across all stations
  - [ ] `hum_min`: Minimum humidity across all stations
  - [ ] `station_count`: Number of stations reporting that day
  - [ ] `reading_count`: Total number of readings that day

**Behavior**:
- [ ] Groups data by date (ignoring time component)
- [ ] Computes statistics across all stations for each day
- [ ] Handles missing dates (no data for a day = no row in output)

**Tests**:
- [x] Test basic daily summary functionality
- [x] Test daily summary with empty DataFrame
- [x] Test error handling when required columns are missing

---

### 3. `station_daily_summary(df: pd.DataFrame) -> pd.DataFrame`

**Purpose**: Compute daily summary statistics for each station (pivot table).

**Status**: ⬜ Not Started

**Inputs**:
- [ ] Same as `daily_summary`

**Outputs**:
- [ ] Multi-index DataFrame with:
  - [ ] Index level 0: Station name
  - [ ] Index level 1: Date
  - [ ] Columns: Same statistics as `station_summary` but for each day

**Behavior**:
- [ ] Creates a pivot-style summary with stations as rows and dates as columns
- [ ] Facilitates station comparison over time

**Tests**:
- [x] Test basic station daily summary functionality
- [x] Test station daily summary with empty DataFrame

---

### 4. `data_quality_report(df: pd.DataFrame) -> dict`

**Purpose**: Generate a data quality report for the dataset.

**Status**: ⬜ Not Started

**Inputs**:
- [ ] `df`: DataFrame with weather station data

**Outputs**:
- [ ] Dictionary containing:
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
- [ ] Defines outliers as values outside reasonable ranges:
  - [ ] Temperature: < -50°C or > 60°C
  - [ ] Humidity: < 0% or > 100%
- [ ] Calculates data completeness as percentage of non-null values
- [ ] Identifies most and least active stations

**Tests**:
- [x] Test basic data quality report functionality
- [x] Test outlier detection in quality report
- [x] Test station activity metrics in quality report
- [x] Test quality report with empty DataFrame

---

### 5. `station_rankings(df: pd.DataFrame, metric: str = "temp_mean", ascending: bool = False) -> pd.DataFrame`

**Purpose**: Rank stations by a specific metric.

**Status**: ⬜ Not Started

**Inputs**:
- [ ] `df`: DataFrame with weather station data
- [ ] `metric`: Metric to rank by (default: "temp_mean")
  - [ ] Valid metrics: any column from `station_summary` output
- [ ] `ascending`: Sort order (default: False = highest first)

**Outputs**:
- [ ] DataFrame with stations ranked by the specified metric, containing:
  - [ ] All columns from `station_summary`
  - [ ] Additional `rank` column with ranking (1 = highest/lowest depending on `ascending`)

**Behavior**:
- [ ] Uses `station_summary` internally to get statistics
- [ ] Handles ties by assigning same rank, then skipping next rank(s)
- [ ] Example: ranks 1, 1, 3 for tied first place

**Tests**:
- [x] Test basic station rankings functionality
- [x] Test ascending rankings
- [x] Test handling of tied values in rankings
- [x] Test error handling for invalid metric
- [x] Test rankings with empty DataFrame

---

### 6. `export_summary_report(df: pd.DataFrame, output_path: str | Path, format: str = "csv") -> Path`

**Purpose**: Export a comprehensive summary report to file.

**Status**: ⬜ Not Started

**Inputs**:
- [ ] `df`: DataFrame with weather station data
- [ ] `output_path`: Path for the output file
- [ ] `format`: Output format ("csv", "json", "excel")

**Outputs**:
- [ ] Path to the created file

**Behavior**:
- [ ] Creates a comprehensive report including:
  - [ ] Overall statistics
  - [ ] Station summaries
  - [ ] Data quality metrics
  - [ ] Station rankings
- [ ] Saves to the specified format
- [ ] Creates parent directories if they don't exist
- [ ] Validates output path is within project directory

**Tests**:
- [x] Test exporting summary report to CSV
- [x] Test exporting summary report to JSON
- [x] Test error handling for invalid format
- [x] Test that parent directories are created if they don't exist

---

## Data Assumptions

- [ ] **Temperature**: Values in Celsius (°C), numeric
- [ ] **Humidity**: Values as percentage (0-100), numeric
- [ ] **Station Names**: String identifiers, may contain spaces/special characters
- [ ] **Timestamps**: Datetime objects or parseable strings
- [ ] **Missing Values**: Represented as NaN, None, or empty strings

## Error Handling

- [ ] **Missing Required Columns**: Raise `ValueError` with descriptive message
- [ ] **Invalid Data Types**: Attempt conversion, raise `TypeError` if impossible
- [ ] **Empty DataFrame**: Return appropriate empty structure (not an error)
- [ ] **Invalid Output Paths**: Raise `ValueError` for paths outside project root

## Dependencies

- [ ] `pandas` for DataFrame operations
- [ ] `pathlib` for path manipulation
- [ ] Standard library only (no additional dependencies)

## Testing Requirements

- [ ] Each function must have comprehensive test coverage including:
  - [ ] Basic functionality tests
  - [ ] Edge case tests (empty, single value, all NaN)
  - [ ] Error handling tests
  - [ ] Data type conversion tests
  - [ ] Side effect tests (original DataFrame unchanged)
  - [ ] Performance tests for large datasets (>10,000 rows)

---

## Implementation Checklist

### Phase 1: Core Functionality
- [ ] Implement `station_summary()` function
- [ ] All `TestStationSummary` tests passing

### Phase 2: Time-based Analysis
- [ ] Implement `daily_summary()` function
- [ ] Implement `station_daily_summary()` function
- [ ] All daily summary tests passing

### Phase 3: Quality & Rankings
- [ ] Implement `data_quality_report()` function
- [ ] Implement `station_rankings()` function
- [ ] All quality and ranking tests passing

### Phase 4: Export & Integration
- [ ] Implement `export_summary_report()` function
- [ ] All export tests passing
- [ ] Integration tests with other modules

### Final Validation
- [ ] All 28 tests passing
- [ ] Code follows PEP 8 guidelines
- [ ] Type hints added for all functions
- [ ] Docstrings completed for all functions
- [ ] Performance validated with large datasets