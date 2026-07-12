"""Plotting for the field-study pipeline."""
from __future__ import annotations

from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def temperature_timeline(df: pd.DataFrame, out_path: str | Path):
    """Plot one temperature line per station over time and save to out_path."""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    for station, group in df.groupby("station"):
        group = group.sort_values("timestamp")
        ax.plot(group["timestamp"], group["temperature"], label=station)

    ax.set_xlabel("Time")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Temperature over time by station")
    ax.legend(title="Station")
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)
    return out_path
