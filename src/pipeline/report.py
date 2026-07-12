"""Markdown report generation for the field-study pipeline."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from pipeline.stats import station_summary


def write_report(df: pd.DataFrame, out_path: str | Path, raw_count: int | None = None,
                 plot_name: str = "plot.png"):
    """Write a markdown report with row counts, per-station stats, and a plot link.

    ``df`` is the cleaned frame. ``raw_count`` is the number of rows before
    cleaning (optional). ``plot_name`` is the plot filename, linked relative to
    the report location.
    """
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    cleaned_count = len(df)
    summary = station_summary(df)

    lines = ["# Field Study Report", ""]
    lines.append("## Introduction")
    lines.append("")
    lines.append(
        f"This report summarizes the field-study measurements that were recorded "
        f"at {len(summary)} weather stations and exported to "
        f"`data/raw/measurements.csv`. It is generally the case that the raw "
        f"export arrives with mixed units and several different date formats, "
        f"so the pipeline cleans the readings before any statistic is computed: "
        f"temperatures are converted to °C, humidity values recorded as missing "
        f"are marked as missing rather than being counted as zero, and rows that "
        f"are exact duplicates of another row are dropped. What is shown below "
        f"is a per-station summary of temperature and humidity, followed by a "
        f"timeline plot of every cleaned reading."
    )
    lines.append("")
    lines.append("## Row counts")
    lines.append("")
    if raw_count is not None:
        lines.append(f"- Raw rows: {raw_count}")
        lines.append(f"- Cleaned rows: {cleaned_count}")
        lines.append(f"- Dropped (duplicates): {raw_count - cleaned_count}")
    else:
        lines.append(f"- Cleaned rows: {cleaned_count}")
    lines.append("")

    lines.append("## Per-station summary")
    lines.append("")
    lines.append("| station | temp_mean (°C) | temp_min (°C) | temp_max (°C) | hum_mean (%) |")
    lines.append("| --- | ---: | ---: | ---: | ---: |")
    for station, row in summary.iterrows():
        lines.append(
            f"| {station} | {row['temp_mean']:.2f} | {row['temp_min']:.2f} "
            f"| {row['temp_max']:.2f} | {row['hum_mean']:.2f} |"
        )
    lines.append("")

    lines.append("## Temperature timeline")
    lines.append("")
    lines.append(f"![Temperature timeline]({plot_name})")
    lines.append("")

    out_path.write_text("\n".join(lines))
    return out_path
