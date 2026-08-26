import matplotlib.pyplot as plt
import pandas as pd


def temperature_timeline(df: pd.DataFrame, out_path: str) -> None:
    """Plot temperature over time with one line per station."""
    plt.figure(figsize=(10, 6))
    
    stations = df['station'].unique()
    for station in stations:
        station_data = df[df['station'] == station].sort_values('timestamp')
        plt.plot(
            station_data['timestamp'],
            station_data['temperature'],
            label=station,
            marker='o',
            linestyle='-'
        )
    
    plt.title('Temperature Timeline by Station')
    plt.xlabel('Timestamp')
    plt.ylabel('Temperature')
    plt.legend(title='Station')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
