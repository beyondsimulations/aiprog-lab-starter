# AGENTS.md

Teaching material for the **AI-Assisted Programming workshop** at HSU.

## Purpose
- `legacy_analysis.py`: Intentionally flawed script for refactoring exercises (hardcoded paths, redundant code)
- `data/raw/measurements.csv`: Sample field study data
- `capstone/`: Student projects

---

## Guidelines

### Code
- Preserve educational intent; keep changes incremental
- Follow PEP 8, use type hints, add docstrings
- Prefer modular functions over monolithic scripts
- Use `pathlib` for paths

### Data
- CSV has header row
- Column 3: Temperature (float, mixed C/F units)
- Column 5: Humidity (float, may use comma as decimal separator)
- Handle missing/invalid data gracefully

### Paths
- **Never** use absolute paths
- Use relative paths from project root (e.g., `data/raw/measurements.csv`)
- Save outputs to `data/processed/` or `data/visualizations/`

### Dependencies
- Package manager: **uv**
- Current: `csv`, `matplotlib` (Agg backend)
- Prefer standard library where possible
- Justify new dependencies for educational value

### Testing
- No formal test suite
- Validate by running script and checking output/plots
- Use print statements or assertions for new functionality
- **Always use `uv run python <script>` to execute Python scripts**

---

## Common Tasks

### Refactoring `legacy_analysis.py`
1. Replace hardcoded paths with relative paths
2. Extract repeated logic into functions
3. Add error handling
4. Use `pathlib` for path manipulation
5. Save outputs to `data/processed/` or `data/visualizations/`

### Adding Features
- Add new functions with docstrings
- Document data requirements
- Update this file with new assumptions

---

## Known Issues
- Legacy script mixes Celsius/Fahrenheit without conversion
- European decimal format (comma) not handled in humidity values
- Missing 2024 data referenced in TODO

---

## Validation
- Verify averages and plots match expected output
- Script must run without errors on fresh clone
