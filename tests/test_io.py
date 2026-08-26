# tests/test_io.py
import pandas as pd
from pipeline.io import load_raw, clean

def test_na_humidity_becomes_nan(tmp_path):
    p = tmp_path / "m.csv"
    p.write_text(
        "reading_id,station,timestamp,temperature,temp_unit,humidity_pct,wind_ms\n"
        "R0001,Alpha,2025-03-01 06:00,12.0,C,n/a,3.0\n"
    )
    cleaned_df, _, _ = clean(load_raw(p))
    assert pd.isna(cleaned_df.loc[0, "humidity_pct"])
