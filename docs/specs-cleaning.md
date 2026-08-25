# Spec: data loading and cleaning
Goal: load data/raw/measurements.csv into a clean table ready for analysis.
Module: src/pipeline/io.py, functions load_raw(path), clean(df).

## Acceptance criteria:
- [ ] all three timestamp formats parse into one datetime column
  - Formats: MM/DD/YYYY HH:MM AM/PM, YYYY-MM-DD HH:MM, DD.MM.YYYY HH:MM
- [ ] temperatures unified to °C (temp_unit column consulted using C = (F - 32) * 5/9, then column dropped)
- [ ] humidity: "", "n/a", -99 → missing (NaN); decimal commas parsed (e.g., "35,5" → 35.5)
- [ ] wind: "calm" → 0.0; column numeric (float)
- [ ] station names stripped of whitespace
- [ ] exact duplicate rows dropped; report how many (12 duplicates expected)
- [ ] column types: `timestamp` is `datetime64`; `temperature`, `humidity_pct`, `wind_ms` are `float`
- [ ] cleaned data saved to data/processed/cleaned_measurements.csv

## Implementation details:
- Package manager: **uv** (as per AGENTS.md)
- Create directory structure: src/pipeline/
- Add pandas dependency: `uv add pandas`
- clean() function returns: (cleaned DataFrame, summary_dict, summary_string)
- Refactor legacy_analysis.py to use load_raw() and clean()
- Ensure matplotlib is available via uv if needed for legacy_analysis.py

## Data observations (612 rows):
- Temperature units: 460 C, 152 F
- Humidity missing: 36 empty, 21 "n/a", 16 -99
- Wind "calm": 36 occurrences
- Station whitespace: at least 1 occurrence (" Charlie ")
- Duplicate rows: 12 exact duplicates

## Code quality requirements (diagnostics):
- [ ] All imports sorted and properly formatted
- [ ] All imports resolvable (no "could not be resolved" errors)
- [ ] Use context managers for file operations (no bare `open()`)
- [ ] No bare `except` clauses - use specific exception types
- [ ] All variables have known types (use type hints)
- [ ] No unused variables (use `_` for intentional unused)
- [ ] Use `list.copy()` instead of list concatenation where appropriate
- [ ] Consider logging exceptions instead of silent pass/continue

## Final validation:
- [ ] Run diagnostics on the project: should show 0 errors, minimal warnings
- [ ] Run `python legacy_analysis.py` without errors
- [ ] All output files generated correctly

Out of scope: statistics, plotting, the CLI.
