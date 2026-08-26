import argparse
import pandas as pd
from pathlib import Path

from .plots import temperature_timeline
from .report import write_report


def main():
    parser = argparse.ArgumentParser(description='Run data processing pipeline')
    parser.add_argument('--raw', required=True, help='Path to raw CSV file')
    parser.add_argument('--out', required=True, help='Output directory')
    args = parser.parse_args()

    # Load data
    df = pd.read_csv(args.raw)
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed', errors='coerce')
    df['humidity_pct'] = pd.to_numeric(df['humidity_pct'].str.replace(',', '.'), errors='coerce')

    # Create output directories
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    viz_dir = out_dir / 'visualizations'
    viz_dir.mkdir(parents=True, exist_ok=True)

    # Generate outputs
    plot_path = viz_dir / 'temperature_timeline.png'
    temperature_timeline(df, str(plot_path))

    report_path = out_dir / 'report.md'
    write_report(df, str(report_path))

    print(f"Pipeline complete. Outputs in {out_dir}")


if __name__ == '__main__':
    main()
