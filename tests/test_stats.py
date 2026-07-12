import pandas as pd
from pipeline.stats import station_summary


def test_station_summary_means():
    df = pd.DataFrame({
        "station": ["Alpha", "Alpha", "Bravo"],
        "temperature": [10.0, 14.0, 20.0],
        "humidity_pct": [50.0, None, 80.0],
    })
    out = station_summary(df)
    assert out.loc["Alpha", "temp_mean"] == 12.0
    assert out.loc["Alpha", "temp_min"] == 10.0
    assert out.loc["Alpha", "hum_mean"] == 50.0
    assert out.loc["Bravo", "temp_max"] == 20.0
