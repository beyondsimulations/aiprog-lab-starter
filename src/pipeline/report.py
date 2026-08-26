import pandas as pd
from pathlib import Path

from .stats import station_summary


def write_report(df: pd.DataFrame, out_path: str) -> None:
    """Write a markdown summary report."""
    lines = []
    
    # Introduction
    lines.append("# Data Report\n")
    lines.append(
        "This report summarizes environmental measurements collected from multiple "
        "monitoring stations. The data includes temperature and humidity readings "
        "taken at regular intervals. Below you will find key statistics and "
        "visualizations of the collected data.\n"
    )
    
    # Row counts
    lines.append(f"## Overview\n")
    lines.append(f"- **Total measurements**: {len(df)}\n")
    lines.append(f"- **Stations**: {df['station'].nunique()}\n")
    lines.append(f"- **Date range**: {df['timestamp'].min()} to {df['timestamp'].max()}\n")
    
    # Per-station table
    lines.append("\n## Station Statistics\n")
    summary = station_summary(df)
    lines.append(summary.to_markdown())
    
    # Plot link
    lines.append("\n## Visualization")
    lines.append("- [Temperature Timeline](./visualizations/temperature_timeline.png)\n")
    
    Path(out_path).write_text(''.join(lines))
