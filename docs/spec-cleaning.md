# Spec: data loading and cleaning
Goal: load data/raw/measurements.csv into a clean table ready for analysis.
Module: src/pipeline/io.py — functions load_raw(path), clean(df).
Acceptance criteria:
- [ ] all three timestamp formats parse into one datetime column
- [ ] temperatures unified to °C (temp_unit column consulted, then dropped)
- [ ] humidity: "", "n/a", -99 → missing (NaN); decimal commas parsed
- [ ] wind: "calm" → 0.0; column numeric
- [ ] station names stripped of whitespace
- [ ] exact duplicate rows dropped; report how many
Out of scope: statistics, plotting, the CLI.

Extra acceptance criteria (added after reading the data in Lab 1):
- [ ] resulting column types are guaranteed: `timestamp` is `datetime64`,
      `temperature`, `humidity_pct`, and `wind_ms` are `float`
- [ ] the row index is reset to a contiguous 0..n-1 range after duplicates are
      dropped, so downstream `.loc` access by position is stable
