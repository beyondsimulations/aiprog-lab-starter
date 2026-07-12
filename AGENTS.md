# AGENTS.md

Field-study data pipeline: clean raw weather-station measurements and produce summary stats, a plot, and a report.

- `data/raw/` is READ-ONLY. Never modify or overwrite files there.
- Use `uv` for everything (running code, tests, adding dependencies).
- Explain your changes before committing.

## Commands

- Run tests: `uv run pytest`
- Quick check: `uv run python -c "from pipeline.io import load_raw, clean; print(clean(load_raw('data/raw/measurements.csv')).dtypes)"`
- Add a dependency: `uv add <package>` (dev: `uv add --dev <package>`)

Loading and cleaning now live in `src/pipeline/io.py` (`load_raw`, `clean`); the
old `legacy_analysis.py` has been removed.
