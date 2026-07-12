import pandas as pd
from pipeline.io import load_raw, clean


def test_na_humidity_becomes_nan(tmp_path):
    p = tmp_path / "m.csv"
    p.write_text(
        "reading_id,station,timestamp,temperature,temp_unit,humidity_pct,wind_ms\n"
        "R0001,Alpha,2025-03-01 06:00,12.0,C,n/a,3.0\n"
    )
    df = clean(load_raw(p))
    assert pd.isna(df.loc[0, "humidity_pct"])


def test_fahrenheit_converted_exactly(tmp_path):
    p = tmp_path / "m.csv"
    p.write_text(
        "reading_id,station,timestamp,temperature,temp_unit,humidity_pct,wind_ms\n"
        "R0001,Alpha,2025-03-01 06:00,53.6,F,50.0,3.0\n"
    )
    df = clean(load_raw(p))
    # (53.6 - 32) * 5 / 9 == 12.0
    assert df.loc[0, "temperature"] == 12.0


def test_negative99_humidity_becomes_nan(tmp_path):
    p = tmp_path / "m.csv"
    p.write_text(
        "reading_id,station,timestamp,temperature,temp_unit,humidity_pct,wind_ms\n"
        "R0001,Alpha,2025-03-01 06:00,12.0,C,-99,3.0\n"
    )
    df = clean(load_raw(p))
    assert pd.isna(df.loc[0, "humidity_pct"])


def test_empty_humidity_becomes_nan(tmp_path):
    p = tmp_path / "m.csv"
    p.write_text(
        "reading_id,station,timestamp,temperature,temp_unit,humidity_pct,wind_ms\n"
        "R0001,Alpha,2025-03-01 06:00,12.0,C,,3.0\n"
    )
    df = clean(load_raw(p))
    assert pd.isna(df.loc[0, "humidity_pct"])


def test_decimal_comma_humidity_parsed(tmp_path):
    p = tmp_path / "m.csv"
    p.write_text(
        "reading_id,station,timestamp,temperature,temp_unit,humidity_pct,wind_ms\n"
        'R0001,Alpha,2025-03-01 06:00,12.0,C,"35,5",3.0\n'
    )
    df = clean(load_raw(p))
    assert df.loc[0, "humidity_pct"] == 35.5


def test_wind_calm_becomes_zero(tmp_path):
    p = tmp_path / "m.csv"
    p.write_text(
        "reading_id,station,timestamp,temperature,temp_unit,humidity_pct,wind_ms\n"
        "R0001,Alpha,2025-03-01 06:00,12.0,C,50.0,calm\n"
    )
    df = clean(load_raw(p))
    assert df.loc[0, "wind_ms"] == 0.0


def test_station_whitespace_stripped(tmp_path):
    p = tmp_path / "m.csv"
    p.write_text(
        "reading_id,station,timestamp,temperature,temp_unit,humidity_pct,wind_ms\n"
        "R0001, Charlie ,2025-03-01 06:00,12.0,C,50.0,3.0\n"
    )
    df = clean(load_raw(p))
    assert df.loc[0, "station"] == "Charlie"


def test_exact_duplicate_rows_dropped(tmp_path):
    p = tmp_path / "m.csv"
    row = "R0001,Alpha,2025-03-01 06:00,12.0,C,50.0,3.0\n"
    p.write_text(
        "reading_id,station,timestamp,temperature,temp_unit,humidity_pct,wind_ms\n"
        + row
        + row
        + "R0002,Bravo,2025-03-01 07:00,13.0,C,55.0,4.0\n"
    )
    df = clean(load_raw(p))
    assert len(df) == 2


def test_all_three_timestamp_formats_parsed(tmp_path):
    p = tmp_path / "m.csv"
    p.write_text(
        "reading_id,station,timestamp,temperature,temp_unit,humidity_pct,wind_ms\n"
        "R0001,Alpha,2025-03-01 06:00,12.0,C,50.0,3.0\n"
        "R0002,Bravo,05.03.2025 22:30,13.0,C,55.0,4.0\n"
        "R0003,Charlie,03/05/2025 11:15 PM,14.0,C,60.0,5.0\n"
    )
    df = clean(load_raw(p))
    assert str(df["timestamp"].dtype).startswith("datetime64")
    assert df["timestamp"].notna().all()


def test_temp_unit_column_dropped(tmp_path):
    p = tmp_path / "m.csv"
    p.write_text(
        "reading_id,station,timestamp,temperature,temp_unit,humidity_pct,wind_ms\n"
        "R0001,Alpha,2025-03-01 06:00,12.0,C,50.0,3.0\n"
    )
    df = clean(load_raw(p))
    assert "temp_unit" not in df.columns
