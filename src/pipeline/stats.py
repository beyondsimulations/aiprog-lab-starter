import pandas as pd


def station_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Generate summary statistics per station."""
    return df.groupby('station').agg({
        'temperature': ['mean', 'min', 'max', 'count'],
        'humidity_pct': ['mean', 'min', 'max']
    }).round(2)
