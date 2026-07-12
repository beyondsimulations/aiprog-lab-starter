"""Command-line interface for the field-study pipeline."""
from __future__ import annotations

import argparse
from pathlib import Path

from pipeline.io import clean, load_raw
from pipeline.plots import temperature_timeline
from pipeline.report import write_report


def main(argv=None):
    parser = argparse.ArgumentParser(prog="pipeline")
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="Clean data, then write a plot and report.")
    run.add_argument("--raw", required=True, help="Path to the raw CSV.")
    run.add_argument("--out", required=True, help="Output directory.")

    args = parser.parse_args(argv)

    if args.command == "run":
        out_dir = Path(args.out)
        out_dir.mkdir(parents=True, exist_ok=True)

        raw = load_raw(args.raw)
        cleaned = clean(raw)

        plot_path = out_dir / "plot.png"
        temperature_timeline(cleaned, plot_path)

        report_path = out_dir / "report.md"
        write_report(cleaned, report_path, raw_count=len(raw),
                     plot_name=plot_path.name)

        print(f"Wrote {plot_path}")
        print(f"Wrote {report_path}")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
