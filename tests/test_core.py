import pathlib

import pandas as pd

from gpx_explorer.core import parse_gpx_to_dataframe

DATA_DIR = pathlib.Path(__file__).with_suffix("").with_name("data")


def test_parse_single_track(tmp_path):
    df = parse_gpx_to_dataframe(DATA_DIR / "short_track.gpx")
    assert isinstance(df, pd.DataFrame)
    assert {"lat", "lon", "ele", "time"}.issubset(df.columns)
    # fastest point should be indexed correctly
    speed_col = df["speed_m_s"]
    assert speed_col.max() == speed_col.loc[df["speed_m_s"].idxmax()]
